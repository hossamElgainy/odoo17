from odoo import api, fields, models, tools

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    def action_do_something(self):
        print(self,"printed from account move ")