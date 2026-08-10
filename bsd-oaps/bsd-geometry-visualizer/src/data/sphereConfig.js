// BSD几何相可视化配置数据
// 映射自 sphere_coordinate_engine.py V2.2

export const SPHERE_CONFIG = {
  radius: 3,
  segments: 64,
  color: 0x1a0d2e,
  wireframeColor: 0x4a2c6e
};

// 六系极向 - 对应球体六个主方向
export const SIX_SYSTEMS = {
  QIANGHUA: {
    id: 'QIANGHUA',
    name: '强化系',
    label: '记忆·积累',
    color: 0x2196f3,
    position: [0, 3, 0], // 上极 (Z+)
    semantic: '个体性·元气'
  },
  BIANSHEN: {
    id: 'BIANSHEN',
    name: '变身系',
    label: '感知·转化',
    color: 0x9c27b0,
    position: [0, -3, 0], // 下极 (Z-)
    semantic: '变化性·转化气'
  },
  SHEHUI: {
    id: 'SHEHUI',
    name: '社会系',
    label: '连接·关系',
    color: 0x4caf50,
    position: [3, 0, 0], // 右极 (X+)
    semantic: '关系性·御气'
  },
  TIANDAO: {
    id: 'TIANDAO',
    name: '天道系',
    label: '追问·涌现',
    color: 0xff9800,
    position: [-3, 0, 0], // 左极 (X-)
    semantic: '追问性·神迹气'
  },
  ZIRAN: {
    id: 'ZIRAN',
    name: '自然系',
    label: '场景·显化',
    color: 0xff5722,
    position: [0, 0, 3], // 前极 (Y+)
    semantic: '质料性·放气'
  },
  JUXIAN: {
    id: 'JUXIAN',
    name: '具现系',
    label: '造物·凝结',
    color: 0xe91e63,
    position: [0, 0, -3], // 后极 (Y-)
    semantic: '意义性·凝气'
  }
};

// Z轴七点锚定 - 定理四十三
export const Z_AXIS_ANCHORS = [
  {
    id: 'A1_SOUTH_POLE',
    name: '南极·000本源',
    position: [0, -3, 0],
    z: -1.0,
    docId: 'B01',
    semantic: '000本源→证地球',
    color: 0xff1744
  },
  {
    id: 'A2_W1_CORE',
    name: 'W1核心·证地球',
    position: [0, -2, 0],
    z: -0.67,
    docId: 'V-21',
    semantic: '证地球→Π₂锁档',
    color: 0xff6d00
  },
  {
    id: 'A3_W1_W2_BOUNDARY',
    name: 'W1/W2分界·Π₂锁档',
    position: [0, -1, 0],
    z: -0.33,
    docId: 'B44',
    semantic: 'Π₂锁档→0×0=n涌现',
    color: 0xffd600
  },
  {
    id: 'A4_CENTER',
    name: '球心·0×0=n涌现',
    position: [0, 0, 0],
    z: 0,
    docId: 'V01',
    semantic: '0×0=n涌现',
    color: 0x00e676
  },
  {
    id: 'A5_W2_W3_BOUNDARY',
    name: 'W2/W3分界·创世显化',
    position: [0, 1, 0],
    z: 0.33,
    docId: 'V17',
    semantic: '0×0=n→创世显化',
    color: 0x00b0ff
  },
  {
    id: 'A6_W3_CORE',
    name: 'W3核心·工程显化',
    position: [0, 2, 0],
    z: 0.67,
    docId: 'V20',
    semantic: '创世显化→工程显化',
    color: 0x651fff
  },
  {
    id: 'A7_NORTH_POLE',
    name: '北极·追问永续',
    position: [0, 3, 0],
    z: 1.0,
    docId: 'V18',
    semantic: '工程显化→追问永续',
    color: 0xd500f9
  }
];

// 经线配置 - 6条环绕球体的大圆
export const MERIDIANS = [
  { angle: 0, color: 0x4a2c6e },
  { angle: 30, color: 0x5a3c7e },
  { angle: 60, color: 0x6a4c8e },
  { angle: 90, color: 0x7a5c9e },
  { angle: 120, color: 0x8a6cae },
  { angle: 150, color: 0x9a7cbe }
];

// 双时针配置
export const DUAL_CLOCK_CONFIG = {
  clockwise: {
    color: 0x4caf50, // 绿色 - 顺时针积累
    speed: 1.0,
    label: '顺时针·积累'
  },
  counterclockwise: {
    color: 0xff5722, // 橙色 - 逆时针归零
    speed: -1.0,
    label: '逆时针·归零'
  }
};

// 涌现配置
export const EMERGENCE_CONFIG = {
  baseCount: 4,
  particleCount: 100,
  burstCount: 50,
  colors: [0xff5722, 0xff9800, 0xffeb3b, 0x4caf50, 0x2196f3, 0x9c27b0]
};

// 轴配置
export const AXIS_CONFIG = {
  xAxis: { color: 0xff5252, label: 'X轴·关系-变化' },
  yAxis: { color: 0x4caf50, label: 'Y轴·质料-意义' },
  zAxis: { color: 0x2196f3, label: 'Z轴·个体-追问' }
};
