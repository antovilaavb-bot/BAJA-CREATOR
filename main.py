import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium
import requests
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Confital Wave Designer Pro", layout="wide")

# 2. MOTOR DE CÁLCULO (Lógica de Ingeniería)
class WaveEngine:
    @staticmethod
    def calcular_profundidad_critica(h):
        return h * 1.28

    @staticmethod
    def get_score(h, t, v_dir, v_vel):
        score = 0
        if 1.5 <= h <= 3.0 and t >= 12: score += 50
        if 80 <= v_dir <= 140 and v_vel < 25: score += 50
        return score

# 3. INTERFAZ: BARRA LATERAL (Controles)
st.sidebar.title("🎮 Panel de Control")
st.sidebar.markdown("---")

# Selectores de Tiempo y Ubicación
modo_tiempo = st.sidebar.selectbox("Modo Temporal", ["Tiempo Real", "Previsión"])
v_vel = st.sidebar.slider("Intensidad Viento (km/h)", 0, 60, 15)
v_dir = st.sidebar.slider("Dirección Viento (°)", 0, 360, 100)

# 4. CUERPO PRINCIPAL: MAPA Y DASHBOARD
st.title("🌊 Confital Wave Designer Pro")
st.write("Suite de Inteligencia Costera y Diseño Batimétrico")

col_mapa, col_stats = st.columns([2, 1])

with col_mapa:
    m = folium.Map(location=[28.17, -15.43], zoom_start=14, tiles="CartoDB dark_matter")
    # Añadimos captura de clic
    mapa_output = st_folium(m, width="100%", height=400)

# 5. SIMULACIÓN 3D (Lógica de Visualización)
st.subheader("🛰️ Simulación de Interacción 3D")

# Generamos datos de prueba para el visualizador
x = np.linspace(0, 50, 50)
y = np.linspace(0, 30, 30)
X, Y = np.meshgrid(x, y)
# Simulamos una rampa batimétrica (laja)
Z_fondo = -0.1 * X + (np.sin(Y/5) * 0.5) 
Z_agua = np.exp(-((X-25)**2)/20) * 2 # Ola base

# Aplicamos efecto viento
factor_viento = 1.1 if 80 <= v_dir <= 140 else 0.9
Z_agua_viento = Z_agua * factor_viento

fig = go.Figure(data=[
    go.Surface(z=Z_fondo, x=X, y=Y, colorscale='Greys', showscale=False, opacity=0.8),
    go.Surface(z=Z_agua_viento, x=X, y=Y, colorscale='Blues', opacity=0.7)
])

fig.update_layout(scene=dict(aspectmode='manual', aspectratio=dict(x=2, y=1, z=0.5)),
                  paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0))

st.plotly_chart(fig, use_container_width=True)

# 6. ALERTAS Y KPI
score = WaveEngine.get_score(1.8, 14, v_dir, v_vel) # Ejemplo con 1.8m y 14s

if score >= 80:
    st.success(f"🔥 SESIÓN ÉPICA DETECTADA: Score {score}/100")
else:
    st.info(f"📊 Calidad del Spot: {score}/100")