# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError
import base64


class TestFacialRecognition(TransactionCase):
    """
    Tests pour la reconnaissance faciale
    """
    
    def setUp(self):
        super(TestFacialRecognition, self).setUp()
        self.User = self.env['res.users']
        self.user = self.User.create({
            'name': 'Test User Facial',
            'login': 'test_facial',
            'email': 'test.facial@example.com',
        })
    
    def test_facial_recognition_disabled_by_default(self):
        """
        Test: La reconnaissance faciale est désactivée par défaut
        """
        self.assertFalse(self.user.facial_recognition_enabled)
        self.assertFalse(self.user.facial_data)
    
    def test_facial_recognition_constraint_no_data(self):
        """
        Test: Impossible d'activer la reconnaissance sans données faciales
        """
        with self.assertRaises(ValidationError):
            self.user.facial_recognition_enabled = True
    
    def test_facial_recognition_with_data(self):
        """
        Test: Activation possible avec données faciales
        """
        # Données factices (dans un vrai test, utiliser de vraies données encodées)
        fake_data = base64.b64encode(b'fake_facial_encoding').decode('utf-8')
        
        self.user.write({
            'facial_data': fake_data,
            'facial_recognition_enabled': True,
        })
        
        self.assertTrue(self.user.facial_recognition_enabled)
        self.assertEqual(self.user.facial_data, fake_data)
    
    def test_facial_data_removal(self):
        """
        Test: La suppression des données faciales fonctionne (RGPD)
        """
        fake_data = base64.b64encode(b'fake_facial_encoding').decode('utf-8')
        
        self.user.write({
            'facial_data': fake_data,
            'facial_recognition_enabled': True,
        })
        
        # Suppression
        self.user.action_remove_facial_data()
        
        self.assertFalse(self.user.facial_recognition_enabled)
        self.assertFalse(self.user.facial_data)
        self.assertFalse(self.user.facial_consent_date)
    
    def test_facial_registration_disabled_globally(self):
        """
        Test: Impossible d'enregistrer des données si la feature est désactivée
        """
        # Désactivation globale
        self.env['ir.config_parameter'].sudo().set_param(
            'eazynova.facial_recognition_enabled', 'False'
        )
        
        with self.assertRaises(UserError):
            self.user.action_register_facial_data()
            