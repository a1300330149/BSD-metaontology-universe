"""
BSD虚拟宇宙引擎·核心整合模块
[归属基底：L0总本源层·六系核心公理·球体坐标系·双时针·互相内含]
[对应公理：所有核心公理的工程集成·SAGA引擎工作流]
[V1.0·2026-08-01·四向展开法·引擎核心]

核心：整合实体化、场景化、时间化、规则化四个维度，
形成可运行的BSD虚拟宇宙引擎。
引擎遵循SAGA工作流：感知→分析→生成→行动。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math

# 导入四个维度的模块
from bsd_entity import (
    BSDEntity, EntityType, EntityPhase, EntityRegistry,
    EntitySixSystemWeight, SphereCoordinate, TripleBalanceState,
    create_entity_moon, create_entity_virtual_earth, create_entity_real_star,
)
from bsd_scene import (
    BSDScene, SceneType, SceneZone, SceneGenerator,
    SceneCoordinate, SceneAtmosphere, MaterialAllocation,
)
from bsd_timeline import (
    BSDTimeline, ClockState, LifecyclePhase, LifecycleState,
    TimelineEvent, create_quick_lifecycle,
)
from bsd_rule_engine import (
    BSDRuleEngine, RulePriority, RuleStatus, InteractionType,
    BSDRule, RuleCondition, RuleAction,
)


class UniverseState(str, Enum):
    """宇宙状态"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    EVOLVING = "evolving"
    ZEROING = "zeroing"
    PERPETUAL = "perpetual"


class SAGAPhase(str, Enum):
    """SAGA工作流阶段"""
    SENSE = "sense"          # 感知·扫描实体/场景状态
    ANALYZE = "analyze"      # 分析·评估规则触发条件
    GENERATE = "generate"    # 生成·执行规则动作
    ACT = "act"              # 行动·更新宇宙状态


@dataclass
class UniverseConfig:
    """宇宙配置"""
    max_entities: int = 1000
    max_scenes: int = 100
    tick_interval: float = 1.0
    clockwise_speed: float = 1.0
    counterclockwise_speed: float = 1.0
    auto_evolution: bool = True
    enable_triad_resonance: bool = True
    enable_material_subset: bool = True


@dataclass
class SAGACycleResult:
    """SAGA循环结果"""
    cycle_id: int
    phase: SAGAPhase
    entities_processed: int
    scenes_processed: int
    rules_triggered: int
    interactions: List[Dict] = field(default_factory=list)
    state_changes: List[Dict] = field(default_factory=list)


