
from odoo import models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.depends('x_studio_purchase_budget', 'x_studio_delivery_price')
    def _compute_delivery_purchase_price(self):
        for record in self:
            delivery = record.x_studio_delivery_price or 0.0
            budget = record.x_studio_purchase_budget or 0.0

            record.x_studio_delivery_purchase_price = (
                delivery - budget if delivery > 0 else 0.0
            )

    @api.depends(
        'x_studio_total_sales_budget',
        'x_studio_purchase_budget',
        'x_studio_delivery_purchase_price'
    )
    def _compute_remaining_budget(self):
        for record in self:
            total_budget = record.x_studio_total_sales_budget or 0.0
            purchase_amt = record.x_studio_purchase_budget or 0.0
            delivery_diff = record.x_studio_delivery_purchase_price or 0.0

            record.x_studio_po_remaining_budget = (
                total_budget - purchase_amt - delivery_diff
            )