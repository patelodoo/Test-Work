# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.tools import float_round
from odoo.addons.hr_attendance.controllers.main import HrAttendance
import datetime


class HrAttendanceInherit(HrAttendance):

    # Overriden this method to get last attendance of the employee.
    @staticmethod
    def _get_employee_info_response(employee):
        employee_data = HrAttendance._get_employee_info_response(employee)
        if employee_data:
            employee_data['last_attendance_id'] = employee.last_attendance_id.id
        return employee_data

    # Fetch the list of projects and tasks which is available in the system to render on Attenace Kiosk Screen.
    @http.route('/hr_attendance/projects_data', type="json", auth="public")
    def project_data(self, token):
        project_ids = request.env['project.project'].sudo().search([])
        task_ids = request.env['project.task'].sudo().search([])
        projects = [{'id': project.id, 'name': project.name} for project in project_ids]
        tasks = [{'id': task.id, 'name': task.name, 'project_id': task.project_id.id} for task in task_ids]
        return {
            'projects': projects,
            'tasks': tasks
        }

    # Update the Attendance Record with selected project,task and description if employee is checked in.
    @http.route('/hr_attendance/update_project_data', type="json", auth="public")
    def update_project_data(self, attendance_id, update_data):
        attendance_id = request.env['hr.attendance'].sudo().browse(attendance_id)
        if attendance_id and not attendance_id.check_out:
            attendance_id.write(update_data)
        return True