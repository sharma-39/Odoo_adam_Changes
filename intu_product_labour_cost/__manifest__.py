{
    'name': 'Custom Product Labour Cost',
    'version': '1.0',
    'summary': 'Add Labour Cost field to Product Template below Standard Price',
    'description': 'Adds x_studio_product_labour_cost float field to product.template.',
    'category': 'Inventory',
    'author': 'Your Name',
    'website': 'https://yourcompany.com',
    'depends': ['product'],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
