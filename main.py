import streamlit as st

st.set_page_config(page_title="Test")
st.title("🌊 BAJA-CREATOR: Conectado")
st.write("Si lees esto, el servidor funciona perfectamente.")

# Prueba de widgets
altura = st.slider("Prueba de control", 0, 10, 5)
st.metric("Nivel de señal", f"{altura} ok")
