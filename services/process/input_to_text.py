import speech_recognition as sr


def transcribe_audio(filename):
    r = sr.Recognizer()
    #audio = r.listen(filename)
    with sr.AudioFile(filename) as source:
        audio = r.record(source) 

    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Has dicho: " + texto)
    except sr.UnknownValueError:
        print("No se entendió lo que dijiste.")
    except sr.RequestError as e:
        print(f"Error de conexión: {e}")
    return texto