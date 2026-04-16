{
    'name': 'Sale Order Discount Custom',
    'version': '1.0',
    'summary': 'Adds line-level discount calculation and total discount display in Sales Order tax totals',
    'description': """
Sale Order Discount Custom Module
================================

This module enhances the Sales Order functionality by introducing advanced discount handling at both line and order level.

Key Features:
-------------
- Line item discount calculation support
- Total discount computation across Sales Order
- Display of discount value below tax totals section
- Improved pricing transparency for customers
- Enhanced Sales Order financial summary view

Business Benefits:
------------------
- Clear visibility of applied discounts
- Improved pricing accuracy
- Better customer communication in quotations
- Easier financial reconciliation
- Enhanced reporting for sales analysis

Dependencies:
-------------
- base
- sale
- account

Author:
-------
Sharma M
""",
    'author': 'Sharma M',
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