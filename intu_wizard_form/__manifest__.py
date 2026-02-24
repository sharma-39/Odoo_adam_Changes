{
    'name': '(Bom Changes) Custom Models Wizard Form',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Custom Wizard Form with Lines',
    'author': 'Sharma Murugaiyan',
    'depends': ['base', 'sale', 'project', 'uom'],
    'data': [
        'views/wizard_form_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}