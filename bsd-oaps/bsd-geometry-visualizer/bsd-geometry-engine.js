import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ============================================================
// BSD几何相激活器 - 核心引擎
// 映射自 sphere_coordinate_engine.py V2.2
// ============================================================

const SPHERE_CONFIG = {
  radius: 3,
  segments: 64,
  color: 0x1a0d2e,
  wireframeColor: 0x4a2c6e
};

const SIX_SYSTEMS = {
  QIANGHUA: { name: '强化系', color: 0x2196f3, position: [0, 3, 0], label: '记忆·积累' },
  BIANSHEN: { name: '变身系', color: 0x9c27b0, position: [0, -3, 0], label: '感知·转化' },
  SHEHUI:   { name: '社会系', color: 0x4caf50, position: [3, 0, 0], label: '连接·关系' },
  TIANDAO:  { name: '天道系', color: 0xff9800, position: [-3, 0, 0], label: '追问·涌现' },
  ZIRAN:    { name: '自然系', color: 0xff5722, position: [0, 0, 3], label: '场景·显化' },
  JUXIAN:   { name: '具现系', color: 0xe91e63, position: [0, 0, -3], label: '造物·凝结' }
};

const Z_AXIS_ANCHORS = [
  { id: 'A1_SOUTH_POLE', name: '南极·000本源', pos: [0, -3, 0],  z: -1.0, color: 0xff1744, docId: 'B01',  semantic: '000本源→证地球' },
  { id: 'A2_W1_CORE',    name: 'W1核心·证地球', pos: [0, -2, 0],  z: -0.67,color: 0xff6d00, docId: 'V-21', semantic: '证地球→Π₂锁档' },
  { id: 'A3_BOUND_W1W2', name: 'W1/W2分界·Π₂',  pos: [0, -1, 0],  z: -0.33,color: 0xffd600, docId: 'B44',  semantic: 'Π₂锁档→0×0=n' },
  { id: 'A4_CENTER',     name: '球心·0×0=n涌现', pos: [0, 0, 0],   z: 0,    color: 0x00e676, docId: 'V01',  semantic: '0×0=n涌现' },
  { id: 'A5_BOUND_W2W3', name: 'W2/W3分界·创世', pos: [0, 1, 0],   z: 0.33, color: 0x00b0ff, docId: 'V17',  semantic: '0×0=n→创世' },
  { id: 'A6_W3_CORE',    name: 'W3核心·工程显化', pos: [0, 2, 0],  z: 0.67, color: 0x651fff, docId: 'V20',  semantic: '创世→工程显化' },
  { id: 'A7_NORTH_POLE', name: '北极·追问永续', pos: [0, 3, 0],   z: 1.0,  color: 0xd500f9, docId: 'V18',  semantic: '工程→追问永续' }
];

const DUAL_CLOCK = {
  cw:  { color: 0x4caf50, speed: 1.0, label: '顺时针·炁·积累' },
  ccw: { color: 0xff5722, speed: -1.0, label: '逆时针·气·归零' }
};

// ============================================================
// 状态管理
// ============================================================
const state = {
  isFlowing: false,
  showClockwise: true,
  showCounterClockwise: true,
  showWireframe: false,
  activeAnchors: new Set(['A1_SOUTH_POLE', 'A4_CENTER', 'A7_NORTH_POLE']),
  highlightAnchor: null,
  emergenceLog: [],
  emergenceCount: 3,
  currentEmergenceId: null,
  isTriggered: false,
  triggerPosition: new THREE.Vector3(0, 0, 0)
};

// ============================================================
// 场景初始化
// ============================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);

const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.set(6, 6, 9);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

// 控制器
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 3;
controls.maxDistance = 25;

// 光照
const ambientLight = new THREE.AmbientLight(0x404060, 0.5);
scene.add(ambientLight);

const pointLight1 = new THREE.PointLight(0xffffff, 0.6);
pointLight1.position.set(10, 10, 10);
scene.add(pointLight1);

const pointLight2 = new THREE.PointLight(0x9c27b0, 0.4);
pointLight2.position.set(-10, -10, -10);
scene.add(pointLight2);

