{
    "name": "Product Category BOM Flag (BOM Changes)",
    "version": "1.0",
    "summary": "Adds a BOM applicability checkbox in Product Category for manufacturing control",
    "category": "Inventory",
    "description": """
Product Category BOM Flag Module
===============================

This module extends the Product Category model to include a BOM (Bill of Materials) control flag.

Key Features:
-------------
- Adds a BOM checkbox in Product Category
- Controls whether products in a category are eligible for BOM usage
- Integration with Manufacturing (MRP) module
- Helps classify products for production workflow
- Supports better manufacturing planning and control

Business Benefits:
------------------
- Improved control over manufacturing eligibility
- Better product categorization for production
- Reduced errors in BOM creation
- Streamlined manufacturing configuration
- Clear separation of manufacturable vs non-manufacturable categories

Dependencies:
-------------
- product
- project
- mrp

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "depends": ["product", "project", "mrp"],
    "data": [
        "views/product_category_view.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}