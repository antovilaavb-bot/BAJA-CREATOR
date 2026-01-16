import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página profesional
st.set_page_config(page_title="Confital Wave Designer Pro", layout="wide")

st.title("🌊 Confital Wave Designer Pro")
st.sidebar.header("Parámetros de la Ola")

# Controles de usuario (UI Profesional)
h = st.sidebar.slider("Altura de la Ola (m)", 1.0, 8.0, 4.0)
s = st.sidebar.slider("Velocidad del Periodo", 0.5, 3.0, 1.8)
c = st.sidebar.slider("Curvatura del Tubo", 1.0, 5.0, 2.5)
t_val = st.sidebar.slider("Cierre del Tubo (Tightness)", 0.1, 0.8, 0.3)

# El código HTML/Three.js embebido
three_js_code = f"""
<div id="container"></div>
<script type="importmap">
  {{
    "imports": {{
      "three": "https://unpkg.com/three@0.160.0/build/three.module.js"
    }}
  }}
</script>
<script type="module">
    import * as THREE from 'three';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('container').appendChild(renderer.domElement);

    // Material con Transparencia y DoubleSide (Back-face Culling OFF)
    const material = new THREE.MeshPhysicalMaterial({{
        color: 0x00aaff,
        transmission: 0.9,
        thickness: 1.5,
        roughness: 0.05,
        transparent: true,
        opacity: 0.8,
        side: THREE.DoubleSide
    }});

    const geometry = new THREE.PlaneGeometry(60, 100, 120, 120);
    const sea = new THREE.Mesh(geometry, material);
    sea.rotation.x = -Math.PI / 2;
    scene.add(sea);

    const sun = new THREE.DirectionalLight(0xffffff, 1.5);
    sun.position.set(10, 20, 10);
    scene.add(sun);
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));

    camera.position.set(5, 5, 25);
    camera.lookAt(0, 0, 0);

    function animate(time) {{
        requestAnimationFrame(animate);
        const t = time * 0.001 * {s};
        const pos = sea.geometry.attributes.position.array;

        for (let i = 0; i < pos.length; i += 3) {{
            let x = pos[i];
            let y = pos[i + 1];

            const waveFace = Math.sin(y * {t_val} + t);
            pos[i + 2] = waveFace * {h};

            // Efecto Tubo
            if (pos[i + 2] > 0.5) {{ 
                const lip = Math.pow(pos[i + 2] / {h}, 2);
                pos[i] = x + (lip * {c});
            }}
        }}
        sea.geometry.attributes.position.needsUpdate = true;
        renderer.render(scene, camera);
    }}
    animate();
</script>
<style>
    body {{ margin: 0; overflow: hidden; }}
    canvas {{ width: 100% !important; height: 500px !important; border-radius: 15px; }}
</style>
"""

# Renderizar el componente
components.html(three_js_code, height=550)

st.info("💡 Consejo Pro: Usa los controles laterales para ajustar el labio de la ola y generar el tubo perfecto.")
