{
    'name': 'Custom Purchase Fields',
    'version': '1.0',
    'category': 'Purchase',
    'summary': 'Enhances Purchase Order with budgeting, approval workflow, RFQ status, payment tracking, and project integration fields',
    'description': """
Custom Purchase Fields Module
===========================

This module extends Purchase Order and Purchase Order Lines with advanced business logic, budgeting controls, approval workflow, and integration with Sales and Project modules.

Key Features:
-------------
- RFQ Approval status tracking
- Project-based budget validation and control
- Vendor payment tracking and amount due calculation
- Automatic RFQ numbering using sequences
- Sales Order linkage from Purchase Orders
- Purchase type classification (Material Request / Normal Order)
- Vendor TRN/VAT tracking
- Budget remaining validation before approval
- Custom approval workflow with business rules
- Purchase Order line enhancements

Fields Added (Purchase Order):
-----------------------------
- RFQ Status (Approved / Not Approved)
- Amount Due
- Remaining Budget
- Total Sales Budget (from Project)
- Payment Status (Fully / Partially / Not Paid)
- Purchase Type
- Responsible User
- RFQ Number
- Sales Order Link
- Vendor TRN Number
- PO Tags (Many2many)
- Approval Flags
- Remarks
- Discount & Before Discount Amount
- Vendor Paid Amount

Fields Added (Purchase Order Line):
----------------------------------
- Purchase Type Order
- Purchase Type Flag
- Purchase Type Selection
- Remarks

Business Benefits:
------------------
- Strong procurement approval control
- Budget-aware purchasing system
- Better vendor payment tracking
- Improved integration between Project → Purchase → Sales
- Reduced overspending and unauthorized purchases
- Centralized RFQ and PO workflow management

Dependencies:
-------------
- purchase
- sale
- account

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Intulogic Private Limited - Sharma M',
    'category': 'Purchase',
    'depends': ['purchase', 'sale', 'account'],
    'data': [
        'views/purchase_order_view.xml',
        'data/sequence.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}