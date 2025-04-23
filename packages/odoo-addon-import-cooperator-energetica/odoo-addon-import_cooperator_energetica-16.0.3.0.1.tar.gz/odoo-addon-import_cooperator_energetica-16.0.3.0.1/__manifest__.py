{
    "name": "Odoo Import Cooperator Energetica",
    "summary": "Odoo Import Cooperator Energetica",
    "version": "16.0.3.0.1",
    "category": "Account",
    "author": "Coopdevs Treball",
    "website": "https://coopdevs.coop",
    "license": "AGPL-3",
    "depends": [
        "cooperator",
        "energetica_cooperator",
        "queue_job",
    ],
    "data": [
        "data/ir_action_server.xml",
        "security/ir.model.access.csv",
        "views/menuitems.xml",
        "views/import_cooperator_view.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": True,
    "images": [],
}
