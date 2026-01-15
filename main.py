import streamlit as st
import pandas as pd
import numpy as np
import requests

# 1. ESTILO Y CONFIGURACIÓN
st.set_page_config(page_title="BAJA-CREATOR PRO", layout="wide", page_icon="🌊")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { border: 1px solid #00d4ff; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON SATÉLITE (API)
@st.cache_data(ttl=3600)
def get_data():
    try:
        # Consulta a Open-Meteo para El Confital
        r = requests.get("https://api.open-meteo.com/v1/marine?latitude=28.17&longitude=-15.43&hourly=wave_height,wave_period&timezone=auto").json()
        return r['hourly']['wave_height'][0], r['hourly']['wave_period'][0]
    except:
        return 1.5, 12.0

h_api, p_api = get_data()

# 3. INTERFAZ PRINCIPAL
st.title("🌊 BAJA-CREATOR | Ocean Intelligence")
st.write("Análisis de dinámica de fluidos y predicción de oleaje en tiempo real.")

# Columnas de métricas
c1, c2, c3 = st.columns(3)
c1.metric("Altura Actual (API)", f"{h_api} m")
c2.metric("Periodo Actual (API)", f"{p_api} s")
c3.metric("Ubicación", "El Confital", "GC")

st.divider()

# 4. CONTROLES Y GRÁFICO
col_control, col_grafico = st.columns([1, 2])

with col_control:
    st.subheader("🛠️ Simulación")
    h_sim = st.slider("Altura de Ola (m)", 0.0, 5.0, float(h_api))
    p_sim = st.slider("Periodo (s)", 4, 20, int(p_api))
    
    # Cálculo técnico
    energia = (h_sim**2) * p_sim
    st.info(f"**Energía estimada:** {energia:.1f} kJ/m")
    
    if p_sim > 13:
        st.success("🔥 Swell de largo periodo: Calidad Épica")

with col_grafico:
    st.subheader("📉 Curva de Potencia en la Laja")
    # Generamos datos de la curva
    x = np.linspace(0, 50, 50)
    y = (h_sim * p_sim) / (x + 1)
    df_plot = pd.DataFrame({"Distancia (m)": x, "Potencia": y}).set_index("Distancia (m)")
    st.area_chart(df_plot, color="#00d4ff")

# 5. MAPA DE POSICIONAMIENTO
st.subheader("📍 Coordenadas de Análisis")
st.map(pd.DataFrame({'lat': [28.175], 'lon': [-15.437]}), zoom=14)
