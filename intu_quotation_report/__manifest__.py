{
    "name": "Customized Quotation Report",
    "version": "1.0",
    "category": "Sales",
    "summary": "Custom external layout and enhanced quotation report for Sales Order",
    "description": """
Customized Quotation Report Module
=================================

This module provides a fully customized external layout and enhanced quotation report for Sales Orders in Odoo.

Key Features:
-------------
- Custom Quotation Report template for Sales Orders
- Customized external layout for professional document presentation
- Modified standard report layout for consistent branding
- Custom paper format configuration
- Additional enhancements in Sales Order form view
- Improved print-ready quotation design

Business Benefits:
------------------
- Professional and branded quotation documents
- Improved customer presentation quality
- Standardized report layout across organization
- Better readability and structured output
- Enhanced sales documentation workflow

Dependencies:
-------------
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "author": "Sharma M",
    "depends": ["sale"],
    "data": [
        "reports/quotation_report.xml",
        "reports/web_external_layout_quotation.xml",
        "reports/web_external_layout_standard.xml",
        "reports/paperformat.xml",
        "views/sales_order_view.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}