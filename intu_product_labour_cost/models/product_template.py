from odoo import models, fields, api

# ---------------------------
# Sale Order Line Add-ons
# ---------------------------

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_product_labour_cost = fields.Float(
        string="Labour Cost",
        help="Labour cost associated with the product"
    )
    