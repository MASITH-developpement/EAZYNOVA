# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DocumentOCRWizard(models.TransientModel):
    _name = 'eazynova.document.ocr.wizard'
    _description = 'OCR de Document'

    file_data = fields.Binary(string='Fichier', required=True, attachment=False)
    file_name = fields.Char(string='Nom du Fichier')
    file_type = fields.Selection([
        ('pdf', 'PDF'),
        ('image', 'Image'),
    ], string='Type', default='pdf', required=True)

    extracted_text = fields.Text(string='Texte Extrait', readonly=True)

    def action_extract(self):
        """Extrait le texte du document"""
        self.ensure_one()

        ai_service = self.env['eazynova.ai.service']
        result = ai_service.extract_data_from_document(
            self.file_data,
            self.file_type
        )

        self.extracted_text = str(result)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.document.ocr.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
