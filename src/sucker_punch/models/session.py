from pydantic import BaseModel

from .company import Company


class Session(BaseModel):
    """Usuario que entró a la app y su empresa en Odoo."""

    uid: int
    user_name: str
    company_name: str
    country_code: str = ''  # 'EC' con la localización de Ecuador
    # Cómo redondea Odoo el IVA: round_per_line o round_globally (ver odoo_totals.py)
    tax_rounding: str = 'round_per_line'
    # Diarios permitidos del usuario (módulo account_restrict_journal). Vacío: todos
    allowed_journal_ids: list[int] = []
    company: Company = Company()  # encabezado de la factura impresa
