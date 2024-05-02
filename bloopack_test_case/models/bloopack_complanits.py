# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from datetime import datetime


class BloopackComplaints(models.Model):
    _name = 'bloopack.complaints'
    _description = "This Module is provide information about bloopack complaints"
    _inherit = 'mail.thread'
    _order = 'complaint_number desc'

    AVAILABLE_PRIORITIES = [
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High'),
    ]

    name = fields.Char("Name", required=True)
    complaint_number = fields.Char("Complaint Number", readonly=True, default=lambda self: _('New'), copy=False)
    email = fields.Char("Email", required=True)
    address = fields.Char("Address", required=True)
    phone = fields.Char("Phone", required=True)
    zip = fields.Char("Zip Code", required=True)
    city = fields.Char("City", required=True)
    state_id = fields.Many2one('res.country.state', string="State", required=True)
    country_id = fields.Many2one("res.country", required=True)
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', default=AVAILABLE_PRIORITIES[0][0])
    type = fields.Many2one('complaint.type', "Type", required=True)
    type_name = fields.Char(related='type.name', string="Type Name")
    user_id = fields.Many2one(related='type.user_id', string="Assigned To")
    description = fields.Char("Problem Description", required=True)
    action_plan = fields.Html("Action Plan")
    resolve_date = fields.Datetime("Resolve / Drop Date")
    resolve_reason = fields.Html("Resolve / Drop Reason")
    state = fields.Selection([
        ('new', 'New'),
        ('review', 'In Review'),
        ('progress', 'In Progress'),
        ('solved', 'Solved'),
        ('dropped', 'Dropped')], 'State', default='new', tracking=True)

    def action_set_to_draft(self):
        ''' Set State to new '''
        self.write({'state': 'new', 'resolve_date': "", "resolve_reason": ""})

    def action_action_plan(self):
        ''' Set State to In Progrss '''
        self.write({'state': 'progress'})

    def action_classify_complaint(self):
        ''' Set State to In Review '''
        self.write({'state': 'review'})

    def action_resolve_complaint(self):
        ''' Resolve the complaint and inform about the complaint '''
        self.write({'state': 'solved', 'resolve_date': datetime.now()})
        template_id = self.env.ref('bloopack_test_case.solved_complaint_email_template')
        self.env['mail.template'].browse(template_id.id).with_context({'action_plan': self.action_plan}).send_mail(self.id, force_send=True)

    def create(self, vals_list):
        ''' Create Complaint And Generate Sequence Number '''
        if not vals_list.get('complaint_number') or vals_list.get('complaint_number') == _('New'):
            vals_list['complaint_number'] = self.env['ir.sequence'].next_by_code('bloopack.complaints') or _('New')
        res = super(BloopackComplaints, self).create(vals_list)
        template_id = self.env.ref('bloopack_test_case.new_complaint_request_email_template')
        self.env['mail.template'].browse(template_id.id).send_mail(res.id, force_send=False)
        return res
