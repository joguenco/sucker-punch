from pydantic import BaseModel, Field

FONT_SIZE_MIN = 10
FONT_SIZE_MAX = 24

# De dónde salió cada dato (se muestra en Configuración)
FROM_SYSTEM = 'Sistema'
FROM_ENV_FILE = '.env'
FROM_DEFAULT = 'Por defecto'


class Settings(BaseModel):
    """Configuración de la app: conexión a Odoo y tamaño de letra."""

    # 127.0.0.1 y no localhost: en Windows localhost prueba IPv6 primero y cada llamada
    # tardaba 15 segundos
    url: str = 'http://127.0.0.1:8019'
    database: str = 'odoo19_ec'
    api_key: str = ''
    font_size: int = 14
    # Al guardar, avisar si un producto no tiene stock (apagado: se vende igual y en
    # Odoo el stock queda en negativo)
    stock_warning: bool = True
    # campo → FROM_SYSTEM, FROM_ENV_FILE o FROM_DEFAULT ('' si no está en ningún lado)
    sources: dict[str, str] = Field(default_factory=dict)

    @property
    def is_complete(self) -> bool:
        return bool(self.url and self.database and self.api_key)

    def is_from_system(self, field: str) -> bool:
        return self.sources.get(field) == FROM_SYSTEM
