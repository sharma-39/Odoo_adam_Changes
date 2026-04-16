{
    'name': 'Project OnCreate Action',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Auto-populates project fields from Sales Order during project creation',
    'description': """
Project OnCreate Action Module
=============================

This module automatically updates Project fields when a Project is created from a Sales Order.

Key Features:
-------------
- Auto-fetch Sales Order data during Project creation
- Sets Project name using Sales Order name and subject
- Auto-fills budget-related fields from Sales Order
- Ensures consistent mapping between Sales Order and Project
- Reduces manual data entry in project setup

Business Logic:
--------------
On project creation:
- Subject is taken from Sales Order (x_studio_subject)
- Project name is updated as: "ProjectName - Subject"
- Budget fields are populated from Sales Order AMC percentage total

Mapped Fields:
-------------
- x_studio_material_budget
- x_studio_remaining_budget
- x_studio_total_sales_budget

Dependencies:
-------------
- project
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'depends': ['project', 'sale'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}