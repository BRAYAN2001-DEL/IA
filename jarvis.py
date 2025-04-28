import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
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

def interpretar_fecha(texto_fecha):
    """Interpreta expresiones como 'hoy', 'ayer', 'mañana'."""
    if "hoy" in texto_fecha:
        return datetime.now().strftime("%Y-%m-%d")
    elif "ayer" in texto_fecha:
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "anteayer" in texto_fecha:
        return (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    elif "mañana" in texto_fecha:
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        fecha_parseada = parse(texto_fecha, languages=['es'])
        if fecha_parseada:
            return fecha_parseada.strftime("%Y-%m-%d")
    return None

def obtener_noticias(fecha=None, categoria=None, pagina=1):
    """Obtiene noticias de NewsAPI sobre Ecuador y las lee en voz alta."""
    base_url = f"https://newsapi.org/v2/everything?q=ecuador&apiKey={NEWSAPI_KEY}&language=es&pageSize=3&page={pagina}"

    if fecha:
        base_url += f"&from={fecha}&to={fecha}"
    if categoria:
        base_url += f"&category={categoria}"  # Aunque everything no usa category

    response = requests.get(base_url)
    noticias = response.json()

    if noticias.get('status') == 'ok' and noticias.get('totalResults', 0) > 0:
        return noticias['articles']
    else:
        return []

def preguntar_fecha():
    """Pregunta por la fecha hasta obtener una válida."""
    while True:
        talk("¿De qué fecha quieres las noticias? Di 'hoy', 'ayer', 'mañana', o una fecha como '15 de marzo'.")
        fecha_respuesta = escuchar()
        fecha = interpretar_fecha(fecha_respuesta)
        if fecha:
            return fecha
        else:
            talk("No entendí la fecha. Intenta de nuevo.")

def preguntar_categoria():
    """Pregunta por la categoría hasta obtener una válida o ninguna."""
    while True:
        talk("¿Qué categoría? Tecnología, deportes, salud, ciencia, negocios, etc. Di 'ninguna' para omitir.")
        categoria_respuesta = escuchar()
        if categoria_respuesta == "ninguna":
            return None
        categoria = CATEGORIAS_MAP.get(categoria_respuesta.lower())
        if categoria:
            return categoria
        else:
            talk("No reconocí esa categoría. Intenta de nuevo.")

def procesar_comando(comando):
    """Procesa el comando de voz y ejecuta acciones."""
    if "noticias" in comando:
        fecha = preguntar_fecha()
        categoria = preguntar_categoria()
        pagina = 1

        while True:
            noticias = obtener_noticias(fecha, categoria, pagina)
            if noticias:
                for article in noticias:
                    talk(f"Titular: {article['title']}")
                    talk(f"Descripción: {article.get('description', 'Sin descripción')}")
                    time.sleep(1)

                # Preguntar si quiere más noticias
                talk("¿Quieres escuchar más noticias?")
                respuesta = escuchar()
                if "sí" in respuesta or "si" in respuesta or "más" in respuesta:
                    pagina += 1
                    continue
                else:
                    break
            else:
                talk("No encontré más noticias.")
                break

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
