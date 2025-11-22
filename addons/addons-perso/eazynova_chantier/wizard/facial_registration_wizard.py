# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging

_logger = logging.getLogger(__name__)


class FacialRegistrationWizard(models.TransientModel):
    """
    Wizard pour l'enregistrement des données de reconnaissance faciale
    Capture et traitement de l'image faciale de l'utilisateur
    """
    _name = 'eazynova.facial.registration.wizard'
    _description = 'Assistant Enregistrement Reconnaissance Faciale'
    
    user_id = fields.Many2one(
        'res.users',
        string="Utilisateur",
        required=True,
        default=lambda self: self.env.user
    )
    
    facial_image = fields.Binary(
        string="Image faciale",
        required=True,
        help="Photo de votre visage pour la reconnaissance"
    )
    
    facial_image_filename = fields.Char(
        string="Nom du fichier"
    )
    
    consent_gdpr = fields.Boolean(
        string="Je consens",
        help="Je consens au traitement de mes données biométriques"
    )
    
    state = fields.Selection([
        ('capture', 'Capture'),
        ('process', 'Traitement'),
        ('confirm', 'Confirmation'),
    ], default='capture',
       string="État"
    )
    
    quality_score = fields.Float(
        string="Score qualité",
        readonly=True,
        help="Score de qualité de l'image (0-100)"
    )
    
    error_message = fields.Text(
        string="Message d'erreur",
        readonly=True
    )
    
    @api.constrains('consent_gdpr')
    def _check_consent(self):
        """
        Vérifie que le consentement RGPD est donné
        """
        for wizard in self:
            if not wizard.consent_gdpr:
                raise ValidationError(_("Le consentement RGPD est obligatoire pour activer la reconnaissance faciale."))
    
    def action_process_image(self):
        """
        Traite l'image faciale et extrait les caractéristiques
        """
        self.ensure_one()
        
        if not self.facial_image:
            raise UserError(_("Veuillez capturer une image avant de continuer."))
        
        if not self.consent_gdpr:
            raise UserError(_("Vous devez consentir au traitement de vos données biométriques."))
        
        try:
            # Import des bibliothèques
            import face_recognition
            import numpy as np
            from PIL import Image
            import io
            
            # Décodage de l'image
            image_data = base64.b64decode(self.facial_image)
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            # Détection des visages
            face_locations = face_recognition.face_locations(image_array)
            
            if len(face_locations) == 0:
                self.write({
                    'state': 'capture',
                    'error_message': _("Aucun visage détecté. Veuillez reprendre une photo avec votre visage bien visible."),
                    'quality_score': 0.0
                })
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': self._name,
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }
            
            if len(face_locations) > 1:
                self.write({
                    'state': 'capture',
                    'error_message': _("Plusieurs visages détectés. Assurez-vous d'être seul sur la photo."),
                    'quality_score': 0.0
                })
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': self._name,
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }
            
            # Encodage du visage
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if len(face_encodings) == 0:
                self.write({
                    'state': 'capture',
                    'error_message': _("Impossible d'encoder le visage. Veuillez améliorer la qualité de l'image."),
                    'quality_score': 0.0
                })
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': self._name,
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }
            
            face_encoding = face_encodings[0]
            
            # Calcul du score de qualité (simplifié)
            quality_score = self._calculate_quality_score(face_locations[0], image.size)
            
            if quality_score < 60:
                self.write({
                    'state': 'capture',
                    'error_message': _("Qualité de l'image insuffisante (score: %.1f/100). Assurez-vous d'avoir un bon éclairage et que votre visage est bien visible.") % quality_score,
                    'quality_score': quality_score
                })
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': self._name,
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }
            
            # Encodage en base64 pour stockage
            encoding_bytes = face_encoding.tobytes()
            encoding_base64 = base64.b64encode(encoding_bytes).decode('utf-8')
            
            # Mise à jour de l'utilisateur
            self.user_id.sudo().write({
                'facial_data': encoding_base64,
                'facial_recognition_enabled': True,
                'facial_consent_date': fields.Datetime.now(),
                'facial_last_update': fields.Datetime.now(),
            })
            
            self.write({
                'state': 'confirm',
                'quality_score': quality_score,
                'error_message': False
            })
            
            _logger.info(f"Données faciales enregistrées pour l'utilisateur {self.user_id.login} (qualité: {quality_score:.1f})")
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
            
        except ImportError:
            raise UserError(_("Les bibliothèques de reconnaissance faciale ne sont pas installées sur le serveur.\n\nContactez votre administrateur."))
        except Exception as e:
            _logger.error(f"Erreur lors du traitement de l'image faciale: {str(e)}")
            raise UserError(_("Erreur lors du traitement de l'image: %s") % str(e))
    
    def _calculate_quality_score(self, face_location, image_size):
        """
        Calcule un score de qualité de l'image
        
        Args:
            face_location: Tuple (top, right, bottom, left)
            image_size: Tuple (width, height)
            
        Returns:
            float: Score de 0 à 100
        """
        top, right, bottom, left = face_location
        width, height = image_size
        
        # Taille du visage
        face_width = right - left
        face_height = bottom - top
        face_area = face_width * face_height
        image_area = width * height
        
        # Le visage devrait occuper entre 15% et 60% de l'image
        face_ratio = (face_area / image_area) * 100
        
        score = 100.0
        
        # Pénalité si le visage est trop petit
        if face_ratio < 15:
            score -= (15 - face_ratio) * 3
        
        # Pénalité si le visage est trop grand
        if face_ratio > 60:
            score -= (face_ratio - 60) * 2
        
        # Pénalité si le visage n'est pas centré
        face_center_x = (left + right) / 2
        face_center_y = (top + bottom) / 2
        image_center_x = width / 2
        image_center_y = height / 2
        
        offset_x = abs(face_center_x - image_center_x) / width
        offset_y = abs(face_center_y - image_center_y) / height
        
        if offset_x > 0.2:
            score -= (offset_x - 0.2) * 100
        if offset_y > 0.2:
            score -= (offset_y - 0.2) * 100
        
        return max(0.0, min(100.0, score))
    
    def action_confirm(self):
        """
        Confirme l'enregistrement
        """
        self.ensure_one()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Reconnaissance faciale activée'),
                'message': _('Vos données de reconnaissance faciale ont été enregistrées avec succès (qualité: %.1f/100).') % self.quality_score,
                'type': 'success',
                'sticky': False,
            }
        }