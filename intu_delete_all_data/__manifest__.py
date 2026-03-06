{
    'name': 'Delete All Transaction Data',
    'version': '1.0',
    'summary': 'Delete all transactional data from Odoo',
    'description': 'Custom wizard to delete Sale Orders, Purchase Orders, Invoices, Projects, Tasks, Stock, Products etc.',
    'author': 'Custom',
    'category': 'Tools',
    'depends': [
        'sale',
        'purchase',
        'stock',
        'account',
        'project',
        'hr_expense'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/data_cleanup_wizard_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}