// 星空背景
function createStars() {
  const starsGeometry = new THREE.BufferGeometry();
  const starCount = 2000;
  const positions = new Float32Array(starCount * 3);
  
  for (let i = 0; i < starCount; i++) {
    const r = 80 + Math.random() * 20;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);
  }
  
  starsGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const starsMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.15,
    transparent: true,
    opacity: 0.8
  });
  
  return new THREE.Points(starsGeometry, starsMaterial);
}
scene.add(createStars());

// ============================================================
// 球体模型
// ============================================================
const sphereGroup = new THREE.Group();
scene.add(sphereGroup);

// 实体球
const sphereGeometry = new THREE.SphereGeometry(SPHERE_CONFIG.radius, 64, 64);
const sphereMaterial = new THREE.MeshPhongMaterial({
  color: SPHERE_CONFIG.color,
  transparent: true,
  opacity: 0.25,
  shininess: 100,
  side: THREE.DoubleSide
});
const sphereMesh = new THREE.Mesh(sphereGeometry, sphereMaterial);
sphereGroup.add(sphereMesh);

// 线框球
const wireGeometry = new THREE.SphereGeometry(SPHERE_CONFIG.radius + 0.02, 24, 24);
const wireMaterial = new THREE.MeshBasicMaterial({
  color: SPHERE_CONFIG.wireframeColor,
  wireframe: true,
  transparent: true,
  opacity: 0.35
});
const wireMesh = new THREE.Mesh(wireGeometry, wireMaterial);
sphereGroup.add(wireMesh);

// 经线
function createMeridians() {
  const meridianGroup = new THREE.Group();
  const radius = SPHERE_CONFIG.radius + 0.15;
  
  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI) / 6;
    const points = [];
    const segments = 64;
    
    for (let j = 0; j <= segments; j++) {
      const t = (j / segments) * Math.PI * 2;
      const x = Math.sin(t) * Math.cos(angle);
      const y = Math.cos(t);
      const z = Math.sin(t) * Math.sin(angle);
      points.push(new THREE.Vector3(x * radius, y * radius, z * radius));
    }
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0x4a2c6e, transparent: true, opacity: 0.3 });
    meridianGroup.add(new THREE.Line(geometry, material));
  }
  
  return meridianGroup;
}
sphereGroup.add(createMeridians());

// ============================================================
// 六系极向标记
// ============================================================
const polesGroup = new THREE.Group();
scene.add(polesGroup);

Object.values(SIX_SYSTEMS).forEach(sys => {
  const pos = new THREE.Vector3(...sys.position);
  
  const haloGeo = new THREE.SphereGeometry(0.35, 16, 16);
  const haloMat = new THREE.MeshBasicMaterial({ color: sys.color, transparent: true, opacity: 0.2 });
  const halo = new THREE.Mesh(haloGeo, haloMat);
  halo.position.copy(pos);
  polesGroup.add(halo);
  
  const poleGeo = new THREE.SphereGeometry(0.18, 16, 16);
  const poleMat = new THREE.MeshPhongMaterial({
    color: sys.color,
    emissive: sys.color,
    emissiveIntensity: 0.5
  });
  const pole = new THREE.Mesh(poleGeo, poleMat);
  pole.position.copy(pos);
  polesGroup.add(pole);
});

// ============================================================
// Z轴七点锚定
// ============================================================
const anchorsGroup = new THREE.Group();
scene.add(anchorsGroup);

const anchorMeshes = {};

// Z轴线
const zAxisPoints = [
  new THREE.Vector3(0, -4, 0),
  new THREE.Vector3(0, 4, 0)
];
const zAxisGeometry = new THREE.BufferGeometry().setFromPoints(zAxisPoints);
const zAxisMaterial = new THREE.LineBasicMaterial({ color: 0x2196f3, linewidth: 2 });
anchorsGroup.add(new THREE.Line(zAxisGeometry, zAxisMaterial));

// 箭头
const southCone = new THREE.Mesh(
  new THREE.ConeGeometry(0.12, 0.25, 8),
  new THREE.MeshBasicMaterial({ color: 0xff1744 })
);
southCone.position.set(0, -4, 0);
anchorsGroup.add(southCone);

