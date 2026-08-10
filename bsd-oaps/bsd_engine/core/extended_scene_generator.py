"""
BSD虚拟宇宙场景扩展模块
[归属基底：L0总本源层·六系核心公理·球体坐标系·互相内含]
[对应公理：场景即实体公理·跨区融合公理·互相内含进阶]
[V1.0·2026-08-01·场景扩展·混合场域+跨区域复合场]

核心：在基础场景之上，提供混合场域和跨区域复合场的高级场景生成。
混合场域：单区域内多系融合（如农业+生物+化学混合场）
复合场：跨区域场域耦合（如潜力-显化复合场·拓扑-永续复合场）
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math

from bsd_scene import (
    SceneZone, SceneType, SceneCoordinate, SceneAtmosphere,
    MaterialAllocation, BSDScene, SceneGenerator,
)


class CompoundMode(str, Enum):
    """复合模式"""
    MIXED_WITHIN_ZONE = "mixed_within_zone"          # 单区域内混合
    CROSS_ZONE_BRIDGE = "cross_zone_bridge"          # 跨区域桥接
    MULTI_ZONE_ARCH = "multi_zone_arch"              # 多区域拱门
    SPANNING_POLE = "spanning_pole"                  # 极轴贯穿


class MixedSceneConfig:
    """混合场域配置·单区域内多系融合"""

    def __init__(self, configs: List[Tuple[SceneType, float]]):
        self.configs = configs  # [(SceneType, 权重), ...]
        
    def compute_atmosphere(self) -> SceneAtmosphere:
        """根据子场景类型加权计算混合氛围"""
        atmo = SceneAtmosphere()
        for stype, weight in self.configs:
            preset = SceneGenerator.SCENE_PRESETS.get(stype, SceneAtmosphere())
            atmo.agriculture += preset.agriculture * weight
            atmo.biology += preset.biology * weight
            atmo.industry += preset.industry * weight
            atmo.chemistry += preset.chemistry * weight
            atmo.economy += preset.economy * weight
            atmo.politics += preset.politics * weight
        # 归一化
        total = atmo.agriculture + atmo.biology + atmo.industry + \
                atmo.chemistry + atmo.economy + atmo.politics
        if total > 0:
            atmo.agriculture /= total
            atmo.biology /= total
            atmo.industry /= total
            atmo.chemistry /= total
            atmo.economy /= total
            atmo.politics /= total
        return atmo

    def compute_material(self) -> MaterialAllocation:
        """计算混合素材配置·取各子场景素材的并集"""
        all_platforms = []
        all_capabilities = []
        for stype, _ in self.configs:
            mat = SceneGenerator()._configure_material(stype)
            if mat.primary_platform_id:
                all_platforms.append(mat.primary_platform_id)
            all_platforms.extend(mat.secondary_platform_ids)
            all_capabilities.extend(mat.material_capabilities)
        
        # 去重
        all_platforms = list(dict.fromkeys(all_platforms))
        all_capabilities = list(dict.fromkeys(all_capabilities))
        
        primary = all_platforms[0] if all_platforms else "updream"
        secondary = all_platforms[1:7] if len(all_platforms) > 1 else []
        
        return MaterialAllocation(
            primary_platform_id=primary,
            secondary_platform_ids=secondary,
            material_capabilities=all_capabilities[:8],
            allocation_ratio=min(0.8, 0.3 + 0.1 * len(self.configs)),
        )

    def describe(self) -> str:
        parts = [f"{st.value}(w={w:.1f})" for st, w in self.configs]
        return f"混合[{'+'.join(parts)}]"


@dataclass
class CompoundSceneLink:
    """跨区域复合场·链接配置"""
    source_zone: SceneZone
    target_zone: SceneZone
    bridge_type: str = "direct"  # direct/arch/spanning
    bridge_strength: float = 1.0
    bidirectional: bool = True
    description: str = ""


class ExtendedSceneGenerator:
    """BSD扩展场景生成器·混合场域+跨区域复合场"""

    def __init__(self, base_generator: Optional[SceneGenerator] = None):
        self.base = base_generator or SceneGenerator()
        self._mixed_scenes: Dict[str, BSDScene] = {}
        self._compound_links: List[CompoundSceneLink] = []

    def create_mixed_scene(
        self,
        scene_id: str,
        name: str,
        zone: SceneZone,
        configs: List[Tuple[SceneType, float]],
        description: str = "",
    ) -> BSDScene:
        """创建混合场域·单区域内多系融合
        
        Args:
            scene_id: 场景ID
            name: 场景名称
            zone: 所在区域
            configs: [(SceneType, 权重), ...] 至少2种类型
            description: 描述
        """
        assert len(configs) >= 2, "混合场域至少需要2种子类型"
        
        cfg = MixedSceneConfig(configs)
        atmosphere = cfg.compute_atmosphere()
        material = cfg.compute_material()
        
        # 计算区域坐标
        zone_cfg = self.base.ZONE_MAP.get(zone, self.base.ZONE_MAP[SceneZone.TOPOLOGY])
        lat_min, lat_max = zone_cfg["lat_range"]
        
        # 混合场域在区域内创建一个子区域
        sub_lat_min = lat_min + 0.1
        sub_lat_max = lat_max - 0.1
        if sub_lat_min >= sub_lat_max:
            sub_lat_min = lat_min
            sub_lat_max = lat_max
        
        scene = BSDScene(
            scene_id=scene_id,
            name=name,
            scene_type=SceneType.MIXED,
            zone=zone,
            coord=SceneCoordinate(
                lat_min=sub_lat_min, lat_max=sub_lat_max,
                lon_min=45.0, lon_max=315.0,  # 180度跨度
                center_lat=(sub_lat_min + sub_lat_max) / 2,
                center_lon=180.0,
                radius_deg=45.0,
            ),
            atmosphere=atmosphere,
            description=description or f"{name}·{cfg.describe()}·{zone.value}区",
            dominant_function=self._describe_mixed_function(configs),
            material=material,
        )
        
        self._mixed_scenes[scene_id] = scene
        self.base._scenes[scene_id] = scene
        return scene

    def create_compound_scene(
        self,
        scene_id: str,
        name: str,
        source_config: Tuple[SceneType, SceneZone],
        target_config: Tuple[SceneType, SceneZone],
        bridge_type: str = "direct",
        description: str = "",
    ) -> BSDScene:
        """创建跨区域复合场·两个不同区域的场景耦合
        
        Args:
            scene_id: 场景ID
            name: 场景名称
            source_config: (源场景类型, 源区域)
            target_config: (目标场景类型, 目标区域)
            bridge_type: 桥接类型 direct/arch/spanning
        """
        src_type, src_zone = source_config
        tgt_type, tgt_zone = target_config
        
        # 计算跨区域坐标·覆盖两个区域
        src_cfg = self.base.ZONE_MAP[src_zone]
        tgt_cfg = self.base.ZONE_MAP[tgt_zone]
        
        lat_min = min(src_cfg["lat_range"][0], tgt_cfg["lat_range"][0])
        lat_max = max(src_cfg["lat_range"][1], tgt_cfg["lat_range"][1])
        
        # 混合氛围·两种类型加权
        atmo_src = self.base.SCENE_PRESETS.get(src_type, SceneAtmosphere())
        atmo_tgt = self.base.SCENE_PRESETS.get(tgt_type, SceneAtmosphere())
        atmosphere = SceneAtmosphere(
            agriculture=(atmo_src.agriculture + atmo_tgt.agriculture) / 2,
            biology=(atmo_src.biology + atmo_tgt.biology) / 2,
            industry=(atmo_src.industry + atmo_tgt.industry) / 2,
            chemistry=(atmo_src.chemistry + atmo_tgt.chemistry) / 2,
            economy=(atmo_src.economy + atmo_tgt.economy) / 2,
            politics=(atmo_src.politics + atmo_tgt.politics) / 2,
        )
        
        # 复合素材配置
        mat_src = self.base._configure_material(src_type)
        mat_tgt = self.base._configure_material(tgt_type)
        material = MaterialAllocation(
            primary_platform_id=mat_src.primary_platform_id,
            secondary_platform_ids=list(set(mat_src.secondary_platform_ids + mat_tgt.secondary_platform_ids))[:6],
            material_capabilities=list(dict.fromkeys(mat_src.material_capabilities + mat_tgt.material_capabilities))[:6],
            allocation_ratio=0.7,
        )
        
        # 复合场景使用MIXED类型·跨越两个区域
        mid_lat = (lat_min + lat_max) / 2
        scene = BSDScene(
            scene_id=scene_id,
            name=name,
            scene_type=SceneType.MIXED,
            zone=src_zone,  # 使用源区域作为主区域标识
            coord=SceneCoordinate(
                lat_min=lat_min, lat_max=lat_max,
                lon_min=0, lon_max=360,
                center_lat=mid_lat,
                center_lon=180.0,
                radius_deg=90.0,
            ),
            atmosphere=atmosphere,
            description=description or f"{name}·{src_zone.value}→{tgt_zone.value}·{bridge_type}桥接",
            dominant_function=self._describe_compound_function(src_type, tgt_type, bridge_type),
            material=material,
        )
        
        # 记录复合链接
        self._compound_links.append(CompoundSceneLink(
            source_zone=src_zone,
            target_zone=tgt_zone,
            bridge_type=bridge_type,
            description=f"{scene_id}: {src_type.value}({src_zone.value}) ↔ {tgt_type.value}({tgt_zone.value})",
        ))
        
        self._mixed_scenes[scene_id] = scene
        self.base._scenes[scene_id] = scene
        return scene

    def _describe_mixed_function(self, configs: List[Tuple[SceneType, float]]) -> str:
        func_map = {
            SceneType.QIANGHUA_AGRICULTURE: "承载·生长",
            SceneType.ZIRAN_BIOLOGY: "变化·繁衍",
            SceneType.JUXIAN_INDUSTRY: "凝结·制造",
            SceneType.BIANSHEN_CHEMISTRY: "相变·反应",
            SceneType.SHEHUI_ECONOMY: "连接·交换",
            SceneType.TIANDAO_POLITICS: "法则·秩序",
        }
        parts = [func_map.get(st, "未知") for st, _ in configs]
        return f"混合场·{'×'.join(parts)}·互相内含融合"

    def _describe_compound_function(self, src_type: SceneType, tgt_type: SceneType, bridge: str) -> str:
        src_func = self.base._describe_function(src_type)
        tgt_func = self.base._describe_function(tgt_type)
        bridge_desc = {"direct": "直接桥接", "arch": "拱门结构", "spanning": "极轴贯穿"}.get(bridge, bridge)
        return f"复合场·{src_func}↔{tgt_func}·{bridge_desc}"

    def get_compound_report(self) -> str:
        """生成扩展场景报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("BSD扩展场景生成器·混合场域+跨区域复合场")
        lines.append("=" * 70)
        
        lines.append(f"\n【混合场域】{len(self._mixed_scenes)}个")
        for sid, scene in self._mixed_scenes.items():
            lines.append(f"  {scene.get_scene_signature()}")
        
        lines.append(f"\n【跨区域复合链接】{len(self._compound_links)}条")
        for link in self._compound_links:
            lines.append(f"  {link.description} | 桥接={link.bridge_type} | 强度={link.bridge_strength}")
        
        # 区域间桥接统计
        zone_pairs: Dict[str, int] = {}
        for link in self._compound_links:
            key = f"{link.source_zone.value}↔{link.target_zone.value}"
            zone_pairs[key] = zone_pairs.get(key, 0) + 1
        lines.append("\n【区域桥接统计】")
        for pair, count in zone_pairs.items():
            lines.append(f"  {pair}: {count}条桥接")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


