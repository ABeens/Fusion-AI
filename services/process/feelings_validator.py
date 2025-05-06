from flask import jsonify
from transformers import pipeline
import os

# Configurar directorios de caché en una ubicación con permisos de escritura
#os.environ['TRANSFORMERS_CACHE'] = '/tmp/.cache'
#os.environ['HF_HOME'] = '/tmp/.cache'

# Asegurar que el directorio existe
#os.makedirs('/tmp/.cache', exist_ok=True)

# Inicializar el modelo de sentiment analysis
# Este modelo ya viene específicamente entrenado para sentimiento con 5 niveles
sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    # No necesitamos from_tf=True para este modelo específico ya que usa PyTorch por defecto
)

# Mapeo de sentimientos (este modelo ya devuelve estrellas directamente)
SENTIMENT_MAP = {
    '1 star': 'Muy Negativo',
    '2 stars': 'Negativo',
    '3 stars': 'Neutral',
    '4 stars': 'Positivo',
    '5 stars': 'Muy Positivo'
}

def validate_sentiment(texto):
    # El modelo devuelve una lista de diccionarios
    resultado = sentiment_classifier(texto)[0]  # Tomamos el primero porque solo analizamos un texto
    
    # Imprimir para depuración
    print(f"Resultado original: {resultado}")
    
    # Este modelo específico ya devuelve etiquetas como "1 star", "2 stars", etc.
    stars = resultado['label']
    confidence = resultado['score']
    
    return {
        "texto": texto,
        "stars": stars,
        "sentiment": SENTIMENT_MAP[stars],
        "confidence": round(confidence * 100, 2)
    }
