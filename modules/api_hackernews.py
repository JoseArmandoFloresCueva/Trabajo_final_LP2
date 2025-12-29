import requests
from datetime import datetime
import time

def extraer_hackernews():
    print("--- Iniciando API: Hacker News ---")
    lista = []
    try:
        # Obtenemos los IDs de las historias de empleo
        ids = requests.get("https://hacker-news.firebaseio.com/v0/jobstories.json").json()
        
        # Limitamos a las últimas 20 ofertas para evitar tiempos de carga largos en la demo
        for id_job in ids[:20]:
            job = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id_job}.json").json()
            
            if job and 'title' in job:
                titulo = job.get('title', '')
                t_low = titulo.lower()
                
                # Filtro de Exclusión: Evitamos cargos Senior/Manager
                if not any(x in t_low for x in ['senior', 'lead', 'manager', 'architect']):
                    lista.append({
                        "fecha_extraccion": datetime.now().strftime("%Y-%m-%d"),
                        "titulo": titulo,
                        "empresa": "Startup (HN)", # HackerNews no siempre da el nombre de la empresa explícito
                        "fuente": "HackerNews",
                        "url": f"https://news.ycombinator.com/item?id={id_job}",
                        "descripcion_breve": titulo
                    })
            # Pequeña pausa para no saturar la conexión
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error HN: {e}")
    return lista
