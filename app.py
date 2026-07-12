import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Sistema Solar 3D",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Dados dos planetas
# (distância e raio em escala artística, não em proporção real,
#  para que tudo caiba na tela e fique visualmente interessante)
# ---------------------------------------------------------------------------
PLANETS = [
    {
        "id": "sun",
        "name": "Sol",
        "type": "star",
        "color": "#ffcc33",
        "emissive": "#ff9900",
        "radius": 6.0,
        "distance": 0,
        "orbit_speed": 0,
        "rotation_speed": 0.02,
        "moons": 0,
        "real_radius_km": "696.340",
        "real_distance": "—",
        "day_length": "27 dias (rotação)",
        "year_length": "—",
        "temp": "5.500 °C (superfície)",
        "description": "O Sol é a estrela no centro do nosso sistema solar. É uma esfera quente de plasma "
                       "que gera energia por fusão nuclear, transformando hidrogênio em hélio. Ele é "
                       "responsável por mais de 99% da massa de todo o sistema solar.",
        "facts": [
            "Sozinho, o Sol representa cerca de 99,86% da massa do sistema solar.",
            "A luz do Sol leva cerca de 8 minutos para chegar até a Terra.",
            "Sua temperatura no núcleo chega a 15 milhões de °C.",
        ],
    },
    {
        "id": "mercury",
        "name": "Mercúrio",
        "type": "planet",
        "color": "#9c9c9c",
        "emissive": "#000000",
        "radius": 0.9,
        "distance": 12,
        "orbit_speed": 4.15,
        "rotation_speed": 0.004,
        "moons": 0,
        "real_radius_km": "2.439,7",
        "real_distance": "57,9 milhões km",
        "day_length": "59 dias terrestres",
        "year_length": "88 dias terrestres",
        "temp": "-180 °C a 430 °C",
        "description": "Mercúrio é o menor planeta do sistema solar e o mais próximo do Sol. Não tem "
                       "atmosfera relevante, o que gera uma variação de temperatura extrema entre o dia e a noite.",
        "facts": [
            "Um dia em Mercúrio dura mais que seu próprio ano.",
            "É o planeta com a maior variação de temperatura do sistema solar.",
            "Sua superfície é cheia de crateras, parecida com a da Lua.",
        ],
    },
    {
        "id": "venus",
        "name": "Vênus",
        "type": "planet",
        "color": "#e8c27a",
        "emissive": "#000000",
        "radius": 1.4,
        "distance": 17,
        "orbit_speed": 1.62,
        "rotation_speed": -0.001,
        "moons": 0,
        "real_radius_km": "6.051,8",
        "real_distance": "108,2 milhões km",
        "day_length": "243 dias terrestres",
        "year_length": "225 dias terrestres",
        "temp": "~465 °C",
        "description": "Vênus é o planeta mais quente do sistema solar por causa de um efeito estufa intenso "
                       "causado por sua atmosfera densa de CO2. Gira ao contrário da maioria dos planetas.",
        "facts": [
            "É o planeta mais quente, mesmo sendo mais distante do Sol que Mercúrio.",
            "Gira em sentido retrógrado (ao contrário) em relação à maioria dos planetas.",
            "É o objeto mais brilhante do céu noturno depois da Lua.",
        ],
    },
    {
        "id": "earth",
        "name": "Terra",
        "type": "planet",
        "color": "#2b6ea8",
        "emissive": "#0a1a2a",
        "radius": 1.5,
        "distance": 23,
        "orbit_speed": 1.0,
        "rotation_speed": 0.02,
        "moons": 1,
        "real_radius_km": "6.371",
        "real_distance": "149,6 milhões km",
        "day_length": "24 horas",
        "year_length": "365,25 dias",
        "temp": "-88 °C a 58 °C",
        "description": "A Terra é o único planeta conhecido com vida. Sua atmosfera, água líquida e campo "
                       "magnético criam condições únicas que a tornam habitável.",
        "facts": [
            "É o único planeta que não recebeu o nome de uma divindade grega ou romana.",
            "71% da superfície é coberta por água.",
            "Possui um único satélite natural: a Lua.",
        ],
    },
    {
        "id": "mars",
        "name": "Marte",
        "type": "planet",
        "color": "#c1440e",
        "emissive": "#1a0500",
        "radius": 1.1,
        "distance": 29,
        "orbit_speed": 0.53,
        "rotation_speed": 0.018,
        "moons": 2,
        "real_radius_km": "3.389,5",
        "real_distance": "227,9 milhões km",
        "day_length": "24h 37min",
        "year_length": "687 dias terrestres",
        "temp": "-153 °C a 20 °C",
        "description": "Conhecido como o 'planeta vermelho' por causa do óxido de ferro em sua superfície. "
                       "Tem o maior vulcão e o maior cânion já descobertos no sistema solar.",
        "facts": [
            "Possui o Monte Olimpo, o maior vulcão do sistema solar.",
            "Tem duas luas pequenas: Fobos e Deimos.",
            "É o principal alvo de missões humanas de exploração espacial.",
        ],
    },
    {
        "id": "jupiter",
        "name": "Júpiter",
        "type": "planet",
        "color": "#c9a06b",
        "emissive": "#1a1208",
        "radius": 3.6,
        "distance": 40,
        "orbit_speed": 0.084,
        "rotation_speed": 0.04,
        "moons": 95,
        "real_radius_km": "69.911",
        "real_distance": "778,5 milhões km",
        "day_length": "9h 56min",
        "year_length": "11,9 anos terrestres",
        "temp": "~-108 °C (topo das nuvens)",
        "description": "Júpiter é o maior planeta do sistema solar, um gigante gasoso com uma tempestade "
                       "gigante conhecida como Grande Mancha Vermelha, ativa há séculos.",
        "facts": [
            "É tão grande que caberiam mais de 1.300 Terras dentro dele.",
            "A Grande Mancha Vermelha é uma tempestade maior que a Terra.",
            "Tem pelo menos 95 luas conhecidas, incluindo a gigante Ganimedes.",
        ],
    },
    {
        "id": "saturn",
        "name": "Saturno",
        "type": "planet",
        "color": "#e3d3a3",
        "emissive": "#1a1608",
        "radius": 3.2,
        "distance": 52,
        "orbit_speed": 0.034,
        "rotation_speed": 0.038,
        "moons": 146,
        "real_radius_km": "58.232",
        "real_distance": "1,43 bilhão km",
        "day_length": "10h 42min",
        "year_length": "29,5 anos terrestres",
        "temp": "~-139 °C",
        "description": "Saturno é famoso por seu deslumbrante sistema de anéis, formados principalmente "
                       "por partículas de gelo e rocha. É o segundo maior planeta do sistema solar.",
        "facts": [
            "Seus anéis são compostos majoritariamente de gelo, com um pouco de rocha e poeira.",
            "É o planeta menos denso do sistema solar — flutuaria na água.",
            "Tem mais de 140 luas confirmadas, incluindo Titã, maior que Mercúrio.",
        ],
        "has_rings": True,
    },
    {
        "id": "uranus",
        "name": "Urano",
        "type": "planet",
        "color": "#a6e3e9",
        "emissive": "#04181a",
        "radius": 2.3,
        "distance": 62,
        "orbit_speed": 0.012,
        "rotation_speed": -0.03,
        "moons": 28,
        "real_radius_km": "25.362",
        "real_distance": "2,87 bilhões km",
        "day_length": "17h 14min",
        "year_length": "84 anos terrestres",
        "temp": "~-197 °C",
        "description": "Urano é um gigante de gelo que gira praticamente 'deitado', com um eixo de "
                       "rotação inclinado cerca de 98 graus em relação à sua órbita.",
        "facts": [
            "Gira quase de lado, provavelmente por causa de uma colisão antiga.",
            "Foi o primeiro planeta descoberto com um telescópio, em 1781.",
            "Tem um sistema de anéis fino e escuro, difícil de observar.",
        ],
    },
    {
        "id": "neptune",
        "name": "Netuno",
        "type": "planet",
        "color": "#3b5bdb",
        "emissive": "#050820",
        "radius": 2.2,
        "distance": 72,
        "orbit_speed": 0.006,
        "rotation_speed": 0.032,
        "moons": 16,
        "real_radius_km": "24.622",
        "real_distance": "4,5 bilhões km",
        "day_length": "16h 6min",
        "year_length": "165 anos terrestres",
        "temp": "~-201 °C",
        "description": "Netuno é o planeta mais distante do Sol e tem os ventos mais fortes já registrados "
                       "no sistema solar, chegando a mais de 2.000 km/h.",
        "facts": [
            "Foi descoberto por cálculos matemáticos antes de ser observado diretamente.",
            "Tem os ventos mais rápidos do sistema solar.",
            "Sua lua Tritão orbita em sentido retrógrado, sugerindo que foi capturada.",
        ],
    },
]

