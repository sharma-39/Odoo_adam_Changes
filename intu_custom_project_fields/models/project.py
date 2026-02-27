from odoo import models, fields,api

class Project(models.Model):
    _inherit = 'project.project'

    x_studio_total_sales_budget = fields.Float(string="Budget (Allocated)",readonly=True)
    x_studio_purchase_budget = fields.Float(string="PO Purchased Amount",readonly=True)

    x_studio_po_remaining_budget = fields.Float(
        string="PO Remaining Budget",
        compute="_compute_remaining_budget",
        readonly=True,
        copy=True  # Set to True if you want to search or group by this field
    )
    x_studio_project_cpercentage = fields.Float(
        string="Progress",
        compute="_compute_project_progress",
        store=True,
        readonly=True,  # Useful for seeing average progress in pivot views
    )

    x_studio_delivery_price = fields.Float(string="Delivery Price")
    x_studio_receipt_received = fields.Float(string="Receipt Received")

    x_studio_delivery_purchase_price = fields.Float(
        string="Stocked Materials Value",
        compute="_compute_delivery_purchase_price",
        copy=True,
        readonly=True,
    )
    x_studio_remaining_budget = fields.Integer(string="Remaining Budget")

    x_studio_material_budget = fields.Float(
        string="Remaining Material Budget",
        readonly=True,
    )

    x_studio_progress_percentage = fields.Float(
        string="Progress Percentage",
        compute="_compute_progress_time_based",
        copy=True
    )
    x_studio_project_cpercentage = fields.Float(
        string="Progress",
        compute="_compute_project_task_progress",
        copy=True,
        help="Percentage of closed tasks vs total tasks."
    )

    x_studio_project_invoice_status = fields.Integer(
        string="Project Invoice Status",
        compute="_compute_project_invoice_status",
        copy=True
    )
    x_studio_project_manager = fields.Many2one('hr.employee', string="Project Manager")
    x_studio_project_percentage = fields.Float(string="Project Percentage")

    @api.depends('x_studio_total_sales_budget', 'x_studio_purchase_budget', 'x_studio_delivery_purchase_price')
    def _compute_remaining_budget(self):
        for record in self:
            # Safely get values or default to 0.0
            total_budget = record.x_studio_total_sales_budget or 0.0
            purchase_amt = record.x_studio_purchase_budget or 0.0
            stocked_val = record.x_studio_delivery_purchase_price or 0.0

            # Logic: Subtracting both committed POs and stocked material costs
            # Using abs() if stocked_val is stored as a negative number
            if purchase_amt or stocked_val:
                record.x_studio_po_remaining_budget = total_budget - purchase_amt - abs(stocked_val)
            else:
                record.x_studio_po_remaining_budget = 0.0


   # @api.depends('x_studio_total_sales_budget', 'x_studio_delivery_price',
    #             'x_studio_purchase_budget', 'x_studio_delivery_purchase_price')
    #def _compute_material_budget(self):
            #    for record in self:
            # A1: Total Budget (e.g., 15,500)
            #A1 = record.x_studio_total_sales_budget or 0.0

            # Actual Delivery Price (The cost incurred so far)
            # Using your requested logic: abs(Budget - Delivery Price)
            #delivery_price = record.x_studio_delivery_price or 0.0

            # Final Calculation
            #record.x_studio_material_budget = abs(A1 - delivery_price)

    @api.depends('x_studio_purchase_budget', 'x_studio_delivery_price')
    def _compute_delivery_purchase_price(self):
        for record in self:
            # Calculate the raw difference
            # Delivery Price (Actual) - Purchase Budget (Planned)
            delivery = record.x_studio_delivery_price or 0.0
            budget = record.x_studio_purchase_budget or 0.0

            difference = delivery - budget

            # If you want to include the 5% overhead mentioned in your comment:
            # result = difference + (difference * 0.05)
            # Otherwise, use the standard difference:
            record.x_studio_delivery_purchase_price = difference

    @api.depends('task_count', 'closed_task_count')
    def _compute_project_progress(self):
        for record in self:
            # A1: Closed Tasks
            closed = record.closed_task_count or 0.0
            # A2: Total Tasks
            total = record.task_count or 0.0

            # Logic: (Closed / Total) * 100
            # The 'if total' check prevents "Division by Zero" errors
            if total > 0:
                record.x_studio_project_cpercentage = (closed / total) * 100.0
            else:
                record.x_studio_project_cpercentage = 0.0

    @api.depends('allocated_hours', 'remaining_hours')
    def _compute_progress_time_based(self):
        for record in self:
            allocated = record.allocated_hours or 0.0
            remaining = record.remaining_hours or 0.0

            if allocated > 0:
                # Progress = (Used Hours / Total Allocated) * 100
                # Note: (Allocated - Remaining) = Hours Spent
                raw_progress = ((allocated - remaining) / allocated) * 100

                # Logic: Keep it between 0.0 and 100.0
                record.x_studio_progress_percentage = max(0.0, min(raw_progress, 100.0))
            else:
                # If no hours are allocated, progress is technically undefined or 0
                record.x_studio_progress_percentage = 0.0

    @api.depends('task_count', 'closed_task_count')
    def _compute_project_task_progress(self):
        for record in self:
            # A1: Closed Tasks (Numerator)
            closed = record.closed_task_count or 0.0
            # A2: Total Tasks (Denominator)
            total = record.task_count or 0.0

            # Prevent DivisionByZero: If there are no tasks, progress is 0.
            if total > 0:
                record.x_studio_project_cpercentage = 100.0 * (closed / total)
            else:
                record.x_studio_project_cpercentage = 0.0

    @api.depends('task_ids.x_studio_task_invoice_status', 'task_ids.stage_id.fold')
    def _compute_project_invoice_status(self):
        for record in self:
            total_status_value = 0
            open_task_count = 0

            # Iterate through all tasks linked to this project
            for task in record.task_ids:
                # Only count tasks in active stages (not folded)
                if task.stage_id and not task.stage_id.fold:
                    open_task_count += 1
                    total_status_value += (task.x_studio_task_invoice_status or 0)

            # Calculate the average integer value
            if open_task_count > 0:
                record.x_studio_project_invoice_status = int(total_status_value / open_task_count)
            else:
                record.x_studio_project_invoice_status = 0

