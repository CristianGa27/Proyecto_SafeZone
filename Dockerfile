# Usar la imagen oficial de Python
FROM python:3.10-slim

# Evitar que Python escriba archivos .pyc y activar el log de errores al instante
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer la carpeta donde trabajará el contenedor
WORKDIR /app

# Instalar dependencias del sistema requeridas para mysql y compilación
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo tu código fuente a la imagen Docker
COPY . /app/

# Ejecutar collectstatic y Gunicorn
# Render usa la variable de entorno $PORT para exponer tu app automáticamente
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn safezone_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
