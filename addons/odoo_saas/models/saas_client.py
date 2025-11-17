# -*- coding: utf-8 -*-
"""
Modèle de gestion des clients SaaS
Gère les informations clients, domaines et isolation des données
"""

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import re
import logging

_logger = logging.getLogger(__name__)


class SaasClient(models.Model):
    """
    Représente un client SaaS (tenant)
    Chaque client dispose de ses propres données isolées
    """
    _name = 'saas.client'
    _description = 'Client SaaS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # === INFORMATIONS DE BASE ===
    name = fields.Char(
        string='Nom du Client',
        required=True,
        tracking=True,
        index=True,
        help="Nom de l'entreprise ou organisation cliente"
    )

    code = fields.Char(
        string='Code Client',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Code unique d'identification du client"
    )

    active = fields.Boolean(
        string='Actif',
        default=True,
        tracking=True,
        help="Décochez pour désactiver le client sans le supprimer"
    )

    # === CONTACT ===
    email = fields.Char(
        string='Email',
        required=True,
        help="Adresse email principale"
    )

    phone = fields.Char(
        string='Téléphone',
        help="Numéro de téléphone"
    )

    # === CONFIGURATION SAAS ===
    subdomain = fields.Char(
        string='Sous-domaine',
        required=True,
        index=True,
        tracking=True,
        help="Sous-domaine unique pour accéder à l'instance (ex: client.votredomaine.com)"
    )

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('pending', 'En Attente'),
        ('active', 'Actif'),
        ('suspended', 'Suspendu'),
        ('cancelled', 'Annulé')
    ], string='État', default='draft', required=True, tracking=True,
        help="État actuel du client SaaS")

    # === LIMITES ET QUOTAS ===
    max_users = fields.Integer(
        string='Utilisateurs Max',
        default=10,
        required=True,
        help="Nombre maximum d'utilisateurs autorisés"
    )

    current_users = fields.Integer(
        string='Utilisateurs Actuels',
        default=0,
        help="Nombre actuel d'utilisateurs actifs"
    )

    max_storage_gb = fields.Float(
        string='Stockage Max (GB)',
        default=5.0,
        required=True,
        help="Espace de stockage maximum en gigaoctets"
    )

    current_storage_gb = fields.Float(
        string='Stockage Utilisé (GB)',
        default=0.0,
        help="Espace de stockage actuellement utilisé"
    )

    # === ABONNEMENT ===
    plan_id = fields.Many2one(
        comodel_name='saas.plan',
        string='Plan Souscrit',
        tracking=True,
        help="Plan d'abonnement du client"
    )

    # === DATES ===
    activation_date = fields.Datetime(
        string='Date d\'Activation',
        readonly=True,
        tracking=True,
        help="Date de première activation du client"
    )

    expiration_date = fields.Datetime(
        string='Date d\'Expiration',
        tracking=True,
        help="Date d'expiration de l'abonnement"
    )

    # === NOTES ===
    notes = fields.Text(
        string='Notes Internes',
        help="Notes et remarques internes"
    )

    # === CONTRAINTES SQL ===
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Le code client doit être unique !'),
        ('subdomain_unique', 'UNIQUE(subdomain)',
         'Le sous-domaine doit être unique !'),
        ('max_users_positive', 'CHECK(max_users > 0)',
         'Le nombre d\'utilisateurs max doit être positif !'),
        ('max_storage_positive', 'CHECK(max_storage_gb > 0)',
         'Le stockage max doit être positif !'),
    ]

    # === MÉTHODES ONCHANGE ===
    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        """Met à jour les limites selon le plan choisi"""
        if self.plan_id:
            self.max_users = self.plan_id.max_users
            self.max_storage_gb = self.plan_id.max_storage_gb

    # === CONTRAINTES ET VALIDATIONS ===
    @api.constrains('subdomain')
    def _check_subdomain(self):
        """Valide le format du sous-domaine"""
        for record in self:
            if record.subdomain:
                if not re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$', record.subdomain):
                    raise ValidationError(_(
                        'Le sous-domaine doit contenir uniquement des lettres minuscules, '
                        'chiffres et tirets. Il ne peut pas commencer ou finir par un tiret.'
                    ))
                if len(record.subdomain) < 3:
                    raise ValidationError(
                        _('Le sous-domaine doit contenir au moins 3 caractères.'))
                if len(record.subdomain) > 63:
                    raise ValidationError(
                        _('Le sous-domaine ne peut pas dépasser 63 caractères.'))

    @api.constrains('current_users', 'max_users')
    def _check_user_limit(self):
        """Vérifie que la limite d'utilisateurs n'est pas dépassée"""
        for record in self:
            if record.current_users > record.max_users:
                raise ValidationError(_(
                    'Limite d\'utilisateurs dépassée ! '
                    'Utilisateurs actuels: %s, Maximum autorisé: %s'
                ) % (record.current_users, record.max_users))

    # === MÉTHODES CREATE/WRITE ===
    @api.model_create_multi
    def create(self, vals_list):
        """Création sécurisée avec génération automatique du code"""
        for vals in vals_list:
            if vals.get('code', _('Nouveau')) == _('Nouveau'):
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'saas.client') or _('Nouveau')

        clients = super(SaasClient, self).create(vals_list)

        for client in clients:
            _logger.info(f'Client SaaS créé: {client.code} - {client.name}')

        return clients

    def write(self, vals):
        """Modification sécurisée avec validations"""
        if 'code' in vals:
            raise UserError(_('Le code client ne peut pas être modifié !'))

        if 'state' in vals:
            for record in self:
                _logger.info(
                    f'Client {record.code}: changement d\'état {record.state} -> {vals["state"]}'
                )

        return super(SaasClient, self).write(vals)

    def unlink(self):
        """Suppression sécurisée"""
        for record in self:
            if record.state == 'active':
                raise UserError(_(
                    'Impossible de supprimer un client actif ! '
                    'Veuillez d\'abord le suspendre ou l\'annuler.'
                ))

        _logger.warning(
            f'Suppression des clients: {", ".join(self.mapped("code"))}')
        return super(SaasClient, self).unlink()

    # === ACTIONS MÉTIER ===
    def action_activate(self):
        """Active le client SaaS"""
        self.ensure_one()

        if self.state == 'active':
            raise UserError(_('Ce client est déjà actif !'))

        if not self.plan_id:
            raise UserError(
                _('Veuillez d\'abord sélectionner un plan d\'abonnement !'))

        self.write({
            'state': 'active',
            'activation_date': fields.Datetime.now(),
        })

        _logger.info(f'Client {self.code} activé avec succès')

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Succès'),
                'message': _('Le client a été activé avec succès !'),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_suspend(self):
        """Suspend le client (conserve les données)"""
        self.ensure_one()

        if self.state != 'active':
            raise UserError(_('Seul un client actif peut être suspendu !'))

        self.state = 'suspended'
        _logger.warning(f'Client {self.code} suspendu')

        return True

    def action_cancel(self):
        """Annule le client"""
        self.ensure_one()

        self.state = 'cancelled'
        _logger.warning(f'Client {self.code} annulé')

        return True
