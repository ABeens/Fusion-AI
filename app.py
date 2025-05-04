from flask import Flask, Blueprint, jsonify, request
from flask_restx import Api, Resource, reqparse
from services.process.input_to_text import transcribe_audio
import os
from config import AUDIO_FILENAME

# Crear la aplicación Flask
app = Flask(__name__)

# Crear la API Flask-RESTX
api = Api(app, version='1.0', title='API de Transcripción',
          description='Una API para la transcripción de audio')

# Crear el Blueprint
transcribe_bp = Blueprint('transcribe_bp', __name__)

# Crear la clase de recursos para Flask-RESTX
class Transcribir(Resource):
    def post(self):
        # Obtener el archivo de la solicitud
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "No se recibió ningún archivo"}), 400

        # Guardar el archivo temporalmente
        filepath = "temp_audio.wav"
        file.save(filepath)

        # Procesar la transcripción del audio
        resultado = transcribe_audio(filepath)

        # Eliminar archivo temporal después de procesar
        os.remove(filepath)

        # Devolver la transcripción en formato JSON
        return jsonify({"transcripcion": resultado})

# Registrar la clase de recursos en la API
api.add_resource(Transcribir, '/transcribe')

# Registrar el Blueprint en la app (si deseas usar blueprints)
app.register_blueprint(transcribe_bp)

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    app.run(debug=True)
