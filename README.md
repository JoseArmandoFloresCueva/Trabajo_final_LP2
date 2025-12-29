Monitor de Empleabilidad - Informe Técnico del Proyecto

Integrantes:
-huarcayaariasd-bit: Huarcaya Arias, Danilo
-Joseflores23: Flores Cueva, Jose Armando
-RichiTM28: Terreros Mosquera, Wellington Ricardo

1. Descripción y Objetivos:
Este proyecto es una herramienta de Inteligencia de Negocios (BI) enfocada en la empleabilidad. Su objetivo es extraer, procesar y visualizar en tiempo real las tecnologías más demandadas para desarrolladores de software, consolidando información de múltiples fuentes internacionales.

2. Planeación del Diseño y Extracción de Datos:
    2.1. Selección de Fuentes:
    Para garantizar una muestra representativa, se seleccionaron tres fuentes con arquitecturas diferentes:
    - GetOnBoard: Fuente principal para Latinoamérica (Web Scraping).
    - Remotive: Fuente global para trabajo remoto (API REST).
    - HackerNews: Fuente de nicho para Startups de alto nivel (API Pública).
    2.2. Estrategia de Filtrado: "Lógica de Exclusión"Durante la fase de análisis, detectamos que filtrar estrictamente por la palabra "Junior" eliminaba el 90% de las ofertas relevantes, ya que muchas empresas publican títulos genéricos (ej: "Python Developer") aptos para juniors.Solución Implementada:En lugar de buscar inclusivamente ("Junior"), aplicamos un algoritmo de exclusión:"Aceptar todas las ofertas disponibles, EXCEPTO aquellas que contengan explícitamente términos de alta jerarquía (Senior, Lead, Principal, Manager, Architect)."
    2.3. Estructuración y Normalización (Data Pipeline): Dado que cada fuente entrega los datos en formatos distintos (HTML, JSON anidado, Listas), se diseñó un esquema de diccionario unificado para la combinacion de datos:
    Campo UnificadoOrigen GetOnBoardOrigen RemotiveOrigen HackerNewstituloTag <a>.titleKey job['title']Key story['title']empresaTexto inferidoKey job['company_name']String estático "Startup (HN)"descripcion_breveTítulo crudoTítulo + TagsTítulo + Textourlhref relativo + Base URLKey job['url']URL construida con ID

3. Arquitectura del Sistema (Diseño Técnico)
El sistema sigue el patrón ETL (Extract, Transform, Load) integrado en una aplicación web interactiva.Fragmento de códigograph LR
    A[Fuentes Externas] --> B(Módulos de Extracción);
    B --> C{Normalización y Filtrado};
    C --> D[DataFrame Pandas];
    D --> E[(Archivo CSV Consolidado)];
    E --> F[Visualización Streamlit];
Tecnologías Clave:
- Streamlit: Para la interfaz gráfica y reactividad (st.rerun para actualización dinámica).
- BeautifulSoup4: Para el parsing de HTML en GetOnBoard.
- Urllib3: Configurado para evasión de bloqueos SSL (verify=False) asegurando compatibilidad en cualquier entorno Windows.
- Pandas & Matplotlib: Para la manipulación tabular y generación de gráficos estadísticos.

4. Estructura del Repositorio
trabajo_final-lp2/
│
├── app.py                 # (Main) Orquestador de la aplicación web y visualización
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Documentación técnica
│
├── modules/               # Capa de Lógica de Negocio (Backend)
│   ├── scraper_getonboard.py  # Lógica de Web Scraping y manejo SSL
│   ├── api_remotive.py        # Consumo API REST
│   └── api_hackernews.py      # Consumo API Iterativa
│
├── docs/                  # Documentación adicional
│   └── diccionario_datos.md
│
└── data/                  # Capa de Persistencia (Generado automáticamente)
    └── ofertas_consolidadas.csv

5. Evidencia del Trabajo en Equipo (Distribución de Módulos)
El desarrollo se realizó de forma modular, permitiendo trabajar en paralelo y luego integrar las partes en app.py.
- Danilo: Ingeniería de Datos & Scraping
Implementación del módulo complejo scraper_getonboard.py (Manejo de SSL y HTML Parsing).
Definición del entorno de ejecución (requirements.txt).
Documentación de la estructura de datos (docs/diccionario_datos.md).

- Wellington: Integración API & Documentación Técnica
Implementación del módulo api_remotive.py con filtrado de etiquetas.
Redacción del Informe Técnico Profesional (README.md).
Control de calidad de la documentación.

- Jose: Desarrollo Frontend & API Secundaria
Desarrollo de la aplicación web principal (app.py) usando Streamlit.
Implementación del módulo api_hackernews.py.
Lógica de integración final y generación de gráficos.

6. Instrucciones de Instalación:
- Clonar repositorio o descargar archivos.
- Instalar dependencias:
 Bash: pip install -r requirements.txt
- Ejecutar la aplicación:
Bash streamlit run app.py
La aplicación abrirá automáticamente una pestaña en el navegador mostrando el Dashboard.

Curso: Lenguaje de Programación 2 
Fecha: Diciembre 2025
