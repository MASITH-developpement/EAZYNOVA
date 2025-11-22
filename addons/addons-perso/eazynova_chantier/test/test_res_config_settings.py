# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestResConfigSettings(TransactionCase):
    """
    Tests pour les paramètres de configuration EAZYNOVA
    """
    
    def setUp(self):
        super(TestResConfigSettings, self).setUp()
        self.ConfigSettings = self.env['res.config.settings']
    
    def test_facial_recognition_tolerance_valid(self):
        """
        Test: La tolérance de reconnaissance faciale accepte des valeurs valides
        """
        config = self.ConfigSettings.create({
            'facial_recognition_tolerance': 0.5
        })
        self.assertEqual(config.facial_recognition_tolerance, 0.5)
    
    def test_facial_recognition_tolerance_invalid_high(self):
        """
        Test: La tolérance de reconnaissance faciale rejette les valeurs > 1.0
        """
        with self.assertRaises(ValidationError):
            self.ConfigSettings.create({
                'facial_recognition_tolerance': 1.5
            })
    
    def test_facial_recognition_tolerance_invalid_low(self):
        """
        Test: La tolérance de reconnaissance faciale rejette les valeurs < 0.0
        """
        with self.assertRaises(ValidationError):
            self.ConfigSettings.create({
                'facial_recognition_tolerance': -0.5
            })
    
    def test_ai_provider_default(self):
        """
        Test: Le provider IA par défaut est Anthropic
        """
        config = self.ConfigSettings.create({})
        self.assertEqual(config.ai_provider, 'anthropic')
    
    def test_ocr_enabled_default(self):
        """
        Test: L'OCR est activé par défaut
        """
        config = self.ConfigSettings.create({})
        self.assertTrue(config.ocr_enabled)
    
    def test_facial_recognition_warning_message(self):
        """
        Test: L'activation de la reconnaissance faciale déclenche un avertissement
        """
        config = self.ConfigSettings.create({})
        result = config._onchange_facial_recognition()
        
        # Pas d'avertissement si désactivé
        self.assertFalse(result)
        
        # Avertissement si activé
        config.facial_recognition_enabled = True
        result = config._onchange_facial_recognition()
        self.assertIn('warning', result)
        