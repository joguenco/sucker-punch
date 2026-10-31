from pydantic import BaseModel, field_validator


class Company(BaseModel):
    """Empresa del usuario: lo que sale en el encabezado de la factura impresa."""

    name: str = ''  # razón social
    business_name: str = ''  # nombre comercial
    vat: str = ''  # RUC
    address: str = ''
    phone: str = ''
    email: str = ''
    # Leyendas del SRI (localización de Ecuador); vacías si no aplican
    regimen: str = ''  # ej. CONTRIBUYENTE RÉGIMEN RIMPE
    retention_agent: str = ''  # resolución de agente de retención
    forced_accounting: str = ''  # obligado a llevar contabilidad: SI o NO
    environment: str = ''  # ambiente del SRI: Pruebas o Producción

    @field_validator('*', mode='before')
    @classmethod
    def empty_if_false(cls, value):
        # Odoo devuelve False cuando un campo de texto está vacío
        return '' if value is False else value
