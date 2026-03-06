from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    x_create_mr_flag = fields.Boolean(
        string="MR Created",
        compute="_compute_mr_flag",
        copy=True
    )

    @api.depends('bom_line_ids.product_qty', 'bom_line_ids.x_studio_mr_qty')
    def _compute_mr_flag(self):

        for rec in self:
            total_qty = sum(rec.bom_line_ids.mapped('product_qty'))
            total_mr_qty = sum(rec.bom_line_ids.mapped('x_studio_mr_qty'))

            rec.x_create_mr_flag = total_qty == total_mr_qty


    def action_create_mr_bom(self):

        for rec in self:

            total_qty = sum(rec.bom_line_ids.mapped('product_qty'))
            total_mr_qty = sum(rec.bom_line_ids.mapped('x_studio_mr_qty'))

            if total_qty == total_mr_qty:
                rec.x_create_mr_flag = True



    def action_create_mr_bom(self):
        self.ensure_one()  # make sure only one BOM is used

        lines = []
        bom = self

        for bom_line in bom.bom_line_ids:
            remaining_qty = bom_line.product_qty - (bom_line.x_studio_mr_qty or 0)

            # Skip fully consumed lines
            if remaining_qty <= 0:
                continue

            lines.append((0, 0, {
                'x_studio_product': bom_line.product_id.display_name,
                'x_studio_component': bom_line.product_id.id,
                'x_studio_qty': remaining_qty,
                'x_studio_old_qty': bom_line.product_qty,
                'x_studio_many2one_field_4a2_1j8lb2oqp': bom_line.product_id.id,
                'x_studio_remarks': bom_line.x_studio_remarks,
                'x_studio_unit': bom_line.product_uom_id.id,
            }))
        if not lines:
            raise UserError(
                "⚠️ Material requests have been generated for all BOM lines; "
                "no additional quantities are required beyond the BOM demand."
            )

        # 🔍 Find related Sale Order
        sale_order = self.env['sale.order'].search([
            ('name', 'ilike', bom.product_tmpl_id.display_name)
        ], limit=1)

        # 🔍 Find related Project
        project = self.env['project.project'].search([
            ('name', 'ilike', bom.product_tmpl_id.display_name)
        ], limit=1)

        return {
            'name': 'Create Material Request',
            'type': 'ir.actions.act_window',
            'res_model': 'x.wizard.form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_x_name': bom.product_tmpl_id.display_name,
                'default_x_studio_bom_id': bom.product_tmpl_id.id,  # ✅ usually better to pass bom.id
                'default_x_studio_reference': bom.code,
                'default_x_wizard_sales_order_no': sale_order.id if sale_order else False,
                'default_x_wizard_product_id': bom.product_tmpl_id.id,
                'default_x_studio_projects': project.id if project else False,
                'default_x_wizard_form_line_ids': lines,
            },
        }