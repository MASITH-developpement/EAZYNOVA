# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA Chantier',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Gestion de chantiers avec IA et gestion documentaire',
    'description': """
        EAZYNOVA Chantier
        =================
        
        Fonctionnalités :
        * Gestion complète des chantiers
        * Suivi des tâches et planning
        * Gestion documentaire par chantier
        * Assistant IA intégré
        * OCR pour import de documents
        * Suivi budgétaire et main d'œuvre
        * Rapports et analyses
        
        Intégration avec :
        * EAZYNOVA Facture
        * EAZYNOVA Frais
        * EAZYNOVA Stock
        * EAZYNOVA Compta
    """,
    'author': 'EAZYNOVA',
    'website': 'https://eazynova-production.up.railway.app/',
    'license': 'LGPL-3',
    'depends': [
        'eazynova',
        'project',
        'hr',
        'documents',
    ],
    'data': [
        # Aucun fichier XML présent, à compléter si besoin
    ],
    'assets': {
        'web.assets_backend': [
            'eazynova_chantier/static/src/js/chantier_kanban.js',
            'eazynova_chantier/static/src/xml/chantier_kanban.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}