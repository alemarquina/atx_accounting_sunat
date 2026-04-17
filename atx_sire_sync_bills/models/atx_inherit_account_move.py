from odoo import api, fields, models


class AtxInheritAccountMove(models.Model):
    _inherit = 'account.move'

    # --- Identificación del CPE ---
    atx_cpe_type = fields.Selection(
        selection=[
            ('01', 'Factura electrónica'),
            ('02', 'Recibo por honorarios'),
            ('03', 'Boleta de venta'),
            ('04', 'Liquidación de compra'),
            ('07', 'Nota de crédito'),
            ('08', 'Nota de débito'),
            ('20', 'Comprobante de retención'),
            ('40', 'Comprobante de percepción'),
            ('50', 'DUA (Importaciones)'),
        ],
        string='Tipo CPE',
    )
    atx_serie = fields.Char(string='Serie', size=4)
    atx_correlativo = fields.Char(string='Correlativo', size=8)
    atx_numero_completo = fields.Char(
        string='N° Completo',
        compute='_compute_atx_numero_completo',
        store=True,
    )
    atx_hash_cpe = fields.Char(string='Hash CPE')

    # --- Estado SUNAT ---
    atx_estado_sunat = fields.Selection(
        selection=[
            ('ACEPTADO', 'Aceptado'),
            ('RECHAZADO', 'Rechazado'),
            ('BAJA', 'Baja'),
            ('PENDIENTE', 'Pendiente'),
        ],
        string='Estado SUNAT',
    )
    atx_cdr_numero = fields.Char(string='CDR Número', readonly=True)
    atx_cdr_fecha = fields.Date(string='CDR Fecha', readonly=True)
    atx_estado_proceso = fields.Selection(
        selection=[
            ('nuevo', 'Nuevo'),
            ('revisado', 'Revisado'),
            ('observado', 'Observado'),
            ('contabilizado', 'Contabilizado'),
        ],
        string='Estado Proceso',
        default='nuevo',
    )

    # --- Montos SUNAT para corroborar contra factura física ---
    atx_base_imponible = fields.Monetary(string='Base Imponible SUNAT')
    atx_igv_monto = fields.Monetary(string='IGV SUNAT')
    atx_total_sunat = fields.Monetary(string='Total SUNAT')
    atx_montos_ok = fields.Boolean(
        string='Montos OK',
        compute='_compute_atx_montos_ok',
        store=True,
    )

    # --- Detracción ---
    atx_tiene_detraccion = fields.Boolean(string='Tiene Detracción')
    atx_detraccion_porcentaje = fields.Float(string='Detracción %', digits=(5, 2))
    atx_detraccion_monto = fields.Monetary(string='Monto Detracción')
    atx_detraccion_cuenta = fields.Char(string='Cuenta BN Detracciones')
    atx_detraccion_fecha = fields.Date(string='Fecha Pago Detracción')
    atx_bien_servicio_code = fields.Char(string='Código Bien/Servicio')

    # --- Retención ---
    atx_tiene_retencion = fields.Boolean(string='Tiene Retención')
    atx_retencion_monto = fields.Monetary(string='Monto Retención')
    atx_retencion_porcentaje = fields.Float(string='Retención %', digits=(5, 2))

    # --- Percepción ---
    atx_tiene_percepcion = fields.Boolean(string='Tiene Percepción')
    atx_percepcion_monto = fields.Monetary(string='Monto Percepción')
    atx_percepcion_porcentaje = fields.Float(string='Percepción %', digits=(5, 2))

    # --- Campos DUA (tipo 50) ---
    atx_dua_numero = fields.Char(string='N° DUA')
    atx_dua_aduana = fields.Char(string='Aduana')
    atx_dua_fecha_numeracion = fields.Date(string='Fecha Numeración DUA')

    # --- Nota de crédito/débito (07, 08) ---
    atx_doc_origen_tipo = fields.Char(string='Tipo Doc. Origen')
    atx_doc_origen_serie = fields.Char(string='Serie Doc. Origen')
    atx_doc_origen_numero = fields.Char(string='Número Doc. Origen')
    atx_motivo_nota = fields.Char(string='Motivo')

    # --- Moneda y tipo de cambio ---
    atx_moneda_sunat = fields.Selection(
        selection=[
            ('PEN', 'Soles (PEN)'),
            ('USD', 'Dólares (USD)'),
            ('EUR', 'Euros (EUR)'),
        ],
        string='Moneda SUNAT',
    )
    atx_tipo_cambio_sbs = fields.Float(
        string='T.C. SBS',
        digits=(12, 3),
    )

    # --- Trazabilidad ---
    atx_sync_date = fields.Datetime(string='Última Sincronización', readonly=True)
    atx_sync_origin = fields.Selection(
        selection=[
            ('manual', 'Manual'),
            ('api_sire', 'API SIRE'),
            ('importacion', 'Importación'),
        ],
        string='Origen Sync',
        readonly=True,
    )
    atx_notas_contador = fields.Text(string='Notas del Contador')
    atx_revisado_por = fields.Many2one('res.users', string='Revisado Por')
    atx_revisado_fecha = fields.Datetime(string='Fecha Revisión')

    @api.depends('atx_serie', 'atx_correlativo')
    def _compute_atx_numero_completo(self):
        for move in self:
            if move.atx_serie and move.atx_correlativo:
                move.atx_numero_completo = f'{move.atx_serie}-{move.atx_correlativo}'
            else:
                move.atx_numero_completo = False

    @api.depends('amount_untaxed', 'amount_tax', 'amount_total',
                 'atx_base_imponible', 'atx_igv_monto', 'atx_total_sunat')
    def _compute_atx_montos_ok(self):
        threshold = 0.10
        for move in self:
            if not (move.atx_base_imponible or move.atx_igv_monto or move.atx_total_sunat):
                move.atx_montos_ok = True
                continue
            diff_base = abs(move.amount_untaxed - move.atx_base_imponible)
            diff_igv = abs(move.amount_tax - move.atx_igv_monto)
            diff_total = abs(move.amount_total - move.atx_total_sunat)
            move.atx_montos_ok = (
                diff_base <= threshold
                and diff_igv <= threshold
                and diff_total <= threshold
            )
