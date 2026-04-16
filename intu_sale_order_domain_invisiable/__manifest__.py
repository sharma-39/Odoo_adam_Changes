{
    'name': 'Default Button View in Sales Order',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Controls visibility of Send and Confirm buttons in Sales Order based on approval status',
    'description': """
Default Button View in Sales Order Module
========================================

This module controls the visibility of key Sales Order buttons such as Send and Confirm based on custom approval conditions.

Key Features:
-------------
- Hides or shows Send button based on approval status
- Controls Confirm button visibility dynamically
- Enforces approval workflow before order confirmation
- Improves sales process governance and control
- Prevents unauthorized order progression

Business Logic:
--------------
- Buttons are conditionally displayed based on approval flags
- Only approved orders are allowed to proceed to confirmation
- Ensures structured sales workflow execution

Business Benefits:
------------------
- Strong control over Sales Order processing
- Prevents unauthorized confirmations
- Enforces approval compliance
- Improves operational governance
- Reduces process errors in sales flow

Dependencies:
-------------
- sale

Author:
-------
Intulogic Private Limited
""",
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}