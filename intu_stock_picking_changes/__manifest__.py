{
    'name': 'Stock Picking Changes',
    'version': '1.0',
    'summary': 'Link Purchase Order MR Number to Stock Picking',
    'author': 'Your Name',
    'depends': ['stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}