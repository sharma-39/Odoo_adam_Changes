{
    'name': 'Project Task Stage Auto State',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Automatically updates task state based on stage changes in Project tasks',
    'description': """
Project Task Stage Auto State Module
===================================

This module enhances Project Task management by automatically updating the task state when the stage is changed.

Key Features:
-------------
- Auto-update task state based on stage change
- Synchronization between task stage and state fields
- Improved workflow automation in project management
- Reduces manual updates in task lifecycle
- Ensures consistency between stage and status

Business Benefits:
------------------
- Improved workflow automation
- Reduced manual effort in task tracking
- Better consistency in project task lifecycle
- Enhanced project monitoring and control
- More accurate task status reporting

Dependencies:
-------------
- base
- project
- product

Author:
-------
Custom
""",
    'author': 'Custom',
    'depends': ['base', 'project', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}