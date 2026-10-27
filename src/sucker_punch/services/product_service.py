from ..models.product import Product
from .odoo_client import OdooClient

# Solo bienes (no servicios) que se pueden vender y están en el Punto de Venta
BASE_DOMAIN = [
    ['sale_ok', '=', True],
    ['type', '=', 'consu'],
    ['available_in_pos', '=', True],
]


class ProductService:
    """Consultas de productos e inventario a Odoo."""

    def __init__(self, odoo: OdooClient):
        self.odoo = odoo
        self._rates = None  # {id_impuesto: porcentaje}

    def _tax_rates(self, tax_ids: list[int]) -> dict[int, float]:
        """% de cada impuesto de venta del producto: {id: 15.0}."""
        if self._rates is None:
            rows = self.odoo.call(
                'account.tax',
                'search_read',
                domain=[['amount_type', '=', 'percent']],
                fields=['amount'],
            )
            self._rates = {row['id']: row['amount'] for row in rows}
        return {
            tax_id: self._rates[tax_id] for tax_id in tax_ids if tax_id in self._rates
        }

    def _read(self, domain: list, limit: int) -> list[Product]:
        rows = self.odoo.call(
            'product.product',
            'search_read',
            domain=BASE_DOMAIN + domain,
            fields=list(Product.FIELDS),
            limit=limit,
            order='name',
            # sin el "[referencia]" delante del nombre
            context={**self.odoo.context, 'display_default_code': False},
        )
        products = [Product.model_validate(row) for row in rows]
        for product in products:
            product.tax_rates = self._tax_rates(product.tax_ids)
            product.tax_percent = sum(product.tax_rates.values())
        return products

    def by_code(self, code: str) -> list[Product]:
        """Coincidencia exacta por código de barras o referencia interna."""
        return self._read(
            ['|', ['barcode', '=', code], ['default_code', '=', code]], limit=2
        )

    def search(self, pattern: str, limit: int = 90) -> list[Product]:
        """Busca por nombre, código de barras o referencia.

        Si el patrón trae % se usa como comodín (CHOCOL% = empieza con CHOCOL); si no,
        busca que contenga el texto.
        """
        operator = '=ilike' if '%' in pattern else 'ilike'
        return self._read(
            [
                '|',
                '|',
                ['name', operator, pattern],
                ['barcode', operator, pattern],
                ['default_code', operator, pattern],
            ],
            limit=limit,
        )
