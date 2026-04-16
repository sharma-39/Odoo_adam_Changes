{
    'name': 'MR Wizard',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Material Request Wizard for creating and managing Material Requests efficiently',
    'description': """
Material Request Wizard Module
=============================

This module provides a wizard-based interface to create and manage Material Requests (MR) efficiently within Odoo.

Key Features:
-------------
- Wizard-based Material Request creation
- Streamlined MR generation process
- Integration with Sales, Project, HR, Product, UoM, and Purchase modules
- Simplified workflow for material planning
- Faster and controlled MR creation process

Business Benefits:
------------------
- Reduces manual effort in creating material requests
- Improves procurement planning efficiency
- Enhances coordination between Sales, Project, and Purchase teams
- Provides structured and guided MR creation process
- Reduces errors in material requirement capture

Dependencies:
-------------
- base
- sale
- project
- hr
- product
- uom
- purchase

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'author': 'Custom',
    'depends': [
        'base',
        'sale',
        'project',
        'hr',
        'product',
        'uom',
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mr_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}