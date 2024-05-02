# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from datetime import datetime


class DropComplaint(models.TransientModel):
    _name = 'drop.complaint'
    _description = "Give Reason of droping complaint"

    reason = fields.Html("Reason")

    def drop_complaint(self):
        ''' This Function Drop The Complaint and ask for drop reason '''
        active_id = self.env.context.get('active_id')
        complaint_id = self.env['bloopack.complaints'].browse(active_id)
        complaint_id.write({'state': 'dropped', 'resolve_date': datetime.now(), 'resolve_reason': self.reason})
        email_values = {
            'reason': self.reason,
        }
        template_id = self.env.ref('bloopack_test_case.closed_complaint_email_template')
        self.env['mail.template'].browse(template_id.id).with_context(email_values).send_mail(complaint_id.id,
                                                                                              force_send=True)
