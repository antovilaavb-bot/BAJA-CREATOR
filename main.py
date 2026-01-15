import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="BAJA-CREATOR | Ultra-Realism", layout="wide")

# --- CONTROLES PRO ---
with st.sidebar:
    st.header("🎛️ Ajustes de Realismo")
    h_ola = st.slider("Altura de Ola (m)", 1.0, 6.0, 3.5)
    tubo = st.slider("Proyección del Labio (Tubo)", 0.0, 3.0, 1.8)
    espuma = st.slider("Densidad de Espuma", 0.0, 1.0, 0.5)
    turbulencia = st.slider("Rugosidad del Fondo", 0.0, 1.0, 0.3)

# --- MOTOR DE GEOMETRÍA AVANZADA ---
n = 100
x = np.linspace(0, 100, n)
y = np.linspace(-40, 40, n)
X, Y = np.meshgrid(x, y)

# 1. FONDO VOLCÁNICO (Con ruido para realismo)
ruido_fondo = (np.random.rand(n, n) - 0.5) * turbulencia * 2
Z_fondo = -15 + (0.15 * X) + (5 * np.exp(-(X-70)**2/200 - Y**2/500)) + ruido_fondo
Z_fondo = np.minimum(Z_fondo, 0.1)

# 2. LA OLA (Cilindro matemático)
# Creamos la forma de la ola
fase = (X - 70) / 10
# Esta fórmula genera la "C" del tubo
Z_ola = h_ola * np.exp(-fase**2) * np.cos(Y/25) 
# Deformación del labio (lo que crea el efecto visual de la imagen)
X_deformado = X + (tubo * Z_ola * np.clip(fase + 1, 0, 1))

# 3. CAPA DE ESPUMA (Segunda superficie para realismo)
Z_espuma = np.where(Z_ola > (h_ola * 0.8), Z_ola + 0.2, np.nan)

# --- RENDERIZADO ---
fig = go.Figure()

# Superficie del Fondo (Roca)
fig.add_trace(go.Surface(
    z=Z_fondo, x=X, y=Y,
    colorscale='Greys', showscale=False, opacity=1,
    name="Fondo Volcánico"
))

# Superficie de la Ola (Agua profunda)
fig.add_trace(go.Surface(
    z=Z_ola, x=X_deformado, y=Y,
    colorscale='Blues', opacity=0.8, showscale=False,
    name="Cuerpo de la Ola"
))

# Superficie de Espuma (Blanco vibrante)
if espuma > 0:
    fig.add_trace(go.Surface(
        z=Z_espuma, x=X_deformado, y=Y,
        colorscale=[[0, 'white'], [1, 'white']],
        opacity=espuma, showscale=False, name="Espuma"
    ))

fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(range=[-20, 10], backgroundcolor="rgb(10, 10, 20)"),
        aspectratio=dict(x=1.5, y=1, z=0.5),
        camera=dict(eye=dict(x=1.2, y=-1.4, z=0.6))
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=800,
    paper_bgcolor='black'
)

st.plotly_chart(fig, use_container_width=True)
