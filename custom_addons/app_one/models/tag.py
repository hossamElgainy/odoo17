from odoo import fields, models

class Tag(models.Model):
    _name = 'tag'
    _description = 'Tag'
    name = fields.Char(required=True)