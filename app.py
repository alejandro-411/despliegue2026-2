import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FAVICON = ASSETS_DIR / "favicon.svg"

st.set_page_config(
    page_title="Academic Performance Intelligence | EAM",
    page_icon=str(FAVICON) if FAVICON.exists() else ":material/monitoring:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def ms_icon(name: str, size: int = 20, css_class: str = "") -> str:
    """Renderiza un icono de Material Symbols (librería de Google Fonts)."""
    cls = f"material-symbols-outlined {css_class}".strip()
    return (
        f'<span class="{cls}" '
        f'style="font-size:{size}px;line-height:1;vertical-align:middle;'
        f'font-variation-settings:\'FILL\' 0, \'wght\' 500, \'GRAD\' 0, \'opsz\' 24;">'
        f'{name}</span>'
    )

def inyectar_estilos():
    estilo_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,500,0,0&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,700&display=swap');

    :root {
        --navy-950: #0B1220;
        --navy-900: #12233A;
        --navy-800: #1B3354;
        --slate-700: #3D4F66;
        --slate-500: #6B7C93;
        --slate-200: #D7DEE8;
        --slate-100: #E8EEF5;
        --surface: #F4F7FB;
        --white: #FFFFFF;
        --accent: #0E7C86;
        --accent-soft: #D7F1F3;
        --success: #0F766E;
        --success-bg: #ECFDF8;
        --warning: #B45309;
        --shadow-sm: 0 1px 2px rgba(11, 18, 32, 0.06);
        --shadow-md: 0 8px 24px rgba(11, 18, 32, 0.08);
        --radius: 12px;
        --radius-sm: 8px;
    }

    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined' !important;
        font-weight: normal !important;
        font-style: normal;
        display: inline-block;
        line-height: 1;
        text-transform: none;
        letter-spacing: normal;
        word-wrap: normal;
        white-space: nowrap;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        font-feature-settings: 'liga';
    }

    html, body, [class*="css"], .stApp, .stMarkdown, .stText, p, label, span, div {
        font-family: 'IBM Plex Sans', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 0% -10%, rgba(14, 124, 134, 0.08), transparent 50%),
            radial-gradient(ellipse 60% 40% at 100% 0%, rgba(27, 51, 84, 0.06), transparent 45%),
            linear-gradient(180deg, #EEF3F8 0%, var(--surface) 40%, #E9EFF6 100%) !important;
    }

    [data-testid="stHeader"] {
        background: rgba(244, 247, 251, 0.85) !important;
        backdrop-filter: blur(8px);
        border-bottom: 1px solid var(--slate-200);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--navy-950) 0%, var(--navy-900) 55%, #15304F 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] * {
        color: #E8EEF5 !important;
    }

    [data-testid="stSidebar"] .sidebar-brand {
        padding: 0.5rem 0 1.25rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 1.25rem;
    }

    [data-testid="stSidebar"] .sidebar-brand .brand-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: rgba(14, 124, 134, 0.25);
        color: #7DD3D8 !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.85rem;
    }

    [data-testid="stSidebar"] .sidebar-brand .eyebrow {
        font-size: 0.7rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7DD3D8 !important;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    [data-testid="stSidebar"] .sidebar-brand h2 {
        font-family: 'Fraunces', serif !important;
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: #FFFFFF !important;
        line-height: 1.25;
    }

    [data-testid="stSidebar"] .sidebar-brand p {
        font-size: 0.85rem;
        line-height: 1.45;
        color: #A8B8CC !important;
        margin: 0;
    }

    [data-testid="stSidebar"] .sidebar-meta {
        margin-top: 1.5rem;
        padding: 1rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: var(--radius-sm);
    }

    [data-testid="stSidebar"] .sidebar-meta .meta-row {
        display: flex;
        align-items: flex-start;
        gap: 0.65rem;
        margin-bottom: 0.95rem;
    }

    [data-testid="stSidebar"] .sidebar-meta .meta-row:last-child {
        margin-bottom: 0;
    }

    [data-testid="stSidebar"] .sidebar-meta .meta-icon {
        color: #7DD3D8 !important;
        margin-top: 0.1rem;
    }

    [data-testid="stSidebar"] .sidebar-meta .meta-label {
        font-size: 0.68rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #7DD3D8 !important;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    [data-testid="stSidebar"] .sidebar-meta .meta-value {
        font-size: 0.9rem;
        color: #E8EEF5 !important;
        margin: 0;
        line-height: 1.35;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1180px !important;
    }

    .hero {
        background: linear-gradient(135deg, var(--navy-900) 0%, var(--navy-800) 55%, #1A4A5C 100%);
        border-radius: 16px;
        padding: 2rem 2.25rem;
        margin-bottom: 1.75rem;
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background:
            linear-gradient(120deg, transparent 40%, rgba(14, 124, 134, 0.22) 100%),
            radial-gradient(circle at 90% 20%, rgba(125, 211, 216, 0.18), transparent 35%);
        pointer-events: none;
    }

    .hero-inner {
        position: relative;
        z-index: 1;
    }

    .hero .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.72rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #7DD3D8;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    .hero h1 {
        font-family: 'Fraunces', serif !important;
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: clamp(1.7rem, 2.6vw, 2.35rem);
        line-height: 1.2;
        margin: 0 0 0.65rem 0;
        letter-spacing: -0.02em;
    }

    .hero p {
        color: #C5D0DE !important;
        font-size: 1.02rem;
        line-height: 1.55;
        margin: 0;
        max-width: 720px;
        font-weight: 400;
    }

    .panel {
        background: var(--white);
        border: 1px solid var(--slate-200);
        border-radius: var(--radius);
        padding: 1.35rem 1.5rem 1.5rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 0.5rem;
    }

    .panel-title {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 0.35rem;
    }

    .panel-title .icon-badge {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: var(--accent-soft);
        color: var(--accent) !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .panel-title h3 {
        font-family: 'Fraunces', serif !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: var(--navy-900) !important;
        margin: 0 !important;
        letter-spacing: -0.01em;
    }

    .panel-desc {
        color: var(--slate-500) !important;
        font-size: 0.92rem !important;
        margin: 0.35rem 0 1.1rem 2.75rem !important;
        line-height: 1.45;
    }

    .result-card {
        background: linear-gradient(135deg, var(--success-bg) 0%, #F0FDFA 100%);
        border: 1px solid #A7F3D0;
        border-radius: var(--radius);
        padding: 1.5rem 1.65rem;
        margin-top: 0.5rem;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        background: linear-gradient(180deg, var(--accent), var(--success));
    }

    .result-card .result-label {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--success);
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .result-card .result-title {
        font-family: 'Fraunces', serif !important;
        color: var(--navy-900) !important;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0 0 0.85rem 0;
    }

    .result-card .result-score {
        display: flex;
        align-items: baseline;
        gap: 0.45rem;
        flex-wrap: wrap;
    }

    .result-card .score-value {
        font-family: 'Fraunces', serif !important;
        font-size: 2.4rem;
        font-weight: 700;
        color: var(--navy-900);
        letter-spacing: -0.03em;
        line-height: 1;
    }

    .result-card .score-scale {
        font-size: 1rem;
        color: var(--slate-500);
        font-weight: 500;
    }

    .result-card .score-hint {
        margin-top: 0.75rem;
        font-size: 0.88rem;
        color: var(--slate-700);
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--navy-900) 0%, var(--navy-800) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em;
        border-radius: var(--radius-sm) !important;
        border: 1px solid transparent !important;
        padding: 0.7rem 1.5rem !important;
        transition: all 0.25s ease !important;
        width: 100%;
        box-shadow: 0 4px 14px rgba(18, 35, 58, 0.22) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent) 0%, #0A656D 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 6px 18px rgba(14, 124, 134, 0.35) !important;
        transform: translateY(-1px);
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(14, 124, 134, 0.28) !important;
        outline: none !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        background: transparent;
        border-bottom: 1px solid var(--slate-200);
        padding-bottom: 0;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.25rem !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        font-weight: 600 !important;
        color: var(--slate-500) !important;
        letter-spacing: 0.01em;
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--navy-900) !important;
        border-bottom: 3px solid var(--accent) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.25rem;
    }

    div[data-baseweb="select"] > div,
    .stNumberInput input,
    .stTextInput input {
        border-radius: var(--radius-sm) !important;
        border-color: var(--slate-200) !important;
        background: var(--white) !important;
    }

    div[data-baseweb="select"] > div:hover,
    .stNumberInput input:hover {
        border-color: var(--accent) !important;
    }

    [data-testid="stFileUploader"] {
        background: var(--white);
        border: 1.5px dashed var(--slate-200);
        border-radius: var(--radius);
        padding: 0.75rem;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent);
        background: #F8FCFC;
    }

    .stAlert {
        border-radius: var(--radius-sm) !important;
        box-shadow: var(--shadow-sm);
        border-left-width: 4px !important;
    }

    [data-testid="stExpander"] {
        background: var(--white);
        border: 1px solid var(--slate-200);
        border-radius: var(--radius-sm);
        box-shadow: none;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--slate-200);
        border-radius: var(--radius-sm);
        overflow: hidden;
    }

    label, .stSelectbox label, .stNumberInput label, .stFileUploader label {
        font-weight: 600 !important;
        color: var(--navy-800) !important;
        font-size: 0.9rem !important;
    }

    .section-heading {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 1.25rem 0 0.75rem 0;
        color: var(--accent);
    }

    .section-heading h5 {
        font-family: 'Fraunces', serif !important;
        font-size: 1.05rem !important;
        color: var(--navy-900) !important;
        margin: 0 !important;
        font-weight: 700 !important;
    }

    .nav-wrap {
        margin-bottom: 1rem;
    }

    .footer-note {
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--slate-200);
        color: var(--slate-500);
        font-size: 0.8rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)

