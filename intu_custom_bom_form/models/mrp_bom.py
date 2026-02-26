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
    x_studio_mr_count = fields.Integer(
        string="MR Count",
        compute="_compute_mr_count"
    )

    def goto_mr(self):
        self.ensure_one()  # Ensures the button click only processes one record

        # Use self instead of record
        product_template = self.product_tmpl_id

        if not product_template:
            raise UserError("Product Template is not set.")

        # Search x_custom_form records
        custom_forms = self.env['x_custom_form'].search([
            ('x_studio_sale_order_number', '=', product_template.name)
        ])

        if not custom_forms:
            raise UserError(f"No Custom Form found for: {product_template.name}")

        # Define the base action
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Custom Forms',
            'res_model': 'x_custom_form',
            'target': 'current',
        }

        # Open form view if only one record exists, otherwise show the list
        if len(custom_forms) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': custom_forms.id,
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', custom_forms.ids)],
            })

        return action  # Crucial: Odoo needs the 'return' to trigger the UI change




    @api.depends('product_tmpl_id')
    def _compute_mr_count(self):
        for record in self:
            # 1. Check if product_tmpl_id exists to avoid errors
            if record.product_tmpl_id:
                # 2. Search for custom forms matching the name
                custom_forms_count = self.env['x_custom_form'].search_count([
                    ('x_studio_sale_order_number', '=', record.product_tmpl_id.name)
                ])
                record.x_studio_mr_count = custom_forms_count
            else:
                record.x_studio_mr_count = 0


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

