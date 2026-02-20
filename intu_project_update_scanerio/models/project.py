from odoo import models, api
from odoo.exceptions import UserError
class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        records = super().create(vals)

        for record in records:
            sale_order = record.sale_line_id.order_id
            if not sale_order:
                continue

            # Extract SO Code
            name = sale_order.name or ''

            subject = sale_order.x_studio_subject or ''

            record.update({
                'name': f"{name} - {subject}",
                'x_studio_material_budget': sale_order.x_studio_amc_percentage_total or 0.0,
                'x_studio_remaining_budget': sale_order.x_studio_amc_percentage_total or 0.0,
                'x_studio_total_sales_budget': sale_order.x_studio_amc_percentage_total or 0.0,
            })

        return records