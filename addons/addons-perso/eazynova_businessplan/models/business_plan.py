# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class BusinessPlan(models.Model):
    _name = 'business.plan'
    _description = 'Business Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    # Informations de base
    name = fields.Char(
        string='Nom du Business Plan',
        required=True,
        tracking=True,
        index=True
    )
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Société',
        required=True,
        default=lambda self: self.env.company,
        tracking=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )

    # Dates
    date_start = fields.Date(
        string='Date de début',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    date_end = fields.Date(
        string='Date de fin',
        required=True,
        tracking=True
    )
    duration_months = fields.Integer(
        string='Durée (mois)',
        compute='_compute_duration_months',
        store=True
    )

    # État et validation
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('submitted', 'Soumis'),
        ('validated', 'Validé'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True, tracking=True)

    validated_by = fields.Many2one(
        'res.users',
        string='Validé par',
        readonly=True,
        tracking=True
    )
    validation_date = fields.Datetime(
        string='Date de validation',
        readonly=True,
        tracking=True
    )

    # Description et objectifs
    description = fields.Html(
        string='Description',
        tracking=True
    )
    executive_summary = fields.Html(
        string='Résumé exécutif',
        help='Synthèse du business plan'
    )
    objectives = fields.Html(
        string='Objectifs stratégiques',
        help='Objectifs principaux du business plan'
    )

    # Données financières
    budget_total = fields.Monetary(
        string='Budget total',
        currency_field='currency_id',
        tracking=True
    )
    revenue_target = fields.Monetary(
        string='Chiffre d\'affaires cible',
        currency_field='currency_id',
        tracking=True
    )
    profit_target = fields.Monetary(
        string='Bénéfice cible',
        currency_field='currency_id',
        tracking=True
    )
    investment_required = fields.Monetary(
        string='Investissement requis',
        currency_field='currency_id',
        tracking=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    # Marché et stratégie
    market_analysis = fields.Html(
        string='Analyse de marché',
        help='Analyse du marché cible et de la concurrence'
    )
    target_market = fields.Text(
        string='Marché cible',
        help='Description du marché cible'
    )
    competitive_advantage = fields.Text(
        string='Avantages concurrentiels',
        help='Points différenciateurs par rapport à la concurrence'
    )
    marketing_strategy = fields.Html(
        string='Stratégie marketing',
        help='Plan marketing et communication'
    )

    # Organisation et ressources
    organizational_structure = fields.Html(
        string='Structure organisationnelle',
        help='Organisation de l\'équipe et responsabilités'
    )
    team_size = fields.Integer(
        string='Taille de l\'équipe',
        help='Nombre de personnes prévues'
    )
    key_resources = fields.Text(
        string='Ressources clés',
        help='Ressources matérielles et humaines nécessaires'
    )

    # Indicateurs et suivi
    indicator_ids = fields.One2many(
        'business.plan.indicator',
        'business_plan_id',
        string='Indicateurs de suivi',
        copy=False
    )
    indicator_count = fields.Integer(
        string='Nombre d\'indicateurs',
        compute='_compute_indicator_count'
    )

    # Champs calculés pour tableau de bord
    progress = fields.Float(
        string='Progression (%)',
        compute='_compute_progress',
        store=True
    )
    achievement_rate = fields.Float(
        string='Taux de réalisation (%)',
        compute='_compute_achievement_rate',
        store=True
    )

    # Notes et pièces jointes
    notes = fields.Text(string='Notes internes')
    attachment_count = fields.Integer(
        string='Nombre de pièces jointes',
        compute='_compute_attachment_count'
    )

    # Couleur pour kanban
    color = fields.Integer(string='Couleur')

    @api.depends('date_start', 'date_end')
    def _compute_duration_months(self):
        for plan in self:
            if plan.date_start and plan.date_end:
                delta = plan.date_end - plan.date_start
                plan.duration_months = max(1, round(delta.days / 30))
            else:
                plan.duration_months = 0

    @api.depends('indicator_ids')
    def _compute_indicator_count(self):
        for plan in self:
            plan.indicator_count = len(plan.indicator_ids)

    @api.depends('indicator_ids.progress')
    def _compute_progress(self):
        for plan in self:
            if plan.indicator_ids:
                plan.progress = sum(plan.indicator_ids.mapped('progress')) / len(plan.indicator_ids)
            else:
                plan.progress = 0.0

    @api.depends('indicator_ids.achievement_rate')
    def _compute_achievement_rate(self):
        for plan in self:
            if plan.indicator_ids:
                plan.achievement_rate = sum(plan.indicator_ids.mapped('achievement_rate')) / len(plan.indicator_ids)
            else:
                plan.achievement_rate = 0.0

    def _compute_attachment_count(self):
        for plan in self:
            plan.attachment_count = self.env['ir.attachment'].search_count([
                ('res_model', '=', self._name),
                ('res_id', '=', plan.id)
            ])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('business.plan') or _('Nouveau')
        return super().create(vals_list)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for plan in self:
            if plan.date_start and plan.date_end and plan.date_start > plan.date_end:
                raise ValidationError(_('La date de fin doit être postérieure à la date de début.'))

    def action_submit(self):
        """Soumettre le business plan pour validation"""
        for plan in self:
            if plan.state != 'draft':
                raise UserError(_('Seuls les business plans en brouillon peuvent être soumis.'))
            plan.write({'state': 'submitted'})
            plan.message_post(body=_('Business plan soumis pour validation.'))

    def action_validate(self):
        """Valider le business plan et générer les indicateurs"""
        for plan in self:
            if plan.state != 'submitted':
                raise UserError(_('Seuls les business plans soumis peuvent être validés.'))

            # Validation du business plan
            plan.write({
                'state': 'validated',
                'validated_by': self.env.user.id,
                'validation_date': fields.Datetime.now(),
            })

            # Génération automatique des indicateurs de suivi
            plan._generate_indicators()

            # Passage automatique en cours
            plan.write({'state': 'in_progress'})

            plan.message_post(body=_(
                'Business plan validé par %s. %d indicateurs de suivi générés.'
            ) % (self.env.user.name, len(plan.indicator_ids)))

    def action_start(self):
        """Démarrer le business plan"""
        for plan in self:
            if plan.state != 'validated':
                raise UserError(_('Le business plan doit être validé avant de démarrer.'))
            plan.write({'state': 'in_progress'})
            plan.message_post(body=_('Démarrage du business plan.'))

    def action_done(self):
        """Marquer le business plan comme terminé"""
        for plan in self:
            if plan.state != 'in_progress':
                raise UserError(_('Seuls les business plans en cours peuvent être terminés.'))
            plan.write({'state': 'done'})
            plan.message_post(body=_('Business plan terminé.'))

    def action_cancel(self):
        """Annuler le business plan"""
        for plan in self:
            if plan.state == 'done':
                raise UserError(_('Un business plan terminé ne peut pas être annulé.'))
            plan.write({'state': 'cancelled'})
            plan.message_post(body=_('Business plan annulé.'))

    def action_draft(self):
        """Remettre en brouillon"""
        for plan in self:
            if plan.state not in ['submitted', 'cancelled']:
                raise UserError(_('Impossible de remettre ce business plan en brouillon.'))
            plan.write({'state': 'draft'})
            plan.message_post(body=_('Business plan remis en brouillon.'))

    def _generate_indicators(self):
        """Génère automatiquement les indicateurs de suivi basés sur le business plan"""
        self.ensure_one()

        # Supprimer les anciens indicateurs si existants
        self.indicator_ids.unlink()

        indicator_obj = self.env['business.plan.indicator']
        indicators_to_create = []

        # Indicateurs financiers
        if self.revenue_target:
            indicators_to_create.append({
                'name': 'Chiffre d\'affaires',
                'business_plan_id': self.id,
                'indicator_type': 'financial',
                'target_value': self.revenue_target,
                'unit': 'currency',
                'frequency': 'monthly',
                'description': 'Suivi du chiffre d\'affaires réalisé vs. objectif',
            })

        if self.profit_target:
            indicators_to_create.append({
                'name': 'Bénéfice net',
                'business_plan_id': self.id,
                'indicator_type': 'financial',
                'target_value': self.profit_target,
                'unit': 'currency',
                'frequency': 'monthly',
                'description': 'Suivi du bénéfice net vs. objectif',
            })

        if self.budget_total:
            indicators_to_create.append({
                'name': 'Consommation budget',
                'business_plan_id': self.id,
                'indicator_type': 'financial',
                'target_value': self.budget_total,
                'unit': 'currency',
                'frequency': 'monthly',
                'description': 'Suivi de la consommation du budget alloué',
            })

        # Indicateurs de performance
        indicators_to_create.extend([
            {
                'name': 'Taux de satisfaction client',
                'business_plan_id': self.id,
                'indicator_type': 'performance',
                'target_value': 90.0,
                'unit': 'percentage',
                'frequency': 'monthly',
                'description': 'Mesure de la satisfaction client (objectif: 90%)',
            },
            {
                'name': 'Nombre de nouveaux clients',
                'business_plan_id': self.id,
                'indicator_type': 'commercial',
                'target_value': 50.0,
                'unit': 'number',
                'frequency': 'monthly',
                'description': 'Nombre de nouveaux clients acquis par mois',
            },
            {
                'name': 'Taux de conversion',
                'business_plan_id': self.id,
                'indicator_type': 'commercial',
                'target_value': 25.0,
                'unit': 'percentage',
                'frequency': 'monthly',
                'description': 'Taux de conversion prospects -> clients',
            },
        ])

        # Indicateurs RH si équipe définie
        if self.team_size:
            indicators_to_create.append({
                'name': 'Effectif réalisé',
                'business_plan_id': self.id,
                'indicator_type': 'hr',
                'target_value': float(self.team_size),
                'unit': 'number',
                'frequency': 'monthly',
                'description': 'Nombre de personnes dans l\'équipe vs. objectif',
            })

        # Création des indicateurs
        for indicator_data in indicators_to_create:
            indicator_obj.create(indicator_data)

    def action_view_indicators(self):
        """Ouvrir la vue des indicateurs"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Indicateurs de suivi'),
            'res_model': 'business.plan.indicator',
            'view_mode': 'tree,form,graph,pivot',
            'domain': [('business_plan_id', '=', self.id)],
            'context': {'default_business_plan_id': self.id},
        }

    def action_view_attachments(self):
        """Ouvrir la vue des pièces jointes"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pièces jointes'),
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            },
        }
