# -*- coding: utf-8 -*-
"""
Modèle de gestion des plans d'abonnement SaaS
"""

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaasPlan(models.Model):
    """Plans d'abonnement SaaS"""
    _name = 'saas.plan'
    _description = 'Plan d\'Abonnement SaaS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    # === INFORMATIONS DE BASE ===
    name = fields.Char(
        string='Nom du Plan',
        required=True,
        tracking=True,
        help="Nom du plan (ex: Basic, Pro, Enterprise)"
    )

    code = fields.Char(
        string='Code',
        required=True,
        tracking=True,
        help="Code unique du plan"
    )

    active = fields.Boolean(
        string='Actif',
        default=True,
        tracking=True
    )

    sequence = fields.Integer(
        string='Séquence',
        default=10,
        help="Ordre d'affichage"
    )

    description = fields.Text(
        string='Description',
        help="Description détaillée du plan"
    )

    # === TARIFICATION ===
    price_monthly = fields.Float(
        string='Prix Mensuel (€)',
        required=True,
        default=9.99,
        tracking=True,
        help="Prix de l'abonnement mensuel"
    )

    price_yearly = fields.Float(
        string='Prix Annuel (€)',
        required=True,
        default=99.00,
        tracking=True,
        help="Prix de l'abonnement annuel"
    )

    discount_yearly = fields.Float(
        string='Réduction Annuelle (%)',
        compute='_compute_discount_yearly',
        store=True,
        help="Réduction en % pour l'abonnement annuel"
    )

    # === LIMITES ===
    max_users = fields.Integer(
        string='Utilisateurs Maximum',
        required=True,
        default=10,
        help="Nombre maximum d'utilisateurs"
    )

    max_storage_gb = fields.Float(
        string='Stockage Maximum (GB)',
        required=True,
        default=5.0,
        help="Espace de stockage maximum en GB"
    )

    # === FONCTIONNALITÉS ===
    features = fields.Text(
        string='Fonctionnalités',
        help="Liste des fonctionnalités (une par ligne)"
    )

    # === COMPTEURS ===
    client_count = fields.Integer(
        string='Nombre de Clients',
        compute='_compute_client_count',
        help="Nombre de clients utilisant ce plan"
    )

    # === CONTRAINTES SQL ===
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Le code du plan doit être unique !'),
        ('price_monthly_positive', 'CHECK(price_monthly >= 0)',
         'Le prix mensuel doit être positif !'),
        ('price_yearly_positive', 'CHECK(price_yearly >= 0)',
         'Le prix annuel doit être positif !'),
        ('max_users_positive', 'CHECK(max_users > 0)',
         'Le nombre d\'utilisateurs doit être positif !'),
    ]

    # === MÉTHODES COMPUTE ===
    @api.depends('price_monthly', 'price_yearly')
    def _compute_discount_yearly(self):
        """Calcule la réduction pour l'abonnement annuel"""
        for record in self:
            if record.price_monthly > 0:
                monthly_total = record.price_monthly * 12
                if monthly_total > 0:
                    record.discount_yearly = (
                        (monthly_total - record.price_yearly) / monthly_total) * 100
                else:
                    record.discount_yearly = 0.0
            else:
                record.discount_yearly = 0.0

    def _compute_client_count(self):
        """Compte le nombre de clients par plan"""
        for record in self:
            record.client_count = self.env['saas.client'].search_count([
                ('plan_id', '=', record.id),
                ('state', 'in', ['active', 'pending'])
            ])

    # === MÉTHODES ===
    def get_features_list(self):
        """Retourne la liste des fonctionnalités"""
        self.ensure_one()
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def action_view_clients(self):
        """Ouvre la liste des clients du plan"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Clients - %s') % self.name,
            'res_model': 'saas.client',
            'view_mode': 'tree,form',
            'domain': [('plan_id', '=', self.id)],
            'context': {'default_plan_id': self.id},
        }
