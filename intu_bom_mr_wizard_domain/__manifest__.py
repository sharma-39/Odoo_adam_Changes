{
    'name': 'MRP BOM MR Flag',
    'version': '1.0',
    'summary': 'Prevents duplicate Material Requests by validating BOM quantity fulfillment',
    'description': 'This module extends the Manufacturing (MRP) process by controlling Material Request creation based on BOM quantity fulfillment. It compares BOM quantity with existing Material Request quantity and hides the Create MR button when the required quantity is already satisfied, preventing duplicate or unnecessary requests and ensuring accurate procurement flow.',
    'depends': ['mrp'],
    'data': [
        'views/mrp_bom_view.xml',
    ],
    'installable': True,
    'application': False,
}