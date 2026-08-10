"""
BSD虚拟宇宙场景化模块
[归属基底：L0总本源层·六系核心公理·球体坐标系·场域存在论]
[对应公理：球体坐标公理·互相内含公理·素材子集定理·场景即实体公理]
[V1.0·2026-08-01·四向展开法·场景化维度]

核心：将球体坐标空间转化为可运行的场域。
每个场景都有：坐标范围→六系氛围→实体容器→素材子集配置。
场景是实体的容器，是素材的调度中心。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


class SceneZone(str, Enum):
    """场景所在区域·对应Z轴七点语义链"""
    ORIGIN = "origin"                # 本源区·南极·B01·000空无
    POTENTIAL = "potential"          # 潜力区·W1层·0∞
    TOPOLOGY = "topology"            # 拓扑区·W2层·Π₂³球心
    MANIFEST = "manifest"            # 显化区·W3层·6³工程
    PERPETUAL = "perpetual"          # 永续区·北极·V18·0×0=n


class SceneType(str, Enum):
    """场景类型·对应六系应用学科"""
    QIANGHUA_AGRICULTURE = "agriculture"      # 强化系·农业场
    ZIRAN_BIOLOGY = "biology"                  # 自然系·生物场
    JUXIAN_INDUSTRY = "industry"              # 具现系·工业场
    BIANSHEN_CHEMISTRY = "chemistry"          # 变身系·化学场
    SHEHUI_ECONOMY = "economy"                # 社会系·经济场
    TIANDAO_POLITICS = "politics"             # 天道系·政治场
    MIXED = "mixed"                            # 混合场域


@dataclass
class SceneCoordinate:
    """场景坐标范围·球体上的一个区域"""
    lat_min: float = -1.0
    lat_max: float = 1.0
    lon_min: float = 0.0
    lon_max: float = 360.0
    center_lat: float = 0.0
    center_lon: float = 180.0
    radius_deg: float = 30.0  # 场景半径（度）

    def contains(self, lat: float, lon: float) -> bool:
        """判断坐标是否在场景内"""
        return self.lat_min <= lat <= self.lat_max and \
               self.lon_min <= lon <= self.lon_max

    def area_deg2(self) -> float:
        """场景面积（度²近似）"""
        lat_span = self.lat_max - self.lat_min
        lon_span = self.lon_max - self.lon_min
        return lat_span * lon_span


@dataclass
class SceneAtmosphere:
    """场景六系氛围·决定场域性质"""
    # 强化系权重·农业承载力
    agriculture: float = 0.20
    # 自然系权重·生物多样性
    biology: float = 0.20
    # 具现系权重·工业密度
    industry: float = 0.20
    # 变身系权重·化学反应活性
    chemistry: float = 0.15
    # 社会系权重·经济活跃度
    economy: float = 0.15
    # 天道系权重·政治控制度
    politics: float = 0.10

    def dominant_atmosphere(self) -> Tuple[str, float]:
        weights = [
            ("农业/强化", self.agriculture),
            ("生物/自然", self.biology),
            ("工业/具现", self.industry),
            ("化学/变身", self.chemistry),
            ("经济/社会", self.economy),
            ("政治/天道", self.politics),
        ]
        return max(weights, key=lambda x: x[1])

    def as_dict(self) -> Dict[str, float]:
        return {
            "agriculture": self.agriculture,
            "biology": self.biology,
            "industry": self.industry,
            "chemistry": self.chemistry,
            "economy": self.economy,
            "politics": self.politics,
        }


@dataclass
class MaterialAllocation:
    """场景素材子集分配·定理五十四"""
    primary_platform_id: str = ""       # 主素材平台（一般为Updream）
    secondary_platform_ids: List[str] = field(default_factory=list)  # 辅助素材平台
    material_capabilities: List[str] = field(default_factory=list)  # 素材能力列表
    allocation_ratio: float = 0.0        # 素材分配比

    def describe(self) -> str:
        sec = ", ".join(self.secondary_platform_ids) if self.secondary_platform_ids else "无"
        caps = ", ".join(self.material_capabilities) if self.material_capabilities else "无"
        return f"主平台={self.primary_platform_id} | 辅助=[{sec}] | 能力=[{caps}] | 分配={self.allocation_ratio:.0%}"


@dataclass
class BSDScene:
    """BSD虚拟宇宙场景·核心类
    
    [归属基底：球体坐标空间+六系学科体系+素材子集定理]
    [对应公理：场景即实体公理·互相内含公理·素材子集定理五十四]
    """
    scene_id: str
    name: str
    scene_type: SceneType
    zone: SceneZone

    # 场景坐标范围
    coord: SceneCoordinate = field(default_factory=SceneCoordinate)

    # 六系氛围
    atmosphere: SceneAtmosphere = field(default_factory=SceneAtmosphere)

    # 场域描述
    description: str = ""
    dominant_function: str = ""

    # 实体容器
    entity_ids: List[str] = field(default_factory=list)

    # 素材子集分配
    material: MaterialAllocation = field(default_factory=MaterialAllocation)

    # 场景激活状态
    is_active: bool = True
    activation_level: float = 1.0  # 0~1

    # 场景生命统计
    total_resources: float = 0.0
    complexity_index: float = 0.0

    def add_entity(self, entity_id: str):
        if entity_id not in self.entity_ids:
            self.entity_ids.append(entity_id)

    def remove_entity(self, entity_id: str):
        if entity_id in self.entity_ids:
            self.entity_ids.remove(entity_id)

    def entity_count(self) -> int:
        return len(self.entity_ids)

    def compute_complexity(self) -> float:
        """场域复杂度·基于实体数量和六系多样性"""
        base = len(self.entity_ids) * 0.1
        atm_vals = self.atmosphere.as_dict().values()
        diversity = sum(1 for v in atm_vals if v > 0.1)
        return min(10.0, base * diversity * self.activation_level)

    def activate(self, level: float = 1.0):
        self.is_active = True
        self.activation_level = max(0.0, min(1.0, level))

    def deactivate(self):
        self.is_active = False
        self.activation_level = 0.0

    def get_scene_signature(self) -> str:
        dom_atm, dom_val = self.atmosphere.dominant_atmosphere()
        return (f"[{self.scene_id}] {self.name} | "
                f"类型={self.scene_type.value} | "
                f"区域={self.zone.value} | "
                f"主导氛围={dom_atm}({dom_val:.2f}) | "
                f"实体数={self.entity_count()} | "
                f"激活度={self.activation_level:.1%} | "
                f"{self.material.describe()}")


class SceneGenerator:
    """BSD场景生成器·根据六系学科体系自动配置场景"""

    SCENE_PRESETS = {
        SceneType.QIANGHUA_AGRICULTURE: SceneAtmosphere(
            agriculture=0.50, biology=0.20, industry=0.05,
            chemistry=0.10, economy=0.10, politics=0.05
        ),
        SceneType.ZIRAN_BIOLOGY: SceneAtmosphere(
            agriculture=0.20, biology=0.50, industry=0.05,
            chemistry=0.10, economy=0.10, politics=0.05
        ),
        SceneType.JUXIAN_INDUSTRY: SceneAtmosphere(
            agriculture=0.10, biology=0.05, industry=0.55,
            chemistry=0.15, economy=0.10, politics=0.05
        ),
        SceneType.BIANSHEN_CHEMISTRY: SceneAtmosphere(
            agriculture=0.05, biology=0.10, industry=0.15,
            chemistry=0.50, economy=0.10, politics=0.10
        ),
        SceneType.SHEHUI_ECONOMY: SceneAtmosphere(
            agriculture=0.10, biology=0.10, industry=0.10,
            chemistry=0.05, economy=0.45, politics=0.20
        ),
        SceneType.TIANDAO_POLITICS: SceneAtmosphere(
            agriculture=0.05, biology=0.05, industry=0.05,
            chemistry=0.05, economy=0.20, politics=0.60
        ),
        SceneType.MIXED: SceneAtmosphere(
            agriculture=0.17, biology=0.17, industry=0.17,
            chemistry=0.16, economy=0.17, politics=0.16
        ),
    }

    ZONE_MAP = {
        SceneZone.ORIGIN: {"lat_range": (-1.0, -0.5), "lon_range": (0, 360)},
        SceneZone.POTENTIAL: {"lat_range": (-0.5, -0.1), "lon_range": (0, 360)},
        SceneZone.TOPOLOGY: {"lat_range": (-0.1, 0.1), "lon_range": (0, 360)},
        SceneZone.MANIFEST: {"lat_range": (0.1, 0.6), "lon_range": (0, 360)},
        SceneZone.PERPETUAL: {"lat_range": (0.6, 1.0), "lon_range": (0, 360)},
    }

    def __init__(self):
        self._scenes: Dict[str, BSDScene] = {}

    def create_scene(
        self,
        scene_id: str,
        name: str,
        scene_type: SceneType,
        zone: SceneZone,
        description: str = "",
    ) -> BSDScene:
        """根据预设配置创建场景"""
        # 获取六系氛围预设
        atmosphere = self.SCENE_PRESETS.get(scene_type, self.SCENE_PRESETS[SceneType.MIXED])

        # 获取区域坐标
        zone_cfg = self.ZONE_MAP.get(zone, self.ZONE_MAP[SceneZone.TOPOLOGY])
        lat_min, lat_max = zone_cfg["lat_range"]
        lon_min, lon_max = zone_cfg["lon_range"]

        # 计算中心坐标
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2

        # 根据场景类型配置素材子集
        material = self._configure_material(scene_type)

        scene = BSDScene(
            scene_id=scene_id,
            name=name,
            scene_type=scene_type,
            zone=zone,
            coord=SceneCoordinate(
                lat_min=lat_min, lat_max=lat_max,
                lon_min=lon_min, lon_max=lon_max,
                center_lat=center_lat, center_lon=center_lon,
                radius_deg=abs(lat_max - lat_min) * 30,
            ),
            atmosphere=atmosphere,
            description=description or f"{name}·{scene_type.value}场·{zone.value}区",
            dominant_function=self._describe_function(scene_type),
            material=material,
        )

        self._scenes[scene_id] = scene
        return scene

    def _configure_material(self, scene_type: SceneType) -> MaterialAllocation:
        """根据场景类型配置素材子集分配"""
        config_map = {
            SceneType.QIANGHUA_AGRICULTURE: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["pika", "vidu", "hailuo"],
                material_capabilities=["text_to_video", "image_to_video", "style_transfer", "chinese_optimized"],
                allocation_ratio=0.6,
            ),
            SceneType.ZIRAN_BIOLOGY: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["sora", "luma", "firefly"],
                material_capabilities=["text_to_video", "long_video", "physics_simulation", "nature_scene"],
                allocation_ratio=0.6,
            ),
            SceneType.JUXIAN_INDUSTRY: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["sora", "firefly", "runway"],
                material_capabilities=["text_to_video", "3d_generation", "physics_simulation", "pro_workflow"],
                allocation_ratio=0.7,
            ),
            SceneType.BIANSHEN_CHEMISTRY: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["runway", "pika", "svd"],
                material_capabilities=["text_to_video", "motion_control", "vfx_cg", "local_redraw"],
                allocation_ratio=0.5,
            ),
            SceneType.SHEHUI_ECONOMY: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["kling", "hunyuan", "jimeng"],
                material_capabilities=["text_to_video", "chinese_optimized", "multi_shot", "platform_distribution"],
                allocation_ratio=0.5,
            ),
            SceneType.TIANDAO_POLITICS: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["firefly", "luma", "runway"],
                material_capabilities=["text_to_video", "pro_workflow", "director_mode", "project_management"],
                allocation_ratio=0.4,
            ),
            SceneType.MIXED: MaterialAllocation(
                primary_platform_id="updream",
                secondary_platform_ids=["runway", "pika", "sora", "kling", "vidu", "hailuo", "luma", "svd", "firefly", "hunyuan", "jimeng"],
                material_capabilities=["text_to_video", "image_to_video", "style_transfer", "chinese_optimized", "long_video", "3d_generation"],
                allocation_ratio=0.3,
            ),
        }
        return config_map.get(scene_type, config_map[SceneType.MIXED])

    def _describe_function(self, scene_type: SceneType) -> str:
        func_map = {
            SceneType.QIANGHUA_AGRICULTURE: "承载·生长·转化原料为能量",
            SceneType.ZIRAN_BIOLOGY: "变化·繁衍·维持生态循环",
            SceneType.JUXIAN_INDUSTRY: "凝结·制造·将理念具现为产品",
            SceneType.BIANSHEN_CHEMISTRY: "相变·反应·物质形态转化",
            SceneType.SHEHUI_ECONOMY: "连接·交换·社会关系与资源流动",
            SceneType.TIANDAO_POLITICS: "法则·秩序·系统规则与治理",
            SceneType.MIXED: "综合·多系·跨领域融合场域",
        }
        return func_map.get(scene_type, "未知场域")

    def get_scene(self, scene_id: str) -> Optional[BSDScene]:
        return self._scenes.get(scene_id)

    def list_scenes(self, zone: Optional[SceneZone] = None) -> List[BSDScene]:
        if zone is None:
            return list(self._scenes.values())
        return [s for s in self._scenes.values() if s.zone == zone]

    def move_entity_to_scene(self, entity_id: str, target_scene_id: str) -> bool:
        """将实体从当前场景移到目标场景·互相内含的动态调整"""
        target = self._scenes.get(target_scene_id)
        if not target:
            return False
        # 从所有场景中移除
        for scene in self._scenes.values():
            if entity_id in scene.entity_ids:
                scene.entity_ids.remove(entity_id)
        # 添加到目标场景
        target.add_entity(entity_id)
        return True

    def generate_scene_report(self) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append("BSD虚拟宇宙场景生成器·总览报告")
        lines.append("=" * 70)
        lines.append(f"\n场景总数：{len(self._scenes)}")

        # 按区域统计
        zone_counts: Dict[str, int] = {}
        for s in self._scenes.values():
            z = s.zone.value
            zone_counts[z] = zone_counts.get(z, 0) + 1
        lines.append("\n【区域分布】")
        for z, cnt in sorted(zone_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {z}: {cnt}个场景")

        # 按类型统计
        type_counts: Dict[str, int] = {}
        for s in self._scenes.values():
            t = s.scene_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        lines.append("\n【类型分布】")
        for t, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {t}: {cnt}个场景")

        # 素材子集统计
        lines.append("\n【素材子集分配概览】")
        for s in list(self._scenes.values())[:5]:
            lines.append(f"  {s.scene_id}: {s.material.describe()}")
        if len(self._scenes) > 5:
            lines.append(f"  ... 还有{len(self._scenes) - 5}个场景")

        # 场景签名
        lines.append("\n【场景签名概览】")
        for s in list(self._scenes.values())[:10]:
            lines.append(f"  {s.get_scene_signature()}")
        if len(self._scenes) > 10:
            lines.append(f"  ... 还有{len(self._scenes) - 10}个场景")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


# 模块公开API
__all__ = [
    "SceneZone", "SceneType",
    "SceneCoordinate", "SceneAtmosphere",
    "MaterialAllocation",
    "BSDScene",
    "SceneGenerator",
]
