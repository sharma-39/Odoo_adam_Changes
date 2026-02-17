from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ---------------------------
# Sale Order Line Add-ons
# ---------------------------

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_product_labour_cost = fields.Float(
        string="Labour Cost",
        help="Labour cost associated with the product"
    )
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_unit_cost_material = fields.Float(
        string="UCM",
        compute="_compute_unit_cost_material",
        store=True,  # no comma after this if adding readonly
        readonly=False,  # optional, default is False
    )

    x_unit_labour_cost = fields.Float(
        string="ULC",
        compute="_compute_unit_labour_cost",
        store=True,
        readonly=False,  # optional
    )

    x_studio_material_cost = fields.Float(
        string="AMC",
        compute="_compute_material_cost",
        store=True
    )
    x_studio_labour_cost = fields.Float(
        string="ALC",
        compute="_compute_labour_cost",
        store=True
    )
    x_studio_total_cost = fields.Float(
        string="Total Cost",
        compute="_compute_total_cost",
        store=True
    )

    @api.depends('product_template_id', 'product_uom_qty')
    def _compute_unit_cost_material(self):
        for line in self:
            line.x_unit_cost_material = line.product_template_id.standard_price or 0.0

    @api.depends('product_template_id')
    def _compute_unit_labour_cost(self):
        for line in self:
            line.x_unit_labour_cost = line.product_template_id.x_studio_product_labour_cost or 0.0

    @api.depends('product_uom_qty', 'x_unit_cost_material', 'x_unit_labour_cost')
    def _compute_material_cost(self):
        for line in self:
            line.x_studio_material_cost = line.product_uom_qty * line.x_unit_cost_material if line.product_uom_qty else 0.0

    @api.depends('product_uom_qty', 'x_unit_labour_cost', 'x_unit_cost_material')
    def _compute_labour_cost(self):
        for line in self:
            line.x_studio_labour_cost = line.product_uom_qty * line.x_unit_labour_cost if line.product_uom_qty else 0.0

    @api.depends('x_studio_material_cost', 'x_studio_labour_cost')
    def _compute_total_cost(self):
        for line in self:
            line.x_studio_total_cost = (line.x_studio_material_cost or 0.0) + (line.x_studio_labour_cost or 0.0)


# ---------------------------
# Sale Order Add-ons
# ---------------------------
class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_alc_total = fields.Float(
        string="Total ALC",
        compute="_compute_total_alc",
        store=True
    )
    x_amc_total = fields.Float(
        string="Total AMC",
        compute="_compute_total_amc",
        store=True
    )
    x_studio_amc_alc_total = fields.Float(
        string="Actual Total Cost (ALC & AMC)",
        compute="_compute_actual_total",
        store=True
    )
    x_studio_amc_percentage = fields.Integer(
        string="Set Purchase Budget Ratio (%)"
    )
    x_studio_set_purchase_budget_valueamt = fields.Float(
        string="Set Purchase Budget Value(Amt)",
        default=0.0
    )
    x_studio_amc_percentage_total = fields.Float(
        string="Project Material Budget Share",
        compute="_compute_amc_percentage_total",
        store=True
    )

    @api.depends('order_line.x_studio_labour_cost')
    def _compute_total_alc(self):
        for order in self:
            order.x_alc_total = sum(line.x_studio_labour_cost or 0.0 for line in order.order_line)

    @api.depends('order_line.x_studio_material_cost')
    def _compute_total_amc(self):
        for order in self:
            order.x_amc_total = sum(line.x_studio_material_cost or 0.0 for line in order.order_line)

    @api.depends('order_line.x_studio_labour_cost', 'order_line.x_studio_material_cost')
    def _compute_actual_total(self):
        for order in self:
            order.x_studio_amc_alc_total = sum(
                (line.x_studio_labour_cost or 0.0) + (line.x_studio_material_cost or 0.0)
                for line in order.order_line
            )

    @api.depends('x_studio_amc_percentage', 'x_amc_total', 'x_studio_set_purchase_budget_valueamt')
    def _compute_amc_percentage_total(self):
        for order in self:
            if 0 <= (order.x_studio_amc_percentage or 0) <= 100:
                order.x_studio_amc_percentage_total = (
                    (order.x_studio_set_purchase_budget_valueamt or 0.0) +
                    ((order.x_amc_total or 0.0) * (order.x_studio_amc_percentage or 0) / 100)
                )
            else:
                order.x_studio_amc_percentage = 0
                order.x_studio_amc_percentage_total = 0.0

    @api.constrains('x_studio_amc_percentage')
    def _check_amc_percentage(self):
        for order in self:
            if order.x_studio_amc_percentage > 100:
                raise ValidationError("AMC Percentage cannot be greater than 100%")
