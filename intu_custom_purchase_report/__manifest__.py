{
    "name": "Purchase Custom Report",
    "version": "1.0",
    "category": "purchase",
    "summary": "Custom Purchase Report for enhanced purchase document printing and reporting",
    "description": """
Purchase Custom Report Module
=============================

This module enhances the default Odoo Purchase functionality by introducing a custom purchase report format and improved reporting structure.

Key Features:
-------------
- Custom Purchase Order report layout
- Improved readability of purchase documents
- Structured report action for easy printing
- Enhanced purchase reporting for business use
- Custom view modifications for purchase order screen

Business Benefits:
------------------
- Standardized purchase document format
- Better vendor communication
- Improved reporting clarity
- Professional purchase order print layout
- Supports business branding and customization

Dependencies:
-------------
- purchase
- account

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "depends": ["purchase", "account"],
    "data": [
        "reports/purchase_report.xml",
        "reports/report_action.xml",
        "views/purchase_order_view.xml"
    ],
    "installable": True,
    "application": False,
}