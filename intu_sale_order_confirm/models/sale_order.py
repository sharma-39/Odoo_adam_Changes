from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_product_created = fields.Boolean(string="Product Created", default=False)


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for record in self:

            # Assign SO sequence only if confirming
            if record.name in ('New', False):
                next_so = self.env['ir.sequence'].next_by_code('sale.order.custom')
                record.name = next_so

            # Get Category
            category = self.env["product.category"].search(
                [("name", "=", "Sale Order")], limit=1
            )

            if not category:
                category = self.env["product.category"].create({
                    "name": "Sale Order"
                })

            # Check if product already exists
            existing_product = self.env["product.product"].search(
                ["|", ("default_code", "=", record.name),
                 ("name", "=", record.name)],
                limit=1
            )

            if not existing_product:
                self.env["product.product"].create({
                    "name": record.name,
                    "type": "consu",
                    "list_price": 0,
                    "sale_ok": False,
                    "purchase_ok": False,
                    "categ_id": category.id,
                })

                record.x_product_created = True
            record.x_confirm_enable= False
            # Search existing report for this Sale Order
            sales_report = self.env['x_sales_report'].search([
                ('x_studio_sales_order', '=', record.id)
            ], limit=1)

            values = {
                'x_name': record.name,
                'x_studio_quote_no': record.x_order_reference_number,
                'x_studio_sales_order': record.id,
                'x_studio_customer_id': record.partner_id.id,
                'x_studio_project_value': record.amount_total,
            }

            if sales_report:
                # Update existing record
                sales_report.write(values)
            else:
                # Create new record
                self.env['x_sales_report'].create(values)

        return res
