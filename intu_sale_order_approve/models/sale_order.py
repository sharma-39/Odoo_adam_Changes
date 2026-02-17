from odoo import models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_approve_order(self):
        for record in self:
            if record.order_line:  # at least one order line
                if record.x_studio_amc_percentage_total > 0:
                    record.write({
                        'x_approved': False,
                        'x_approved_widget_enable': True,
                        'x_confirm_enable': True,
                        'x_studio_approved_status': 'Approved'
                    })
                else:
                    raise UserError("Budget not specified. Kindly update the budget details to continue.")
            else:
                raise UserError("Line items must be added before proceeding.")
