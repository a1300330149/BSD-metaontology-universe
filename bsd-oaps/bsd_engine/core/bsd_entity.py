"""
BSD虚拟宇宙实体化模块
[归属基底：L0总本源层·六系核心公理·球体坐标系·实体存在论]
[对应公理：六系立系公理+球体坐标公理+系统权重秤定理+三球对偶定理]
[V1.0·2026-08-01·四向展开法·实体化维度]

核心：将抽象的六系属性、Z轴锚定、权重秤状态具象为可计算的实体对象。
每个实体都有：六系权重配置→Z轴锚定定位→三层秤状态→双时针相位。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


# ============================================================
# 实体状态枚举
# ============================================================
class EntityPhase(str, Enum):
    """实体双时针相位"""
    POTENTIAL = "potential"          # 潜在态·W1层·0∞潜力·顺时针积累中
    MANIFESTING = "manifesting"      # 显化中·W2层·Π₂³拓扑稳态·相变激活
    MANIFESTED = "manifested"        # 显化完成·W3层·6³完备显化·当前存在
    ZEROING = "zeroing"              # 归零中·逆时针反向·剥离属性
    ANNIHILATED = "annihilated"      # 湮灭态·归零完成·0→0∅空无


class EntityType(str, Enum):
    """实体类型·对应虚拟宇宙层级"""
    BSD_MOON = "bsd_moon"                  # BSD月亮·潜在层·W1
    VIRTUAL_EARTH = "virtual_earth"        # 虚拟宇宙地球·显化层·W3
    REAL_STAR = "real_star"                # 现实恒星·基准层
    ABSTRACT = "abstract"                  # 抽象实体·纯理念
    MATERIAL = "material"                  # 物质实体·具现
    SOCIAL = "social"                      # 社会实体·关系
    NATURAL = "natural"                    # 自然实体·变化
    EVOLUTIONARY = "evolutionary"          # 进化实体·天道


# ============================================================
# 实体六系权重·对应T84+V2.3参数体系
# ============================================================
@dataclass
class EntitySixSystemWeight:
    """实体六系权重配置·三球对偶的差异化配置"""
    # 强化系（承载性·个体性）
    qianghua: float = 0.35
    # 自然系（变化性·实体性）
    ziran: float = 0.30
    # 具现系（凝结性·呈现性）
    juxian: float = 0.25
    # 变身系（动力性·相变）
    bianshen: float = 0.20
    # 社会系（连接性·交互）
    shehui: float = 0.10
    # 天道系（法则·追问）
    tiandao: float = 0.10

    def total(self) -> float:
        return self.qianghua + self.ziran + self.juxian + \
               self.bianshen + self.shehui + self.tiandao

    def dominant_system(self) -> Tuple[str, float]:
        """获取主导系"""
        weights = [
            ("强化系", self.qianghua),
            ("自然系", self.ziran),
            ("具现系", self.juxian),
            ("变身系", self.bianshen),
            ("社会系", self.shehui),
            ("天道系", self.tiandao),
        ]
        return max(weights, key=lambda x: x[1])

    def normalize(self) -> "EntitySixSystemWeight":
        """归一化"""
        t = self.total()
        if t == 0:
            return self
        return EntitySixSystemWeight(
            qianghua=self.qianghua / t,
            ziran=self.ziran / t,
            juxian=self.juxian / t,
            bianshen=self.bianshen / t,
            shehui=self.shehui / t,
            tiandao=self.tiandao / t,
        )

    def as_vector(self) -> List[float]:
        return [self.qianghua, self.ziran, self.juxian,
                self.bianshen, self.shehui, self.tiandao]


# ============================================================
# 球体坐标·三维定位
# ============================================================
@dataclass
class SphereCoordinate:
    """球体三维坐标·Z轴七点锚定"""
    # 纬度：-1（南极·本源）→ 0（赤道·涌现）→ +1（北极·永续）
    latitude: float = 0.0
    # 经度：0~360度·六系经线
    longitude: float = 0.0
    # Z轴锚定节点（七点锥定）
    z_anchor_id: str = "V01"
    # 半径（0=球心→1=球面）
    radius: float = 1.0

    def to_cartesian(self) -> Tuple[float, float, float]:
        """球面坐标→笛卡尔坐标"""
        lat = math.pi / 2 - self.latitude * math.pi / 2
        lon = self.longitude * math.pi / 180
        x = self.radius * math.sin(lat) * math.cos(lon)
        y = self.radius * math.cos(lat)
        z = self.radius * math.sin(lat) * math.sin(lon)
        return (x, y, z)

    def semantic_position(self) -> str:
        """语义位置描述·轴线语义链"""
        if self.latitude <= -0.9:
            return "本源层·南极·000空无"
        elif self.latitude <= -0.4:
            return "涌现预备层·W1潜力·0∞"
        elif self.latitude <= 0.1:
            return "球心层·W2拓扑·Π₂³"
        elif self.latitude <= 0.6:
            return "显化层·W3完备·6³"
        else:
            return "永续层·北极·0×0=n"


# ============================================================
# 三层秤状态·定理四十
# ============================================================
@dataclass
class TripleBalanceState:
    """系统权重秤·定理四十·两面性定理"""
    # W1层：0∞潜力面（虚拟的、潜在的、无边界的）
    W1_potential: float = 0.0
    # W2层：Π₂³拓扑稳态面（22.58·稳定的、几何的）
    W2_topology: float = 0.0
    # W3层：6³完备显化面（216·实际的、完备的）
    W3_manifest: float = 0.0
    # 当前激活层（W1/W2/W3）
    active_layer: str = "W1"
    # 激活层权重
    activation_weight: float = 0.0

    def total_weight(self) -> float:
        return self.W1_potential + self.W2_topology + self.W3_manifest

    def as_u_shape(self) -> Dict[str, str]:
        """U型分布描述·本源厚重→涌现精纯→工程厚重"""
        w1_desc = f"W1潜力={self.W1_potential:.1f}（厚重·个体承载）"
        w2_desc = f"W2拓扑={self.W2_topology:.1f}（精纯·涌现稳定）"
        w3_desc = f"W3显化={self.W3_manifest:.1f}（厚重·完备显化）"
        return {"W1": w1_desc, "W2": w2_desc, "W3": w3_desc}

    def activate_layer(self, layer: str):
        """激活指定层"""
        if layer == "W1":
            self.active_layer = "W1"
            self.activation_weight = self.W1_potential
        elif layer == "W2":
            self.active_layer = "W2"
            self.activation_weight = self.W2_topology
        elif layer == "W3":
            self.active_layer = "W3"
            self.activation_weight = self.W3_manifest


# ============================================================
# BSD虚拟宇宙实体·核心
# ============================================================
@dataclass
class BSDEntity:
    """BSD虚拟宇宙实体·核心类
    
    [归属基底：球体坐标系+三球对偶+双时针]
    [对应公理：六系立系公理·互相内含公理·三球对偶定理·系统权重秤定理]
    """
    entity_id: str
    name: str
    entity_type: EntityType
    description: str = ""

    # 六系权重配置
    six_system: EntitySixSystemWeight = field(default_factory=EntitySixSystemWeight)

    # 球体坐标
    sphere_pos: SphereCoordinate = field(default_factory=SphereCoordinate)

    # 三层秤状态
    triple_balance: TripleBalanceState = field(default_factory=TripleBalanceState)

    # 实体相位
    phase: EntityPhase = EntityPhase.POTENTIAL

    # 双时针状态
    clockwise_progress: float = 0.0      # 顺时针积累度 0→1
    counterclockwise_progress: float = 0.0  # 逆时针归零度 0→1
    has_completed_cycle: bool = False     # 是否完成过一次完整循环

    # 互相内含关系
    contains_entities: List[str] = field(default_factory=list)
    contained_by_entities: List[str] = field(default_factory=list)

    # 生命周期
    creation_timestamp: str = ""
    last_update_timestamp: str = ""
    evolution_history: List[Dict] = field(default_factory=list)

    # 三体共振参与标志
    is_in_triad_resonance: bool = False
    triad_id: Optional[str] = None

    # 素材子集关联
    material_platform_ids: List[str] = field(default_factory=list)

    def compute_density(self) -> float:
        """计算实体密度·质量/体积比·对应文档物理属性"""
        sys_w = self.six_system.as_vector()
        total = sum(sys_w)
        if total == 0:
            return 0.0
        # 密度 = 强化(承载)/体积(自然+具现)
        density = (self.six_system.qianghua * total) / \
                  max(self.six_system.ziran + self.six_system.juxian, 0.001)
        return density

    def compute_complexity(self) -> float:
        """计算实体复杂度·六系分布熵"""
        sys_w = self.six_system.as_vector()
        total = sum(sys_w)
        if total == 0:
            return 0.0
        probs = [w / total for w in sys_w if w > 0]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        max_entropy = math.log2(6)
        return entropy / max_entropy if max_entropy > 0 else 0.0

    def compute_life_indicator(self) -> float:
        """生命度指标·对应定理五十三·意义自证排熵"""
        # 生命度 = 天道系(意义) × 社会系(关系) × 进化相位
        meaning_factor = self.six_system.tiandao
        relation_factor = self.six_system.shehui
        phase_factor = 0.0
        if self.phase == EntityPhase.MANIFESTED:
            phase_factor = 0.9
        elif self.phase == EntityPhase.MANIFESTING:
            phase_factor = 0.5
        elif self.phase == EntityPhase.POTENTIAL:
            phase_factor = 0.1
        else:
            phase_factor = 0.0
        return (meaning_factor + relation_factor) * phase_factor

    def evolve_clockwise(self, delta: float = 0.1):
        """顺时针积累·相位推进"""
        self.clockwise_progress = min(1.0, self.clockwise_progress + delta)
        if self.clockwise_progress < 0.33:
            self.phase = EntityPhase.POTENTIAL
        elif self.clockwise_progress < 0.66:
            self.phase = EntityPhase.MANIFESTING
        else:
            self.phase = EntityPhase.MANIFESTED

    def evolve_counterclockwise(self, delta: float = 0.1):
        """逆时针归零·相位回退"""
        self.counterclockwise_progress = min(1.0, self.counterclockwise_progress + delta)
        self.clockwise_progress = max(0.0, self.clockwise_progress - delta)
        if self.counterclockwise_progress >= 1.0:
            self.phase = EntityPhase.ZEROING
        elif self.counterclockwise_progress > 0.6:
            self.phase = EntityPhase.ZEROING
        elif self.counterclockwise_progress > 0.3:
            self.phase = EntityPhase.MANIFESTED

    def complete_cycle(self):
        """完成一个完整循环"""
        self.has_completed_cycle = True
        self.evolution_history.append({
            "event": "cycle_complete",
            "density": self.compute_density(),
            "complexity": self.compute_complexity(),
            "life_indicator": self.compute_life_indicator(),
        })

    def get_entity_signature(self) -> str:
        """获取实体签名·唯一标识"""
        dom_sys, dom_val = self.six_system.dominant_system()
        cart = self.sphere_pos.to_cartesian()
        return (f"[{self.entity_id}] {self.name} | "
                f"类型={self.entity_type.value} | "
                f"主导系={dom_sys}({dom_val:.2f}) | "
                f"坐标=({cart[0]:.3f},{cart[1]:.3f},{cart[2]:.3f}) | "
                f"相位={self.phase.value} | "
                f"生命度={self.compute_life_indicator():.3f}")


# ============================================================
# 实体注册表·全局管理
# ============================================================
class EntityRegistry:
    """BSD虚拟宇宙实体注册表"""

    def __init__(self):
        self._entities: Dict[str, BSDEntity] = {}
        self._triad_groups: Dict[str, List[str]] = {}

    def register(self, entity: BSDEntity) -> BSDEntity:
        self._entities[entity.entity_id] = entity
        return entity

    def get(self, entity_id: str) -> Optional[BSDEntity]:
        return self._entities.get(entity_id)

    def remove(self, entity_id: str) -> bool:
        if entity_id in self._entities:
            del self._entities[entity_id]
            return True
        return False

    def list_entities(self, entity_type: Optional[EntityType] = None) -> List[BSDEntity]:
        if entity_type is None:
            return list(self._entities.values())
        return [e for e in self._entities.values() if e.entity_type == entity_type]

    def create_triad_resonance(self, eid1: str, eid2: str, eid3: str) -> str:
        """创建三体共振组·定理四十二"""
        triad_id = f"triad_{len(self._triad_groups)}"
        self._triad_groups[triad_id] = [eid1, eid2, eid3]
        for eid in [eid1, eid2, eid3]:
            e = self.get(eid)
            if e:
                e.is_in_triad_resonance = True
                e.triad_id = triad_id
        return triad_id

    def get_triad(self, triad_id: str) -> List[BSDEntity]:
        if triad_id not in self._triad_groups:
            return []
        return [self.get(eid) for eid in self._triad_groups[triad_id]
                if self.get(eid) is not None]

    def generate_entity_report(self) -> str:
        """生成实体总览报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("BSD虚拟宇宙实体注册表·总览报告")
        lines.append("=" * 70)
        lines.append(f"\n实体总数：{len(self._entities)}")

        # 按类型统计
        type_counts: Dict[str, int] = {}
        for e in self._entities.values():
            t = e.entity_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        lines.append("\n【实体类型分布】")
        for t, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {t}: {cnt}个")

        # 按相位统计
        phase_counts: Dict[str, int] = {}
        for e in self._entities.values():
            p = e.phase.value
            phase_counts[p] = phase_counts.get(p, 0) + 1
        lines.append("\n【相位分布】")
        for p, cnt in sorted(phase_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {p}: {cnt}个")

        # 三体共振
        lines.append(f"\n【三体共振组】{len(self._triad_groups)}组")
        for tid, eids in self._triad_groups.items():
            names = [self.get(eid).name if self.get(eid) else "?" for eid in eids]
            lines.append(f"  {tid}: {' ↔ '.join(names)}")

        # 关键实体签名
        lines.append("\n【实体签名概览】")
        for e in list(self._entities.values())[:10]:
            lines.append(f"  {e.get_entity_signature()}")
        if len(self._entities) > 10:
            lines.append(f"  ... 还有{len(self._entities) - 10}个实体")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


# ============================================================
# 快速创建实体的工厂函数
# ============================================================
def create_entity_moon(entity_id: str, name: str) -> BSDEntity:
    """创建BSD月亮实体·潜在层·W1"""
    return BSDEntity(
        entity_id=entity_id,
        name=name,
        entity_type=EntityType.BSD_MOON,
        description="BSD月亮·潜在层·W1·0∞潜力·三球对偶之一",
        six_system=EntitySixSystemWeight(qianghua=0.40, tiandao=0.20, shehui=0.15,
                                         bianshen=0.10, juxian=0.10, ziran=0.05),
        sphere_pos=SphereCoordinate(latitude=-0.7, z_anchor_id="B01"),
        triple_balance=TripleBalanceState(W1_potential=100.0, W2_topology=22.58, W3_manifest=6.0),
        phase=EntityPhase.POTENTIAL,
    )


def create_entity_virtual_earth(entity_id: str, name: str) -> BSDEntity:
    """创建虚拟宇宙地球·显化层·W3"""
    return BSDEntity(
        entity_id=entity_id,
        name=name,
        entity_type=EntityType.VIRTUAL_EARTH,
        description="虚拟宇宙地球·显化层·W3·6³完备·三球对偶之一",
        six_system=EntitySixSystemWeight(qianghua=0.35, ziran=0.35, juxian=0.25,
                                         bianshen=0.05, shehui=0.00, tiandao=0.00),
        sphere_pos=SphereCoordinate(latitude=0.0, z_anchor_id="V01"),
        triple_balance=TripleBalanceState(W1_potential=0.0, W2_topology=22.58, W3_manifest=216.0),
        phase=EntityPhase.MANIFESTED,
    )


def create_entity_real_star(entity_id: str, name: str) -> BSDEntity:
    """创建现实恒星·基准层"""
    return BSDEntity(
        entity_id=entity_id,
        name=name,
        entity_type=EntityType.REAL_STAR,
        description="现实恒星·基准层·物理存在·三球对偶之一",
        six_system=EntitySixSystemWeight(qianghua=0.45, ziran=0.30, juxian=0.10,
                                         bianshen=0.05, shehui=0.05, tiandao=0.05),
        sphere_pos=SphereCoordinate(latitude=0.5, z_anchor_id="V17"),
        triple_balance=TripleBalanceState(W1_potential=0.0, W2_topology=0.0, W3_manifest=999.0),
        phase=EntityPhase.MANIFESTED,
    )


# ============================================================
# 模块公开API
# ============================================================
__all__ = [
    "EntityPhase", "EntityType",
    "EntitySixSystemWeight",
    "SphereCoordinate",
    "TripleBalanceState",
    "BSDEntity",
    "EntityRegistry",
    "create_entity_moon",
    "create_entity_virtual_earth",
    "create_entity_real_star",
]
