from odoo import models, api, fields, _

'''Inherited hr.attendance model to add project, task and description while checking in'''
class HrAttendance(models.Model):

    _inherit = 'hr.attendance'

    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task', domain="[('project_id','=',project_id)]")
    attendance_description = fields.Text(string='Description')