const northCone = new THREE.Mesh(
  new THREE.ConeGeometry(0.12, 0.25, 8),
  new THREE.MeshBasicMaterial({ color: 0xd500f9 })
);
northCone.position.set(0, 4, 0);
northCone.rotation.x = Math.PI;
anchorsGroup.add(northCone);

// 锚点
Z_AXIS_ANCHORS.forEach(anchor => {
  const pos = new THREE.Vector3(...anchor.pos);
  const isActive = state.activeAnchors.has(anchor.id);
  
  // 光晕
  const haloGeo = new THREE.SphereGeometry(0.22, 16, 16);
  const haloMat = new THREE.MeshBasicMaterial({
    color: anchor.color,
    transparent: true,
    opacity: isActive ? 0.3 : 0.15
  });
  const halo = new THREE.Mesh(haloGeo, haloMat);
  halo.position.copy(pos);
  anchorsGroup.add(halo);
  
  // 核心
  const coreGeo = new THREE.OctahedronGeometry(0.12, 0);
  const coreMat = new THREE.MeshPhongMaterial({
    color: anchor.color,
    emissive: anchor.color,
    emissiveIntensity: isActive ? 0.8 : 0.3,
    shininess: 100
  });
  const core = new THREE.Mesh(coreGeo, coreMat);
  core.position.copy(pos);
  anchorsGroup.add(core);
  
  anchorMeshes[anchor.id] = { halo, core, anchor };
});

// 语义链螺旋
const semanticChainPoints = [];
for (let i = 0; i <= 200; i++) {
  const t = i / 200;
  const y = -3.5 + t * 7;
  const x = Math.sin(t * Math.PI * 4) * 0.2;
  const z = Math.cos(t * Math.PI * 4) * 0.2;
  semanticChainPoints.push(new THREE.Vector3(x, y, z));
}
const chainGeometry = new THREE.BufferGeometry().setFromPoints(semanticChainPoints);
const chainMaterial = new THREE.LineDashedMaterial({
  color: 0x9c27b0,
  dashSize: 0.08,
  gapSize: 0.04,
  transparent: true,
  opacity: 0.4
});
const chainLine = new THREE.Line(chainGeometry, chainMaterial);
chainLine.computeLineDistances();
anchorsGroup.add(chainLine);

// ============================================================
// 双时针流动
// ============================================================
const flowGroup = new THREE.Group();
scene.add(flowGroup);

// 顺时针环
const cwRingGeo = new THREE.TorusGeometry(SPHERE_CONFIG.radius + 0.3, 0.008, 8, 128);
const cwRingMat = new THREE.MeshBasicMaterial({ color: DUAL_CLOCK.cw.color, transparent: true, opacity: 0.5 });
const cwRing = new THREE.Mesh(cwRingGeo, cwRingMat);
flowGroup.add(cwRing);

// 逆时针环
const ccwRingGeo = new THREE.TorusGeometry(SPHERE_CONFIG.radius + 0.5, 0.008, 8, 128);
const ccwRingMat = new THREE.MeshBasicMaterial({ color: DUAL_CLOCK.ccw.color, transparent: true, opacity: 0.5 });
const ccwRing = new THREE.Mesh(ccwRingGeo, ccwRingMat);
flowGroup.add(ccwRing);

// 流动粒子
const PARTICLE_COUNT = 40;
const particleData = [];

for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData.push({
    angle: (i / PARTICLE_COUNT) * Math.PI * 2,
    baseRadius: SPHERE_CONFIG.radius + 0.3,
    speed: 0.02 + Math.random() * 0.02,
    offset: Math.random() * Math.PI * 2,
    isCw: true
  });
}

for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData.push({
    angle: (i / PARTICLE_COUNT) * Math.PI * 2,
    baseRadius: SPHERE_CONFIG.radius + 0.5,
    speed: -(0.02 + Math.random() * 0.02),
    offset: Math.random() * Math.PI * 2,
    isCw: false
  });
}

