"""Clientes de la factura (res.partner): buscar por identificación, crear y actualizar.

Al crear, Odoo valida la identificación: el RUC en base_vat, la cédula en l10n_ec y las
excepciones del módulo l10n_ec_base. Si no es válida responde con error y no se crea.
El Consumidor Final no se puede modificar (l10n_ec_base lo bloquea a quien no es admin).
"""

from ..models.customer import FINAL_CONSUMER_VAT, Customer
from .odoo_client import OdooClient

FINAL_CONSUMER_NAME = 'CONSUMIDOR FINAL'
# El SRI no deja facturar más de este total a Consumidor Final (parámetro de Odoo
# l10n_ec_final_consumer_limit, 50 por defecto)
FINAL_CONSUMER_LIMIT = 50.0

# Tipo de identificación de la app → registro de Odoo (módulo, id XML)
ID_TYPE_XMLIDS = {
    'final': ('l10n_ec', 'ec_ruc'),  # Consumidor Final: tipo RUC con 9999999999999
    'cedula': ('l10n_ec', 'ec_dni'),
    'ruc': ('l10n_ec', 'ec_ruc'),
    'passport': ('l10n_latam_base', 'it_pass'),
}
FIELDS = ['vat', 'name', 'email', 'street', 'l10n_latam_identification_type_id']


def guess_id_type(vat: str) -> str:
    """Tipo según el número: 13 nueves Consumidor Final, 10 dígitos cédula, 13 RUC."""
    if vat == FINAL_CONSUMER_VAT:
        return 'final'
    if vat.isdigit() and len(vat) == 10:
        return 'cedula'
    if vat.isdigit() and len(vat) == 13:
        return 'ruc'
    return 'passport'


def is_valid_cedula(vat: str) -> bool:
    """Dígito verificador de la cédula (módulo 10), el mismo cálculo que hace Odoo."""
    if len(vat) != 10 or not vat.isdigit():
        return False
    if not (1 <= int(vat[:2]) <= 24 or vat[:2] in ('30', '50')) or int(vat[2]) >= 6:
        return False
    total = 0
    for digit, weight in zip(vat[:9], (2, 1) * 5):
        product = int(digit) * weight
        total += product - 9 if product > 9 else product
    return (10 - total % 10) % 10 == int(vat[9])


def check_new_customer(customer: Customer) -> tuple[str, str]:
    """Revisa los datos antes de crear el cliente: (campo con error, mensaje)."""
    vat, kind = customer.vat, customer.id_type
    if kind == 'cedula' and (len(vat) != 10 or not vat.isdigit()):
        return 'vat', 'La cédula debe tener 10 números.'
    if kind == 'ruc' and (len(vat) != 13 or not vat.isdigit()):
        return 'vat', 'El RUC debe tener 13 números.'
    if kind == 'passport' and len(vat) < 3:
        return 'vat', 'Escribe el número de pasaporte.'
    return check_contact(customer)


def check_contact(customer: Customer) -> tuple[str, str]:
    """Revisa la Razón Social y el email (al crear o al actualizar el cliente)."""
    if not customer.name.strip():
        return 'name', 'Falta la Razón Social.'
    email = customer.email.strip()
    if email and ('@' not in email or '.' not in email.split('@')[-1]):
        return 'email', 'El email no es válido.'
    return '', ''


class CustomerService:
    def __init__(self, odoo: OdooClient):
        self.odoo = odoo
        self._type_ids = None  # {'cedula': id en Odoo, ...}
        self._country_id = None

    def _types(self) -> dict[str, int]:
        if self._type_ids is None:
            model = 'l10n_latam.identification.type'
            ids = self.odoo.call(model, 'search', domain=[])
            xmlids = self.odoo.call(model, 'get_external_id', ids=ids)
            by_xmlid = {
                tuple(xmlid.split('.', 1)): int(type_id)
                for type_id, xmlid in xmlids.items()
                if xmlid
            }
            self._type_ids = {
                kind: by_xmlid.get(xmlid, 0) for kind, xmlid in ID_TYPE_XMLIDS.items()
            }
        return self._type_ids

    def _ecuador(self) -> int | bool:
        if self._country_id is None:
            ids = self.odoo.call(
                'res.country', 'search', domain=[['code', '=', 'EC']], limit=1
            )
            self._country_id = ids[0] if ids else False
        return self._country_id

    def _to_customer(self, row: dict) -> Customer:
        vat = row['vat'] or ''
        type_id = (row['l10n_latam_identification_type_id'] or [0])[0]
        kinds = [k for k, v in self._types().items() if v == type_id and k != 'final']
        if vat == FINAL_CONSUMER_VAT:
            kind = 'final'
        elif kinds:
            kind = kinds[0]
        else:
            kind = guess_id_type(vat)
        return Customer(
            id=row['id'],
            vat=vat,
            id_type=kind,
            name=row['name'],
            email=row['email'],
            street=row['street'],
        )

    def find(self, vat: str) -> Customer | None:
        """El cliente con esa identificación, o None si no existe en Odoo."""
        rows = self.odoo.call(
            'res.partner',
            'search_read',
            # parent_id vacío: la empresa, no sus contactos (que comparten el RUC)
            domain=[['vat', '=', vat], ['parent_id', '=', False]],
            fields=FIELDS,
            order='id',
            limit=1,
        )
        return self._to_customer(rows[0]) if rows else None

    def final_consumer(self) -> Customer:
        """El Consumidor Final de Odoo; si no existe, lo crea."""
        return self.find(FINAL_CONSUMER_VAT) or self.create(
            Customer(vat=FINAL_CONSUMER_VAT, id_type='final', name=FINAL_CONSUMER_NAME)
        )

    def create(self, customer: Customer) -> Customer:
        new_id = self.odoo.call(
            'res.partner',
            'create',
            vals_list=[
                {
                    'name': customer.name.strip(),
                    'vat': customer.vat,
                    'l10n_latam_identification_type_id': (
                        self._types().get(customer.id_type) or False
                    ),
                    'email': customer.email.strip() or False,
                    'street': customer.street.strip() or False,
                    'country_id': self._ecuador(),
                }
            ],
        )[0]
        return customer.model_copy(update={'id': new_id})

    def update(self, customer: Customer, changes: dict[str, str]):
        """Guarda en Odoo los datos que se corrigieron (name, email o street)."""
        self.odoo.write(
            'res.partner',
            [customer.id],
            {field: value.strip() or False for field, value in changes.items()},
        )
