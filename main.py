from utils.voz import talk, escuchar
from comandos.noticias import manejar_comando_noticias

def main():
    talk("¡Hola! Soy tu asistente de virtual. Di 'noticias' para comenzar o 'adiós' para salir.")
    while True:
        comando = escuchar()
        if "noticias" in comando:
            manejar_comando_noticias()
        elif "adiós" in comando or "adios" in comando:
            talk("¡Hasta luego!")
            break
        else:
            talk("No entendí. Por favor di 'noticias' o 'adiós'.")

if __name__ == "__main__":
    main()
