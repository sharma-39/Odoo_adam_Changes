{
    'name': 'Custom Sales Quotation Sequence (SQ)',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Generates custom Sales Quotation number in format SQ|YEAR|00001 on creation',
    'description': """
Custom Sales Quotation Sequence Module
=====================================

This module customizes the Sales Order numbering system to generate quotation numbers in a structured format.

Sequence Format:
---------------
SQ|YYYY|00001

Key Features:
-------------
- Auto-generate Sales Quotation number on creation
- Year-based sequence reset
- Custom prefix format (SQ|YEAR|)
- Improved quotation tracking and identification
- Ensures unique and structured Sales Order numbering

Business Benefits:
------------------
- Standardized quotation numbering system
- Easier tracking of sales quotations
- Improved reporting and audit traceability
- Better document organization
- Professional sales document identification

Dependencies:
-------------
- sale

Author:
-------
Your Name
""",
    'author': 'Your Name',
    'depends': ['sale'],
    'data': [
        'data/sequence.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}