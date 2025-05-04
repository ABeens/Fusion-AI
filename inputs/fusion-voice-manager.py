import speech_recognition as sr

# Crear el reconocedor
r = sr.Recognizer()

# Usar el micrófono
with sr.Microphone() as source:
    print("Habla ahora...")
    audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Has dicho: " + texto)
    except sr.UnknownValueError:
        print("No se entendió lo que dijiste.")
    except sr.RequestError as e:
        print(f"Error de conexión: {e}")
