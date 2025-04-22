from odoo import fields, models


class SubscriptionRequest(models.Model):
    _inherit = "subscription.request"

    creation_date = fields.Datetime()
    modification_date = fields.Datetime()
    representative_vat = fields.Char()
    notes = fields.Text()
    state_id = fields.Many2one("res.country.state", string="Province")
