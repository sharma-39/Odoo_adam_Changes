{
    'name': '(BOM Changes) Custom Models Wizard Form',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Wizard form to create and manage dynamic line-based records for BOM-related operations',
    'description': """
Custom Wizard Form Module (BOM Changes)
======================================

This module provides a custom wizard interface to create and manage line-based data entries for BOM-related operations in Odoo.

Key Features:
-------------
- Wizard-based data entry form
- Dynamic one-to-many line creation support
- Simplified data capture for BOM-related workflows
- User-friendly interface for structured input
- Integration with Sales and Project modules

Business Logic:
--------------
- Users can create temporary wizard records
- Multiple line items can be added dynamically
- Data can be processed and transferred to target models
- Helps streamline BOM-related operations and data entry

Business Benefits:
------------------
- Faster data entry using wizard interface
- Reduced manual effort in BOM creation workflows
- Improved accuracy in structured data input
- Better user experience for operational users
- Centralized handling of BOM-related inputs

Dependencies:
-------------
- base
- sale
- project
- uom

Author:
-------
Sharma Murugaiyan
""",
    'author': 'Sharma Murugaiyan',
    'depends': ['base', 'sale', 'project', 'uom'],
    'data': [
        'views/wizard_form_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}