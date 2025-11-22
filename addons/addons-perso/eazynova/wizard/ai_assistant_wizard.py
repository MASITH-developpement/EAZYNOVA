# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AIAssistantWizard(models.TransientModel):
    _name = 'eazynova.ai.assistant.wizard'
    _description = 'Assistant IA EAZYNOVA'

    question = fields.Text(string='Question', required=True)
    response = fields.Text(string='Réponse', readonly=True)
    context_info = fields.Text(string='Contexte')

    def action_ask_ai(self):
        """Demande à l'IA"""
        self.ensure_one()

        ai_service = self.env['eazynova.ai.service']
        result = ai_service.analyze_text(
            self.question,
            prompt=self.context_info
        )

        self.response = result

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.ai.assistant.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
