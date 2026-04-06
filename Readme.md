### 0) Levantar Base de Datos con docker compose

docker compose up -d

## Ejecución local

### 1) Crear entorno virtual (se desactiva con: deactivate)

**Linux / macOS**
python3 -m venv .venv
**Windows (PowerShell)**
py -m venv .venv

### 2) Activar entorno virtual

**Linux / macOS**
source .venv/bin/activate
**Windows (PowerShell)**
.\.venv\Scripts\Activate.ps1
**Windows (CMD)**
.\.venv\Scripts\activate.bat

### 3) Actualizar pip e instalar dependencias

python -m pip install --upgrade pip
pip install -r requirements.txt

### 4) Ejecutar Servidor

python -m fastapi dev app/main.py
