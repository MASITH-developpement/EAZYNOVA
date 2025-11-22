# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class EazynovaChantierDocument(models.Model):
    """Documents d'un chantier"""
    _name = 'eazynova.chantier.document'
    _description = 'Document Chantier'
    
    name = fields.Char(string="Nom", required=True)
    chantier_id = fields.Many2one('eazynova.chantier', string="Chantier", required=True, ondelete='cascade')
    document = fields.Binary(string="Fichier", attachment=True)
    document_filename = fields.Char(string="Nom du fichier")
    document_type = fields.Selection([
        ('plan', 'Plan'),
        ('photo', 'Photo'),
        ('facture', 'Facture'),
        ('contrat', 'Contrat'),
        ('autre', 'Autre'),
    ], string="Type", default='autre')
