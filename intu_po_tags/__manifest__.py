{
    'name': 'PO Tags',
    'version': '1.0',
    'summary': 'Manage Purchase Order Tags',
    'description': 'Custom model for PO Tags inside Purchase Configuration.',
    'author': 'Your Name',
    'category': 'Purchase',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/po_category_views.xml',
    ],
    'installable': True,
    'application': False,
}