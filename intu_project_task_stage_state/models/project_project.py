from odoo import models

class ProjectProject(models.Model):
    _inherit = "project.project"

    def write(self, vals):
        res = super().write(vals)

        # Use sudo() to bypass field-level access restrictions
        for record in self.sudo():

            # -----------------------------
            # 1️⃣ Update Product Status
            # -----------------------------
            if record.name:
                parts = record.name.split('-')
                product_name = parts[0].strip()

                product = self.env['product.template'].search([
                    ('name', '=', product_name)
                ], limit=1)

                if product:
                    # Accessing record.stage_id now works because of .sudo()
                    is_done = record.stage_id.name == "Done"

                    product.write({
                        "x_studio_is_project_done": is_done
                    })

            # -----------------------------
            # 2️⃣ Update Project Manager to Tasks
            # -----------------------------
            # We use sudo() on the search/write as well to ensure total coverage
            tasks = self.env['project.task'].sudo().search([
                ('project_id', '=', record.id)
            ])
            if record.stage_id.name == 'Done':
                tasks.write({'tasks.state.id' : '1_done'})


            manager = record.x_studio_project_manager

            if manager:
                tasks.write({
                    'x_studio_project_manager': manager.id,

                })

        return res