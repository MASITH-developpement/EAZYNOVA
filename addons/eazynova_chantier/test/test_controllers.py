# -*- coding: utf-8 -*-

from odoo.tests.common import HttpCase
import json


class TestEazynovaControllers(HttpCase):
    """
    Tests pour les contrôleurs web EAZYNOVA
    """
    
    def setUp(self):
        super(TestEazynovaControllers, self).setUp()
        
        # Activation des fonctionnalités pour les tests
        self.env['ir.config_parameter'].sudo().set_param(
            'eazynova.ai_assistance_enabled', 'True'
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'eazynova.ocr_enabled', 'True'
        )
    
    def test_ai_assist_endpoint_disabled(self):
        """
        Test: L'endpoint IA renvoie une erreur si désactivé
        """
        self.env['ir.config_parameter'].sudo().set_param(
            'eazynova.ai_assistance_enabled', 'False'
        )
        
        self.authenticate('admin', 'admin')
        
        response = self.url_open(
            '/eazynova/ai/assist',
            data=json.dumps({
                'jsonrpc': '2.0',
                'params': {
                    'query': 'Test question'
                }
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        self.assertIn('error', result.get('result', {}))
    
    def test_dashboard_data_endpoint(self):
        """
        Test: L'endpoint dashboard data fonctionne
        """
        self.authenticate('admin', 'admin')
        
        response = self.url_open(
            '/eazynova/dashboard/data',
            data=json.dumps({
                'jsonrpc': '2.0',
                'params': {}
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        self.assertTrue(result.get('result', {}).get('success'))
        self.assertIn('data', result.get('result', {}))
    
    def test_ocr_process_endpoint_no_document(self):
        """
        Test: L'endpoint OCR sans document renvoie une erreur
        """
        self.authenticate('admin', 'admin')
        
        response = self.url_open(
            '/eazynova/ocr/process',
            data=json.dumps({
                'jsonrpc': '2.0',
                'params': {}
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        self.assertIn('error', result.get('result', {}))