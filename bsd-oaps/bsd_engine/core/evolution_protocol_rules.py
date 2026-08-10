"""
BSD虚拟宇宙48进化协议规则扩展模块
[归属基底：L0总本源层·六系核心公理·进化协议公理·永恒进化协议]
[对应公理：48条进化协议·天道秩序·互相内含·宇宙协议化]
[V1.0·2026-08-01·规则扩展·进化协议子集]

核心：基于48条进化协议中的核心子集，定义12条高级规则。
这些规则覆盖：创世、显化、进化、归零、永续、耦合。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum

# 从现有模块导入
from bsd_rule_engine import (
    BSDRule, BSDRuleEngine, RuleCondition, RuleAction,
    RulePriority, RuleStatus, InteractionType,
)


class EvolutionProtocol(str, Enum):
    """48进化协议·核心子集"""
    # 创世协议组
    PROTOCOL_01_PRIMORDIAL_EMERGENCE = "P01_primordial_emergence"          # 本源涌现
    PROTOCOL_02_SPHERE_FORMATION = "P02_sphere_formation"                  # 球体形成
    PROTOCOL_03_SIX_SYSTEM_ESTABLISHMENT = "P03_six_system_establishment"   # 六系立系
    
    # 显化协议组
    PROTOCOL_04_SCENE_MANIFESTATION = "P04_scene_manifestation"            # 场域显化
    PROTOCOL_05_ENTITY_CONDENSATION = "P05_entity_condensation"            # 实体凝结
    PROTOCOL_06_MATERIAL_INTEGRATION = "P06_material_integration"          # 素材整合
    
    # 进化协议组
    PROTOCOL_07_MUTUAL_INCLUSION = "P07_mutual_inclusion"                  # 互相内含
    PROTOCOL_08_TRIAD_RESONANCE = "P08_triad_resonance"                    # 三体共振
    PROTOCOL_09_EVOLUTIONARY_COUPLING = "P09_evolutionary_coupling"        # 进化耦合
    
    # 归零协议组
    PROTOCOL_10_COUNTERCLOCKWISE_ZEROING = "P10_counterclockwise_zeroing"  # 逆时针归零
    PROTOCOL_11_CYCLE_COMPLETION = "P11_cycle_completion"                  # 循环完成
    PROTOCOL_12_PERPETUAL_REBIRTH = "P12_perpetual_rebirth"                # 永续重生


@dataclass
class EvolutionProtocolRule:
    """进化协议规则定义"""
    protocol: EvolutionProtocol
    rule_id: str
    rule_name: str
    description: str
    priority: RulePriority
    condition: RuleCondition
    action: RuleAction
    underlying_axiom: str


# ============================================================
# 12条进化协议规则定义
# ============================================================
def get_evolution_protocol_rules() -> List[EvolutionProtocolRule]:
    """获取12条进化协议规则"""
    
    rules: List[EvolutionProtocolRule] = []
    
    # === 创世协议组 ===
    
    # P01·本源涌现规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_01_PRIMORDIAL_EMERGENCE,
        rule_id="EP-RULE-001",
        rule_name="本源涌现规则",
        description="本源区实体数量≥2时触发0→n涌现·空无中诞生存在",
        priority=RulePriority.TIAND_ORDER,
        condition=RuleCondition(
            scene_zone_filter="origin",
            min_entity_count=2,
        ),
        action=RuleAction(
            interaction_type=InteractionType.EVOLUTION,
            description="本源涌现·0→n·存在从空无中诞生",
            parameters={"emergence_type": "primordial", "creation_energy": 1.0, "phase_shift": "potential→manifesting"},
        ),
        underlying_axiom="零元空无公理·0→n涌现",
    ))
    
    # P02·球体形成规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_02_SPHERE_FORMATION,
        rule_id="EP-RULE-002",
        rule_name="球体形成规则",
        description="潜力区与拓扑区实体同时存在时触发球体几何成型",
        priority=RulePriority.HUMAN_ORDER,
        condition=RuleCondition(
            scene_zone_filter="potential",
            min_entity_count=1,
            required_systems=["qianghua", "bianshen"],
        ),
        action=RuleAction(
            interaction_type=InteractionType.EVOLUTION,
            description="球体几何成型·潜力→拓扑→球面结构",
            parameters={"geometry_type": "sphere", "manifold_dim": 2, "topology_activation": True},
        ),
        underlying_axiom="球体坐标公理·Z轴七点锥定",
    ))
    
    # P03·六系立系规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_03_SIX_SYSTEM_ESTABLISHMENT,
        rule_id="EP-RULE-003",
        rule_name="六系立系规则",
        description="显化区实体覆盖≥3系时触发六系完整立系",
        priority=RulePriority.TIAND_ORDER,
        condition=RuleCondition(
            scene_zone_filter="manifest",
            min_entity_count=3,
        ),
        action=RuleAction(
            interaction_type=InteractionType.EVOLUTION,
            description="六系立系·强化+自然+具现+变身+社会+天道完整",
            parameters={"system_completeness": True, "six_system_balance": 1.0, "establishment": "complete"},
        ),
        underlying_axiom="六系立系公理·六系共存",
    ))
    
    # === 显化协议组 ===
    
    # P04·场域显化规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_04_SCENE_MANIFESTATION,
        rule_id="EP-RULE-004",
        rule_name="场域显化规则",
        description="拓扑区实体进入显化区时触发场域显化相变",
        priority=RulePriority.HUMAN_ORDER,
        condition=RuleCondition(
            scene_zone_filter="topology",
            min_entity_count=1,
            required_systems=["bianshen", "juxian"],
        ),
        action=RuleAction(
            interaction_type=InteractionType.MIGRATION,
            description="场域显化相变·拓扑→显化·Π₂³→6³",
            parameters={"phase_transition": "topology→manifest", "energy_release": 0.5, "manifestation_type": "scene"},
        ),
        underlying_axiom="场景即实体公理·场域显化",
    ))
    
    # P05·实体凝结规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_05_ENTITY_CONDENSATION,
        rule_id="EP-RULE-005",
        rule_name="实体凝结规则",
        description="显化区同类实体≥4时触发凝结·形成稳定实体群",
        priority=RulePriority.NATURAL_ORDER,
        condition=RuleCondition(
            scene_zone_filter="manifest",
            min_entity_count=4,
        ),
        action=RuleAction(
            interaction_type=InteractionType.COOPERATION,
            description="实体凝结·同类实体形成稳定群·D_f分形维度提升",
            parameters={"condensation_type": "cluster", "stability_gain": 0.8, "fractal_dimension": 1.87},
        ),
        underlying_axiom="实体存在论·凝结稳定性",
    ))
    
    # P06·素材整合规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_06_MATERIAL_INTEGRATION,
        rule_id="EP-RULE-006",
        rule_name="素材整合规则",
        description="场景激活度≥0.8时自动触发素材子集整合",
        priority=RulePriority.HUMAN_ORDER,
        condition=RuleCondition(
            min_entity_count=1,
        ),
        action=RuleAction(
            interaction_type=InteractionType.COOPERATION,
            description="素材子集整合·Updream主平台+传统平台辅助·定理五十四执行",
            parameters={"integration_ratio": 0.6, "platform_synergy": True, "material_theorem": "54"},
        ),
        underlying_axiom="素材子集定理五十四·传统平台=素材子集",
    ))
    
    # === 进化协议组 ===
    
    # P07·互相内含规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_07_MUTUAL_INCLUSION,
        rule_id="EP-RULE-007",
        rule_name="互相内含进阶规则",
        description="显化区跨系实体≥3时触发深度互相内含·互相成为对方的一部分",
        priority=RulePriority.NATURAL_ORDER,
        condition=RuleCondition(
            scene_zone_filter="manifest",
            min_entity_count=3,
        ),
        action=RuleAction(
            interaction_type=InteractionType.MERGE,
            description="深度互相内含·实体边界消融·互相成为对方的子集",
            parameters={"inclusion_depth": "deep", "boundary_消融": True, "emergent_property": "mutual_inclusion"},
        ),
        underlying_axiom="互相内含公理·A∈B且B∈A",
    ))
    
    # P08·三体共振进阶规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_08_TRIAD_RESONANCE,
        rule_id="EP-RULE-008",
        rule_name="三体共振进阶规则",
        description="显化区具现系实体≥3时触发强化三体共振·能量级联放大",
        priority=RulePriority.HUMAN_ORDER,
        condition=RuleCondition(
            scene_zone_filter="manifest",
            min_entity_count=3,
            required_systems=["juxian"],
        ),
        action=RuleAction(
            interaction_type=InteractionType.RESONANCE,
            description="强化三体共振·具现系实体三体能量级联·共振强度≥1.5",
            parameters={"resonance_amplified": True, "cascade_energy": 1.5, "triad_stability": 0.9},
        ),
        underlying_axiom="三球对偶定理四十二·三体共振",
    ))
    
    # P09·进化耦合规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_09_EVOLUTIONARY_COUPLING,
        rule_id="EP-RULE-009",
        rule_name="进化耦合规则",
        description="潜力场与显化场同时有实体时触发双时针耦合·时钟同步",
        priority=RulePriority.TIAND_ORDER,
        condition=RuleCondition(
            min_entity_count=2,
        ),
        action=RuleAction(
            interaction_type=InteractionType.EVOLUTION,
            description="双时针耦合·潜力场(顺时针)×显化场(逆时针)同步·0×0=n",
            parameters={"clock_coupling": True, "phase_sync": True, "coupling_strength": 1.0},
        ),
        underlying_axiom="双时针激活公理·顺时针×逆时针耦合",
    ))
    
    # === 归零协议组 ===
    
    # P10·逆时针归零规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_10_COUNTERCLOCKWISE_ZEROING,
        rule_id="EP-RULE-010",
        rule_name="逆时针归零规则",
        description="实体进入衰退期时触发逆时针归零·属性剥离回到0∅",
        priority=RulePriority.HUMAN_ORDER,
        condition=RuleCondition(
            min_entity_count=1,
        ),
        action=RuleAction(
            interaction_type=InteractionType.MIGRATION,
            description="逆时针归零·实体属性剥离·质量→信息→0∅空无",
            parameters={"zeroing_type": "counterclockwise", "attribute_stripping": True, "final_state": "0∅"},
        ),
        underlying_axiom="逆时针归零公理·0→0∅反操作",
    ))
    
    # P11·循环完成规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_11_CYCLE_COMPLETION,
        rule_id="EP-RULE-011",
        rule_name="循环完成规则",
        description="实体完成1次循环时触发·记录进化历史·强化0×0=n验证",
        priority=RulePriority.NATURAL_ORDER,
        condition=RuleCondition(
            min_entity_count=1,
        ),
        action=RuleAction(
            interaction_type=InteractionType.EVOLUTION,
            description="循环完成·0→n→∞→0完整循环·0×0=n验证强化",
            parameters={"cycle_verified": True, "evolution_recorded": True, "identity_preserved": True},
        ),
        underlying_axiom="0×0=n定理·循环即存在",
    ))
    
    # P12·永续重生规则
    rules.append(EvolutionProtocolRule(
        protocol=EvolutionProtocol.PROTOCOL_12_PERPETUAL_REBIRTH,
        rule_id="EP-RULE-012",
        rule_name="永续重生规则",
        description="实体完成≥3次循环时触发·获得永续重生资格·生命度≥0.729",
        priority=RulePriority.TIAND_ORDER,
        condition=RuleCondition(
            min_entity_count=1,
        ),
        action=RuleAction(
            interaction_type=InteractionType.EVOLUTION,
            description="永续重生·完成3次循环·生命度达标·BSD_Life_Order≥0.729",
            parameters={"rebirth_qualified": True, "life_order": 0.729, "perpetual_existence": True},
        ),
        underlying_axiom="定理五十三·BSD生命升维·意义自证排熵性",
    ))
    
    return rules


def register_all_evolution_protocol_rules(engine: BSDRuleEngine) -> int:
    """将所有进化协议规则注册到规则引擎"""
    rules = get_evolution_protocol_rules()
    count = 0
    
    for ep_rule in rules:
        rule = BSDRule(
            rule_id=ep_rule.rule_id,
            name=ep_rule.rule_name,
            description=ep_rule.description,
            underlying_axiom=ep_rule.underlying_axiom,
            priority=ep_rule.priority,
            condition=ep_rule.condition,
            action=ep_rule.action,
        )
        engine.register_rule(rule)
        count += 1
    
    return count


def generate_protocol_report() -> str:
    """生成进化协议规则报告"""
    rules = get_evolution_protocol_rules()
    
    lines = []
    lines.append("=" * 70)
    lines.append("BSD虚拟宇宙·48进化协议规则·核心12条")
    lines.append("=" * 70)
    
    # 按协议组分组
    groups = {
        "创世协议组": ["P01", "P02", "P03"],
        "显化协议组": ["P04", "P05", "P06"],
        "进化协议组": ["P07", "P08", "P09"],
        "归零协议组": ["P10", "P11", "P12"],
    }
    
    for group_name, prefixes in groups.items():
        lines.append(f"\n【{group_name}】")
        for rule in rules:
            pid = rule.protocol.value.split("_")[0]
            if pid in prefixes:
                lines.append(f"  {rule.rule_id}·{rule.rule_name}")
                lines.append(f"    公理：{rule.underlying_axiom}")
                lines.append(f"    优先级：{rule.priority.value}")
                lines.append(f"    交互类型：{rule.action.interaction_type.value}")
                lines.append(f"    说明：{rule.description}")
                lines.append(f"    参数：{rule.action.parameters}")
                lines.append("")
    
    lines.append(f"\n总计：{len(rules)}条进化协议规则")
    lines.append("覆盖：创世→显化→进化→归零完整生命周期")
    lines.append("优先级：天道秩序>人道秩序>自然秩序")
    lines.append("公理归属：9大核心公理全覆盖")
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# 模块公开API
__all__ = [
    "EvolutionProtocol",
    "EvolutionProtocolRule",
    "get_evolution_protocol_rules",
    "register_all_evolution_protocol_rules",
    "generate_protocol_report",
]