def create_standard_extended_scenes(generator: ExtendedSceneGenerator) -> List[BSDScene]:
    """创建标准扩展场景套件·6个混合场+3个复合场"""
    created: List[BSDScene] = []
    
    # === 混合场域（单区域多系融合）===
    
    # 1. 潜力区·农业+生物混合场·强化系与自然系融合
    created.append(generator.create_mixed_scene(
        "mixed_agri_bio", "农生融合场", SceneZone.POTENTIAL,
        [(SceneType.QIANGHUA_AGRICULTURE, 0.5), (SceneType.ZIRAN_BIOLOGY, 0.5)],
        description="潜力区·农业(强化)×生物(自然)混合·生命属性涌现预备",
    ))
    
    # 2. 拓扑区·化学+工业混合场·变身系与具现系融合
    created.append(generator.create_mixed_scene(
        "mixed_chem_ind", "化工融合场", SceneZone.TOPOLOGY,
        [(SceneType.BIANSHEN_CHEMISTRY, 0.5), (SceneType.JUXIAN_INDUSTRY, 0.5)],
        description="拓扑区·化学(变身)×工业(具现)混合·相变预备",
    ))
    
    # 3. 显化区·工业+经济+社会三重混合
    created.append(generator.create_mixed_scene(
        "mixed_ind_eco", "工信融合场", SceneZone.MANIFEST,
        [(SceneType.JUXIAN_INDUSTRY, 0.4), (SceneType.SHEHUI_ECONOMY, 0.3), (SceneType.ZIRAN_BIOLOGY, 0.3)],
        description="显化区·工业×经济×生物三重混合·社会-生态-产业共生",
    ))
    
    # 4. 永续区·政治+经济+天道三重混合
    created.append(generator.create_mixed_scene(
        "mixed_pol_eco", "政经融合场", SceneZone.PERPETUAL,
        [(SceneType.TIANDAO_POLITICS, 0.5), (SceneType.SHEHUI_ECONOMY, 0.3), (SceneType.QIANGHUA_AGRICULTURE, 0.2)],
        description="永续区·政治×经济×农业混合·天道秩序下的经济治理",
    ))
    
    # 5. 显化区·全六系混合场·互相内含终极形态
    created.append(generator.create_mixed_scene(
        "mixed_all_systems", "六系太极场", SceneZone.MANIFEST,
        [
            (SceneType.QIANGHUA_AGRICULTURE, 0.20),
            (SceneType.ZIRAN_BIOLOGY, 0.20),
            (SceneType.JUXIAN_INDUSTRY, 0.15),
            (SceneType.BIANSHEN_CHEMISTRY, 0.15),
            (SceneType.SHEHUI_ECONOMY, 0.15),
            (SceneType.TIANDAO_POLITICS, 0.15),
        ],
        description="显化区·全六系混合·互相内含终极形态·六系太极",
    ))
    
    # 6. 潜力区·本源孕育混合场
    created.append(generator.create_mixed_scene(
        "mixed_primordial", "本源孕育场", SceneZone.POTENTIAL,
        [(SceneType.MIXED, 0.6), (SceneType.QIANGHUA_AGRICULTURE, 0.4)],
        description="潜力区·本源孕育·0∞潜力的初始混合态",
    ))
    
    # === 跨区域复合场 ===
    
    # 7. 潜力→显化·直接桥接·农业场→工业场
    created.append(generator.create_compound_scene(
        "compound_agri_ind", "农工桥接场",
        (SceneType.QIANGHUA_AGRICULTURE, SceneZone.POTENTIAL),
        (SceneType.JUXIAN_INDUSTRY, SceneZone.MANIFEST),
        bridge_type="direct",
        description="潜力(农业)→显化(工业)·直接桥接·原料→产品的连续体",
    ))
    
    # 8. 拓扑→永续·拱门桥接·化学场→政治场
    created.append(generator.create_compound_scene(
        "compound_chem_pol", "化政拱门场",
        (SceneType.BIANSHEN_CHEMISTRY, SceneZone.TOPOLOGY),
        (SceneType.TIANDAO_POLITICS, SceneZone.PERPETUAL),
        bridge_type="arch",
        description="拓扑(化学)→永续(政治)·拱门桥接·微观反应→宏观秩序",
    ))
    
    # 9. 本源→永续·极轴贯穿·混合场
    created.append(generator.create_compound_scene(
        "compound_origin_perpetual", "本源永续极轴场",
        (SceneType.MIXED, SceneZone.ORIGIN),
        (SceneType.MIXED, SceneZone.PERPETUAL),
        bridge_type="spanning",
        description="本源→永续·极轴贯穿·0→n→∞→0完整Z轴语义链",
    ))
    
    return created


# 模块公开API
__all__ = [
    "CompoundMode", "MixedSceneConfig", "CompoundSceneLink",
    "ExtendedSceneGenerator", "create_standard_extended_scenes",
]
