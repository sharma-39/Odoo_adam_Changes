{
    'name': 'Custom Sale Order Extra Fields',
    'version': '1.0',
    'summary': 'Adds Enquiry Ref, Attention, Subject, VAT, Approval Badge in Sale Order',
    'description': """
        Custom Sale Order module that adds:
        - Enquiry Reference (Required)
        - Attention To (Required)
        - Subject (Required)
        - PO Reference
        - VAT Included checkbox
        - Approval workflow fields (hidden)
        - SQ Approval badge in list view
        - Partner Shipping & Invoice visible
    """,
    'author': 'Your Company Name',
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
