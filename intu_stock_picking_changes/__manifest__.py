{
    'name': 'Stock Picking Changes',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Links Purchase Order MR Number with Stock Picking and updates project/material tracking on validation',
    'description': """
Stock Picking Changes Module
===========================

This module enhances Stock Picking functionality by linking Purchase Orders, Material Requests (MR), Projects, and Sales Orders for better end-to-end tracking.

Key Features:
-------------
- Links MR Number from Purchase Order to Stock Picking
- Displays PO MR Number and PO Number in stock picking
- Tracks received and delivered quantities automatically
- Updates project financials based on stock movements
- Synchronizes Material Request workflow with stock operations
- Updates custom forms with received and delivered quantities
- Auto-assigns Sale Order from Project when picking is created

Business Logic:
--------------
- Incoming stock updates project receipt values
- Outgoing stock updates delivery values
- MR-based tracking ensures full procurement lifecycle visibility
- Stock movements update custom MR form quantities
- Ensures traceability between Purchase → Stock → Project → Sale

Business Benefits:
------------------
- Full procurement lifecycle visibility
- Accurate project cost tracking
- Better inventory and MR reconciliation
- Reduced manual entry errors
- Improved operational transparency

Dependencies:
-------------
- stock
- purchase

Author:
-------
Sharma M - Intulogic Private Limited
""",
    'author': 'Sharma M - Intulogic Private Limited',
    'depends': ['stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}