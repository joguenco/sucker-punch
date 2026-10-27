"""Cliente de la API externa JSON-2 de Odoo (19 y 20).

Cada llamada es un POST a /json/2/<modelo>/<método>, autenticado con una clave API en la
cabecera Authorization. Los argumentos van siempre con nombre (domain=..., fields=...).
"""

import requests

from ..models.session import Session
from ..models.settings import Settings


class OdooError(Exception):
    """Error devuelto por Odoo o problema de conexión."""


class OdooClient:
    def __init__(self, settings: Settings, timeout: int = 15):
        self.url = settings.url.rstrip('/')
        self.database = settings.database
        self.timeout = timeout
        self.context = {}
        self.http = requests.Session()
        self.http.headers.update(
            {
                'Authorization': f'bearer {settings.api_key}',
                'X-Odoo-Database': settings.database,
                'User-Agent': 'sucker-punch',
            }
        )

    def _no_connection(self):
        return OdooError(f'No se pudo conectar a {self.url}. ¿Odoo está arrancado?')

    def version(self) -> str:
        try:
            response = self.http.get(f'{self.url}/web/version', timeout=self.timeout)
            return response.json()['version']
        except (requests.RequestException, ValueError, KeyError):
            raise self._no_connection() from None

    def call(self, model: str, method: str, ids: list | None = None, **kwargs):
        """Llama a cualquier método público de un modelo de Odoo."""
        body = dict(kwargs)
        if ids is not None:
            body['ids'] = ids
        if self.context:
            body.setdefault('context', self.context)
        try:
            response = self.http.post(
                f'{self.url}/json/2/{model}/{method}', json=body, timeout=self.timeout
            )
        except requests.RequestException:
            raise self._no_connection() from None
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            raise OdooError(
                'La clave API no es válida o ya venció (revisa Configuración).'
            )
        try:
            message = response.json().get('message', response.text)
        except ValueError:
            message = response.text[:300]
        raise OdooError(f'{model}.{method}: {message}')

    def write(self, model: str, ids: list[int], vals: dict):
        """write: el Update del CRUD.

        JSON-2 pasa los datos con el nombre que usa la última versión de write. Odoo lo
        llama «vals», pero un módulo puede renombrarlo (l10n_ec_base usa «values» en
        res.partner): si Odoo pide «values», se vuelve a mandar con ese nombre.
        """
        try:
            return self.call(model, 'write', ids=ids, vals=vals)
        except OdooError as error:
            if "argument: 'values'" not in str(error):
                raise
            return self.call(model, 'write', ids=ids, values=vals)

    def login(self, user: str, password: str) -> Session:
        """Valida usuario y contraseña, y que la clave API sea de ese mismo usuario.

        JSON-2 no acepta usuario/contraseña, así que la contraseña se valida con
        /web/session/authenticate (ruta jsonrpc del cliente web, no deprecada).
        """
        try:
            response = requests.post(
                f'{self.url}/web/session/authenticate',
                timeout=self.timeout,
                json={
                    'jsonrpc': '2.0',
                    'method': 'call',
                    'params': {'db': self.database, 'login': user, 'password': password},
                },
            )
            data = response.json()
        except (requests.RequestException, ValueError):
            raise self._no_connection() from None
        uid = (data.get('result') or {}).get('uid')
        if 'error' in data or not uid:
            raise OdooError('Usuario o contraseña incorrectos.')

        context = self.call('res.users', 'context_get')
        if context.get('uid') != uid:
            raise OdooError('La clave API de Configuración pertenece a otro usuario.')
        self.context = {'lang': context.get('lang'), 'tz': context.get('tz')}

        odoo_user = self.call(
            'res.users', 'read', ids=[uid], fields=['name', 'company_id']
        )[0]
        company = self.call(
            'res.company',
            'read',
            ids=[odoo_user['company_id'][0]],
            fields=['country_code', 'tax_calculation_rounding_method'],
        )[0]
        return Session(
            uid=uid,
            user_name=odoo_user['name'],
            company_name=odoo_user['company_id'][1],
            country_code=company['country_code'] or '',
            tax_rounding=company['tax_calculation_rounding_method'] or 'round_per_line',
        )