inyectar_estilos()

with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="brand-icon">{ms_icon("monitoring", 24)}</div>
            <div class="eyebrow">EAM · Seminario ML</div>
            <h2>Academic Performance Intelligence</h2>
            <p>Plataforma de apoyo a la toma de decisiones académicas basada en modelos supervisados.</p>
        </div>
        <div class="sidebar-meta">
            <div class="meta-row">
                <span class="meta-icon">{ms_icon("model_training", 18)}</span>
                <div>
                    <div class="meta-label">Modelo</div>
                    <p class="meta-value">Bagging Optimizado</p>
                </div>
            </div>
            <div class="meta-row">
                <span class="meta-icon">{ms_icon("input", 18)}</span>
                <div>
                    <div class="meta-label">Entradas</div>
                    <p class="meta-value">Estilo Felder · Examen de admisión</p>
                </div>
            </div>
            <div class="meta-row">
                <span class="meta-icon">{ms_icon("output", 18)}</span>
                <div>
                    <div class="meta-label">Salida</div>
                    <p class="meta-value">Nota final estimada (0–5)</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-inner">
            <div class="eyebrow">{ms_icon("dashboard", 16)} Dashboard ejecutivo · Predicción académica</div>
            <h1>Estimación de rendimiento estudiantil</h1>
            <p>Sistema de inteligencia artificial para proyectar la calificación final a partir del perfil de aprendizaje y el puntaje de admisión. Diseñado para revisión por stakeholders académicos y de gestión.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def load_resources():
    one_hot_transformer = joblib.load('one_hot_columns.joblib')
    scaler = joblib.load('min_max_scaler.joblib')
    model = joblib.load('bagging_optimizado.joblib')
    return one_hot_transformer, scaler, model

