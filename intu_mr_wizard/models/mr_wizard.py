from odoo import models, fields,_,api
from odoo.exceptions import UserError

# =====================================================
# MAIN MODEL
# =====================================================
class MrWizard(models.Model):
    _name = 'x_mr_wizard'
    _description = 'MR Wizard'
    _rec_name = 'x_name'


    # =====================
    # BASIC
    # =====================
    x_name = fields.Char(string="Description")
    x_studio_mr_number = fields.Char(string="MR Number")
    x_studio_dr_number = fields.Char(string="DO Number")

    x_studio_flow = fields.Char(string="Flow")
    x_studio_flowss = fields.Char(string="Flowss")
    x_studio_job_order = fields.Char(string="Job Order")

    x_studio_job_order_no = fields.Many2one(
        'sale.order',
        string="Job Order"
    )

    x_studio_project = fields.Many2one(
        'project.project',
        string="Project"
    )

    x_studio_responsibility = fields.Many2one(
        'res.users',
        string="Responsibility"
    )

    x_studio_responsibility_emp = fields.Many2one(
        'hr.employee',
        string="Responsibility"
    )

    x_studio_validator = fields.Char(string="Validator")

    x_studio_total_rfq_qty = fields.Float(
        string="Total RFQ Qty"
    )

    # =====================
    # ONE2MANY
    # =====================
    x_mr_wizard_line_ids_e1f04 = fields.One2many(
        'x_mr_wizard_line_ba9e6',
        'x_mr_wizard_id',
        string="Order Lines"
    )

    @api.model_create_multi
    def create(self, vals_list):

        records = super().create(vals_list)

        for record in records:

            # -------------------------------------------------
            # 1️⃣ Find Material Request
            # -------------------------------------------------
            custom_forms = self.env['x_custom_form'].search([
                ('x_studio_mr_number', '=', record.x_studio_mr_number)
            ])

            # -------------------------------------------------
            # 2️⃣ Update Waiting PO Qty
            # -------------------------------------------------
            for wizard_line in record.x_mr_wizard_line_ids_e1f04:

                product = wizard_line.x_studio_mr_name
                rfq_qty = wizard_line.x_studio_rfq_qty or 0.0

                if rfq_qty <= 0:
                    continue

                for custom_form in custom_forms:
                    matching_lines = custom_form.x_custom_form_line_ids.filtered(
                        lambda l: l.x_studio_product == product
                    )

                    for line in matching_lines:
                        line.x_studio_waiting_po_qty += rfq_qty

            # -------------------------------------------------
            # 3️⃣ Group by Vendor
            # -------------------------------------------------
            vendor_lines = {}

            for wizard_line in record.x_mr_wizard_line_ids_e1f04:

                rfq_qty = wizard_line.x_studio_rfq_qty or 0.0
                if rfq_qty <= 0:
                    continue

                product = wizard_line.x_studio_mr_name
                vendor = wizard_line.x_studio_vendor_1
                unit = wizard_line.x_studio_unit

                if not vendor:
                    raise UserError(
                        _("Please select a Vendor for product: %s")
                        % product.display_name
                    )

                vendor_lines.setdefault(vendor.id, [])
                vendor_lines[vendor.id].append({
                    'product': product,
                    'qty': rfq_qty,
                    'remarks': wizard_line.x_name or '',
                    'unit': unit,
                })

            # -------------------------------------------------
            # 4️⃣ Create Purchase Orders
            # -------------------------------------------------
            PurchaseOrder = self.env['purchase.order']

            for vendor_id, lines in vendor_lines.items():

                order_lines = []

                for line_data in lines:
                    order_lines.append((0, 0, {
                        'product_id': line_data['product'].id,
                        'product_qty': line_data['qty'],
                        'product_uom_id': line_data['unit'].id,
                        'name': line_data['product'].display_name,
                        'price_unit': line_data['product'].standard_price,
                        'x_studio_remarks': line_data['remarks'],
                    }))

                po_vals = {
                    'partner_id': vendor_id,
                    'origin': record.x_studio_dr_number,
                    'project_id': record.x_studio_project.id if record.x_studio_project else False,
                    'x_studio_mr_number': record.x_studio_mr_number,
                    'x_studio_purchase_type': "Material Request",
                    'x_studio_responsibility': record.x_studio_responsibility_emp.id if record.x_studio_responsibility_emp else False,
                    'user_id': record.x_studio_responsibility.id if record.x_studio_responsibility else False,
                    'order_line': order_lines,
                }

                PurchaseOrder.create(po_vals)

        return records

# =====================================================
# LINE MODEL
# =====================================================
class MrWizardLine(models.Model):
    _name = 'x_mr_wizard_line_ba9e6'
    _description = 'MR Wizard Line'
    _rec_name = 'x_name'


    # =====================
    # RELATION
    # =====================
    x_mr_wizard_id = fields.Many2one(
        'x_mr_wizard',
        string="MR Wizard",
        ondelete='cascade'
    )

    # =====================
    # BASIC
    # =====================
    x_name = fields.Char(string="Remarks")
    x_studio_sequence = fields.Integer(string="Sequence")

    # =====================
    # PRODUCT
    # =====================
    x_studio_mr_name = fields.Many2one(
        'product.product',
        string="Component"
    )

    x_studio_unit = fields.Many2one(
        'uom.uom',
        string="Unit"
    )

    x_studio_qty = fields.Float(string="Qty")
    x_studio_qty_on_hand = fields.Float(string="Qty On Hand")
    x_studio_required = fields.Char(string="Required")
    x_studio_rfq_qty = fields.Float(string="RFQ Qty")

    # =====================
    # VENDOR
    # =====================
    x_studio_vendor_1 = fields.Many2one(
        'res.partner',
        string="Vendor",
        domain=[('supplier_rank', '>', 0)]
    )

    x_studio_product_supplier = fields.Many2one(
        'product.supplierinfo',
        string="Product Supplier"
    )

    # =====================
    # MONETARY
    # =====================
    x_studio_currency_id = fields.Many2one(
        'res.currency',
        string="Currency"
    )

    x_studio_monetary_field_899_1jc10scbf = fields.Monetary(
        string="Amount",
        currency_field='x_studio_currency_id'
    )

    @api.constrains('x_studio_rfq_qty', 'x_studio_qty')
    def _check_rfq_qty(self):
        for rec in self:
            rfq_qty = rec.x_studio_rfq_qty or 0
            qty_on_hand =  rec.x_studio_qty or 0
            if rec.x_studio_rfq_qty > rec.x_studio_qty:
                raise UserError(
                    f"RFQ Quantity ({rfq_qty}) cannot be greater than Qty On Hand ({qty_on_hand}) "
                    f"for product: {rec.x_studio_mr_name.display_name}"
                )

    @api.constrains('x_studio_total_rfq_qty')
    def _check_total_rfq_qty(self):
        for rec in self:
            # Only validate when record already exists (not during create default)
            if rec.id and rec.x_studio_total_rfq_qty == 0.0:
                raise UserError(_(
                    "RFQ Quantity must be greater than 0."
                ))