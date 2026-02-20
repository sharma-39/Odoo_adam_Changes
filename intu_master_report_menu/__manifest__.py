{
    'name': 'Master Report Sale',
    'version': '1.0',
    'summary': 'Master Sales Report List View',
    'author': 'Your Name',
    'depends': [
        'sale',
        'project',
        'purchase',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/x_sales_report_views.xml',
    ],
    'installable': True,
    'application': True,
}
