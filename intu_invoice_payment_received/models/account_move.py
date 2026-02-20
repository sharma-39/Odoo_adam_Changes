from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_studio_payment_received_amount = fields.Float(
        string="Payment Received Amount",
        compute="_compute_payment_received_amount",
        store=True,
        copy=True
    )

    @api.depends(
        'line_ids.matched_debit_ids.amount',
        'line_ids.matched_credit_ids.amount',
        'line_ids.account_id'
    )
    def _compute_payment_received_amount(self):
        """
        Compute total payment received based on reconciled receivable/payable lines.
        This is the correct accounting way.
        """
        for move in self:
            total = 0.0

            # Only calculate for customer invoices and vendor bills
            if move.move_type in ('out_invoice', 'in_invoice'):
                for line in move.line_ids:

                    # Check receivable/payable accounts
                    if line.account_id.account_type in (
                        'asset_receivable',
                        'liability_payable'
                    ):

                        # Add matched credit amounts
                        for partial in line.matched_credit_ids:
                            total += partial.amount

                        # Add matched debit amounts
                        for partial in line.matched_debit_ids:
                            total += partial.amount

            move.x_studio_payment_received_amount = total