# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ReviewRequest(models.Model):
    """Demande d'avis client"""
    _name = 'eazynova.review.request'
    _description = 'Demande d\'Avis Client'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        readonly=True,
        default='Nouveau'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True,
        ondelete='restrict'
    )

    partner_email = fields.Char(
        string='Email',
        related='partner_id.email',
        store=True
    )

    partner_phone = fields.Char(
        string='Téléphone',
        related='partner_id.phone'
    )

    invoice_id = fields.Many2one(
        'account.move',
        string='Facture',
        domain=[('move_type', '=', 'out_invoice')],
        tracking=True
    )

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Commande',
        tracking=True
    )

    request_date = fields.Datetime(
        string='Date de demande',
        default=fields.Datetime.now,
        required=True,
        tracking=True
    )

    send_date = fields.Datetime(
        string='Date d\'envoi',
        readonly=True,
        tracking=True
    )

    reminder_date = fields.Datetime(
        string='Date de relance',
        tracking=True
    )

    expiry_date = fields.Date(
        string='Date d\'expiration',
        compute='_compute_expiry_date',
        store=True
    )

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('pending', 'En attente'),
        ('sent', 'Envoyée'),
        ('reminded', 'Relancée'),
        ('completed', 'Complétée'),
        ('expired', 'Expirée'),
        ('cancelled', 'Annulée')
    ], string='État', default='draft', required=True, tracking=True)

    review_id = fields.Many2one(
        'eazynova.customer.review',
        string='Avis reçu',
        readonly=True
    )

    platform = fields.Selection([
        ('trustpilot', 'Trustpilot'),
        ('google', 'Google Reviews'),
        ('internal', 'Avis Interne')
    ], string='Plateforme', default='trustpilot', required=True)

    review_link = fields.Char(
        string='Lien vers avis',
        compute='_compute_review_link'
    )

    notes = fields.Text(
        string='Notes'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user,
        tracking=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Génère la référence automatiquement"""
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('eazynova.review.request') or 'Nouveau'
        return super().create(vals_list)

    @api.depends('request_date')
    def _compute_expiry_date(self):
        """Calcule la date d'expiration (30 jours après la demande)"""
        for request in self:
            if request.request_date:
                request.expiry_date = fields.Date.add(
                    request.request_date.date(),
                    days=30
                )
            else:
                request.expiry_date = False

    @api.depends('platform', 'partner_id')
    def _compute_review_link(self):
        """Génère le lien vers la plateforme d'avis"""
        config = self.env['eazynova.trust.config'].sudo().search([], limit=1)

        for request in self:
            if request.platform == 'trustpilot' and config.trustpilot_review_url:
                request.review_link = config.trustpilot_review_url
            elif request.platform == 'google' and config.google_review_url:
                request.review_link = config.google_review_url
            else:
                # Lien vers formulaire interne
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                request.review_link = f"{base_url}/review/submit/{request.id}"

    def action_send_request(self):
        """Envoie la demande d'avis par email"""
        self.ensure_one()

        if not self.partner_email:
            raise UserError('Le client n\'a pas d\'adresse email configurée.')

        # Récupérer le template email
        template = self.env.ref('eazynova_trust.email_template_review_request', raise_if_not_found=False)

        if not template:
            raise UserError('Template d\'email non trouvé.')

        # Envoyer l'email
        template.send_mail(self.id, force_send=True)

        # Mettre à jour l'état
        self.write({
            'state': 'sent',
            'send_date': fields.Datetime.now()
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': f'Demande d\'avis envoyée à {self.partner_id.name}',
                'type': 'success',
            }
        }

    def action_send_reminder(self):
        """Envoie une relance"""
        self.ensure_one()

        if self.state not in ['sent', 'reminded']:
            raise UserError('Seules les demandes envoyées peuvent être relancées.')

        # Récupérer le template de relance
        template = self.env.ref('eazynova_trust.email_template_review_reminder', raise_if_not_found=False)

        if template:
            template.send_mail(self.id, force_send=True)

        self.write({
            'state': 'reminded',
            'reminder_date': fields.Datetime.now()
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': 'Relance envoyée',
                'type': 'success',
            }
        }

    def action_mark_completed(self):
        """Marque la demande comme complétée"""
        self.write({'state': 'completed'})

    def action_cancel(self):
        """Annule la demande"""
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        """Remet en brouillon"""
        self.write({'state': 'draft'})

    def cron_check_expired_requests(self):
        """Marque les demandes expirées"""
        expired_requests = self.search([
            ('state', 'in', ['sent', 'reminded']),
            ('expiry_date', '<', fields.Date.today())
        ])
        expired_requests.write({'state': 'expired'})

    def cron_send_auto_reminders(self):
        """Envoie automatiquement les relances"""
        # Relancer après 14 jours sans réponse
        reminder_date = fields.Datetime.subtract(fields.Datetime.now(), days=14)

        requests_to_remind = self.search([
            ('state', '=', 'sent'),
            ('send_date', '<=', reminder_date),
            ('reminder_date', '=', False)
        ])

        for request in requests_to_remind:
            try:
                request.action_send_reminder()
            except Exception as e:
                _logger.error(f"Erreur lors de l'envoi de la relance pour {request.name}: {str(e)}")
