{
    "name": "Customized Job Order Report",
    "version": "1.0",
    "category": "Sales",
    "summary": "Custom external layout and print format for Sale Order / Job Order reports",
    "description": """
Customized Job Order Report Module
==================================

This module customizes the standard Sale Order report in Odoo by introducing a tailored Job Order layout and external report design.

Key Features:
-------------
- Custom Job Order quotation report format
- Customized external layout for sale orders
- Standard and quotation-specific report templates
- Custom paper format for print optimization
- Improved document presentation for customers

Business Benefits:
------------------
- Professional and branded quotation/Job Order output
- Improved readability of sales documents
- Better customer communication
- Standardized printing format across organization
- Enhanced reporting presentation

Dependencies:
-------------
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "depends": ["sale"],
    "data": [
        "reports/job_quotation_report.xml",
        "reports/web_external_layout_quotation.xml",
        "reports/web_external_layout_standard.xml",
        "reports/paperformat.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}