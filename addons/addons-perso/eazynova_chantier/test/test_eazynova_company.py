# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestEazynovaCompany(TransactionCase):
    """
    Tests pour l'extension du modèle res.company
    """
    
    def setUp(self):
        super(TestEazynovaCompany, self).setUp()
        self.Company = self.env['res.company']
    
    def test_create_company_auto_code(self):
        """
        Test: La création d'une société génère automatiquement un code EAZYNOVA
        """
        company = self.Company.create({
            'name': 'Test Company',
        })
        
        self.assertTrue(company.eazynova_code)
        self.assertNotEqual(company.eazynova_code, '/')
    
    def test_create_company_with_code(self):
        """
        Test: La création d'une société avec un code spécifique conserve ce code
        """
        company = self.Company.create({
            'name': 'Test Company 2',
            'eazynova_code': 'TEST001',
        })
        
        self.assertEqual(company.eazynova_code, 'TEST001')
    
    def test_dashboard_layout_default(self):
        """
        Test: La disposition du dashboard par défaut est 'modern'
        """
        company = self.Company.create({
            'name': 'Test Company 3',
        })
        
        self.assertEqual(company.eazynova_dashboard_layout, 'modern')
    
    def test_compute_stats(self):
        """
        Test: Le calcul des statistiques fonctionne
        """
        company = self.Company.create({
            'name': 'Test Company 4',
        })
        
        # Les stats initiales sont à 0 (pas de modules complémentaires installés)
        self.assertEqual(company.total_chantiers, 0)
        self.assertEqual(company.total_factures, 0)