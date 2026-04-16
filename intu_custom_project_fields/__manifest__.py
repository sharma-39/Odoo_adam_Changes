{
    'name': 'Custom Project Fields',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Migrating Studio fields to a custom module with project budgeting, progress, and invoice tracking enhancements',
    'description': """
Custom Project Fields Module
============================

This module replaces Odoo Studio fields with fully custom Python implementations for better control and performance.

Key Features:
-------------
- Adds Project Manager field in both Project and Task
- Task-level invoice progress tracking based on sale order line
- Project budget management (allocated, purchase, remaining)
- Material and delivery cost tracking
- Task-based and time-based progress calculation
- Project invoice status aggregation from tasks
- Advanced project analytics and KPIs

Business Benefits:
------------------
- Better project cost control
- Real-time progress tracking
- Improved invoice visibility
- Enhanced project performance analytics
- Eliminates dependency on Odoo Studio

Dependencies:
-------------
- hr_timesheet
- project
- hr

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'depends': ['hr_timesheet', 'project', 'hr'],
    'data': [
        'views/project_view.xml',
    ],
    'installable': True,
    'application': False,
}