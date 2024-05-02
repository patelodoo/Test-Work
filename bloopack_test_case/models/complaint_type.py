# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ComplaintsType(models.Model):
    _name = 'complaint.type'
    _description = "This Model provide about compliant types"

    name = fields.Char("Name", required=True)
    user_id = fields.Many2one('res.users', string="Assigned To", required=True)
