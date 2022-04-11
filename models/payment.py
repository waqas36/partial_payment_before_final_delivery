from odoo import api, fields, models, _


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    # New Payment term with Boolean
    is_partial_payment_term = fields.Boolean(string="Partial Payment Term")

    # Constrain to check only 1 payment term is checked for the Boolean
    # @api.constrains('is_partial_payment_term')
    # def _change_partial_status(self):
    #     if self.is_partial_payment_term:
    #         payment_term = self.search([('id', '!=', self.id)])
    #         for term in payment_term:
    #             term.is_partial_payment_term = False