{
    'name': 'Sale Order Budget',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Adds material, labour cost tracking and budget computation on Sales Orders and Order Lines',
    'description': """
Sale Order Budget Module
=======================

This module extends Sales Order and Sales Order Line functionality to support advanced budgeting, cost tracking, and profitability analysis.

Key Features:
-------------
Sale Order Line Enhancements:
- Material Cost (AMC)
- Labour Cost (ALC)
- Unit Material Cost (UCM)
- Unit Labour Cost (ULC)
- Total Cost (Material + Labour)
- Cost validation against sales price

Sale Order Enhancements:
- Total AMC (Material Cost Sum)
- Total ALC (Labour Cost Sum)
- Combined Cost Calculation
- AMC Percentage-based budget allocation
- Project material budget share computation

Business Benefits:
------------------
- Accurate cost tracking per sales order
- Better profitability analysis
- Controlled budget allocation
- Improved pricing strategy
- Early detection of cost overruns
- Better integration between sales and project costing

Dependencies:
-------------
- sale

Author:
-------
IntuLogic Private Limited
""",
    'category': 'Sales',
    'author': 'IntuLogic Private Limited',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}