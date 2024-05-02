{
    'name': 'Bloopack Test Case',
    'summary': """
        This module helps to bloopack can register complaints from website 
    """,
    'description': """
        This module helps to bloopack can register complaints about (question, electrical issue, heating issue,
            etc) for their rented flats. 
    """,
    'license': 'OPL-1',
    'category': 'sale',
    'version': '17.0.0.0',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'wizards/question_complaint_answer.xml',
        'wizards/drop_complaint.xml',
        'views/bloopack_complaints_view.xml',
        'views/complaint_type_view.xml',
        'reports/work_order_report_template.xml'
    ],
}
