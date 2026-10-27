"""Totales de la factura calculados igual que Odoo, para que el total y el vuelto de la
pantalla sean exactamente los que factura Odoo.

Copia la regla de Odoo 19 (~/odoo19/odoo/addons/account/models/account_tax.py,
_add_tax_details_in_base_line y _round_tax_details_*). La empresa elige el redondeo en
Facturación → Ajustes → Impuestos (campo tax_calculation_rounding_method):
- round_per_line: se redondea la base y el IVA de cada línea, y se suman.
- round_globally: se suma todo sin redondear y se redondea al final: la base de toda la
  factura, y el IVA de cada impuesto.
"""

from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal

from ..models.sale_line import SaleLine

CENT = Decimal('0.01')


def money(value: float) -> float:
    """Redondea a centavos como Odoo: la mitad hacia arriba (3.375 → 3.38)."""
    return float(Decimal(repr(value)).quantize(CENT, rounding=ROUND_HALF_UP))


def compute_totals(lines: list[SaleLine], rounding: str = 'round_per_line') -> dict:
    """Base con IVA 0 %, base con IVA, IVA y total (ya redondeados a centavos)."""
    per_line = rounding == 'round_per_line'
    base_0 = base_vat = 0.0
    tax_per_tax = defaultdict(float)  # id del impuesto → IVA acumulado
    for line in lines:
        # Odoo calcula el IVA sobre la base sin redondear
        raw = line.quantity * line.price
        base = money(raw) if per_line else raw
        if line.product.tax_percent:
            base_vat += base
        else:
            base_0 += base
        for tax_id, rate in line.product.tax_rates.items():
            tax = raw * rate / 100
            tax_per_tax[tax_id] += money(tax) if per_line else tax
    vat = money(sum(money(tax) for tax in tax_per_tax.values()))
    untaxed = money(base_0 + base_vat)
    return {
        'rate_0': money(base_0),
        'rate_vat': money(base_vat),
        'vat': vat,
        'total': money(untaxed + vat),
    }
