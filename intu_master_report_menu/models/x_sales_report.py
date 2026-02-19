from odoo import models, fields


class XSalesReport(models.Model):
    _name = 'x_sales_report'
    _description = 'Master Report Sale'

    x_active = fields.Boolean(string="Active", default=True)

    x_name = fields.Char(string="Description")

    x_studio_customer = fields.Char(string="Customer")

    x_studio_customer_id = fields.Many2one(
        'res.partner',
        string="Customer"
    )

    x_studio_invoice_number = fields.Char(
        string="Invoice Number"
    )

    x_studio_invoice_status = fields.Selection([
        ('not_received', 'Not Received'),
        ('partial', 'Partially Received'),
        ('full', 'Fully Received'),
    ], string="Invoice Payment Status")

    x_studio_invoice_value = fields.Float(
        string="Invoice Value"
    )

    x_studio_actual_labour_cost = fields.Float(
        string="Actual Labour Cost"
    )

    x_studio_actual_total_cost = fields.Float(
        string="Actual Total Cost"
    )

    x_studio_job_order = fields.Char(
        string="Job Order"
    )
