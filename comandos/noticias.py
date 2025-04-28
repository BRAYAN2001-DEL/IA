from utils.voz import talk, escuchar
from utils.fechas import interpretar_fecha
from servicios.newsapi_service import obtener_noticias
from config import CATEGORIAS_MAP

#talk es el comando que hace que hable el asistente
def manejar_comando_noticias():
    talk("¿De qué fecha quieres noticias?")
    fecha = None
    while not fecha:
        fecha_texto = escuchar()
        fecha = interpretar_fecha(fecha_texto)
        if not fecha:
            talk("No entendí la fecha. Intenta otra vez.")
    
    talk("¿Qué categoría? Tecnología, deportes, salud, o ninguna.")
    categoria = None
    while categoria is None:
        categoria_texto = escuchar()
        if categoria_texto == "ninguna":
            break
        categoria = CATEGORIAS_MAP.get(categoria_texto.lower())
        if not categoria:
            talk("No reconocí esa categoría. Intenta otra vez.")

    noticias = obtener_noticias(fecha=fecha, categoria=categoria)

    if noticias:
        for articulo in noticias:
            talk(f"Título: {articulo['title']}")
            talk(f"Descripción: {articulo.get('description', 'Sin descripción')}")
    else:
        talk("No encontré noticias para esos filtros.")
