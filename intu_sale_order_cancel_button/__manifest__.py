{
    'name': 'Sale Order Custom Approval Reset',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Resets approval and confirmation states automatically when Sale Order is cancelled',
    'description': """
Sale Order Custom Approval Reset Module
======================================

This module handles automatic reset of approval and confirmation states when a Sales Order is cancelled.

Key Features:
-------------
- Automatically resets approval fields on cancellation
- Clears confirmation-related flags
- Ensures consistent workflow state after cancel action
- Prevents invalid approved/cancelled mixed states
- Maintains clean Sales Order lifecycle control

Business Logic:
--------------
When a Sales Order is cancelled:
- Approval status is reset
- Confirmation flags are cleared
- Order state is normalized for re-processing or deletion logic

Business Benefits:
------------------
- Prevents inconsistent approval states
- Ensures clean workflow transitions
- Improves sales process reliability
- Avoids manual reset of approval fields
- Maintains data integrity in Sales Orders

Dependencies:
-------------
- sale

Author:
-------
Intulogic Private Limited - Sharma M
""",
    'depends': ['sale'],
    'data': [],
    'installable': True,
}