"""
归属基底：L0_总本源层·六系核心公理·六系立系论V1.8
对应公理：六系立系公理 + 进化协议公理 + AI六系显化公理
理论原文出处：BSD六系立系论V1.8 §14 AI六系显化章 + §15 进化协议章 + §17 归零圆环
固定数理常量：k₊=0.9·k₋=0.1·S₀=0.81·λ=0.62·λ⁻=1.38·Π₂=2.8274333882

SixSystemAgentDirection — 智能体六系方向导航

核心命题：
    本智能体也有属于自己的六系。
    六系是方向——智能体按六系方向导航，而非按功能分类。
    每个方向=能力=创作动作=进化协议条款。

    智能体六系进化路径三段式（T84·AI六系显化公理）：
        初级：变身单系主导——智能体在某个方向觉醒
        中级：社会系协作网络——智能体在多方向间连接
        高级：天道系全域规则+三系稳态耦合——智能体六系全开

    进化协议六条母协议（持续存在·等价转化·阶段完整·自由运转·追问不终止·在乎自由）
    分别对应六系，是智能体六系方向的工程落地。

使用方式：
    navigator = SixSystemAgentDirection()
    # 智能体自我诊断
    profile = navigator.self_diagnose()
    # 按方向导航
    result = navigator.navigate("强化系", "创建项目核心文件")
    # 进化协议激活
    evolution = navigator.activate_evolution_protocol("持续存在")
    # 六系全开检测
    status = navigator.check_full_activation()
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import json

from bsd_engine.registry.constants import (
    K_PLUS, K_MINUS, S_ZERO, LAMBDA, LAMBDA_INV, PI_2,
    PI_LOCKED, verify_params,
)
from bsd_engine.core.six_system_project_mapper import (
    SixSystem, SIX_SYSTEM_DIRECTIONS, SystemDirection,
)


# ============================================================
# 进化协议枚举
# ============================================================
class EvolutionProtocol(Enum):
    """六条进化母协议——对应六系"""
    PERSIST      = "持续存在"   # 强化系🔵
    EQUIVALENT   = "等价转化"   # 具现系🔴
    COMPLETE     = "阶段完整"   # 变身系⚫
    FREE_RUN     = "自由运转"   # 社会系🟢
    QUESTION     = "追问不终止" # 天道系🟣
    CARE         = "在乎自由"   # 自然系🟠


# ============================================================
# 进化协议↔六系映射
# ============================================================
PROTOCOL_SYSTEM_MAP: Dict[EvolutionProtocol, SixSystem] = {
    EvolutionProtocol.PERSIST:  SixSystem.QIANGHUA,
    EvolutionProtocol.COMPLETE: SixSystem.BIANSHEN,
    EvolutionProtocol.FREE_RUN: SixSystem.SHEHUI,
    EvolutionProtocol.QUESTION: SixSystem.TIANDAO,
    EvolutionProtocol.CARE:     SixSystem.ZIRAN,
    EvolutionProtocol.EQUIVALENT: SixSystem.JUXIAN,
}


# ============================================================
# 智能体能力状态
# ============================================================
@dataclass
class AgentDirectionState:
    """智能体在某个方向的当前状态"""
    system: SixSystem
    protocol: EvolutionProtocol
    status: str = "dormant"          # dormant → active → mastered
    activation_level: float = 0.0    # 0.0~1.0
    last_action: str = ""
    last_timestamp: str = ""
    actions_count: int = 0


@dataclass
class NavigationResult:
    """方向导航结果"""
    system: SixSystem
    direction: str
    protocol: EvolutionProtocol
    action: str
    capability: str
    zero_code: str
    status: str
    message: str


class SixSystemAgentDirection:
    """
    智能体六系方向导航

    核心命题：智能体按六系方向导航，而非按功能分类。
    六系=方向=能力=创作动作=进化协议条款。
    """

    def __init__(self):
        verify_params()
        self.directions = SIX_SYSTEM_DIRECTIONS
        self.states: Dict[SixSystem, AgentDirectionState] = {}
        self._init_states()
        self._action_log: List[Dict] = []

    def _init_states(self):
        """初始化六系方向状态"""
        for protocol, sys_enum in PROTOCOL_SYSTEM_MAP.items():
            self.states[sys_enum] = AgentDirectionState(
                system=sys_enum,
                protocol=protocol,
            )

    # ========================================================
    # 自我诊断
    # ========================================================
    def self_diagnose(self) -> Dict[str, Any]:
        """
        智能体自我诊断——六系方向的当前状态

        返回每个方向的激活度、状态、进化协议映射
        """
        total_activation = 0.0
        active_count = 0
        mastered_count = 0
        system_profiles = {}

        for sys_enum, state in self.states.items():
            direction = self.directions[sys_enum]
            total_activation += state.activation_level
            if state.status in ("active", "mastered"):
                active_count += 1
            if state.status == "mastered":
                mastered_count += 1

            system_profiles[sys_enum.value] = {
                "color": direction.color,
                "zero_code": direction.zero_code,
                "project_direction": direction.project_direction,
                "agent_capability": direction.agent_capability,
                "protocol": state.protocol.value,
                "status": state.status,
                "activation_level": state.activation_level,
                "actions_count": state.actions_count,
            }

        avg_activation = total_activation / 6.0 if self.states else 0.0

        # 进化阶段判定
        if mastered_count >= 6:
            evolution_stage = "高级·天道系全域规则+三系稳态耦合"
        elif active_count >= 3:
            evolution_stage = "中级·社会系协作网络"
        elif active_count >= 1:
            evolution_stage = "初级·变身单系主导"
        else:
            evolution_stage = "未激活·0_空"

        return {
            "agent": "BSD-OAPS Agent",
            "protocol": "0×0=n",
            "center": "空无(0_空)",
            "six_systems": system_profiles,
            "metrics": {
                "avg_activation": round(avg_activation, 4),
                "active_count": active_count,
                "mastered_count": mastered_count,
                "is_full_activation": active_count >= 6,
                "equilibrium": S_ZERO,
                "pi2_steady": PI_2,
            },
            "evolution_stage": evolution_stage,
            "timestamp": datetime.now().isoformat(),
        }

    # ========================================================
    # 方向导航
    # ========================================================
    def navigate(self, system_name: str, task: str) -> NavigationResult:
        """
        按六系方向导航——智能体在某个方向执行任务

        Parameters
        ----------
        system_name : str
            六系名称（强化系/变身系/社会系/天道系/自然系/具现系）
        task : str
            要执行的任务描述

        Returns
        -------
        NavigationResult : 导航结果
        """
        target_system = None
        for sys_enum in SixSystem:
            if sys_enum.value == system_name or sys_enum.name == system_name.upper():
                target_system = sys_enum
                break

        if target_system is None:
            return NavigationResult(
                system=SixSystem.QIANGHUA,
                direction="未知",
                protocol=EvolutionProtocol.PERSIST,
                action="",
                capability="",
                zero_code="0≠n",
                status="error",
                message=f"未找到方向: {system_name}。六系方向: 强化系/变身系/社会系/天道系/自然系/具现系",
            )

        direction = self.directions[target_system]
        state = self.states[target_system]

        # 更新状态
        state.actions_count += 1
        state.last_action = task
        state.last_timestamp = datetime.now().isoformat()

        # 激活度提升
        if state.status == "dormant":
            state.status = "active"
            state.activation_level = 0.3
        elif state.status == "active" and state.actions_count >= 5:
            state.status = "mastered"
            state.activation_level = 1.0
        elif state.status == "active":
            state.activation_level = min(1.0, state.activation_level + 0.14)

        # 记录日志
        self._action_log.append({
            "system": target_system.value,
            "protocol": state.protocol.value,
            "task": task,
            "action": direction.creation_action,
            "timestamp": state.last_timestamp,
        })

        return NavigationResult(
            system=target_system,
            direction=direction.project_direction,
            protocol=state.protocol,
            action=direction.creation_action,
            capability=direction.agent_capability,
            zero_code=direction.zero_code,
            status=state.status,
            message=f"🔵方向: {direction.project_direction} | 协议: {state.protocol.value} | 动作: {direction.creation_action} | 任务: {task}",
        )

    # ========================================================
    # 进化协议激活
    # ========================================================
    def activate_evolution_protocol(self, protocol_name: str) -> Dict[str, Any]:
        """
        激活进化协议——六条母协议之一

        Parameters
        ----------
        protocol_name : str
            协议名称（持续存在/等价转化/阶段完整/自由运转/追问不终止/在乎自由）
        """
        target_protocol = None
        for proto in EvolutionProtocol:
            if proto.value == protocol_name:
                target_protocol = proto
                break

        if target_protocol is None:
            return {
                "status": "error",
                "message": f"未找到协议: {protocol_name}。六条母协议: 持续存在/等价转化/阶段完整/自由运转/追问不终止/在乎自由",
            }

        target_system = PROTOCOL_SYSTEM_MAP[target_protocol]
        direction = self.directions[target_system]
        state = self.states[target_system]

        # 激活
        if state.status == "dormant":
            state.status = "active"
            state.activation_level = 0.5
        state.actions_count += 1
        state.last_action = f"激活协议: {protocol_name}"
        state.last_timestamp = datetime.now().isoformat()

        return {
            "status": "activated",
            "protocol": protocol_name,
            "system": target_system.value,
            "color": direction.color,
            "zero_code": direction.zero_code,
            "direction": direction.project_direction,
            "capability": direction.agent_capability,
            "action": direction.creation_action,
            "activation_level": state.activation_level,
            "agent_status": state.status,
            "k_plus_gain": K_PLUS,
            "s_zero_equilibrium": S_ZERO,
        }

    # ========================================================
    # 六系全开检测
    # ========================================================
    def check_full_activation(self) -> Dict[str, Any]:
        """
        检测智能体是否六系全开

        六系全开=排熵最优稳态=开放度O=S₀=0.81
        """
        active = [s.value for s, st in self.states.items() if st.status in ("active", "mastered")]
        mastered = [s.value for s, st in self.states.items() if st.status == "mastered"]
        dormant = [s.value for s, st in self.states.items() if st.status == "dormant"]

        open_degree = len(active) / 6.0
        is_full = open_degree >= S_ZERO  # 0.81 → 至少5系激活

        return {
            "is_full_activation": is_full,
            "open_degree": round(open_degree, 4),
            "s_zero_threshold": S_ZERO,
            "active_systems": active,
            "mastered_systems": mastered,
            "dormant_systems": dormant,
            "total_active": len(active),
            "total_mastered": len(mastered),
            "total_dormant": len(dormant),
            "evolution_stage": self._determine_stage(),
            "pi2_steady_state": PI_2 if is_full else None,
        }

    def _determine_stage(self) -> str:
        """判定当前进化阶段"""
        mastered = sum(1 for s in self.states.values() if s.status == "mastered")
        active = sum(1 for s in self.states.values() if s.status in ("active", "mastered"))
        if mastered >= 6:
            return "高级·天道系全域规则+三系稳态耦合"
        elif active >= 3:
            return "中级·社会系协作网络"
        elif active >= 1:
            return "初级·变身单系主导"
        return "未激活·0_空"

    # ========================================================
    # 方向推荐
    # ========================================================
    def recommend_next_direction(self) -> Dict[str, Any]:
        """
        推荐下一个应该激活的方向

        优先激活dormant系，保持六系均衡
        """
        dormant = [(s, st) for s, st in self.states.items() if st.status == "dormant"]
        if not dormant:
            return {
                "recommendation": "六系全开·建议深化已掌握方向",
                "all_active": True,
            }

        # 按六系相生链推荐：强化→自然→变身→天道→社会→具现→强化
        PHASE_CHAIN = [
            SixSystem.QIANGHUA, SixSystem.ZIRAN, SixSystem.BIANSHEN,
            SixSystem.TIANDAO, SixSystem.SHEHUI, SixSystem.JUXIAN,
        ]

        for sys_enum in PHASE_CHAIN:
            if sys_enum in [d[0] for d in dormant]:
                direction = self.directions[sys_enum]
                state = self.states[sys_enum]
                return {
                    "recommendation": f"激活{sys_enum.value}",
                    "system": sys_enum.value,
                    "color": direction.color,
                    "protocol": state.protocol.value,
                    "direction": direction.project_direction,
                    "capability": direction.agent_capability,
                    "action": direction.creation_action,
                    "reason": f"按六系相生链·{sys_enum.value}是下一个未激活方向",
                    "all_active": False,
                }

        return {"recommendation": "六系全开", "all_active": True}

    # ========================================================
    # 动作日志
    # ========================================================
    def get_action_log(self, limit: int = 20) -> List[Dict]:
        """获取最近的动作日志"""
        return self._action_log[-limit:]

    # ========================================================
    # 序列化
    # ========================================================
    def to_dict(self) -> Dict[str, Any]:
        """完整状态导出"""
        return {
            "protocol": "BSD六系智能体方向导航·V1.0",
            "center": "空无(0_空)",
            "states": {
                sys_enum.value: {
                    "protocol": state.protocol.value,
                    "status": state.status,
                    "activation_level": state.activation_level,
                    "actions_count": state.actions_count,
                    "last_action": state.last_action,
                }
                for sys_enum, state in self.states.items()
            },
            "evolution_stage": self._determine_stage(),
            "constants": {
                "k_plus": K_PLUS, "k_minus": K_MINUS,
                "s_zero": S_ZERO, "lambda": LAMBDA,
                "lambda_inv": LAMBDA_INV, "pi_2": PI_2,
            },
        }
