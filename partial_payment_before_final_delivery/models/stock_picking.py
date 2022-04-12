# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = 'stock.picking'

    def compute_order_id(self):
        for rec in self:
            if rec.origin:
                so_rec = self.env['sale.order'].search([('name', '=', rec.origin)])
                rec.so_customer_pickup = so_rec.id
            else:
                rec.so_customer_pickup = False

    so_customer_pickup = fields.Many2one('sale.order', string="Sale Order Reference", compute="compute_order_id")
    is_send = fields.Boolean(string="Is Already Send")

    def button_validate(self):
        for rec in self:
            if rec.origin:
                payment_term_ids = self.env['account.payment.term'].search([
                    ('is_partial_payment_term', '=', True)]) #, limit=1)
                for payment_term_id in payment_term_ids:
                    if rec.so_customer_pickup and rec.so_customer_pickup.payment_term_id.id == payment_term_id.id:
                        invoice_ids = self.env['account.move'].search([
                            ('invoice_origin', '=', rec.origin),
                            ('move_type', '=', 'out_invoice')])
                        if not invoice_ids.ids:
                            raise UserError(_("Invoice is not created for this "
                                              "delivery!"))
                        invoice_due_amount = sum(
                            invoice_ids.mapped('amount_residual'))
                        invoice_amount = sum(
                            invoice_ids.mapped('amount_total'))
                        order_amount = rec.so_customer_pickup.amount_total
                        payment_amount = 0
                        for line in payment_term_id.line_ids:
                            if line.value == 'percent' and line.days == 0 and line.option == 'day_after_invoice_date':
                                payment_amount += order_amount * (line.value_amount / 100)
                            if line.value == 'fixed' and line.days == 0 and line.option == 'day_after_invoice_date':
                                payment_amount += line.value_amount
                        if payment_term_id.line_ids:
                            if (invoice_amount - invoice_due_amount) < payment_amount:
                                raise UserError(_("Agreed Amount for this shipment is not paid yet."))
                        # elif (order_amount / 2 > invoice_amount and not order_amount / 2 < invoice_amount) or \
                        #         invoice_due_amount > 0.0 or not invoice_ids:
                        #     raise UserError(_("Amount for this shipment is not "
                        #                       "fully paid!"))
        return super(Picking, self).button_validate()

    def action_assign(self):
        res = super(Picking, self).action_assign()
        for rec in self:
            if rec.state == 'assigned':
                rec._send_assigned_email()
        return res

    def _send_assigned_email(self):
        ir_config_parameter_obj = self.env['ir.config_parameter']
        stock_mail_assigned_template_id = ir_config_parameter_obj.get_param(
            'partial_payment_before_final_delivery.stock_mail_assigned_template_id', False)

        for stock_pick in self.filtered(lambda p: p.picking_type_id.code == 'outgoing'):
            if not stock_pick.is_send:
                assigned_template_id = int(stock_mail_assigned_template_id)
                stock_pick.with_context(force_send=True).message_post_with_template(assigned_template_id,
                                                                                    email_layout_xmlid='mail.mail_notification_light')
                stock_pick.is_send = True

    def _send_confirmation_email(self):
        for rec in self:
            if rec.so_customer_pickup:
                ir_config_parameter_obj = self.env['ir.config_parameter']
                stock_mail_confirmation_template_id = ir_config_parameter_obj.get_param(
                    'partial_payment_before_final_delivery.stock_mail_confirm_template_id', False)
                for stock_pick in self.filtered(
                        lambda p: p.company_id.stock_move_email_validation and p.picking_type_id.code == 'outgoing'):
                    delivery_template_id = int(stock_mail_confirmation_template_id)
                    stock_pick.with_context(force_send=True).message_post_with_template(delivery_template_id,
                                                                                        email_layout_xmlid='mail.mail_notification_light')
            else:
                return super(Picking, self)._send_confirmation_email()
