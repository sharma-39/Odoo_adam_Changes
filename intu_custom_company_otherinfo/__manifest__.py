{
    'name': 'Custom Company Other Info',
    'version': '1.0',
    'summary': 'Adds a dedicated Other Information tab in the Company form for extended company details including Labour Cost',
    'description': 'This module extends the Odoo Company (res.company) form by adding a new "Other Information" tab. It allows users to store additional company-related details such as Labour Cost and other operational/company-specific fields in a structured manner without modifying the core company configuration. This enhancement improves data organization and provides a cleaner separation of standard and custom company fields.',
    'depends': ['base'],
    'data': [
        'views/res_company_view.xml',
    ],
    'installable': True,
    'application': False,
}