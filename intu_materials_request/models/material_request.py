from odoo import models, fields, api,_
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _name = "x_custom_form"
    _description = "Material Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "display_name"

    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)

    x_studio_mr_number = fields.Char(string="MR Number",readonly=True)
    x_name = fields.Char(string="Name")

    x_studio_sale_order_number = fields.Many2one(
        'sale.order',
        string="Job Order",
        readonly=True
    )

    x_studio_project = fields.Many2one(
        'project.project',
        string="Project",
        readonly=True
    )

    x_studio_delivery_update = fields.Boolean(string="Delivery Update")

    x_studio_mr_priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string="Priority", default='1')

    x_studio_rfq_enable = fields.Boolean(string="RFQ Enable")

    x_studio_delivery_count = fields.Integer(
        string="Delivery Count",
        compute="_compute_delivery_count",
        copy=True
    )

    x_studio_mr_date = fields.Datetime(string="MR Date")

    create_uid = fields.Many2one('res.users', string="Requested By", readonly=True)

    x_studio_expected_deadline = fields.Datetime(string="Expected Deadline")

    x_studio_purchase_count = fields.Integer(
        string="RFQ | PO",
        compute="_compute_purchase_count",
        copy=True
    )

    x_studio_delivery_number = fields.Char(string="Delivery Number")

    x_studio_selection_field_5i4_1j9oojl26 = fields.Selection([
        ('requested', 'Requested'),
        ('partially_delivered', 'Partially Delivered'),
        ('delivered', 'Delivered')
    ], string="Status", default='requested', tracking=True)

    x_custom_form_line_ids = fields.One2many(
        'x.custom.form.line',
        'material_request_id',
        string="Material Request Lines"
    )

    @api.depends('x_studio_mr_number')
    def _compute_purchase_count(self):

        for record in self:
            if not record.x_studio_mr_number:
                record.x_studio_purchase_count = 0
                continue

            purchase_count = self.env['purchase.order'].search_count([
                ('x_studio_mr_number', '=', record.x_studio_mr_number)
            ])

            record.x_studio_purchase_count = purchase_count

    @api.depends('x_studio_mr_number')
    def _compute_delivery_count(self):
        for record in self:
            if record.x_studio_mr_number:
                pickings = self.env['stock.picking'].search([
                    ('x_studio_mr_request_number', '=', record.x_studio_mr_number),
                    ('picking_type_code', '=', 'outgoing')
                ])
                record.x_studio_delivery_count = len(pickings)
            else:
                record.x_studio_delivery_count = 0

    @api.depends('x_studio_mr_number', 'x_name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.x_studio_mr_number or ''} - {rec.x_name or ''}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('x_studio_mr_number') or vals.get('x_studio_mr_number') == 'New':
                vals['x_studio_mr_number'] = self.env['ir.sequence'].next_by_code(
                    'material.request.no'
                ) or 'New'

        # ✅ Capture the created records
        records = super(MaterialRequest, self).create(vals_list)

        # ✅ Trigger the delivery creation on the NEW records
        records.action_create_delivery_bom()

        return records

    def action_create_delivery_bom(self):
        for record in self:

            # 🟢 1️⃣ Get or Create the Sale Order
            sale_order = record.x_studio_sale_order_number

            # 🟢 2️⃣ Confirm Sale Order if not confirmed
            if sale_order.state not in ['sale', 'done']:
                sale_order.action_confirm()

            # 🟢 3️⃣ Picking Type & Locations
            picking_type = sale_order.warehouse_id.out_type_id or \
                           record.env['stock.picking.type'].sudo().search([('code', '=', 'outgoing')], limit=1)

            if not picking_type:
                raise UserError("No outgoing picking type found.")

            location_id = sale_order.warehouse_id.lot_stock_id.id if sale_order.warehouse_id else \
                record.env.ref('stock.stock_location_stock').id

            location_dest_id = sale_order.partner_id.property_stock_customer.id

            # 🟢 4️⃣ Create Only ONE Delivery Order (FIXED)
            picking_name = record.env['ir.sequence'].next_by_code('stock.picking.outgoing') or '/'
            picking = record.env['stock.picking'].sudo().create({
                'name': picking_name,
                'partner_id': sale_order.partner_id.id,
                'picking_type_id': picking_type.id,
                'origin': sale_order.name,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
                'sale_id': sale_order.id,
                'project_id': sale_order.project_id.id if sale_order.project_id else False,
                'x_studio_mr_request_number': record.x_studio_mr_number,
            })

            # 🟢 5️⃣ Create Stock Moves for Each Line
            for line in record.x_custom_form_line_ids:
                product = line.x_studio_product
                qty = line.x_studio_qty or 1.0

                if not product:
                    continue

                record.env['stock.move'].sudo().create({
                    'picking_id': picking.id,
                    'product_id': product.id,
                    'product_uom_qty': qty,

                    'product_uom': product.uom_id.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'description_picking': product.display_name or product.name,
                    'origin': sale_order.name,
                })

            # 🟢 6️⃣ Confirm & Assign the Delivery
            picking.action_confirm()
            picking.write({'sale_id': sale_order.id,'project_id': sale_order.project_id.id if sale_order.project_id else False,})
            # picking.action_assign()
            picking.move_ids.sudo().write({'state': 'confirmed'})

            # 🟢 7️⃣ Fix Backorder Sale ID Linking
            if picking.backorder_id:
                picking.backorder_id.sudo().write({'sale_id': sale_order.id})

            # 🟢 8️⃣ Update Form
            record.write({
                'x_studio_delivery_update': True,
                'x_studio_delivery_number': picking.name,
            })

            record.message_post(body=f"Delivery Order {picking.name} was created.")



    def action_create_rfq_bom(self):
        self.ensure_one()

        lines = []

        # -------------------------------------------------
        # Prepare Wizard Lines
        # -------------------------------------------------
        for line in self.x_custom_form_line_ids:

            product = line.x_studio_product

            mr_qty = line.x_studio_qty or 0.0
            delivered_qty = line.x_studio_received_qty or 0.0
            waiting_po_qty = line.x_studio_waiting_po_qty or 0.0
            received_po_qty = line.x_studio_received_po_qty or 0.0

            rfq_qty = max(
                mr_qty - delivered_qty - received_po_qty - waiting_po_qty,
                0.0
            )

            if rfq_qty <= 0:
                continue

            qty_on_hand = product.qty_available if product else 0.0

            vendor_id = False
            if product and product.seller_ids:
                vendor_id = product.seller_ids[0].partner_id.id

            lines.append((0, 0, {
                'x_studio_sequence': line.x_studio_sequence,
                'x_studio_mr_name': product.id if product else False,
                'x_studio_qty': rfq_qty,
                'x_studio_unit': line.x_studio_unit.id if line.x_studio_unit else False,
                'x_studio_qty_on_hand': qty_on_hand,
                'x_studio_rfq_qty': 0.0,
                'x_name': line.x_studio_remarks_1,
                'x_studio_vendor_1': vendor_id,
            }))

        if not lines:
            raise UserError(_(
                    "No pending quantities available.\n"
                    "All required quantities are already delivered "
                    "or covered by existing PO."
            ))
        # -------------------------------------------------
        # Open Wizard WITHOUT create()
        # -------------------------------------------------
        return {
            'name': _('Create RFQ Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'x_mr_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_x_studio_flow': "create",
                'default_x_studio_job_order_no': self.x_studio_sale_order_number.id if self.x_studio_sale_order_number else False,
                'default_x_studio_mr_number': self.x_studio_mr_number,
                'default_x_studio_dr_number': self.x_studio_delivery_number,
                'default_x_studio_project': self.x_studio_project.id if self.x_studio_project else False,
                'default_x_studio_responsibility': self.env.uid,
                'default_x_mr_wizard_line_ids_e1f04': lines,
            }
        }

    def goto_delivery_form(self):
        # 'self' represents the current record(s)
        self.ensure_one()  # Safety check: ensure we are only clicking from one record

        mr_number = self.x_studio_mr_number

        if not mr_number:
            raise UserError("The MR Number is missing. Cannot find related transfers.")

        # Search for the pickings (Transfers)
        pickings = self.env['stock.picking'].search([
            ('x_studio_mr_request_number', '=', mr_number),
            ('picking_type_code', '=', 'outgoing')
        ])

        if not pickings:
            raise UserError(f"No Stock Picking (Transfer) found for MR: {mr_number}")

        # Prepare the window action
        action = {
            'name': 'Delivery Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'target': 'current',
        }

        if len(pickings) == 1:
            # One record: Open the form view directly
            action.update({
                'view_mode': 'list',
                'res_id': pickings.id,
            })
        else:
            # Multiple records: Open the list (tree) view filtered by IDs
            action.update({
                'view_mode': 'list',
                'domain': [('id', 'in', pickings.ids)],
            })

        return action

    def goto_rfq_form(self):
        self.ensure_one()

        mr_number = self.x_studio_mr_number

        if not mr_number:
            raise UserError(_("MR Number is not defined."))

        purchases = self.env['purchase.order'].search([
            ('x_studio_mr_number', '=', mr_number)
        ])

        if not purchases:
            raise UserError(
                _("No Purchase Order found for MR: %s") % mr_number
            )

        # -------------------------------------------------
        # Single PO → Open Form
        # -------------------------------------------------
        if len(purchases) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Purchase Order'),
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': purchases.id,
                'target': 'current',
            }

        # -------------------------------------------------
        # Multiple POs → Open List
        # -------------------------------------------------
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Orders'),
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', purchases.ids)],
            'target': 'current',
        }

