{
    'name': 'Custom Sale Order Extra Fields',
    'version': '1.0',
    'summary': 'Extends Sale Orders with enquiry tracking, approval fields, VAT option, and additional commercial details',
    'description': """
Custom Sale Order Extra Fields Module
====================================

This module extends the standard Odoo Sale Order functionality by adding additional business and approval-related fields to improve sales tracking and document control.

Key Features:
-------------
- Enquiry Reference field (mandatory for tracking customer enquiries)
- Attention To field for contact/person handling
- Subject field for sales order classification
- PO Reference field for linking purchase orders
- VAT Included checkbox for tax handling clarity
- Hidden approval workflow fields for internal validation
- SQ Approval status badge in list/tree view
- Enhanced visibility of Shipping and Invoice addresses

Business Benefits:
------------------
- Better sales enquiry tracking and traceability
- Improved internal approval workflow control
- Clear financial and tax handling (VAT inclusion flag)
- Enhanced document clarity for sales operations
- Better reporting and filtering of sales orders

Dependencies:
-------------
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Your Company Name',
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}