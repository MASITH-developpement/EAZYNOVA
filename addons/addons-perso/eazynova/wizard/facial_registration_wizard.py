# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class FacialRegistrationWizard(models.TransientModel):
    """Wizard pour l'enregistrement facial"""
    _name = 'eazynova.facial.registration.wizard'
    _description = 'Enregistrement Facial'

    user_id = fields.Many2one(
        'res.users',
        string='Utilisateur',
        required=True,
        default=lambda self: self.env.user
    )

    photo = fields.Binary(
        string='Photo',
        required=True,
        attachment=False,
        help="Photo pour l'enregistrement facial"
    )

    photo_source = fields.Selection(
        [('upload', 'Upload'), ('webcam', 'Webcam')],
        string='Source Photo',
        default='webcam'
    )

    state = fields.Selection(
        [('draft', 'Brouillon'), ('processing', 'Traitement'), ('done', 'Terminé')],
        string='État',
        default='draft'
    )

    result_message = fields.Text(
        string='Résultat',
        readonly=True
    )

    face_count = fields.Integer(
        string='Visages Détectés',
        readonly=True
    )

    quality_score = fields.Float(
        string='Score de Qualité',
        readonly=True
    )

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """Vérifier si l'utilisateur a déjà un enregistrement facial actif"""
        if self.user_id:
            existing = self.env['eazynova.facial.data'].search([
                ('user_id', '=', self.user_id.id),
                ('active', '=', True)
            ], limit=1)

            if existing:
                return {
                    'warning': {
                        'title': _('Enregistrement Existant'),
                        'message': _(
                            "L'utilisateur %s a déjà un enregistrement facial actif. "
                            "Continuer remplacera l'enregistrement existant."
                        ) % self.user_id.name
                    }
                }

    def action_register(self):
        """Enregistre la photo faciale"""
        self.ensure_one()

        if not self.photo:
            raise UserError(_("Veuillez fournir une photo pour l'enregistrement."))

        try:
            # Mettre à jour l'état
            self.state = 'processing'

            # Appeler le service de reconnaissance faciale
            facial_service = self.env['eazynova.facial.service']
            result = facial_service.register_face(
                self.photo,
                self.user_id.id
            )

            if not result.get('success'):
                raise UserError(_(
                    "Erreur lors de l'enregistrement facial: %s"
                ) % result.get('error', 'Erreur inconnue'))

            # Désactiver les anciens enregistrements
            old_records = self.env['eazynova.facial.data'].search([
                ('user_id', '=', self.user_id.id),
                ('active', '=', True)
            ])
            if old_records:
                old_records.write({'active': False})
                old_records.message_post(
                    body=_("Désactivé - Nouvel enregistrement facial créé")
                )

            # Créer le nouvel enregistrement facial
            facial_data = self.env['eazynova.facial.data'].create({
                'user_id': self.user_id.id,
                'photo': self.photo,
                'encoding_data': result.get('encoding'),
                'face_count': result.get('face_count', 0),
                'quality_score': result.get('quality_score', 0),
            })

            # Mettre à jour les résultats du wizard
            self.write({
                'state': 'done',
                'face_count': result.get('face_count', 0),
                'quality_score': result.get('quality_score', 0),
                'result_message': _(
                    "✅ Enregistrement facial réussi!\n\n"
                    "Visages détectés: %d\n"
                    "Score de qualité: %.1f%%\n\n"
                    "%s"
                ) % (
                    result.get('face_count', 0),
                    result.get('quality_score', 0),
                    result.get('message', '')
                )
            })

            _logger.info(
                f"Enregistrement facial créé pour {self.user_id.name} "
                f"(ID: {facial_data.id})"
            )

            # Retourner le wizard avec les résultats
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'eazynova.facial.registration.wizard',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_state': 'done'}
            }

        except Exception as e:
            _logger.exception("Erreur lors de l'enregistrement facial")
            self.state = 'draft'
            raise UserError(_(
                "Erreur lors de l'enregistrement facial:\n%s"
            ) % str(e))

    def action_cancel(self):
        """Annuler le wizard"""
        return {'type': 'ir.actions.act_window_close'}

    def action_reset(self):
        """Réinitialiser le wizard pour un nouvel enregistrement"""
        self.ensure_one()
        self.write({
            'state': 'draft',
            'photo': False,
            'result_message': False,
            'face_count': 0,
            'quality_score': 0
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'eazynova.facial.registration.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
