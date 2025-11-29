# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA - Business Plan (Simplifié)',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Gestion simple de business plans avec indicateurs',
    'description': """
        Business Plan Simple
        ====================

        Module simple pour gérer vos business plans :
        * Créer un business plan (nom, dates, objectif financier)
        * Valider pour générer des indicateurs automatiquement
        * Suivre la progression de vos indicateurs
        * Interface simple et facile à utiliser
    """,
    'author': 'EAZYNOVA',
    'website': 'https://eazynova-production.up.railway.app/',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/businessplan_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/business_plan_views.xml',
        'views/business_plan_indicator_views.xml',
        'views/businessplan_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
