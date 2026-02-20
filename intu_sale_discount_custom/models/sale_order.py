from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Line Item Discount (Float)
    x_studio_line_item_discount = fields.Float(
        string="Line Item Discount",
        compute="_compute_line_item_discount",
        copy=True
    )

    # Total Discount (Float)
    x_studio_total_discount = fields.Float(
        string="Total Discount",
        compute="_compute_total_discount",
        copy=True
    )

    @api.depends(
        'order_line.product_template_id',
        'order_line.price_subtotal'
    )
    def _compute_line_item_discount(self):
        for record in self:
            discount_price_sum = sum(
                line.price_subtotal
                for line in record.order_line
                if line.product_template_id
                and line.product_template_id.name == "Discount"
            )
            record.x_studio_line_item_discount = abs(discount_price_sum)

    @api.depends(
        'amount_undiscounted',
        'amount_untaxed',
        'x_studio_line_item_discount'
    )
    def _compute_total_discount(self):
        for record in self:

            amount_undiscounted = record.amount_undiscounted or 0.0
            untaxed_amount = record.amount_untaxed or 0.0
            line_discount = abs(record.x_studio_line_item_discount or 0.0)

            record.x_studio_total_discount = abs(
                abs(amount_undiscounted - line_discount) - untaxed_amount
            )