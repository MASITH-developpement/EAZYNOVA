# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    eazynova_user_level = fields.Selection([
        ('basic', 'Basique'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert'),
    ], string='Niveau EAZYNOVA', default='basic')
