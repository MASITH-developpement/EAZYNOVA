# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA - Gestion d\'Entreprise',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Module principal de gestion d\'entreprise EAZYNOVA avec IA et reconnaissance faciale',
    'description': """
        EAZYNOVA - Solution de Gestion d'Entreprise
        ============================================
        
        Module principal fournissant :
        * Tableau de bord analytique intelligent
        * Gestion des paramètres globaux
        * Authentification par reconnaissance faciale (optionnelle)
        * Base pour les modules complémentaires (Chantier, Facture, Frais, Compta, Stock)
        * Intégration IA pour l'assistance
        * OCR et gestion documentaire
        
        Sécurité : Conforme RGPD et normes Odoo 19
        Performance : Optimisé pour production
    """,
    'author': 'EAZYNOVA',
    'website': 'https://eazynova-production.up.railway.app/',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
        'portal',
    ],
    'data': [
        # Sécurité (toujours en premier)
        'security/eazynova_security.xml',
        'security/ir.model.access.csv',
        
        # Données
        'data/eazynova_data.xml',
        
        # Vues principales
        'views/eazynova_dashboard_views.xml',
        'views/res_config_settings_views.xml',
        'views/eazynova_menu.xml',
        'views/res_company_views.xml',
        'views/res_users_views.xml',
        # Wizards
        'wizard/ai_assistant_wizard_views.xml',
        'wizard/document_ocr_wizard_views.xml',
        'wizard/facial_registration_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'eazynova/static/src/js/dashboard.js',
            'eazynova/static/src/xml/dashboard.xml',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
}