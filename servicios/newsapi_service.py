import requests
from config import NEWSAPI_KEY

def obtener_noticias(fecha=None, categoria=None, pagina=1):
    # La URL base para obtener las noticias
    url = f"https://newsapi.org/v2/everything?q=ecuador&apiKey={NEWSAPI_KEY}&language=es&pageSize=3&page={pagina}"

    # Añadir parámetros de fecha si están presentes
    if fecha:
        url += f"&from={fecha}&to={fecha}"
    
    # Añadir el parámetro de categoría si está presente
    if categoria:
        url += f"&category={categoria}"  # Nota: No siempre aplica para 'everything'

    # Hacer la solicitud HTTP
    response = requests.get(url)
    datos = response.json()

    # Verificar el estado de la respuesta de la API
    if datos.get('status') == 'ok':
        return datos.get('articles', [])  # Retornar los artículos de la respuesta
    else:
        # Si no hay resultados, retornar una lista vacía
        return []

