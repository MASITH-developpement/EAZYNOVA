# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Odoo OCR Using AI - Purchase Order',
    'version': '19.0.1.0.0',
    'summary': """
                Transform your purchase order processing with the Odoo OCR Using AI app! This powerful tool leverages advanced optical character recognition (OCR) technology and artificial intelligence to streamline the capture and management of purchase orders within your Odoo environment.
                Odoo OCR AI
                AI-based OCR in Odoo
                Odoo OCR integration
                Odoo OCR document processing
                Odoo AI text recognition
                Odoo OCR AI implementation
                Intelligent OCR Odoo
                Automated OCR Odoo
                Odoo OCR solution
                AI OCR Odoo application
                Odoo OCR AI technology
                Optical Character Recognition
                Odoo OCR
                AI-Driven OCR
                AI Document Processing
                OCR AI Integration
                OCR Invoice & Bills
                OCR Sale Order
                OCR Purchase Order
                    OCR Expense
                """,
    'sequence': 10,
    'description': """
        Transform your purchase order processing with the Odoo OCR Using AI app! This powerful 
        tool leverages advanced optical character recognition (OCR) technology and artificial 
        intelligence to streamline the capture and management of purchase orders within your 
        Odoo environment.""",
    'category': 'tools',
    'website': "https://techultrasolutions.com",
    "author": "TechUltra Solutions Private Limited",
    'live_test_url': 'https://ai.fynix.app/',
    'depends': ["purchase", "tus_odoo_ocr_ai_base", "base"],
    'data': [
        'data/ocr_model_data.xml',
        'views/purchase_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tus_odoo_ocr_ai_purchase/static/src/xml/**/*',
            'tus_odoo_ocr_ai_purchase/static/src/js/**/*',
        ],
    },
    "images": ["static/description/main_banner.gif"],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
