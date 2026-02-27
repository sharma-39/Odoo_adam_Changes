from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_studio_bom_request = fields.Boolean(string="BOM Request")
    x_studio_mr_request_number = fields.Char(string="MR Number", readonly=True)

    x_studio_po_mr_number = fields.Char(
        string="PO MR Number",
        compute="_compute_po_details",
        copy=True
    )

    x_studio_po_number = fields.Char(
        string="PO Number",
        compute="_compute_po_details",
        copy=True
    )




    @api.depends('origin')
    def _compute_po_details(self):
        for record in self:
            record.x_studio_po_mr_number = False
            record.x_studio_po_number = False

            if not record.origin:
                continue

            purchase_order = record.env['purchase.order'].search([
                ('name', '=', record.origin),
                ('state', '!=', 'cancel')
            ], limit=1)

            if purchase_order:
                record.x_studio_po_mr_number = purchase_order.x_studio_mr_number or ''
                record.x_studio_po_number = purchase_order.name or ''


    # Prevent duplicate execution
    x_logic_processed = fields.Boolean(default=False)

    def button_validate(self):
        res = super().button_validate()

        for record in self:

            # =====================================================
            # LOGIC 1
            # =====================================================
            done_moves = record.move_ids.filtered(
                lambda m: m.state == "done"
                          and m.quantity > 0
                          and m.picking_id.picking_type_id.code == "incoming"
            )

            total_price = sum(
                (
                        m.product_id.standard_price
                        + (
                                m.product_id.standard_price
                                * m.product_id.supplier_taxes_id.amount
                                / 100
                        )
                )
                * m.quantity
                for m in done_moves
            )

            if record.project_id:
                current_price = (
                        record.project_id.x_studio_receipt_received or 0.0
                )
                record.project_id.write(
                    {
                        "x_studio_receipt_received":
                            current_price + total_price
                    }
                )

            # =====================================================
            # LOGIC 2
            # =====================================================
            done_moves = record.move_ids.filtered(
                lambda m: m.state == "done"
                          and m.quantity > 0
                          and m.picking_id.picking_type_id.code == "outgoing"
            )

            if done_moves:

                total_delivered_price = sum(
                    (
                            m.product_id.standard_price
                            + (
                                    m.product_id.standard_price
                                    * (
                                            m.product_id.supplier_taxes_id.amount
                                            / 100
                                    )
                            )
                    )
                    * m.quantity
                    for m in done_moves
                )

                if record.project_id:
                    current_price = (
                            record.project_id.x_studio_delivery_price or 0.0
                    )
                    record.project_id.write(
                        {
                            "x_studio_delivery_price":
                                current_price
                                + total_delivered_price
                        }
                    )

                delivered_qty_dict = {}
                for move in done_moves:
                    pid = move.product_id.id
                    delivered_qty_dict[pid] = (
                            delivered_qty_dict.get(pid, 0.0)
                            + move.quantity
                    )

                purchase_orders = self.env["purchase.order"].search(
                    [
                        (
                            "project_id",
                            "=",
                            record.project_id.id
                            if record.project_id
                            else False,
                        ),
                        ("state", "=", "purchase"),
                    ]
                )

                received_qty_dict = {}

                for po in purchase_orders:
                    receipts = po.picking_ids.filtered(
                        lambda p: p.picking_type_code
                                  == "incoming"
                    )

                    for receipt in receipts:
                        for move in receipt.move_ids:
                            pid = move.product_id.id

                            received_qty_dict[pid] = (
                                    received_qty_dict.get(pid, 0.0)
                                    + move.product_uom_qty
                            )

                remaining_dict = {}

                for pid, received_qty in received_qty_dict.items():
                    delivered_qty = delivered_qty_dict.get(pid, 0.0)
                    remaining_qty = received_qty - delivered_qty
                    remaining_dict[pid] = remaining_qty

                total_remaining_price = 0.0

                for pid, remaining_qty in remaining_dict.items():

                    if remaining_qty <= 0:
                        continue

                    product = self.env["product.product"].browse(pid)

                    price_with_tax = (
                            product.standard_price
                            + (
                                    product.standard_price
                                    * product.supplier_taxes_id.amount
                                    / 100
                            )
                    )

                    total_remaining_price += (
                            price_with_tax * remaining_qty
                    )

                consentform = self.env["x_custom_form"].search(
                    [
                        (
                            "x_studio_mr_number",
                            "=",
                            record.x_studio_mr_request_number,
                        )
                    ],
                    limit=1,
                )

                if consentform:
                    status = "delivered"

                    for line in (
                            consentform.x_custom_form_line_ids
                    ):
                        pid = line.x_studio_product.id
                        delivered_qty = delivered_qty_dict.get(
                            pid, 0.0
                        )

                        line.write(
                            {
                                "x_studio_received_qty":
                                    (
                                            line.x_studio_received_qty
                                            or 0.0
                                    )
                                    + delivered_qty
                            }
                        )

                        if (
                                line.x_studio_received_qty
                                != line.x_studio_qty
                        ):
                            status = "partially_delivered"

                    consentform.write(
                        {
                            "x_studio_selection_field_5i4_1j9oojl26":
                                status
                        }
                    )

            # =====================================================
            # LOGIC 3
            # =====================================================
            incoming_moves = record.move_ids.filtered(
                lambda m: m.state == "done"
                          and m.picking_id.picking_type_id.code
                          == "incoming"
            )

            if record.project_id:

                sale_orders = self.env["sale.order"].search(
                    [
                        (
                            "project_id",
                            "=",
                            record.project_id.id,
                        )
                    ]
                )

                delivery_orders = self.env["stock.picking"].search(
                    [
                        ("sale_id", "in", sale_orders.ids),
                        ("picking_type_code", "=", "outgoing"),
                        ("state", "!=", "done"),
                    ]
                )

                for picking in delivery_orders:
                    for move in picking.move_ids:
                        product = move.product_id

                        matching_incoming = (
                            incoming_moves.filtered(
                                lambda m:
                                m.product_id.id
                                == product.id
                            )
                        )

                        if matching_incoming:
                            incoming_qty = (
                                matching_incoming[0].quantity
                            )
                            move.update(
                                {
                                    "x_studio_received_qty":
                                        (
                                                move.x_studio_received_qty
                                                or 0.0
                                        )
                                        + incoming_qty
                                }
                            )
                        else:
                            move.update(
                                {
                                    "x_studio_received_qty":
                                        (
                                                move.x_studio_received_qty
                                                or 0.0
                                        )
                                }
                            )

            # =====================================================
            # LOGIC 4
            # =====================================================
            if (
                    record.picking_type_id
                    and record.picking_type_id.code
                    == "incoming"
                    and record.origin
            ):

                received_data = {}

                for move in record.move_ids:
                    if move.product_id:
                        received_data[
                            move.product_id.id
                        ] = (
                                received_data.get(
                                    move.product_id.id, 0.0
                                )
                                + move.quantity
                        )

                purchase_order = self.env[
                    "purchase.order"
                ].search(
                    [
                        ("name", "=", record.origin),
                        ("state", "!=", "cancel"),
                    ],
                    limit=1,
                )

                if purchase_order:

                    mr_number = (
                        purchase_order.x_studio_mr_number
                    )

                    custom_form = self.env[
                        "x_custom_form"
                    ].search(
                        [
                            (
                                "x_studio_mr_number",
                                "=",
                                mr_number,
                            )
                        ],
                        limit=1,
                    )

                    if custom_form:
                        for line in (
                                custom_form
                                        .x_custom_form_line_ids
                        ):
                            product = line.x_studio_product

                            if (
                                    product
                                    and product.id
                                    in received_data
                            ):
                                line.write(
                                    {
                                        "x_studio_received_po_qty":
                                            line.x_studio_received_po_qty
                                            + received_data[
                                                product.id
                                            ]
                                    }
                                )

                                if line.x_studio_waiting_po_qty:
                                    line.write(
                                        {
                                            "x_studio_waiting_po_qty":
                                                line.x_studio_waiting_po_qty
                                                - received_data[
                                                    product.id
                                                ]
                                        }
                                    )

            # =====================================================
            # LOGIC 5
            # =====================================================
            if (
                    record.picking_type_id
                    and record.picking_type_id.code
                    == "outgoing"
                    and record.x_studio_mr_request_number
            ):

                delivered_data = {}

                for move in record.move_ids:
                    if move.product_id:
                        delivered_data[
                            move.product_id.id
                        ] = (
                                delivered_data.get(
                                    move.product_id.id, 0.0
                                )
                                + move.product_uom_qty
                        )

                mr_number = (
                    record.x_studio_mr_request_number
                )

                purchase_order = self.env[
                    "purchase.order"
                ].search(
                    [
                        (
                            "x_studio_mr_number",
                            "=",
                            mr_number,
                        ),
                        ("state", "!=", "cancel"),
                    ],
                    limit=1,
                )

                if purchase_order:

                    incoming_picking = self.env[
                        "stock.picking"
                    ].search(
                        [
                            (
                                "origin",
                                "=",
                                purchase_order.name,
                            ),
                            (
                                "picking_type_id.code",
                                "=",
                                "incoming",
                            ),
                            ("state", "=", "done"),
                        ],
                        limit=1,
                    )

                    received_data = {}

                    if incoming_picking:
                        for move in incoming_picking.move_ids:
                            if move.product_id:
                                received_data[
                                    move.product_id.id
                                ] = (
                                        received_data.get(
                                            move.product_id.id,
                                            0.0,
                                        )
                                        + move.quantity
                                )

                    custom_form = self.env[
                        "x_custom_form"
                    ].search(
                        [
                            (
                                "x_studio_mr_number",
                                "=",
                                mr_number,
                            )
                        ],
                        limit=1,
                    )

                    if custom_form:
                        for line in (
                                custom_form
                                        .x_custom_form_line_ids
                        ):
                            product = line.x_studio_product
                            if not product:
                                continue

                            delivered_qty = (
                                delivered_data.get(
                                    product.id, 0.0
                                )
                            )

                            if line.x_studio_received_po_qty:
                                line.write(
                                    {
                                        "x_studio_received_po_qty":
                                            line.x_studio_received_po_qty
                                            - delivered_qty
                                    }
                                )

            # =====================================================
            # LOGIC 6
            # =====================================================
            if (
                    record.picking_type_id
                    and record.picking_type_id.code
                    == "incoming"
                    and record.origin
            ):

                purchase_order = self.env[
                    "purchase.order"
                ].search(
                    [
                        ("name", "=", record.origin),
                        ("state", "!=", "cancel"),
                    ],
                    limit=1,
                )

                if purchase_order:
                    mr_number = (
                        purchase_order.x_studio_mr_number
                    )

                    record.write(
                        {
                            "x_studio_mr_request_number":
                                mr_number or ""
                        }
                    )

        return res


    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.project_id and record.project_id.reinvoiced_sale_order_id:
            record.sale_id = record.project_id.reinvoiced_sale_order_id.id
        return record