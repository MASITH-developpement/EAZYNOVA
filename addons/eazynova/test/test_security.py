# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError


class TestEazynovaSecurity(TransactionCase):
    """
    Tests pour la sécurité et les droits d'accès
    """
    
    def setUp(self):
        super(TestEazynovaSecurity, self).setUp()
        
        # Création d'utilisateurs avec différents rôles
        self.user_basic = self.env['res.users'].create({
            'name': 'Basic User',
            'login': 'user_basic',
            'email': 'basic@example.com',
            'groups_id': [(6, 0, [self.env.ref('eazynova.group_eazynova_user').id])]
        })
        
        self.user_manager = self.env['res.users'].create({
            'name': 'Manager User',
            'login': 'user_manager',
            'email': 'manager@example.com',
            'groups_id': [(6, 0, [self.env.ref('eazynova.group_eazynova_manager').id])]
        })
        
        self.user_admin = self.env['res.users'].create({
            'name': 'Admin User',
            'login': 'user_admin',
            'email': 'admin@example.com',
            'groups_id': [(6, 0, [self.env.ref('eazynova.group_eazynova_admin').id])]
        })
    
    def test_user_basic_can_read_company(self):
        """
        Test: Un utilisateur basique peut lire les informations de sa société
        """
        company = self.env['res.company'].sudo(self.user_basic).search([
            ('id', '=', self.user_basic.company_id.id)
        ], limit=1)
        
        self.assertTrue(company)
        self.assertEqual(company.id, self.user_basic.company_id.id)
    
    def test_user_basic_cannot_create_company(self):
        """
        Test: Un utilisateur basique ne peut pas créer de société
        """
        with self.assertRaises(AccessError):
            self.env['res.company'].sudo(self.user_basic).create({
                'name': 'Unauthorized Company'
            })
    
    def test_user_manager_can_write_company(self):
        """
        Test: Un manager peut modifier sa société
        """
        company = self.user_manager.company_id
        
        company.sudo(self.user_manager).write({
            'eazynova_dashboard_layout': 'compact'
        })
        
        self.assertEqual(company.eazynova_dashboard_layout, 'compact')
    
    def test_user_admin_full_access(self):
        """
        Test: Un administrateur a tous les droits
        """
        # Lecture
        companies = self.env['res.company'].sudo(self.user_admin).search([])
        self.assertTrue(companies)
        
        # Écriture
        company = self.user_admin.company_id
        company.sudo(self.user_admin).write({
            'eazynova_dashboard_layout': 'classic'
        })
        self.assertEqual(company.eazynova_dashboard_layout, 'classic')
        
        # Création (si les droits le permettent selon la config)
        # Note: En production, même les admins ne créent pas toujours de sociétés
    
    def test_facial_data_privacy(self):
        """
        Test: Les données faciales sont protégées (RGPD)
        Un utilisateur ne peut accéder qu'à ses propres données
        """
        # Création de données faciales pour user_basic
        import base64
        fake_data = base64.b64encode(b'fake_encoding').decode('utf-8')
        
        self.user_basic.sudo().write({
            'facial_data': fake_data,
            'facial_recognition_enabled': True,
        })
        
        # user_manager ne peut pas lire les données faciales de user_basic
        with self.assertRaises(AccessError):
            user_basic_as_manager = self.env['res.users'].sudo(self.user_manager).browse(
                self.user_basic.id
            )
            _ = user_basic_as_manager.facial_data