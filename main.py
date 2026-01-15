import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Confital Designer Pro", layout="wide")

# --- 1. MOTOR DE DATOS REALES (API) ---
def get_real_swell():
    lat, lon = 28.17, -15.43 # El Confital
    url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height,wave_period&timezone=auto"
    try:
        res = requests.get(url).json()
        return res['hourly']['wave_height'][0], res['hourly']['wave_period'][0]
    except:
        return 1.5, 12.0 # Valores por defecto si falla la API

# --- 2. LÓGICA DE FÍSICA Y OPTIMIZACIÓN ---
def calcular_iribarren(h, periodo, pendiente):
    L0 = (9.81 * (periodo**2)) / (2 * np.pi) # Longitud de onda en aguas profundas
    esbeltez = h / L0
    xi = (1/pendiente) / np.sqrt(esbeltez)
    return xi

# --- 3. INTERFAZ DE USUARIO (SIDEBAR) ---
st.sidebar.title("🎮 Panel de Control")
if st.sidebar.button("📡 Cargar Swell Real"):
    h_api, t_api = get_real_swell()
    st.session_state.h = h_api
    st.session_state.t = t_api

h = st.sidebar.slider("Altura de Ola (m)", 0.5, 5.0, st.session_state.get('h', 1.5))
t = st.sidebar.slider("Periodo (s)", 4, 20, st.session_state.get('t', 12))
marea = st.sidebar.slider("Marea (m)", -1.5, 1.5, 0.0)
m = st.sidebar.slider("Pendiente Laja (1:X)", 5, 40, 12)

# --- 4. CÁLCULOS Y DIAGNÓSTICO ---
xi = calcular_iribarren(h, t, m)
st.title("🌊 Wave Engineering: El Confital")
col1, col2, col3 = st.columns(3)
col1.metric("Iribarren (ξ)", f"{xi:.2f}")
col2.metric("Swell", f"{h}m @ {t}s")
col3.metric("Estado", "TUBO" if 1.2 < xi < 2.5 else "DERRAME")

# --- 5. VISUALIZACIÓN 3D INTERACTIVA ---
st.subheader("🔭 Modelo Geométrico 3D")

x = np.linspace(0, 100, 100)
y_cross = np.linspace(0, 30, 30)
X, Y = np.meshgrid(x, y_cross)

# Generar fondo con escalón (Laja)
fondo_base = np.full(100, 12.0)
fondo_base[50:] = 2.5 + marea
Z_fondo = np.tile(-fondo_base, (30, 1))

# Generar Ola (Simulación de cresta)
fase = h * np.sin(X/5) * np.exp(-(X-55)**2 / 300)
Z_agua = np.tile(fase, (1, 1)) 

fig = go.Figure(data=[
    # Fondo Rocoso
    go.Surface(z=Z_fondo, x=X, y=Y, colorscale='Turbid', showscale=False, name="Fondo"),
    # Superficie del Agua
    go.Surface(z=Z_agua, x=X, y=Y, colorscale='Blues', opacity=0.8, name="Ola")
])

fig.update_layout(scene=dict(zaxis=dict(range=[-15, 7])), margin=dict(l=0, r=0, b=0, t=0))
st.plotly_chart(fig, use_container_width=True)

# --- 6. EXPORTACIÓN ---
st.divider()
if st.button("💾 Exportar Diseño para Fabricación"):
    df = pd.DataFrame({'distancia': x, 'profundidad': fondo_base})
    st.download_button("Descargar CSV", df.to_csv(), "diseño_laja.csv", "text/csv")
    st.success("Datos listos para CNC/Impresión 3D")