try:
    one_hot_transformer, scaler, model = load_resources()
except Exception as e:
    st.error(f"Error al cargar los modelos pre-entrenados: {e}")
    st.stop()

def procesar_datos(df_input):
    df_procesado = df_input.copy()
    columnas_a_eliminar = ['ID', 'Año - Semestre', 'Nota_final', 'Aprobo']
    df_procesado = df_procesado.drop(columns=[col for col in columnas_a_eliminar if col in df_procesado.columns], errors='ignore')
    
    si_columnas_one_hot = [col for col in one_hot_transformer if 'Felder_' in col] if isinstance(one_hot_transformer, list) else []
    if 'Felder' in df_procesado.columns:
        for col_name in si_columnas_one_hot:
            valor_esperado = col_name.replace('Felder_', '')
            df_procesado[col_name] = (df_procesado['Felder'] == valor_esperado).astype(int)
        df_procesado = df_procesado.drop(columns=['Felder'])
    
    for col in si_columnas_one_hot:
        if col not in df_procesado.columns:
            df_procesado[col] = 0
            
    if 'Examen_admisión' in df_procesado.columns:
        df_procesado['Examen_admision_scaled'] = scaler.transform(df_procesado[['Examen_admisión']])
        df_procesado = df_procesado.drop(columns=['Examen_admisión'])
        
    columnas_ordenadas = si_columnas_one_hot + ['Examen_admision_scaled']
    
    for col in columnas_ordenadas:
        if col not in df_procesado.columns:
            df_procesado[col] = 0
            
    return df_procesado[columnas_ordenadas]

