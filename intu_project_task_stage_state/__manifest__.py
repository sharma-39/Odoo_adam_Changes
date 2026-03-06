{
    'name': 'Project Task Stage Auto State',
    'version': '1.0',
    'summary': 'Automatically update task state when stage changes',
    'author': 'Custom',
    'depends': ['base','project','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
}