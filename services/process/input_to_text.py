import speech_recognition as sr

def transcribe_audio(filename):
    r = sr.Recognizer()

    try:
        # Usamos el archivo de audio para realizar la transcripción
        with sr.AudioFile(filename) as source:
            audio = r.record(source)  # Captura todo el contenido del audio

        # Intentamos realizar el reconocimiento de voz
        texto = r.recognize_google(audio, language="es-ES")
        print("Has dicho: " + texto)
        return texto  # Retornamos la transcripción
    except sr.UnknownValueError:
        print("No se entendió lo que dijiste.")
        return "Error: No se entendió lo que dijiste."  # Mensaje de error específico
    except sr.RequestError as e:
        print(f"Error de conexión: {e}")
        return f"Error: No se pudo conectar con el servicio de transcripción ({e})"  # Error de conexión
