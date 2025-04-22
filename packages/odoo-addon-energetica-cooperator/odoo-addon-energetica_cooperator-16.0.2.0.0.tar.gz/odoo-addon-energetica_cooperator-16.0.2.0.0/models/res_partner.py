from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    creation_date = fields.Datetime()
    modification_date = fields.Datetime()
    representative_vat = fields.Char()
