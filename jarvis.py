import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

# Inicialización del motor de voz
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Función para decir algo
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Función para obtener las noticias
def obtener_noticias():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=66f5e61e493145b8b6b1214f97f456f6"
    response = requests.get(url)
    noticias = response.json()
    for article in noticias['articles'][:5]:  # Leer las 5 primeras noticias
        talk(f"Titular: {article['title']}")
        talk(f"Descripción: {article['description']}")

# Saludo inicial
talk("Buenos días, soy tu asistente virtual. ¿En qué te puedo ayudar hoy?")

# Bucle para escuchar de manera continua
while True:
    try:
        with sr.Microphone() as source:
            print("Escuchando....")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            rec = listener.recognize_google(voice)
            rec = rec.lower()
            print(f"Has dicho: {rec}")

            if "tiempo" in rec:
                time = datetime.datetime.now().strftime("%H:%M")
                talk(f"La hora actual es {time}")
            elif "nombre" in rec:
                talk("Mi nombre es Asistente Virtual.")
            elif "noticias" in rec:
                obtener_noticias()
            elif "abrir navegador" in rec:
                webbrowser.open('https://www.google.com')
                talk("Abriendo el navegador.")
            elif "adiós" in rec:
                talk("¡Hasta luego! Que tengas un buen día.")
                break  # Rompe el bucle y termina el programa
            else:
                talk("Lo siento, no te he entendido.")
    
    except sr.UnknownValueError:
        talk("No pude entender lo que dijiste, por favor repite.")
    except sr.RequestError:
        talk("Hubo un problema con el servicio de reconocimiento de voz. Intenta más tarde.")
    except Exception as e:
        talk(f"Ocurrió un error inesperado: {str(e)}")
