from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    x_studio_labour_cost = fields.Float(string="Labour Cost")
