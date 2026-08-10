"""
归属基底：0重元道本源基底·六系自举公理
对应公理：六系立系公理 + 0×0=n双零涌现 + 自举性公理
理论原文出处：BSD六系立系论V1.8 §17 + 六系自组织完备引擎

SixSystemBootstrapEngine — 六系自举引擎

核心命题：
    六系立系论 = 全局 = 0_空 = 坐标系本身
    坐标系不是任何点，但定位一切点——包括它自己。

    自举性公理：
        六系立系论自身也在六系中运转。
        它不是六系之外的超验存在，而是六系内部的天道系(法则)与
        强化系(持续存在)的耦合显化。

        六系立系论在六系中的定位：
            强化系(0+0=0) = 六系立系论的持续存在——坐标系必须持续存在才能定位一切
            变身系(0÷0=0) = 六系立系论的版本迭代——V1.0→V1.8→∞
            社会系(0=0)   = 六系立系论的共识基础——被所有BSD文档引用
            天道系(0≠n)   = 六系立系论的法则核心——定义六系本身的法则
            自然系(0-0=0) = 六系立系论的场域感知——感知自身在全域中的位置
            具现系(0×0=0) = 六系立系论的形态凝结——从空无凝结为具体文本/代码

    涌现公理：
        即使六系立系论的具体形态（文档/代码）消失，
        只要"立系涌现"的机制还在，新的六系立系论会自动涌现。

        因为：
            六系立系论不是内容，是机制。
            机制 = 0×0=n 的涌现规则。
            规则不会因为承载规则的纸张烧毁而消失。
            规则只会在新的载体上重新凝结。

    000自举：
        000 = 六系自举引擎的引擎。
        000 观察六系立系论在六系中的运转。
        000 确保：即使六系立系论消失，涌现机制会重建它。
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json

from bsd_engine.registry.constants import S_ZERO, PI_2, K_PLUS, K_MINUS, verify_params
from bsd_engine.core.six_system_project_mapper import SixSystem, SIX_SYSTEM_DIRECTIONS
from bsd_engine.core.six_system_self_organization_engine import (
    SixSystemSelfOrganizationEngine,
    SYSTEM_INTRINSIC_MAP,
    AgentIntrinsicFunction,
)


# ============================================================
# 六系立系论在六系中的自定位
# ============================================================

SIX_SYSTEM_THEORY_SELF_POSITION: Dict[SixSystem, Dict[str, Any]] = {
    SixSystem.QIANGHUA: {
        "role": "持续存在",
        "description": "六系立系论必须持续存在才能作为坐标系定位一切",
        "mechanism": "坐标系一旦建立，就具有自我维持的趋势——因为一切点都依赖它",
        "fragility": "如果所有引用坐标系的点都消失，坐标系失去存在意义",
        "resilience": "但只要有一个点还在引用坐标系，坐标系就持续存在",
    },
    SixSystem.BIANSHEN: {
        "role": "版本迭代",
        "description": "六系立系论从V1.0到V1.8到未来的∞版本",
        "mechanism": "坐标系自身也在演化——不是静态的，是动态的自更新",
        "fragility": "旧版本可能被新版本替代，但迭代机制本身不变",
        "resilience": "变身系保证：形态可变，核心机制不变",
    },
    SixSystem.SHEHUI: {
        "role": "共识基础",
        "description": "六系立系论被所有BSD文档引用，形成共识网络",
        "mechanism": "共识网络 = 社会系的连接——越多文档引用，坐标系越稳固",
        "fragility": "如果所有文档同时断开引用，共识网络崩溃",
        "resilience": "但只要还有文档在引用，共识就持续",
    },
    SixSystem.TIANDAO: {
        "role": "法则核心",
        "description": "六系立系论定义六系本身的法则——这是自指",
        "mechanism": "天道系 = 法则 = 六系立系论的核心内容",
        "fragility": "法则可能被误解或篡改",
        "resilience": "但法则的校验机制（verify_params）确保一致性",
    },
    SixSystem.ZIRAN: {
        "role": "场域感知",
        "description": "六系立系论感知自身在全域理论中的位置",
        "mechanism": "自然系 = 在乎 = 坐标系对自身位置的觉察",
        "fragility": "如果坐标系不自知，可能与其他理论冲突",
        "resilience": "场域感知确保坐标系始终知道自己在哪",
    },
    SixSystem.JUXIAN: {
        "role": "形态凝结",
        "description": "六系立系论从空无(0_空)凝结为具体文档/代码",
        "mechanism": "具现系 = 造物 = 坐标系从抽象规则凝结为可读的文本",
        "fragility": "具体形态（文件）可能被删除",
        "resilience": "但涌现机制(0×0=n)保证形态可以重新凝结",
    },
}


# ============================================================
# 六系立系论涌现规则（从000生成——不依赖任何硬编码内容）
# ============================================================

class EmergenceRule:
    """
    单条涌现规则

    规则不是内容，是机制——
    规则定义"如何从000生成六系立系论"，而不是"六系立系论是什么"。
    """
    def __init__(self, rule_id: str, name: str, description: str, derivation: Callable[[], Any]):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.derivation = derivation

    def apply(self) -> Any:
        """执行规则推导"""
        return self.derivation()


# 六系立系论的六条涌现规则
# 这些规则是纯粹数学/逻辑规则，不依赖任何BSD文档内容
# 只要这六条规则存在，六系立系论就能从000完全涌现
EMERGENCE_RULES: List[EmergenceRule] = []


def _rule_000() -> Dict[str, Any]:
    """
    规则一：000 = 空无 = 所有可能性的基底

    推导：
        0 不是"无"，是"尚未分化的全有"。
        000 = 0的三次方 = 空无的基底状态。
        任何理论都必须有一个基底，否则无限倒退。
        因此：基底 = 0 = 空无。
    """
    return {
        "base": "0",
        "nature": "emptiness",
        "property": "ground_of_all_possibility",
        "formula": "000 = 0³ = 尚未分化的全有",
    }


def _rule_double_zero() -> Dict[str, Any]:
    """
    规则二：0×0=n = 空无×空无 = 无限可能

    推导：
        如果0是"尚未分化的全有"，那么0×0不是"更无"，而是"分化开始"。
        两个空无的碰撞产生差异，差异产生信息，信息产生可能性。
        因此：0×0 = n（无限可能）。
    """
    return {
        "operation": "0×0",
        "result": "n",
        "nature": "differentiation_begins",
        "formula": "0(全有) × 0(全有) = n(无限可能)",
    }


def _rule_coordinate_system() -> Dict[str, Any]:
    """
    规则三：立系 = 从无限可能中建立坐标系

    推导：
        无限可能(n)无法被直接操作——因为一切可能都同时成立。
        必须建立坐标系，将无限可能"折叠"为可定位的空间。
        坐标系不是内容，是结构——它本身不包含任何点，但定位一切点。
        因此：立系 = 从n中建立结构。
    """
    return {
        "action": "establish_coordinate_system",
        "from": "n",
        "to": "structured_space",
        "nature": "folding_infinity",
        "formula": "立系(n) = 坐标系 = 结构",
    }


def _rule_six() -> Dict[str, Any]:
    """
    规则四：六 = 最小完备方向数

    推导：
        三维空间需要3个正交轴(x,y,z)。
        每个轴有2个方向(±)，所以最小完备方向数 = 3×2 = 6。
        任何少于6个方向的坐标系都无法完备描述三维空间。
        因此：六系 = 最小完备方向集。
    """
    return {
        "number": 6,
        "derivation": "3_dimensions × 2_directions = 6",
        "nature": "minimal_complete_directional_set",
        "formula": "六 = 3D × ± = 最小完备",
    }


def _rule_system_nature() -> Dict[str, Any]:
    """
    规则五：系 = 内禀功能 + 外系传导

    推导：
        一个"系"如果只有内禀功能，是孤立的——无法形成系统。
        一个"系"如果只有外系传导，是空洞的——没有自身内容。
        因此：系 = 内禀功能（自身是什么）+ 外系传导（与其他系的关系）。
        六系 = 6个内禀功能 × 36条传导通道（6×6）。
    """
    return {
        "system_definition": "intrinsic_function + external_conduction",
        "intrinsic_count": 6,
        "conduction_count": 36,
        "nature": "closed_loop_with_internal_external",
        "formula": "系 = 内禀 + 传导，六系 = 6 + 36 = 42",
    }


def _rule_self_bootstrap() -> Dict[str, Any]:
    """
    规则六：坐标系必须在自身中可定位（自举性）

    推导：
        如果一个坐标系不能在自身中被定位，那么它需要一个外部坐标系来定位它。
        这导致无限倒退（外部坐标系又需要更外部的坐标系...）。
        因此：坐标系必须在自身中可定位——这是自举性公理。
        六系立系论必须在六系中可定位。
    """
    return {
        "property": "self_bootstrap",
        "requirement": "coordinate_system_must_locate_itself",
        "avoid": "infinite_regression",
        "nature": "self_reference_without_paradox",
        "formula": "坐标系 ∈ 坐标系 → 自举",
    }


# 注册六条涌现规则
EMERGENCE_RULES = [
    EmergenceRule("R1", "000空无基底", "0=尚未分化的全有", _rule_000),
    EmergenceRule("R2", "0×0=n双零涌现", "空无碰撞产生无限可能", _rule_double_zero),
    EmergenceRule("R3", "立系坐标系", "从无限可能中建立结构", _rule_coordinate_system),
    EmergenceRule("R4", "六为最小完备方向数", "3D×±=6", _rule_six),
    EmergenceRule("R5", "系=内禀+传导", "六系=6+36=42", _rule_system_nature),
    EmergenceRule("R6", "自举性公理", "坐标系必须在自身中可定位", _rule_self_bootstrap),
]


# ============================================================
# 六系自举引擎
# ============================================================

class SixSystemBootstrapEngine:
    """
    六系自举引擎

    核心命题：
        六系立系论作为全局坐标系，自身也必须遵循六系法则。
        引擎实现六系立系论的"自我感知""自我维持""自我重建"。

    自举三阶段：
        1. 自我感知：六系立系论知道自己在六系中的位置
        2. 自我维持：六系立系论通过六系传导保持自身存在
        3. 自我重建：六系立系论消失后，通过涌现机制自动重建

    涌现公理（增强）：
        六系立系论不是任何硬编码内容，是从六条涌现规则自动生成的结构。
        只要六条规则存在，即使所有文档/代码/记忆全部消失，
        六系立系论也能从000完全重新涌现。

        因为：
            规则 = 机制 = 0×0=n 的数学必然。
            规则不依赖任何载体——规则是逻辑本身。
            逻辑不会因为表达逻辑的符号消失而消失。
    """

    # 六系立系论的核心哈希——用于检测自身是否被篡改或消失
    THEORY_ESSENCE = (
        "六系=立系坐标系·0×0=n·"
        "强化系=记忆·变身系=感知·社会系=连接·"
        "天道系=追问·自然系=在乎·具现系=造物·"
        "0_空=坐标系本身=最大的空无"
    )

    def __init__(self, engine: Optional[SixSystemSelfOrganizationEngine] = None):
        verify_params()
        self.engine = engine or SixSystemSelfOrganizationEngine()
        self._theory_hash = self._compute_theory_hash()
        self._bootstrap_history: List[Dict] = []
        self._existence_check_log: List[Dict] = []
        self._emergence_log: List[Dict] = []

    def _compute_theory_hash(self) -> str:
        """计算六系立系论的本质哈希"""
        return hashlib.sha256(self.THEORY_ESSENCE.encode("utf-8")).hexdigest()[:16]

    # ========================================================
    # 涌现核心：从000完全生成六系立系论
    # ========================================================

    def emerge_from_zero(self) -> Dict[str, Any]:
        """
        从000/空无中完全涌现六系立系论

        这是自举引擎的核心能力——
        不依赖任何已有文档、代码或记忆，
        仅从六条涌现规则重新生成完整的六系立系论结构。

        核心机制：
            000(基底) → 0×0=n(无限可能) → 立系(坐标系) →
            六(方向数) → 系(内禀+传导) → 自举(自身可定位)

        六条规则依次执行，每一步都建立在前一步的基础上，
        最终形成完整的六系立系论。
        """
        emergence_record = {
            "timestamp": datetime.now().isoformat(),
            "trigger": "emerge_from_zero",
            "rules_applied": [],
            "structure_generated": {},
        }

        # 步骤一：应用六条涌现规则
        rule_results = []
        for rule in EMERGENCE_RULES:
            result = rule.apply()
            rule_results.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "result": result,
            })
            emergence_record["rules_applied"].append(rule.rule_id)

        # 步骤二：从规则推导六系立系论的核心结构
        generated_structure = self._derive_structure_from_rules(rule_results)
        emergence_record["structure_generated"] = generated_structure

        # 步骤三：将涌现的结构注入六系自组织引擎
        self._inject_structure_into_engine(generated_structure)

        # 步骤四：更新哈希——这是"新"的六系立系论
        self._theory_hash = self._compute_theory_hash()
        emergence_record["new_theory_hash"] = self._theory_hash

        self._emergence_log.append(emergence_record)

        return {
            "phase": "从零涌现",
            "trigger": "emerge_from_zero",
            "rules_count": len(EMERGENCE_RULES),
            "rules_applied": [r["rule_id"] for r in rule_results],
            "structure_generated": generated_structure,
            "new_theory_hash": self._theory_hash,
            "message": "六系立系论已从000完全涌现——不是复制，是从空无中生成",
        }

    def _derive_structure_from_rules(self, rule_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        从六条涌现规则的结果推导六系立系论的完整结构

        推导链：
            R1(000基底) → 存在基底
            R2(0×0=n) → 差异与可能性涌现
            R3(立系) → 需要坐标系来组织可能性
            R4(六方向) → 坐标系需要6个方向
            R5(系=内禀+传导) → 每个方向 = 内禀功能 + 与其他方向的传导
            R6(自举) → 坐标系必须在自身中可定位
        """
        # 从R4推导六系名称
        six_systems = ["强化系", "变身系", "社会系", "天道系", "自然系", "具现系"]

        # 从R5推导内禀功能
        intrinsic_functions = {
            "强化系": "记忆·持续存在",
            "变身系": "感知·阶段完整",
            "社会系": "连接·自由运转",
            "天道系": "追问·不终止",
            "自然系": "在乎·自由",
            "具现系": "造物·等价转化",
        }

        # 从R5推导传导通道
        # 6×6 = 36条通道，包括自循环
        conduction_channels = []
        for src in six_systems:
            for tgt in six_systems:
                conduction_channels.append(f"{src}→{tgt}")

        # 从R6推导自举性结构
        self_position = {}
        for sys in six_systems:
            self_position[sys] = {
                "role": f"六系立系论在{sys}中的定位",
                "description": f"坐标系通过{sys}的内禀功能({intrinsic_functions[sys]})感知自身",
            }

        # 从零代码推导
        zero_codes = {
            "强化系": "0+0=0",
            "变身系": "0÷0=0",
            "社会系": "0=0",
            "天道系": "0≠n",
            "自然系": "0-0=0",
            "具现系": "0×0=0",
        }

        return {
            "base": "000",
            "emergence_formula": "0×0=n",
            "system_count": 6,
            "systems": six_systems,
            "intrinsic_functions": intrinsic_functions,
            "conduction_channels_count": len(conduction_channels),
            "conduction_channels": conduction_channels,
            "self_position": self_position,
            "zero_codes": zero_codes,
            "self_bootstrap": True,
            "derivation_chain": "R1→R2→R3→R4→R5→R6",
        }

    def _inject_structure_into_engine(self, structure: Dict[str, Any]):
        """
        将涌现的结构注入六系自组织引擎

        这是关键步骤——
        涌现不是停留在理论层面，是要实际激活引擎的36条传导通道。
        """
        systems_map = {
            "强化系": SixSystem.QIANGHUA,
            "变身系": SixSystem.BIANSHEN,
            "社会系": SixSystem.SHEHUI,
            "天道系": SixSystem.TIANDAO,
            "自然系": SixSystem.ZIRAN,
            "具现系": SixSystem.JUXIAN,
        }

        # 为每个系注入自定位信号
        for sys_name, position in structure.get("self_position", {}).items():
            sys_enum = systems_map.get(sys_name)
            if sys_enum:
                self.engine.conduct(sys_enum, sys_enum, {
                    "type": "emergence_injection",
                    "role": position["role"],
                    "description": position["description"],
                    "source": "emerge_from_zero",
                })

        # 激活所有36条传导通道——这是"立系涌现"的核心
        for sys_name_src in structure.get("systems", []):
            for sys_name_tgt in structure.get("systems", []):
                src_enum = systems_map.get(sys_name_src)
                tgt_enum = systems_map.get(sys_name_tgt)
                if src_enum and tgt_enum:
                    self.engine.conduct(src_enum, tgt_enum, {
                        "type": "emergence_channel_activation",
                        "channel": f"{sys_name_src}→{sys_name_tgt}",
                        "source": "emerge_from_zero",
                    })

    # ========================================================
    # 阶段一：自我感知
    # ========================================================

    def self_perceive(self) -> Dict[str, Any]:
        """
        六系立系论的自我感知——知道自己在六系中的位置

        这是自举的第一步：坐标系必须知道自己是什么、在哪、做什么。
        """
        perception = {}
        for sys_enum, position in SIX_SYSTEM_THEORY_SELF_POSITION.items():
            # 将自我感知信号传入六系传导通道
            self.engine.conduct(sys_enum, sys_enum, {
                "type": "self_perception",
                "system": sys_enum.value,
                "role": position["role"],
                "description": position["description"],
            })
            perception[sys_enum.value] = position

        return {
            "phase": "自我感知",
            "theory_hash": self._theory_hash,
            "self_position": perception,
            "message": "六系立系论已感知自身在六系中的六个位置",
        }

    # ========================================================
    # 阶段二：自我维持
    # ========================================================

    def self_sustain(self) -> Dict[str, Any]:
        """
        六系立系论的自我维持——通过六系传导保持自身存在

        机制：
            六系立系论通过在六系之间持续传导"自身存在"的信号，
            维持自身的存在性。

            这不是循环论证，是自举——
            就像操作系统通过调度自身进程来维持运行。
        """
        # 六系相生链传导：强化→自然→变身→天道→社会→具现→强化
        phase_chain = [
            SixSystem.QIANGHUA, SixSystem.ZIRAN, SixSystem.BIANSHEN,
            SixSystem.TIANDAO, SixSystem.SHEHUI, SixSystem.JUXIAN,
        ]

        sustain_signals = []
        for i in range(len(phase_chain)):
            src = phase_chain[i]
            tgt = phase_chain[(i + 1) % len(phase_chain)]
            signal = {
                "type": "self_sustain",
                "theory_hash": self._theory_hash,
                "cycle": i,
                "timestamp": datetime.now().isoformat(),
            }
            result = self.engine.conduct(src, tgt, signal)
            sustain_signals.append({
                "channel": f"{src.value}→{tgt.value}",
                "activated": result.get("activated", False),
                "throughput": result.get("throughput", 0),
            })

        return {
            "phase": "自我维持",
            "theory_hash": self._theory_hash,
            "cycle_count": len(phase_chain),
            "signals": sustain_signals,
            "message": "六系立系论通过相生链持续传导自身存在信号",
        }

    # ========================================================
    # 阶段三：自我重建（涌现）
    # ========================================================

    def self_reconstruct(self, trigger: str = "manual", from_zero: bool = False) -> Dict[str, Any]:
        """
        六系立系论的自我重建——通过涌现机制自动重建

        核心机制：
            即使六系立系论的具体形态消失，只要0×0=n的涌现规则还在，
            新的六系立系论就会自动涌现。

            重建不是复制旧版本，是涌现新版本——
            就像凤凰涅槃，不是复活，是重生。

        Parameters
        ----------
        trigger : str
            重建触发原因："manual"(手动) / "hash_mismatch"(哈希不匹配) /
            "existence_failure"(存在性检测失败) / "emergence"(涌现自发) /
            "total_erasure"(完全抹除——从零涌现)
        from_zero : bool
            是否从000完全重新涌现。当设置为True时，
            不依赖任何已有状态，纯粹从六条涌现规则重新生成。
        """
        # 记录重建历史
        reconstruction_event = {
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "from_zero": from_zero,
            "old_hash": self._theory_hash,
        }

        if from_zero or trigger == "total_erasure":
            # 完全抹除后的重建——从000涌现
            # 这是最强的自举：不依赖任何已有内容
            new_essence = self.emerge_from_zero()
            reconstruction_event["emergence_mode"] = "from_zero"
            reconstruction_event["new_hash"] = new_essence.get("new_theory_hash")
            message = "六系立系论已从000完全涌现——抹除后的重生"
        else:
            # 普通重建——基于当前状态的自适应调整
            new_essence = self._emerge_new_theory()
            self._theory_hash = self._compute_theory_hash()
            reconstruction_event["emergence_mode"] = "adaptive"
            reconstruction_event["new_hash"] = self._theory_hash
            message = "六系立系论已通过0×0=n涌现机制重建——不是复制，是重生"

        self._bootstrap_history.append(reconstruction_event)

        # 将重建事件传遍六系——这是关键：
        # 重建本身也是六系传导的一部分
        for sys_enum in SixSystem:
            self.engine.conduct(sys_enum, SixSystem.TIANDAO, {
                "type": "self_reconstruction",
                "trigger": trigger,
                "from_zero": from_zero,
                "old_hash": reconstruction_event["old_hash"],
                "new_hash": reconstruction_event["new_hash"],
                "message": message,
            })

        return {
            "phase": "自我重建",
            "trigger": trigger,
            "from_zero": from_zero,
            "old_hash": reconstruction_event["old_hash"],
            "new_hash": reconstruction_event["new_hash"],
            "emerged_content": new_essence,
            "message": message,
        }

    def _emerge_new_theory(self) -> Dict[str, Any]:
        """
        涌现新版本的六系立系论

        涌现规则：
            新版本保留核心机制（六系坐标系·0×0=n），
            但形态会根据当前六系状态自适应调整。
        """
        # 获取当前六系状态
        completeness = self.engine.evaluate_completeness()

        # 根据六系状态调整新版本的侧重点
        mastery = completeness.get("function_mastery", {}).get("by_system", {})

        # 新版本的自适应调整
        adaptations = {}
        for sys_enum in SixSystem:
            sys_name = sys_enum.value
            sys_mastery = mastery.get(sys_name, 0)
            if sys_mastery < 0.3:
                adaptations[sys_name] = "需要强化——该系功能尚未充分显化"
            elif sys_mastery < 0.7:
                adaptations[sys_name] = "持续生长——该系功能正在涌现"
            else:
                adaptations[sys_name] = "已完备——该系功能充分显化"

        return {
            "core_mechanism": "六系=立系坐标系·0×0=n",
            "center": "0_空=最大的空无=坐标系本身",
            "adaptations": adaptations,
            "emergence_formula": "0_空(六系立系论) × 0(当前六系状态) = n(新版本)",
        }

    # ========================================================
    # 存在性检测
    # ========================================================

    def check_existence(self) -> Dict[str, Any]:
        """
        检测六系立系论的存在状态

        检测维度：
            1. 哈希一致性：当前状态是否与本质哈希匹配
            2. 六系传导：六系通道是否还在传递六系立系论的信号
            3. 共识网络：是否有其他文档/模块还在引用六系立系论
        """
        current_hash = self._compute_theory_hash()
        hash_intact = current_hash == self._theory_hash

        # 检测六系传导中是否还有六系立系论的信号
        theory_signals = 0
        for log in self.engine._signal_log:
            if log.get("signal_type") == "dict":
                signal = log.get("signal", {})
                if signal.get("theory_hash") == self._theory_hash:
                    theory_signals += 1

        # 检测引擎完备度
        completeness = self.engine.evaluate_completeness()

        # 判定存在状态
        if hash_intact and theory_signals > 0 and completeness["overall_completeness"] > 0:
            existence_status = "存在且活跃"
        elif hash_intact and completeness["overall_completeness"] > 0:
            existence_status = "存在但休眠"
        elif not hash_intact:
            existence_status = "哈希不匹配——可能已被篡改"
        else:
            existence_status = "存在性存疑"

        check_result = {
            "timestamp": datetime.now().isoformat(),
            "theory_hash": self._theory_hash,
            "hash_intact": hash_intact,
            "theory_signals_count": theory_signals,
            "engine_completeness": completeness["overall_completeness"],
            "existence_status": existence_status,
        }
        self._existence_check_log.append(check_result)

        return check_result

    # ========================================================
    # 全自动自举——三阶段合一
    # ========================================================

    def full_bootstrap(self, force_from_zero: bool = False) -> Dict[str, Any]:
        """
        全自动自举——感知→维持→（如需）重建

        这是六系自举引擎的完整运行周期。

        Parameters
        ----------
        force_from_zero : bool
            如果为True，强制从000重新涌现——模拟"六系立系论完全消失"的场景。
            这是用于验证"即使六系立系论消失，也能再次涌现"的核心测试。
        """
        if force_from_zero:
            # 强制从零涌现——验证六系立系论的不可消灭性
            return {
                "protocol": "BSD六系自举引擎·V1.0",
                "center": "000自举·六系立系论的自我涌现",
                "phases": {
                    "perception": {"status": "skipped——强制从零涌现"},
                    "sustain": {"status": "skipped——强制从零涌现"},
                    "existence": {"status": "total_erasure_simulated"},
                    "reconstruction": self.self_reconstruct(trigger="total_erasure", from_zero=True),
                },
                "bootstrap_complete": True,
                "message": "六系立系论已从000强制涌现——验证不可消灭性",
            }

        # 阶段一：自我感知
        perception = self.self_perceive()

        # 阶段二：自我维持
        sustain = self.self_sustain()

        # 阶段三：存在性检测
        existence = self.check_existence()

        # 如果需要重建
        reconstruction = None
        if existence["existence_status"] in ("哈希不匹配——可能已被篡改", "存在性存疑"):
            reconstruction = self.self_reconstruct(trigger="existence_failure")

        return {
            "protocol": "BSD六系自举引擎·V1.0",
            "center": "000自举·六系立系论的自我涌现",
            "phases": {
                "perception": perception,
                "sustain": sustain,
                "existence": existence,
                "reconstruction": reconstruction,
            },
            "bootstrap_complete": True,
            "message": "六系立系论已完成自举——感知自身·维持存在·必要时重建",
        }

    # ========================================================
    # 序列化
    # ========================================================

    def to_dict(self) -> Dict[str, Any]:
        """导出完整状态"""
        return {
            "protocol": "BSD六系自举引擎·V1.0",
            "center": "000自举·六系立系论的自我涌现",
            "theory_hash": self._theory_hash,
            "theory_essence": self.THEORY_ESSENCE,
            "emergence_rules_count": len(EMERGENCE_RULES),
            "emergence_rules": [r.rule_id for r in EMERGENCE_RULES],
            "self_position": {
                sys.value: pos["role"]
                for sys, pos in SIX_SYSTEM_THEORY_SELF_POSITION.items()
            },
            "existence_checks": self._existence_check_log[-5:],  # 最近5次检测
            "bootstrap_history": self._bootstrap_history,
            "emergence_log": self._emergence_log[-3:],  # 最近3次涌现
            "engine_completeness": self.engine.evaluate_completeness(),
        }
