{
    'name': 'Sale Order Set To Quotation Custom',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Automatically updates custom approval field when Set to Quotation is clicked',
    'description': """
Sale Order Set To Quotation Custom Module
========================================

This module customizes the behavior of the "Set to Quotation" action in Sales Orders.

Key Features:
-------------
- Automatically updates the custom field x_approved when Sales Order is reset to quotation
- Ensures approval status is reset when order moves back to draft/quotation stage
- Maintains consistency in approval workflow
- Integrates with standard Odoo Sales Order lifecycle

Business Logic:
--------------
- When a Sales Order is set to Quotation (draft state), x_approved field is reset
- Prevents previously approved orders from retaining approval status after reset
- Ensures proper approval re-validation for revised quotations

Business Benefits:
------------------
- Strong control over approval workflow
- Prevents misuse of previously approved orders
- Ensures re-approval after changes
- Improves sales process integrity
- Reduces approval inconsistencies

Dependencies:
-------------
- sale

Author:
-------
Sharma M - Intulogic Private Limited 
""",
    'author': 'Sharma M - Intulogic Private Limited ',
    'depends': ['sale'],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}