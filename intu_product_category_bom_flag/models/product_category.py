from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = "product.category"

    x_studio_bom_list = fields.Boolean(
        string="BOM List",
        help="Enable this if the category is related to BOM."
    )