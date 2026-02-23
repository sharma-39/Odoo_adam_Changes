{
    "name": "Customized Quotation Report",
    "version": "1.0",
    "category": "Sales",
    "summary": "Custom external layout for Sale Order",
    "depends": ["sale"],
    "data": [
        "reports/quotation_report.xml",
        "reports/web_external_layout_quotation.xml",
        "reports/web_external_layout_standard.xml",
        "reports/paperformat.xml",
    ],
    "installable": True,
    "application": False,
}