# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    eazynova_enabled = fields.Boolean(
        string='EAZYNOVA Activé',
        default=True,
        help="Activer les fonctionnalités EAZYNOVA pour cette société"
    )
