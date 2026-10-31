# sucker-punch
JSON-2 API Client for Point of Sale

## Dependencies
- https://docs.astral.sh/uv/

## Project created with uv
```
uv init
```
## Create python virtual environment
```
uv venv
```
or
```
python3.14 -m venv .venv
```
## Activate python virtual environment
```
source .venv/bin/activate
```
or
```
. .venv/bin/activate
```
or on powershell
```
.venv\Scripts\Activate.ps1
```
## Install dependencies
```
uv sync
```
## Utilities
Util commands
### Add ruff
```
uv add --dev ruff
```
### Check syntax
```
ruff check
```
### Format
```
ruff format
```
## Run
```
uv run sucker-punch
```
## Designer
```
uvx --from pyside6-essentials pyside6-designer
```
## Structure Projects
📁 nombre_proyecto
│
├── 📁 assets                 # Recursos estáticos
│   ├── 📁 images             # Logos, íconos y gráficos (.png, .svg)
│   └── 📁 styles             # Hojas de estilo de Qt (.qss)
│
├── 📁 src                    # Código fuente principal de la aplicación
│   │
│   ├── 📁 models             # Modelos de datos y entidades de negocio
│   │   ├── __init__.py
│   │   └── cliente_model.py
│   │
│   ├── 📁 viewmodels         # Lógica de presentación y enlace de datos
│   │   ├── __init__.py
│   │   ├── base_viewmodel.py # Clase base con mecanismos de propiedades/señales
│   │   └── main_viewmodel.py
│   │
│   ├── 📁 views              # Interfaz de usuario (Componentes de PySide)
│   │   ├── 📁 ui             # Opcional: Archivos .ui de Qt Designer
│   │   │   └── main_window.ui
│   │   ├── __init__.py
│   │   └── main_view.py      # Clase de PySide (MainWindow) sin lógica de negocio
│   │
│   └── 📁 services           # Conectores y lógica externa (BD, APIs, Archivos)
│       ├── __init__.py
│       ├── database_service.py
│       └── config_service.py
│
├── .gitignore                # Archivos a ignorar en Git (__pycache__, venv)
├── .env                # Configuraciones globales de la app
├── main.py                   # Punto de entrada (Inicializa QApplication y las capas)
├── README.md                 # Documentación del proyecto
└── requirements.txt          # Dependencias (pyside6, etc.)


## Run
```
uv run sucker-punch
```
La primera vez pide **Configuración**: dirección de Odoo (`http://127.0.0.1:8019`), base de
datos, clave API (Odoo → Mis preferencias → Seguridad → Agregar clave API) y tamaño de letra.
Al guardar se crea el archivo `.env` (está en `.gitignore`, nunca se sube a git).

## Configuración (.env y variables de entorno)
Cada dato se busca en este orden y se usa el primero que se encuentre:
1. **Variable de entorno del sistema** (Windows o Linux).
2. **Archivo `.env`**: junto al `.exe` cuando está compilado con PyInstaller, o en la raíz
   del proyecto cuando se ejecuta con `uv run sucker-punch`.
3. Valor por defecto (la clave API no tiene).

| Variable | Dato | Por defecto |
|---|---|---|
| `ODOO_URL` | Dirección de Odoo | `http://127.0.0.1:8019` |
| `ODOO_DB` | Base de datos | `odoo19_ec` |
| `ODOO_API_KEY` | Clave API del usuario que vende (ej.: Caja) | — |
| `FONT_SIZE` | Tamaño de letra (10 a 24) | `14` |
| `STOCK_WARNING` | Avisar al guardar si no hay stock: `1` sí, `0` no (se vende igual y en Odoo el stock queda en negativo) | `1` |
| `PRINTER` | Impresora de Windows (o de Linux, CUPS) donde sale la factura al guardar; vacío: no imprime | — |
| `PRINTER_SIMULATE` | Simular impresora: `1` muestra la factura en pantalla como saldría impresa, sin imprimir | `0` |

Configuración muestra al lado de cada dato de dónde sale (**Sistema**, **.env** o
**Por defecto**) y solo escribe en el `.env`. Lo que viene del sistema queda bloqueado: se
cambia en las variables de entorno. Ejemplo en `.env.example`.

## Teclado (Punto de Venta)
| Tecla | Qué hace |
|---|---|
| Enter | Busca el código (o el nombre) y salta a una fila nueva |
| `5.CODIGO` o `5*CODIGO` + Enter | Cantidad 5 (sirve con escáner: escribir `5.` y escanear). Decimales: `1,5.CODIGO` o `1.5*CODIGO`. La cantidad debe ser mayor que 0 |
| F9 | Maestro de Artículos (inventario) |
| F2 | Cambiar el precio unitario de la línea (solo para esta factura). Enter cambia, Esc no |
| ↑ ↓ | Cambiar de línea |
| Shift+F6 | Borrar la línea; las de abajo suben |
| Ctrl+F | Buscar una línea dentro de la factura |
| Ctrl+L | Limpiar la factura (como recién abierta) |
| Ctrl+P | Reimprimir la última factura guardada |
| Ctrl+Enter | Guardar: abre **Pago Efectivo** y luego **Cambio** |

**Pago Efectivo**: Efectivo, Tarjeta, Depósito / Transferencia y Otros; se puede dividir.
Enter: si ya alcanza pasa a Cambio; si falta, salta a la siguiente forma con lo que falta.
El vuelto solo sale del efectivo. Esc vuelve a la factura.