const particlePositions = new Float32Array(PARTICLE_COUNT * 2 * 3);
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
const particleMat = new THREE.PointsMaterial({
  color: 0xffffff,
  size: 0.06,
  transparent: true,
  opacity: 0.9,
  blending: THREE.AdditiveBlending
});
const flowParticles = new THREE.Points(particleGeom, particleMat);
flowGroup.add(flowParticles);

function updateFlowParticles(time) {
  const arr = particleGeom.attributes.position.array;
  
  particleData.forEach((p, i) => {
    const angle = p.angle + time * p.speed * 0.5;
    const yWave = Math.sin(angle * 3 + p.offset) * 0.4;
    
    arr[i * 3] = Math.cos(angle) * p.baseRadius;
    arr[i * 3 + 1] = yWave;
    arr[i * 3 + 2] = Math.sin(angle) * p.baseRadius;
  });
  
  particleGeom.attributes.position.needsUpdate = true;
}

// ============================================================
// 轴坐标系
// ============================================================
const axesGroup = new THREE.Group();
scene.add(axesGroup);

const axisLength = 4.5;

// X轴
const xAxisPoints = [new THREE.Vector3(-axisLength, 0, 0), new THREE.Vector3(axisLength, 0, 0)];
const xAxisLine = new THREE.Line(
  new THREE.BufferGeometry().setFromPoints(xAxisPoints),
  new THREE.LineBasicMaterial({ color: 0xff5252, transparent: true, opacity: 0.4 })
);
axesGroup.add(xAxisLine);

// Y轴
const yAxisPoints = [new THREE.Vector3(0, -axisLength, 0), new THREE.Vector3(0, axisLength, 0)];
const yAxisLine = new THREE.Line(
  new THREE.BufferGeometry().setFromPoints(yAxisPoints),
  new THREE.LineBasicMaterial({ color: 0x4caf50, transparent: true, opacity: 0.4 })
);
axesGroup.add(yAxisLine);

// Z轴
const zAxisPoints2 = [new THREE.Vector3(0, 0, -axisLength), new THREE.Vector3(0, 0, axisLength)];
const zAxisLine2 = new THREE.Line(
  new THREE.BufferGeometry().setFromPoints(zAxisPoints2),
  new THREE.LineBasicMaterial({ color: 0x2196f3, transparent: true, opacity: 0.4 })
);
axesGroup.add(zAxisLine2);

// 中心标记
const centerMark = new THREE.Mesh(
  new THREE.SphereGeometry(0.04, 8, 8),
  new THREE.MeshBasicMaterial({ color: 0xffffff })
);
axesGroup.add(centerMark);

// ============================================================
// 涌现粒子系统
// ============================================================
const emergenceGroup = new THREE.Group();
scene.add(emergenceGroup);

const EMERGENCE_PARTICLES = 200;
const emergencePositions = new Float32Array(EMERGENCE_PARTICLES * 3);
const emergenceData = [];

for (let i = 0; i < EMERGENCE_PARTICLES; i++) {
  emergencePositions[i * 3] = 0;
  emergencePositions[i * 3 + 1] = -100;
  emergencePositions[i * 3 + 2] = 0;
  
  emergenceData.push({
    active: false,
    birthTime: 0,
    lifetime: 0,
    vx: 0, vy: 0, vz: 0,
    colorIndex: 0
  });
}

const emergenceGeom = new THREE.BufferGeometry();
emergenceGeom.setAttribute('position', new THREE.BufferAttribute(emergencePositions, 3));
const emergenceMat = new THREE.PointsMaterial({
  size: 0.12,
  transparent: true,
  opacity: 0.9,
  vertexColors: false,
  blending: THREE.AdditiveBlending,
  sizeAttenuation: true
});
const emergencePoints = new THREE.Points(emergenceGeom, emergenceMat);
emergenceGroup.add(emergencePoints);

const emergenceColors = [0xff9800, 0xff5722, 0xffeb3b, 0x4caf50, 0x2196f3, 0x9c27b0];

