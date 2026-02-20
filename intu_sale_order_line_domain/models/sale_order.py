from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # This field determines if adding lines is allowed
    can_add_line = fields.Boolean(compute="_compute_can_add_line")

    def _compute_can_add_line(self):
        for record in self:
            # Your custom logic here
            if record.state == 'draft' and record.partner_id:
                record.can_add_line = True
            else:
                record.can_add_line = False