**Cambio**: Valor, Pagado y Cambio, y el cliente (arranca en Consumidor Final). Enter en
Identificación lo busca en Odoo: si existe se llenan sus datos y el cursor va a Guardar; si
no, se escriben y se crea al guardar. Razón Social, Email y Dirección se pueden corregir:
al guardar se actualizan en Odoo (`res.partner` → `write`), solo lo que cambió. El
Consumidor Final no se edita. Más de $50 solo con cédula o RUC (regla del SRI).

## Factura impresa
Al guardar, si la factura quedó confirmada en Odoo, sale en la impresora de
Configuración, o en la ventana **Simulación de impresora** si está encendido Simular
impresora (Esc la cierra). Configuración → Probar impresora saca una factura de ejemplo.

El formato es una plantilla XML como `Printer.Ticket.xml` de DonPos:
`src/sucker_punch/templates/factura.xml` (etiquetas `ticket`, `line`, `text` con `align`,
`length` y `bold`, `cut` y `opendrawer`; los datos en sintaxis Jinja2, `{{ ... }}`). Para
cambiarla sin volver a compilar, se copia junto al `.env` con el nombre `factura.xml` y se
edita ahí: si existe, se usa esa.

La app solo imprime: no manda la orden de abrir el cajón (`<opendrawer/>` de la
plantilla todavía no se usa). Con impresoras de Windows, el corte del papel y el cajón
conectado a la impresora los hace su driver, si se configura en las preferencias de la
impresora (por ejemplo, abrir el cajón al imprimir).
Esc vuelve a Pago Efectivo. Al terminar sale «Compra realizada» (y si el cliente es nuevo
o se actualizó).

En Odoo cada pago se registra en el diario que tenga su **forma de pago SRI**
(Facturación → Configuración → Diarios): Efectivo `01`, Tarjeta `19`, Depósito y Otros `20`.
Si ningún diario la tiene, se usa el de Efectivo o el de Banco.

Los totales se calculan con el mismo redondeo que Odoo (`services/odoo_totals.py`, según
Facturación → Ajustes → Impuestos), así el total y el vuelto son los que factura Odoo. Un
producto sin impuesto de venta no entra a la factura (el SRI la rechaza), y el aviso de
stock solo sale en productos con seguimiento de inventario.

El usuario de la clave API (ej.: Caja) necesita en Odoo: Ventas, Inventario (validar la
entrega), Facturación (confirmar la factura y registrar pagos) y crear contactos.

## Views
Las pantallas se editan en Qt Designer (`views/ui/*.ui`); en `views/` no hay lógica.
Con `darkmode=0` Designer se ve claro, igual que la app (sin eso toma el modo oscuro de
Windows):
```
uv run pyside6-designer -platform windows:darkmode=0
```
Las columnas de la tabla del Punto de Venta se editan en Designer (título, orden,
alineación). Cada columna se reconoce por su nombre interno en la propiedad `whatsThis`:
`number`, `code`, `uom`, `name`, `quantity`, `price`, `discount`, `subtotal`, `tax`, `ice`.

Después de cambiar un `.ui`, regenerar su `ui_*.py` (no se editan a mano):
```
uv run pyside6-uic src/sucker_punch/views/ui/point_of_sale.ui -o src/sucker_punch/views/ui_point_of_sale.py
uv run ruff format src/sucker_punch/views/ui_point_of_sale.py
```

## Build (ejecutable con PyInstaller)
El ejecutable se arma en el mismo sistema donde se va a usar: el de Windows en Windows y
el de Linux en Linux. `build/`, `dist/` y `*.spec` están en `.gitignore`.

Una sola vez, en los dos sistemas (cerrar antes la app):
```
uv add --dev pyinstaller
```

### Windows
Armar (sale `dist\sucker-punch.exe`):
```
uv run pyinstaller main.py --onefile --windowed --name sucker-punch --icon src/sucker_punch/assets/images/icon.ico --add-data "src/sucker_punch/assets;sucker_punch/assets" --paths src --noconfirm
```
Usar: copiar `sucker-punch.exe` a una carpeta normal (ej. `C:\SuckerPunch\`, no en
`Program Files`) y abrirlo con doble clic. Configuración crea el `.env` al lado del `.exe`.
Si Windows avisa «Windows protegió su PC»: Más información → Ejecutar de todas formas.

### Linux (Ubuntu)
Qt necesita esta librería para abrir ventanas (una sola vez):
```
sudo apt install libxcb-cursor0
```
Armar (sale `dist/sucker-punch`, sin `.exe`). Cambia el separador de `--add-data` (`:` en
vez de `;`) y no lleva `--icon` (en Linux el ejecutable no tiene ícono; la ventana sí):
```
uv run pyinstaller main.py --onefile --windowed --name sucker-punch --add-data "src/sucker_punch/assets:sucker_punch/assets" --paths src --noconfirm
```
Usar: copiar `sucker-punch` a una carpeta (ej. `~/SuckerPunch/`) y abrirlo:
```
./sucker-punch
```
Configuración crea el `.env` al lado (en Linux es un archivo oculto: se ve con `ls -a`).
Armarlo en la versión de Ubuntu más antigua donde se vaya a usar.

En los dos sistemas la PC no necesita Python, y cada cambio en el código pide volver a
armar el ejecutable.
