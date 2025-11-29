# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessPlan(models.Model):
    _name = 'business.plan'
    _description = 'Business Plan'
    _inherit = ['mail.thread']
    _order = 'create_date desc'

    # Informations essentielles
    name = fields.Char(string='Nom du Business Plan', required=True, tracking=True)
    reference = fields.Char(string='Référence', readonly=True, copy=False, default='Nouveau')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user, required=True)

    # Dates
    date_start = fields.Date(string='Date de début', required=True, default=fields.Date.today)
    date_end = fields.Date(string='Date de fin', required=True)

    # État simplifié (3 états seulement)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('done', 'Terminé'),
    ], string='État', default='draft', required=True, tracking=True)

    # Contenu
    description = fields.Text(string='Description du projet')
    objectives = fields.Text(string='Objectifs principaux')

    # Finance (un seul objectif financier)
    revenue_target = fields.Monetary(string='Objectif de chiffre d\'affaires', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # Indicateurs
    indicator_ids = fields.One2many('business.plan.indicator', 'business_plan_id', string='Indicateurs')
    indicator_count = fields.Integer(compute='_compute_indicator_count')
    progress = fields.Float(string='Progression (%)', compute='_compute_progress')

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'Nouveau') == 'Nouveau':
                vals['reference'] = self.env['ir.sequence'].next_by_code('business.plan') or 'Nouveau'
        return super().create(vals_list)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for plan in self:
            if plan.date_start and plan.date_end and plan.date_start > plan.date_end:
                raise ValidationError(_('La date de fin doit être après la date de début.'))

    def action_validate(self):
        """Valider et générer les indicateurs"""
        for plan in self:
            plan.state = 'validated'
            plan._generate_indicators()
            plan.message_post(body=_('Business plan validé. %d indicateurs créés.') % len(plan.indicator_ids))

    def action_done(self):
        """Terminer le business plan"""
        self.state = 'done'

    def _generate_indicators(self):
        """Génère 3 indicateurs simples"""
        self.ensure_one()
        self.indicator_ids.unlink()

        indicators = []
        if self.revenue_target:
            indicators.append({
                'name': 'Chiffre d\'affaires',
                'business_plan_id': self.id,
                'target_value': self.revenue_target,
            })

        indicators.extend([
            {'name': 'Satisfaction client (%)', 'business_plan_id': self.id, 'target_value': 90},
            {'name': 'Nouveaux clients', 'business_plan_id': self.id, 'target_value': 10},
        ])

        for ind in indicators:
            self.env['business.plan.indicator'].create(ind)

    def action_view_indicators(self):
        """Voir les indicateurs"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Indicateurs',
            'res_model': 'business.plan.indicator',
            'view_mode': 'tree,form',
            'domain': [('business_plan_id', '=', self.id)],
            'context': {'default_business_plan_id': self.id},
        }
