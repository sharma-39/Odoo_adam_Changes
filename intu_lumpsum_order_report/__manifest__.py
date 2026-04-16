{
    "name": "Customized Lumpsum Report",
    "version": "1.0",
    "category": "Sales",
    "summary": "Custom external layout for Sale Order Lumpsum quotation report",
    "description": """
Customized Lumpsum Report Module
================================

This module customizes the Sale Order quotation report in Odoo to support a Lumpsum pricing format with a tailored external layout.

Key Features:
-------------
- Custom Lumpsum quotation report format
- Dedicated external layout for Lumpsum sales orders
- Standard and quotation-specific report templates
- Custom paper format for optimized printing
- Improved presentation for fixed-price (Lumpsum) quotations

Business Benefits:
------------------
- Clear presentation of fixed-price quotations
- Professional and branded sales documents
- Improved customer understanding of Lumpsum pricing
- Standardized report structure across organization
- Enhanced sales documentation quality

Dependencies:
-------------
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "depends": ["sale"],
    "data": [
        "reports/lumpsum_quotation_report.xml",
        "reports/web_external_layout_quotation.xml",
        "reports/web_external_layout_standard.xml",
        "reports/paperformat.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}