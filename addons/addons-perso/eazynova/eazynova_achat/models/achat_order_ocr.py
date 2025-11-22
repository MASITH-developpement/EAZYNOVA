# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AchatOrderOCR(models.Model):
    _inherit = 'purchase.order'

    ocr_attachment_id = fields.Many2one('ir.attachment', string="Facture/Bon scanné (OCR)")
    ocr_extracted_text = fields.Text(string="Texte extrait (OCR)")
    ia_suggestion = fields.Text(string="Suggestion IA (commande)")
    chantier_id = fields.Many2one('project.project', string="Chantier lié")

    def action_ocr_extract(self):
        # Appel à l'OCR (ex: Tesseract, pdf2image, etc.)
        # Appel à l'IA (OpenAI, Claude, etc.) pour suggestion de saisie
        # À implémenter selon l'intégration technique
        self.ocr_extracted_text = _("Texte extrait simulé")
        self.ia_suggestion = _("Suggestion IA simulée pour la commande d'achat")
        return True
