# Imagen base de Python 3.12
FROM python:3.12-slim

# Establecer variables de entorno para cache y Flask
ENV TRANSFORMERS_CACHE=/tmp/hf_cache
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=7860

# Crear carpeta para cache de modelos y dar permisos globales
RUN mkdir -p /tmp/hf_cache && chmod -R 777 /tmp/hf_cache

# Crear y definir el directorio de trabajo
WORKDIR /app

# Copiar el código fuente
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Descargar el modelo en build-time para evitar errores en runtime
RUN python -c "\
from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment'); \
AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')"

# Comando por defecto al ejecutar el contenedor
CMD ["flask", "run"]
