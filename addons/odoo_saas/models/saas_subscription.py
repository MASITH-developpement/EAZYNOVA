# -*- coding: utf-8 -*-
"""
Modèle de gestion des abonnements SaaS
"""

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class SaasSubscription(models.Model):
    """Abonnements SaaS"""
    _name = 'saas.subscription'
    _description = 'Abonnement SaaS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # === INFORMATIONS DE BASE ===
    name = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
        help="Référence unique de l'abonnement"
    )

    client_id = fields.Many2one(
        comodel_name='saas.client',
        string='Client',
        required=True,
        ondelete='restrict',
        tracking=True,
        help="Client concerné par l'abonnement"
    )

    plan_id = fields.Many2one(
        comodel_name='saas.plan',
        string='Plan',
        required=True,
        ondelete='restrict',
        tracking=True,
        help="Plan d'abonnement souscrit"
    )

    # === PÉRIODE ===
    start_date = fields.Date(
        string='Date de Début',
        required=True,
        default=fields.Date.today,
        tracking=True,
        help="Date de début de l'abonnement"
    )

    end_date = fields.Date(
        string='Date de Fin',
        required=True,
        tracking=True,
        help="Date de fin de l'abonnement"
    )

    duration = fields.Selection([
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ], string='Durée', required=True, default='monthly', tracking=True)

    days_remaining = fields.Integer(
        string='Jours Restants',
        compute='_compute_days_remaining',
        help="Nombre de jours avant expiration"
    )

    # === ÉTAT ===
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('cancelled', 'Annulé')
    ], string='État', default='draft', required=True, tracking=True)

    auto_renew = fields.Boolean(
        string='Renouvellement Automatique',
        default=True,
        tracking=True,
        help="Renouveler automatiquement à l'expiration"
    )

    # === TARIFICATION ===
    price = fields.Float(
        string='Prix (€)',
        compute='_compute_price',
        store=True,
        help="Prix de l'abonnement selon la durée"
    )

    # === NOTES ===
    notes = fields.Text(
        string='Notes',
        help="Notes sur l'abonnement"
    )

    # === CONTRAINTES SQL ===
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'La référence doit être unique !'),
        ('dates_check', 'CHECK(end_date > start_date)',
         'La date de fin doit être après la date de début !'),
    ]

    # === MÉTHODES COMPUTE ===
    @api.depends('plan_id', 'duration')
    def _compute_price(self):
        """Calcule le prix selon le plan et la durée"""
        for record in self:
            if record.plan_id:
                if record.duration == 'yearly':
                    record.price = record.plan_id.price_yearly
                else:
                    record.price = record.plan_id.price_monthly
            else:
                record.price = 0.0

    @api.depends('end_date')
    def _compute_days_remaining(self):
        """Calcule les jours restants"""
        today = fields.Date.today()
        for record in self:
            if record.end_date:
                delta = record.end_date - today
                record.days_remaining = delta.days
            else:
                record.days_remaining = 0

    # === MÉTHODES ONCHANGE ===
    @api.onchange('start_date', 'duration')
    def _onchange_duration(self):
        """Calcule la date de fin selon la durée"""
        if self.start_date and self.duration:
            if self.duration == 'yearly':
                self.end_date = self.start_date + relativedelta(years=1)
            else:
                self.end_date = self.start_date + relativedelta(months=1)

    # === MÉTHODES CREATE ===
    @api.model_create_multi
    def create(self, vals_list):
        """Création avec génération de référence"""
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'saas.subscription') or _('Nouveau')

        return super(SaasSubscription, self).create(vals_list)

    # === ACTIONS MÉTIER ===
    def action_activate(self):
        """Active l'abonnement"""
        self.ensure_one()

        if self.state == 'active':
            raise UserError(_('Cet abonnement est déjà actif !'))

        self.write({
            'state': 'active',
            'start_date': fields.Date.today(),
        })

        # Mettre à jour le client
        if self.client_id:
            self.client_id.write({
                'plan_id': self.plan_id.id,
                'expiration_date': fields.Datetime.from_string(str(self.end_date)),
            })

        _logger.info(f'Abonnement {self.name} activé')

        return True

    def action_renew(self):
        """Renouvelle l'abonnement"""
        self.ensure_one()

        if self.state != 'active':
            raise UserError(
                _('Seul un abonnement actif peut être renouvelé !'))

        new_start = self.end_date + relativedelta(days=1)
        if self.duration == 'yearly':
            new_end = new_start + relativedelta(years=1)
        else:
            new_end = new_start + relativedelta(months=1)

        self.write({
            'start_date': new_start,
            'end_date': new_end,
        })

        _logger.info(f'Abonnement {self.name} renouvelé jusqu\'au {new_end}')

        return True

    def action_cancel(self):
        """Annule l'abonnement"""
        self.ensure_one()

        self.state = 'cancelled'
        _logger.warning(f'Abonnement {self.name} annulé')

        return True

    def check_expiration(self):
        """Cron : Vérifier les abonnements expirés"""
        today = fields.Date.today()
        expired_subs = self.search([
            ('state', '=', 'active'),
            ('end_date', '<', today)
        ])

        for sub in expired_subs:
            if sub.auto_renew:
                sub.action_renew()
            else:
                sub.state = 'expired'
                if sub.client_id:
                    sub.client_id.action_suspend()

        _logger.info(
            f'{len(expired_subs)} abonnements traités pour expiration')
