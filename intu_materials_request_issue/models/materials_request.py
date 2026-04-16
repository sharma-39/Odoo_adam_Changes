from odoo import models, fields, api,_
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _inherit = "x_custom_form"

    def action_create_rfq_bom(self):
        self.ensure_one()

        lines = []

        # -------------------------------------------------
        # Prepare Wizard Lines
        # -------------------------------------------------
        for line in self.x_custom_form_line_ids:

            product = line.x_studio_product

            mr_qty = line.x_studio_qty or 0.0
            delivered_qty = line.x_studio_received_qty or 0.0
            waiting_po_qty = line.x_studio_waiting_po_qty or 0.0
            received_po_qty = line.x_studio_received_po_qty or 0.0

            rfq_qty = max(
                mr_qty - delivered_qty - received_po_qty - waiting_po_qty,
                0.0
            )

            if rfq_qty <= 0:
                continue

            qty_on_hand = product.qty_available if product else 0.0

            vendor_id = False
            if product and product.seller_ids:
                vendor_id = product.seller_ids[0].partner_id.id

            lines.append((0, 0, {
                'x_studio_sequence': line.x_studio_sequence,
                'x_studio_mr_name': product.id if product else False,
                'x_studio_qty': rfq_qty,
                'x_studio_unit': line.x_studio_unit.id if line.x_studio_unit else False,
                'x_studio_qty_on_hand': qty_on_hand,
                'x_studio_rfq_qty': 0.0,
                'x_name': line.x_studio_remarks_1,
                'x_studio_vendor_1': vendor_id,
            }))

        if not lines:
            raise UserError(_(
                    "No pending quantities available.\n"
                    "All required quantities are already delivered "
                    "or covered by existing PO."
            ))
        # -------------------------------------------------
        # Open Wizard WITHOUT create()
        # -------------------------------------------------
        return {
            'name': _('Create RFQ Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'x_mr_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_x_studio_flow': "create",
                'default_x_studio_job_order_no': self.x_studio_sale_order_number.id if self.x_studio_sale_order_number else False,
                'default_x_studio_mr_number': self.x_studio_mr_number,
                'default_x_studio_dr_number': self.x_studio_delivery_number,
                'default_x_studio_project': self.x_studio_project.id if self.x_studio_project else False,
                'default_x_studio_responsibility': self.env.uid,
                'default_x_mr_wizard_line_ids_e1f04': lines,
            }
        }
