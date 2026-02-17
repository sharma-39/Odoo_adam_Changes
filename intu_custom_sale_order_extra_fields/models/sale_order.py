from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
