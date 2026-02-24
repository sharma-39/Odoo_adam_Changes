from odoo import models, fields,api
from odoo.exceptions import UserError



class XWizardFormLine(models.Model):
    _name = 'x.wizard.form.line'
    _description = 'Wizard Form Line'

    x_name = fields.Char('Description')
    x_studio_component = fields.Many2one('product.product', 'Component')
    x_studio_expected_deadline = fields.Datetime('Expected Deadline')
    x_studio_many2one_field_2au_1j8lb1nj6 = fields.Many2one('res.partner', 'New Many2One')
    x_studio_many2one_field_4a2_1j8lb2oqp = fields.Many2one('product.product', 'Product Variant')
    x_studio_mr_qty = fields.Float('MR Qty')
    x_studio_old_qty = fields.Float('Old Qty')
    x_studio_product = fields.Char('Product')
    x_studio_qty = fields.Float('Demand')
    x_studio_total_mr_qty = fields.Float('Total MR Qty')
    x_studio_remarks = fields.Char('Remarks')
    x_studio_sequence = fields.Integer('Sequence')
    x_studio_unit = fields.Many2one('uom.uom', 'Unit')
    x_wizard_form_id = fields.Many2one(
        'x.wizard.form',
        'Wizard Form',
        ondelete='cascade'
    )


    @api.constrains('x_studio_qty', 'x_studio_mr_qty')
    def _check_mr_not_greater_than_demand(self):
        for rec in self:
            if rec.x_studio_qty and rec.x_studio_mr_qty:
                if rec.x_studio_mr_qty > rec.x_studio_qty:
                    raise UserError(
                        f"({self.x_studio_product}) "
                        "Entered quantity exceeds the demand quantity. "
                        "Please adjust it accordingly."
                    )

    @api.constrains('x_studio_mr_qty')
    def _check_mr_qty(self):
        for rec in self:
            if rec.x_studio_mr_qty <= 0:
                raise UserError("MR Qty must be greater than 0.")