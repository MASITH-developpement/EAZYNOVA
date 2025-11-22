# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessDenied
import json
import logging
import base64

_logger = logging.getLogger(__name__)


class EazynovaController(http.Controller):
    """
    Contrôleur principal EAZYNOVA
    Gestion des endpoints pour IA, OCR et reconnaissance faciale
    """
    
    @http.route('/eazynova/facial/authenticate', type='json', auth='none', csrf=False)
    def facial_authenticate(self, **kw):
        """
        Endpoint d'authentification par reconnaissance faciale
        
        Args:
            image_data: Image faciale en base64
            db: Nom de la base de données
            
        Returns:
            dict: {'success': bool, 'uid': int, 'session_id': str}
        """
        try:
            # Vérification des paramètres
            if not kw.get('image_data') or not kw.get('db'):
                return {'success': False, 'error': _('Paramètres manquants')}
            
            # Vérification que la fonctionnalité est activée
            db = kw.get('db')
            registry = http.Registry(db)
            
            with registry.cursor() as cr:
                env = http.Environment(cr, http.SUPERUSER_ID, {})
                
                facial_enabled = env['ir.config_parameter'].sudo().get_param(
                    'eazynova.facial_recognition_enabled', 'False'
                )
                
                if facial_enabled != 'True':
                    return {
                        'success': False, 
                        'error': _('La reconnaissance faciale n\'est pas activée')
                    }
                
                # Authentification
                user_id = env['res.users'].sudo().authenticate_by_facial(
                    kw.get('image_data')
                )
                
                if user_id:
                    # Création de session
                    user = env['res.users'].sudo().browse(user_id)
                    
                    # Log de connexion
                    _logger.info(f"Authentification faciale réussie pour {user.login}")
                    
                    return {
                        'success': True,
                        'uid': user_id,
                        'username': user.login,
                        'name': user.name
                    }
                else:
                    return {
                        'success': False,
                        'error': _('Reconnaissance faciale échouée')
                    }
                    
        except Exception as e:
            _logger.error(f"Erreur d'authentification faciale: {str(e)}")
            return {
                'success': False,
                'error': _('Erreur serveur lors de l\'authentification')
            }
    
    @http.route('/eazynova/ai/assist', type='json', auth='user')
    def ai_assist(self, **kw):
        """
        Endpoint pour l'assistance IA
        
        Args:
            query: Question de l'utilisateur
            context: Contexte additionnel (optionnel)
            
        Returns:
            dict: {'success': bool, 'response': str}
        """
        try:
            # Vérification que l'IA est activée
            ai_enabled = request.env['ir.config_parameter'].sudo().get_param(
                'eazynova.ai_assistance_enabled', 'False'
            )
            
            if ai_enabled != 'True':
                return {
                    'success': False,
                    'error': _('L\'assistance IA n\'est pas activée')
                }
            
            query = kw.get('query', '')
            context = kw.get('context', {})
            
            if not query:
                return {'success': False, 'error': _('Question vide')}
            
            # TODO: Intégration avec l'API IA (OpenAI, Anthropic, etc.)
            # Pour l'instant, réponse mockée
            response = self._process_ai_query(query, context)
            
            return {
                'success': True,
                'response': response
            }
            
        except Exception as e:
            _logger.error(f"Erreur assistance IA: {str(e)}")
            return {
                'success': False,
                'error': _('Erreur lors du traitement de la requête')
            }
    
    def _process_ai_query(self, query, context):
        """
        Traite une requête IA (à implémenter avec l'API choisie)
        
        Args:
            query: Question
            context: Contexte
            
        Returns:
            str: Réponse de l'IA
        """
        # Récupération du provider
        provider = request.env['ir.config_parameter'].sudo().get_param(
            'eazynova.ai_provider', 'anthropic'
        )
        api_key = request.env['ir.config_parameter'].sudo().get_param(
            'eazynova.ai_api_key', ''
        )
        
        if not api_key:
            return _("Configuration IA incomplète. Veuillez configurer la clé API.")
        
        # TODO: Implémenter l'appel API selon le provider
        if provider == 'anthropic':
            return self._call_anthropic_api(query, context, api_key)
        elif provider == 'openai':
            return self._call_openai_api(query, context, api_key)
        else:
            return _("Provider IA non supporté")
    
    def _call_anthropic_api(self, query, context, api_key):
        """
        Appel à l'API Anthropic Claude
        """
        # TODO: Implémenter l'appel réel
        return f"Réponse IA (Anthropic) pour: {query}"
    
    def _call_openai_api(self, query, context, api_key):
        """
        Appel à l'API OpenAI
        """
        # TODO: Implémenter l'appel réel
        return f"Réponse IA (OpenAI) pour: {query}"
    
    @http.route('/eazynova/ocr/process', type='json', auth='user')
    def ocr_process(self, **kw):
        """
        Endpoint pour le traitement OCR de documents
        
        Args:
            document: Document en base64
            document_type: Type de document (facture, contrat, etc.)
            
        Returns:
            dict: {'success': bool, 'text': str, 'data': dict}
        """
        try:
            # Vérification que l'OCR est activé
            ocr_enabled = request.env['ir.config_parameter'].sudo().get_param(
                'eazynova.ocr_enabled', 'False'
            )
            
            if ocr_enabled != 'True':
                return {
                    'success': False,
                    'error': _('L\'OCR n\'est pas activé')
                }
            
            document = kw.get('document', '')
            document_type = kw.get('document_type', 'generic')
            
            if not document:
                return {'success': False, 'error': _('Document manquant')}
            
            # TODO: Implémenter le traitement OCR avec Tesseract ou API cloud
            result = self._process_ocr(document, document_type)
            
            return {
                'success': True,
                'text': result.get('text', ''),
                'data': result.get('data', {})
            }
            
        except Exception as e:
            _logger.error(f"Erreur OCR: {str(e)}")
            return {
                'success': False,
                'error': _('Erreur lors du traitement OCR')
            }
    
    def _process_ocr(self, document, document_type):
        """
        Traite un document avec OCR
        
        Args:
            document: Document base64
            document_type: Type de document
            
        Returns:
            dict: Résultat OCR
        """
        # TODO: Implémenter avec Tesseract, Google Vision, etc.
        return {
            'text': 'Texte extrait du document...',
            'data': {
                'confidence': 0.95,
                'language': 'fr'
            }
        }
    
    @http.route('/eazynova/dashboard/data', type='json', auth='user')
    def dashboard_data(self, **kw):
        """
        Récupère les données pour le tableau de bord
        
        Returns:
            dict: Données du tableau de bord
        """
        try:
            company = request.env.company
            
            # Statistiques de base
            data = {
                'company': {
                    'name': company.name,
                    'code': company.eazynova_code or 'N/A',
                },
                'stats': {
                    'chantiers': company.total_chantiers,
                    'factures': company.total_factures,
                },
                'user': {
                    'name': request.env.user.name,
                    'facial_enabled': request.env.user.facial_recognition_enabled,
                }
            }
            
            # Ajout des données des modules installés
            if request.env['ir.module.module'].search([
                ('name', '=', 'eazynova_chantier'),
                ('state', '=', 'installed')
            ]):
                # TODO: Ajouter données chantiers
                pass
            
            return {'success': True, 'data': data}
            
        except Exception as e:
            _logger.error(f"Erreur récupération données dashboard: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            