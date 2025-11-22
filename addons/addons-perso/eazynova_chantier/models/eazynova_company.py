# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Company(models.Model):
    """
    Extension du modèle res.company pour EAZYNOVA
    Ajout de paramètres spécifiques à la gestion d'entreprise
    """
    _inherit = 'res.company'

    def action_view_chantiers(self):
        """
        Action serveur pour afficher les chantiers liés à la société
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Chantiers'),
            'res_model': 'eazynova.chantier',
            'view_mode': 'tree,form',
            'domain': [('company_id', '=', self.id)],
            'context': {'default_company_id': self.id},
        }

    def action_view_factures(self):
        """
        Action serveur pour afficher les factures liées aux chantiers de la société
        """
        # Récupère les IDs des chantiers liés à la société
        chantier_ids = self.env['eazynova.chantier'].search([('company_id', '=', self.id)]).ids
        # Récupère les factures liées à ces chantiers (supposé champ chantier_id sur account.move)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Factures des chantiers'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('chantier_id', 'in', chantier_ids)],
            'context': {'default_company_id': self.id},
        }
    
    # Paramètres EAZYNOVA
    eazynova_code = fields.Char(
        string="Code EAZYNOVA",
        help="Code unique de l'entreprise dans le système EAZYNOVA",
        copy=False
    )
    
    eazynova_dashboard_layout = fields.Selection([
        ('classic', 'Classique'),
        ('modern', 'Moderne'),
        ('compact', 'Compact'),
    ], string="Disposition du tableau de bord",
       default='modern',
       help="Définit la disposition par défaut du tableau de bord"
    )
    
    # Statistiques (calculées)
    total_chantiers = fields.Integer(
        string="Nombre de chantiers",
        compute='_compute_stats',
        store=False
    )
    
    total_factures = fields.Integer(
        string="Nombre de factures",
        compute='_compute_stats',
        store=False
    )
    
    @api.depends('name')  # Dépendance factice pour forcer le calcul
    def _compute_stats(self):
        """
        Calcule les statistiques de l'entreprise
        Ces champs seront complétés par les modules complémentaires
        """
        for company in self:
            # Placeholder - sera surchargé par les modules CHANTIER et FACTURE
            company.total_chantiers = 0
            company.total_factures = 0
    
    @api.model
    def create(self, vals):
        """
        Génère automatiquement un code EAZYNOVA unique à la création
        """
        if not vals.get('eazynova_code'):
            vals['eazynova_code'] = self.env['ir.sequence'].next_by_code('eazynova.company') or '/'
        return super(Company, self).create(vals)