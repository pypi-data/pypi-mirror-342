import base64
import re
from datetime import datetime
from urllib.parse import urljoin

from odoo import http
from odoo.http import request
from odoo.tools.translate import _

from odoo.addons.cooperator_website.controllers import main as emyc_wsc


class WebsiteSubscription(emyc_wsc.WebsiteSubscription):
    def fill_values(self, values, is_company, logged, load_from_user=False):
        values = super(WebsiteSubscription, self).fill_values(values, is_company, logged, load_from_user=False)
        values.update({
            'country_id': 68,
            'states': self.get_states()
        })
        return values

    def get_states(self):
        # Show only spanish provinces 
        states = request.env["res.country.state"].sudo().search([
            ("country_id", "=", 68)
        ])
        return states
