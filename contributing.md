# Como contribuir

## Setup

Se necesita tener Python instalado, idealmente 3.10 o superior.

```bash
# Se crea un entorno virtual de desarrollo
python -m venv .venv

# Se activa el entorno virtual (cada vez)
# [MacOS/Linux]
source .venv/bin/activate
# [Windows]
.venv\Scripts\activate.bat

# Se instalan las dependencias
pip install -r requirements.txt

# Correr el servidor
python -m uvicorn src.app:app --reload
```

