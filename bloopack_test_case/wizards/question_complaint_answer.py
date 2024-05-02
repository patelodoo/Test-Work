# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from datetime import datetime


class ComplaintAnswer(models.TransientModel):
    _name = 'question.complaint.answer'
    _description = "Give Answer to complaint answer"

    answer = fields.Html("Answer")

    def close_complaint(self):
        ''' This Function Give the answer that asked by bloopack '''
        active_id = self.env.context.get('active_id')
        complaint_id = self.env['bloopack.complaints'].browse(active_id)
        print("=== Complaint ID ===", complaint_id)
        complaint_id.write({'state': 'solved', 'resolve_date': datetime.now(), 'resolve_reason': self.answer})
        email_values = {
            'answer': self.answer,
        }
        template_id = self.env.ref('bloopack_test_case.question_answer_complaint_email_template')
        self.env['mail.template'].browse(template_id.id).with_context(email_values).send_mail(complaint_id.id,
                                                                                              force_send=True)
