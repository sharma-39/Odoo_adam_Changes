{
    'name': 'Custom Product Labour Cost',
    'version': '1.0',
    'summary': 'Adds Labour Cost field to Product Template for costing and pricing analysis',
    'description': """
Custom Product Labour Cost Module
================================

This module extends the Product Template model by adding a Labour Cost field to support enhanced product costing structure.

Key Features:
-------------
- Adds Labour Cost field in Product Template
- Placed below Standard Price for better visibility
- Supports product cost calculation and pricing analysis
- Helps in manufacturing and service cost evaluation
- Improves product profitability tracking

Business Benefits:
------------------
- Better cost breakdown (Material + Labour)
- Improved pricing strategy
- Enhanced product profitability analysis
- Useful for manufacturing and service-based costing
- Better financial transparency in product management

Dependencies:
-------------
- product

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'category': 'Inventory',
    'author': 'Intulogic Private Limited - Sharma M',
    'depends': ['product'],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}