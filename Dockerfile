# Usamos una imagen base de Python 3.12
FROM python:3.12-slim

# Instalar dependencias del sistema, incluyendo PortAudio y herramientas necesarias para pyaudio, se necesita en whisper
# --------------------------------------------
#RUN apt-get update && apt-get install -y \
#    portaudio19-dev \
#    python3-dev \
#    gcc \
#    g++ \
#    && rm -rf /var/lib/apt/lists/*
# --------------------------------------------


# Crear y definir el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt


# Comando para ejecutar tu aplicación en render
#CMD ["python", "app.py"]

#Para huggingface

ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=7860

# Ejecutar el comando para iniciar Flask
CMD ["flask", "run"]