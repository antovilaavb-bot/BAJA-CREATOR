import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="BAJA-CREATOR | El Confital", layout="wide")

st.title("📐 Simulación de Batimetría: La Baja del Confital")
st.write("Modelado de la plataforma volcánica y el labio de la ola en la sección de la 'Laja'.")

# --- CONTROLES DE INGENIERÍA ---
with st.sidebar:
    st.header("Configuración del Spot")
    marea = st.slider("Nivel de Marea (m)", 0.0, 3.0, 1.5, help="Afecta a la profundidad sobre la laja")
    intensidad_swell = st.slider("Swell (m)", 1.0, 6.0, 3.0)
    proyeccion_labio = st.slider("Proyección del Labio (Tubo)", 0.5, 2.5, 1.2)
    st.markdown("---")
    st.info("La baja del Confital se caracteriza por un fondo de roca volcánica muy somero que genera una ola de alta energía.")

# --- MOTOR DE MODELADO (EL CONFITAL) ---
x = np.linspace(0, 100, 120)  # De mar adentro hacia la costa
y = np.linspace(-30, 30, 100) # Ancho de la sección
X, Y = np.meshgrid(x, y)

# 1. Simulación de la Batimetría del Confital
# Creamos una plataforma que sube bruscamente (el escalón de roca)
profundidad_base = -18 + marea
# La "Laja": una elevación central más agresiva
laja = 12 * np.exp(-(X-70)**2 / 150 - (Y)**2 / 400)
# Pendiente general hacia la orilla
pendiente = 0.1 * X
Z_fondo = profundidad_base + laja + pendiente
Z_fondo = np.minimum(Z_fondo, 0.2) # Limitar a ras de agua

# 2. Dinámica de la Ola (Modelado del Tubo)
# La ola crece donde la profundidad es menor (sobre la laja)
amplitud_ola = intensidad_swell * np.exp(-(X-72)**2 / 40) * (1 / (1 + np.abs(Y)/15))
# Efecto 'Cilindro': Desplazamos la malla X según la altura Z para crear el tubo
X_tubo = X + (amplitud_ola * proyeccion_labio)
Z_ola = amplitud_ola

# --- RENDERIZADO 3D ---
fig = go.Figure()

# Fondo: Textura de Roca Volcánica (Grises oscuros)
fig.add_trace(go.Surface(
    z=Z_fondo, x=X, y=Y, 
    colorscale=[[0, '#000000'], [1, '#4d4d4d']], 
    showscale=False, name="Fondo (Roca)"
))

# Ola: Textura de Agua (Azules con transparencia)
fig.add_trace(go.Surface(
    z=Z_ola, x=X_tubo, y=Y, 
    colorscale='Blues', opacity=0.85, 
    name="Ola (Impacto)"
))

fig.update_layout(
    scene=dict(
        xaxis_title='Océano -> Costa',
        yaxis_title='Sección (Punta)',
        zaxis_title='Profundidad/Altura',
        zaxis=dict(range=[-20, 10]),
        aspectratio=dict(x=1.8, y=1, z=0.4),
        camera=dict(eye=dict(x=1.5, y=-1.5, z=0.6))
    ),
    height=750,
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# --- ANÁLISIS TÉCNICO ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Análisis de la Laja")
    st.write("El modelo muestra cómo la elevación central (la laja) concentra la energía. "
             "Al reducirse la profundidad bruscamente, la base de la ola se frena y el labio se proyecta.")
with col2:
    if proyeccion_labio > 1.5:
        st.warning("⚠️ CONDICIÓN DE TUBO: El labio supera la vertical de la base (Cilindro detectado).")
    else:
        st.info("ℹ️ CONDICIÓN DE PARED: Ola con sección abierta, ideal para maniobras.")
