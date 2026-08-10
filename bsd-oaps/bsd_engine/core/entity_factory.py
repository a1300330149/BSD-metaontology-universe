"""
BSD虚拟宇宙实体工厂模块
[归属基底：L0总本源层·六系核心公理·实体存在论·互相内含]
[对应公理：实体存在论·场景即实体公理·互相内含公理]
[V1.0·2026-08-01·实体扩展·批量创建+自动分配]

核心：批量创建特定类型实体，并根据六系属性自动分配到最佳场景。
工厂支持：按类型批量生成、按属性智能分配、三体共振自动组建、生命周期自动注册。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random

from bsd_entity import (
    BSDEntity, EntityType, EntityPhase, EntityRegistry,
    EntitySixSystemWeight, SphereCoordinate, TripleBalanceState,
)
from bsd_scene import (
    BSDScene, SceneType, SceneZone, SceneGenerator,
)
from bsd_timeline import BSDTimeline, LifecyclePhase, LifecycleState


class FactoryStrategy(str, Enum):
    """工厂创建策略"""
    UNIFORM = "uniform"                  # 均匀创建·所有实体相同
    GRADIENT = "gradient"                # 梯度创建·权重渐变
    RANDOM = "random"                    # 随机创建·权重随机
    DIVERSIFIED = "diversified"          # 多样化创建·覆盖多系


class AssignmentStrategy(str, Enum):
    """场景分配策略"""
    AUTO_BY_SYSTEM = "auto_by_system"    # 根据主导系自动分配
    AUTO_BY_ZONE = "auto_by_zone"        # 根据区域自动分配
    ROUND_ROBIN = "round_robin"          # 轮询分配
    DENSITY_BALANCE = "density_balance"  # 密度平衡分配
    MANUAL = "manual"                    # 手动指定


@dataclass
class EntityTemplate:
    """实体创建模板"""
    entity_type: EntityType
    base_weight: EntitySixSystemWeight = field(default_factory=EntitySixSystemWeight)
    latitude_range: Tuple[float, float] = (-1.0, 1.0)
    longitude_range: Tuple[float, float] = (0.0, 360.0)
    z_anchor_id: str = "V01"
    base_name_prefix: str = "Entity"
    base_description: str = ""
    phase: EntityPhase = EntityPhase.POTENTIAL
    lifecycle_config: Dict = field(default_factory=dict)


@dataclass
class FactoryBatchResult:
    """批量创建结果"""
    batch_id: str
    entities_created: List[BSDEntity]
    entities_assigned: Dict[str, List[str]]  # scene_id -> [entity_ids]
    triad_groups_created: List[str]
    total_count: int
    success_rate: float

    def summary(self) -> str:
        lines = [f"批量创建#{self.batch_id}: {self.total_count}个实体"]
        lines.append(f"  成功率: {self.success_rate:.0%}")
        lines.append(f"  创建实体数: {len(self.entities_created)}")
        lines.append(f"  分配场景数: {len(self.entities_assigned)}")
        lines.append(f"  三体组数: {len(self.triad_groups_created)}")
        for sid, eids in self.entities_assigned.items():
            lines.append(f"    场景{sid}: {len(eids)}个实体")
        return "\n".join(lines)


class BSDEntityFactory:
    """BSD实体工厂·批量创建+自动分配
    
    [归属基底：实体存在论+场景即实体公理+互相内含公理]
    [对应公理：实体存在论·六系属性决定场景归属·三体共振自动组建]
    """

    # 实体类型→推荐场景类型映射
    ENTITY_TYPE_SCENE_MAP: Dict[EntityType, List[SceneType]] = {
        EntityType.ABSTRACT: [SceneType.MIXED, SceneType.TIANDAO_POLITICS],
        EntityType.MATERIAL: [SceneType.JUXIAN_INDUSTRY, SceneType.BIANSHEN_CHEMISTRY],
        EntityType.SOCIAL: [SceneType.SHEHUI_ECONOMY, SceneType.MIXED],
        EntityType.NATURAL: [SceneType.ZIRAN_BIOLOGY, SceneType.QIANGHUA_AGRICULTURE],
        EntityType.EVOLUTIONARY: [SceneType.TIANDAO_POLITICS, SceneType.MIXED],
        EntityType.BSD_MOON: [SceneType.MIXED],
        EntityType.VIRTUAL_EARTH: [SceneType.JUXIAN_INDUSTRY, SceneType.MIXED],
        EntityType.REAL_STAR: [SceneType.MIXED],
    }

    # 实体类型→六系推荐权重映射
    ENTITY_TYPE_WEIGHT_MAP: Dict[EntityType, EntitySixSystemWeight] = {
        EntityType.ABSTRACT: EntitySixSystemWeight(qianghua=0.10, ziran=0.10, juxian=0.10,
                                                   bianshen=0.15, shehui=0.15, tiandao=0.40),
        EntityType.MATERIAL: EntitySixSystemWeight(qianghua=0.30, ziran=0.15, juxian=0.30,
                                                   bianshen=0.15, shehui=0.05, tiandao=0.05),
        EntityType.SOCIAL: EntitySixSystemWeight(qianghua=0.15, ziran=0.15, juxian=0.10,
                                                 bianshen=0.10, shehui=0.35, tiandao=0.15),
        EntityType.NATURAL: EntitySixSystemWeight(qianghua=0.20, ziran=0.35, juxian=0.15,
                                                   bianshen=0.15, shehui=0.10, tiandao=0.05),
        EntityType.EVOLUTIONARY: EntitySixSystemWeight(qianghua=0.15, ziran=0.15, juxian=0.10,
                                                       bianshen=0.15, shehui=0.15, tiandao=0.30),
    }

    def __init__(
        self,
        entity_registry: EntityRegistry,
        scene_generator: SceneGenerator,
        timeline: BSDTimeline,
    ):
        self.registry = entity_registry
        self.scene_gen = scene_generator
        self.timeline = timeline
        self._batch_counter = 0
        self._templates: Dict[str, EntityTemplate] = {}
        self._assignment_log: List[Dict] = []

    def register_template(self, template_id: str, template: EntityTemplate):
        """注册实体创建模板"""
        self._templates[template_id] = template

    def create_batch(
        self,
        entity_type: EntityType,
        count: int,
        strategy: FactoryStrategy = FactoryStrategy.UNIFORM,
        assignment: AssignmentStrategy = AssignmentStrategy.AUTO_BY_SYSTEM,
        prefix: str = "",
        weight_override: Optional[EntitySixSystemWeight] = None,
        create_triad: bool = True,
        auto_register_timeline: bool = True,
    ) -> FactoryBatchResult:
        """批量创建实体并自动分配场景
        
        Args:
            entity_type: 实体类型
            count: 创建数量
            strategy: 创建策略
            assignment: 分配策略
            prefix: 实体ID前缀
            weight_override: 权重覆盖
            create_triad: 是否自动组建三体共振
            auto_register_timeline: 是否自动注册生命周期
        """
        self._batch_counter += 1
        batch_id = f"batch_{self._batch_counter:03d}"
        
        entities: List[BSDEntity] = []
        prefix = prefix or entity_type.value
        
        # 获取基础权重
        base_weight = weight_override or self.ENTITY_TYPE_WEIGHT_MAP.get(
            entity_type, EntitySixSystemWeight()
        )
        
        for i in range(count):
            # 根据策略计算个体权重
            individual_weight = self._compute_individual_weight(
                base_weight, strategy, i, count
            )
            
            # 根据策略计算坐标
            coords = self._compute_coordinates(entity_type, strategy, i, count)
            
            # 创建实体
            entity_id = f"{prefix}_{i+1:03d}"
            entity = BSDEntity(
                entity_id=entity_id,
                name=f"{prefix}-{i+1:03d}",
                entity_type=entity_type,
                description=f"工厂批量创建·{entity_type.value}·#{i+1}",
                six_system=individual_weight,
                sphere_pos=SphereCoordinate(
                    latitude=coords[0],
                    longitude=coords[1],
                    z_anchor_id=self._map_latitude_to_anchor(coords[0]),
                ),
                triple_balance=TripleBalanceState(
                    W1_potential=100.0 * individual_weight.qianghua,
                    W2_topology=22.58,
                    W3_manifest=216.0 * individual_weight.juxian,
                ),
                phase=EntityPhase.POTENTIAL,
            )
            
            # 注册实体
            self.registry.register(entity)
            entities.append(entity)
            
            # 注册生命周期
            if auto_register_timeline:
                self.timeline.register_entity_lifecycle(
                    entity_id,
                    emergence_duration=5.0,
                    growth_duration=15.0 + i * 2.0,
                    stability_duration=30.0 + i * 3.0,
                    decay_duration=8.0,
                    zeroing_duration=5.0,
                    max_cycles=2,
                )
        
        # 自动分配到场景
        assignment_map = self._assign_to_scenes(entities, assignment)
        
        # 自动组建三体共振
        triad_groups: List[str] = []
        if create_triad and len(entities) >= 3:
            triad_groups = self._auto_create_triads(entities)
        
        # 记录分配日志
        self._assignment_log.append({
            "batch_id": batch_id,
            "entity_type": entity_type.value,
            "count": count,
            "strategy": strategy.value,
            "assignment": assignment.value,
            "scenes_used": list(assignment_map.keys()),
            "triads_created": len(triad_groups),
        })
        
        success_rate = len(entities) / count if count > 0 else 0.0
        
        return FactoryBatchResult(
            batch_id=batch_id,
            entities_created=entities,
            entities_assigned=assignment_map,
            triad_groups_created=triad_groups,
            total_count=count,
            success_rate=success_rate,
        )

    def _compute_individual_weight(
        self,
        base: EntitySixSystemWeight,
        strategy: FactoryStrategy,
        index: int,
        total: int,
    ) -> EntitySixSystemWeight:
        """计算个体权重·根据策略差异化"""
        if strategy == FactoryStrategy.UNIFORM:
            return EntitySixSystemWeight(
                qianghua=base.qianghua,
                ziran=base.ziran,
                juxian=base.juxian,
                bianshen=base.bianshen,
                shehui=base.shehui,
                tiandao=base.tiandao,
            )
        elif strategy == FactoryStrategy.GRADIENT:
            # 梯度策略·权重渐变
            t = index / max(total - 1, 1)
            return EntitySixSystemWeight(
                qianghua=base.qianghua * (1 - t) + 0.1 * t,
                ziran=base.ziran * (1 - t) + 0.2 * t,
                juxian=base.juxian * (1 - t) + 0.3 * t,
                bianshen=base.bianshen * (1 - t) + 0.2 * t,
                shehui=base.shehui * (1 - t) + 0.15 * t,
                tiandao=base.tiandao * (1 - t) + 0.05 * t,
            )
        elif strategy == FactoryStrategy.RANDOM:
            total = base.total()
            scale = 1.0 if total > 0 else 0.35
            return EntitySixSystemWeight(
                qianghua=random.uniform(0.1, 0.5),
                ziran=random.uniform(0.1, 0.5),
                juxian=random.uniform(0.1, 0.5),
                bianshen=random.uniform(0.05, 0.3),
                shehui=random.uniform(0.05, 0.3),
                tiandao=random.uniform(0.05, 0.3),
            )
        elif strategy == FactoryStrategy.DIVERSIFIED:
            # 多样化策略·每个实体强化不同的系
            systems = ["qianghua", "ziran", "juxian", "bianshen", "shehui", "tiandao"]
            dominant_idx = index % 6
            weights = [0.15] * 6
            weights[dominant_idx] = 0.50
            return EntitySixSystemWeight(
                **{systems[i]: w for i, w in enumerate(weights)}
            )
        return base

    def _compute_coordinates(
        self,
        entity_type: EntityType,
        strategy: FactoryStrategy,
        index: int,
        total: int,
    ) -> Tuple[float, float]:
        """计算实体坐标"""
        if strategy == FactoryStrategy.RANDOM:
            lat = random.uniform(-1.0, 1.0)
            lon = random.uniform(0, 360)
        elif strategy == FactoryStrategy.GRADIENT:
            t = index / max(total - 1, 1)
            lat = -1.0 + 2.0 * t  # 从南极到北极
            lon = (index * 360.0 / max(total, 1)) % 360
        elif strategy == FactoryStrategy.DIVERSIFIED:
            lat = -1.0 + 2.0 * (index // 6) / max(total // 6, 1)
            lon = (index % 6) * 60.0 + 30.0
        else:
            lat = 0.0
            lon = (index * 360.0 / max(total, 1)) % 360
        
        return (lat, lon)

    def _map_latitude_to_anchor(self, lat: float) -> str:
        """根据纬度映射到Z轴锚定节点"""
        if lat <= -0.9:
            return "B01"
        elif lat <= -0.4:
            return "W1"
        elif lat <= 0.1:
            return "V01"
        elif lat <= 0.6:
            return "W3"
        else:
            return "V18"

    def _assign_to_scenes(
        self,
        entities: List[BSDEntity],
        strategy: AssignmentStrategy,
    ) -> Dict[str, List[str]]:
        """将实体分配到场景"""
        assignment_map: Dict[str, List[str]] = {}
        available_scenes = self.scene_gen.list_scenes()
        
        if not available_scenes:
            return assignment_map
        
        if strategy == AssignmentStrategy.AUTO_BY_SYSTEM:
            # 根据主导系自动分配
            for entity in entities:
                dom_sys, _ = entity.six_system.dominant_system()
                target_scene = self._find_scene_by_system(dom_sys, available_scenes)
                if target_scene:
                    target_scene.add_entity(entity.entity_id)
                    if target_scene.scene_id not in assignment_map:
                        assignment_map[target_scene.scene_id] = []
                    assignment_map[target_scene.scene_id].append(entity.entity_id)
        
        elif strategy == AssignmentStrategy.AUTO_BY_ZONE:
            # 根据区域自动分配
            for entity in entities:
                lat = entity.sphere_pos.latitude
                target_scene = self._find_scene_by_latitude(lat, available_scenes)
                if target_scene:
                    target_scene.add_entity(entity.entity_id)
                    if target_scene.scene_id not in assignment_map:
                        assignment_map[target_scene.scene_id] = []
                    assignment_map[target_scene.scene_id].append(entity.entity_id)
        
        elif strategy == AssignmentStrategy.ROUND_ROBIN:
            # 轮询分配
            for i, entity in enumerate(entities):
                scene = available_scenes[i % len(available_scenes)]
                scene.add_entity(entity.entity_id)
                if scene.scene_id not in assignment_map:
                    assignment_map[scene.scene_id] = []
                assignment_map[scene.scene_id].append(entity.entity_id)
        
        elif strategy == AssignmentStrategy.DENSITY_BALANCE:
            # 密度平衡·分配到实体最少的场景
            for entity in entities:
                min_scene = min(available_scenes, key=lambda s: s.entity_count())
                min_scene.add_entity(entity.entity_id)
                if min_scene.scene_id not in assignment_map:
                    assignment_map[min_scene.scene_id] = []
                assignment_map[min_scene.scene_id].append(entity.entity_id)
        
        return assignment_map

    def _find_scene_by_system(
        self,
        system_name: str,
        scenes: List[BSDScene],
    ) -> Optional[BSDScene]:
        """根据六系名称查找最佳场景"""
        # 系统名→场景类型的映射
        sys_scene_map = {
            "强化系": SceneType.QIANGHUA_AGRICULTURE,
            "自然系": SceneType.ZIRAN_BIOLOGY,
            "具现系": SceneType.JUXIAN_INDUSTRY,
            "变身系": SceneType.BIANSHEN_CHEMISTRY,
            "社会系": SceneType.SHEHUI_ECONOMY,
            "天道系": SceneType.TIANDAO_POLITICS,
        }
        target_type = sys_scene_map.get(system_name)
        # 优先找类型匹配的场景
        for scene in scenes:
            if target_type and scene.scene_type == target_type:
                return scene
        # 否则找混合场景
        for scene in scenes:
            if scene.scene_type == SceneType.MIXED:
                return scene
        return scenes[0] if scenes else None

    def _find_scene_by_latitude(
        self,
        lat: float,
        scenes: List[BSDScene],
    ) -> Optional[BSDScene]:
        """根据纬度查找最佳场景"""
        target_zone = None
        if lat <= -0.5:
            target_zone = SceneZone.ORIGIN
        elif lat <= -0.1:
            target_zone = SceneZone.POTENTIAL
        elif lat <= 0.1:
            target_zone = SceneZone.TOPOLOGY
        elif lat <= 0.6:
            target_zone = SceneZone.MANIFEST
        else:
            target_zone = SceneZone.PERPETUAL
        
        for scene in scenes:
            if scene.zone == target_zone:
                return scene
        return scenes[0] if scenes else None

    def _auto_create_triads(self, entities: List[BSDEntity]) -> List[str]:
        """自动组建三体共振组"""
        triad_ids: List[str] = []
        for i in range(0, len(entities) - 2, 3):
            e1, e2, e3 = entities[i], entities[i+1], entities[i+2]
            triad_id = self.registry.create_triad_resonance(
                e1.entity_id, e2.entity_id, e3.entity_id
            )
            triad_ids.append(triad_id)
        return triad_ids

    def get_assignment_log(self, limit: int = 20) -> List[Dict]:
        """获取分配日志"""
        return self._assignment_log[-limit:]

    def generate_factory_report(self) -> str:
        """生成工厂报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("BSD实体工厂·总览报告")
        lines.append("=" * 70)
        
        lines.append(f"\n总批次数：{self._batch_counter}")
        lines.append(f"实体注册表总数：{len(self.registry.list_entities())}")
        
        # 按类型统计
        type_counts: Dict[str, int] = {}
        for e in self.registry.list_entities():
            t = e.entity_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        lines.append("\n【实体类型分布】")
        for t, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {t}: {cnt}个")
        
        # 分配日志
        lines.append(f"\n【分配日志】最近{len(self._assignment_log)}条")
        for log in self._assignment_log[-5:]:
            lines.append(f"  #{log['batch_id']}: {log['entity_type']}×{log['count']} | {log['strategy']} | {log['assignment']} | {log['scenes_used']}")
        
        # 三体统计
        lines.append(f"\n【三体共振组】{len(self.registry._triad_groups)}组")
        
        # 模板统计
        lines.append(f"\n【已注册模板】{len(self._templates)}个")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


def create_population_mix(
    factory: BSDEntityFactory,
    counts: Dict[EntityType, int],
    strategy: FactoryStrategy = FactoryStrategy.DIVERSIFIED,
) -> List[FactoryBatchResult]:
    """创建一个完整的实体种群混合·覆盖多种类型"""
    results: List[FactoryBatchResult] = []
    
    for entity_type, count in counts.items():
        if count > 0:
            result = factory.create_batch(
                entity_type=entity_type,
                count=count,
                strategy=strategy,
                assignment=AssignmentStrategy.AUTO_BY_SYSTEM,
                create_triad=True,
            )
            results.append(result)
    
    return results


# 模块公开API
__all__ = [
    "FactoryStrategy", "AssignmentStrategy",
    "EntityTemplate", "FactoryBatchResult",
    "BSDEntityFactory", "create_population_mix",
]
