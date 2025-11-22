# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class TechnicianPortal(http.Controller):
    @http.route('/intervention/technicien', type='http', auth='user', website=True)
    def technician_dashboard(self, **kw):
        user = request.env.user
        # Récupère les interventions assignées au technicien connecté
        # Lire uniquement les champs nécessaires côté intervention pour le dashboard
        interventions = request.env['intervention.intervention'].sudo().search_read([
            ('technicien_principal_id.user_id', '=', user.id),
            ('statut_terrain', 'in', ['planifie', 'en_route', 'sur_site', 'en_cours'])
        ], ['id', 'numero', 'date_prevue', 'statut_terrain', 'client_final_id', 'donneur_ordre_id'])
        # Récupérer les partenaires clients référencés afin d'éviter des read() multiples
        client_ids = [i['client_final_id'][0] for i in interventions if i.get('client_final_id')]
        partner_map = {}
        if client_ids:
            partners = request.env['res.partner'].sudo().search_read([('id', 'in', client_ids)], ['id', 'name', 'email', 'phone'])
            partner_map = {p['id']: p for p in partners}
        # Préparer mapping intervention_id -> client fields
        client_fields = {}
        for i in interventions:
            cid = i.get('client_final_id') and i.get('client_final_id')[0]
            if cid:
                client_fields[i['id']] = partner_map.get(cid, {})
        return request.render('intervention.technician_portal_template', {
            'interventions': interventions,
            'user': user,
            'client_fields': client_fields,
        })

    @http.route('/intervention/technicien/arrivee/<int:intervention_id>', type='http', auth='user', website=True, csrf=False, methods=['POST'])
    def technician_arrivee(self, intervention_id, **kw):
        intervention = request.env['intervention.intervention'].sudo().browse(intervention_id)
        if intervention and intervention.statut_terrain in ['planifie', 'en_route']:
            intervention.write({'statut_terrain': 'sur_site'})
        return request.redirect('/intervention/technicien')