class BSDUniverseEngine:
    """BSD虚拟宇宙引擎·整合四向展开
    
    [归属基底：球体坐标系+三球对偶+双时针+规则公理]
    [对应公理：六系立系公理·互相内含公理·进化协议公理·天道秩序]
    
    整合：
    1. EntityRegistry（实体化）
    2. SceneGenerator（场景化）
    3. BSDTimeline（时间化）
    4. BSDRuleEngine（规则化）
    形成完整的可运行虚拟宇宙。
    """

    def __init__(self, config: Optional[UniverseConfig] = None):
        self.config = config or UniverseConfig()
        
        # 四向展开·四个核心管理器
        self.entity_registry = EntityRegistry()
        self.scene_generator = SceneGenerator()
        self.timeline = BSDTimeline()
        self.rule_engine = BSDRuleEngine()
        
        # 宇宙状态
        self.universe_state: UniverseState = UniverseState.INITIALIZING
        self.saga_cycle_count: int = 0
        self._current_saga_phase: SAGAPhase = SAGAPhase.SENSE
        self._saga_results: List[SAGACycleResult] = []
        
        # 运行历史
        self._universe_history: List[Dict] = []
        
        # 初始化日志
        self._log_universe_event("init", "BSD虚拟宇宙引擎初始化完成")

    # ============================================================
    # 宇宙初始化·创建标准三球对偶+核心场景
    # ============================================================
    def initialize_standard_universe(self):
        """初始化标准宇宙·三球对偶+六系场景"""
        self.universe_state = UniverseState.INITIALIZING
        
        # 1. 创建三球对偶实体
        moon = create_entity_moon("ent_moon", "BSD月亮")
        earth = create_entity_virtual_earth("ent_earth", "虚拟宇宙地球")
        star = create_entity_real_star("ent_star", "现实恒星")
        
        self.entity_registry.register(moon)
        self.entity_registry.register(earth)
        self.entity_registry.register(star)
        
        # 2. 创建三体共振组
        triad_id = self.entity_registry.create_triad_resonance(
            "ent_moon", "ent_earth", "ent_star"
        )
        
        # 3. 创建六系场景（覆盖五个区域）
        # 本源区
        self.scene_generator.create_scene(
            "scene_origin", "本源广场", SceneType.MIXED, SceneZone.ORIGIN,
            description="0元空无·宇宙起源"
        )
        
        # 潜力区
        self.scene_generator.create_scene(
            "scene_agriculture", "农业潜力场", SceneType.QIANGHUA_AGRICULTURE, SceneZone.POTENTIAL,
            description="强化系·农业潜力·W1层"
        )
        
        # 拓扑区
        self.scene_generator.create_scene(
            "scene_chemistry", "化学拓扑场", SceneType.BIANSHEN_CHEMISTRY, SceneZone.TOPOLOGY,
            description="变身系·化学反应·球心W2层"
        )
        
        # 显化区
        self.scene_generator.create_scene(
            "scene_industry", "工业显化场", SceneType.JUXIAN_INDUSTRY, SceneZone.MANIFEST,
            description="具现系·工业显化·W3层"
        )
        self.scene_generator.create_scene(
            "scene_biology", "生物显化场", SceneType.ZIRAN_BIOLOGY, SceneZone.MANIFEST,
            description="自然系·生物显化·W3层"
        )
        self.scene_generator.create_scene(
            "scene_economy", "经济显化场", SceneType.SHEHUI_ECONOMY, SceneZone.MANIFEST,
            description="社会系·经济显化·W3层"
        )
        
        # 永续区
        self.scene_generator.create_scene(
            "scene_politics", "政治永续场", SceneType.TIANDAO_POLITICS, SceneZone.PERPETUAL,
            description="天道系·政治秩序·永续层"
        )
        
        # 4. 将实体分配到场景
        self.scene_generator.get_scene("scene_origin").add_entity("ent_moon")
        self.scene_generator.get_scene("scene_industry").add_entity("ent_earth")
        self.scene_generator.get_scene("scene_politics").add_entity("ent_star")
        
        # 5. 注册实体生命周期
        self.timeline.register_entity_lifecycle(
            "ent_moon", 
            emergence_duration=3.0, growth_duration=10.0,
            stability_duration=20.0, decay_duration=5.0,
            zeroing_duration=3.0, max_cycles=5,
        )
        self.timeline.register_entity_lifecycle(
            "ent_earth",
            emergence_duration=5.0, growth_duration=20.0,
            stability_duration=40.0, decay_duration=10.0,
            zeroing_duration=5.0, max_cycles=3,
        )
        self.timeline.register_entity_lifecycle(
            "ent_star",
            emergence_duration=10.0, growth_duration=50.0,
            stability_duration=100.0, decay_duration=20.0,
            zeroing_duration=10.0, max_cycles=999,
        )
        
        # 6. 启动双时针（耦合模式）
        self.timeline.start_clock(ClockState.COUPLED)
        self.timeline.set_speed(self.config.clockwise_speed, self.config.counterclockwise_speed)
        
        self.universe_state = UniverseState.RUNNING
        self._log_universe_event("initialize", f"标准宇宙初始化完成·三球对偶={triad_id}·{len(self.scene_generator.list_scenes())}个场景")

    # ============================================================
    # SAGA工作流·单循环执行
    # ============================================================
    def run_saga_cycle(self, delta_time: float = 1.0) -> SAGACycleResult:
        """执行一个完整的SAGA循环"""
        self.saga_cycle_count += 1
        result = SAGACycleResult(
            cycle_id=self.saga_cycle_count,
            phase=self._current_saga_phase,
            entities_processed=0,
            scenes_processed=0,
            rules_triggered=0,
        )
        
        # Phase 1: SENSE（感知）·扫描状态
        self._current_saga_phase = SAGAPhase.SENSE
        entity_count = len(self.entity_registry.list_entities())
        scene_count = len(self.scene_generator.list_scenes())
        result.entities_processed = entity_count
        result.scenes_processed = scene_count
        
        # Phase 2: ANALYZE（分析）·评估规则
        self._current_saga_phase = SAGAPhase.ANALYZE
        
        # 分析每个场景的规则触发条件
        for scene in self.scene_generator.list_scenes():
            entities_in_scene = len(scene.entity_ids)
            # 收集该场景实体的六系
            scene_systems = set()
            for eid in scene.entity_ids:
                entity = self.entity_registry.get(eid)
                if entity:
                    ws = entity.six_system.as_vector()
                    sys_names = ["qianghua", "ziran", "juxian", "bianshen", "shehui", "tiandao"]
                    for i, w in enumerate(ws):
                        if w > 0.1:
                            scene_systems.add(sys_names[i])
            
            # 创建规则上下文并评估
            context = self.rule_engine.create_context(
                scene_zone=scene.zone.value,
                entity_count=entities_in_scene,
                systems=list(scene_systems),
            )
            triggered = self.rule_engine.evaluate_and_execute(context)
            result.interactions.extend(triggered)
        
        result.rules_triggered = len(result.interactions)
        
        # Phase 3: GENERATE（生成）·时间推进
        self._current_saga_phase = SAGAPhase.GENERATE
        self.timeline.tick(delta_time)
        
        # 收集状态变化
        for eid, state in self.timeline.get_all_states().items():
            result.state_changes.append({
                "entity_id": eid,
                "new_phase": state.phase.value,
                "cycle_count": state.cycle_count,
            })
        
        # Phase 4: ACT（行动）·更新宇宙
        self._current_saga_phase = SAGAPhase.ACT
        
        # 更新实体密度/复杂度/生命度
        for entity in self.entity_registry.list_entities():
            entity.compute_density()
            entity.compute_complexity()
            entity.compute_life_indicator()
        
        # 检查是否进入归零/永生状态
        all_cycles = [s.cycle_count for s in self.timeline.get_all_states().values()]
        if all(c >= 3 for c in all_cycles) and all_cycles:
            self.universe_state = UniverseState.PERPETUAL
        elif any(s.phase.value == "zeroing" for s in self.timeline.get_all_states().values()):
            self.universe_state = UniverseState.ZEROING
        
        # 保存结果
        self._saga_results.append(result)
        
        self._log_universe_event(
            "saga_cycle",
            f"SAGA#{result.cycle_id}完成·规则触发={result.rules_triggered}·宇宙状态={self.universe_state.value}"
        )
        
        return result

    # ============================================================
    # 批量运行·模拟宇宙演化
    # ============================================================
    def simulate_universe(self, total_cycles: int, delta_time: float = 1.0) -> Dict:
        """模拟宇宙演化·运行N个SAGA循环"""
        self.universe_state = UniverseState.EVOLVING
        
        # 记录初始状态
        initial_entities = len(self.entity_registry.list_entities())
        initial_scenes = len(self.scene_generator.list_scenes())
        
        # 运行循环
        for _ in range(total_cycles):
            self.run_saga_cycle(delta_time)
        
        # 汇总结果
        final_entities = len(self.entity_registry.list_entities())
        final_scenes = len(self.scene_generator.list_scenes())
        
        # 统计实体生命周期完成情况
        completed_cycles = {}
        for eid, state in self.timeline.get_all_states().items():
            completed_cycles[eid] = state.cycle_count
        
        # 统计规则触发
        total_rule_triggers = sum(
            r.trigger_count for r in self.rule_engine.list_rules()
        )
        
        summary = {
            "total_cycles_run": total_cycles,
            "initial_entities": initial_entities,
            "final_entities": final_entities,
            "initial_scenes": initial_scenes,
            "final_scenes": final_scenes,
            "final_universe_state": self.universe_state.value,
            "entity_cycles_completed": completed_cycles,
            "total_rule_triggers": total_rule_triggers,
            "saga_cycles_executed": len(self._saga_results),
            "interactions_count": sum(
                len(r.interactions) for r in self._saga_results
            ),
        }
        
        self.universe_state = UniverseState.RUNNING
        self._log_universe_event(
            "simulate",
            f"宇宙模拟完成·{total_cycles}循环·规则触发{total_rule_triggers}次·最终状态={self.universe_state.value}"
        )
        
        return summary

    # ============================================================
    # 实体操作接口
    # ============================================================
    def add_entity_to_scene(self, entity_id: str, scene_id: str) -> bool:
        """将实体添加到场景"""
        return self.scene_generator.move_entity_to_scene(entity_id, scene_id)

    def create_custom_entity(
        self,
        entity_id: str,
        name: str,
        entity_type: EntityType,
        latitude: float = 0.0,
        longitude: float = 0.0,
        z_anchor_id: str = "V01",
        **kwargs,
    ) -> BSDEntity:
        """创建自定义实体"""
        entity = BSDEntity(
            entity_id=entity_id,
            name=name,
            entity_type=entity_type,
            sphere_pos=SphereCoordinate(
                latitude=latitude,
                longitude=longitude,
                z_anchor_id=z_anchor_id,
            ),
            **kwargs,
        )
        self.entity_registry.register(entity)
        self.timeline.register_entity_lifecycle(entity_id)
        self._log_universe_event("create_entity", f"实体{entity_id}创建完成")
        return entity

    # ============================================================
    # 宇宙报告生成
    # ============================================================
    def generate_full_report(self) -> str:
        """生成完整的宇宙状态报告"""
        lines = []
        lines.append("=" * 80)
        lines.append("BSD虚拟宇宙引擎·完整状态报告")
        lines.append("=" * 80)
        
        # 宇宙状态
        lines.append(f"\n【宇宙状态】{self.universe_state.value}")
        lines.append(f"SAGA循环计数：{self.saga_cycle_count}")
        lines.append(f"双时针：{self.timeline.clock_state.value} | "
                     f"顺时针={self.timeline.clockwise_speed}x | "
                     f"逆时针={self.timeline.counterclockwise_speed}x")
        
        # 实体统计
        entity_report = self.entity_registry.generate_entity_report()
        lines.append(f"\n【实体层·实体化维度】")
        lines.append(entity_report)
        
        # 场景统计
        scene_report = self.scene_generator.generate_scene_report()
        lines.append(f"\n【场景层·场景化维度】")
        lines.append(scene_report)
        
        # 时间线统计
        timeline_report = self.timeline.generate_timeline_report()
        lines.append(f"\n【时间层·时间化维度】")
        lines.append(timeline_report)
        
        # 规则统计
        rule_report = self.rule_engine.generate_rule_report()
        lines.append(f"\n【规则层·规则化维度】")
        lines.append(rule_report)
        
        # 四向展开完整性评估
        lines.append(f"\n{'='*80}")
        lines.append("【四向展开完整性评估】")
        lines.append(f"{'='*80}")
        
        entity_count = len(self.entity_registry.list_entities())
        scene_count = len(self.scene_generator.list_scenes())
        lifecycle_count = len(self.timeline.get_all_states())
        rule_count = len(self.rule_engine.list_rules())
        
        lines.append(f"\n  ① 实体化：{entity_count}个实体注册 {'✅' if entity_count > 0 else '❌'}")
        lines.append(f"  ② 场景化：{scene_count}个场景生成 {'✅' if scene_count > 0 else '❌'}")
        lines.append(f"  ③ 时间化：{lifecycle_count}个生命周期管理 {'✅' if lifecycle_count > 0 else '❌'}")
        lines.append(f"  ④ 规则化：{rule_count}条规则加载 {'✅' if rule_count > 0 else '❌'}")
        
        # 互相内含检查
        triad_count = len(self.entity_registry._triad_groups)
        lines.append(f"\n  互相内含：{triad_count}个三体共振组 {'✅' if triad_count > 0 else '❌'}")
        
        # 素材子集检查
        material_scenes = sum(
            1 for s in self.scene_generator.list_scenes()
            if s.material.primary_platform_id
        )
        lines.append(f"  素材子集：{material_scenes}/{scene_count}个场景配置素材 {'✅' if material_scenes == scene_count else '⚠️'}")
        
        # 宇宙完备性
        all_complete = entity_count > 0 and scene_count > 0 and lifecycle_count > 0 and rule_count > 0
        lines.append(f"\n  【宇宙完备性】{'✅ 四向展开完整' if all_complete else '❌ 缺失维度'}")
        
        # 交互历史
        total_interactions = sum(
            len(r.interactions) for r in self._saga_results
        )
        lines.append(f"\n【交互历史】总交互次数={total_interactions}")
        lines.append(f"【SAGA循环】已执行{len(self._saga_results)}个循环")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    # ============================================================
    # 日志
    # ============================================================
    def _log_universe_event(self, event_type: str, description: str):
        self._universe_history.append({
            "event_type": event_type,
            "description": description,
            "state": self.universe_state.value,
        })

    def get_universe_history(self, limit: int = 50) -> List[Dict]:
        return self._universe_history[-limit:]


# 模块公开API
__all__ = [
    "UniverseState", "SAGAPhase",
    "UniverseConfig", "SAGACycleResult",
    "BSDUniverseEngine",
]
