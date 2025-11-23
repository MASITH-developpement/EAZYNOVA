# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class TrustController(http.Controller):

    @http.route('/review/submit/<int:request_id>', type='http', auth='public', website=True)
    def submit_review(self, request_id, **kwargs):
        """Page de soumission d'avis"""
        review_request = request.env['eazynova.review.request'].sudo().browse(request_id)

        if not review_request.exists():
            return request.redirect('/404')

        return request.render('eazynova_trust.review_submit_page', {
            'review_request': review_request
        })
