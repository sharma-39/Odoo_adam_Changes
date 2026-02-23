from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_studio_is_project_done = fields.Boolean(
        string="Project Done",
        compute="_compute_project_done",
        copy=True,
        store=True
    )

    x_studio_is_create_job_order = fields.Boolean(
        string="Create Job Order",
        compute="_compute_job_order",
        copy=True,
        store=True
    )

    # ---------------------------------------------------------
    # 1️⃣ Compute Project Done
    # ---------------------------------------------------------

    @api.depends('name')
    def _compute_project_done(self):
        Project = self.env['project.project']

        for product in self:
            product.x_studio_is_project_done = False

            if product.name:
                project = Project.search(
                    [('name', 'ilike', product.name)],
                    limit=1
                )

                if project and project.stage_id and \
                        'done' in project.stage_id.name.lower():
                    product.x_studio_is_project_done = True

    # ---------------------------------------------------------
    # 2️⃣ Compute BOM
    # ---------------------------------------------------------

    @api.depends('name')
    def _compute_job_order(self):
        Bom = self.env['mrp.bom']

        for product in self:
            product.x_studio_is_create_job_order = False

            if product.name:
                bom = Bom.search(
                    [('product_tmpl_id.name', 'ilike', product.name)],
                    limit=1
                )

                product.x_studio_is_create_job_order = bool(bom)
