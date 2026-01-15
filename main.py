import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="BAJA-CREATOR | Tube Designer", layout="wide")

st.title("📐 Simulador de Morfología de Ola y Fondo")

# --- CONTROLES DE DISEÑO ---
st.sidebar.header("Configuración de la Baja")
tipo_fondo = st.sidebar.selectbox("Tipo de Fondo", ["Rampa Plana", "Escalón (Step)", "Pico (A-Frame)"])
pendiente = st.sidebar.slider("Pendiente del fondo (%)", 5, 30, 15)
st.sidebar.markdown("---")
st.sidebar.header("Dinámica del Labio")
agresividad = st.sidebar.slider("Agresividad del Tubo", 0.1, 2.0, 1.0)
altura_ola = st.sidebar.slider("Altura (m)", 1.0, 8.0, 3.0)

# --- MOTOR GEOMÉTRICO ---
x = np.linspace(0, 60, 100)
y = np.linspace(-20, 20, 100)
X, Y = np.meshgrid(x, y)

# 1. Modelado del fondo (La Baja)
if tipo_fondo == "Rampa Plana":
    Z_fondo = -(20 - (pendiente/100 * X))
elif tipo_fondo == "Escalón (Step)":
    Z_fondo = np.where(X < 30, -15, -2)
else: # Pico
    Z_fondo = -(15 - (pendiente/100 * X)) + (np.abs(Y)/2)

Z_fondo = np.maximum(Z_fondo, -0.5)

# 2. Modelado del Tubo (El Labio)
# Creamos una deformación que lanza el "Z" hacia arriba y el "X" hacia adelante
Z_ola = np.zeros_like(X)
# Punto de rotura (donde el fondo es poco profundo)
mask_rompiente = X > 35 

# Ecuación para el "labio" de la ola
# Usamos una campana de Gauss deformada para simular el cilindro
Z_ola = (altura_ola * np.exp(-(X-40)**2 / 20)) * (1 / (1 + np.abs(Y)/10))

# Simulamos el "labio" lanzándose hacia adelante
X_deformado = X + (Z_ola * agresividad) 

# --- RENDERIZADO 3D ---
fig = go.Figure()

# Dibujamos el Fondo
fig.add_trace(go.Surface(z=Z_fondo, x=X, y=Y, colorscale='Greys', opacity=0.8, showscale=False, name="Fondo"))

# Dibujamos la Ola con la deformación del labio
fig.add_trace(go.Surface(z=Z_ola, x=X_deformado, y=Y, colorscale='Blues', opacity=0.9, name="Ola/Tubo"))

fig.update_layout(
    scene=dict(
        zaxis=dict(range=[-20, 10]),
        aspectratio=dict(x=1.5, y=1, z=0.5),
        camera=dict(eye=dict(x=1.2, y=-1.5, z=0.8))
    ),
    height=700,
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

st.info("💡 **Consejo Pro:** Mueve el slider de 'Agresividad del Tubo' para ver cómo el labio (la malla azul) se proyecta hacia adelante superando la base, creando el efecto visual del tubo.")
