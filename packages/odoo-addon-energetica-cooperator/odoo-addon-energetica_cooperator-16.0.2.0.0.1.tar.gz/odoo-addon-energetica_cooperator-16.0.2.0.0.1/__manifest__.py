{
    "name": "Odoo customizations for Energetica Cooperator",
    "version": "16.0.2.0.0",
    "depends": [
        "base",
        "cooperator",
        "cooperator_website",
        "l10n_es",
        "l10n_es_cooperator",
    ],
    "author": "Coopdevs Treball SCCL",
    "category": "Cooperator",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Odoo customizations for Energetica Cooperator.
    """,
    "data": [
        "views/res_partner.xml",
        "views/subscription_request.xml",
        "views/subscription_template.xml",
    ],
    "installable": True,
}
