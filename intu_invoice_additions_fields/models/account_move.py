from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        # 1. Pre-process the values before creation
        for vals in vals_list:
            origin = vals.get('invoice_origin')
            if origin and origin.startswith('PO'):
                vals['payment_reference'] = origin
                # If you want it blank on creation:
                vals['narration'] = ""

        # 2. Create the records
        records = super(AccountMove, self).create(vals_list)
        return records

    def write(self, vals):
        # 4. Handle updates to existing records
        res = super(AccountMove, self).write(vals)

        # If narration was updated, post to chatter
        if 'narration' in vals:
            for record in self:
                record.message_post(body="Terms & Condition Updated Successfully")
        return res


    x_studio_payment_received_amount = fields.Float(
        string="Payment Received Amount",
        compute="_compute_payment_received_amount",
        store=True,
        copy=True
    )

    @api.depends(
        'line_ids.matched_debit_ids.amount',
        'line_ids.matched_credit_ids.amount',
        'line_ids.account_id'
    )
    def _compute_payment_received_amount(self):
        """
        Compute total payment received based on reconciled receivable/payable lines.
        This is the correct accounting way.
        """
        for move in self:
            total = 0.0

            # Only calculate for customer invoices and vendor bills
            if move.move_type in ('out_invoice', 'in_invoice'):
                for line in move.line_ids:

                    # Check receivable/payable accounts
                    if line.account_id.account_type in (
                            'asset_receivable',
                            'liability_payable'
                    ):

                        # Add matched credit amounts
                        for partial in line.matched_credit_ids:
                            total += partial.amount

                        # Add matched debit amounts
                        for partial in line.matched_debit_ids:
                            total += partial.amount

            move.x_studio_payment_received_amount = total
    # =====================================================
    # SALE ORDER AUTO LINK FROM INVOICE LINES
    # =====================================================

    x_studio_sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        compute="_compute_sale_order",
        copy=True
    )

    x_studio_sale_order_label = fields.Char(
        string="Sale Order Label",
        compute="_compute_sale_order",
        copy=True
    )

    @api.depends('invoice_line_ids.sale_line_ids.order_id')
    def _compute_sale_order(self):
        for invoice in self:
            sale_orders = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')

            if sale_orders:
                invoice.x_studio_sale_order_id = sale_orders[0].id
                names = ', '.join(sale_orders.mapped('name'))
                totals = ', '.join(str(so.amount_total) for so in sale_orders)
                invoice.x_studio_sale_order_label = f"{names} - {totals}"
            else:
                invoice.x_studio_sale_order_id = False
                invoice.x_studio_sale_order_label = False

    # =====================================================
    # PROJECT FROM SALE ORDER
    # =====================================================

    x_projects = fields.Many2one(
        "project.project",
        string="Project",
        compute="_compute_project",
        copy=True
    )

    @api.depends('x_studio_sale_order_id')
    def _compute_project(self):
        for record in self:
            record.x_projects = record.x_studio_sale_order_id.project_id.id if record.x_studio_sale_order_id else False

    # =====================================================
    # PROJECT RELATED FIELDS
    # =====================================================

    x_allocated_time = fields.Float(
        string="Total Labour Hour",
        compute="_compute_project_fields",
        copy=True
    )

    x_invoice_project_budget = fields.Float(
        string="Total Budget",
        compute="_compute_project_fields",
        copy=True
    )

    x_invoice_project_remain_budget = fields.Float(
        string="Remaining Budget",
        compute="_compute_project_fields",
        copy=True
    )

    x_invoice_project_status = fields.Many2one(
        "project.task.type",
        string="Project Status",
        compute="_compute_project_fields",
        copy=True
    )

    x_studio_project_percentage = fields.Float(
        string="Project %",
        compute="_compute_project_fields",
        copy=True
    )

    @api.depends(
        'x_projects',
        'x_projects.allocated_hours',
        'x_projects.x_studio_total_sales_budget',
        'x_projects.x_studio_material_budget',
        'x_projects.stage_id',
        'x_projects.x_studio_progress_percentage'
    )
    def _compute_project_fields(self):
        for record in self:
            if record.x_projects:
                project = record.x_projects
                record.x_allocated_time = project.allocated_hours or 0.0
                record.x_invoice_project_budget = project.x_studio_total_sales_budget or 0.0
                record.x_invoice_project_remain_budget = project.x_studio_material_budget or 0.0
                record.x_invoice_project_status = project.stage_id.id
                record.x_studio_project_percentage = project.x_studio_progress_percentage or 0.0
            else:
                record.x_allocated_time = 0.0
                record.x_invoice_project_budget = 0.0
                record.x_invoice_project_remain_budget = 0.0
                record.x_invoice_project_status = False
                record.x_studio_project_percentage = 0.0

    # =====================================================
    # SALE ORDER RELATED FIELDS
    # =====================================================

    x_invoice_sales_order_status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', 'Quotation Sent'),
            ('sale', 'Sale Order'),
            ('cancel', 'Cancelled')
        ],
        string="SO Status",
        compute="_compute_sale_order_fields",
        copy=True
    )

    x_invoice_status = fields.Char(
        string="Invoice Status",
        compute="_compute_sale_order_fields",
        copy=True
    )

    x_sale_labour_cost = fields.Float(
        string="Total Labour Cost",
        compute="_compute_sale_order_fields",
        copy=True
    )

    x_sale_order_so_value = fields.Float(
        string="Project Value",
        compute="_compute_sale_order_fields",
        copy=True
    )

    x_sales_order_status = fields.Char(
        string="SO Status (Char)",
        compute="_compute_sale_order_fields",
        copy=True
    )

    @api.depends(
        'x_studio_sale_order_id',
        'x_studio_sale_order_id.state',
        'x_studio_sale_order_id.amount_total',
        'x_studio_sale_order_id.x_alc_total',
        'x_studio_sale_order_id.x_sales_order_invoice_status'
    )
    def _compute_sale_order_fields(self):
        for record in self:
            so = record.x_studio_sale_order_id

            if so:
                record.x_invoice_sales_order_status = so.state
                record.x_invoice_status = so.x_sales_order_invoice_status
                record.x_sale_labour_cost = so.x_alc_total or 0.0
                record.x_sale_order_so_value = so.amount_total or 0.0
                record.x_sales_order_status = so.state
            else:
                record.x_invoice_sales_order_status = False
                record.x_invoice_status = False
                record.x_sale_labour_cost = 0.0
                record.x_sale_order_so_value = 0.0
                record.x_sales_order_status = False

    # =====================================================
    # PAYMENT RELATED
    # =====================================================

    x_received_amt = fields.Float(
        string="Received Payment",
        compute="_compute_received_amt",
        copy=True
    )

    # =====================================================
    # VENDOR TRN
    # =====================================================

    x_studio_vendor_trn_no = fields.Char(
        string="TRN No",
        compute="_compute_vendor_trn",
        copy=True
    )

    x_studio_vendor_trn_no_1 = fields.Char(
        string="TRN No 2",
        compute="_compute_vendor_trn",
        copy=True
    )

    x_studio_paid_amt = fields.Float(
        string="Paid Amount",
        compute="_compute_paid_amount",
        copy=True
    )

    @api.depends('amount_total', 'amount_residual', 'move_type', 'state')
    def _compute_paid_amount(self):
        for record in self:
            if record.move_type in ('out_invoice', 'in_invoice') and record.state == 'posted':
                record.x_studio_paid_amt = record.amount_total - record.amount_residual
            else:
                record.x_studio_paid_amt = 0.0


    @api.depends('partner_id', 'partner_shipping_id')
    def _compute_vendor_trn(self):
        for record in self:
            record.x_studio_vendor_trn_no = record.partner_id.vat if record.partner_id else False
            record.x_studio_vendor_trn_no_1 = record.partner_shipping_id.vat if record.partner_shipping_id else False

    # =====================================================
    # PRINT OPTION SELECTION
    # =====================================================

    x_studio_print_jod_as_customer_ref = fields.Selection(
        [
            ('source_document', 'Source Document'),
            ('customer_reference', 'Customer Reference')
        ],
        string="Print JOD as Customer Ref"
    )