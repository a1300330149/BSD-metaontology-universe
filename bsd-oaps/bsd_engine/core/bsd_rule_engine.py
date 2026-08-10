"""
BSD虚拟宇宙规则化模块
[归属基底：L0总本源层·六系核心公理·互相内含公理·进化协议公理]
[对应公理：互相内含公理·宇宙协议化公理·永恒进化协议·天道秩序]
[V1.0·2026-08-01·四向展开法·规则化维度]

核心：将公理转化为可执行的交互规则。
规则引擎：定义实体间的交互规则、进化协议、秩序执行。
所有规则遵循：天道秩序 > 人道秩序 > 自然秩序。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Set
from enum import Enum


class RulePriority(str, Enum):
    """规则优先级·天道秩序>人道秩序>自然秩序"""
    TIAND_ORDER = "tiand_order"          # 天道秩序·最高优先级
    HUMAN_ORDER = "human_order"          # 人道秩序·次高优先级
    NATURAL_ORDER = "natural_order"      # 自然秩序·基础优先级


class RuleStatus(str, Enum):
    """规则状态"""
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"


class InteractionType(str, Enum):
    """实体交互类型"""
    MERGE = "merge"                      # 融合·互相内含
    RESONANCE = "resonance"              # 共振·三体对偶
    EVOLUTION = "evolution"              # 进化·协议执行
    MIGRATION = "migration"              # 迁移·场域转换
    CONFLICT = "conflict"                # 冲突·六系对抗
    COOPERATION = "cooperation"          # 协作·六系互补


@dataclass
class RuleCondition:
    """规则触发条件"""
    entity_type_filter: Optional[str] = None
    scene_zone_filter: Optional[str] = None
    min_entity_count: int = 0
    max_entity_count: int = 999
    required_systems: List[str] = field(default_factory=list)
    exclude_systems: List[str] = field(default_factory=list)
    custom_check: Optional[Callable] = None

    def evaluate(self, context: Dict) -> bool:
        if self.entity_type_filter:
            entity_type = context.get("entity_type", "")
            if entity_type != self.entity_type_filter:
                return False
        
        if self.scene_zone_filter:
            zone = context.get("scene_zone", "")
            if zone != self.scene_zone_filter:
                return False
        
        entity_count = context.get("entity_count", 0)
        if entity_count < self.min_entity_count or entity_count > self.max_entity_count:
            return False
        
        systems = set(context.get("systems", []))
        if self.required_systems:
            req_set = set(self.required_systems)
            if not req_set.issubset(systems):
                return False
        if self.exclude_systems:
            exc_set = set(self.exclude_systems)
            if exc_set.intersection(systems):
                return False
        
        if self.custom_check:
            return self.custom_check(context)
        
        return True


@dataclass
class RuleAction:
    """规则执行动作"""
    interaction_type: InteractionType
    target_entity_ids: List[str] = field(default_factory=list)
    target_scene_ids: List[str] = field(default_factory=list)
    parameters: Dict = field(default_factory=dict)
    description: str = ""

    def execute(self, context: Dict) -> Dict:
        """执行动作·返回执行结果"""
        return {
            "action": self.interaction_type.value,
            "targets": len(self.target_entity_ids),
            "scenes": len(self.target_scene_ids),
            "parameters": self.parameters,
            "description": self.description,
            "success": True,
        }


@dataclass
class BSDRule:
    """BSD规则·核心类"""
    rule_id: str
    name: str
    description: str
    
    # 公理归属
    underlying_axiom: str = ""
    
    # 优先级
    priority: RulePriority = RulePriority.NATURAL_ORDER
    
    # 条件与动作
    condition: RuleCondition = field(default_factory=RuleCondition)
    action: RuleAction = field(default_factory=RuleAction)
    
    # 状态
    status: RuleStatus = RuleStatus.ACTIVE
    
    # 触发历史
    trigger_count: int = 0
    last_trigger_time: float = 0.0
    
    # 启用/禁用
    enabled: bool = True

    def can_trigger(self, context: Dict) -> bool:
        if not self.enabled or self.status != RuleStatus.ACTIVE:
            return False
        return self.condition.evaluate(context)

    def trigger(self, context: Dict) -> Dict:
        self.trigger_count += 1
        result = self.action.execute(context)
        result["rule_id"] = self.rule_id
        result["rule_name"] = self.name
        return result


class BSDRuleEngine:
    """BSD虚拟宇宙规则引擎
    
    [归属基底：互相内含公理+进化协议公理+天道秩序]
    [对应公理：宇宙协议化公理·永恒进化协议·天道秩序优先级]
    """

    def __init__(self):
        self._rules: Dict[str, BSDRule] = {}
        self._interaction_history: List[Dict] = []
        self._axiom_registry: Dict[str, List[str]] = {}
        
        # 自动加载内置规则
        self._load_builtin_rules()

    def _load_builtin_rules(self):
        """加载内置规则集·基于核心公理"""
        
        # 规则1：三体共振触发·定理四十二
        self.register_rule(BSDRule(
            rule_id="RULE-001",
            name="三体共振规则",
            description="三个实体在同一场域相遇时触发共振·对应定理四十二·三球对偶",
            underlying_axiom="三球对偶定理·定理四十二",
            priority=RulePriority.HUMAN_ORDER,
            condition=RuleCondition(
                min_entity_count=3,
                max_entity_count=3,
            ),
            action=RuleAction(
                interaction_type=InteractionType.RESONANCE,
                description="触发三体共振·场域能量提升",
                parameters={"resonance_strength": 1.0, "energy_boost": 0.3},
            ),
        ))
        
        # 规则2：六系互补融合·互相内含公理
        self.register_rule(BSDRule(
            rule_id="RULE-002",
            name="六系互补融合规则",
            description="强化系+自然系相遇时产生生命属性融合·互相内含的显化",
            underlying_axiom="互相内含公理",
            priority=RulePriority.NATURAL_ORDER,
            condition=RuleCondition(
                required_systems=["qianghua", "ziran"],
            ),
            action=RuleAction(
                interaction_type=InteractionType.MERGE,
                description="强化+自然融合→生命属性涌现",
                parameters={"fusion_type": "life_emergence", "stability": 0.7},
            ),
        ))
        
        # 规则3：工业聚集效应·具现系饱和
        self.register_rule(BSDRule(
            rule_id="RULE-003",
            name="工业聚集规则",
            description="具现系实体密度超过阈值时触发工业聚集效应",
            underlying_axiom="系统权重秤定理·定理四十",
            priority=RulePriority.NATURAL_ORDER,
            condition=RuleCondition(
                min_entity_count=5,
                required_systems=["juxian"],
            ),
            action=RuleAction(
                interaction_type=InteractionType.COOPERATION,
                description="工业聚集·规模效应激活",
                parameters={"scale_effect": True, "efficiency_boost": 1.5},
            ),
        ))
        
        # 规则4：天道系秩序强制·政治场域
        self.register_rule(BSDRule(
            rule_id="RULE-004",
            name="天道秩序规则",
            description="天道系实体自动获得最高秩序执行权·天道秩序>人道秩序>自然秩序",
            underlying_axiom="天道秩序优先级公理",
            priority=RulePriority.TIAND_ORDER,
            condition=RuleCondition(
                required_systems=["tiandao"],
            ),
            action=RuleAction(
                interaction_type=InteractionType.EVOLUTION,
                description="天道秩序强制执行·规则优先级提升",
                parameters={"priority_boost": True, "enforcement_level": 3},
            ),
        ))
        
        # 规则5：化学相变触发·变身系
        self.register_rule(BSDRule(
            rule_id="RULE-005",
            name="化学相变规则",
            description="变身系实体与自然系实体相遇时触发化学反应",
            underlying_axiom="六系立系公理·变身系动力性",
            priority=RulePriority.NATURAL_ORDER,
            condition=RuleCondition(
                required_systems=["bianshen", "ziran"],
            ),
            action=RuleAction(
                interaction_type=InteractionType.EVOLUTION,
                description="化学相变·新物质涌现",
                parameters={"phase_change": True, "new_complexity": 0.5},
            ),
        ))
        
        # 规则6：经济循环规则·社会系
        self.register_rule(BSDRule(
            rule_id="RULE-006",
            name="经济循环规则",
            description="社会系实体数量足够时形成经济循环·资源流动",
            underlying_axiom="互相内含公理·社会连接性",
            priority=RulePriority.HUMAN_ORDER,
            condition=RuleCondition(
                min_entity_count=3,
                required_systems=["shehui"],
            ),
            action=RuleAction(
                interaction_type=InteractionType.COOPERATION,
                description="经济循环·资源流动效率提升",
                parameters={"flow_efficiency": 0.8, "cycle_activated": True},
            ),
        ))

    def register_rule(self, rule: BSDRule):
        """注册规则"""
        self._rules[rule.rule_id] = rule
        axiom = rule.underlying_axiom
        if axiom not in self._axiom_registry:
            self._axiom_registry[axiom] = []
        if rule.rule_id not in self._axiom_registry[axiom]:
            self._axiom_registry[axiom].append(rule.rule_id)

    def unregister_rule(self, rule_id: str):
        if rule_id in self._rules:
            del self._rules[rule_id]

    def enable_rule(self, rule_id: str, enabled: bool = True):
        if rule_id in self._rules:
            self._rules[rule_id].enabled = enabled

    def set_rule_status(self, rule_id: str, status: RuleStatus):
        if rule_id in self._rules:
            self._rules[rule_id].status = status

    def evaluate_and_execute(self, context: Dict) -> List[Dict]:
        """评估所有规则并执行符合条件的动作"""
        triggered_results = []
        
        # 按优先级排序规则
        sorted_rules = sorted(
            self._rules.values(),
            key=lambda r: list(RulePriority).index(r.priority),
        )
        
        for rule in sorted_rules:
            if rule.can_trigger(context):
                result = rule.trigger(context)
                triggered_results.append(result)
                self._interaction_history.append(result)
        
        return triggered_results

    def create_context(
        self,
        entity_type: str = "",
        scene_zone: str = "",
        entity_count: int = 0,
        systems: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict:
        """创建规则评估上下文"""
        context = {
            "entity_type": entity_type,
            "scene_zone": scene_zone,
            "entity_count": entity_count,
            "systems": systems or [],
        }
        context.update(kwargs)
        return context

    def get_rule(self, rule_id: str) -> Optional[BSDRule]:
        return self._rules.get(rule_id)

    def list_rules(self, priority: Optional[RulePriority] = None) -> List[BSDRule]:
        rules = list(self._rules.values())
        if priority:
            return [r for r in rules if r.priority == priority]
        return rules

    def get_axiom_rules(self, axiom: str) -> List[BSDRule]:
        rule_ids = self._axiom_registry.get(axiom, [])
        return [self._rules[rid] for rid in rule_ids if rid in self._rules]

    def simulate_interaction(
        self,
        entity_count: int,
        systems: List[str],
        scene_zone: str = "manifest",
    ) -> Dict:
        """模拟一次实体交互评估"""
        context = self.create_context(
            scene_zone=scene_zone,
            entity_count=entity_count,
            systems=systems,
        )
        
        triggered = self.evaluate_and_execute(context)
        
        return {
            "context": context,
            "triggered_rules": len(triggered),
            "results": triggered,
            "total_rules_evaluated": len(self._rules),
        }

    def generate_rule_report(self) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append("BSD虚拟宇宙规则引擎·总览报告")
        lines.append("=" * 70)
        
        lines.append(f"\n规则总数：{len(self._rules)}")
        
        # 按公理分组
        lines.append("\n【公理归属分布】")
        for axiom, rule_ids in self._axiom_registry.items():
            lines.append(f"  {axiom}: {len(rule_ids)}条规则")
        
        # 按优先级统计
        priority_counts: Dict[str, int] = {}
        for r in self._rules.values():
            p = r.priority.value
            priority_counts[p] = priority_counts.get(p, 0) + 1
        lines.append("\n【优先级分布】")
        for p, cnt in sorted(priority_counts.items()):
            lines.append(f"  {p}: {cnt}条规则")
        
        # 触发统计
        total_triggers = sum(r.trigger_count for r in self._rules.values())
        lines.append(f"\n【累计触发次数】{total_triggers}")
        
        # 规则详情
        lines.append("\n【规则详情】")
        for r in self._rules.values():
            lines.append(f"\n  {r.rule_id}·{r.name}")
            lines.append(f"    公理：{r.underlying_axiom}")
            lines.append(f"    优先级：{r.priority.value} | 状态：{r.status.value} | 启用：{r.enabled}")
            lines.append(f"    触发次数：{r.trigger_count}")
            lines.append(f"    说明：{r.description}")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


# 模块公开API
__all__ = [
    "RulePriority", "RuleStatus", "InteractionType",
    "RuleCondition", "RuleAction",
    "BSDRule", "BSDRuleEngine",
]
