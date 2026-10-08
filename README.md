# sucker-punch
XML RPC Client for Point of Sale

## Project created with uv
```
uv init
```
## Create python virtual environment
```
virtualenv .venv
```
or
```
virtualenv -p python3.12 .venv
```
or
```
python3.12 -m venv .venv
```
## Activate python virtual environment
```
source .venv/bin/activate
```
or
```
. .venv/bin/activate
```

## Update pip and tools
```
pip install -U pip
pip install --upgrade wheel
pip install --upgrade setuptools
```
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

