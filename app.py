import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Monitor de Empleabilidad", layout="wide")

# -------------------------------------------------------------------------
# Importación de modulos con tolerancia a fallos
# Usamos try-except para que la Interfaz Gráfica cargue aunque falte algún scraper.
# -------------------------------------------------------------------------
try:
    from modules.scraper_getonboard import extraer_getonboard
    from modules.api_remotive import extraer_remotive
    from modules.api_hackernews import extraer_hackernews
except ImportError:
    st.warning("Nota: Algunos módulos de extracción aún no están disponibles en el sistema.")

# --- LÓGICA DE ANÁLISIS ---
def analizar_skills(df):
    """
    Analiza la columna 'descripcion_breve' buscando palabras clave (Keywords)
    de tecnologías específicas usando expresiones regulares (Regex).
    """
    # Diccionario de normalización: Agrupa variantes (ej: React, Node -> JS)
    skills_map = {
        'Python': ['python', 'django', 'flask', 'fastapi', 'pandas'],
        'JavaScript': ['javascript', 'js', 'react', 'node', 'vue', 'angular', 'typescript'],
        'Java': ['java', 'spring', 'kotlin', 'android'],
        'SQL': ['sql', 'mysql', 'postgres', 'postgresql', 'database', 'mongodb'],
        'AWS': ['aws', 'amazon', 'ec2', 'lambda', 'cloud'],
        'Docker': ['docker', 'kubernetes', 'k8s', 'container'],
        'HTML/CSS': ['html', 'css', 'sass', 'bootstrap', 'tailwind'],
        'C#': ['c#', '.net', 'dotnet'],
        'PHP': ['php', 'laravel'],
        'Git': ['git', 'github', 'gitlab']
    }
    conteo = {tech: 0 for tech in skills_map}
    
    # Recorremos la columna 'descripcion_breve'
    for text in df['descripcion_breve']:
        if not isinstance(text, str): continue
        text = text.lower()
        for tech_main, keywords in skills_map.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text):
                    conteo[tech_main] += 1
                    break
    return pd.Series(conteo).sort_values(ascending=False)

# --- INTERFAZ DE USUARIO (FRONTEND) ---
st.title("📊 Monitor de Tecnologías Más Demandadas")
st.markdown("Sistema de Inteligencia de Negocios integrado con **GetOnBoard, Remotive y HackerNews**.")

# Botón de Acción
if st.button("🔄 Ejecutar Scraping en Tiempo Real"):
    datos = []
    bar = st.progress(0)
    
    # Bloque 1: GetOnBoard
    try:
        st.info("Conectando con GetOnBoard...")
        if 'extraer_getonboard' in globals():
            datos.extend(extraer_getonboard())
        bar.progress(33)
    except: st.error("Error al conectar con GetOnBoard")

    # Bloque 2: Remotive
    try:
        st.info("Conectando con Remotive...")
        if 'extraer_remotive' in globals():
            datos.extend(extraer_remotive())
        bar.progress(66)
    except: st.error("Error al conectar con Remotive")

    # Bloque 3: HackerNews
    try:
        st.info("Conectando con HackerNews...")
        if 'extraer_hackernews' in globals():
            datos.extend(extraer_hackernews())
        bar.progress(100)
    except: st.error("Error al conectar con HackerNews")

    # Procesamiento final
    if datos:
        df = pd.DataFrame(datos)
        if not os.path.exists('data'): os.makedirs('data')
        df.to_csv("data/ofertas_consolidadas.csv", index=False)
        st.success(f"¡Éxito! Se procesaron {len(df)} ofertas laborales.")
        st.rerun() # Recarga la página para mostrar los nuevos gráficos
    else:
        st.error("No se encontraron datos. Verifique la conexión o los módulos.")

# --- VISUALIZACIÓN DE RESULTADOS ---
if os.path.exists("data/ofertas_consolidadas.csv"):
    df = pd.read_csv("data/ofertas_consolidadas.csv")
    
    # Layout de 2 columnas
    col1, col2 = st.columns([2, 1])
    ranking = analizar_skills(df)
    
    with col1:
        st.subheader("Tendencia de Mercado (Top 10)")
        fig, ax = plt.subplots(figsize=(8, 5))
        ranking.plot(kind='bar', color='#2E86C1', ax=ax)
        ax.set_ylabel("Frecuencia de aparición")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with col2:
        st.subheader("Datos Cuantitativos")
        st.write(ranking)
    
    st.markdown("---")
    st.subheader("🔍 Explorador de Ofertas (Vista Filtrada)")
    # Seleccionamos solo columnas limpias para mostrar al usuario
    cols_visuales = ['fecha_extraccion', 'titulo', 'empresa', 'fuente', 'url']
    st.dataframe(df[cols_visuales], use_container_width=True)
