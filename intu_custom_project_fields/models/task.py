from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # 1. Project Manager Field
    x_studio_project_manager = fields.Many2one(
        'hr.employee',
        string='Project Manager'
    )

    # 2. Task Invoice Status Field
    x_studio_task_invoice_status = fields.Integer(
        string='Task Invoice Status',
        compute='_compute_task_invoice_status',
        copy=True,  # Set to True if you want to search or group by this field
        help="Percentage of the linked sales order line that has been invoiced."
    )

    @api.depends('sale_line_id.qty_invoiced', 'sale_line_id.product_uom_qty')
    def _compute_task_invoice_status(self):
        for record in self:
            sale_line = record.sale_line_id

            # Check if sale line exists and has a quantity to avoid DivisionByZero
            if sale_line and sale_line.product_uom_qty > 0:
                # Calculate percentage
                percentage = (sale_line.qty_invoiced / sale_line.product_uom_qty) * 100

                # Ensure we don't exceed 100% and round to nearest whole number
                record.x_studio_task_invoice_status = int(round(min(percentage, 100)))
            else:
                # Default to 0 if no sales line is linked
                record.x_studio_task_invoice_status = 0