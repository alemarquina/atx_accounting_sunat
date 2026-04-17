from odoo import fields, models


class AtxSyncWizard(models.TransientModel):
    _name = 'atx.sync.wizard'
    _description = 'SIRE Sync Wizard'

    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company,
    )
    atx_periodo = fields.Char(
        string='Período (YYYYMM)',
        required=True,
        size=6,
    )

    def action_sync(self):
        # Fase 4 — API SUNAT/SIRE integration goes here
        return {'type': 'ir.actions.act_window_close'}
