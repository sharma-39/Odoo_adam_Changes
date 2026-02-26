{
    "name": "Purchase Custom Report",
    "version": "1.0",
    "category": "purchase",
    "summary": "Purchase Report summary",
    "depends": ["purchase", "account"],
    "data": [
        "reports/purchase_report.xml",
        "reports/report_action.xml",
        "views/purchase_order_view.xml",

    ],
    "installable": True,
    "application": False,
}
