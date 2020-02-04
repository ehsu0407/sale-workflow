# Copyright 2011 Akretion Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2013 Camptocamp SA (author: Guewen Baconnier)
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.move"

    workflow_sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Workflow Sales Order',
        compute='_compute_workflow_sale_order',
        store=True,
    )

    workflow_process_id = fields.Many2one(
        comodel_name='sale.workflow.process',
        string='Sale Workflow Process',
        related="workflow_sale_id.workflow_process_id",
        store=True,
    )

    @api.depends('invoice_line_ids')
    def _compute_workflow_sale_order(self):
        for invoice in self:
            sales_order = None
            # All invoice lines must belong to the same sales order for this to return its workflow_process_id
            for line in invoice.invoice_line_ids:
                for sale_line in line.sale_line_ids:
                    if sales_order is None:
                        sales_order = sale_line.order_id
                    elif sales_order != sale_line.order_id:
                        # different sales order line found in this invoice, no workflow id possible
                        sales_order = None
                        break

                if not sales_order:
                    # No sales order could be found linked to this invoice.
                    break

            if sales_order:
                invoice.workflow_sale_id = sales_order.id
            else:
                invoice.workflow_sale_id = None
