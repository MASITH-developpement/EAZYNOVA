# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    """
    Extension des paramètres généraux pour EAZYNOVA
    Permet la configuration de la reconnaissance faciale et des fonctionnalités IA
    """
    _inherit = 'res.config.settings'
    
    # Reconnaissance faciale
    facial_recognition_enabled = fields.Boolean(
        string="Activer la reconnaissance faciale",
        help="Permet aux utilisateurs de se connecter par reconnaissance faciale",
        config_parameter='eazynova.facial_recognition_enabled'
    )
    
    facial_recognition_tolerance = fields.Float(
        string="Tolérance de reconnaissance",
        default=0.6,
        help="Seuil de confiance pour la reconnaissance faciale (0.0 à 1.0)",
        config_parameter='eazynova.facial_recognition_tolerance'
    )
    
    # Assistance IA
    ai_assistance_enabled = fields.Boolean(
        string="Activer l'assistance IA",
        default=True,
        help="Active l'assistant IA dans tous les modules EAZYNOVA",
        config_parameter='eazynova.ai_assistance_enabled'
    )
    
    ai_provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic Claude'),
        ('local', 'Modèle local'),
    ], string="Fournisseur IA",
       default='anthropic',
       config_parameter='eazynova.ai_provider'
    )
    
    ai_api_key = fields.Char(
        string="Clé API IA",
        help="Clé API pour le fournisseur IA sélectionné",
        config_parameter='eazynova.ai_api_key'
    )
    
    # OCR (Reconnaissance de caractères)
    ocr_enabled = fields.Boolean(
        string="Activer l'OCR",
        default=True,
        help="Active la reconnaissance de caractères pour l'import de documents",
        config_parameter='eazynova.ocr_enabled'
    )
    
    # Gestion documentaire
    document_management_enabled = fields.Boolean(
        string="Gestion documentaire avancée",
        default=True,
        help="Active la gestion documentaire par affaire/chantier",
        config_parameter='eazynova.document_management_enabled'
    )
    
    @api.constrains('facial_recognition_tolerance')
    def _check_tolerance(self):
        """
        Vérifie que la tolérance de reconnaissance faciale est dans les limites acceptables
        """
        for record in self:
            if record.facial_recognition_tolerance and not (0.0 <= record.facial_recognition_tolerance <= 1.0):
                raise ValidationError(_("La tolérance doit être comprise entre 0.0 et 1.0"))
    
    @api.onchange('facial_recognition_enabled')
    def _onchange_facial_recognition(self):
        """
        Avertissement lors de l'activation de la reconnaissance faciale
        """
        if self.facial_recognition_enabled:
            return {
                'warning': {
                    'title': _("Reconnaissance faciale"),
                    'message': _("L'activation de la reconnaissance faciale nécessite :\n"
                               "- Le consentement explicite des utilisateurs (RGPD)\n"
                               "- Une connexion HTTPS sécurisée\n"
                               "- L'installation de dépendances Python (face_recognition, opencv)"),
                }
            }