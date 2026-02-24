from odoo import models, fields

class StockPicking(models.Model):
    _inherit = "stock.picking"

    x_studio_bom_request = fields.Boolean(
        string="BOM Request"
    )

    x_studio_mr_request_number = fields.Char(
        string="MR Number"
    )

    x_studio_po_mr_number = fields.Char(
        string="PO MR Number"
    )

    x_studio_po_number = fields.Char(
        string="PO Number"
    )