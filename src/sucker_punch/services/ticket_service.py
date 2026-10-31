"""Factura impresa: arma los datos de la venta, llena la plantilla XML y la lee.

La plantilla tiene el formato de Printer.Ticket.xml de DonPos (etiquetas ticket, line,
text, cut y opendrawer), con los datos en sintaxis Jinja2. La que viene con la app está
en templates/factura.xml; si hay un factura.xml junto al .env, se usa ese.
"""

import platform
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, TemplateError

from ..models.company import Company
from ..models.customer import FINAL_CONSUMER_VAT, Customer
from ..models.payment import METHODS, Payment
from ..models.sale_line import SaleLine
from ..models.sale_result import SaleResult
from ..models.session import Session
from ..models.ticket import (
    PrintLine,
    Printout,
    PrintText,
    Ticket,
    TicketLine,
    TicketPayment,
)
from .odoo_totals import money
from .settings_service import env_file_path

TEMPLATE = Path(__file__).resolve().parents[1] / 'templates' / 'factura.xml'
TEMPLATE_NAME = 'factura.xml'


class TicketError(Exception):
    """La plantilla de la factura tiene un error."""


def template_path() -> Path:
    """factura.xml junto al .env si existe; si no, la plantilla de la app."""
    custom = env_file_path().parent / TEMPLATE_NAME
    return custom if custom.is_file() else TEMPLATE


def quantity_text(value: float) -> str:
    """Cantidad sin ceros de más: 1 → '1', 1.5 → '1.5', 0.25 → '0.25'."""
    return f'{value:.3f}'.rstrip('0').rstrip('.')


def build_ticket(
    lines: list[SaleLine],
    totals: dict,
    customer: Customer,
    payment: Payment,
    result: SaleResult,
    session: Session,
) -> Ticket:
    """Los datos de una venta ya guardada en Odoo, para la plantilla."""
    company = (
        session.company if session.company.name else Company(name=session.company_name)
    )
    return Ticket(
        company=company,
        number=result.number or result.invoice,
        access_key=result.access_key,
        date=datetime.now().astimezone(),
        customer=customer,
        lines=[
            TicketLine(
                code=line.product.barcode or line.product.default_code,
                name=line.product.name,
                quantity=line.quantity,
                price=money(line.price * (1 + line.product.tax_percent / 100)),
                total=money(line.subtotal + line.tax),
                taxed=bool(line.product.tax_percent),
            )
            for line in lines
        ],
        rate_0=totals['rate_0'],
        rate_vat=totals['rate_vat'],
        vat=totals['vat'],
        total=totals['total'],
        cash=payment.cash,
        change=payment.change,
        payments=[
            TicketPayment(name=METHODS[method], amount=amount)
            for method, amount in payment.amounts().items()
            if method != 'cash'
        ],
        user=session.user_name,
        terminal=platform.node(),
    )


def sample_ticket() -> Ticket:
    """Factura de ejemplo para Configuración → Probar impresora."""
    return Ticket(
        company=Company(
            business_name='PRUEBA DE IMPRESORA',
            name='Empresa de ejemplo',
            vat='0000000000001',
            address='Dirección de ejemplo',
            forced_accounting='SI',
            environment='Pruebas',
        ),
        number='000-000-000000000',
        access_key='0' * 49,
        date=datetime.now().astimezone(),
        customer=Customer(
            vat=FINAL_CONSUMER_VAT, id_type='final', name='CONSUMIDOR FINAL'
        ),
        lines=[
            TicketLine(
                code='0001',
                name='PRODUCTO DE EJEMPLO CON NOMBRE LARGO',
                quantity=2,
                price=1.15,
                total=2.30,
                taxed=True,
            ),
            TicketLine(
                code='0002', name='PAN', quantity=1, price=0.25, total=0.25, taxed=False
            ),
        ],
        rate_0=0.25,
        rate_vat=2.00,
        vat=0.30,
        total=2.55,
        cash=3.00,
        change=0.45,
        user='Ejemplo',
        terminal=platform.node(),
    )


def render(ticket: Ticket, path: Path | None = None) -> Printout:
    """Llena la plantilla con los datos de la factura y la lee línea por línea."""
    path = path or template_path()
    environment = Environment(autoescape=True, trim_blocks=True, lstrip_blocks=True)
    environment.filters['money'] = lambda value: f'{value:.2f}'
    environment.filters['qty'] = quantity_text
    try:
        source = path.read_text(encoding='utf-8-sig')
        xml = environment.from_string(source).render(
            ticket=ticket, company=ticket.company
        )
    except OSError as error:
        raise TicketError(f'No se pudo leer la plantilla {path}.\n\n{error}') from None
    except TemplateError as error:
        line = getattr(error, 'lineno', None)
        where = f', línea {line}' if line else ''
        raise TicketError(
            f'La plantilla {path.name} tiene un error{where}:\n{error}'
        ) from None
    try:
        return parse(xml)
    except ET.ParseError as error:
        raise TicketError(
            f'La plantilla {path.name} no es un XML válido después de llenarla:\n{error}'
        ) from None


def align(text: str, position: str, length: int | None) -> str:
    """Como DonPos: el texto se corta o se rellena con espacios hasta ese largo."""
    if length is None:
        return text
    text = text[:length]
    if position == 'right':
        return text.rjust(length)
    if position == 'center':
        return text.center(length)
    return text.ljust(length)


def parse(xml: str) -> Printout:
    """Lee el XML ya llenado: <ticket> con <line>, <text> y <cut/>, y <opendrawer/>."""
    root = ET.fromstring(xml.strip())
    printout = Printout(open_drawer=root.find('.//opendrawer') is not None)
    for ticket in root.iter('ticket'):
        for element in ticket:
            if element.tag == 'cut':
                printout.lines.append(PrintLine(cut=True))
            elif element.tag == 'line':
                texts = []
                for part in element.iter('text'):
                    length = part.get('length')
                    texts.append(
                        PrintText(
                            text=align(
                                part.text or '',
                                part.get('align', 'left'),
                                int(length) if length else None,
                            ),
                            bold=part.get('bold') == 'true',
                            underline=part.get('underline') == 'true',
                        )
                    )
                size = element.get('size', '0')
                printout.lines.append(
                    PrintLine(texts=texts, size=int(size) if size.isdigit() else 0)
                )
            # image y barcode de DonPos todavía no se imprimen
    return printout
