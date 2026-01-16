import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Confital Physics Render Pro", layout="wide")

st.sidebar.header("🛠️ Configuración del Motor")
n_particles = st.sidebar.select_slider("Número de Esferas (Física)", options=[100, 300, 600, 1000], value=600)
reef_height = st.sidebar.slider("Altura de la 'Baja' (Arrecife)", 0.0, 5.0, 3.5)
particle_size = st.sidebar.slider("Tamaño del Spray", 0.05, 0.3, 0.12)

three_js_code = f"""
<div id="container" style="width: 100%; height: 650px; background: radial-gradient(circle, #1a2a6c, #b21f1f, #fdbb2d);"></div>

<script type="importmap">
  {{ "imports": {{ "three": "https://unpkg.com/three@0.160.0/build/three.module.js" }} }}
</script>

<script type="module">
    import * as THREE from 'three';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 650, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(window.innerWidth, 650);
    renderer.shadowMap.enabled = true;
    document.getElementById('container').appendChild(renderer.domElement);

    // 1. RENDER DE ALTA: InstancedMesh (Cada partícula es una esfera 3D real)
    const sphereGeo = new THREE.SphereGeometry({particle_size}, 8, 8);
    const sphereMat = new THREE.MeshPhysicalMaterial({{
        color: 0xffffff,
        transmission: 0.6,
        thickness: 0.5,
        roughness: 0.0,
        metalness: 0.1,
        ior: 1.33
    }});

    const count = {n_particles};
    const mesh = new THREE.InstancedMesh(sphereGeo, sphereMat, count);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    // 2. LA BAJA (Caja de colisión del Confital)
    const reefGeo = new THREE.BoxGeometry(10, {reef_height}, 30);
    const reefMat = new THREE.MeshStandardMaterial({{ color: 0x221100, roughness: 1.0 }});
    const reef = new THREE.Mesh(reefGeo, reefMat);
    reef.position.set(10, {reef_height}/2 - 2, 0);
    scene.add(reef);

    // Luces de escena para realismo 3D
    const mainLight = new THREE.DirectionalLight(0xffffff, 2);
    mainLight.position.set(20, 30, 10);
    scene.add(mainLight);
    scene.add(new THREE.AmbientLight(0x404040, 1.5));

    // Datos de partículas
    const dummy = new THREE.Object3D();
    const pData = Array.from({{ length: count }}, () => ({{
        pos: new THREE.Vector3((Math.random()-0.5)*50, Math.random()*5, (Math.random()-0.5)*30),
        vel: new THREE.Vector3(-0.1, 0, 0)
    }}));

    camera.position.set(25, 15, 30);
    camera.lookAt(0, 0, 0);

    function animate(time) {{
        requestAnimationFrame(animate);
        const t = time * 0.001;

        for (let i = 0; i < count; i++) {{
            let p = pData[i];
            
            // FÍSICA: Movimiento circular (Swell)
            p.pos.y += Math.sin(p.pos.x * 0.2 + t) * 0.05;
            p.pos.x += p.vel.x;

            // COLISIÓN: Si choca con el arrecife, sube y se convierte en spray
            if (p.pos.x > 5 && p.pos.x < 15) {{
                if (p.pos.y < {reef_height} - 2) {{
                    p.pos.y += 0.2; // La ola sube por el fondo
                    p.vel.x = -0.15; // Proyección hacia adelante (Tubo)
                }}
            }}

            // Gravedad básica
            if (p.pos.y > 0) p.pos.y -= 0.01;

            // Reset
            if (p.pos.x < -25) p.pos.x = 25;

            dummy.position.copy(p.pos);
            dummy.updateMatrix();
            mesh.setMatrixAt(i, dummy.instanceMatrix);
        }}
        
        mesh.instanceMatrix.needsUpdate = true;
        renderer.render(scene, camera);
    }}
    animate();
</script>
"""

components.html(three_js_code, height=670)

st.write("### Explicación del Motor Profesional")
st.markdown("""
- **InstancedMesh:** Es la técnica que usan los videojuegos para renderizar miles de objetos iguales (como balas o gotas) sin que el PC explote.
- **Physics Engine:** Las partículas detectan la posición del cubo (`reef`). Cuando entran en su zona, su vector de velocidad cambia para subir y luego caer, simulando el labio del tubo.
- **Render de Alta:** El material `MeshPhysicalMaterial` calcula cómo la luz atraviesa cada gota.
""")
