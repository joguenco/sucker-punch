"""Lee y guarda la configuración de la app.

Cada dato se busca primero en las variables de entorno del sistema y, si no está, en el
archivo .env. Si no está en ninguno se usa el valor por defecto. Configuración solo
escribe en el .env, nunca en las variables del sistema.

El .env va junto al .exe cuando la app está compilada con PyInstaller, y en la raíz del
proyecto cuando se ejecuta con `uv run sucker-punch`. Está en .gitignore: la clave API
nunca termina en git.
"""

import os
import sys
from pathlib import Path

from ..models.settings import (
    FONT_SIZE_MAX,
    FONT_SIZE_MIN,
    FROM_DEFAULT,
    FROM_ENV_FILE,
    FROM_SYSTEM,
    Settings,
)

# Campo de Settings → nombre de la variable de entorno y de la línea en el .env
VARIABLES = {
    'url': 'ODOO_URL',
    'database': 'ODOO_DB',
    'api_key': 'ODOO_API_KEY',
    'font_size': 'FONT_SIZE',
    'stock_warning': 'STOCK_WARNING',
}


def to_bool(value) -> bool:
    """1, true, sí… = encendido; 0, false, no, off = apagado (otra cosa: encendido)."""
    if isinstance(value, bool):
        return value
    return value.strip().lower() not in ('0', 'false', 'no', 'off')


def to_text(value) -> str:
    """Cómo se escribe cada dato en el .env (sí/no como 1/0)."""
    if isinstance(value, bool):
        return '1' if value else '0'
    return str(value)


def env_file_path() -> Path:
    if getattr(sys, 'frozen', False):  # .exe de PyInstaller
        return Path(sys.executable).parent / '.env'
    # src/sucker_punch/services/settings_service.py → raíz del proyecto
    return Path(__file__).resolve().parents[3] / '.env'


def _line_name(line: str) -> str:
    """Nombre de una línea NOMBRE=valor ('' si es vacía o un comentario)."""
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        return ''
    return line.split('=', 1)[0].removeprefix('export ').strip()


def read_env_file(path: Path) -> dict[str, str]:
    values = {}
    if path.is_file():
        # utf-8-sig: el Bloc de notas a veces guarda con BOM al inicio
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if name := _line_name(line):
                values[name] = line.split('=', 1)[1].strip().strip('\'"')
    return values


def write_env_file(path: Path, values: dict[str, str]):
    """Cambia o agrega las líneas NOMBRE=valor sin tocar las demás ni los comentarios."""
    lines = path.read_text(encoding='utf-8-sig').splitlines() if path.is_file() else []
    pending = dict(values)
    for index, line in enumerate(lines):
        if (name := _line_name(line)) in pending:
            lines[index] = f'{name}={pending.pop(name)}'
    lines += [f'{name}={value}' for name, value in pending.items()]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


class SettingsService:
    def __init__(self, path: Path | None = None):
        self.path = path or env_file_path()

    def load(self) -> Settings:
        file_values = read_env_file(self.path)
        default = Settings()
        values, sources = {}, {}
        for field, name in VARIABLES.items():
            if os.environ.get(name, '').strip():
                values[field] = os.environ[name].strip()
                sources[field] = FROM_SYSTEM
            elif file_values.get(name):
                values[field] = file_values[name]
                sources[field] = FROM_ENV_FILE
            else:
                values[field] = getattr(default, field)
                sources[field] = FROM_DEFAULT if values[field] else ''
        try:
            font_size = int(values['font_size'])
        except ValueError:
            font_size = default.font_size
        values['font_size'] = min(max(font_size, FONT_SIZE_MIN), FONT_SIZE_MAX)
        values['stock_warning'] = to_bool(values['stock_warning'])
        return Settings(**values, sources=sources)

    def save(self, settings: Settings):
        """Escribe en el .env lo que no viene del sistema. Si no existe, lo crea."""
        write_env_file(
            self.path,
            {
                name: to_text(getattr(settings, field))
                for field, name in VARIABLES.items()
                if not settings.is_from_system(field)
            },
        )
