"""
BSD虚拟宇宙引擎→Updream智能体对接适配器
[归属基底：四向展开法+SAGA工作流+进化协议+素材子集定理五十四]
[对应公理：场景即实体公理·互相内含公理·素材子集定理]
[V1.0·2026-08-01·工程对接·BSD引擎输出→Updream创作输入]

核心：将BSD虚拟宇宙引擎的SAGA循环输出，映射为Updream智能体的创作工作流。
对接机制：
- 实体化→角色/道具对象池
- 场景化→场景/环境配置
- 时间化→剧情时间线/节奏控制
- 规则化→创作规则/约束条件
- 素材子集→素材调用路由
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import json

from bsd_universe_engine import BSDUniverseEngine, SAGACycleResult, SAGAPhase
from bsd_entity import BSDEntity, EntityType, EntitySixSystemWeight
from bsd_scene import BSDScene, SceneType, SceneZone
from bsd_rule_engine import BSDRuleEngine


class UpdreamTaskType(str, Enum):
    """Updream创作任务类型"""
    CHARACTER_DESIGN = "character_design"           # 角色设计
    SCENE_DESIGN = "scene_design"                   # 场景设计
    PROP_DESIGN = "prop_design"                     # 道具设计
    STORYBOARD = "storyboard"                       # 分镜
    ANIMATION = "animation"                         # 动画
    DIALOGUE = "dialogue"                           # 对话
    SOUND_DESIGN = "sound_design"                   # 音效
    COLOR_GRADING = "color_grading"                 # 调色
    POST_PRODUCTION = "post_production"             # 后期


class UpdreamSystemMapping(str, Enum):
    """六系→Updream创作域映射"""
    QIANGHUA_CHARACTER = "character"     # 强化系→角色塑造
    ZIRAN_ENVIRONMENT = "environment"   # 自然系→环境氛围
    JUXIAN_PROP = "prop"                # 具现系→道具造物
    BIANSHEN_TRANSFORM = "transform"    # 变身系→形态变化
    SHEHUI_SOCIAL = "social"            # 社会系→社交互动
    TIANDO_AESTHETIC = "aesthetic"      # 天道系→美学风格


@dataclass
class UpdreamTask:
    """Updream创作任务"""
    task_id: str
    task_type: UpdreamTaskType
    title: str
    description: str
    priority: int = 5  # 1-10
    estimated_duration: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    bsd_entity_ids: List[str] = field(default_factory=list)
    bsd_scene_ids: List[str] = field(default_factory=list)
    bsd_rule_ids: List[str] = field(default_factory=list)
    material_platform_id: str = ""
    material_capabilities: List[str] = field(default_factory=list)
    status: str = "pending"
    output_url: str = ""


@dataclass
class UpdreamWorkflow:
    """Updream工作流配置"""
    workflow_id: str
    name: str
    description: str
    tasks: List[UpdreamTask] = field(default_factory=list)
    current_phase: str = "sensing"
    progress: float = 0.0
    created_at: str = ""
    updated_at: str = ""


class BSDUpdreamBridge:
    """BSD引擎→Updream智能体对接桥
    
    [归属基底：四向展开法+SAGA工作流+进化协议]
    [对应公理：场景即实体公理·互相内含公理·素材子集定理五十四]
    
    核心映射：
    BSD四向展开 → Updream创作维度
    ├── 实体化 → 角色/道具对象池
    ├── 场景化 → 场景/环境配置  
    ├── 时间化 → 剧情时间线/节奏控制
    └── 规则化 → 创作规则/约束条件
    
    SAGA循环 → Updream工作流阶段
    ├── SENSE（感知）→ 需求分析/素材收集
    ├── ANALYZE（分析）→ 创意构思/结构规划
    ├── GENERATE（生成）→ 内容创作/产品产出
    └── ACT（行动）→ 部署发布/迭代优化
    """

    # 六系→Updream创作域映射表
    SYSTEM_TO_DOMAIN = {
        "qianghua": UpdreamSystemMapping.QIANGHUA_CHARACTER,
        "ziran": UpdreamSystemMapping.ZIRAN_ENVIRONMENT,
        "juxian": UpdreamSystemMapping.JUXIAN_PROP,
        "bianshen": UpdreamSystemMapping.BIANSHEN_TRANSFORM,
        "shehui": UpdreamSystemMapping.SHEHUI_SOCIAL,
        "tiandao": UpdreamSystemMapping.TIANDO_AESTHETIC,
    }

    # 实体类型→Updream任务类型映射
    ENTITY_TYPE_TO_TASK = {
        EntityType.ABSTRACT: [UpdreamTaskType.STORYBOARD, UpdreamTaskType.DIALOGUE],
        EntityType.MATERIAL: [UpdreamTaskType.PROP_DESIGN, UpdreamTaskType.ANIMATION],
        EntityType.SOCIAL: [UpdreamTaskType.DIALOGUE, UpdreamTaskType.SOUND_DESIGN],
        EntityType.NATURAL: [UpdreamTaskType.SCENE_DESIGN, UpdreamTaskType.COLOR_GRADING],
        EntityType.EVOLUTIONARY: [UpdreamTaskType.POST_PRODUCTION, UpdreamTaskType.ANIMATION],
        EntityType.BSD_MOON: [UpdreamTaskType.STORYBOARD],
        EntityType.VIRTUAL_EARTH: [UpdreamTaskType.SCENE_DESIGN, UpdreamTaskType.CHARACTER_DESIGN],
        EntityType.REAL_STAR: [UpdreamTaskType.POST_PRODUCTION],
    }

    # 场景类型→Updream任务类型映射
    SCENE_TYPE_TO_TASK = {
        SceneType.QIANGHUA_AGRICULTURE: [UpdreamTaskType.SCENE_DESIGN, UpdreamTaskType.COLOR_GRADING],
        SceneType.ZIRAN_BIOLOGY: [UpdreamTaskType.SCENE_DESIGN, UpdreamTaskType.ANIMATION],
        SceneType.JUXIAN_INDUSTRY: [UpdreamTaskType.PROP_DESIGN, UpdreamTaskType.ANIMATION],
        SceneType.BIANSHEN_CHEMISTRY: [UpdreamTaskType.ANIMATION, UpdreamTaskType.POST_PRODUCTION],
        SceneType.SHEHUI_ECONOMY: [UpdreamTaskType.DIALOGUE, UpdreamTaskType.SOUND_DESIGN],
        SceneType.TIANDAO_POLITICS: [UpdreamTaskType.STORYBOARD, UpdreamTaskType.COLOR_GRADING],
        SceneType.MIXED: [UpdreamTaskType.SCENE_DESIGN, UpdreamTaskType.CHARACTER_DESIGN, UpdreamTaskType.POST_PRODUCTION],
    }

    def __init__(self, engine: BSDUniverseEngine):
        self.engine = engine
        self._workflows: Dict[str, UpdreamWorkflow] = {}
        self._task_counter = 0
        self._bridge_log: List[Dict] = []
        self._on_task_created: Optional[Callable[[UpdreamTask], None]] = None
        self._on_workflow_completed: Optional[Callable[[UpdreamWorkflow], None]] = None

    def create_workflow_from_saga(
        self,
        workflow_name: str,
        cycles_to_analyze: int = 10,
    ) -> UpdreamWorkflow:
        """从SAGA循环结果创建Updream工作流
        
        Args:
            workflow_name: 工作流名称
            cycles_to_analyze: 分析多少个SAGA循环的历史数据
        """
        self._task_counter += 1
        workflow_id = f"wf_{self._task_counter:03d}"
        
        # 获取引擎当前状态
        entities = self.engine.entity_registry.list_entities()
        scenes = self.engine.scene_generator.list_scenes()
        rules = self.engine.rule_engine.list_rules()
        history = self.engine.get_universe_history(limit=cycles_to_analyze)
        
        # 分析SAGA历史，收集状态变化和规则触发
        triggered_rules = set()
        state_changes: List[Dict] = []
        for event in history:
            if event.get("event_type") == "rule_triggered":
                triggered_rules.add(event.get("rule_id", ""))
            elif event.get("event_type") == "phase_transition":
                state_changes.append(event)
        
        # 基于实体和场景创建创作任务
        tasks = self._generate_tasks_from_universe(entities, scenes, rules, triggered_rules)
        
        # 创建工作流
        workflow = UpdreamWorkflow(
            workflow_id=workflow_id,
            name=workflow_name,
            description=f"基于BSD宇宙状态的创作工作流·{len(entities)}实体·{len(scenes)}场景·{len(rules)}规则",
            tasks=tasks,
            current_phase="sensing",
            progress=0.0,
        )
        
        self._workflows[workflow_id] = workflow
        
        # 记录对接日志
        self._bridge_log.append({
            "action": "create_workflow",
            "workflow_id": workflow_id,
            "entity_count": len(entities),
            "scene_count": len(scenes),
            "rule_count": len(rules),
            "triggered_rules": len(triggered_rules),
            "task_count": len(tasks),
        })
        
        # 触发回调
        for task in tasks:
            if self._on_task_created:
                self._on_task_created(task)
        
        return workflow

    def _generate_tasks_from_universe(
        self,
        entities: List[BSDEntity],
        scenes: List[BSDScene],
        rules: List,
        triggered_rules: set,
    ) -> List[UpdreamTask]:
        """从宇宙状态生成创作任务列表"""
        tasks: List[UpdreamTask] = []
        task_counter = 0
        
        # 1. 基于实体创建任务
        for entity in entities:
            task_types = self.ENTITY_TYPE_TO_TASK.get(entity.entity_type, [])
            dominant_system, _ = entity.six_system.dominant_system()
            
            for task_type in task_types[:2]:  # 每个实体最多2个任务
                task_counter += 1
                task_id = f"task_{task_counter:04d}"
                
                task = UpdreamTask(
                    task_id=task_id,
                    task_type=task_type,
                    title=f"{entity.name}·{task_type.value}",
                    description=self._generate_task_description(entity, task_type, dominant_system),
                    priority=self._calculate_priority(entity, task_type),
                    estimated_duration=self._estimate_duration(entity, task_type),
                    bsd_entity_ids=[entity.entity_id],
                    material_platform_id=self._select_material_platform(entity, task_type),
                )
                tasks.append(task)
        
        # 2. 基于场景创建任务
        for scene in scenes:
            task_types = self.SCENE_TYPE_TO_TASK.get(scene.scene_type, [])
            
            for task_type in task_types[:2]:
                task_counter += 1
                task_id = f"task_{task_counter:04d}"
                
                # 找到该场景的实体
                scene_entity_ids = list(scene.entity_ids)
                
                task = UpdreamTask(
                    task_id=task_id,
                    task_type=task_type,
                    title=f"{scene.name}·{task_type.value}",
                    description=self._generate_scene_task_description(scene, task_type),
                    priority=min(10, 5 + len(scene_entity_ids)),
                    estimated_duration=10.0 + len(scene_entity_ids) * 2.0,
                    bsd_scene_ids=[scene.scene_id],
                    bsd_entity_ids=scene_entity_ids[:5],  # 最多关联5个实体
                    material_platform_id=scene.material.primary_platform_id,
                    material_capabilities=scene.material.material_capabilities[:4],
                )
                tasks.append(task)
        
        # 3. 基于触发规则创建任务
        for rule in rules:
            if rule.rule_id in triggered_rules:
                task_counter += 1
                task_id = f"task_{task_counter:04d}"
                
                task = UpdreamTask(
                    task_id=task_id,
                    task_type=UpdreamTaskType.STORYBOARD,
                    title=f"规则触发·{rule.name}",
                    description=f"基于规则「{rule.name}」的创作任务·{rule.description}",
                    priority=min(10, rule.trigger_count // 10 + 3),
                    estimated_duration=5.0 + rule.trigger_count * 0.5,
                    bsd_rule_ids=[rule.rule_id],
                    status="ready",
                )
                tasks.append(task)
        
        return tasks

    def _generate_task_description(
        self,
        entity: BSDEntity,
        task_type: UpdreamTaskType,
        dominant_system: str,
    ) -> str:
        """生成任务描述"""
        domain = self.SYSTEM_TO_DOMAIN.get(dominant_system, "general")
        phase_map = {
            "potential": "概念设计阶段",
            "growth": "原型开发阶段",
            "stability": "生产制作阶段",
            "manifested": "定稿呈现阶段",
            "decay": "迭代优化阶段",
            "zeroing": "归档重构阶段",
        }
        phase_desc = phase_map.get(entity.phase.value, "当前阶段")
        
        return (
            f"基于BSD虚拟宇宙实体「{entity.name}」的{task_type.value}任务。"
            f"实体类型：{entity.entity_type.value}。"
            f"主导创作域：{domain}。"
            f"当前状态：{phase_desc}。"
            f"六系权重：强化={entity.six_system.qianghua:.2f}/自然={entity.six_system.ziran:.2f}/"
            f"具现={entity.six_system.juxian:.2f}/变身={entity.six_system.bianshen:.2f}/"
            f"社会={entity.six_system.shehui:.2f}/天道={entity.six_system.tiandao:.2f}。"
            f"建议创作方向：根据主导系「{dominant_system}」进行{domain}领域的{task_type.value}创作。"
        )

    def _generate_scene_task_description(
        self,
        scene: BSDScene,
        task_type: UpdreamTaskType,
    ) -> str:
        """生成场景任务描述"""
        dominant_atm, atm_value = scene.atmosphere.dominant_atmosphere()
        return (
            f"基于BSD虚拟宇宙场景「{scene.name}」的{task_type.value}任务。"
            f"场景类型：{scene.scene_type.value}·{scene.zone.value}区。"
            f"实体数量：{scene.entity_count()}。"
            f"激活度：{scene.activation_level:.1%}。"
            f"主导氛围：{dominant_atm}（强度={atm_value:.2f}）。"
            f"素材配置：主平台={scene.material.primary_platform_id}·辅助={scene.material.secondary_platform_ids[:3]}。"
            f"建议利用场景中的六系混合氛围进行{task_type.value}创作。"
        )

    def _calculate_priority(
        self,
        entity: BSDEntity,
        task_type: UpdreamTaskType,
    ) -> int:
        """计算任务优先级（1-10）"""
        priority = 5
        
        # 实体生命周期阶段影响优先级
        phase_boost = {
            "potential": 2,   # 潜力阶段需要更多关注
            "growth": 3,      # 成长阶段优先级最高
            "stability": 1,   # 稳定阶段常规优先级
            "manifested": 0,  # 显现阶段最低
        }
        priority += phase_boost.get(entity.phase.value, 0)
        
        # 主导系影响
        dominant_sys, weight = entity.six_system.dominant_system()
        if dominant_sys == "tiandao":  # 天道系优先级更高
            priority += 2
        elif dominant_sys == "qianghua":  # 强化系中等
            priority += 1
        
        return min(10, priority)

    def _estimate_duration(
        self,
        entity: BSDEntity,
        task_type: UpdreamTaskType,
    ) -> float:
        """估算任务持续时间（小时）"""
        base_duration = {
            UpdreamTaskType.CHARACTER_DESIGN: 8.0,
            UpdreamTaskType.SCENE_DESIGN: 6.0,
            UpdreamTaskType.PROP_DESIGN: 4.0,
            UpdreamTaskType.STORYBOARD: 12.0,
            UpdreamTaskType.ANIMATION: 16.0,
            UpdreamTaskType.DIALOGUE: 3.0,
            UpdreamTaskType.SOUND_DESIGN: 5.0,
            UpdreamTaskType.COLOR_GRADING: 4.0,
            UpdreamTaskType.POST_PRODUCTION: 20.0,
        }
        return base_duration.get(task_type, 8.0)

    def _select_material_platform(
        self,
        entity: BSDEntity,
        task_type: UpdreamTaskType,
    ) -> str:
        """根据实体属性推荐素材平台"""
        # 默认优先使用updream
        return "updream"

    def advance_workflow_phase(self, workflow_id: str) -> Optional[UpdreamWorkflow]:
        """推进工作流阶段（对应SAGA循环推进）"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return None
        
        phases = ["sensing", "analyzing", "generating", "acting", "completed"]
        current_idx = phases.index(workflow.current_phase)
        
        if current_idx < len(phases) - 1:
            workflow.current_phase = phases[current_idx + 1]
            workflow.progress = (current_idx + 1) / len(phases) * 100
            
            # 阶段完成时的回调
            if workflow.current_phase == "completed" and self._on_workflow_completed:
                self._on_workflow_completed(workflow)
        
        return workflow

    def get_workflow(self, workflow_id: str) -> Optional[UpdreamWorkflow]:
        """获取工作流"""
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> List[UpdreamWorkflow]:
        """列出所有工作流"""
        return list(self._workflows.values())

    def get_bridge_report(self) -> str:
        """生成对接桥报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("BSD虚拟宇宙引擎→Updream智能体对接桥·状态报告")
        lines.append("=" * 70)
        
        lines.append(f"\n【对接工作流】{len(self._workflows)}个")
        for wf in self._workflows.values():
            completed = len([t for t in wf.tasks if t.status == "completed"])
            lines.append(f"  {wf.workflow_id}·{wf.name}")
            lines.append(f"    阶段={wf.current_phase}·进度={wf.progress:.0f}%")
            lines.append(f"    任务={len(wf.tasks)}个·已完成={completed}个")
            lines.append(f"    描述={wf.description}")
        
        lines.append(f"\n【对接日志】最近{min(len(self._bridge_log), 10)}条")
        for log in self._bridge_log[-10:]:
            lines.append(f"  [{log['action']}] {log.get('workflow_id', '')}·"
                        f"实体={log.get('entity_count', 0)}·"
                        f"场景={log.get('scene_count', 0)}·"
                        f"规则={log.get('rule_count', 0)}·"
                        f"任务={log.get('task_count', 0)}")
        
        lines.append(f"\n【引擎状态】")
        lines.append(f"  SAGA循环：{self.engine.saga_cycle_count}次")
        lines.append(f"  宇宙状态：{self.engine._current_saga_phase.value}")
        lines.append(f"  实体数：{len(self.engine.entity_registry.list_entities())}个")
        lines.append(f"  场景数：{len(self.engine.scene_generator.list_scenes())}个")
        lines.append(f"  规则数：{len(self.engine.rule_engine.list_rules())}条")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)

    def set_callbacks(
        self,
        on_task_created: Optional[Callable[[UpdreamTask], None]] = None,
        on_workflow_completed: Optional[Callable[[UpdreamWorkflow], None]] = None,
    ):
        """设置回调函数"""
        self._on_task_created = on_task_created
        self._on_workflow_completed = on_workflow_completed


def create_updream_workflow_from_engine(
    engine: BSDUniverseEngine,
    workflow_name: str,
    cycles_to_analyze: int = 10,
) -> Tuple[BSDUpdreamBridge, UpdreamWorkflow]:
    """便捷函数：从引擎创建对接桥和工作流"""
    bridge = BSDUpdreamBridge(engine)
    workflow = bridge.create_workflow_from_saga(
        workflow_name=workflow_name,
        cycles_to_analyze=cycles_to_analyze,
    )
    return bridge, workflow


# 模块公开API
__all__ = [
    "UpdreamTaskType", "UpdreamSystemMapping",
    "UpdreamTask", "UpdreamWorkflow",
    "BSDUpdreamBridge", "create_updream_workflow_from_engine",
]
