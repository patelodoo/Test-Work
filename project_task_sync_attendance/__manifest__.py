# -*- coding: utf-8 -*-
{
    "name": "Project Task Sync Attendance",
    "summary": "Add project, and its related task, description when employee checks in/out",
    "version": "17.0.0.0.1",
    "category": "Human Resources/Attendances",
    "installable": True,
    'application': False,
    "depends": [
        "hr_attendance", "project"
    ],
    "data": [
        'views/hr_attendance_views.xml',
    ],
    "assets": {
        'web.assets_backend': [
            'project_task_sync_attendance/static/src/js/public_kiosk_app.js',
            'project_task_sync_attendance/static/src/xml/public_kiosk_app.xml',

        ],
        'hr_attendance.assets_public_attendance': [
            'project_task_sync_attendance/static/src/js/public_kiosk_app.js',
            'project_task_sync_attendance/static/src/xml/public_kiosk_app.xml',
        ],
    },
}
