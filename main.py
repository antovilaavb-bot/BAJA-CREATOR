import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Confital Wave Designer Pro", layout="wide")

st.sidebar.header("🎛️ Controles de Ingeniería")
h = st.sidebar.slider("Altura del Swell", 1.0, 6.0, 3.5)
c = st.sidebar.slider("Potencia del Tubo", 0.5, 4.0, 2.8)
s = st.sidebar.slider("Velocidad Mar", 0.5, 3.0, 1.5)

three_js_code = f"""
<div id="container" style="width: 100%; height: 600px; border-radius: 20px; overflow: hidden;"></div>

<script type="importmap">
  {{ "imports": {{ "three": "https://unpkg.com/three@0.160.0/build/three.module.js" }} }}
</script>

<script type="module">
    import * as THREE from 'three';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x112233); // Fondo oscuro para resaltar el agua

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 600, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(window.innerWidth, 600);
    document.getElementById('container').appendChild(renderer.domElement);

    // --- SHADER PERSONALIZADO (Crea la espuma y el color pro) ---
    const waveShader = {{
        uniforms: {{
            uTime: {{ value: 0 }},
            uHeight: {{ value: {h} }},
            uCurl: {{ value: {c} }}
        }},
        vertexShader: `
            varying float vHeight;
            varying vec2 vUv;
            uniform float uTime;
            uniform float uHeight;
            uniform float uCurl;

            void main() {{
                vUv = uv;
                vec3 pos = position;
                
                // Algoritmo de Tubo
                float phase = pos.y * 0.2 + uTime;
                float wave = sin(phase);
                pos.z = wave * uHeight;

                // Proyección del labio para el tubo
                if (pos.z > 0.0) {{
                    float lip = pow(pos.z / uHeight, 2.0);
                    pos.x += lip * uCurl;
                }}

                vHeight = pos.z;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
            }}
        `,
        fragmentShader: `
            varying float vHeight;
            uniform float uHeight;
            
            void main() {{
                // Color base: Azul profundo
                vec3 deepBlue = vec3(0.02, 0.15, 0.3);
                // Color medio: Turquesa Confital
                vec3 turquoise = vec3(0.1, 0.7, 0.8);
                // Color cresta: Espuma blanca
                vec3 foam = vec3(1.0, 1.0, 1.0);

                float mixFactor = (vHeight + uHeight) / (uHeight * 2.0);
                vec3 color = mix(deepBlue, turquoise, mixFactor);

                // Si está cerca de la cresta, añadir espuma
                if (vHeight > uHeight * 0.8) {{
                    color = mix(color, foam, (vHeight - uHeight *