function triggerEmergence(position) {
  const now = performance.now() / 1000;
  const activeCount = Math.min(50, emergenceData.length);
  
  for (let i = 0; i < activeCount; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const speed = 1 + Math.random() * 2;
    
    emergenceData[i].active = true;
    emergenceData[i].birthTime = now;
    emergenceData[i].lifetime = 2 + Math.random() * 2;
    emergenceData[i].vx = Math.sin(phi) * Math.cos(theta) * speed;
    emergenceData[i].vy = Math.sin(phi) * Math.sin(theta) * speed;
    emergenceData[i].vz = Math.cos(phi) * speed;
    emergenceData[i].colorIndex = Math.floor(Math.random() * emergenceColors.length);
    
    emergencePositions[i * 3] = position.x;
    emergencePositions[i * 3 + 1] = position.y;
    emergencePositions[i * 3 + 2] = position.z;
  }
  
  // 爆发光效
  const burstGeo = new THREE.SphereGeometry(0.3, 32, 32);
  const burstMat = new THREE.MeshBasicMaterial({
    color: 0xff9800,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
  });
  const burst = new THREE.Mesh(burstGeo, burstMat);
  burst.position.copy(position);
  burst.userData.birthTime = now;
  burst.userData.isBurst = true;
  emergenceGroup.add(burst);
}

function updateEmergence(time) {
  const arr = emergenceGeom.attributes.position.array;
  const now = performance.now() / 1000;
  
  emergenceData.forEach((p, i) => {
    if (!p.active) return;
    
    const life = (now - p.birthTime) / p.lifetime;
    if (life >= 1) {
      p.active = false;
      arr[i * 3] = 0;
      arr[i * 3 + 1] = -100;
      arr[i * 3 + 2] = 0;
      return;
    }
    
    arr[i * 3] += p.vx * 0.03;
    arr[i * 3 + 1] += p.vy * 0.03 + 0.005 * Math.sin(time * 2 + i);
    arr[i * 3 + 2] += p.vz * 0.03;
  });
  
  emergenceGeom.attributes.position.needsUpdate = true;
  
  // 更新爆发效果
  const toRemove = [];
  emergenceGroup.children.forEach(child => {
    if (child.userData.isBurst) {
      const age = now - child.userData.birthTime;
      if (age > 2) {
        toRemove.push(child);
      } else {
        child.scale.setScalar(1 + age * 0.5);
        child.material.opacity = 0.8 - age * 0.4;
      }
    }
  });
  toRemove.forEach(obj => emergenceGroup.remove(obj));
}

