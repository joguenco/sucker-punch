from pydantic import BaseModel


class SaleResult(BaseModel):
    """Lo que quedó en Odoo al guardar una venta."""

    order: str  # pedido, ej. S00012
    invoice: str  # factura, ej. FAC 001-001-000000012
    total: float
    payment_state: str  # en español, ej. Pagada
    # Para la factura impresa (vacíos sin la localización de Ecuador)
    number: str = ''  # ej. 001-001-000000012
    access_key: str = ''  # clave de acceso del SRI, 49 dígitos
