# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class EazynovaChantier(models.Model):
    """
    Modèle principal pour la gestion de chantiers
    Représente un chantier de construction avec toutes ses caractéristiques
    """
    _name = 'eazynova.chantier'
    _description = 'Chantier de Construction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, name'
    
    # === INFORMATIONS DE BASE ===
    name = fields.Char(
        string="Nom du chantier",
        required=True,
        tracking=True,
        help="Nom complet du chantier"
    )
    
    code = fields.Char(
        string="Code",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Code unique du chantier (auto-généré)"
    )
    
    reference_client = fields.Char(
        string="Référence client",
        tracking=True,
        help="Référence du client pour ce chantier"
    )
    
    # === STATUT ===
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('in_progress', 'En cours'),
        ('suspended', 'Suspendu'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string="État",
       default='draft',
       required=True,
       tracking=True,
       help="État actuel du chantier"
    )
    
    priority = fields.Selection([
        ('0', 'Normale'),
        ('1', 'Importante'),
        ('2', 'Urgente'),
        ('3', 'Critique'),
    ], string="Priorité",
       default='0',
       tracking=True
    )
    
    # === DATES ===
    date_start = fields.Date(
        string="Date de début",
        required=True,
        tracking=True,
        help="Date prévue de début des travaux"
    )
    
    date_end = fields.Date(
        string="Date de fin prévue",
        required=True,
        tracking=True,
        help="Date prévue de fin des travaux"
    )
    
    date_end_real = fields.Date(
        string="Date de fin réelle",
        readonly=True,
        tracking=True,
        help="Date réelle de fin des travaux"
    )
    
    # === CLIENT & CONTACT ===
    partner_id = fields.Many2one(
        'res.partner',
        string="Client",
        required=True,
        tracking=True,
        domain=[('customer_rank', '>', 0)],
        help="Client principal du chantier"
    )
    
    partner_address_id = fields.Many2one(
        'res.partner',
        string="Adresse du chantier",
        tracking=True,
        help="Adresse où se situe le chantier"
    )
    
    contact_ids = fields.Many2many(
        'res.partner',
        string="Contacts",
        domain=[('is_company', '=', False)],
        help="Contacts associés au chantier"
    )
    
    # === LOCALISATION GPS ===
    gps_latitude = fields.Float(
        string="Latitude",
        digits=(10, 7),
        help="Coordonnée GPS - Latitude"
    )
    
    gps_longitude = fields.Float(
        string="Longitude",
        digits=(10, 7),
        help="Coordonnée GPS - Longitude"
    )
    
    # === ÉQUIPE & RESPONSABLES ===
    user_id = fields.Many2one(
        'res.users',
        string="Chef de chantier",
        required=True,
        default=lambda self: self.env.user,
        tracking=True,
        help="Responsable principal du chantier"
    )
    
    equipe_ids = fields.One2many(
        'eazynova.chantier.equipe',
        'chantier_id',
        string="Équipes",
        help="Équipes affectées au chantier"
    )
    
    # === PHASES & TÂCHES ===
    phase_ids = fields.One2many(
        'eazynova.chantier.phase',
        'chantier_id',
        string="Phases",
        help="Phases du chantier"
    )
    
    tache_ids = fields.One2many(
        'eazynova.chantier.tache',
        'chantier_id',
        string="Tâches",
        help="Tâches du chantier"
    )
    
    # === BUDGET ===
    budget_previsionnel = fields.Monetary(
        string="Budget prévisionnel",
        currency_field='currency_id',
        tracking=True,
        help="Budget total prévu pour le chantier"
    )
    
    budget_consomme = fields.Monetary(
        string="Budget consommé",
        compute='_compute_budget',
        store=True,
        currency_field='currency_id',
        help="Budget réellement consommé"
    )
    
    budget_restant = fields.Monetary(
        string="Budget restant",
        compute='_compute_budget',
        store=True,
        currency_field='currency_id',
        help="Budget restant disponible"
    )
    
    taux_consommation = fields.Float(
        string="Taux de consommation (%)",
        compute='_compute_budget',
        store=True,
        help="Pourcentage du budget consommé"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string="Devise",
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    # === AVANCEMENT ===
    progress = fields.Float(
        string="Avancement (%)",
        compute='_compute_progress',
        store=True,
        help="Pourcentage d'avancement du chantier"
    )
    
    # === FACTURATION ===
    invoice_ids = fields.One2many(
        'account.move',
        'chantier_id',
        string="Factures",
        domain=[('move_type', '=', 'out_invoice')],
        help="Factures clients liées au chantier"
    )
    
    invoice_count = fields.Integer(
        string="Nombre de factures",
        compute='_compute_invoice_count'
    )
    
    # === DOCUMENTS ===
    attachment_count = fields.Integer(
        string="Nombre de documents",
        compute='_compute_attachment_count'
    )
    
    # === SOCIÉTÉ ===
    company_id = fields.Many2one(
        'res.company',
        string="Société",
        required=True,
        default=lambda self: self.env.company
    )
    
    # === NOTES ===
    description = fields.Html(
        string="Description",
        help="Description détaillée du chantier"
    )
    
    note = fields.Text(
        string="Notes internes",
        help="Notes internes (non visibles par le client)"
    )
    
    # === CONTRAINTES SQL ===
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Le code du chantier doit être unique !'),
        ('check_dates', 'CHECK(date_end >= date_start)', 'La date de fin doit être postérieure à la date de début !'),
        ('check_budget', 'CHECK(budget_previsionnel >= 0)', 'Le budget doit être positif !'),
    ]
    
    # === MÉTHODES COMPUTE ===
    
    @api.depends('phase_ids.progress')
    def _compute_progress(self):
        """Calcule l'avancement global du chantier"""
        for chantier in self:
            if chantier.phase_ids:
                chantier.progress = sum(chantier.phase_ids.mapped('progress')) / len(chantier.phase_ids)
            else:
                chantier.progress = 0.0
    
    @api.depends('budget_previsionnel', 'invoice_ids.amount_total')
    def _compute_budget(self):
        """Calcule les indicateurs budgétaires"""
        for chantier in self:
            # Budget consommé = somme des factures
            chantier.budget_consomme = sum(chantier.invoice_ids.filtered(
                lambda inv: inv.state == 'posted'
            ).mapped('amount_total'))
            
            # Budget restant
            chantier.budget_restant = chantier.budget_previsionnel - chantier.budget_consomme
            
            # Taux de consommation
            if chantier.budget_previsionnel > 0:
                chantier.taux_consommation = (chantier.budget_consomme / chantier.budget_previsionnel) * 100
            else:
                chantier.taux_consommation = 0.0
    
    def _compute_invoice_count(self):
        """Compte le nombre de factures"""
        for chantier in self:
            chantier.invoice_count = len(chantier.invoice_ids)
    
    def _compute_attachment_count(self):
        """Compte le nombre de documents attachés"""
        for chantier in self:
            chantier.attachment_count = self.env['ir.attachment'].search_count([
                ('res_model', '=', self._name),
                ('res_id', '=', chantier.id)
            ])
    
    # === MÉTHODES CRUD ===
    
    @api.model
    def create(self, vals):
        """Génère automatiquement le code du chantier"""
        if vals.get('code', _('Nouveau')) == _('Nouveau'):
            vals['code'] = self.env['ir.sequence'].next_by_code('eazynova.chantier') or _('Nouveau')
        return super(EazynovaChantier, self).create(vals)
    
    # === ACTIONS ===
    
    def action_confirm(self):
        """Confirme le chantier"""
        for chantier in self:
            if chantier.state == 'draft':
                chantier.write({'state': 'confirmed'})
                chantier.message_post(body=_("Chantier confirmé"))
    
    def action_start(self):
        """Démarre le chantier"""
        for chantier in self:
            if chantier.state in ('draft', 'confirmed'):
                chantier.write({'state': 'in_progress'})
                chantier.message_post(body=_("Chantier démarré"))
    
    def action_suspend(self):
        """Suspend le chantier"""
        for chantier in self:
            if chantier.state == 'in_progress':
                chantier.write({'state': 'suspended'})
                chantier.message_post(body=_("Chantier suspendu"))
    
    def action_resume(self):
        """Reprend le chantier"""
        for chantier in self:
            if chantier.state == 'suspended':
                chantier.write({'state': 'in_progress'})
                chantier.message_post(body=_("Chantier repris"))
    
    def action_done(self):
        """Termine le chantier"""
        for chantier in self:
            if chantier.state == 'in_progress':
                chantier.write({
                    'state': 'done',
                    'date_end_real': fields.Date.today()
                })
                chantier.message_post(body=_("Chantier terminé"))
    
    def action_cancel(self):
        """Annule le chantier"""
        for chantier in self:
            if chantier.state not in ('done', 'cancelled'):
                chantier.write({'state': 'cancelled'})
                chantier.message_post(body=_("Chantier annulé"))
    
    def action_view_invoices(self):
        """Affiche les factures du chantier"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Factures'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('chantier_id', '=', self.id)],
            'context': {
                'default_chantier_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_move_type': 'out_invoice',
            }
        }
    
    def action_view_attachments(self):
        """Affiche les documents du chantier"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Documents'),
            'res_model': 'ir.attachment',
            'view_mode': 'tree,form',
            'domain': [
                ('res_model', '=', self._name),
                ('res_id', '=', self.id)
            ],
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            }
        }
    
    def action_open_map(self):
        """Ouvre la carte avec la localisation GPS"""
        self.ensure_one()
        if not self.gps_latitude or not self.gps_longitude:
            raise UserError(_("Aucune coordonnée GPS définie pour ce chantier."))
        
        # URL Google Maps
        url = f"https://www.google.com/maps/search/?api=1&query={self.gps_latitude},{self.gps_longitude}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
        