from odoo import models, fields,api,_
from odoo.exceptions import UserError


# ==========================================
# Purchase Order Extension
# ==========================================
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    x_studio_rfq_enable_selection = fields.Selection(
        [
            ('approved', 'Approved'),
            ('not_approved', 'Not Approved'),
        ],
        string="RFQ Status",
        compute="_compute_rfq_status",
        copy=True,
        readonly=True
    )

    x_studio_amount_due = fields.Float(
        string="Amount Due",
        compute="_compute_amount_due",
        copy=True,
        readonly=True
    )
    x_studio_approvel_enable = fields.Boolean(string="Approval Enable")
    x_studio_budget = fields.Float(
        string="Remaining Budget",
        compute="_compute_remaining_budget",
        copy=True
    )
    x_studio_confirm = fields.Boolean(string="Confirm")
    x_studio_float_field_59q_1jcocq6ln = fields.Float(string="New Decimal")

    x_studio_many2many_field_2ug_1jbk4gjr5 = fields.Many2many(
        'res.partner',
        string="New Many2Many"
    )

    x_studio_mr_number = fields.Char(string="MR Number")

    x_studio_po_approve = fields.Boolean(string="RFQ Approved")
    x_studio_po_approved_widget = fields.Boolean(string="PO Approved Widget")

    x_studio_total_sales_budget = fields.Float(
        string="Total Sales Budget",
        compute="_compute_total_sales_budget",
        copy=True,
        readonly=True
    )
    x_studio_po_status = fields.Selection([
        ('Fully Paid', 'Fully Paid'),
        ('Partially Paid', 'Partially Paid'),
        ('Not Paid', 'Not Paid'),
    ], string="Payment Status", default="Not Paid",
        compute="_compute_po_payment_status",
        copy=True)

    x_studio_purchase_type = fields.Selection([
        ('Material Request', 'Material Request'),
        ('Normal Order', 'Normal Order')
    ], string="Purchase Type", default="Normal Order")

    x_studio_responsibility = fields.Many2one(
        'res.users',
        string="Responsible"
    )

    x_studio_rfq_number = fields.Char(string="RFQ Number",readonly=True)

    x_studio_sales_order = fields.Many2one(
        'sale.order',
        string="Sales Order",
        compute="_compute_sales_order_from_origin",
        copy=True,
        readonly=True
    )

    x_studio_text_field_9nt_1jbk4lnmp = fields.Text(string="Remarks")

    x_studio_total_before_discount = fields.Float(
        string="Total Before Discount",
        compute="_compute_total_before_discount",
        copy=True,
        readonly=True
    )
    x_studio_total_discount = fields.Float(string="Total Discount")

    x_studio_type = fields.Char(string="Type")
    x_studio_vendor_bill_paid_amount = fields.Float(
        string="Vendor Bill Paid Amount",
        compute="_compute_vendor_paid_amount",
        copy=True,
        readonly=True
    )
    x_studio_vendor_trn_no = fields.Char(
        string="TRN No",
        compute="_compute_vendor_trn",
        copy=True,
        readonly=True
    )
    x_studio_po_tags = fields.Many2many(
        'x_po_category',  # The destination model
        string="PO Tags"
    )


    @api.depends('x_studio_po_approve')
    def _compute_rfq_status(self):
        for record in self:
            if record.x_studio_po_approve:
                record.x_studio_rfq_enable_selection = 'approved'
            else:
                record.x_studio_rfq_enable_selection = 'not_approved'

    @api.depends('project_id')
    def _compute_remaining_budget(self):
        for record in self:
            if record.project_id:
                if record.project_id.x_studio_po_remaining_budget:
                    record.x_studio_budget = (
                            record.project_id.x_studio_po_remaining_budget or 0.0
                    )
                else:
                    record.x_studio_budget = (record.project_id.x_studio_total_sales_budget or 0.0);
            else:
                record.x_studio_budget = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Generate your custom reference first
            if not vals.get('x_studio_rfq_number'):
                vals['x_studio_rfq_number'] = self.env['ir.sequence'].next_by_code(
                    'purchase.order.ref_seq'
                )

        # Let Odoo create the record (it will probably assign a PO number here)
        records = super(PurchaseOrder, self).create(vals_list)

        # NOW force the name to 'New' for the created records
        # This overwrites whatever the standard sequence just did
        records.write({'name': 'New'})

        return records

    @api.depends('project_id', 'project_id.x_studio_material_budget')
    def _compute_total_sales_budget(self):
        for record in self:
            if record.project_id:
                record.x_studio_total_sales_budget = (
                        record.project_id.x_studio_material_budget or 0.0
                )
            else:
                record.x_studio_total_sales_budget = 0.0

    @api.depends('partner_id', 'partner_id.vat')
    def _compute_vendor_trn(self):
        for record in self:
            if record.partner_id:
                record.x_studio_vendor_trn_no = record.partner_id.vat or False
            else:
                record.x_studio_vendor_trn_no = False

    @api.depends(
        'invoice_ids.state',
        'invoice_ids.payment_state',
        'invoice_ids.x_studio_paid_amt'
    )
    def _compute_vendor_paid_amount(self):
        for record in self:
            total_paid = 0.0

            for inv in record.invoice_ids:
                if inv.state != 'cancel' and inv.payment_state in ('paid', 'in_payment', 'partial'):
                    total_paid += inv.x_studio_paid_amt or 0.0

            record.x_studio_vendor_bill_paid_amount = total_paid

    @api.depends('origin')
    def _compute_sales_order_from_origin(self):
        for record in self:
            sale_order = False

            if record.origin:
                picking = self.env['stock.picking'].search(
                    [('name', '=', record.origin)],
                    limit=1
                )

                if picking and picking.sale_id:
                    sale_order = picking.sale_id.id

            record.x_studio_sales_order = sale_order

    @api.depends(
        'invoice_ids.state',
        'invoice_ids.payment_state',
        'invoice_ids.amount_residual'
    )
    def _compute_amount_due(self):
        for record in self:
            total = 0.0

            for inv in record.invoice_ids:
                # Skip cancelled invoices
                if inv.state == 'cancel':
                    continue

                # Exclude fully unpaid
                if inv.payment_state != 'not_paid':
                    total += inv.amount_residual or 0.0

            record.x_studio_amount_due = total

    @api.depends(
        'x_studio_amount_due', 'amount_total', 'state', 'x_studio_vendor_bill_paid_amount'
    )
    def _compute_po_payment_status(self):
        for record in self:
            invoice_count = 0

            if record.invoice_ids:
                invoice_count = len(
                    record.invoice_ids.filtered(
                        lambda inv: inv.state != "cancel" and inv.payment_state in ('paid', 'in_payment', 'partial')
                    )
                )

            po_total = record.amount_total or 0.0
            paid_amt = record.x_studio_vendor_bill_paid_amount or 0.0

            status = "Not Paid"  # Default

            if invoice_count != 0 and record.state == "purchase":
                # Fully Paid (with float tolerance)
                if abs(paid_amt - po_total) < 0.01:
                    status = "Fully Paid"

                # Not Paid
                elif abs(paid_amt) < 0.01:
                    status = "Not Paid"

                # Partially Paid
                elif 0.01 < paid_amt < po_total:
                    status = "Partially Paid"

                # Fallback
                else:
                    status = "Not Paid"

            record.x_studio_po_status = status

    @api.depends(
        'order_line.product_qty',
        'order_line.price_unit',
        'order_line.price_subtotal',
        'order_line.price_total',
        'amount_total',
        'amount_untaxed'
    )
    def _compute_total_before_discount(self):
        for order in self:
            total = sum(
                (line.product_qty * line.price_unit)
                for line in order.order_line
            )
            order.x_studio_total_before_discount = total

    def action_custom_approve(self):
        for record in self:

            # 1️⃣ Check Order Lines
            if not record.order_line:
                raise UserError(
                    _("❌ Unable to approve: The Purchase Order has no Order Lines.")
                )

            # 2️⃣ Budget Validation (Except Normal Order)
            if record.x_studio_purchase_type != "Normal Order":
                remaining_budget = record.project_id.x_studio_po_remaining_budget or 0.0

                if record.amount_total > remaining_budget:
                    raise UserError(_(
                        "⚠️ Purchase Order total (%s) exceeds the budget limit (%s)"
                    ) % (record.amount_total, remaining_budget))

            # 3️⃣ Vendor Restriction
            partner_name = record.partner_id.name or ""
            if "ADAM EMC" in partner_name.upper():
                raise UserError(_(
                    "Kindly revise the Vendor Name so that it does not proceed with the AMC vendor."
                ))

            # 4️⃣ Approve
            record.write({
                'x_studio_po_approved_widget': False,
                'x_studio_po_approve': True
            })

        return True

    def button_confirm(self):
        # 1. Run the standard Odoo confirmation logic
        res = super(PurchaseOrder, self).call_button_confirm()  # or super().button_confirm()

        for record in self:
            # 2. Check if the name is still 'New' or was just assigned the default '/'
            # We also check if it's in the 'purchase' state as confirmed by super()
            if record.state <= 'purchase' and record.name in ('New', '/', False):

                # 3. Fetch your specific sequence
                new_name = self.env['ir.sequence'].next_by_code('purchase.order.normal')

                # 4. Use write() to bypass standard sequence protection
                if new_name:
                    record.write({'name': new_name})

        return res

    def button_confirm(self):
        res = super().button_confirm()

        for record in self:
            if record.state == 'purchase' and record.name in ('New', False):
                next_seq = self.env['ir.sequence'].next_by_code(
                    'purchase.order.normal'
                )

                record.name = next_seq

            if record.project_id:
                record.project_id.write({
                    # remaining Budget
                    'x_studio_purchase_budget': record.project_id.x_studio_purchase_budget + record.amount_total,
                })
        return res

    def button_approve_custom(self):
        """ Custom Approve Button Logic """
        for record in self:
            partner_name = record.partner_id.name or ""

            # 1. Vendor Check
            if "ADAM EMC" in partner_name.upper():
                raise UserError("🛑 Revision Required: Orders cannot proceed with the AMC vendor (ADAM EMC).")

            # 2. Lines Check
            if not record.order_line:
                raise UserError("❌ Unable to approve: The Purchase Order has no Order Lines.")

            # 3. Budget Validation
            if record.x_studio_purchase_type != "Normal Order" and record.project_id:
                remaining = record.project_id.x_studio_po_remaining_budget or 0.0
                if record.amount_total > remaining:
                    raise UserError(
                        f"⚠️ Budget Exceeded!\nTotal: {record.amount_total:,.2f}\nRemaining: {remaining:,.2f}")

            # 4. Mark Approved
            record.write({
                'x_studio_po_approved_widget':False,
                'x_studio_po_approve': True
            })


# ==========================================
# Purchase Order Line Extension
# ==========================================
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_purchase_type = fields.Char(string="Purchase Type Order")

    x_studio_purchase_type = fields.Boolean(string="Purchase Type")

    x_studio_purchase_type_selection = fields.Selection([
        ('Material Request', 'Material Request'),
        ('Normal Order', 'Normal Order'),
    ], string="Purchase Type")

    x_studio_remarks = fields.Char(string="Remarks")