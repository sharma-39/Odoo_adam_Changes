{
    "name": "Material Request (BOM Changes)",
    "version": "1.0",
    "category": "Custom",
    "summary": "Material Request module to manage material requests linked with BOM, Sales, Purchase, and Project",
    "description": """
Material Request Module
======================

This module introduces a Material Request system integrated with BOM (Bill of Materials), Sales, Purchase, Project, and Manufacturing modules.

Key Features:
-------------
- Material Request form and list view
- Integration with BOM (Manufacturing)
- Link with Sales Orders, Purchase Orders, and Projects
- Sequence generation for Material Requests
- Structured workflow for material requirement tracking
- Improved inventory planning and procurement coordination

Business Benefits:
------------------
- Better material planning and control
- Improved procurement workflow efficiency
- Seamless integration between Sales, Purchase, and Manufacturing
- Reduced material shortages and delays
- Centralized material request tracking system

Dependencies:
-------------
- mail
- sale
- project
- purchase
- mrp

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "depends": ["mail", "sale", "project", "purchase", "mrp"],
    "data": [
        "views/material_request_views.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}