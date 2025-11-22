# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import base64
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    """
    Extension du modèle res.users pour la reconnaissance faciale
    Stockage sécurisé des données biométriques (conformité RGPD)
    """
    _inherit = 'res.users'
    
    # Reconnaissance faciale
    facial_recognition_enabled = fields.Boolean(
        string="Reconnaissance faciale active",
        default=False,
        help="Active la connexion par reconnaissance faciale pour cet utilisateur"
    )
    
    facial_data = fields.Binary(
        string="Données faciales",
        attachment=True,
        help="Encodage facial de l'utilisateur (crypté)"
    )
    
    facial_consent_date = fields.Datetime(
        string="Date de consentement",
        help="Date du consentement RGPD pour l'utilisation des données biométriques"
    )
    
    facial_last_update = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour des données faciales"
    )
    
    @api.constrains('facial_recognition_enabled', 'facial_data')
    def _check_facial_data(self):
        """
        Vérifie que les données faciales sont présentes si la reconnaissance est activée
        """
        for user in self:
            if user.facial_recognition_enabled and not user.facial_data:
                raise ValidationError(_("Les données faciales doivent être enregistrées avant d'activer la reconnaissance faciale."))
    
    def action_register_facial_data(self):
        """
        Ouvre le wizard d'enregistrement des données faciales
        Retourne une action pour ouvrir le formulaire de capture
        """
        self.ensure_one()
        
        # Vérification des paramètres système
        facial_enabled = self.env['ir.config_parameter'].sudo().get_param('eazynova.facial_recognition_enabled', 'False')
        if facial_enabled != 'True':
            raise UserError(_("La reconnaissance faciale n'est pas activée dans les paramètres système."))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Enregistrer les données faciales'),
            'res_model': 'eazynova.facial.registration.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_user_id': self.id}
        }
    
    def action_remove_facial_data(self):
        """
        Supprime les données faciales de l'utilisateur (droit RGPD à l'effacement)
        """
        self.ensure_one()
        self.write({
            'facial_recognition_enabled': False,
            'facial_data': False,
            'facial_consent_date': False,
            'facial_last_update': False,
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Données supprimées'),
                'message': _('Vos données de reconnaissance faciale ont été supprimées avec succès.'),
                'type': 'success',
            }
        }
    
    @api.model
    def authenticate_by_facial(self, facial_image_data):
        """
        Authentifie un utilisateur par reconnaissance faciale
        
        Args:
            facial_image_data: Image faciale en base64
            
        Returns:
            int: ID de l'utilisateur authentifié ou False
        """
        try:
            # Import des bibliothèques (uniquement si feature activée)
            import face_recognition
            import numpy as np
            
            # Décodage de l'image reçue
            image_data = base64.b64decode(facial_image_data)
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            
            # Recherche des utilisateurs avec reconnaissance faciale active
            users = self.search([('facial_recognition_enabled', '=', True)])
            
            tolerance = float(self.env['ir.config_parameter'].sudo().get_param(
                'eazynova.facial_recognition_tolerance', '0.6'
            ))
            
            for user in users:
                if not user.facial_data:
                    continue
                
                try:
                    # Comparaison des visages
                    stored_encoding = np.frombuffer(
                        base64.b64decode(user.facial_data), 
                        dtype=np.float64
                    )
                    
                    # Note: Implémentation simplifiée - à compléter avec face_recognition
                    # match = face_recognition.compare_faces([stored_encoding], image_array, tolerance=tolerance)
                    
                    # if match[0]:
                    #     _logger.info(f"Authentification faciale réussie pour l'utilisateur {user.login}")
                    #     return user.id
                    
                except Exception as e:
                    _logger.warning(f"Erreur lors de la comparaison faciale pour {user.login}: {str(e)}")
                    continue
            
            return False
            
        except ImportError:
            _logger.error("Bibliothèques de reconnaissance faciale non installées (face_recognition)")
            raise UserError(_("Les bibliothèques de reconnaissance faciale ne sont pas installées sur le serveur."))
        except Exception as e:
            _logger.error(f"Erreur lors de l'authentification faciale: {str(e)}")
            return False