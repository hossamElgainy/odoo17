from email.policy import default

from stdnum.nl import postcode

from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread','mail.activity.mixin'] # for chatter
    _rec_name = 'postcode'
    _description = 'Property'

    ref = fields.Char(default="New",readonly=True)
    name = fields.Char(required=True,size=200)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=True)
    expected_selling_date = fields.Date()
    is_late = fields.Boolean(default=False)
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff',store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('south', 'South'),
        ('north', 'North'),
        ('east', 'East'),
        ('west', 'West'),
    ],default='south')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ],default='draft')
    active = fields.Boolean(default=True)

    owner_id = fields.Many2one('owner') # add a relation with owners model
    tag_ids = fields.Many2many('tag')
    line_ids = fields.One2many('property.line','property_id')
    owner_address = fields.Char(related='owner_id.address',readonly=False)
    owner_phone = fields.Char(related='owner_id.phone')

    _sql_constraints = [ # add constraint on database level(height level)
        ('unique_name','unique("name")','This Name Is Exist')#constraint name(any name),constraint(field),message To Show
    ]
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for record in self:
            if record.bedrooms == 0 :
                raise ValidationError('Bedrooms must be greater than 0')

    def action_draft(self):
        for record in self:
            record.property_history_create(record.state,'draft',"")
            record.state = 'draft'

    def action_pending(self):
        for record in self:
            record.property_history_create(record.state, 'pending',"")
            record.state = 'pending'

    def action_sold(self):
        for record in self:
            record.property_history_create(record.state, 'sold',"")
            record.state = 'sold'

    def action_closed(self):
        for record in self:
            record.property_history_create(record.state, 'closed',"")
            record.state = 'closed'

    @api.depends('expected_price','selling_price') #decorator for computed fields
    def _compute_diff(self):
        for record in self:
            record.diff = abs(record.expected_price - record.selling_price)

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for record in property_ids:
            if record.expected_selling_date and record.expected_selling_date <fields.Date.today():
                record.is_late = True

    @api.model
    def create(self, vals):
        res = super(Property,self).create(vals)
        if res.ref=='New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def property_history_create(self,old_state,new_state,reason):
        for record in self:
            record.env['property.history'].create({
                'user_id':record.env.uid,
                'property_id':record.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason':reason or ""
            })

    def action_change_state_wizerd(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id':self.id}
        return action

    def action(self):
        print(self.env['owner'].search([]))

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action') # get the action
        view_id = self.env.ref('app_one.owner_view_form').id #get the form id
        action['res_id'] = self.owner_id.id # get the owner id
        action['views'] = [[view_id,'form']] # identify it to open the form view not the tree view
        return action

    def property_xlsx_report(self):
        return {
            'type':'ir.actions.act_url',
            'url':f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }
    # @api.model
    # def create(self,vals): # override the creation method
    #     res = super(Property,self).create(vals)
    #     print('inside create method')
    #     return res
    # 
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None): ########## read ##########
    #     res = super(Property,self)._search(domain, offset, limit, order, access_rights_uid)
    #     print ('inside search method')
    #     return res
    #
    # def write(self,vals): ############### update #############
    #     res = super(Property,self).write(vals)
    #     print ('inside write method')
    #     return res
    #
    # def unlink(self): ################### Delete ##############
    #     res = super(Property,self).unlink()
    #     print ('inside unlink method')
    #     return res
class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Lines'

    area = fields.Float()
    description = fields.Char()

    property_id= fields.Many2one('property')