from odoo import models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()

        for record in self:
            record.write({
                'x_approved': False,
                'x_approved_widget_enable': False,
                'x_confirm_enable': False,
                'x_studio_approved_status': 'Not Approved'
            })

        return res
