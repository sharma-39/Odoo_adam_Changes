from odoo import models,api,_,fields
from odoo.exceptions import UserError

class MrpBom(models.Model):
    _inherit = "mrp.bom"
    x_studio_approve_enable = fields.Boolean(
        string="Approved",
        default=False,
        readonly=True
    )
    x_status_bar = fields.Selection(
        [('draft', 'Not Approved'), ('approve', 'Approved')],
        string='Status',
        default='draft'
    )

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id_set_project(self):
        if self.product_tmpl_id:
            project = self.env['project.project'].search(
                [('name', 'ilike', self.product_tmpl_id.name)],
                limit=1
            )
            self.project_id = project.id if project else False

            if not project:
                return {
                    'warning': {
                        'title': _('Project Not Found'),
                        'message': _('No project matches "%s".') % self.product_tmpl_id.name,
                    }
                }
        else:
            self.project_id = False

    @api.model
    def create(self, vals):
        # 1. Create the BoM first to get the record data
        bom = super(MrpBom, self).create(vals)

        # 2. Get the name from the template linked to the BoM
        # We use .name to get the actual text string
        search_term = bom.product_tmpl_id.name

        if search_term:
            # 3. Search for any product where the template name CONTAINS the search_term
            # 'ilike' is the standard Odoo operator for case-insensitive fuzzy matching
            products = self.env['product.product'].search([
                ('product_tmpl_id.name', 'ilike', search_term)
            ])

            # 4. Update the custom Studio field on all found variants
            if products:
                products.write({'x_studio_is_create_job_order': True})

        return bom


    def action_approve_bom(self):
        for record in self:
            if len(record.bom_line_ids) != 0:
                # Update status bar field
                record.write({'x_status_bar': 'approve'})
                # Enable approve flag
                record.write({'x_studio_approve_enable': True})
                # Post message in chatter
                body_log = f"BOM Product '{record.product_tmpl_id.name}' Approved"
                record.message_post(body=body_log)
            else:
                raise UserError(_("No BOM lines found. Please add lines."))

    def action_revise_bom(self):
        for record in self:
            if len(record.bom_line_ids) != 0:
                # Update status bar field
                record.write({'x_status_bar': 'draft'})
                # Enable approve flag
                record.write({'x_studio_approve_enable': False})
                # Post message in chatter
                body_log = f"BOM Product '{record.product_tmpl_id.name}' Revised"
                record.message_post(body=body_log)
            else:
                raise UserError(_("No BOM lines found. Please add lines."))

    def action_create_mr_bom(self):
        for record in self:
            if len(record.bom_line_ids) != 0:
                return
