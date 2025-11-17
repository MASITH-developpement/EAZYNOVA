# -*- coding: utf-8 -*-
{
    'name': 'Odoo SaaS Manager',
    'version': '19.0.1.0.0',
    'category': 'SaaS',
    'summary': 'Gestion complète des clients SaaS et abonnements',
    'description': """
        Module SaaS pour Odoo 19
        ========================
        * Gestion multi-clients (tenants)
        * Plans d'abonnement flexibles
        * Isolation complète des données
        * Facturation automatique
        * Gestion des limites d'utilisation
        * Dashboard analytics
    """,
    'author': 'Eazynova',
    'website': 'https://www.eazynova.com',
    'depends': [
        'base',
        'mail',
        'web',
    ],
    'data': [
        # Sécurité - À charger en premier
        'security/saas_security.xml',
        'security/ir.model.access.csv',

        # Données initiales
        'data/saas_data.xml',

        # Vues
        'views/saas_client_views.xml',
        'views/saas_plan_views.xml',
        'views/saas_subscription_views.xml',
        'views/saas_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
