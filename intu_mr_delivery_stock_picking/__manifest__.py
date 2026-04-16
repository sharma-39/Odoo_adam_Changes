{
    "name": "Custom Stock Picking Fields",
    "version": "1.0",
    "category": "Inventory",
    "summary": "Adds BOM, MR, and PO tracking fields to Stock Picking for improved traceability",
    "description": """
Custom Stock Picking Fields Module
==================================

This module extends the Stock Picking model to add additional tracking fields for better inventory and procurement traceability.

Fields Added:
-------------
- BOM Request (Boolean)
- MR Number (Char)
- PO MR Number (Char)
- PO Number (Char)

Technical Purpose:
------------------
These fields help track relationships between Material Requests (MR), Purchase Orders (PO), and BOM (Bill of Materials) within stock operations.

Business Benefits:
------------------
- Improved traceability across Inventory, Purchase, and Manufacturing
- Better tracking of procurement flow
- Easier debugging and audit of stock movements
- Clear linkage between MR → PO → Stock Picking process

Dependencies:
-------------
- stock

Author:
-------
Intulogic Private Limited - Sharma M
""",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}