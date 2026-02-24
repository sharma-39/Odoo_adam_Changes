{
    "name": "(BOm Changes)Material Request",
    "version": "1.0",
    "category": "Custom",
    "summary": "Material Request Management",
    "depends": ["mail", "sale", "project", "purchase"],
    "data": [
        "views/material_request_views.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
    ],
    "installable": True,
    "application": True,
}