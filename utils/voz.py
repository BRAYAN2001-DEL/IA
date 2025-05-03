import speech_recognition as sr
import pyttsx3
import time

# Inicializar motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
engine.setProperty('voice', engine.getProperty('voices')[0].id)

listener = sr.Recognizer()

# Función para hablar
def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Diccionario opcional para normalizar números hablados
NUMEROS_MAP = {
    "uno": "1", "primero": "1",
    "dos": "2", "segundo": "2",
    "tres": "3", "tercero": "3",
    "cuatro": "4", "cuarto": "4",
    "cinco": "5", "quinto": "5",
    "seis": "6", "sexto": "6",
    "siete": "7", "séptimo": "7",
    "ocho": "8", "octavo": "8",
    "nueve": "9", "noveno": "9",
    "diez": "10", "décimo": "10"
}


def normalizar_numeros(texto):
    palabras = texto.split()
    normalizado = [NUMEROS_MAP.get(palabra, palabra) for palabra in palabras]
    return " ".join(normalizado)

# Función mejorada para escuchar
def escuchar():
    with sr.Microphone() as source:
        print("Ajustando al ruido ambiente...")
        listener.adjust_for_ambient_noise(source, duration=1.5)

        print("Escuchando...")
        intentos = 3
        while intentos > 0:
            try:
                audio = listener.listen(source, timeout=5, phrase_time_limit=5)
                texto = listener.recognize_google(audio, language="es-ES").lower()
                texto = normalizar_numeros(texto)
                print(f"Usuario: {texto}")
                return texto
            except sr.UnknownValueError:
                talk("No entendí lo que dijiste. Intenta de nuevo.")
            except sr.RequestError:
                talk("Error de conexión con el servicio de reconocimiento.")
                return ""
            except sr.WaitTimeoutError:
                talk("No detecté voz. Intenta hablar con más claridad.")
            intentos -= 1

        talk("No logré entender después de varios intentos.")
        return ""

# Ejemplo de uso
if __name__ == "__main__":
    talk("¡Hola! ¿En qué puedo ayudarte hoy?")
    while True:
        comando = escuchar()
        if "cerrar comando" in comando:
            talk("Saliendo del comando. ¡Hasta pronto!")
            break
        elif comando:
            talk(f"Has dicho: {comando}")
        time.sleep(1)
