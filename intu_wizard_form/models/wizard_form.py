from odoo import models, fields, api
from odoo.exceptions import UserError
class XWizardForm(models.Model):
    _name = 'x.wizard.form'
    _description = 'Wizard Form'

    x_name = fields.Char('Name',readonly=True)
    x_studio_expected_deadline = fields.Datetime('Expected Deadline')
    x_studio_projects = fields.Many2one('project.project', 'Project')
    x_studio_validator = fields.Boolean('Validator')
    x_wizard_sales_order_no = fields.Many2one('sale.order', 'Sales Order')
    x_studio_total_mr_qty = fields.Float('Total MR Qty', compute='_compute_total_mr_qty', store=True)
    x_studio_bom_id = fields.Many2one('product.template', 'BoM ID')

    x_wizard_form_line_ids = fields.One2many(
        'x.wizard.form.line',
        'x_wizard_form_id',
        'Wizard Form Lines'
    )

    @api.depends('x_wizard_form_line_ids.x_studio_mr_qty')
    def _compute_total_mr_qty(self):
        for rec in self:
            rec.x_studio_total_mr_qty = sum(line.x_studio_mr_qty for line in rec.x_wizard_form_line_ids)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # ✅ Step 2: Get BoM
        product_tmpl_id = record.x_studio_bom_id.id
        bom = self.env['mrp.bom'].sudo().search([
            ('product_tmpl_id', '=', product_tmpl_id)
        ], limit=1)

        if not bom:
            raise UserError(
                f"No BoM found for Product Template: {record.x_studio_bom_id.display_name}"
            )

        # ✅ Step 3: Update BoM Lines
        for line in record.x_wizard_form_line_ids:
            product_id = line.x_studio_many2one_field_4a2_1j8lb2oqp.id
            new_qty = line.x_studio_mr_qty or 0

            bom_lines = bom.bom_line_ids.filtered(
                lambda bl: bl.product_id.id == product_id
            )

            if bom_lines:
                for bl in bom_lines:
                    updated_qty = (bl.x_studio_mr_qty or 0) + new_qty
                    bl.sudo().write({'x_studio_mr_qty': updated_qty})
            else:
                self.env['mrp.bom.line'].sudo().create({
                    'bom_id': bom.id,
                    'product_id': product_id,
                    'x_studio_mr_qty': new_qty,
                })

        # ✅ Step 4: Build Custom Lines
        lines = []
        for wiz_line in record.x_wizard_form_line_ids:
            if wiz_line.x_studio_mr_qty:
                lines.append((0, 0, {
                    'x_studio_sequence': wiz_line.x_studio_sequence,
                    'x_studio_product': wiz_line.x_studio_many2one_field_4a2_1j8lb2oqp.id,
                    'x_studio_qty': wiz_line.x_studio_mr_qty,
                    'x_studio_expected_deadline': wiz_line.x_studio_expected_deadline
                                                  or record.x_studio_expected_deadline,
                    'x_studio_unit': wiz_line.x_studio_unit.id if wiz_line.x_studio_unit else False,
                    'x_studio_remarks_1':wiz_line.x_studio_remarks,
                }))
        if not lines:
            raise UserError(
                "No pending quantities available.\n"
                "All required quantities are already delivered or covered by existing PO."
            )

        # ✅ Step 5: Create Custom Form
        if lines:
            self.env['x_custom_form'].sudo().create({
                'x_name': record.x_studio_bom_id.display_name,
                'x_studio_mr_date': record.create_date,
                'x_studio_sale_order_number': record.x_wizard_sales_order_no.id,
                'x_studio_project': record.x_studio_projects.id,
                'x_studio_expected_deadline': record.x_studio_expected_deadline,
                'x_custom_form_line_ids': lines,
            })

        return record