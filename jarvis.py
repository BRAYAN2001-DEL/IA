import speech_recognition as sr
import pyttsx3
from datetime import datetime
import requests
import os
import time
from dateparser import parse  # pip install dateparser

# Configuración inicial
listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)

# --- Constantes ---
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "66f5e61e493145b8b6b1214f97f456f6")
CATEGORIAS_MAP = {
    "tecnología": "technology",
    "deportes": "sports",
    "salud": "health",
    "negocios": "business",
    "ciencia": "science",
    "entretenimiento": "entertainment",
    "general": "general",
}
CATEGORIAS_VALIDAS = list(CATEGORIAS_MAP.keys())

# --- Funciones principales ---
def talk(text):
    """Habla el texto dado."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def escuchar():
    """Escucha y devuelve el texto reconocido."""
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
        try:
            texto = listener.recognize_google(audio, language="es-ES").lower()
            print(f"Usuario: {texto}")
            return texto
        except sr.UnknownValueError:
            talk("No te entendí. ¿Podrías repetir?")
            return ""
        except sr.RequestError:
            talk("Error en el servicio de voz. Intenta más tarde.")
            return ""

def obtener_noticias(fecha=None, categoria=None):
    """Obtiene noticias de NewsAPI sobre Ecuador y las lee en voz alta."""
    base_url = f"https://newsapi.org/v2/everything?q=ecuador&apiKey={NEWSAPI_KEY}&language=es"

    if fecha:
        base_url += f"&from={fecha}&to={fecha}"
    if categoria:
        base_url += f"&category={categoria}"  # Aunque everything no usa category, por compatibilidad si quieres luego cambiar

    response = requests.get(base_url)
    noticias = response.json()

    if noticias.get('status') == 'ok' and noticias.get('totalResults', 0) > 0:
        for article in noticias['articles'][:3]:  # Solo las 3 primeras
            talk(f"Titular: {article['title']}")
            talk(f"Descripción: {article.get('description', 'Sin descripción')}")
            time.sleep(1)
    else:
        talk("No encontré noticias con esos filtros.")

def procesar_comando(comando):
    """Procesa el comando de voz y ejecuta acciones."""
    if "noticias" in comando:
        # Paso 1: (Ya no pedimos país porque siempre será Ecuador)
        talk("¿De qué fecha quieres las noticias? Di 'hoy', 'ayer', o una fecha como '15 de marzo'.")
        fecha_respuesta = escuchar()

        fecha = None
        if fecha_respuesta:
            fecha_parseada = parse(fecha_respuesta, languages=['es'])
            if fecha_parseada:
                fecha = fecha_parseada.strftime("%Y-%m-%d")
            else:
                fecha = datetime.now().strftime("%Y-%m-%d")
        else:
            fecha = datetime.now().strftime("%Y-%m-%d")

        # Paso 2: Pedir categoría
        talk("¿Qué categoría? Tecnología, deportes, salud, ciencia, negocios, etc. Di 'ninguna' para omitir.")
        categoria_respuesta = escuchar()
        categoria = None
        if categoria_respuesta and categoria_respuesta != "ninguna":
            categoria = CATEGORIAS_MAP.get(categoria_respuesta.lower())

        # Obtener noticias
        talk(f"Buscando noticias de Ecuador...")
        obtener_noticias(fecha, categoria)

    elif "adiós" in comando or "adios" in comando:
        talk("¡Hasta luego!")
        return False

    else:
        talk("No entendí el comando. Prueba con 'noticias' o 'adiós'.")
    return True

# --- Ejecución principal ---
if __name__ == "__main__":
    talk("¡Hola! Soy tu asistente de noticias de Ecuador. Di 'noticias' para comenzar o 'adiós' para salir.")
    while True:
        try:
            comando = escuchar()
            if comando and not procesar_comando(comando):
                break
        except Exception as e:
            talk(f"Error: {str(e)}")
            time.sleep(2)
