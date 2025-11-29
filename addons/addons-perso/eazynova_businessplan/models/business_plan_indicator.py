# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessPlanIndicator(models.Model):
    _name = 'business.plan.indicator'
    _description = 'Indicateur de Business Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    # Informations de base
    name = fields.Char(
        string='Nom de l\'indicateur',
        required=True,
        tracking=True
    )
    sequence = fields.Integer(
        string='Séquence',
        default=10
    )
    business_plan_id = fields.Many2one(
        'business.plan',
        string='Business Plan',
        required=True,
        ondelete='cascade',
        index=True
    )
    company_id = fields.Many2one(
        related='business_plan_id.company_id',
        string='Société',
        store=True,
        readonly=True
    )

    # Type et catégorie
    indicator_type = fields.Selection([
        ('financial', 'Financier'),
        ('commercial', 'Commercial'),
        ('performance', 'Performance'),
        ('quality', 'Qualité'),
        ('hr', 'Ressources Humaines'),
        ('operational', 'Opérationnel'),
        ('strategic', 'Stratégique'),
    ], string='Type d\'indicateur', required=True, default='performance', tracking=True)

    category = fields.Selection([
        ('kpi', 'KPI Principal'),
        ('metric', 'Métrique'),
        ('target', 'Objectif'),
    ], string='Catégorie', default='metric')

    # Description
    description = fields.Text(
        string='Description',
        help='Description détaillée de l\'indicateur'
    )

    # Valeurs et objectifs
    unit = fields.Selection([
        ('currency', 'Monétaire'),
        ('percentage', 'Pourcentage'),
        ('number', 'Nombre'),
        ('ratio', 'Ratio'),
        ('days', 'Jours'),
        ('hours', 'Heures'),
    ], string='Unité de mesure', required=True, default='number')

    target_value = fields.Float(
        string='Valeur cible',
        required=True,
        tracking=True,
        help='Valeur objectif à atteindre'
    )
    current_value = fields.Float(
        string='Valeur actuelle',
        tracking=True,
        help='Valeur actuellement réalisée'
    )
    previous_value = fields.Float(
        string='Valeur précédente',
        help='Valeur de la période précédente'
    )

    # Devise pour indicateurs monétaires
    currency_id = fields.Many2one(
        related='business_plan_id.currency_id',
        string='Devise',
        readonly=True
    )

    # Calculs et progression
    progress = fields.Float(
        string='Progression (%)',
        compute='_compute_progress',
        store=True,
        help='Progression par rapport à l\'objectif'
    )
    achievement_rate = fields.Float(
        string='Taux de réalisation (%)',
        compute='_compute_achievement_rate',
        store=True,
        help='Taux de réalisation de l\'objectif'
    )
    variance = fields.Float(
        string='Écart',
        compute='_compute_variance',
        store=True,
        help='Écart entre la valeur actuelle et la cible'
    )
    variance_percentage = fields.Float(
        string='Écart (%)',
        compute='_compute_variance',
        store=True,
        help='Écart en pourcentage'
    )

    # Seuils et alertes
    min_threshold = fields.Float(
        string='Seuil minimum',
        help='Seuil en dessous duquel une alerte est déclenchée'
    )
    max_threshold = fields.Float(
        string='Seuil maximum',
        help='Seuil au-dessus duquel une alerte est déclenchée'
    )
    alert_status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'Attention'),
        ('critical', 'Critique'),
    ], string='Statut', compute='_compute_alert_status', store=True)

    # Périodicité et suivi
    frequency = fields.Selection([
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('quarterly', 'Trimestriel'),
        ('yearly', 'Annuel'),
    ], string='Fréquence de suivi', required=True, default='monthly')

    last_update_date = fields.Date(
        string='Dernière mise à jour',
        default=fields.Date.today
    )
    next_review_date = fields.Date(
        string='Prochaine révision',
        compute='_compute_next_review_date',
        store=True
    )

    # Responsable
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user,
        tracking=True
    )

    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('achieved', 'Atteint'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True, tracking=True)

    # Historique des valeurs
    history_ids = fields.One2many(
        'business.plan.indicator.history',
        'indicator_id',
        string='Historique'
    )

    # Notes
    notes = fields.Text(string='Notes')

    # Couleur pour visualisation
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True
    )

    @api.depends('current_value', 'target_value')
    def _compute_progress(self):
        for indicator in self:
            if indicator.target_value:
                indicator.progress = min(100.0, (indicator.current_value / indicator.target_value) * 100)
            else:
                indicator.progress = 0.0

    @api.depends('current_value', 'target_value')
    def _compute_achievement_rate(self):
        for indicator in self:
            if indicator.target_value:
                indicator.achievement_rate = (indicator.current_value / indicator.target_value) * 100
            else:
                indicator.achievement_rate = 0.0

    @api.depends('current_value', 'target_value')
    def _compute_variance(self):
        for indicator in self:
            indicator.variance = indicator.current_value - indicator.target_value
            if indicator.target_value:
                indicator.variance_percentage = (indicator.variance / indicator.target_value) * 100
            else:
                indicator.variance_percentage = 0.0

    @api.depends('achievement_rate', 'min_threshold', 'max_threshold')
    def _compute_alert_status(self):
        for indicator in self:
            if indicator.achievement_rate >= 100:
                indicator.alert_status = 'ok'
            elif indicator.achievement_rate >= 80:
                indicator.alert_status = 'ok'
            elif indicator.achievement_rate >= 50:
                indicator.alert_status = 'warning'
            else:
                indicator.alert_status = 'critical'

    @api.depends('alert_status')
    def _compute_color(self):
        color_map = {
            'ok': 10,      # Vert
            'warning': 3,  # Jaune
            'critical': 1, # Rouge
        }
        for indicator in self:
            indicator.color = color_map.get(indicator.alert_status, 0)

    @api.depends('last_update_date', 'frequency')
    def _compute_next_review_date(self):
        from dateutil.relativedelta import relativedelta
        for indicator in self:
            if indicator.last_update_date:
                date = indicator.last_update_date
                if indicator.frequency == 'daily':
                    indicator.next_review_date = date + relativedelta(days=1)
                elif indicator.frequency == 'weekly':
                    indicator.next_review_date = date + relativedelta(weeks=1)
                elif indicator.frequency == 'monthly':
                    indicator.next_review_date = date + relativedelta(months=1)
                elif indicator.frequency == 'quarterly':
                    indicator.next_review_date = date + relativedelta(months=3)
                elif indicator.frequency == 'yearly':
                    indicator.next_review_date = date + relativedelta(years=1)
                else:
                    indicator.next_review_date = False
            else:
                indicator.next_review_date = False

    @api.constrains('target_value')
    def _check_target_value(self):
        for indicator in self:
            if indicator.target_value < 0:
                raise ValidationError(_('La valeur cible doit être positive.'))

    def write(self, vals):
        # Sauvegarder l'historique avant modification
        if 'current_value' in vals:
            for indicator in self:
                if indicator.current_value != vals['current_value']:
                    self.env['business.plan.indicator.history'].create({
                        'indicator_id': indicator.id,
                        'date': fields.Date.today(),
                        'value': vals['current_value'],
                        'note': vals.get('notes', ''),
                    })
        return super().write(vals)

    def action_activate(self):
        """Activer l'indicateur"""
        self.write({'state': 'active'})

    def action_achieve(self):
        """Marquer comme atteint"""
        self.write({'state': 'achieved'})

    def action_fail(self):
        """Marquer comme échoué"""
        self.write({'state': 'failed'})

    def action_view_history(self):
        """Voir l'historique de l'indicateur"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Historique'),
            'res_model': 'business.plan.indicator.history',
            'view_mode': 'tree,form,graph',
            'domain': [('indicator_id', '=', self.id)],
            'context': {'default_indicator_id': self.id},
        }


class BusinessPlanIndicatorHistory(models.Model):
    _name = 'business.plan.indicator.history'
    _description = 'Historique des valeurs d\'indicateur'
    _order = 'date desc'

    indicator_id = fields.Many2one(
        'business.plan.indicator',
        string='Indicateur',
        required=True,
        ondelete='cascade',
        index=True
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today
    )
    value = fields.Float(
        string='Valeur',
        required=True
    )
    note = fields.Text(string='Note')
    user_id = fields.Many2one(
        'res.users',
        string='Saisi par',
        default=lambda self: self.env.user,
        readonly=True
    )
