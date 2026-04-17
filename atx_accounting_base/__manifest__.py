{
    'name': 'ATX Accounting Base',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Base module for ATX accounting integrations (shared models and config)',
    'author': 'Alessandro Marquina',
    'license': 'LGPL-3',
    'depends': [
        'accountant',
        'l10n_pe',
    ],
    'data': [
        'security/atx_security.xml',
        'security/ir.model.access.csv',
        'views/atx_cpe_config_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
