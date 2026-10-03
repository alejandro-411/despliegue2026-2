import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Configuración inicial de la página (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="Predicción de Aprobación",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inyección de CSS (Estilo profesional tipo SCSS) e Íconos (FontAwesome)
def inyectar_estilos():
    estilo_css = """
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Variables de tema (Simulando SCSS) */
    :root {
        --primary-blue: #0A3D62;
        --secondary-blue: #3C6382;
        --accent-color: #0ABDE3;
        --bg-light: #F8F9FA;
        --text-dark: #2C3E50;
        --success-color: #10AC84;
        --border-radius: 8px;
    }

    /* Tipografía global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-dark);
    }

    /* Títulos personalizados con íconos */
    .main-title {
        color: var(--primary-blue);
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 10px;
        border-bottom: 3px solid var(--accent-color);
    }
    
    .subtitle {
        color: var(--secondary-blue);
        font-weight: 400;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Estilización de Botones */
    .stButton > button {
        background-color: var(--primary-blue);
        color: white;
        font-weight: 600;
        border-radius: var(--border-radius);
        border: none;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease-in-out;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: var(--accent-color);
        color: white;
        box-shadow: 0 4px 12px rgba(10, 189, 227, 0.4);
        transform: translateY(-2px);
    }

    /* Alertas y Success Messages */
    .stAlert {
        border-left: 5px solid var(--success-color);
        border-radius: var(--border-radius);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Contenedores de pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: var(--bg-light);
        border-radius: var(--border-radius) var(--border-radius) 0 0;
        border: 1px solid #E1E8ED;
        border-bottom: none;
        font-weight: 600;
        color: var(--secondary-blue);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-blue) !important;
        color: white !important;
    }
    </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)

inyectar_estilos()

# Encabezado Principal de la App
st.markdown('<div class="main-title"><i class="fa-solid fa-chart-line"></i> Dashboard de Predicción de Rendimiento Académico</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistema de Inteligencia Artificial para estimar la calificación final de los estudiantes basado en perfiles de aprendizaje y admisión.</div>', unsafe_allow_html=True)

# Cargar los recursos (modelos y transformadores) una sola vez
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

# Función modular para procesar datos
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

# Crear pestañas para la UI
tab1, tab2 = st.tabs(["✍️ Ingreso Manual", "📁 Procesamiento por Lotes (Excel)"])

with tab1:
    st.markdown('<h3><i class="fa-solid fa-user-pen"></i> Evaluación Individual</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        opciones_felder = ['sensorial', 'activo', 'visual', 'equilibrio', 'secuencial', 'reflexivo', 'verbal', 'intuitivo']
        felder_input = st.selectbox("Estilo de aprendizaje (Felder):", opciones_felder)
    with col2:
        examen_input = st.number_input("Puntaje de Admisión:", min_value=0.0, max_value=5.0, value=3.83, step=0.01)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Ejecutar Modelo Predictivo"):
        df_input_manual = pd.DataFrame({'Felder': [felder_input], 'Examen_admisión': [examen_input]})
        try:
            with st.spinner('Analizando perfil del estudiante...'):
                df_procesado = procesar_datos(df_input_manual)
                prediccion = model.predict(df_procesado)
                
            st.markdown(f"""
            <div style='background-color: #E8F8F5; padding: 20px; border-radius: 8px; border-left: 5px solid #10AC84;'>
                <h4 style='color: #10AC84; margin-top: 0;'><i class="fa-solid fa-bullseye"></i> Resultado de la Predicción</h4>
                <p style='font-size: 1.2rem; margin-bottom: 0;'>Nota Final Estimada: <strong>{prediccion[0]:.2f} / 5.00</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Ver matriz de datos procesados"):
                st.dataframe(df_procesado)
        except Exception as e:
            st.error(f"Ocurrió un error en el motor de inferencia: {e}")

with tab2:
    st.markdown('<h3><i class="fa-solid fa-file-excel"></i> Análisis Masivo de Estudiantes</h3>', unsafe_allow_html=True)
    archivo_subido = st.file_uploader("Cargar dataset (.xlsx) para evaluación por lotes:", type=["xlsx", "xls"])
    
    if archivo_subido is not None:
        try:
            df_excel = pd.read_excel(archivo_subido)
            with st.expander("Vista previa de datos originales", expanded=False):
                st.dataframe(df_excel.head())
            
            if st.button("Generar Reporte Predictivo"):
                with st.spinner('Procesando pipeline de datos y ejecutando predicciones...'):
                    df_procesado_batch = procesar_datos(df_excel)
                    predicciones = model.predict(df_procesado_batch)
                    
                    df_resultados = df_excel.copy()
                    df_resultados['Predicción_Nota_Final'] = predicciones.round(2)
                    
                    st.success("¡Análisis masivo completado exitosamente!")
                    st.markdown('<h5><i class="fa-solid fa-table-list"></i> Resultados Consolidados</h5>', unsafe_allow_html=True)
                    st.dataframe(df_resultados, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error crítico al procesar el archivo: {e}")
