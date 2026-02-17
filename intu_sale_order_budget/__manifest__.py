{
    'name': 'Sale Order Budget',
    'version': '1.0',
    'summary': 'Add Budget Info fields to Sale Orders and Sale Order Lines',
    'description': 'Custom fields for material and labour cost calculations on Sale Order Lines and aggregated budget info on Sale Orders.',
    'category': 'Sales',
    'author': 'IntuLogic Private limited',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
