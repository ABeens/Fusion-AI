from flask import Flask, Blueprint, request
from flask_restx import Api, Resource
from services.process.input_to_text import transcribe_audio
import os
import tempfile

app = Flask(__name__)
api = Api(app, version='1.0', title='API de Transcripción',
          description='Una API para la transcripción de audio')

transcribe_bp = Blueprint('transcribe_bp', __name__)

class Transcribir(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No se recibió ningún archivo"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "Nombre de archivo vacío"}, 400

        try:
            # Crear un archivo temporal con permisos
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                filepath = temp_file.name
                file.save(filepath)
            
            # Procesar la transcripción
            resultado = transcribe_audio(filepath)
        except Exception as e:
            return {"error": f"Error al procesar el audio: {str(e)}"}, 500
        finally:
            # Asegurarse de eliminar el archivo temporal
            if 'filepath' in locals() and os.path.exists(filepath):
                os.unlink(filepath)

        return {"transcripcion": resultado}

api.add_resource(Transcribir, '/transcribe')
app.register_blueprint(transcribe_bp)

if __name__ == '__main__':
    app.run(debug=True)