{
    'name': 'Invoice Additional Fields',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Adds computed payment, sales order, project, and vendor tracking fields in invoices',
    'description': """
Invoice Additional Fields Module
================================

This module extends Odoo Accounting (account.move) to provide advanced invoice-level analytics and business tracking.

Key Features:
-------------
- Computed Payment Received Amount from reconciled entries
- Sales Order linkage from invoice lines
- Project integration via Sales Order
- Project budget, progress, and status tracking
- Vendor TRN/VAT information on invoices
- Paid amount calculation (Total - Residual)
- Sales Order status and financial visibility
- Custom print/reference selection option

Business Benefits:
------------------
- Real-time payment tracking
- End-to-end visibility from Sales → Invoice → Project
- Improved financial reporting accuracy
- Better vendor and customer compliance tracking
- Enhanced project costing and performance monitoring

Dependencies:
-------------
- account
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Intulogic Private Limited - Sharma M',
    'depends': ['account', 'sale'],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}