{
    'name': 'PO Tags',
    'version': '1.0',
    'summary': 'Manage and categorize Purchase Orders using custom PO Tags',
    'description': """
PO Tags Module
=============

This module introduces a custom tagging system for Purchase Orders to improve categorization, filtering, and reporting within the Purchase application.

Key Features:
-------------
- Custom PO Tag management model
- Integration of PO Tags in Purchase configuration
- Many2one relationship from Purchase Order to PO Tags
- Hierarchical tag structure support (parent-child relation)
- Improved purchase order classification and reporting

Business Benefits:
------------------
- Better organization of Purchase Orders
- Easier filtering and tracking of procurement categories
- Improved reporting and analytics on purchase data
- Flexible tagging system for procurement workflow
- Enhanced purchase configuration management

Dependencies:
-------------
- base
- purchase

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Intulogic Private Limited - Sharma M',
    'category': 'Purchase',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/po_category_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}