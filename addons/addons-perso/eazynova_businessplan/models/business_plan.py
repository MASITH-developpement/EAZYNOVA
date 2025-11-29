# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessPlan(models.Model):
    _name = 'business.plan'
    _description = 'Business Plan'
    _inherit = ['mail.thread']
    _order = 'create_date desc'

    # ========== INFORMATIONS GÉNÉRALES ==========
    name = fields.Char(string='Nom du projet / entreprise', required=True, tracking=True)
    reference = fields.Char(string='Référence', readonly=True, copy=False, default='Nouveau')
    user_id = fields.Many2one('res.users', string='Porteur du projet', default=lambda self: self.env.user, required=True)

    date_start = fields.Date(string='Date de début', required=True, default=fields.Date.today)
    date_end = fields.Date(string='Date de fin', required=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('done', 'Terminé'),
    ], string='État', default='draft', required=True, tracking=True)

    # ========== 1. RÉSUMÉ EXÉCUTIF ==========
    executive_summary = fields.Text(
        string='Résumé exécutif',
        help='Synthèse du projet en quelques lignes (objectif, marché, avantage concurrentiel)')

    # ========== 2. PRÉSENTATION DU PROJET ==========
    project_description = fields.Text(
        string='Description du projet',
        help='Décrivez votre projet en détail : quelle est votre activité, votre vision ?')

    legal_form = fields.Selection([
        ('individual', 'Entreprise individuelle'),
        ('eurl', 'EURL'),
        ('sarl', 'SARL'),
        ('sas', 'SAS'),
        ('sa', 'SA'),
        ('other', 'Autre'),
    ], string='Forme juridique')

    location = fields.Char(string='Localisation', help='Où sera basée votre entreprise ?')

    # ========== 3. PRODUITS ET SERVICES ==========
    products_services = fields.Text(
        string='Produits et services',
        help='Décrivez vos produits/services : que vendez-vous ? Quelles sont leurs caractéristiques ?')

    value_proposition = fields.Text(
        string='Proposition de valeur',
        help='Quelle valeur apportez-vous à vos clients ? Qu\'est-ce qui vous différencie ?')

    # ========== 4. ANALYSE DE MARCHÉ ==========
    target_market = fields.Text(
        string='Marché cible',
        help='Qui sont vos clients cibles ? Quel est votre marché (taille, croissance) ?')

    competitors = fields.Text(
        string='Concurrence',
        help='Qui sont vos concurrents ? Quels sont leurs forces et faiblesses ?')

    competitive_advantage = fields.Text(
        string='Avantages concurrentiels',
        help='Pourquoi les clients vous choisiront plutôt que vos concurrents ?')

    # ========== 5. STRATÉGIE MARKETING ET COMMERCIALE ==========
    marketing_strategy = fields.Text(
        string='Stratégie marketing',
        help='Comment allez-vous vous faire connaître ? (communication, publicité, réseaux sociaux...)')

    sales_strategy = fields.Text(
        string='Stratégie commerciale',
        help='Comment allez-vous vendre ? (canaux de vente, prix, distribution...)')

    customer_acquisition = fields.Text(
        string='Acquisition clients',
        help='Comment allez-vous acquérir vos premiers clients ?')

    # ========== 6. ORGANISATION ET ÉQUIPE ==========
    team_structure = fields.Text(
        string='Structure de l\'équipe',
        help='Qui compose votre équipe ? Quels sont les rôles et compétences ?')

    team_size = fields.Integer(string='Nombre de personnes', default=1)

    key_partners = fields.Text(
        string='Partenaires clés',
        help='Quels sont vos partenaires stratégiques ? (fournisseurs, distributeurs...)')

    # ========== 7. PRÉVISIONS FINANCIÈRES ==========
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # Année 1
    revenue_year1 = fields.Monetary(string='CA prévisionnel Année 1', currency_field='currency_id')
    costs_year1 = fields.Monetary(string='Charges Année 1', currency_field='currency_id')
    profit_year1 = fields.Monetary(string='Résultat Année 1', compute='_compute_profit_year1', store=True)

    # Année 2
    revenue_year2 = fields.Monetary(string='CA prévisionnel Année 2', currency_field='currency_id')
    costs_year2 = fields.Monetary(string='Charges Année 2', currency_field='currency_id')
    profit_year2 = fields.Monetary(string='Résultat Année 2', compute='_compute_profit_year2', store=True)

    # Année 3
    revenue_year3 = fields.Monetary(string='CA prévisionnel Année 3', currency_field='currency_id')
    costs_year3 = fields.Monetary(string='Charges Année 3', currency_field='currency_id')
    profit_year3 = fields.Monetary(string='Résultat Année 3', compute='_compute_profit_year3', store=True)

    breakeven_point = fields.Text(
        string='Seuil de rentabilité',
        help='À partir de quel chiffre d\'affaires êtes-vous rentable ?')

    # ========== 8. BESOINS DE FINANCEMENT ==========
    initial_investment = fields.Monetary(
        string='Investissement initial total',
        currency_field='currency_id',
        help='Total des investissements nécessaires au démarrage')

    own_contribution = fields.Monetary(
        string='Apport personnel',
        currency_field='currency_id',
        help='Montant que vous apportez personnellement')

    funding_needed = fields.Monetary(
        string='Besoin de financement',
        compute='_compute_funding_needed',
        store=True,
        currency_field='currency_id',
        help='Montant à financer (investissement - apport)')

    funding_sources = fields.Text(
        string='Sources de financement',
        help='Comment comptez-vous financer votre projet ? (prêt bancaire, levée de fonds, aides...)')

    # ========== 9. RISQUES ET OPPORTUNITÉS ==========
    risks = fields.Text(
        string='Risques identifiés',
        help='Quels sont les principaux risques de votre projet ?')

    mitigation_plan = fields.Text(
        string='Plan de mitigation',
        help='Comment comptez-vous gérer ces risques ?')

    opportunities = fields.Text(
        string='Opportunités',
        help='Quelles opportunités de développement voyez-vous ?')

    # ========== INDICATEURS ==========
    indicator_ids = fields.One2many('business.plan.indicator', 'business_plan_id', string='Indicateurs')
    indicator_count = fields.Integer(compute='_compute_indicator_count')
    progress = fields.Float(string='Progression (%)', compute='_compute_progress')

    # ========== CALCULS ==========
    @api.depends('revenue_year1', 'costs_year1')
    def _compute_profit_year1(self):
        for plan in self:
            plan.profit_year1 = (plan.revenue_year1 or 0) - (plan.costs_year1 or 0)

    @api.depends('revenue_year2', 'costs_year2')
    def _compute_profit_year2(self):
        for plan in self:
            plan.profit_year2 = (plan.revenue_year2 or 0) - (plan.costs_year2 or 0)

    @api.depends('revenue_year3', 'costs_year3')
    def _compute_profit_year3(self):
        for plan in self:
            plan.profit_year3 = (plan.revenue_year3 or 0) - (plan.costs_year3 or 0)

    @api.depends('initial_investment', 'own_contribution')
    def _compute_funding_needed(self):
        for plan in self:
            plan.funding_needed = (plan.initial_investment or 0) - (plan.own_contribution or 0)

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
        """Génère des indicateurs basés sur les prévisions"""
        self.ensure_one()
        self.indicator_ids.unlink()

        indicators = []

        # Indicateurs financiers année 1
        if self.revenue_year1:
            indicators.append({
                'name': 'CA Année 1',
                'business_plan_id': self.id,
                'target_value': self.revenue_year1,
            })

        if self.revenue_year2:
            indicators.append({
                'name': 'CA Année 2',
                'business_plan_id': self.id,
                'target_value': self.revenue_year2,
            })

        if self.revenue_year3:
            indicators.append({
                'name': 'CA Année 3',
                'business_plan_id': self.id,
                'target_value': self.revenue_year3,
            })

        # Indicateurs de performance
        indicators.extend([
            {'name': 'Nouveaux clients', 'business_plan_id': self.id, 'target_value': 50},
            {'name': 'Satisfaction client (%)', 'business_plan_id': self.id, 'target_value': 90},
        ])

        # Indicateur d'équipe
        if self.team_size > 1:
            indicators.append({
                'name': 'Effectif',
                'business_plan_id': self.id,
                'target_value': self.team_size,
            })

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
