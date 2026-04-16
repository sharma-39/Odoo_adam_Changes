{
    'name': 'Delete All Transaction Data',
    'version': '1.0',
    'summary': 'Utility tool to safely remove transactional data such as sales, purchase, accounting, stock, and project records',
    'description': """
Delete All Transaction Data Module
==================================

This module provides a controlled wizard to delete transactional data from Odoo for testing, development, or database reset purposes.

Supported Data Types:
---------------------
- Sales Orders
- Purchase Orders
- Invoices (Customer & Vendor)
- Stock / Inventory Movements
- Products
- Project Tasks and Projects
- HR Expenses

Key Features:
-------------
- Centralized cleanup wizard
- Selective or full transactional data deletion
- Menu-driven access for admin users
- Helps reset database for testing environments
- Avoids manual database cleanup operations

Security Warning:
-----------------
This module permanently deletes data and should only be used in non-production environments.

Dependencies:
-------------
- sale
- purchase
- stock
- account
- project
- hr_expense

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Custom',
    'category': 'Tools',
    'depends': [
        'sale',
        'purchase',
        'stock',
        'account',
        'project',
        'hr_expense'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/data_cleanup_wizard_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}