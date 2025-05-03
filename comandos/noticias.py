from utils.voz import talk, escuchar
from utils.fechas import interpretar_fecha
from servicios.newsapi_service import obtener_noticias
from config import CATEGORIAS_MAP

def manejar_comando_noticias():
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
    
    talk("¿Qué categoría? Tecnología, deportes, salud, o ninguna.")
    categoria = None
    while categoria is None:
        categoria_texto = escuchar()
        if "cerrar comando" in categoria_texto.lower():
            talk("Saliendo del comando de noticias.")
            return
        if categoria_texto.lower() == "ninguna":
            break
        categoria = CATEGORIAS_MAP.get(categoria_texto.lower())
        if not categoria:
            talk("No reconocí esa categoría. Intenta otra vez.")
    
    try:
        noticias, total_results = obtener_noticias(fecha=fecha, categoria=categoria, pagina=1, page_size=10)

        if noticias:
            talk(f"Encontré {total_results} noticias para la fecha {fecha} en la categoría {categoria if categoria else 'ninguna'}.")
            talk(f"Cada página tiene 10 noticias.")
            
            talk("¿Cuántas noticias deseas escuchar? Indica un número.")
            cantidad_noticias = None
            while not cantidad_noticias:
                cantidad_texto = escuchar()
                if "cerrar comando" in cantidad_texto.lower():
                    talk("Saliendo del comando de noticias.")
                    return
                try:
                    cantidad_noticias = int(cantidad_texto)
                    if cantidad_noticias <= 0:
                        talk("Por favor, ingresa un número mayor que 0.")
                        cantidad_noticias = None
                except ValueError:
                    talk("No entendí el número. Intenta otra vez.")

            cantidad_noticias = min(cantidad_noticias, total_results)

            talk("¿Desde qué página quieres comenzar? Puedes elegir la página 1, la 2, o cualquier otra.")
            pagina_inicio = None
            while not pagina_inicio:
                pagina_inicio_texto = escuchar()
                if "cerrar comando" in pagina_inicio_texto.lower():
                    talk("Saliendo del comando de noticias.")
                    return
                try:
                    pagina_inicio = int(pagina_inicio_texto)
                    if pagina_inicio <= 0:
                        talk("Por favor, ingresa un número mayor que 0 para la página.")
                except ValueError:
                    talk("No entendí la página. Por favor, di un número válido.")
            
            total_pages = (total_results // 10) + (1 if total_results % 10 != 0 else 0)
            talk(f"Hay {total_pages} páginas de noticias disponibles.")

            pagina = pagina_inicio
            noticias_restantes = cantidad_noticias

            while noticias_restantes > 0 and pagina <= total_pages:
                noticias, _ = obtener_noticias(fecha=fecha, categoria=categoria, pagina=pagina, page_size=10)

                if noticias:
                    for articulo in noticias:
                        if noticias_restantes <= 0:
                            break
                        talk(f"Título: {articulo['title']}")
                        talk(f"Descripción: {articulo.get('description', 'Sin descripción')}")
                        noticias_restantes -= 1
                else:
                    break
                pagina += 1

            if noticias_restantes > 0:
                talk("Has llegado al final de las noticias disponibles.")
            else:
                talk("Eso es todo por ahora.")
        else:
            talk("No encontré noticias para esos filtros.")
    except Exception as e:
        talk("Hubo un problema al obtener las noticias. Intenta más tarde.")
        print(f"Error al obtener noticias: {e}")
