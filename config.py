import os

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "66f5e61e493145b8b6b1214f97f456f6")

CATEGORIAS_MAP = {
    "tecnología": "technology",
    "deportes": "sports",
    "salud": "health",
    "ciencia": "science",
    "negocios": "business",
    "entretenimiento": "entertainment",
    "general": "general",
}
