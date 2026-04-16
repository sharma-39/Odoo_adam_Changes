{
    'name': 'Sale Order Line Domain Control',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Controls visibility and editability of Sale Order Lines based on Sale Order state',
    'description': """
Sale Order Line Domain Control Module
====================================

This module controls the behavior of Sales Order Lines based on the state of the Sales Order.

Key Features:
-------------
- Restricts editing of order lines based on Sales Order state
- Applies domain conditions dynamically in form views
- Prevents modification after approval or confirmation
- Enhances workflow integrity and data protection
- Ensures consistency in Sales Order lifecycle

Business Logic:
--------------
- Order lines become read-only or restricted based on Sales Order state
- Editing is allowed only in draft or allowed states
- Prevents accidental changes after order confirmation

Business Benefits:
------------------
- Strong control over Sales Order data integrity
- Prevents unauthorized modifications
- Improves workflow discipline
- Reduces operational errors
- Ensures accurate sales documentation

Dependencies:
-------------
- sale

Author:
-------
Sharma M - Intulogic Private Limited 
""",
    'author': 'Sharma M - Intulogic Private Limited ',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}