# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SaasSubscription(models.Model):
    """Abonnement SaaS d'un client"""
    _name = 'saas.subscription'
    _description = 'Abonnement SaaS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user,
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Société',
        default=lambda self: self.env.company,
    )

    # Plan et tarification
    plan_id = fields.Many2one(
        'saas.plan',
        string='Plan',
        required=True,
        tracking=True,
    )
    nb_users = fields.Integer(
        string='Nombre d\'utilisateurs',
        default=5,
        required=True,
        tracking=True,
    )
    monthly_price = fields.Monetary(
        string='Prix mensuel (HT)',
        compute='_compute_prices',
        store=True,
        currency_field='currency_id',
    )
    setup_fee = fields.Monetary(
        string='Frais de configuration (HT)',
        compute='_compute_prices',
        store=True,
        currency_field='currency_id',
    )
    total_monthly = fields.Monetary(
        string='Total mensuel (HT)',
        compute='_compute_prices',
        store=True,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        related='company_id.currency_id',
        readonly=True,
    )

    # Dates
    date_start = fields.Date(
        string='Date de début',
        default=fields.Date.today,
        required=True,
        tracking=True,
    )
    date_end = fields.Date(
        string='Date de fin',
        tracking=True,
    )
    trial_end_date = fields.Date(
        string='Fin de la période d\'essai',
        compute='_compute_trial_end_date',
        store=True,
    )
    next_billing_date = fields.Date(
        string='Prochaine facturation',
        tracking=True,
    )

    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('trial', 'Essai gratuit'),
        ('active', 'Actif'),
        ('suspended', 'Suspendu'),
        ('cancelled', 'Annulé'),
        ('expired', 'Expiré'),
    ], string='État', default='draft', required=True, tracking=True)

    # Instance
    instance_id = fields.Many2one(
        'saas.instance',
        string='Instance',
        readonly=True,
    )
    instance_url = fields.Char(
        string='URL de l\'instance',
        related='instance_id.url',
        readonly=True,
    )

    # Facturation
    invoice_ids = fields.One2many(
        'account.move',
        'saas_subscription_id',
        string='Factures',
        readonly=True,
    )
    invoice_count = fields.Integer(
        string='Nombre de factures',
        compute='_compute_invoice_count',
    )

    # Devis et Commandes
    sale_order_ids = fields.One2many(
        'sale.order',
        'saas_subscription_id',
        string='Devis/Commandes',
        readonly=True,
    )
    sale_order_count = fields.Integer(
        string='Nombre de devis',
        compute='_compute_sale_order_count',
    )
    quotation_sent = fields.Boolean(
        string='Devis envoyé',
        default=False,
        tracking=True,
        help='Indique si le devis a été envoyé au client après la période d\'essai',
    )
    quotation_id = fields.Many2one(
        'sale.order',
        string='Devis principal',
        readonly=True,
        help='Devis généré automatiquement après la période d\'essai',
    )

    # Paiements récurrents
    recurring_payment_active = fields.Boolean(
        string='Paiement récurrent actif',
        default=False,
        tracking=True,
    )
    unpaid_months = fields.Integer(
        string='Mois impayés',
        default=0,
        tracking=True,
        help='Nombre de mois impayés (accumulation en cas de défaut)',
    )
    amount_due = fields.Monetary(
        string='Montant dû',
        compute='_compute_amount_due',
        store=True,
        currency_field='currency_id',
        help='Total des mensualités impayées',
    )
    payment_failed_count = fields.Integer(
        string='Échecs de paiement',
        default=0,
        tracking=True,
    )
    last_payment_attempt = fields.Datetime(
        string='Dernière tentative de paiement',
        readonly=True,
    )

    # Configuration payée
    setup_paid = fields.Boolean(
        string='Configuration payée',
        default=False,
        tracking=True,
    )

    @api.model
    def create(self, vals):
        """Générer une référence unique à la création"""
        if vals.get('name', _('Nouveau')) == _('Nouveau'):
            vals['name'] = self.env['ir.sequence'].next_by_code('saas.subscription') or _('Nouveau')
        return super().create(vals)

    @api.depends('plan_id', 'nb_users')
    def _compute_prices(self):
        """Calculer les prix selon le plan et le nombre d'utilisateurs"""
        for subscription in self:
            if subscription.plan_id:
                plan = subscription.plan_id
                base_price = plan.monthly_price
                extra_users = max(0, subscription.nb_users - plan.included_users)
                extra_price = extra_users * plan.extra_user_price

                subscription.monthly_price = base_price + extra_price
                subscription.setup_fee = plan.setup_fee if not subscription.setup_paid else 0.0
                subscription.total_monthly = subscription.monthly_price
            else:
                subscription.monthly_price = 0.0
                subscription.setup_fee = 0.0
                subscription.total_monthly = 0.0

    @api.depends('date_start', 'plan_id')
    def _compute_trial_end_date(self):
        """Calculer la date de fin de période d'essai"""
        for subscription in self:
            if subscription.date_start and subscription.plan_id:
                trial_days = subscription.plan_id.trial_days or 30
                subscription.trial_end_date = subscription.date_start + timedelta(days=trial_days)
            else:
                subscription.trial_end_date = False

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """Compter les factures"""
        for subscription in self:
            subscription.invoice_count = len(subscription.invoice_ids)

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        """Compter les devis/commandes"""
        for subscription in self:
            subscription.sale_order_count = len(subscription.sale_order_ids)

    @api.depends('unpaid_months', 'monthly_price')
    def _compute_amount_due(self):
        """Calculer le montant total dû (mois impayés × prix mensuel)"""
        for subscription in self:
            subscription.amount_due = subscription.unpaid_months * subscription.monthly_price

    def action_start_trial(self):
        """Démarrer la période d'essai"""
        for subscription in self:
            if subscription.state != 'draft':
                raise UserError(_('Seuls les abonnements en brouillon peuvent démarrer un essai.'))

            # Créer l'instance Odoo
            instance = self.env['saas.instance'].create({
                'name': f'{subscription.partner_id.name} - EAZYNOVA',
                'subscription_id': subscription.id,
                'partner_id': subscription.partner_id.id,
                'plan_id': subscription.plan_id.id,
                'max_users': subscription.nb_users,
            })

            # Provisionner l'instance
            instance.action_provision()

            subscription.write({
                'state': 'trial',
                'instance_id': instance.id,
            })

            # Envoyer email de bienvenue
            template = self.env.ref('eazynova_website.email_template_trial_start', raise_if_not_found=False)
            if template:
                template.send_mail(subscription.id, force_send=True)

    def action_activate(self):
        """Activer l'abonnement (fin de période d'essai ou activation directe)"""
        for subscription in self:
            if subscription.state not in ['trial', 'draft', 'suspended']:
                raise UserError(_('Impossible d\'activer cet abonnement dans l\'état actuel.'))

            # Si pas d'instance, en créer une
            if not subscription.instance_id:
                subscription.action_start_trial()

            # Générer la facture de configuration si non payée
            if not subscription.setup_paid and subscription.setup_fee > 0:
                subscription._create_setup_invoice()

            subscription.write({
                'state': 'active',
                'next_billing_date': fields.Date.today() + timedelta(days=30),
            })

            # Envoyer email de confirmation
            template = self.env.ref('eazynova_website.email_template_subscription_active', raise_if_not_found=False)
            if template:
                template.send_mail(subscription.id, force_send=True)

    def action_suspend(self):
        """Suspendre l'abonnement"""
        for subscription in self:
            subscription.state = 'suspended'
            if subscription.instance_id:
                subscription.instance_id.action_suspend()

    def action_cancel(self):
        """Annuler l'abonnement"""
        for subscription in self:
            subscription.write({
                'state': 'cancelled',
                'date_end': fields.Date.today(),
            })

    def _create_setup_invoice(self):
        """Créer la facture de configuration"""
        self.ensure_one()

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'saas_subscription_id': self.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Configuration EAZYNOVA - {self.plan_id.name}',
                'quantity': 1,
                'price_unit': self.setup_fee,
            })],
        })

        return invoice

    def _create_monthly_invoice(self):
        """Créer la facture mensuelle"""
        self.ensure_one()

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'saas_subscription_id': self.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Abonnement EAZYNOVA {self.plan_id.name} - {self.nb_users} utilisateurs',
                'quantity': 1,
                'price_unit': self.monthly_price,
            })],
        })

        # Planifier la prochaine facture
        self.next_billing_date = fields.Date.today() + timedelta(days=30)

        return invoice

    def _create_quotation_after_trial(self):
        """
        Créer un devis automatiquement après la période d'essai
        Ce devis explique que l'abonnement est nécessaire pour continuer
        """
        self.ensure_one()

        if self.quotation_sent or self.quotation_id:
            _logger.warning(f'Devis déjà généré pour {self.name}')
            return self.quotation_id

        # Récupérer les articles de produit
        product_standard = self.env.ref('eazynova_website.product_eazynova_standard', raise_if_not_found=False)
        product_extra_user = self.env.ref('eazynova_website.product_eazynova_extra_user', raise_if_not_found=False)

        if not product_standard:
            raise UserError(_('Article EAZYNOVA Standard non trouvé. Vérifiez les données.'))

        # Calculer utilisateurs supplémentaires
        extra_users = max(0, self.nb_users - self.plan_id.included_users)

        # Lignes du devis
        order_lines = [(0, 0, {
            'product_id': product_standard.id,
            'product_uom_qty': 1,
            'price_unit': self.plan_id.monthly_price,
            'name': f"""EAZYNOVA - Abonnement Mensuel Standard

✅ Inclus : {self.plan_id.included_users} utilisateurs
✅ Accès complet à tous les modules
✅ Support technique par email
✅ Mises à jour automatiques
✅ Stockage cloud sécurisé

⚠️ IMPORTANT : Votre période d'essai gratuite de 30 jours arrive à terme.
Pour continuer à utiliser EAZYNOVA sans interruption, validez ce devis.

Le paiement sera automatiquement renouvelé chaque mois.
En cas de défaut de paiement, votre accès sera suspendu et les mensualités
continueront à courir jusqu'au règlement complet du solde dû.""",
        })]

        # Ajouter utilisateurs supplémentaires si nécessaire
        if extra_users > 0 and product_extra_user:
            order_lines.append((0, 0, {
                'product_id': product_extra_user.id,
                'product_uom_qty': extra_users,
                'price_unit': self.plan_id.extra_user_price,
                'name': f'Utilisateurs supplémentaires (×{extra_users})',
            }))

        # Créer le devis
        quotation = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'saas_subscription_id': self.id,
            'date_order': fields.Datetime.now(),
            'validity_date': fields.Date.today() + timedelta(days=15),
            'note': f"""
CONDITIONS D'ABONNEMENT EAZYNOVA

1. PÉRIODE D'ESSAI
Votre période d'essai gratuite de 30 jours prend fin le {self.trial_end_date.strftime('%d/%m/%Y')}.

2. ABONNEMENT
En validant ce devis, vous activez un abonnement mensuel récurrent à {self.monthly_price}€ HT/mois.
Le premier prélèvement aura lieu dès validation.
Les prélèvements suivants seront effectués automatiquement chaque mois.

3. DÉFAUT DE PAIEMENT
En cas d'échec de paiement :
- Votre accès sera immédiatement SUSPENDU
- Les mensualités continueront à COURIR (même si accès suspendu)
- La reconnexion nécessitera le paiement du SOLDE TOTAL DÛ

Exemple : 3 mois d'impayés = 3 × {self.monthly_price}€ = {self.monthly_price * 3}€ à régler

4. RÉSILIATION
Vous pouvez résilier à tout moment depuis votre espace client.
Les données seront supprimées 30 jours après résiliation.

Questions ? Contactez-nous : support@eazynova.com
            """,
            'order_line': order_lines,
        })

        # Mettre à jour l'abonnement
        self.write({
            'quotation_id': quotation.id,
            'quotation_sent': True,
        })

        return quotation

    def action_confirm_quotation(self):
        """
        Confirmer le devis et activer le paiement récurrent
        Appelée automatiquement quand le client valide le devis
        """
        self.ensure_one()

        if not self.quotation_id:
            raise UserError(_('Aucun devis associé à cet abonnement.'))

        if self.quotation_id.state not in ['sale', 'done']:
            raise UserError(_('Le devis doit être confirmé avant d\'activer l\'abonnement.'))

        # Activer l'abonnement et le paiement récurrent
        self.write({
            'state': 'active',
            'recurring_payment_active': True,
            'next_billing_date': fields.Date.today() + timedelta(days=30),
            'unpaid_months': 0,
        })

        _logger.info(f'Abonnement {self.name} activé avec paiement récurrent')

        # Envoyer email de confirmation
        template = self.env.ref('eazynova_website.email_template_subscription_active', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def _process_recurring_payment(self):
        """
        Traiter un paiement mensuel récurrent
        Retourne True si succès, False si échec
        """
        self.ensure_one()

        try:
            # Créer la facture mensuelle
            invoice = self._create_monthly_invoice()

            # Tenter le paiement automatique (à implémenter avec gateway de paiement)
            # Pour l'instant, on suppose que la facture est créée et en attente de paiement

            self.write({
                'last_payment_attempt': fields.Datetime.now(),
            })

            _logger.info(f'Paiement récurrent traité pour {self.name}')
            return True

        except Exception as e:
            _logger.error(f'Échec paiement récurrent pour {self.name}: {str(e)}')
            self._handle_payment_failure()
            return False

    def _handle_payment_failure(self):
        """
        Gérer un échec de paiement
        - Incrémenter compteurs
        - Suspendre si nécessaire
        - Notifier client
        """
        self.ensure_one()

        self.write({
            'payment_failed_count': self.payment_failed_count + 1,
            'unpaid_months': self.unpaid_months + 1,
            'last_payment_attempt': fields.Datetime.now(),
        })

        _logger.warning(f'Échec paiement #{self.payment_failed_count} pour {self.name} - {self.unpaid_months} mois impayé(s)')

        # Suspendre immédiatement en cas d'impayé
        if self.state == 'active':
            self.action_suspend_for_nonpayment()

        # Envoyer notification
        template = self.env.ref('eazynova_website.email_template_payment_failed', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_suspend_for_nonpayment(self):
        """
        Suspendre l'abonnement pour défaut de paiement
        Les mois continuent à courir même suspendu !
        """
        self.ensure_one()

        if self.state != 'active':
            return

        self.write({'state': 'suspended'})

        # Suspendre l'instance (couper l'accès)
        if self.instance_id and self.instance_id.state == 'active':
            self.instance_id.write({'state': 'suspended'})
            _logger.warning(f'Instance suspendue pour {self.name} - Impayé: {self.amount_due}€')

        # Notification client
        self.message_post(
            body=f"""⚠️ ABONNEMENT SUSPENDU POUR DÉFAUT DE PAIEMENT

Mois impayés : {self.unpaid_months}
Montant dû : {self.amount_due}€ HT

IMPORTANT : Les mensualités continuent à courir pendant la suspension.
Pour réactiver votre accès, réglez le solde total via votre espace client.

Solde actuel : {self.amount_due}€
(Ce montant augmente de {self.monthly_price}€ chaque mois)
            """,
            subject='⚠️ Suspension pour impayé',
        )

    def action_pay_outstanding(self):
        """
        Payer le solde dû et réactiver l'abonnement
        À appeler après paiement manuel du solde
        """
        self.ensure_one()

        if self.amount_due <= 0:
            raise UserError(_('Aucun montant dû.'))

        # Créer une facture pour le solde
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'saas_subscription_id': self.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Régularisation - {self.unpaid_months} mois impayé(s) EAZYNOVA',
                'quantity': 1,
                'price_unit': self.amount_due,
            })],
        })

        # Réinitialiser les compteurs après paiement confirmé
        # (à faire automatiquement via webhook paiement)
        self.write({
            'unpaid_months': 0,
            'payment_failed_count': 0,
        })

        # Réactiver
        if self.state == 'suspended':
            self.action_activate()

        _logger.info(f'Solde payé et abonnement réactivé pour {self.name}')

        return {
            'name': _('Facture de régularisation'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def _cron_send_trial_end_quotations(self):
        """
        Cron quotidien : Envoyer les devis aux abonnements en fin d'essai
        Exécuté 3 jours avant la fin de la période d'essai
        """
        today = fields.Date.today()
        warning_date = today + timedelta(days=3)

        trials = self.search([
            ('state', '=', 'trial'),
            ('trial_end_date', '=', warning_date),
            ('quotation_sent', '=', False),
        ])

        for trial in trials:
            try:
                # Générer le devis
                quotation = trial._create_quotation_after_trial()

                # Envoyer par email
                template = self.env.ref('eazynova_website.email_template_quotation_trial_end', raise_if_not_found=False)
                if template:
                    # Envoyer en contexte avec le devis
                    template.with_context(quotation_id=quotation.id).send_mail(trial.id, force_send=True)

                _logger.info(f'Devis envoyé pour {trial.name} (fin essai: {trial.trial_end_date})')

            except Exception as e:
                _logger.error(f'Erreur envoi devis pour {trial.name}: {str(e)}')

    @api.model
    def _cron_check_trial_expiration(self):
        """Vérifier les périodes d'essai expirées (cron quotidien)"""
        today = fields.Date.today()
        trials = self.search([
            ('state', '=', 'trial'),
            ('trial_end_date', '<', today),
        ])

        for trial in trials:
            _logger.info(f'Période d\'essai expirée pour {trial.name}')
            # Envoyer notification
            template = self.env.ref('eazynova_website.email_template_trial_expired', raise_if_not_found=False)
            if template:
                template.send_mail(trial.id, force_send=True)

            # Marquer comme expiré
            trial.state = 'expired'

    @api.model
    def _cron_generate_invoices(self):
        """Générer les factures mensuelles (cron quotidien)"""
        today = fields.Date.today()
        subscriptions = self.search([
            ('state', '=', 'active'),
            ('next_billing_date', '<=', today),
        ])

        for subscription in subscriptions:
            try:
                subscription._create_monthly_invoice()
                _logger.info(f'Facture générée pour {subscription.name}')
            except Exception as e:
                _logger.error(f'Erreur génération facture pour {subscription.name}: {str(e)}')

    @api.model
    def _cron_check_unpaid_subscriptions(self):
        """Vérifier les abonnements impayés et supprimer les bases après 30 jours"""
        today = fields.Date.today()
        expired = self.search([
            ('state', '=', 'expired'),
            ('trial_end_date', '<', today - timedelta(days=30)),
        ])

        for subscription in expired:
            if subscription.instance_id:
                _logger.info(f'Suppression de l\'instance pour {subscription.name} (30 jours sans paiement)')
                subscription.instance_id.action_delete()

    def action_view_invoices(self):
        """Voir les factures de l'abonnement"""
        self.ensure_one()
        return {
            'name': _('Factures'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('saas_subscription_id', '=', self.id)],
            'context': {'default_saas_subscription_id': self.id},
        }


# Extension du modèle de commande/devis
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    saas_subscription_id = fields.Many2one(
        'saas.subscription',
        string='Abonnement SaaS',
        readonly=True,
        help='Abonnement SaaS associé à ce devis/commande',
    )

    def action_confirm(self):
        """Override pour activer automatiquement l'abonnement à la confirmation"""
        res = super().action_confirm()

        # Si c'est une commande liée à un abonnement SaaS
        for order in self:
            if order.saas_subscription_id:
                # Activer le paiement récurrent
                try:
                    order.saas_subscription_id.action_confirm_quotation()
                    _logger.info(f'Abonnement {order.saas_subscription_id.name} activé via devis {order.name}')
                except Exception as e:
                    _logger.error(f'Erreur activation abonnement via devis {order.name}: {str(e)}')

        return res


# Extension du modèle de facture
class AccountMove(models.Model):
    _inherit = 'account.move'

    saas_subscription_id = fields.Many2one(
        'saas.subscription',
        string='Abonnement SaaS',
        readonly=True,
    )