PLANETS_JSON = json.dumps(PLANETS, ensure_ascii=False)

# ---------------------------------------------------------------------------
# Sidebar - controles
# ---------------------------------------------------------------------------
st.sidebar.title("🪐 Controles")
st.sidebar.markdown(
    "Use o **scroll do mouse** (ou os botões) sobre a cena para "
    "**dar zoom** e navegar de planeta em planeta."
)

speed = st.sidebar.slider("Velocidade das órbitas", 0.0, 5.0, 1.0, 0.1)
show_orbits = st.sidebar.checkbox("Mostrar linhas de órbita", True)
show_labels = st.sidebar.checkbox("Mostrar nomes dos planetas", True)

planet_names = [p["name"] for p in PLANETS]
jump_to = st.sidebar.selectbox("Ir direto para:", planet_names, index=0)
jump_index = planet_names.index(jump_to)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Distâncias e tamanhos estão em escala artística (não proporcional) "
    "para que o sistema inteiro caiba na tela."
)

st.title("☀️ Sistema Solar Interativo em 3D")
st.caption(
    "Role o zoom (scroll) dentro da cena para viajar de um planeta ao próximo. "
    "Arraste com o mouse para girar a câmera."
)

# ---------------------------------------------------------------------------
# HTML/JS com Three.js
# ---------------------------------------------------------------------------
HTML_TEMPLATE = r"""
<div id="scene-container" style="width:100%; height:800px; position:relative; background:#000010; border-radius:12px; overflow:hidden;">
  <canvas id="solar-canvas" style="display:block; width:100%; height:100%;"></canvas>

  <div id="info-panel" style="
      position:absolute; top:16px; left:16px; max-width:340px;
      background:rgba(10,12,24,0.82); backdrop-filter: blur(6px);
      border:1px solid rgba(255,255,255,0.12); border-radius:14px;
      padding:18px 20px; color:#e8ecf7; font-family:'Segoe UI',Roboto,sans-serif;
      box-shadow:0 8px 24px rgba(0,0,0,0.4); transition:opacity .3s ease;">
    <div id="info-name" style="font-size:22px; font-weight:700; margin-bottom:4px;"></div>
    <div id="info-desc" style="font-size:13px; line-height:1.5; opacity:0.9; margin-bottom:10px;"></div>
    <div id="info-stats" style="font-size:12px; line-height:1.7; opacity:0.85;"></div>
    <div id="info-facts" style="font-size:12px; line-height:1.6; margin-top:10px; opacity:0.9;"></div>
  </div>

  <div style="position:absolute; bottom:16px; left:50%; transform:translateX(-50%); display:flex; gap:10px;">
    <button id="btn-prev" style="pointer-events:auto; cursor:pointer; background:rgba(255,255,255,0.1); color:#fff; border:1px solid rgba(255,255,255,0.25); border-radius:8px; padding:8px 16px; font-size:14px;">◀ Anterior</button>
    <button id="btn-next" style="pointer-events:auto; cursor:pointer; background:rgba(255,255,255,0.1); color:#fff; border:1px solid rgba(255,255,255,0.25); border-radius:8px; padding:8px 16px; font-size:14px;">Próximo ▶</button>
  </div>

  <div id="hint" style="position:absolute; top:16px; right:16px; color:#aab2c8; font-size:12px; font-family:sans-serif; background:rgba(10,12,24,0.6); padding:8px 12px; border-radius:8px;">
    🖱️ Scroll = navegar entre planetas<br/>🖐️ Arraste = girar câmera
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
(function() {
  const PLANETS = __PLANETS_JSON__;
  const SPEED_MULT = __SPEED__;
  const SHOW_ORBITS = __SHOW_ORBITS__;
  const SHOW_LABELS = __SHOW_LABELS__;
  const START_INDEX = __START_INDEX__;

  const container = document.getElementById('scene-container');
  const canvas = document.getElementById('solar-canvas');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 2000);

  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Estrelas de fundo
  function createStarField() {
    const starGeo = new THREE.BufferGeometry();
    const starCount = 3000;
    const positions = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      const r = 400 + Math.random() * 800;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);
      positions[i*3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i*3+2] = r * Math.cos(phi);
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 1.1, sizeAttenuation: true });
    return new THREE.Points(starGeo, starMat);
  }
  scene.add(createStarField());

  // Luz do sol
  const sunLight = new THREE.PointLight(0xffffff, 2.2, 0, 0.5);
  scene.add(sunLight);
  scene.add(new THREE.AmbientLight(0x404050, 0.6));

  const bodies = []; // { data, mesh, orbitAngle, group }

  PLANETS.forEach((p, idx) => {
    const geo = new THREE.SphereGeometry(p.radius, 48, 48);
    let mat;
    if (p.type === 'star') {
      mat = new THREE.MeshBasicMaterial({ color: p.color });
    } else {
      mat = new THREE.MeshStandardMaterial({
        color: p.color,
        emissive: p.emissive,
        emissiveIntensity: 0.4,
        roughness: 0.85,
        metalness: 0.05
      });
    }
    const mesh = new THREE.Mesh(geo, mat);

    const group = new THREE.Group();
    if (p.distance > 0) {
      mesh.position.x = p.distance;
    }
    group.add(mesh);

    // Anel de Saturno
    if (p.has_rings) {
      const ringGeo = new THREE.RingGeometry(p.radius * 1.4, p.radius * 2.3, 64);
      const ringMat = new THREE.MeshStandardMaterial({
        color: 0xd8c9a3, side: THREE.DoubleSide, transparent: true, opacity: 0.75, roughness: 1
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2 - 0.35;
      ring.position.x = p.distance;
      group.add(ring);
    }

    // Linha de órbita
    if (p.distance > 0 && SHOW_ORBITS) {
      const orbitPts = [];
      for (let a = 0; a <= 128; a++) {
        const ang = (a / 128) * Math.PI * 2;
        orbitPts.push(new THREE.Vector3(Math.cos(ang) * p.distance, 0, Math.sin(ang) * p.distance));
      }
      const orbitGeo = new THREE.BufferGeometry().setFromPoints(orbitPts);
      const orbitMat = new THREE.LineBasicMaterial({ color: 0x445077, transparent: true, opacity: 0.5 });
      scene.add(new THREE.LineLoop(orbitGeo, orbitMat));
    }

    // Label (sprite de texto simples via canvas)
    let label = null;
    if (SHOW_LABELS) {
      const canvasLbl = document.createElement('canvas');
      const ctx = canvasLbl.getContext('2d');
      canvasLbl.width = 256; canvasLbl.height = 64;
      ctx.font = 'bold 34px sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.fillText(p.name, 128, 40);
      const tex = new THREE.CanvasTexture(canvasLbl);
      const spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false });
      label = new THREE.Sprite(spriteMat);
      label.scale.set(8, 2, 1);
      label.position.set(p.distance, p.radius + 2.5, 0);
      group.add(label);
    }

    scene.add(group);
    bodies.push({
      data: p,
      mesh: mesh,
      group: group,
      orbitAngle: Math.random() * Math.PI * 2,
      worldPos: new THREE.Vector3()
    });
  });

  camera.position.set(0, 20, 40);
  camera.lookAt(0, 0, 0);

  // --- Navegação por zoom entre planetas ---
  let currentIndex = START_INDEX;
  let targetPos = new THREE.Vector3();
  let targetLook = new THREE.Vector3();
  let camPosSmooth = camera.position.clone();
  let lookSmooth = new THREE.Vector3();
  let wheelAccum = 0;
  const WHEEL_THRESHOLD = 260;

  function focusDistanceFor(p) {
    return Math.max(p.radius * 4.2, 6) + (p.type === 'star' ? 10 : 0);
  }

  function updateInfoPanel() {
    const p = bodies[currentIndex].data;
    document.getElementById('info-name').innerText = (p.type === 'star' ? '☀️ ' : '🪐 ') + p.name;
    document.getElementById('info-desc').innerText = p.description;
    document.getElementById('info-stats').innerHTML =
      '<b>Raio real:</b> ' + p.real_radius_km + ' km<br/>' +
      '<b>Distância do Sol:</b> ' + p.real_distance + '<br/>' +
      '<b>Dia:</b> ' + p.day_length + ' &nbsp; <b>Ano:</b> ' + p.year_length + '<br/>' +
      '<b>Temperatura:</b> ' + p.temp + '<br/>' +
      '<b>Luas:</b> ' + p.moons;
    document.getElementById('info-facts').innerHTML =
      '<b>Curiosidades:</b><ul style="margin:4px 0 0 18px; padding:0;">' +
      p.facts.map(f => '<li>' + f + '</li>').join('') + '</ul>';
  }

  function goTo(index) {
    currentIndex = ((index % bodies.length) + bodies.length) % bodies.length;
    updateInfoPanel();
  }

  document.getElementById('btn-next').addEventListener('click', () => goTo(currentIndex + 1));
  document.getElementById('btn-prev').addEventListener('click', () => goTo(currentIndex - 1));

  container.addEventListener('wheel', (e) => {
    e.preventDefault();
    wheelAccum += e.deltaY;
    if (wheelAccum > WHEEL_THRESHOLD) {
      goTo(currentIndex + 1);
      wheelAccum = 0;
    } else if (wheelAccum < -WHEEL_THRESHOLD) {
      goTo(currentIndex - 1);
      wheelAccum = 0;
    }
  }, { passive: false });

  // Controles de arraste (rotação livre ao redor do alvo), sem zoom nativo
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableZoom = false;
  controls.enablePan = false;
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = false;

  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const dt = clock.getDelta();
    const t = clock.getElapsedTime();

    bodies.forEach((b) => {
      const p = b.data;
      if (p.distance > 0) {
        b.orbitAngle += p.orbit_speed * 0.15 * SPEED_MULT * dt;
        b.group.rotation.y = 0;
        b.mesh.position.x = Math.cos(b.orbitAngle) * p.distance;
        b.mesh.position.z = Math.sin(b.orbitAngle) * p.distance;
      }
      b.mesh.rotation.y += p.rotation_speed * SPEED_MULT * 2 * dt * 30;
      b.mesh.getWorldPosition(b.worldPos);
    });

    // atualizar alvo da câmera suavemente
    const focus = bodies[currentIndex];
    const dist = focusDistanceFor(focus.data);
    const dir = new THREE.Vector3().subVectors(camPosSmooth, focus.worldPos);
    if (dir.length() < 0.001) dir.set(0.4, 0.25, 1);
    dir.normalize();

    targetLook.copy(focus.worldPos);
    targetPos.copy(focus.worldPos).add(dir.multiplyScalar(dist)).add(new THREE.Vector3(0, dist * 0.35, 0));

    camPosSmooth.lerp(targetPos, 1 - Math.pow(0.001, dt));
    lookSmooth.lerp(targetLook, 1 - Math.pow(0.001, dt));

    camera.position.copy(camPosSmooth);
    controls.target.copy(lookSmooth);
    controls.update();

    sunLight.position.copy(bodies[0].worldPos);

    renderer.render(scene, camera);
  }

  updateInfoPanel();
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
})();
</script>
"""

