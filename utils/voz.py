import speech_recognition as sr
import pyttsx3
import time
import random

# Inicializar el motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Ajustar la velocidad de habla
engine.setProperty('volume', 1)  # Volumen máximo
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Cambiar la voz si lo deseas

listener = sr.Recognizer()

# Función para hablar (respuestas del asistente)
def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Función para escuchar
def escuchar():
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source, duration=1)  # Ajuste dinámico
        while True:  # Reintentar hasta que se capture algo
            try:
                audio = listener.listen(source, timeout=10, phrase_time_limit=10)
                texto = listener.recognize_google(audio, language="es-ES").lower()
                print(f"Usuario: {texto}")
                return texto
            except sr.UnknownValueError:
                talk("Lo siento, no pude entender lo que dijiste. ¿Podrías repetirlo?")
            except sr.RequestError:
                talk("Hubo un problema con el servicio de reconocimiento. Intenta más tarde.")
                return ""
            except sr.WaitTimeoutError:
                talk("No detecté nada. Por favor, habla más claro.")


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
        time.sleep(1)  # Pausa para evitar que el sistema se sobrecargue con peticiones continuas
 