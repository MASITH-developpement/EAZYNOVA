# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EazynovaWebsiteController(http.Controller):

    @http.route('/saas/signup/submit', type='http', auth='public', website=True, csrf=False)
    def signup_submit_any(self, **post):
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(f"[DEBUG SIGNUP] >>> Entrée dans signup_submit_any | method={request.httprequest.method} | post={post} | params={dict(request.params)} | form={dict(request.httprequest.form)}")
        return request.render('eazynova_website.signup_error', {'error': 'Debug: route catch-all atteinte.'})

    """Contrôleur principal du site web EAZYNOVA SaaS"""

    @http.route('/', type='http', auth='public', website=True)
    def home(self, **kwargs):
        """Page d'accueil"""
        values = {
            'plans': request.env['saas.plan'].sudo().search([('active', '=', True)]),
        }
        return request.render('eazynova_website.homepage', values)

    @http.route('/saas/features', type='http', auth='public', website=True)
    def features(self, **kwargs):
        """Page des fonctionnalités"""
        values = {
            'features': request.env['saas.plan.feature'].sudo().search([]),
        }
        return request.render('eazynova_website.features', values)

    @http.route('/saas/pricing', type='http', auth='public', website=True)
    def pricing(self, **kwargs):
        """Page de tarification"""
        values = {
            'plans': request.env['saas.plan'].sudo().search([('active', '=', True)], order='sequence'),
        }
        return request.render('eazynova_website.pricing', values)

    @http.route('/saas/signup', type='http', auth='public', website=True)
    def signup(self, **kwargs):
        """Formulaire d'inscription"""
        values = {
            'plans': request.env['saas.plan'].sudo().search([('active', '=', True)], order='sequence'),
            'countries': request.env['res.country'].sudo().search([]),
        }
        return request.render('eazynova_website.signup', values)

    @http.route('/saas/signup/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def signup_submit(self, **post):
        """Traitement ultra-robuste du formulaire d'inscription (Odoo 19 CE)"""
        import logging
        _logger = logging.getLogger(__name__)
        try:
            # LOGGING ULTRA-PRECOS
            _logger.warning(f"[DEBUG SIGNUP] ENTRY: post={post} | type(post)={type(post)} | request.params={request.params} | type(request.params)={type(request.params)} | form={getattr(request.httprequest, 'form', None)} | type(form)={type(getattr(request.httprequest, 'form', None))}")

            # Si post ou request.params est une liste, on prend le premier élément dict
            def ensure_dict(obj):
                if isinstance(obj, dict):
                    return obj
                if isinstance(obj, (list, tuple)) and obj and isinstance(obj[0], dict):
                    return obj[0]
                return {}

            post_dict = ensure_dict(post)
            params_dict = ensure_dict(request.params)
            # request.httprequest.form est un MultiDict, on le convertit en dict de listes
            form_dict = {}
            if hasattr(request.httprequest, 'form'):
                try:
                    for k in request.httprequest.form:
                        form_dict[k] = request.httprequest.form.getlist(k)
                except Exception as e:
                    _logger.warning(f"[DEBUG SIGNUP] form parse error: {e}")

            # Fusionne tout (form > post > params)
            all_data = {}
            for d in (params_dict, post_dict):
                for k, v in d.items():
                    all_data.setdefault(k, []).extend(v if isinstance(v, list) else [v])
            for k, v in form_dict.items():
                all_data.setdefault(k, []).extend(v if isinstance(v, list) else [v])

            _logger.warning(f"[DEBUG SIGNUP] all_data (fusionné): {all_data}")

            def flatten_value(val):
                if isinstance(val, (list, tuple)):
                    if not val:
                        return ''
                    return flatten_value(val[0])
                return str(val) if val is not None else ''

            required_fields = ['company_name', 'contact_name', 'email', 'phone', 'plan_id', 'nb_users']
            cleaned = {}
            for field in required_fields:
                val = all_data.get(field, [''])
                val_flat = flatten_value(val)
                _logger.warning(f"[DEBUG SIGNUP] FLAT field {field}: type={type(val_flat)} value={val_flat}")
                cleaned[field] = val_flat
                if not val_flat:
                    return request.render('eazynova_website.signup_error', {
                        'error': f'Le champ {field} est requis.',
                    })


            # Champs optionnels
            for opt in ['street', 'zip', 'city', 'country_id']:
                val = all_data.get(opt, [''])
                cleaned[opt] = flatten_value(val)

            email = cleaned['email']
            company_name = cleaned['company_name']

            # Recherche d'une instance active ou trial pour ce partenaire/société
            existing_partner = request.env['res.partner'].sudo().search([
                ('email', '=', email)
            ], limit=1)


            # Recherche d'une instance active/trial liée à ce partenaire OU au nom de société
            domain_instance = ['&',
                ('state', 'in', ['active', 'trial']),
                '|',
                    ('partner_id', '=', existing_partner.id if existing_partner else 0),
                    ('name', 'ilike', company_name)
            ]
            existing_instance = request.env['saas.instance'].sudo().search(domain_instance, limit=1)

            if existing_instance:
                # Renvoi des credentials par email
                existing_instance._send_credentials_email()
                return request.render('eazynova_website.signup_error', {
                    'error': _(u"Une base de données existe déjà pour cette société. Les codes d'accès viennent de vous être renvoyés par email. Si vous n'avez rien reçu, vérifiez vos spams ou contactez le support."),
                })

            # Sinon, création/MAJ du partenaire et provisioning normal
            partner_values = {
                'name': company_name,
                'contact_name': cleaned['contact_name'],
                'email': email,
                'phone': cleaned['phone'],
                'street': cleaned['street'],
                'zip': cleaned['zip'],
                'city': cleaned['city'],
                'country_id': int(cleaned['country_id']) if cleaned['country_id'].isdigit() else False,
                'is_company': True,
            }
            _logger.warning(f"[DEBUG SIGNUP] partner_values: {partner_values}")

            if existing_partner:
                partner = existing_partner
                partner.sudo().write(partner_values)
            else:
                partner = request.env['res.partner'].sudo().create(partner_values)

            plan_id = int(cleaned['plan_id']) if cleaned['plan_id'].isdigit() else 0
            nb_users = int(cleaned['nb_users']) if cleaned['nb_users'].isdigit() else 5
            plan = request.env['saas.plan'].sudo().browse(plan_id)
            _logger.warning(f"[DEBUG SIGNUP] plan_id: {plan.id} nb_users: {nb_users}")

            subscription = request.env['saas.subscription'].sudo().create({
                'partner_id': partner.id,
                'plan_id': plan.id,
                'nb_users': nb_users,
            })

            subscription.action_start_trial()
            _logger.warning(f"[DEBUG SIGNUP] redirect to success {subscription.id}")
            return request.redirect(f'/saas/signup/success/{subscription.id}')

        except Exception as e:
            _logger.error(f'[DEBUG SIGNUP] Erreur lors de l\'inscription: {str(e)}', exc_info=True)
            return request.render('eazynova_website.signup_error', {
                'error': 'Une erreur est survenue lors de l\'inscription. Veuillez réessayer ou nous contacter.',
            })

    @http.route('/saas/signup/success/<int:subscription_id>', type='http', auth='public', website=True)
    def signup_success(self, subscription_id, **kwargs):
        """Page de succès après inscription"""
        subscription = request.env['saas.subscription'].sudo().browse(subscription_id)

        if not subscription.exists():
            return request.redirect('/saas/signup')

        values = {
            'subscription': subscription,
        }
        return request.render('eazynova_website.signup_success', values)

    @http.route('/saas/calculate-price', type='json', auth='public', website=True)
    def calculate_price(self, plan_id, nb_users):
        """Calculer le prix pour un plan et un nombre d'utilisateurs (AJAX)"""
        plan = request.env['saas.plan'].sudo().browse(int(plan_id))

        if not plan.exists():
            return {'error': 'Plan non trouvé'}

        base_price = plan.monthly_price
        extra_users = max(0, int(nb_users) - plan.included_users)
        extra_price = extra_users * plan.extra_user_price
        total_monthly = base_price + extra_price

        return {
            'base_price': base_price,
            'extra_users': extra_users,
            'extra_price': extra_price,
            'total_monthly': total_monthly,
            'setup_fee': plan.setup_fee,
            'currency_symbol': '€',
        }
