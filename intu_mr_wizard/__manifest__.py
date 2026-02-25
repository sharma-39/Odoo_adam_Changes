{
    'name': 'MR Wizard',
    'version': '1.0',
    'summary': 'Material Request Wizard',
    'author': 'Custom',
    'depends': [
        'base',
        'sale',
        'project',
        'hr',
        'product',
        'uom',
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mr_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
}