def render_evaluacion_individual():
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">
                <span class="icon-badge">{ms_icon("edit_note", 20)}</span>
                <h3>Evaluación individual</h3>
            </div>
            <p class="panel-desc">Capture el estilo de aprendizaje y el puntaje de admisión para obtener una proyección inmediata de la nota final.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        opciones_felder = ['sensorial', 'activo', 'visual', 'equilibrio', 'secuencial', 'reflexivo', 'verbal', 'intuitivo']
        felder_input = st.selectbox("Estilo de aprendizaje (Felder):", opciones_felder)
    with col2:
        examen_input = st.number_input("Puntaje de Admisión:", min_value=0.0, max_value=5.0, value=3.83, step=0.01)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Ejecutar Modelo Predictivo", key="btn_manual"):
        df_input_manual = pd.DataFrame({'Felder': [felder_input], 'Examen_admisión': [examen_input]})
        try:
            with st.spinner('Analizando perfil del estudiante...'):
                df_procesado = procesar_datos(df_input_manual)
                prediccion = model.predict(df_procesado)
                
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">{ms_icon("query_stats", 16)} Resultado de inferencia</div>
                <div class="result-title">Nota final estimada</div>
                <div class="result-score">
                    <span class="score-value">{prediccion[0]:.2f}</span>
                    <span class="score-scale">/ 5.00</span>
                </div>
                <div class="score-hint">Proyección generada por el ensamble Bagging a partir del perfil ingresado.</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Ver matriz de datos procesados"):
                st.dataframe(df_procesado)
        except Exception as e:
            st.error(f"Ocurrió un error en el motor de inferencia: {e}")

def render_analisis_masivo():
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">
                <span class="icon-badge">{ms_icon("upload_file", 20)}</span>
                <h3>Análisis masivo de estudiantes</h3>
            </div>
            <p class="panel-desc">Cargue un archivo Excel para evaluar un cohort completo y consolidar las predicciones en un reporte tabular.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    archivo_subido = st.file_uploader("Cargar dataset (.xlsx) para evaluación por lotes:", type=["xlsx", "xls"])
    
    if archivo_subido is not None:
        try:
            df_excel = pd.read_excel(archivo_subido)
            with st.expander("Vista previa de datos originales", expanded=False):
                st.dataframe(df_excel.head())
            
            if st.button("Generar Reporte Predictivo", key="btn_batch"):
                with st.spinner('Procesando pipeline de datos y ejecutando predicciones...'):
                    df_procesado_batch = procesar_datos(df_excel)
                    predicciones = model.predict(df_procesado_batch)
                    
                    df_resultados = df_excel.copy()
                    df_resultados['Predicción_Nota_Final'] = predicciones.round(2)
                    
                    st.success("Análisis masivo completado exitosamente.")
                    st.markdown(
                        f"""
                        <div class="section-heading">
                            {ms_icon("table_chart", 20)}
                            <h5>Resultados consolidados</h5>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.dataframe(df_resultados, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error crítico al procesar el archivo: {e}")

if HAS_OPTION_MENU:
    st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)
    seccion = option_menu(
        menu_title=None,
        options=["Ingreso Manual", "Procesamiento por Lotes"],
        icons=["pencil-square", "file-earmark-spreadsheet"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0",
                "background-color": "transparent",
                "border-bottom": "1px solid #D7DEE8",
            },
            "icon": {"color": "#0E7C86", "font-size": "16px"},
            "nav-link": {
                "font-family": "IBM Plex Sans, sans-serif",
                "font-size": "0.95rem",
                "font-weight": "600",
                "color": "#6B7C93",
                "padding": "0.75rem 1.1rem",
                "border-radius": "0",
                "margin": "0 0.15rem",
                "--hover-color": "#E8EEF5",
            },
            "nav-link-selected": {
                "background-color": "transparent",
                "color": "#12233A",
                "border-bottom": "3px solid #0E7C86",
                "font-weight": "700",
            },
        },
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if seccion == "Ingreso Manual":
        render_evaluacion_individual()
    else:
        render_analisis_masivo()
else:
    tab1, tab2 = st.tabs([
        ":material/edit_note: Ingreso Manual",
        ":material/upload_file: Procesamiento por Lotes (Excel)",
    ])
    with tab1:
        render_evaluacion_individual()
    with tab2:
        render_analisis_masivo()

st.markdown(
    f"""
    <div class="footer-note">
        {ms_icon("verified", 16)}
        Academic Performance Intelligence · Seminario de Machine Learning · Uso interno para stakeholders
    </div>
    """,
    unsafe_allow_html=True
)
