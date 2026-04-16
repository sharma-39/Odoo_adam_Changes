{
    'name': 'Master Report Sales',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Centralized master list view for Sales reporting with multi-module integration',
    'description': """
Master Report Sales Module
=========================

This module provides a centralized master reporting view for sales-related data by integrating information from multiple Odoo modules.

Key Features:
-------------
- Centralized Sales Master Report list view
- Integration with Sales, Project, Purchase, and Accounting modules
- Consolidated reporting for business analysis
- Enhanced visibility of cross-module transactions
- Custom list view for reporting and tracking

Business Benefits:
------------------
- Single view for sales-related operations
- Better decision-making with unified data
- Improved cross-module visibility (Sales, Project, Purchase, Accounting)
- Simplified reporting structure for management
- Efficient data tracking across business processes

Dependencies:
-------------
- sale
- project
- purchase
- account

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Sharma M ',
    'depends': [
        'sale',
        'project',
        'purchase',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/x_sales_report_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}