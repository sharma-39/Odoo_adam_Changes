from odoo import models, fields,api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_sales_order_invoice_status = fields.Selection([
        ('Not Received', 'Not Received'),
        ('Partially Received', 'Partially Received'),
        ('Fully Received', 'Fully Received'),
    ], string="Invoice Payment Status",
        compute="_compute_invoice_payment_status",
        copy=True)

    # Below payment_term_id
    x_studio_po_reference = fields.Char(string="PO Reference",)
    x_studio_attention_to = fields.Char(string="Attention To",required=True)
    x_studio_subject = fields.Char(string="Subject",required=True)

    # Below partner_id (Invisible fields)
    x_approved_widget_enable = fields.Boolean(default=False)
    x_confirm_enable = fields.Boolean(default=False)
    x_approved = fields.Boolean(default=False)

    # Other Info Tab
    x_studio_include_vat_in_print = fields.Boolean(
        string="VAT Included",
        default=False
    )
    x_client_ref_id = fields.Char(
        string="Enquiry Reference",
        required=True
    )
    x_studio_approved_status = fields.Selection(
        [('Approved', 'Approved'), ('Not Approved', 'Not Approved')],
        string="SQ Approval",
        default='Not Approved',
        tracking=True,
    )

    def _update_project_budget(self, vals):
        """ Internal method to handle budget logic for both Create and Write """
        for record in self:

            if record:
                project = record.project_id
                if project:
                    # Current material budget in the project
                    current_material_budget = project.x_studio_material_budget or 0.0
                    # Total sales budget previously allocated
                    total_sales_budget = project.x_studio_total_sales_budget or 0.0
                    # New budget from this sale order
                    new_sale_budget = record.x_studio_amc_percentage_total or 0.0

                    po_purchase = project.x_studio_purchase_budget or 0.0

                    # --- Budget Adjustment Logic ---
                    if total_sales_budget > new_sale_budget:
                        if po_purchase > new_sale_budget:
                            raise UserError(
                                f"⚠️ Budget update not allowed. The amount {po_purchase} has already been included in the project budget."
                            )
                        else:
                            remain_budget = po_purchase - new_sale_budget
                            project.write({
                                'x_studio_material_budget': abs(remain_budget),
                                'x_studio_total_sales_budget': new_sale_budget,
                                'x_studio_purchase_budget': abs(new_sale_budget - abs(remain_budget)),
                            })
                    else:

                        # Value higher, so update
                        budget_difference = new_sale_budget - total_sales_budget
                        updated_budget = current_material_budget + budget_difference
                        project.write({
                            'x_studio_material_budget': updated_budget,
                            'x_studio_total_sales_budget': new_sale_budget,
                        })

                # --- Step 2: Link all invoices to this sale order ---
                #invoices = record.env['account.move'].search([
                #   ('ref', '=', record.name)])

                # Update all found invoices with sale order id
                #invoices.write({
                  #  'x_studio_sale_order_id': record.id
                #})

                # Safely collect all invoice names (avoid bool error)
                #invoice_names = ', '.join(str(n or '') for n in invoices.mapped('name'))

                # Optional: Show confirmation
                # raise UserError(f"✅ Linked Invoices: {invoice_names or 'No Invoices Found'}")

            else:
                raise UserError(f"⚠️ No Sale Order found for origin: {record.origin or 'N/A'}")

    def write(self, vals):
        # Check if budget-related fields are in the update
        budget_fields = [
            'x_studio_amc_percentage_total',
            'x_studio_set_purchase_budget_valueamt',
            'x_studio_amc_percentage'
        ]

        res = super(SaleOrder, self).write(vals)

        if any(field in vals for field in budget_fields):
            self._update_project_budget(vals)

        return res


    @api.depends(
        'order_line.invoice_lines.move_id.amount_residual',
        'order_line.invoice_lines.move_id.amount_total',
        'order_line.invoice_lines.move_id.state'
    )
    def _compute_invoice_payment_status(self):
        for order in self:

            # Get only posted customer invoices
            invoices = order.order_line.mapped('invoice_lines.move_id').filtered(
                lambda m: m.state == 'posted' and m.move_type == 'out_invoice'
            )

            if not invoices:
                order.x_sales_order_invoice_status = 'Not Received'
                continue

            total_due = sum(invoices.mapped('amount_residual'))
            total_invoice_amount = sum(invoices.mapped('amount_total'))
            total_paid = total_invoice_amount - total_due

            if total_paid <= 0:
                order.x_sales_order_invoice_status = 'Not Received'

            elif total_due == 0:
                order.x_sales_order_invoice_status = 'Fully Received'

            else:
                order.x_sales_order_invoice_status = 'Partially Received'
