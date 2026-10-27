from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Product(BaseModel):
    """Un registro de product.product tal como lo devuelve search_read."""

    model_config = ConfigDict(populate_by_name=True)

    # Campos que se le piden a Odoo (product.product hereda los de product.template)
    FIELDS: ClassVar[tuple] = (
        'id',
        'display_name',
        'barcode',
        'default_code',
        'lst_price',
        'uom_id',
        'qty_available',
        'is_storable',
        'taxes_id',
    )

    id: int
    name: str = Field(alias='display_name')
    barcode: str = ''
    default_code: str = ''
    price: float = Field(0.0, alias='lst_price')
    uom: str = Field('', alias='uom_id')
    stock: float = Field(0.0, alias='qty_available')
    is_storable: bool = False  # «Seguimiento de inventario»: si no, el stock siempre es 0
    tax_ids: list[int] = Field(default_factory=list, alias='taxes_id')
    # Los llena ProductService: % de cada impuesto ({id: 15.0}) y la suma
    tax_rates: dict[int, float] = Field(default_factory=dict)
    tax_percent: float = 0.0

    @field_validator('barcode', 'default_code', mode='before')
    @classmethod
    def empty_if_false(cls, value):
        # Odoo devuelve False cuando un campo de texto está vacío
        return '' if value is False else value

    @field_validator('uom', mode='before')
    @classmethod
    def many2one_name(cls, value):
        # Los many2one llegan como [id, "Nombre"] o False
        if isinstance(value, (list, tuple)):
            return value[1]
        return value or ''

    @property
    def code(self) -> str:
        return self.barcode or self.default_code
