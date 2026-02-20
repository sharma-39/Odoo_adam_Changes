from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_draft(self):
        """
        Triggered when clicking 'Set to Quotation'
        """
        res = super().action_draft()

        # Update custom field
        self.write({
            'x_approved': True
        })

        return res