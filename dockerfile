# Usar una imagen oficial de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que la aplicación se ejecutará
# Render asignará un puerto dinámicamente, Gunicorn lo usará.
EXPOSE 10000

# Comando para ejecutar la aplicación usando Gunicorn
# Esta sintaxis (shell form) permite la sustitución de variables de entorno como ${PORT}
CMD gunicorn --bind 0.0.0.0:${PORT} app:app