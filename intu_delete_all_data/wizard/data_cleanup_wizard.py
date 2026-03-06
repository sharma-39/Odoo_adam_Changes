from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class DataCleanupWizard(models.TransientModel):
    _name = "data.cleanup.wizard"
    _description = "Delete All Transaction Data"

    confirm = fields.Boolean(string="Confirm Deletion")

    def action_delete_all_data(self):

        env = self.env

        # Delete Sale Orders
        # List of custom models to delete
        models_to_delete = [
            'x_sales_report',
            'x_po_category',
            'x_custom_form',
            'x.wizard.form',
            'x_mr_wizard'
        ]

        # Loop through the list and delete records
        for model_name in models_to_delete:
            records = env[model_name].search([])
            for record in records:
                try:
                    record.unlink()
                except Exception as e:
                    _logger.info(f"Cannot delete record {record.id} from {model_name}: {e}")

        # --- SALE ORDERS ---
        sale_orders = env['sale.order'].search([])
        for order in sale_orders:
            try:
                try:
                    order.action_unlock()
                except:
                    pass
                if order.state != 'cancel':
                    order.action_cancel()
                    order.unlink()
            except Exception as e:
                _logger.info(f"Cannot delete Sale Order {order.name}: {e}")

        purchase_orders = env['purchase.order'].search([])

        for po in purchase_orders:
            try:
                # 1️⃣ If state is NOT purchase → unlock then cancel
                if po.state != 'purchase':
                    try:
                        po.button_unlock()
                    except Exception:
                        pass  # ignore if already unlocked

                    if po.state != 'cancel':
                        try:
                            po.button_cancel()
                        except Exception:
                            pass

                # 2️⃣ If state IS purchase → cancel directly after unlock
                else:
                    try:
                        po.button_unlock()
                    except Exception:
                        pass

                    try:
                        po.button_cancel()
                    except Exception:
                        pass

                # 3️⃣ Finally delete
                try:
                    po.unlink()
                except Exception as e:
                    _logger.info(f"Cannot delete PO {po.name}: {e}")

            except Exception as e:
                _logger.info(f"Error handling PO {po.name}: {e}")

        # --- DELETE ANALYTIC LINES ---
        env['account.analytic.line'].search([]).unlink()

        # --- DELETE TASKS ---
        tasks = env['project.task'].search([])
        for task in tasks:
            task.unlink()

        # --- DELETE PROJECTS ---
        projects = env['project.project'].search([])
        for project in projects:
            try:
                # Delete dependent Project Updates first
                updates = env['project.update'].search([('project_id', '=', project.id)])
                updates.unlink()

                # Now delete the project
                project.unlink()
            except Exception as e:
                _logger.warning(f"Cannot delete Project {project.name}: {e}")

        # --- DELETE BOMs ---
        boms = env['mrp.bom'].search([])
        for bom in boms:
            try:
                # Optionally cancel linked manufacturing orders first
                mfg_orders = env['mrp.production'].search([('bom_id', '=', bom.id)])
                for mo in mfg_orders:
                    try:
                        if mo.state not in ('cancel', 'done'):
                            mo.action_cancel()
                        mo.unlink()
                    except Exception as e:
                        _logger.info(f"Cannot delete Manufacturing Order {mo.name}: {e}")

                # Delete the BOM itself
                bom.unlink()
            except Exception as e:
                _logger.info(f"Cannot delete BOM {bom.name}: {e}")

        # --- DELETE CUSTOMER INVOICES ---

        # --- DELETE CREDIT NOTES / DEBIT NOTES ---
        refunds = env['account.move'].search([('move_type', 'in', ['out_refund', 'in_refund'])])
        for refund in refunds:
            try:
                if refund.state != 'draft':
                    refund.button_draft()
                refund.unlink()
            except Exception as e:
                _logger.info(f"Cannot delete Refund {refund.name}: {e}")

        # --- DELETE PAYMENTS ---
        payments = env['account.payment'].search([])
        for payment in payments:
            try:
                if payment.state != 'draft':
                    payment.action_draft()
                payment.unlink()
            except Exception as e:
                _logger.info(f"Cannot delete Payment {payment.name}: {e}")

        customer_invoices = env['account.move'].search([])
        for invoice in customer_invoices:
            try:
                if invoice.state != 'draft':
                    invoice.button_draft()  # reset to draft if posted
                invoice.unlink()
            except Exception as e:
                _logger.info(f"Cannot delete Customer Invoice {invoice.name}: {e}")

        # --- DELETE VENDOR BILLS ---
        # vendor_bills = env['account.move'].search([('move_type', '=', 'in_invoice')])
        # for bill in vendor_bills:
        #     try:
        #         if bill.state != 'draft':
        #             bill.button_draft()
        #         bill.unlink()
        #     except Exception as e:
        #         _logger.info(f"Cannot delete Vendor Bill {bill.name}: {e}")
        # vendor_bills = env['account.move'].search([('move_type', '=', 'in_invoice')])

        # for bill in vendor_bills:
        #     for line in bill.line_ids:
        #         if line.reconciled:
        #             line.remove_move_reconcile()

        #         # Reset to draft
        #         if bill.state != 'draft':
        #             bill.button_draft()

        #         # Delete
        #         bill.unlink()

        # except Exception as e:
        #     _logger.error(f"Failed to delete bill {bill.name}: {str(e)}")

        purchase_orders = env['purchase.order'].search([])

        for po in purchase_orders:
            try:
                # 1️⃣ If state is NOT purchase → unlock then cancel
                if po.state != 'purchase':
                    try:
                        po.button_unlock()
                    except Exception:
                        pass  # ignore if already unlocked

                    if po.state != 'cancel':
                        try:
                            po.button_cancel()
                        except Exception:
                            pass

                # 2️⃣ If state IS purchase → cancel directly after unlock
                else:
                    try:
                        po.button_unlock()
                    except Exception:
                        pass

                    try:
                        po.button_cancel()
                    except Exception:
                        pass

                # 3️⃣ Finally delete
                try:
                    po.unlink()
                except Exception as e:
                    _logger.info(f"Cannot delete PO {po.name}: {e}")

            except Exception as e:
                _logger.info(f"Error handling PO {po.name}: {e}")

        products = env['product.product'].search([('name', 'ilike', 'JOD')])
        for product in products:
            product.unlink()

        templates = env['product.template'].search([('name', 'ilike', 'JOD')])
        templates.unlink()

        done_pickings = env['stock.picking'].search([('state', '=', 'done')])

        # Run server action safely on each done picking
        for done in done_pickings:
            try:
                env['ir.actions.server'].sudo().browse(1030).with_context(
                    active_model='stock.picking',
                    active_ids=[done.id],
                ).run()
            except Exception as e:
                _logger.error(f"Error running server action on picking {done.id}: {e}")

        # Now, delete pickings safely

        done_moves = env['stock.move.line'].search([('state', '=', 'done')])
        for move in done_moves:
            move.write({"state": "New"})
        done_moves = env['stock.move.line'].search([])
        for move_line in done_moves:
            try:
                move_line.sudo().unlink()
            except Exception as e:
                _logger.error(f"Error unlinking move line {move_line.id}: {e}")

        pickings = env['stock.picking'].search([])  # Or filter specific pickings

        for picking in pickings:
            try:
                picking.unlink()
            except Exception as e:
                # Log or raise error
                _logger.error(f"Error deleting picking {picking.name}: {e}")

        # First, set all expenses to draft (so they can be deleted)
        expenses = env['hr.expense'].search([])
        expenses.write({'state': 'draft'})

        # Now unlink all
        expenses.unlink()

        # Search all stock.quant records
        quants = env['stock.quant'].search([])

        # Unlink them
        quants.unlink()

        moves = env['stock.move'].search([])
        moves.write({'state': 'draft'})
        moves.unlink()

        moves = env['stock.move.line'].search([])
        moves.unlink()
        quants = env['stock.quant'].search([])

        quants.unlink()

        products = env['product.product'].search([
            ('name', '!=', 'Service on Timesheets')  # Exclude by name
        ])

        for product in products:
            env['sale.order.template.line'].search([('product_id', '=', product.id)]).unlink()
            # Remove dependent sale order lines
            env['sale.order.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove dependent purchase order lines
            env['purchase.order.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove dependent stock moves
            env['stock.move'].search([('product_id', '=', product.id)]).unlink()

            # Remove stock quants
            env['stock.quant'].search([('product_id', '=', product.id)]).unlink()

            # Remove account move lines
            env['account.move.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove account move lines
            env['account.move.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove analytic lines
            env['account.analytic.line'].search([('product_id', '=', product.id)]).unlink()
            product.unlink()

        # Finally, unlink the product itsel
        # Get all products
        products = env['product.product'].with_context(active_test=False).search([
            ('active', '=', False),
            ('name', '!=', 'Booking Fees')  # Exclude by name
        ])

        for product in products:
            env['sale.order.template.line'].search([('product_id', '=', product.id)]).unlink()
            # Remove dependent sale order lines
            env['sale.order.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove dependent purchase order lines
            env['purchase.order.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove dependent stock moves
            env['stock.move'].search([('product_id', '=', product.id)]).unlink()

            # Remove stock quants
            env['stock.quant'].search([('product_id', '=', product.id)]).unlink()

            # Remove account move lines
            env['account.move.line'].search([('product_id', '=', product.id)]).unlink()

            # Remove analytic lines
            env['account.analytic.line'].search([('product_id', '=', product.id)]).unlink()

            # Finally, unlink the product itself
            product.unlink()

        all_sequences = env['ir.sequence'].search([])
        for seq in all_sequences:
            seq.write({
                'number_next': 1,
                'number_next_actual': 0
            })


        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'All transaction data deleted!',
                'sticky': False,
            }
        }