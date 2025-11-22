# -*- coding: utf-8 -*-
"""
Module EAZYNOVA - Gestion d'Entreprise
Initialisation des composants du module
"""

from . import models
from . import wizard
from . import controllers

import os
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """
    Hook post-installation pour configurer les paramètres par défaut
    
    1. Configure les valeurs par défaut
    2. Synchronise avec les variables d'environnement Railway (si présentes)
    3. Log les configurations pour debug
    
    Args:
        env: Environnement Odoo
    """
    _logger.info("=" * 60)
    _logger.info("EAZYNOVA - Initialisation du module")
    _logger.info("=" * 60)
    
    # Configuration de la société par défaut
    company = env['res.company'].search([], limit=1)
    if company:
        _logger.info("Société trouvée: %s", company.name)
    
    # ========================================
    # ÉTAPE 1: Paramètres par défaut
    # ========================================
    default_params = {
        'eazynova.facial_recognition_enabled': 'False',
        'eazynova.facial_recognition_tolerance': '0.6',
        'eazynova.ai_assistance_enabled': 'True',
        'eazynova.ai_provider': 'anthropic',
        'eazynova.ocr_enabled': 'True',
        'eazynova.document_management_enabled': 'True',
    }
    
    _logger.info("Configuration des paramètres par défaut...")
    for param_key, default_value in default_params.items():
        env['ir.config_parameter'].sudo().set_param(param_key, default_value)
        _logger.info("  ✓ %s = %s", param_key, default_value)
    
    # ========================================
    # ÉTAPE 2: Synchronisation avec Railway
    # ========================================
    _logger.info("Synchronisation avec les variables d'environnement Railway...")
    
    # Mapping: Variable d'environnement Railway → Paramètre Odoo
    env_to_param = {
        'EAZYNOVA_AI_ENABLED': ('eazynova.ai_assistance_enabled', 'boolean'),
        'EAZYNOVA_AI_PROVIDER': ('eazynova.ai_provider', 'string'),
        'EAZYNOVA_AI_API_KEY': ('eazynova.ai_api_key', 'secret'),
        'EAZYNOVA_FACIAL_ENABLED': ('eazynova.facial_recognition_enabled', 'boolean'),
        'EAZYNOVA_FACIAL_TOLERANCE': ('eazynova.facial_recognition_tolerance', 'float'),
        'EAZYNOVA_OCR_ENABLED': ('eazynova.ocr_enabled', 'boolean'),
        'EAZYNOVA_OCR_LANGUAGE': ('eazynova.ocr_language', 'string'),
        'EAZYNOVA_DOCUMENT_MANAGEMENT_ENABLED': ('eazynova.document_management_enabled', 'boolean'),
    }
    
    synced_count = 0
    for env_var, (param_key, param_type) in env_to_param.items():
        value = os.environ.get(env_var)
        
        if value:
            # Conversion selon le type
            if param_type == 'boolean':
                # Convertir 'true'/'false' en 'True'/'False' pour Odoo
                value = 'True' if value.lower() in ['true', '1', 'yes'] else 'False'
            elif param_type == 'float':
                # Valider que c'est bien un float
                try:
                    float(value)
                except ValueError:
                    _logger.warning("  ⚠️  %s: valeur invalide '%s', ignorée", env_var, value)
                    continue
            elif param_type == 'secret':
                # Masquer les secrets dans les logs
                log_value = value[:10] + "..." if len(value) > 10 else "***"
                _logger.info("  ✓ %s → %s = %s", env_var, param_key, log_value)
                env['ir.config_parameter'].sudo().set_param(param_key, value)
                synced_count += 1
                continue
            
            # Enregistrer le paramètre
            env['ir.config_parameter'].sudo().set_param(param_key, value)
            _logger.info("  ✓ %s → %s = %s", env_var, param_key, value)
            synced_count += 1
        else:
            _logger.debug("  ○ %s: non définie (utilisation valeur par défaut)", env_var)
    
    if synced_count > 0:
        _logger.info("✅ %d variable(s) Railway synchronisée(s)", synced_count)
    else:
        _logger.info("ℹ️  Aucune variable Railway trouvée, utilisation des valeurs par défaut")
    
    # ========================================
    # ÉTAPE 3: Vérifications et warnings
    # ========================================
    _logger.info("Vérification de la configuration...")
    
    # Vérifier la clé API IA
    ai_enabled = env['ir.config_parameter'].sudo().get_param('eazynova.ai_assistance_enabled', 'False')
    ai_api_key = env['ir.config_parameter'].sudo().get_param('eazynova.ai_api_key', '')
    
    if ai_enabled == 'True' and not ai_api_key:
        _logger.warning("⚠️  L'assistance IA est activée mais aucune clé API n'est configurée!")
        _logger.warning("⚠️  Ajoutez la variable EAZYNOVA_AI_API_KEY dans Railway")
    
    # Vérifier Tesseract pour l'OCR
    ocr_enabled = env['ir.config_parameter'].sudo().get_param('eazynova.ocr_enabled', 'False')
    if ocr_enabled == 'True':
        try:
            import pytesseract
            tesseract_version = pytesseract.get_tesseract_version()
            _logger.info("  ✓ Tesseract OCR détecté: v%s", tesseract_version)
        except Exception as e:
            _logger.warning("⚠️  OCR activé mais Tesseract non trouvé: %s", str(e))
            _logger.warning("⚠️  Installez Tesseract ou désactivez l'OCR")
    
    # Vérifier face_recognition pour la reconnaissance faciale
    facial_enabled = env['ir.config_parameter'].sudo().get_param('eazynova.facial_recognition_enabled', 'False')
    if facial_enabled == 'True':
        try:
            import face_recognition
            _logger.info("  ✓ Bibliothèque face_recognition détectée")
        except ImportError:
            _logger.warning("⚠️  Reconnaissance faciale activée mais face_recognition non installé")
            _logger.warning("⚠️  Installez face_recognition ou désactivez la fonctionnalité")
    
    # ========================================
    # ÉTAPE 4: Résumé de la configuration
    # ========================================
    _logger.info("=" * 60)
    _logger.info("RÉSUMÉ DE LA CONFIGURATION EAZYNOVA")
    _logger.info("=" * 60)
    _logger.info("Intelligence Artificielle:")
    _logger.info("  - Activée: %s", ai_enabled)
    _logger.info("  - Provider: %s", env['ir.config_parameter'].sudo().get_param('eazynova.ai_provider', 'N/A'))
    _logger.info("  - Clé API: %s", "Configurée ✓" if ai_api_key else "Non configurée ✗")
    _logger.info("")
    _logger.info("Reconnaissance Faciale:")
    _logger.info("  - Activée: %s", facial_enabled)
    _logger.info("  - Tolérance: %s", env['ir.config_parameter'].sudo().get_param('eazynova.facial_recognition_tolerance', 'N/A'))
    _logger.info("")
    _logger.info("OCR:")
    _logger.info("  - Activé: %s", ocr_enabled)
    _logger.info("  - Langue: %s", env['ir.config_parameter'].sudo().get_param('eazynova.ocr_language', 'fra'))
    _logger.info("")
    _logger.info("Gestion Documentaire:")
    _logger.info("  - Activée: %s", env['ir.config_parameter'].sudo().get_param('eazynova.document_management_enabled', 'N/A'))
    _logger.info("=" * 60)
    _logger.info("✅ Initialisation EAZYNOVA terminée avec succès")
    _logger.info("=" * 60)