# ==============================
# MATERIAL REQUEST LINE
# ==============================

class MaterialRequestLine(models.Model):
    _name = "x.custom.form.line"
    _description = "Material Request Line"
    _order = "x_studio_sequence asc"

    material_request_id = fields.Many2one(
        'x_custom_form',
        string="Material Request",
        ondelete="cascade"
    )

    x_studio_sequence = fields.Integer(string="Sequence")

    x_name = fields.Char(string="Description")

    x_studio_product = fields.Many2one(
        'product.product',
        string="Material Name",
        readonly=True
    )

    x_studio_many2one_field_1md_1j8iqtd9q = fields.Many2one(
        'product.product',
        string="Product",
        readonly=True
    )

    x_studio_unit = fields.Many2one(
        'uom.uom',
        string="Unit"
    )

    x_studio_allowed_uom = fields.Many2many(
        'uom.uom',
        string="Allowed UOM",
        compute="_compute_allowed_uom",
        copy=True
    )

    x_studio_qty = fields.Float(string="MR Qty")
    x_studio_qty_available = fields.Float(string="Qty Available")
    x_studio_received_qty = fields.Float(string="Delivery Qty",readonly=True)

    x_studio_po_rfq_qty = fields.Float(string="PO Qty",readonly=True)
    x_studio_received_po_qty = fields.Float(string="PO Received Qty")
    x_studio_waiting_po_qty = fields.Float(string="Waiting PO Qty")

    x_studio_expected_deadline = fields.Datetime(string="Expected Deadline")

    x_studio_remarks_1 = fields.Char(string="Remarks")

    @api.depends('x_studio_product')
    def _compute_allowed_uom(self):
        for record in self:
            if record.x_studio_product:
                # Use .ids to ensure you're passing a list of integers
                record.x_studio_allowed_uom = record.x_studio_product.uom_ids.ids
            else:
                # Clear the field if no product is selected
                record.x_studio_allowed_uom = [(5, 0, 0)]

