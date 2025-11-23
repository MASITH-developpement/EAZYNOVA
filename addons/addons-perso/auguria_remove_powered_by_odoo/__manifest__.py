# -*- coding: utf-8 -*-
# Copyright (C) 2022 - Auguria (<https://www.auguria.fr>).
{
    'name': 'Remove Powered By Odoo',
    'version': '19.0.0.1',
    'author': 'Auguria SAS',
    'license': 'LGPL-3',
    'category': 'Email',
    'website': 'https://www.auguria.fr/en/blog/modules-odoo-auguria-9/remove-powered-by-odoo-249',
    'images': ['static/description/banner.png'],
    'summary': 'Remove Powered By Odoo',
    'description': """Remove power by odoo on footer of emails and the website""",
    'depends': ['base', 'mail', 'web'],
    'data': [
        'views/mail_template_remove_odoo_views.xml',
        'views/website_footer_brand_promotion.xml'
    ],
    'images':['static/description/cover.png'],
    'installable': True,
    'support': 'support@auguria.fr',
    'application': True,
}
