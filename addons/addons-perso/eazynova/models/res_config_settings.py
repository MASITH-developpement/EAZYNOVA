# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    eazynova_ai_enabled = fields.Boolean(
        string='Activer le Service IA',
        config_parameter='eazynova.ai.enabled'
    )

    eazynova_ai_provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('claude', 'Claude (Anthropic)'),
    ], string='Fournisseur IA', config_parameter='eazynova.ai.provider')

    eazynova_ai_api_key = fields.Char(
        string='Clé API IA',
        config_parameter='eazynova.ai.api_key'
    )

    eazynova_ocr_enabled = fields.Boolean(
        string='Activer l\'OCR',
        default=True,
        config_parameter='eazynova.ocr.enabled'
    )
