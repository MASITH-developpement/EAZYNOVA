# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA - Gestion de Chantiers',
    'version': '19.0.1.0.0',
    'category': 'Construction',
    'summary': 'Gestion complète des chantiers de construction',
    'description': """
        EAZYNOVA - Gestion de Chantiers
        ================================
        
        Fonctionnalités :
        * Création et suivi de chantiers
        * Géolocalisation GPS
        * Gestion des phases et tâches
        * Affectation d'équipes
        * Suivi budgétaire par chantier
        * Planning des interventions
        * Documents par chantier
        * Historique complet
        * Rapports et analyses
    """,
    'author': 'EAZYNOVA',
    'website': 'https://eazynova-production.up.railway.app/',
    'license': 'LGPL-3',
    'depends': [
        'eazynova',  # Module CORE requis
        'project',   # Utilise la gestion de projets Odoo
    ],
    'data': [
        # Sécurité
        'security/chantier_security.xml',
        'security/ir.model.access.csv',
        
        # Données
        'data/chantier_data.xml',
        'data/chantier_sequence.xml',
        
        # Vues
        'views/eazynova_chantier_views.xml',
        'views/eazynova_chantier_phase_views.xml',
        'views/eazynova_chantier_tache_views.xml',
        'views/eazynova_chantier_equipe_views.xml',
        'views/chantier_menu.xml',
        
        # Rapports
        'report/chantier_report_views.xml',
        'report/chantier_report_templates.xml',
    ],
    'demo': [
        'demo/chantier_demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}