# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Odoo OCR Using AI - Expense',
    'version': '19.0.1.0.0',
    'summary': """
                Transform your Expense processing with the Odoo OCR Using AI app! This powerful tool leverages advanced optical character recognition (OCR) technology and artificial intelligence to streamline the capture and management of Expense within your Odoo environment.
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
        Transform your Expense processing with the Odoo OCR Using AI app! This powerful tool
        leverages advanced optical character recognition (OCR) technology and artificial 
        intelligence to streamline the capture and management of Expense within your Odoo 
        environment.""",
    'category': 'tools',
    'website': "https://techultrasolutions.com",
    "author": "TechUltra Solutions Pvt. Ltd.",
    'depends': ["hr_expense", "tus_odoo_ocr_ai_base", "account"],
    'data': [
        'data/ocr_model_data.xml',
        'views/hr_expense_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tus_odoo_ocr_ai_expense/static/src/xml/**/*',
            'tus_odoo_ocr_ai_expense/static/src/js/**/*',
        ],
    },
    "images": ["static/description/main_banner.gif"],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
