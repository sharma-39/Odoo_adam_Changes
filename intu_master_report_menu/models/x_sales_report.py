from odoo import models, fields, api


class XSalesReport(models.Model):
    _name = 'x_sales_report'
    _description = 'Master Report Sale'
    _order = 'x_studio_sequence asc'

    # -----------------------
    # BASIC
    # -----------------------

    x_active = fields.Boolean(string="Active", default=True)
    x_name = fields.Char(string="Description")
    x_studio_sequence = fields.Integer(string="Sequence")

    # -----------------------
    # CUSTOMER
    # -----------------------

    x_studio_customer = fields.Char(string="Customer")

    x_studio_customer_id = fields.Many2one(
        'res.partner',
        string="Customer"
    )

    # -----------------------
    # SALES / PROJECT
    # -----------------------

    x_studio_sales_order = fields.Many2one(
        'sale.order',
        string="PROJECT"
    )

    x_studio_projects = fields.Many2one(
        'project.project',
        string="SUBJECT",
        compute="_compute_project",
        copy=True
    )

    x_studio_quote_no = fields.Char(string="Quote No")

    x_studio_job_order = fields.Char(string="Job Order")

    x_studio_project_ = fields.Float(
        string="Project %",
        compute="_compute_project_percentage",
        copy=True
    )

    x_studio_project_value = fields.Float(
        string="Project Value",
        compute="_compute_project_value",
        copy=True
    )

    x_studio_project_total_materials_cost = fields.Float(
        string="Total Material Cost",
        compute="_compute_material_cost",
        copy=True
    )

    x_studio_total_budget = fields.Float(
        string="Total Budget",
        compute="_compute_total_budget",
        copy=True
    )

    x_studio_remaining_budget = fields.Float(
        string="Remaining Budget",
        compute="_compute_remaining_budget",
        copy=True
    )

    # -----------------------
    # LABOUR
    # -----------------------

    x_studio_actual_labour_cost = fields.Float(
        string="Actual Labour Cost",
        compute="_compute_actual_labour_cost",
        copy=True,

    )

    x_studio_total_labour_cost = fields.Float(
        string="Total Labour Cost",
        compute="_compute_total_labour_cost",
        copy=True
    )

    x_studio_total_labour_hour = fields.Float(
        string="Total Labour Hour",
        compute="_compute_total_labour_hour",
        copy=True
    )

    x_studio_actual_total_cost = fields.Float(
        string="Actual Total Cost",
        compute="_compute_actual_total_cost",
        copy=True
    )

    # -----------------------
    # INVOICE
    # -----------------------

    x_studio_invoice_number = fields.Char(
        string="Invoice Number",
        compute="_compute_invoice_number",
        copy=True
    )

    x_studio_invoice_status = fields.Selection([
        ('not_received', 'Not Received'),
        ('partial', 'Partially Received'),
        ('full', 'Fully Received'),
    ], string="Invoice Payment Status",
       compute="_compute_invoice_payment_status",
       copy=True
    )

    x_studio_project_invoice_status = fields.Float(
        string="Project Invoice Status (%)",
        compute="_compute_invoice_progress",
        copy=True
    )

    x_studio_invoice_value = fields.Float(
        string="Invoice Value",
        compute="_compute_invoice_value",
        copy=True
    )

    x_studio_received_payment = fields.Float(
        string="Received Payment",
        compute="_compute_received_payment",
        copy=True
    )

    x_studio_pending_payment = fields.Float(
        string="Pending Payment",
        compute="_compute_pending_payment",
        copy=True
    )

    # =====================================================
    # COMPUTE METHODS
    # =====================================================

    @api.depends('x_studio_sales_order')
    def _compute_project(self):
        for record in self:
            record.x_studio_projects = (
                record.x_studio_sales_order.project_id
                if record.x_studio_sales_order else False
            )

    # -----------------------------------------------------

    @api.depends('x_studio_projects.task_completion_percentage')
    def _compute_project_percentage(self):
        for record in self:
            record.x_studio_project_ = (
                record.x_studio_projects.task_completion_percentage
                if record.x_studio_projects else 0.0
            )

    # -----------------------------------------------------

    @api.depends('x_studio_quote_no')
    def _compute_project_value(self):
        for record in self:
            if record.x_studio_quote_no:
                order = self.env['sale.order'].search([
                    ('x_order_reference_number', '=', record.x_studio_quote_no)
                ], limit=1)
                record.x_studio_project_value = order.amount_total if order else 0.0
            else:
                record.x_studio_project_value = 0.0

    # -----------------------------------------------------

    @api.depends('x_studio_projects')
    def _compute_material_cost(self):
        for record in self:
            if record.x_studio_projects:
                purchase_orders = self.env['purchase.order'].search([
                    ('project_id', '=', record.x_studio_projects.id)
                ])
                record.x_studio_project_total_materials_cost = sum(
                    purchase_orders.mapped('amount_total')
                )
            else:
                record.x_studio_project_total_materials_cost = 0.0

    # -----------------------------------------------------

    @api.depends('x_studio_projects')
    def _compute_total_budget(self):
        for record in self:
            record.x_studio_total_budget = (
                record.x_studio_projects.x_studio_total_sales_budget
                if record.x_studio_projects else 0.0
            )

    @api.depends('x_studio_projects','x_studio_sales_order')
    def _compute_actual_labour_cost(self):
        for record in self:
            total_labour_cost = 0.0
            project = record.x_studio_projects
            if project:
                # Calculate used hours
                used_hours = project.allocated_hours - project.remaining_hours
                # Get company's labour cost safely
                labour_rate = 0.0
                if record.x_studio_sales_order and record.x_studio_sales_order.company_id:
                    labour_rate = record.x_studio_sales_order.company_id.x_studio_labour_cost or 0.0
                total_labour_cost = used_hours * labour_rate

            record['x_studio_actual_labour_cost'] = total_labour_cost

    # -----------------------------------------------------

    @api.depends('x_studio_projects')
    def _compute_remaining_budget(self):
        for record in self:
            record.x_studio_remaining_budget = (
                record.x_studio_projects.x_studio_po_remaining_budget
                if record.x_studio_projects else 0.0
            )

    # -----------------------------------------------------

    @api.depends('x_studio_sales_order')
    def _compute_total_labour_cost(self):
        for record in self:
            record.x_studio_total_labour_cost = (
                record.x_studio_sales_order.x_alc_total
                if record.x_studio_sales_order else 0.0
            )

    # -----------------------------------------------------

    @api.depends(
        'x_studio_projects.allocated_hours',
        'x_studio_projects.remaining_hours'
    )
    def _compute_total_labour_hour(self):
        for record in self:
            if record.x_studio_projects:
                record.x_studio_total_labour_hour = (
                    (record.x_studio_projects.allocated_hours or 0.0)
                    - (record.x_studio_projects.remaining_hours or 0.0)
                )
            else:
                record.x_studio_total_labour_hour = 0.0

    @api.depends(
        'x_studio_project_total_materials_cost','x_studio_actual_labour_cost'
    )
    def _compute_actual_total_cost(self):
        for record in self:
            tmc = record.x_studio_project_total_materials_cost or 0.0;
            alc = record.x_studio_actual_labour_cost or 0.0
            record['x_studio_actual_total_cost'] = tmc + alc
    # -----------------------------------------------------

    @api.depends('x_studio_invoice_number')
    def _compute_received_payment(self):
        for record in self:
            total_received = 0.0
            if record.x_studio_invoice_number:
                invoice_numbers = [
                    num.strip()
                    for num in record.x_studio_invoice_number.split(',')
                ]

                invoices = self.env['account.move'].search([
                    ('name', 'in', invoice_numbers),
                    ('move_type', '=', 'out_invoice')
                ])

                total_received = sum(
                    invoices.mapped('x_studio_payment_received_amount')
                )

            record.x_studio_received_payment = total_received

    # -----------------------------------------------------

    @api.depends('x_studio_project_value', 'x_studio_received_payment')
    def _compute_pending_payment(self):
        for record in self:
            pending = (
                (record.x_studio_project_value or 0.0)
                - (record.x_studio_received_payment or 0.0)
            )
            record.x_studio_pending_payment = pending if pending > 0 else 0.0

    # -----------------------------------------------------

    @api.depends(
        'x_studio_sales_order.invoice_ids.amount_total',
        'x_studio_sales_order.amount_total'
    )
    def _compute_invoice_progress(self):
        for record in self:
            order = record.x_studio_sales_order
            if order:
                total = order.amount_total or 0.0
                invoiced = sum(order.invoice_ids.mapped('amount_total'))

                if total > 0:
                    percent = (invoiced / total) * 100
                    record.x_studio_project_invoice_status = min(percent, 100)
                else:
                    record.x_studio_project_invoice_status = 0.0
            else:
                record.x_studio_project_invoice_status = 0.0

    # -----------------------------------------------------

    @api.depends('x_studio_received_payment', 'x_studio_project_value')
    def _compute_invoice_payment_status(self):
        for record in self:
            total = record.x_studio_project_value or 0.0
            received = record.x_studio_received_payment or 0.0

            if received == 0:
                record.x_studio_invoice_status = 'not_received'
            elif received < total:
                record.x_studio_invoice_status = 'partial'
            else:
                record.x_studio_invoice_status = 'full'

    @api.depends(
        'x_studio_invoice_number'
    )
    def _compute_invoice_value(self):
        for record in self:
            total_tax = 0.0

            if record.x_studio_invoice_number:
                # Always split (works for single & multiple)
                invoice_numbers = [
                    inv.strip()
                    for inv in record.x_studio_invoice_number.split(',')
                    if inv.strip()
                ]

                invoices = self.env['account.move'].search([
                    ('name', 'in', invoice_numbers),
                    ('move_type', '=', 'out_invoice'),
                ])

                total_tax = sum(invoices.mapped('amount_total'))

            record.x_studio_invoice_value = total_tax

    @api.depends('x_studio_sales_order')
    def _compute_invoice_number(self):
        for record in self:
            invoice_numbers = []

            if record.x_studio_sales_order:
                invoices = record.x_studio_sales_order.invoice_ids.filtered(
                    lambda inv: inv.state != 'cancel'
                )

                invoice_numbers = invoices.mapped('name')

            record.x_studio_invoice_number = ', '.join(invoice_numbers) if invoice_numbers else False
