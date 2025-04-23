from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    creation_date = fields.Datetime()
    modification_date = fields.Datetime()
    representative_vat = fields.Char()

    def create_users_from_cooperator_partners(self):
        for record in self:
            if record.cooperator:
                vals = {
                    "partner_id": record.id,
                    "groups_id": [self.env.ref("base.group_portal").id],
                    "email": record.email,
                    "firstname": record.firstname,
                    "lastname": record.lastname,
                    "lang": record.lang,
                }
                if record.is_company:
                    vals["login"] = record.company_register_number or record.email
                else:
                    vals["login"] = record.vat or record.representative_vat or record.email

                user = (
                    self.env["res.users"]
                    .sudo()
                    .with_context(no_reset_password=True)
                    .create(vals)
                )
