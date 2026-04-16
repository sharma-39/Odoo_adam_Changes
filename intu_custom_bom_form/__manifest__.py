{
    "name": "(BOM Changes) Custom MRP BOM Form",
    "version": "1.0",
    "category": "Manufacturing",
    "summary": "Improves and customizes the MRP BOM form layout for better usability",
    "description": "This module extends the standard Odoo Manufacturing (MRP) functionality by customizing the Bill of Materials (BOM) form view. It enhances the layout structure to improve readability, user experience, and structured data entry. The module is purely a UI enhancement and does not modify core manufacturing logic or calculations.",
    "depends": ["mrp", "product"],
    "data": [
        "views/mrp_bom_view.xml",
    ],
    "installable": True,
    "application": False,
}