from flask import Flask, Blueprint, request
from flask_restx import Api, Resource
from services.process.feelings_validator import validate_sentiment
from services.process.input_to_text import transcribe_audio
import os
import tempfile

#os.environ["TRANSFORMERS_CACHE"] = "/tmp/hf_cache"
#os.makedirs("/tmp/hf_cache", exist_ok=True)
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
            transcription = transcribe_audio(filepath)
            feeling=validate_sentiment(transcription)
            resultado = {
                "transcripcion": transcription,
                "sentimiento": feeling
            }
        except Exception as e:
            return {"error": f"Error al procesar el audio: {str(e)}"}, 500
        finally:
            # Asegurarse de eliminar el archivo temporal
            if 'filepath' in locals() and os.path.exists(filepath):
                os.unlink(filepath)

        return resultado

api.add_resource(Transcribir, '/transcribe')
app.register_blueprint(transcribe_bp)

if __name__ == '__main__':
    app.run(debug=True)