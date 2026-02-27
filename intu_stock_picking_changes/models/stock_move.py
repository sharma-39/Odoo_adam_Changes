from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    x_studio_received_qty = fields.Float(
        string="Received Quantity"
    )

