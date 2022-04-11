# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_assigned_mail_template(self):
        try:
            return self.env.ref('partial_payment_before_final_delivery.mail_template_data_delivery_assigned').id
        except ValueError:
            return False
    
    def _stock_mail_confirm_template_id(self):
        try:
            return self.env.ref('partial_payment_before_final_delivery.mail_template_data_delivery_confirm').id
        except ValueError:
            return False
    
    stock_mail_assigned_template_id = fields.Many2one('mail.template', string="Email Template Assigned picking",
        domain="[('model', '=', 'stock.picking')]",
        default=_default_assigned_mail_template,
        help="Email sent to the customer once the order is Assigned.")
    
    stock_mail_confirm_template_id = fields.Many2one('mail.template', string="Email Template Delivered picking",
        domain="[('model', '=', 'stock.picking')]",
        default= _stock_mail_confirm_template_id,
        help="Email sent to the customer once the order is Validated.")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config_parameter_obj = self.env['ir.config_parameter']
       

        stock_mail_assigned_template_id = ir_config_parameter_obj.get_param(
            'partial_payment_before_final_delivery.stock_mail_assigned_template_id', False)
        stock_mail_confirm_template_id = ir_config_parameter_obj.get_param(
            'partial_payment_before_final_delivery.stock_mail_confirm_template_id', False)
        res.update(
            stock_mail_assigned_template_id = int(stock_mail_assigned_template_id) or False,
            stock_mail_confirm_template_id = int(stock_mail_confirm_template_id) or False
        )
        return res

    def set_values(self):

        super(ResConfigSettings, self).set_values()
        irconfigparams = self.env['ir.config_parameter']
        irconfigparams.set_param(
            'partial_payment_before_final_delivery.stock_mail_assigned_template_id', self.stock_mail_assigned_template_id.id)
        irconfigparams.set_param(
            'partial_payment_before_final_delivery.stock_mail_confirm_template_id', self.stock_mail_confirm_template_id.id)
#         
