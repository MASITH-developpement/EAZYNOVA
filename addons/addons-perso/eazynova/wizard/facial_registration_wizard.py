# -*- coding: utf-8 -*-

from odoo import models, fields


class FacialRegistrationWizard(models.TransientModel):
    _name = 'eazynova.facial.registration.wizard'
    _description = 'Enregistrement Facial'

    user_id = fields.Many2one('res.users', string='Utilisateur', required=True)
    photo = fields.Binary(string='Photo', attachment=False)
    status = fields.Char(string='Statut', readonly=True, default='En attente')

    def action_register(self):
        """Enregistre la photo faciale (stub)"""
        self.ensure_one()
        self.status = 'Fonctionnalité à implémenter'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.facial.registration.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
