from odoo import fields, models


class AtxSyncLog(models.Model):
    _name = 'atx.sync.log'
    _description = 'SUNAT Sync Log'
    _order = 'atx_sync_date desc'

    company_id = fields.Many2one('res.company', required=True, ondelete='cascade')
    atx_sync_date = fields.Datetime(string='Sync Date', required=True)
    atx_periodo = fields.Char(string='Period (YYYYMM)', size=6)
    atx_origin = fields.Selection(
        selection=[
            ('manual', 'Manual'),
            ('api_sire', 'API SIRE'),
            ('importacion', 'Import'),
        ],
        string='Origin',
        required=True,
    )
    atx_total_facturas = fields.Integer(string='Total Bills')
    atx_nuevas = fields.Integer(string='New')
    atx_existentes = fields.Integer(string='Already Existing')
    atx_errores = fields.Integer(string='Errors')
    atx_notas = fields.Text(string='Notes')
    atx_state = fields.Selection(
        selection=[
            ('ok', 'Success'),
            ('parcial', 'Partial'),
            ('error', 'Error'),
        ],
        string='State',
        default='ok',
        required=True,
    )
