from odoo import models, fields

class Project(models.Model):
    _inherit = 'project.project'

    x_studio_total_sales_budget = fields.Float(string="Budget (Allocated)")
    x_studio_purchase_budget = fields.Float(string="PO Purchased Amount")

    x_studio_po_remaining_budget = fields.Float(string="PO Remaining Budget")

    x_studio_delivery_price = fields.Float(string="Delivery Price")
    x_studio_receipt_received = fields.Float(string="Receipt Received")

    x_studio_delivery_purchase_price = fields.Float(string="Stocked Materials Value")


    x_studio_remaining_budget = fields.Integer(string="Remaining Budget")


    x_studio_material_budget = fields.Float(string="Remaining Material Budget")

    x_studio_progress_percentage = fields.Float(string="Progress Percentage")
    x_studio_project_cpercentage = fields.Float(string="Progress")

    x_studio_project_invoice_status = fields.Integer(string="Project Invoice Status")
    x_studio_project_manager = fields.Many2one('hr.employee', string="Project Manager")
    x_studio_project_percentage = fields.Float(string="Project Percentage")



