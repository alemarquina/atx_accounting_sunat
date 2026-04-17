{
    'name': 'ATX SIRE Sync Bills',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Sync vendor bills from SUNAT SIRE into Odoo (Peru)',
    'author': 'Alessandro Marquina',
    'license': 'LGPL-3',
    'depends': [
        'atx_accounting_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/atx_cpe_type_data.xml',
        'views/atx_account_move_views.xml',
        'wizard/atx_sync_wizard_views.xml',
        'views/atx_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
