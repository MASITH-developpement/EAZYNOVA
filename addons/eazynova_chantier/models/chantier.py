# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class EazynovaChantier(models.Model):
    """
    Modèle principal pour la gestion des chantiers
    Un chantier représente un projet de construction/travaux
    """
    _name = 'eazynova.chantier'
    _description = 'Chantier EAZYNOVA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, name'
    
    # Informations de base
    name = fields.Char(
        string="Nom du chantier",
        required=True,
        tracking=True,
        help="Nom descriptif du chantier"
    )
    
    reference = fields.Char(
        string="Référence",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
        help="Référence unique du chantier"
    )
    
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
        ('0', 'Normal'),
        ('1', 'Élevée'),
        ('2', 'Urgente'),
    ], string="Priorité",
       default='0',
       tracking=True
    )
    
    # Dates
    date_start = fields.Date(
        string="Date de début",
        required=True,
        default=fields.Date.today,
        tracking=True,
        help="Date prévue de démarrage du chantier"
    )
    
    date_end = fields.Date(
        string="Date de fin prévue",
        required=True,
        tracking=True,
        help="Date prévue de fin du chantier"
    )
    
    date_end_real = fields.Date(
        string="Date de fin réelle",
        readonly=True,
        tracking=True,
        help="Date réelle de fin du chantier"
    )
    
    duration_days = fields.Integer(
        string="Durée (jours)",
        compute='_compute_duration',
        store=True,
        help="Durée prévue du chantier en jours"
    )
    
    # Relations
    company_id = fields.Many2one(
        'res.company',
        string="Société",
        required=True,
        default=lambda self: self.env.company,
        help="Société propriétaire du chantier"
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string="Client",
        required=True,
        tracking=True,
        help="Client pour lequel le chantier est réalisé"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string="Chef de chantier",
        tracking=True,
        default=lambda self: self.env.user,
        help="Responsable principal du chantier"
    )
    
    team_ids = fields.Many2many(
        'hr.employee',
        string="Équipe",
        help="Équipe affectée au chantier"
    )
    
    # Localisation
    address = fields.Char(
        string="Adresse du chantier",
        required=True,
        tracking=True
    )
    
    address_city = fields.Char(
        string="Ville"
    )
    
    address_zip = fields.Char(
        string="Code postal"
    )
    
    address_latitude = fields.Float(
        string="Latitude",
        digits=(10, 7),
        help="Coordonnées GPS - Latitude"
    )
    
    address_longitude = fields.Float(
        string="Longitude",
        digits=(10, 7),
        help="Coordonnées GPS - Longitude"
    )
    
    # Budget et facturation
    budget_planned = fields.Monetary(
        string="Budget prévisionnel",
        currency_field='currency_id',
        tracking=True,
        help="Budget initial prévu pour le chantier"
    )
    
    budget_spent = fields.Monetary(
        string="Budget dépensé",
        currency_field='currency_id',
        compute='_compute_budget_spent',
        store=True,
        help="Montant total des dépenses engagées"
    )
    
    budget_remaining = fields.Monetary(
        string="Budget restant",
        currency_field='currency_id',
        compute='_compute_budget_remaining',
        store=True,
        help="Budget restant = Budget prévisionnel - Budget dépensé"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string="Devise",
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    # Tâches et progression
    task_ids = fields.One2many(
        'eazynova.chantier.task',
        'chantier_id',
        string="Tâches"
    )
    
    task_count = fields.Integer(
        string="Nombre de tâches",
        compute='_compute_task_count'
    )
    
    progress = fields.Float(
        string="Progression (%)",
        compute='_compute_progress',
        store=True,
        help="Pourcentage de progression du chantier"
    )
    
    # Documents
    document_ids = fields.One2many(
        'eazynova.chantier.document',
        'chantier_id',
        string="Documents"
    )
    
    document_count = fields.Integer(
        string="Nombre de documents",
        compute='_compute_document_count'
    )
    
    # Factures (relation avec module facture)
    invoice_ids = fields.One2many(
        'eazynova.facture',
        'chantier_id',
        string="Factures"
    )
    
    invoice_count = fields.Integer(
        string="Nombre de factures",
        compute='_compute_invoice_count'
    )
    
    # Notes
    description = fields.Html(
        string="Description",
        help="Description détaillée du chantier"
    )
    
    notes = fields.Text(
        string="Notes internes"
    )
    
    # Tags
    tag_ids = fields.Many2many(
        'eazynova.chantier.tag',
        string="Étiquettes"
    )
    
    # Couleur pour vue Kanban
    color = fields.Integer(
        string="Couleur",
        default=0
    )
    
    # IA et automatisation
    ai_suggestions = fields.Text(
        string="Suggestions IA",
        readonly=True,
        help="Suggestions générées par l'IA"
    )
    
    @api.model
    def create(self, vals):
        """
        Génère automatiquement la référence du chantier à la création
        Format: CHANT/YYYY/XXXXX
        """
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('eazynova.chantier') or _('Nouveau')
        return super(EazynovaChantier, self).create(vals)
    
    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        """
        Calcule la durée du chantier en jours
        """
        for chantier in self:
            if chantier.date_start and chantier.date_end:
                delta = chantier.date_end - chantier.date_start
                chantier.duration_days = delta.days + 1
            else:
                chantier.duration_days = 0
    
    @api.depends('task_ids.cost')
    def _compute_budget_spent(self):
        """
        Calcule le budget dépensé en sommant les coûts des tâches
        """
        for chantier in self:
            chantier.budget_spent = sum(chantier.task_ids.mapped('cost'))
    
    @api.depends('budget_planned', 'budget_spent')
    def _compute_budget_remaining(self):
        """
        Calcule le budget restant
        """
        for chantier in self:
            chantier.budget_remaining = chantier.budget_planned - chantier.budget_spent
    
    @api.depends('task_ids')
    def _compute_task_count(self):
        """
        Compte le nombre de tâches
        """
        for chantier in self:
            chantier.task_count = len(chantier.task_ids)
    
    @api.depends('task_ids.progress')
    def _compute_progress(self):
        """
        Calcule la progression globale du chantier
        Moyenne pondérée de la progression des tâches
        """
        for chantier in self:
            if chantier.task_ids:
                total_progress = sum(chantier.task_ids.mapped('progress'))
                chantier.progress = total_progress / len(chantier.task_ids)
            else:
                chantier.progress = 0.0
    
    @api.depends('document_ids')
    def _compute_document_count(self):
        """
        Compte le nombre de documents
        """
        for chantier in self:
            chantier.document_count = len(chantier.document_ids)
    
    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """
        Compte le nombre de factures
        """
        for chantier in self:
            chantier.invoice_count = len(chantier.invoice_ids)
    
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """
        Vérifie la cohérence des dates
        """
        for chantier in self:
            if chantier.date_start and chantier.date_end:
                if chantier.date_end < chantier.date_start:
                    raise ValidationError(_("La date de fin doit être postérieure à la date de début."))
    
    @api.constrains('budget_planned')
    def _check_budget(self):
        """
        Vérifie que le budget est positif
        """
        for chantier in self:
            if chantier.budget_planned < 0:
                raise ValidationError(_("Le budget prévisionnel doit être positif."))
    
    def action_confirm(self):
        """
        Confirme le chantier
        """
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("Seul un chantier en brouillon peut être confirmé."))
        
        self.write({'state': 'confirmed'})
        
        # Message dans le chatter
        self.message_post(
            body=_("Chantier confirmé par %s") % self.env.user.name,
            message_type='notification'
        )
        
        return True
    
    def action_start(self):
        """
        Démarre le chantier
        """
        self.ensure_one()
        if self.state not in ['confirmed', 'suspended']:
            raise UserError(_("Le chantier doit être confirmé pour être démarré."))
        
        self.write({'state': 'in_progress'})
        
        self.message_post(
            body=_("Chantier démarré le %s") % fields.Date.today(),
            message_type='notification'
        )
        
        return True
    
    def action_suspend(self):
        """
        Suspend le chantier
        """
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_("Seul un chantier en cours peut être suspendu."))
        
        self.write({'state': 'suspended'})
        
        self.message_post(
            body=_("Chantier suspendu par %s") % self.env.user.name,
            message_type='notification'
        )
        
        return True
    
    def action_done(self):
        """
        Clôture le chantier
        """
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_("Seul un chantier en cours peut être clôturé."))
        
        # Vérification que toutes les tâches sont terminées
        if any(task.state != 'done' for task in self.task_ids):
            raise UserError(_("Toutes les tâches doivent être terminées avant de clôturer le chantier."))
        
        self.write({
            'state': 'done',
            'date_end_real': fields.Date.today()
        })
        
        self.message_post(
            body=_("Chantier clôturé le %s") % fields.Date.today(),
            message_type='notification'
        )
        
        return True
    
    def action_cancel(self):
        """
        Annule le chantier
        """
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_("Un chantier terminé ne peut pas être annulé."))
        
        self.write({'state': 'cancelled'})
        
        self.message_post(
            body=_("Chantier annulé par %s") % self.env.user.name,
            message_type='notification'
        )
        
        return True
    
    def action_view_tasks(self):
        """
        Ouvre la vue des tâches du chantier
        """
        self.ensure_one()
        return {
            'name': _('Tâches - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.chantier.task',
            'view_mode': 'tree,form,kanban',
            'domain': [('chantier_id', '=', self.id)],
            'context': {'default_chantier_id': self.id}
        }
    
    def action_view_documents(self):
        """
        Ouvre la vue des documents du chantier
        """
        self.ensure_one()
        return {
            'name': _('Documents - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.chantier.document',
            'view_mode': 'tree,form',
            'domain': [('chantier_id', '=', self.id)],
            'context': {'default_chantier_id': self.id}
        }
    
    def action_view_invoices(self):
        """
        Ouvre la vue des factures du chantier
        """
        self.ensure_one()
        return {
            'name': _('Factures - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.facture',
            'view_mode': 'tree,form',
            'domain': [('chantier_id', '=', self.id)],
            'context': {'default_chantier_id': self.id}
        }
    
    def action_get_ai_suggestions(self):
        """
        Obtient des suggestions de l'IA pour optimiser le chantier
        """
        self.ensure_one()
        
        # Vérification que l'IA est activée
        ai_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'eazynova.ai_assistance_enabled', 'False'
        )
        
        if ai_enabled != 'True':
            raise UserError(_("L'assistance IA n'est pas activée."))
        
        # Préparation du contexte pour l'IA
        context = {
            'chantier_name': self.name,
            'budget_planned': self.budget_planned,
            'budget_spent': self.budget_spent,
            'progress': self.progress,
            'duration_days': self.duration_days,
            'task_count': self.task_count,
        }
        
        # TODO: Appel API IA
        suggestions = _("Suggestions IA à implémenter...")
        
        self.write({'ai_suggestions': suggestions})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Suggestions IA'),
                'message': suggestions,
                'type': 'info',
                'sticky': True,
            }
        }


class EazynovaChantierTag(models.Model):
    """
    Tags pour catégoriser les chantiers
    """
    _name = 'eazynova.chantier.tag'
    _description = 'Étiquette Chantier'
    
    name = fields.Char(
        string="Nom",
        required=True,
        translate=True
    )
    
    color = fields.Integer(
        string="Couleur",
        default=0
    )