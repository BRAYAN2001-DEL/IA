from datetime import datetime, timedelta
from dateparser import parse

def interpretar_fecha(texto_fecha):
    texto_fecha = texto_fecha.lower()
    if "hoy" in texto_fecha:
        return datetime.now().strftime("%Y-%m-%d")
    if "ayer" in texto_fecha:
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if "mañana" in texto_fecha:
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    fecha_parseada = parse(texto_fecha, languages=['es'])
    if fecha_parseada:
        return fecha_parseada.strftime("%Y-%m-%d")
    return None
