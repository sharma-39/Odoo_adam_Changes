{
    "name": "Sale Order Approve Button",
    "version": "1.0",
    "category": "Sales",
    "summary": "Adds a custom Approve button with validation and workflow control on Sales Orders",
    "description": """
Sale Order Approve Button Module
===============================

This module introduces a custom approval mechanism for Sales Orders, enabling controlled validation before confirming quotations.

Key Features:
-------------
- Adds custom Approve button in Sales Order form
- Applies business validation rules before approval
- Controls Sales Order confirmation workflow
- Restricts unauthorized or incomplete orders
- Improves approval governance in sales process

Business Benefits:
------------------
- Strong approval control over Sales Orders
- Reduced risk of incorrect order confirmation
- Better workflow governance
- Improved sales process compliance
- Centralized validation before order processing

Dependencies:
-------------
- sale

Author:
-------
Sharma M - Intulogic Private Limited 
""",
    "author": "Sharma M - Intulogic Private Limited ",
    "depends": ["sale"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}