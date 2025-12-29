import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
# -------------------------------------------------------------------------
# CONFIGURACIÓN DE SEGURIDAD
# Desactivamos las advertencias de seguridad SSL.
# Esto es necesario porque en entornos corporativos o educativos (Windows),
# los certificados de Python a veces fallan al conectar con sitios https.
# -------------------------------------------------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extraer_getonboard():
    print("--- Iniciando Scraping: GetOnBoard ---")
    lista = []
    url_base = "https://www.getonbrd.com"
    url = f"{url_base}/jobs/programming"

    try:
        # Usamos verify=False para evitar errores de certificado SSL.
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
        # Manejo de redirecciones o errores 404
        if res.status_code == 404:
            res = requests.get("https://www.getonbrd.com/jobs/programming", verify=False)

        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('a', class_='gb-results-list__item')

        for link in links:
            titulo = link.get('title')
            url_rel = link.get('href')
            if not titulo:
                continue
            # --- ESTRATEGIA DE EXCLUSIÓN ---
            # En lugar de buscar solo "Junior" (que trae pocos resultados),
            # aceptamos todo y EXCLUIMOS explícitamente los cargos altos.
            t_low = titulo.lower()
            if not any(x in t_low for x in ['senior', 'lead', 'manager', 'architect', 'principal']):
                # Normalización de datos
                lista.append({
                    "fecha_extraccion": datetime.now().strftime("%Y-%m-%d"),
                    "titulo": titulo,
                    "empresa": "GetOnBoard",
                    "fuente": "GetOnBoard",
                    "url": url_rel if url_rel.startswith('http') else f"{url_base}{url_rel}",
                    "descripcion_breve": titulo
                })

        print(f"GetOnBoard finalizado: {len(lista)} ofertas.")

    except Exception as e:
        print(f"Error GOB: {e}")

    return lista

if __name__ == "__main__":
    datos = extraer_getonboard()
    print(f"Total encontrado: {len(datos)}")
