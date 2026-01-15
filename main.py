import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="BAJA-CREATOR | Dynamic Wave Simulator", layout="wide", page_icon="🌊")

st.title("🌊 BAJA-CREATOR: Simulador Dinámico de Ola y Batimetría")
st.write("Ajusta el fondo marino y las características del swell para predecir el comportamiento de la rompiente.")

# 2. CONTROLES DE INGENIERÍA (BARRA LATERAL)
st.sidebar.header("🛠️ Parámetros de Diseño")
st.sidebar.markdown("**Fondo Marino (Batimetría):**")
pendiente_fondo = st.sidebar.slider("Inclinación del Fondo (%)", 1.0, 15.0, 7.0, help="Pendiente del fondo marino hacia la costa.")
profundidad_max_fondo = st.sidebar.slider("Profundidad Inicial (m)", 10, 40, 25, help="Profundidad máxima del área de simulación.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Características de la Ola (Swell):**")
altura_ola = st.sidebar.slider("Altura de Ola (m)", 0.5, 7.0, 2.5, help="Altura de la ola en aguas abiertas.")
periodo_ola = st.sidebar.slider("Periodo de Ola (s)", 5, 20, 12, help="Tiempo entre crestas de ola.")

# 3. MOTOR DE CÁLCULO FÍSICO (INTERACCIÓN OLA-FONDO)

# Malla para el fondo y la ola
x = np.linspace(0, 100, 70)  # Distancia hacia la costa (más detalle)
y = np.linspace(0, 50, 40)   # Ancho de la sección
X, Y = np.meshgrid(x, y)

# Cálculo del Fondo Marino (la 'baja')
Z_fondo = -(profundidad_max_fondo - (pendiente_fondo/100 * X))
Z_fondo = np.maximum(Z_fondo, -0.2) # Evitar que el fondo suba por encima del nivel del mar

# Cálculo de la Ola (interactuando con el fondo)
# La ola crece y se deforma al acercarse a la poca profundidad
# Usamos una función que simula el incremento de altura y la ruptura
profundidad_relativa = -Z_fondo # Profundidad actual en cada punto
altura_relativa = altura_ola * (1 + (periodo_ola / 20) * np.exp(-profundidad_relativa / 10))
# La ola rompe cuando la profundidad es menor a 1.3 veces la altura de ola
Z_ola_surface = np.sin((X/periodo_ola) * 2 * np.pi + Y/10) * altura_relativa * np.exp(-X/40) # Forma sinusoidal de la ola
Z_ola_surface[profundidad_relativa < (altura_relativa * 0.8)] *= 0.5 # Efecto de rompiente visual

# Ajuste visual para que la ola no esté por debajo del nivel del mar en la rompiente
Z_ola_surface = np.maximum(Z_ola_surface, 0) 


# 4. VISUALIZADOR 3D PROFESIONAL CON PLOTLY
st.subheader("Visualización 3D Dinámica de la Ola y el Fondo")

fig = go.Figure(data=[
    # Capa del Fondo Marino (color tierra/gris)
    go.Surface(z=Z_fondo, x=X, y=Y, colorscale='Greys_r', showscale=False, name="Fondo Marino", opacity=0.9),
    # Capa de la Ola (azul)
    go.Surface(z=Z_ola_surface, x=X, y=Y, colorscale='Blues', opacity=0.7, name="Ola Rompiente")
])

fig.update_layout(
    scene=dict(
        xaxis_title='Distancia a la Costa (m)',
        yaxis_title='Ancho del Frente de Ola (m)',
        zaxis_title='Altura/Profundidad (m)',
        zaxis=dict(range=[-profundidad_max_fondo, altura_ola * 2]), # Rango para ver todo el espectro
        aspectratio=dict(x=1.5, y=0.8, z=0.4), # Ajusta la perspectiva 3D
        camera=dict(eye=dict(x=1.8, y=1.8, z=0.5)) # Posición inicial de la cámara
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=700,
    paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente para Streamlit
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)

# 5. RESUMEN DE INGENIERÍA Y ALERTAS
st.markdown("---")
col_info, col_metrics = st.columns(2)

with col_info:
    st.info("### 📊 Análisis de Rompiente")
    st.write(f"Con una **pendiente del {pendiente_fondo:.1f}%** y una ola de **{altura_ola:.1f}m** y **{periodo_ola}s**, la ola tiende a ser de tipo **{ 'tubera (Plunging)' if pendiente_fondo > 10 else 'murallera (Spilling)' }**.")
    st.write("La interacción del periodo con la batimetría define la potencia y forma del rompiente.")

with col_metrics:
    distancia_rompiente_estimada = (profundidad_max_fondo / (pendiente_fondo/100)) - (altura_ola * 2) # Estimación
    st.metric("Distancia Estimada de Impacto (desde inicio)", f"{max(0, distancia_rompiente_estimada):.1f} metros")
    st.metric("Profundidad Crítica de Rompiente", f"{altura_ola * 1.3:.1f} metros")
    st.metric("Energía Calculada de la Ola", f"{altura_ola**2 * periodo_ola:.1f} kJ/m")
