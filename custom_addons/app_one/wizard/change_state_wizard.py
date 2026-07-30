from odoo import api, fields, models, tools



class ChangeState(models.TransientModel):
    _name='change.state'
    _description = 'Change State'

    property_id = fields.Many2one('property')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ],default='draft')
    reason = fields.Char()

    def action_confirm(self):
        if self.state == 'closed':
            self.property_id.state = self.state
            self.property_id.property_history_create('closed',self.state,self.reason)
