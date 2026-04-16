{
    "name": "Invoice Custom Report",
    "version": "1.0",
    "category": "account",
    "summary": "Custom Invoice Report for enhanced purchase and accounting document printing",
    "description": "This module provides a custom invoice report in Odoo accounting. It enhances the standard invoice layout by adding a structured and user-friendly report format for better readability and professional document presentation.",
    "depends": ["account"],
    "data": [
        "reports/invoice_report.xml",
        "reports/report_action.xml",
        "views/invoice_report_view.xml"
    ],
    "installable": True,
    "application": False
}