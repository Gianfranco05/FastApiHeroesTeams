# 1. Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# 3. Copiar solo el archivo de requerimientos primero
# (Esto optimiza el caché de Docker para que las construcciones sean más rápidas)
COPY ./requirements.txt /code/requirements.txt

# 4. Instalar las dependencias de tu proyecto
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiar toda la carpeta 'app' con tu código fuente
COPY ./app /code/app

# 6. Comando de arranque a prueba de fallos para la nube
# Usamos uvicorn directamente y le decimos que escuche en 0.0.0.0
# Usamos la variable $PORT que Railway inyecta automáticamente, o 8000 por defecto
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}