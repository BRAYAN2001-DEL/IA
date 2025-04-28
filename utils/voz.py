import speech_recognition as sr
import pyttsx3

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)

def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def escuchar():
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
        try:
            texto = listener.recognize_google(audio, language="es-ES").lower()
            print(f"Usuario: {texto}")
            return texto
        except Exception:
            return ""
