import requests
from config import NEWSAPI_KEY

def obtener_noticias(fecha=None, categoria=None, pagina=1):
    url = f"https://newsapi.org/v2/everything?q=ecuador&apiKey={NEWSAPI_KEY}&language=es&pageSize=3&page={pagina}"
    
    if fecha:
        url += f"&from={fecha}&to={fecha}"
    if categoria:
        url += f"&category={categoria}"  # Nota: no siempre aplica para everything

    response = requests.get(url)
    datos = response.json()

    if datos.get('status') == 'ok':
        return datos.get('articles', [])
    else:
        return []
