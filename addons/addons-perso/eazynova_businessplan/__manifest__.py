# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA - Business Plan',
    'version': '19.0.1.0.0',
    'category': 'Productivity/Management',
    'summary': 'Gestion de business plans avec génération automatique d\'indicateurs de suivi',
    'description': """
        EAZYNOVA - Business Plan
        =========================

        Module de gestion de business plans permettant :
        * Création et suivi de business plans structurés
        * Validation workflow avec états
        * Génération automatique d'indicateurs de suivi
        * Tableau de bord avec KPIs
        * Analyses financières et prévisionnelles
        * Suivi des objectifs et réalisations

        Ce module s'intègre avec les modules comptables et de gestion d'EAZYNOVA.
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
        # Sécurité
        'security/businessplan_security.xml',
        'security/ir.model.access.csv',

        # Données
        'data/sequence_data.xml',
        'data/indicator_templates.xml',

        # Vues
        'views/business_plan_views.xml',
        'views/business_plan_indicator_views.xml',
        'views/businessplan_menu.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
