# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA Chantier',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Gestion de chantiers avec IA et gestion documentaire',
    'author': 'EAZYNOVA',
    'website': 'https://eazynova-production.up.railway.app/',
    'license': 'LGPL-3',
    'depends': ['eazynova'],
    'data': [
        'security/ir.model.access.csv',
        'data/chantier_sequence.xml',
        'views/chantier_menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