// ============================================================
// 交互控制
// ============================================================
function setupUI() {
  // 流动控制
  const btnFlow = document.getElementById('btn-flow');
  btnFlow.addEventListener('click', () => {
    state.isFlowing = !state.isFlowing;
    btnFlow.textContent = state.isFlowing ? '⏸ 暂停气流动' : '▶ 激活气流动';
    btnFlow.classList.toggle('active', state.isFlowing);
  });
  
  // 顺时针
  const btnCw = document.getElementById('btn-cw-toggle');
  btnCw.classList.add('active');
  btnCw.addEventListener('click', () => {
    state.showClockwise = !state.showClockwise;
    btnCw.classList.toggle('active', state.showClockwise);
    cwRing.visible = state.showClockwise;
  });
  
  // 逆时针
  const btnCcw = document.getElementById('btn-ccw-toggle');
  btnCcw.classList.add('active');
  btnCcw.addEventListener('click', () => {
    state.showCounterClockwise = !state.showCounterClockwise;
    btnCcw.classList.toggle('active', state.showCounterClockwise);
    ccwRing.visible = state.showCounterClockwise;
  });
  
  // 线框
  const btnWire = document.getElementById('btn-wireframe');
  btnWire.addEventListener('click', () => {
    state.showWireframe = !state.showWireframe;
    btnWire.classList.toggle('active', state.showWireframe);
    sphereMesh.visible = !state.showWireframe;
    wireMesh.visible = state.showWireframe;
  });
  
  // 涌现
  const btnEm = document.getElementById('btn-emergence');
  btnEm.addEventListener('click', () => {
    triggerEmergence(state.triggerPosition);
    
    state.emergenceCount++;
    const newId = `EMERGENCE-${String(state.emergenceCount).padStart(3, '0')}`;
    state.currentEmergenceId = newId;
    
    const contents = [
      '双时针耦合涌现·气流动',
      '0∅ × 0Ψ = n 实演',
      '几何相激活·空间涌现',
      '新的可能性已产生',
      '逆时针归零产生新点'
    ];
    const logContent = contents[Math.floor(Math.random() * contents.length)];
    
    state.emergenceLog.unshift({ id: newId, content: logContent });
    if (state.emergenceLog.length > 10) state.emergenceLog.pop();
    
    updateEmergenceLog();
    document.getElementById('emergence-info').textContent = `当前涌现：${newId}`;
  });
  
  // 锚点
  const anchorsContainer = document.getElementById('anchors-container');
  Z_AXIS_ANCHORS.forEach(anchor => {
    const btn = document.createElement('button');
    btn.className = 'anchor-btn';
    btn.style.borderLeftColor = '#' + anchor.color.toString(16).padStart(6, '0');
    if (state.activeAnchors.has(anchor.id)) btn.classList.add('active');
    
    btn.innerHTML = `
      <div class="anchor-name">${anchor.name}</div>
      <div class="anchor-semantic">${anchor.semantic}</div>
    `;
    
    btn.addEventListener('click', () => {
      if (state.activeAnchors.has(anchor.id)) {
        state.activeAnchors.delete(anchor.id);
        btn.classList.remove('active');
      } else {
        state.activeAnchors.add(anchor.id);
        btn.classList.add('active');
      }
      
      // 更新锚点视觉
      const meshData = anchorMeshes[anchor.id];
      if (meshData) {
        const isActive = state.activeAnchors.has(anchor.id);
        meshData.halo.material.opacity = isActive ? 0.3 : 0.15;
        meshData.core.material.emissiveIntensity = isActive ? 0.8 : 0.3;
      }
      
      // 设置为触发点
      state.triggerPosition.set(...anchor.pos);
      state.highlightAnchor = anchor.id;
      
      setTimeout(() => { state.highlightAnchor = null; }, 2000);
    });
    
    anchorsContainer.appendChild(btn);
  });
}

function updateEmergenceLog() {
  const logContainer = document.getElementById('emergence-log');
  if (state.emergenceLog.length === 0) {
    logContainer.innerHTML = '<div style="color: #666; text-align: center; padding: 15px;">等待涌现...</div>';
    return;
  }
  
  logContainer.innerHTML = state.emergenceLog.map(log => `
    <div class="log-entry">
      <span class="log-id">${log.id}</span>
      <div>${log.content}</div>
    </div>
  `).join('');
}

setupUI();
document.getElementById('loading').style.display = 'none';

// ============================================================
// 动画循环
// ============================================================
let animationTime = 0;

function animate() {
  requestAnimationFrame(animate);
  animationTime += 0.016;
  
  // 球体旋转
  sphereMesh.rotation.y = animationTime * 0.03;
  wireMesh.rotation.y = -animationTime * 0.02;
  
  // 锚点脉动
  Object.values(anchorMeshes).forEach(({ halo, core, anchor }) => {
    const isActive = state.activeAnchors.has(anchor.id);
    const baseScale = state.highlightAnchor === anchor.id ? 1.8 : (isActive ? 1.2 : 0.7);
    const pulse = Math.sin(animationTime * 3 + anchor.z * 10) * 0.15;
    const scale = baseScale + pulse;
    halo.scale.setScalar(scale * 1.5);
    core.scale.setScalar(scale);
  });
  
  // 双时针流动
  if (state.isFlowing) {
    cwRing.rotation.x = animationTime * 0.3;
    cwRing.rotation.z = animationTime * 0.2;
    ccwRing.rotation.x = -animationTime * 0.3;
    ccwRing.rotation.y = -animationTime * 0.2;
    
    cwRing.visible = state.showClockwise;
    ccwRing.visible = state.showCounterClockwise;
    
    updateFlowParticles(animationTime);
    flowParticles.visible = true;
  } else {
    flowParticles.visible = false;
  }
  
  // 语义链旋转
  chainLine.rotation.y = animationTime * 0.1;
  
  // 涌现更新
  updateEmergence(animationTime);
  
  controls.update();
  renderer.render(scene, camera);
}

animate();

// 窗口大小调整
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