html_code = (
    HTML_TEMPLATE
    .replace("__PLANETS_JSON__", PLANETS_JSON)
    .replace("__SPEED__", str(speed))
    .replace("__SHOW_ORBITS__", "true" if show_orbits else "false")
    .replace("__SHOW_LABELS__", "true" if show_labels else "false")
    .replace("__START_INDEX__", str(jump_index))
)

components.html(html_code, height=820, scrolling=False)

st.markdown("---")

# ---------------------------------------------------------------------------
# Conteúdo textual complementar (acessível, sem depender do 3D)
# ---------------------------------------------------------------------------
st.subheader("📚 Ficha detalhada de cada corpo celeste")
tabs = st.tabs([p["name"] for p in PLANETS])
for tab, p in zip(tabs, PLANETS):
    with tab:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### {p['name']}")
            st.write(p["description"])
            st.markdown("**Curiosidades:**")
            for f in p["facts"]:
                st.markdown(f"- {f}")
        with col2:
            st.metric("Raio real", f"{p['real_radius_km']} km")
            st.metric("Distância do Sol", p["real_distance"])
            st.metric("Duração do dia", p["day_length"])
            st.metric("Duração do ano", p["year_length"])
            st.metric("Temperatura", p["temp"])
            st.metric("Luas", p["moons"])

st.caption(
    "Feito com Python, Streamlit e Three.js. Distâncias e tamanhos na cena 3D "
    "estão em escala artística para fins de visualização."
)
