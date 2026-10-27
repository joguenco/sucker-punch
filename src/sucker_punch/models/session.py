from pydantic import BaseModel


class Session(BaseModel):
    """Usuario que entró a la app y su empresa en Odoo."""

    uid: int
    user_name: str
    company_name: str
    country_code: str = ''  # 'EC' con la localización de Ecuador
    # Cómo redondea Odoo el IVA: round_per_line o round_globally (ver odoo_totals.py)
    tax_rounding: str = 'round_per_line'
