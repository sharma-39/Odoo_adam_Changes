{
    "name": "Sale Order Custom Sequence & Product Creation",
    "summary": "Custom Sale Order numbering format (JOD|YEAR|000001) and automatic product creation on confirmation",
    "version": "1.0",
    "author": "Your Company Name",
    "category": "Sales",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "product"
    ],
    "description": """
Sale Order Custom Sequence & Product Creation Module
====================================================

This module enhances the Sales Order workflow by introducing a custom numbering sequence and automatic product creation logic during order confirmation.

Key Features:
-------------
- Custom Sales Order sequence format: JOD|YEAR|000001
- Year-based dynamic numbering system
- Automatic product creation when confirming Sales Order
- Seamless integration with Product and Sales modules
- Improved traceability and document identification

Business Logic:
--------------
1. Sales Order is assigned a custom sequence on creation:
   Format: JOD|YYYY|XXXXXX

2. On Sales Order confirmation:
   - System automatically creates products (based on configuration or order lines)
   - Ensures product availability for invoicing and delivery workflows

Business Benefits:
------------------
- Standardized Sales Order numbering format
- Better document tracking and identification
- Reduced manual product creation effort
- Faster order processing workflow
- Improved integration between Sales and Product modules

Dependencies:
-------------
- sale
- product

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "data": [
        "data/sequence.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}