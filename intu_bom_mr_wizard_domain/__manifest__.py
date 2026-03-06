{
    'name': 'MRP BOM MR Flag',
    'version': '1.0',
    'summary': 'Hide Create MR Button when BOM qty matches MR qty',
    'depends': ['mrp'],
    'data': [
        'views/mrp_bom_view.xml',
    ],
    'installable': True,
    'application': False,
}