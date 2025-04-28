from utils.voz import talk, escuchar
from utils.fechas import interpretar_fecha
from servicios.newsapi_service import obtener_noticias
from config import CATEGORIAS_MAP

# talk es el comando que hace que hable el asistente
def manejar_comando_noticias():
    # Preguntar la fecha y verificar la respuesta
    talk("¿De qué fecha quieres noticias?")
    fecha = None
    while not fecha:
        fecha_texto = escuchar()
        if "cerrar comando" in fecha_texto.lower():
            talk("Saliendo del comando de noticias.")
            return
        fecha = interpretar_fecha(fecha_texto)
        if not fecha:
            talk("No entendí la fecha. Intenta otra vez.")
    
    # Preguntar la categoría
    talk("¿Qué categoría? Tecnología, deportes, salud, o ninguna.")
    categoria = None
    while categoria is None:
        categoria_texto = escuchar()
        if "cerrar comando" in categoria_texto.lower():
            talk("Saliendo del comando de noticias.")
            return
        if categoria_texto == "ninguna":
            break
        categoria = CATEGORIAS_MAP.get(categoria_texto.lower())
        if not categoria:
            talk("No reconocí esa categoría. Intenta otra vez.")
    
    try:
        noticias = obtener_noticias(fecha=fecha, categoria=categoria)
        if noticias:
            # Leer los primeros 3 artículos
            for articulo in noticias[:3]:
                talk(f"Título: {articulo['title']}")
                descripcion = articulo.get('description', 'Sin descripción')
                talk(f"Descripción: {descripcion}")
            
            # Preguntar si quiere más noticias
            talk("¿Quieres escuchar más noticias? Di 'sigue' o 'no'.")
            respuesta = escuchar().lower()

            while respuesta == "sigue":
                for articulo in noticias[3:]:
                    talk(f"Título: {articulo['title']}")
                    talk(f"Descripción: {articulo.get('description', 'Sin descripción')}")
                
                talk("¿Quieres escuchar más noticias? Di 'sigue' para más o 'no' para finalizar.")
                respuesta = escuchar().lower()

                # Verificar si el usuario quiere cerrar el comando
                if "cerrar comando" in respuesta:
                    talk("Saliendo del comando de noticias.")
                    return

            if respuesta != "sigue":
                talk("Fin de las noticias.")
        else:
            talk("No encontré noticias para esos filtros.")
    except Exception as e:
        talk("Hubo un problema al obtener las noticias. Intenta más tarde.")
        print(f"Error al obtener noticias: {e}")

