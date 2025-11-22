# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class EazynovaChantierTask(models.Model):
    """Taches d'un chantier"""
    _name = 'eazynova.chantier.task'
    _description = 'Tache Chantier'
    _order = 'sequence, name'
    
    name = fields.Char(string="Tache", required=True)
    chantier_id = fields.Many2one('eazynova.chantier', string="Chantier", required=True, ondelete='cascade')
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('todo', 'A faire'),
        ('in_progress', 'En cours'),
        ('done', 'Termine'),
    ], string="Etat", default='todo', required=True)
    progress = fields.Float(string="Progression (%)", default=0.0)
    cost = fields.Monetary(string="Cout", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='chantier_id.currency_id', store=True)
