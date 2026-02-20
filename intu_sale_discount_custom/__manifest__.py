{
    'name': 'Sale Order Discount Custom',
    'version': '1.0',
    'summary': 'Adds Line Item Discount and Total Discount in Sale Order Tax Totals',
    'description': """
        Custom module to:
        - Calculate discount lines
        - Compute total discount
        - Display discount below Taxes in Sale Order
    """,
    'author': 'Sharma M',
    'website': '',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'views/sale_tax_totals.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}