from odoo import models, fields
odomodel


class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
