# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http, SUPERUSER_ID, _, _lt
from odoo.exceptions import ValidationError


class WebsiteComplaint(http.Controller):

    @http.route('/website/complaint', methods=['POST'], auth="public", website=True, csrf=False)
    def website_complaint(self, **kw):
        ''' This controller save the data comes from the bloopack register form and redirect to thank you page '''
        try:
            values = {
                'name': kw.get('name'),
                'email': kw.get('email'),
                'address': kw.get('address'),
                'type': kw.get('type_id'),
                'description': kw.get('description'),
                'phone': kw.get('phone'),
                'country_id': kw.get('country_id'),
                'state_id': kw.get('state_id'),
                'zip': kw.get('zip'),
                'city': kw.get('city'),
            }
            record = request.env['bloopack.complaints'].with_user(SUPERUSER_ID).with_context(
            ).create(values)
            thank_you_data = {'number': record.complaint_number}
            return request.render('bloopack_test_case.complaint_thanks', thank_you_data)

        except Exception as error:
            raise ValidationError(error)

    @http.route('/bloopack/complaint/form', type='http', auth="public", website=True)
    def bloopack_complaint_data(self, **kwargs):
        ''' This controller Redirect to the bloopack register web form with data '''
        return request.render("bloopack_test_case.bloopack_complaint")
