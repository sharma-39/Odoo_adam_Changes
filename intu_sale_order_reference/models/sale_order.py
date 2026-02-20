from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_order_reference_number = fields.Char(
        string="Order Reference Number",
        readonly=True,
        copy=False
    )

    @api.model_create_multi
    def create(self, vals_list):
    
        for vals in vals_list:

            # Always force name = 'New'
            vals['name'] = 'New'

            # Generate your custom reference
            if not vals.get('x_order_reference_number'):
                vals['x_order_reference_number'] = self.env[
                    'ir.sequence'
                ].next_by_code('sale.order.normal')

        # Call super BUT skip default sale sequence logic
        self = self.with_context(default_name='New')
        records = super(SaleOrder, self).create(vals_list)

        # Force again after create (safety)
        records.write({'name': 'New'})
        records.write({'x_approved':True})
        return records
