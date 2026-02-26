from odoo import models, fields

class PoCategory(models.Model):
    _name = 'x_po_category'
    _description = 'Po Tags'
    _rec_name = 'x_name'
    _order = 'x_studio_sequence asc, id asc'

    x_name = fields.Char(
        string="Tag",
        required=True
    )

    x_studio_sequence = fields.Integer(
        string="Sequence",
        default=10
    )