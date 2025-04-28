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
    
    # Obtener las noticias iniciales
    try:
        noticias = obtener_noticias(fecha=fecha, categoria=categoria, pagina=1)
        total_noticias = len(noticias)

        if total_noticias > 0:
            # Informar cuántas noticias están disponibles
            talk(f"Hay {total_noticias} noticias disponibles para esa fecha y categoría.")

            # Leer las primeras 3 noticias
            for articulo in noticias[:3]:
                talk(f"Título: {articulo['title']}")
                descripcion = articulo.get('description', 'Sin descripción')
                talk(f"Descripción: {descripcion}")

            # Preguntar si quiere más noticias
            talk("¿Quieres escuchar más noticias de la misma página? Di 'sigue' para continuar con la misma página, o 'otra' para cambiar a la siguiente página.")
            respuesta = escuchar().lower()

            pagina_actual = 1
            while respuesta == "sigue":
                # Continuar con la misma página
                for articulo in noticias[3:]:
                    talk(f"Título: {articulo['title']}")
                    talk(f"Descripción: {articulo.get('description', 'Sin descripción')}")

                talk("¿Quieres seguir escuchando más noticias de esta página?")
                respuesta = escuchar().lower()

            # Si el usuario quiere cambiar a la siguiente página
            if respuesta == "otra":
                pagina_actual += 1
                noticias = obtener_noticias(fecha=fecha, categoria=categoria, pagina=pagina_actual)
                total_noticias = len(noticias)
                if total_noticias > 0:
                    talk(f"Hay {total_noticias} noticias disponibles en la página {pagina_actual}.")

                    for articulo in noticias[:3]:
                        talk(f"Título: {articulo['title']}")
                        talk(f"Descripción: {articulo.get('description', 'Sin descripción')}")

                    talk("¿Quieres escuchar más noticias de esta página?")
                    respuesta = escuchar().lower()

                else:
                    talk("No hay más noticias disponibles en esa página.")

            # Si el usuario ya no quiere más noticias
            if respuesta != "sigue" and respuesta != "otra":
                talk("Fin de las noticias.")
        else:
            talk("No encontré noticias para esos filtros.")
    except Exception as e:
        talk("Hubo un problema al obtener las noticias. Intenta más tarde.")
        print(f"Error al obtener noticias: {e}")
