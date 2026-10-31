"""Factura impresa: los datos que ve la plantilla (templates/factura.xml) y lo que sale de
leerla, línea por línea, para la impresora o la pantalla."""

from datetime import datetime

from pydantic import BaseModel

from .company import Company
from .customer import Customer

ACCESS_KEY_LENGTH = 49
ACCESS_KEY_SPLIT = 39  # como DonPos: 39 dígitos en una línea y los 10 que sobran en otra


class TicketLine(BaseModel):
    """Una línea de la factura impresa. Precio y valor con IVA, como en DonPos."""

    code: str
    name: str
    quantity: float
    price: float  # precio unitario con IVA
    total: float  # valor de la línea con IVA
    taxed: bool  # el producto tiene IVA


class TicketPayment(BaseModel):
    name: str  # Tarjeta, Depósito / Transferencia u Otros
    amount: float


class Ticket(BaseModel):
    """Lo que la plantilla puede poner en la factura impresa."""

    company: Company
    number: str  # ej. 001-001-000000012
    access_key: str = ''  # clave de acceso del SRI
    date: datetime
    customer: Customer
    lines: list[TicketLine]
    # Totales como en la pantalla del Punto de Venta
    rate_0: float  # base con IVA 0 %
    rate_vat: float  # base con IVA
    vat: float
    total: float
    cash: float = 0.0  # efectivo entregado
    change: float = 0.0
    payments: list[TicketPayment] = []  # las demás formas de pago
    user: str = ''  # atendido por
    terminal: str = ''  # nombre de la computadora

    @property
    def access_key_line1(self) -> str:
        if len(self.access_key) != ACCESS_KEY_LENGTH:
            return ''
        return self.access_key[:ACCESS_KEY_SPLIT]

    @property
    def access_key_line2(self) -> str:
        if len(self.access_key) != ACCESS_KEY_LENGTH:
            return ''
        return self.access_key[ACCESS_KEY_SPLIT:]

    @property
    def quantity(self) -> float:
        """Cantidad de productos (suma de las cantidades)."""
        return sum(line.quantity for line in self.lines)


class PrintText(BaseModel):
    """Un pedazo de una línea: el texto ya alineado y con su largo."""

    text: str
    bold: bool = False
    underline: bool = False


class PrintLine(BaseModel):
    """Una línea del papel. size: 0 normal, 1 doble alto, 2 doble ancho, 3 los dos."""

    texts: list[PrintText] = []
    size: int = 0
    cut: bool = False  # aquí se corta el papel

    @property
    def text(self) -> str:
        return ''.join(part.text for part in self.texts)


class Printout(BaseModel):
    """La factura lista para imprimir o mostrar en pantalla."""

    lines: list[PrintLine] = []
    # La plantilla pide abrir el cajón. Todavía no se manda a la impresora: hoy lo abre
    # el driver de la impresora, si está configurado así
    open_drawer: bool = False
