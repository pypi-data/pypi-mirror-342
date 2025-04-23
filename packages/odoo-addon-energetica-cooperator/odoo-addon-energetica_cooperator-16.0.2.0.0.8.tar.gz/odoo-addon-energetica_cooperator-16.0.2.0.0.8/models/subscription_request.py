from odoo import fields, models


class SubscriptionRequest(models.Model):
    _inherit = "subscription.request"

    creation_date = fields.Datetime()
    modification_date = fields.Datetime()
    representative_vat = fields.Char()
    notes = fields.Text()
    state_id = fields.Many2one("res.country.state", string="Province")
    vat = fields.Char()

    def get_partner_vals(self):
        vals = super().get_partner_vals()
        vals["vat"] = self.vat
        return vals

    def get_partner_company_vals(self):
        vals = super().get_partner_company_vals()
        vals["company_register_number"] = self.company_register_number
        vals["representative_vat"] = self.representative_vat
        return vals

    def get_required_field(self):
        req_fields = super().get_required_field()[:]
        req_fields.append("vat")

        return req_fields

    def _get_partner_domain(self):
        if self.vat:
            return [("vat", "=", self.vat)]
        else:
            return None
