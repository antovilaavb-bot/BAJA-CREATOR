import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# 1. CONFIGURACIÓN DE INTERFAZ DE ALTO NIVEL
st.set_page_config(
    page_title="BAJA-CREATOR | Pro Wave Intelligence",
    page_icon="🌊",
    layout="wide"
)

# Estética Profesional (Modo Oscuro Forzado)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    div[data-testid="stMetricValue"] { color: #00d4ff; font-family: monospace; }
    .stPlotlyChart { border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE DATOS (CONEXIÓN API SATELITAL)
@st.cache_data(ttl=3600)
def fetch_marine_data():
    # Coordenadas exactas de El Confital (La Laja)
    lat, lon = 28.17, -15.43
    url = f"https://api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height,wave_period,wave_direction&timezone=auto"
    try:
        response = requests.get(url).json()
        current_h = response['hourly']['wave_height'][0]
        current_p = response['hourly']['wave_period'][0]
        return current_h, current_p
    except:
        return 1.2, 11.0 # Valores de respaldo (Backup)

h_real, p_real = fetch_marine_data()

# 3. BARRA LATERAL (CONTROL DE INGENIERÍA)
st.sidebar.header("🛠️ Parámetros de Simulación")
st.sidebar.markdown("Ajusta las variables para ver el comportamiento del swell en la baja.")

h_sim = st.sidebar.slider("Altura de Ola (m)", 0.0, 5.0, float(h_real))
p_sim = st.sidebar.slider("Periodo (s)", 4, 22, int(p_real))
coef_marea = st.sidebar.select_slider("Coeficiente de Marea", options=["Baja", "Media", "Alta"])

# 4. DASHBOARD PRINCIPAL
st.title("🌊 BAJA-CREATOR PRO")
st.caption(f"Sincronizado con estación meteorológica local | {datetime.now().strftime('%H:%M')} GMT")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Altura Swell", f"{h_sim} m")
col2.metric("Periodo", f"{p_sim} s")
col3.metric("Energía", f"{(h_sim**2 * p_sim):.1f} kJ/m")
col4.metric("Estado", "Óptimo" if p_sim > 12 else "Regular")

st.markdown("---")

# 5. MAPA Y ANÁLISIS DE ENERGÍA
c1, c2 = st.columns([1, 1])  # <-- FALTA EL "st.columns([1, 1])"

with c1:
    st.subheader("📍 Ubicación de la Baja")

