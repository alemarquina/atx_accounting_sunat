from odoo import fields, models


class AtxCpeConfig(models.Model):
    _name = 'atx.cpe.config'
    _description = 'SUNAT API Configuration per Company'
    _rec_name = 'company_id'

    company_id = fields.Many2one(
        'res.company',
        required=True,
        ondelete='cascade',
    )
    atx_client_id = fields.Char(string='Client ID')
    atx_client_secret = fields.Char(
        string='Client Secret',
        groups='base.group_system',
    )
    atx_ruc = fields.Char(string='RUC', size=11)
    atx_sol_user = fields.Char(string='SOL User')
    atx_sol_password = fields.Char(
        string='SOL Password',
        groups='base.group_system',
    )
    atx_environment = fields.Selection(
        selection=[
            ('produccion', 'Producción'),
            ('pruebas', 'Pruebas'),
        ],
        string='Environment',
        default='pruebas',
        required=True,
    )
    atx_ultimo_periodo = fields.Char(
        string='Last Period (YYYYMM)',
        size=6,
    )
    atx_active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('company_unique', 'unique(company_id)', 'Only one SUNAT config per company is allowed.'),
    ]
