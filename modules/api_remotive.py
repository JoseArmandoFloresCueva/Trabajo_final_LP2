import requests
from datetime import datetime

def extraer_remotive():
    print("--- Iniciando API: Remotive ---")
    lista = []
    try:
        # Remotive devuelve un JSON directo, no requiere scraping.
        res = requests.get("https://remotive.com/api/remote-jobs?category=software-dev")
        data = res.json()
        # La API devuelve una lista bajo la clave 'jobs
        for job in data.get('jobs', []):
            titulo = job.get('title', '')
            # Filtro Anti-Senior
            if not any(x in titulo.lower() for x in ['senior', 'lead', 'manager', 'principal']):
                tags = " ".join(job.get('tags', []))
                # Normalización al esquema común del proyecto
                lista.append({
                    "fecha_extraccion": datetime.now().strftime("%Y-%m-%d"),
                    "titulo": titulo,
                    "empresa": job.get('company_name', ''),
                    "fuente": "Remotive",
                    "url": job.get('url', ''),
                    # Concatenamos tags para mejorar la detección de skills
                    "descripcion_breve": f"{titulo} {tags}" 
                })
    except Exception as e:
        print(f"Error Remotive: {e}")
    return lista
