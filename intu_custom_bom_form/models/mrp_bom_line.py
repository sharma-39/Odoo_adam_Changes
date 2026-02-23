from odoo import models, api, _
from odoo.exceptions import UserError

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.onchange('product_id')
    def _onchange_product_id_check_duplicate(self):
        if not self.product_id or not self.bom_id:
            return

        # Count how many times this product appears in the current UI lines
        # We use '._origin' to handle comparison between NewId and real IDs
        count = 0
        for line in self.bom_id.bom_line_ids:
            if line.product_id == self.product_id:
                count += 1

        if count > 1:
            # Clear the field so the user is forced to pick a different one
            product_name = self.product_id.display_name
            self.product_id = False

            return {
                'warning': {
                    'title': _('Duplicate Product'),
                    'message': _(
                        'The product "%s" is already in this BOM. Duplicate lines are not allowed.') % product_name,
                }
            }