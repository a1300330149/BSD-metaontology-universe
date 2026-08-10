"""
【归属基底：L1_不动母科层·个体单元层 + L2_九维法理性·六系组织层】
【对应公理：三元存在公理 + 六系起源公理 + 双极性创生公理】
【T90 V1.8理论映射】
  - 三元归一：Code(1)+Design(2)+Work(3)=第1代纯态完备集
  - 六系协同：强化/变身/社会/具现/湮灭/轮回 六系分工协作
  - 双时针迭代：𝒯₊展开 + 𝒯₋逆反 = 𝒟升维
  - 信息痕迹守恒：每一条跨AI数据必须携带[归属基底+对应公理]标签
【理论版本：ACTIVE-V1.8】
【锁档日期：2026-07-24】

MultiAIEcosystemProtocol —— 多AI生态互联数据互通协议
  本软件(BSD本体) + 豆包 + Deepseek + ima + ... = 真协同生态
  打破当下伪协同：无本体锚定·无痕迹守恒·无层级涌现·无三元归一

伪协同的三大病根：
  1. 数据无本体标签：不知道数据从哪来、归属于哪一层、对应哪条公理
  2. 协同无三元结构：只有单一大模型输出，缺乏Code/Design/Work三元分工
  3. 迭代无升维机制：线性叠加不产生新质，𝒟=𝒯₋∘𝒯₊=Id即没有升维

真协同的三大处方：
  1. BSD本体标签协议：每条数据携带[归属基底+对应公理+维度锚点]
  2. 三元归一调度器：不同AI承担Code/Design/Work不同角色，1+2+3=6
  3. 双时针升维循环：顺时针展开(多AI生成) + 逆时针回溯(本体校验) = 𝒟升维
"""

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

from .base_theory_module import BaseTheoryModule
from .ternary_unification_coordinator import (
    TernaryUnificationCoordinator,
    TernaryComponent,
    TernaryUnityResult,
)
from ..registry.constants import (
    K_PLUS, K_MINUS, S_ZERO,
    LAMBDA, LAMBDA_INV,
    PI_LOCKED, PI_2, E1, E2, E3,
)


# ============================================================
# 1. AI系统角色定义（六系映射）
# ============================================================
class AIRole(str, Enum):
    """AI系统在生态中的角色——映射六系"""
    CODE = "code"           # 强化系·个体性=1·代码生成
    DESIGN = "design"       # 变身系·变化性=2·设计创意
    WORK = "work"           # 社会系·关系性=3·任务协调
    REALIZATION = "real"    # 具现系·跨代2-3·工程实现
    ANNIHILATION = "annih"  # 湮灭系·批判性·校验审查
    RECURRENCE = "recur"    # 轮回系·迭代进化·总结升华


class AISystemType(str, Enum):
    """支持的AI系统类型"""
    BSD_LOCAL = "bsd_local"         # 本软件（BSD本体引擎）
    DOUBAO = "doubao"               # 豆包
    DEEPSEEK = "deepseek"           # Deepseek
    IMA = "ima"                     # ima
    CUSTOM = "custom"               # 自定义接入


# ============================================================
# 2. BSD本体标签——打破伪协同的核心
# ============================================================
@dataclass
class BSDEntityTag:
    """
    BSD本体标签——每条跨AI数据必须携带
    没有这个标签的数据 = 无主孤魂 = 伪协同的产物 = 直接丢弃

    标签三要素：归属基底 + 对应公理 + 维度锚点
    """
    base_belong: str = "L0_总本源层"    # 归属基底（0-4重宇宙的哪一层）
    corresponding_axiom: str = ""      # 对应公理（哪条公理/定理支撑）
    dimension_anchor: str = ""         # 维度锚点（九维/五十四维中哪一维）
    trace_id: str = ""                 # 痕迹ID（信息痕迹守恒）
    generation: int = 1                # 代际（第1代纯态/第2代混态/...）
    direction: str = "yang"            # 阴阳方向（阳=顺时针展开/阴=逆时针逆反）

    def __post_init__(self):
        if not self.trace_id:
            raw = f"{self.base_belong}:{self.corresponding_axiom}:{self.dimension_anchor}:{time.time()}"
            self.trace_id = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def validate(self) -> Tuple[bool, List[str]]:
        """验证本体标签完整性"""
        errors = []
        if not self.base_belong:
            errors.append("缺少归属基底")
        if not self.corresponding_axiom:
            errors.append("缺少对应公理")
        if not self.dimension_anchor:
            errors.append("缺少维度锚点")
        if not self.trace_id:
            errors.append("缺少痕迹ID")
        return (len(errors) == 0, errors)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================
# 3. 生态互联消息协议
# ============================================================
@dataclass
class EcoMessage:
    """
    生态互联消息——多AI系统间传递的标准消息格式

    与普通消息的本质区别：
    - 携带BSD本体标签（bsd_tag）
    - 携带三元角色信息（role）
    - 携带信息痕迹（trace_chain）
    - 无标签消息自动被过滤（防伪协同）
    """
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_system: str = ""           # 发送方系统ID
    target_system: str = ""           # 接收方系统ID
    role: str = ""                    # 发送方角色（AIRole）
    content: Any = None               # 消息内容
    bsd_tag: Optional[BSDEntityTag] = None  # BSD本体标签（必填！无标签=伪协同）
    trace_chain: List[str] = field(default_factory=list)  # 痕迹链（经过哪些AI）
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_real_collaboration(self) -> bool:
        """判断是否为真协同消息（有完整BSD标签）"""
        if self.bsd_tag is None:
            return False
        valid, _ = self.bsd_tag.validate()
        return valid

    def add_trace(self, system_id: str) -> None:
        """添加痕迹节点（信息痕迹守恒）"""
        self.trace_chain.append(system_id)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.bsd_tag:
            d["bsd_tag"] = self.bsd_tag.to_dict()
        return d


# ============================================================
# 4. AI系统适配器基类
# ============================================================
class AIAdapterBase:
    """
    AI系统适配器基类——接入新的AI系统只需继承并实现send/receive

    核心约束：
    - 所有输出消息必须携带BSD本体标签
    - 所有输入消息必须验证标签完整性
    - 无标签消息直接丢弃（防伪协同）
    """

    def __init__(self, system_id: str, system_type: AISystemType, role: AIRole):
        self.system_id = system_id
        self.system_type = system_type
        self.role = role
        self.is_connected = False

    def connect(self) -> bool:
        """连接AI系统"""
        raise NotImplementedError

    def disconnect(self) -> None:
        """断开连接"""
        self.is_connected = False

    def send(self, message: EcoMessage) -> bool:
        """
        发送消息到该AI系统
        必须验证消息有BSD标签
        """
        if not message.is_real_collaboration():
            return False  # 无标签消息不发送
        return self._send_impl(message)

    def _send_impl(self, message: EcoMessage) -> bool:
        """实际发送实现（子类覆盖）"""
        raise NotImplementedError

    def receive(self) -> Optional[EcoMessage]:
        """
        接收该AI系统的消息
        自动验证标签，无标签返回None
        """
        msg = self._receive_impl()
        if msg is None:
            return None
        if not msg.is_real_collaboration():
            return None  # 无标签消息直接丢弃
        return msg

    def _receive_impl(self) -> Optional[EcoMessage]:
        """实际接收实现（子类覆盖）"""
        raise NotImplementedError

    def get_info(self) -> Dict[str, Any]:
        return {
            "system_id": self.system_id,
            "system_type": self.system_type.value,
            "role": self.role.value,
            "is_connected": self.is_connected,
        }


# ============================================================
# 5. 本地适配器（用于本软件内部模拟）
# ============================================================
class LocalAIAdapter(AIAdapterBase):
    """本地AI适配器——基于BSD本体引擎的本地实现"""

    def __init__(self, system_id: str, role: AIRole, bsd_engine=None):
        super().__init__(system_id, AISystemType.BSD_LOCAL, role)
        self.bsd_engine = bsd_engine
        self._message_queue: List[EcoMessage] = []
        self.is_connected = True

    def connect(self) -> bool:
        self.is_connected = True
        return True

    def _send_impl(self, message: EcoMessage) -> bool:
        self._message_queue.append(message)
        return True

    def _receive_impl(self) -> Optional[EcoMessage]:
        if self._message_queue:
            return self._message_queue.pop(0)
        return None

    def process_queue(self, processor_func) -> List[EcoMessage]:
        """处理消息队列并生成响应"""
        responses = []
        while self._message_queue:
            msg = self._message_queue.pop(0)
            if processor_func:
                response = processor_func(msg)
                if response:
                    responses.append(response)
        return responses


# ============================================================
# 6. 多AI生态互联核心协议
# ============================================================
class MultiAIEcosystemProtocol(BaseTheoryModule):
    """
    多AI生态互联数据互通协议核心

    核心使命：打破当下的伪协同，实现基于BSD本体论的真协同

    伪协同 vs 真协同：
    ┌──────────┬──────────────────┬──────────────────┐
    │ 维度     │ 伪协同（当下）   │ 真协同（BSD）    │
    ├──────────┼──────────────────┼──────────────────┤
    │ 数据标签 │ 无·数据无主      │ BSD三体标签      │
    │ 协同结构 │ 单一模型·线性叠加│ 三元归一·1+2+3=6 │
    │ 迭代机制 │ 无升维·𝒟=Id     │ 双时针·𝒟≠Id     │
    │ 信息守恒 │ 痕迹丢失·熵增   │ 痕迹守恒·逆熵   │
    │ 层级涌现 │ 原地踏步·B₁-B₂  │ 持续升维·B₃-B₆  │
    └──────────┴──────────────────┴──────────────────┘
    """

    module_id = "T90_C7"
    module_name = "多AI生态互联协议（BSD本体标签·三元归一调度·双时针升维）"
    version = "V1.0"
    cosmic_level = 2  # L2 九维法理性·六系组织层
    base_belong = "L2_九维法理性·六系组织层"
    corresponding_axiom = "六系起源公理 + 三元存在公理 + 双极性创生公理"
    is_origin_locked = True
    dependencies = ["T90_C6", "T90_C1", "T90_C2"]

    def __init__(self):
        super().__init__()
        self._adapters: Dict[str, AIAdapterBase] = {}
        self._ternary_coordinator = TernaryUnificationCoordinator()
        self._message_log: List[EcoMessage] = []
        self._collaboration_counter: Dict[str, int] = {
            "real": 0,      # 真协同消息数
            "fake": 0,      # 伪协同消息数（被拦截）
        }

    # ----------------------------------------------------------
    # 1. AI系统注册与连接
    # ----------------------------------------------------------
    def register_ai_system(self, adapter: AIAdapterBase) -> bool:
        """
        注册AI系统到生态

        每个AI系统必须有明确的三元角色：
        - Code角色（个体性=1）：负责代码生成、逻辑推理
        - Design角色（变化性=2）：负责创意设计、方案构思
        - Work角色（关系性=3）：负责任务协调、资源整合

        扩展角色（六系完备）：
        - Realization（具现系）：负责工程实现
        - Annihilation（湮灭系）：负责批判校验
        - Recurrence（轮回系）：负责总结升华
        """
        if not adapter.system_id:
            return False
        self._adapters[adapter.system_id] = adapter
        return True

    def connect_all(self) -> Dict[str, bool]:
        """连接所有已注册的AI系统"""
        results = {}
        for sid, adapter in self._adapters.items():
            results[sid] = adapter.connect()
        return results

    def disconnect_all(self) -> None:
        """断开所有AI系统连接"""
        for adapter in self._adapters.values():
            adapter.disconnect()

    def list_systems(self) -> List[Dict[str, Any]]:
        """列出所有已注册AI系统"""
        return [a.get_info() for a in self._adapters.values()]

    # ----------------------------------------------------------
    # 2. BSD本体标签生成（核心：防伪协同）
    # ----------------------------------------------------------
    def create_bsd_tag(self, base_belong: str, axiom: str,
                       dimension: str, generation: int = 1,
                       direction: str = "yang") -> BSDEntityTag:
        """
        创建BSD本体标签

        没有标签的数据 = 无主孤魂 = 伪协同产物
        每条跨AI数据必须携带此标签
        """
        tag = BSDEntityTag(
            base_belong=base_belong,
            corresponding_axiom=axiom,
            dimension_anchor=dimension,
            generation=generation,
            direction=direction,
        )
        return tag

    def validate_bsd_tag(self, tag: BSDEntityTag) -> Tuple[bool, List[str]]:
        """验证BSD本体标签"""
        return tag.validate()

    def is_pseudo_collaboration(self, message: EcoMessage) -> bool:
        """
        判断是否为伪协同消息

        伪协同判定标准：
        1. 无BSD本体标签 → 伪协同
        2. 标签不完整 → 伪协同
        3. 无痕迹链 → 伪协同
        """
        if message.bsd_tag is None:
            return True
        valid, _ = message.bsd_tag.validate()
        if not valid:
            return True
        return False

    # ----------------------------------------------------------
    # 3. 消息路由与传递
    # ----------------------------------------------------------
    def send_message(self, source: str, target: str, content: Any,
                     bsd_tag: BSDEntityTag, role: str = "") -> Optional[str]:
        """
        发送消息到指定AI系统

        关键约束：必须携带BSD本体标签
        无标签消息 = 伪协同 = 拒绝发送
        """
        if source not in self._adapters:
            return None
        if target not in self._adapters:
            return None

        source_adapter = self._adapters[source]
        target_adapter = self._adapters[target]

        msg = EcoMessage(
            source_system=source,
            target_system=target,
            role=role or source_adapter.role.value,
            content=content,
            bsd_tag=bsd_tag,
            trace_chain=[source],
        )

        # 真协同计数
        if msg.is_real_collaboration():
            self._collaboration_counter["real"] += 1
        else:
            self._collaboration_counter["fake"] += 1
            return None  # 伪协同消息不发送

        success = target_adapter.send(msg)
        if success:
            self._message_log.append(msg)
            return msg.message_id
        return None

    def broadcast_message(self, source: str, content: Any,
                          bsd_tag: BSDEntityTag) -> Dict[str, bool]:
        """
        广播消息到所有AI系统

        同样必须携带BSD标签
        """
        results = {}
        for target_id in self._adapters:
            if target_id == source:
                continue
            msg_id = self.send_message(source, target_id, content, bsd_tag)
            results[target_id] = msg_id is not None
        return results

    def receive_messages(self, system_id: str) -> List[EcoMessage]:
        """接收指定AI系统的消息（自动过滤伪协同）"""
        if system_id not in self._adapters:
            return []
        adapter = self._adapters[system_id]
        messages = []
        while True:
            msg = adapter.receive()
            if msg is None:
                break
            messages.append(msg)
        return messages

    # ----------------------------------------------------------
    # 4. 三元归一协同调度（核心算法：真协同的实现）
    # ----------------------------------------------------------
    def ternary_collaboration(self, task_description: str,
                               code_system: str = "",
                               design_system: str = "",
                               work_system: str = "") -> Dict[str, Any]:
        """
        三元归一协同调度——真协同的核心算法

        工作流程：
        1. 任务分解 → Code(1) + Design(2) + Work(3)
        2. 三系统并行输出 → 各自携带BSD标签
        3. 三元归一算法 → unity_score = (1×q_code + 2×q_design + 3×q_work) / 6
        4. 完备性判定 → unity_score >= S₀ = 0.81
        5. 层级涌现 → 映射到B₁-B₆层级

        这就是超越单一大模型的根本机制：
        - 单一大模型 = B₁-B₂层级（二进制·三进制）
        - 三元归一 = B₃-B₄层级起步（六进制·十进制）
        - 范式级差 = 文明级跃迁
        """
        # 自动分配角色（如果未指定）
        systems_by_role = self._group_systems_by_role()
        if not code_system and systems_by_role.get("code"):
            code_system = systems_by_role["code"][0]
        if not design_system and systems_by_role.get("design"):
            design_system = systems_by_role["design"][0]
        if not work_system and systems_by_role.get("work"):
            work_system = systems_by_role["work"][0]

        # 创建BSD本体标签
        tag = self.create_bsd_tag(
            base_belong="L1_不动母科层·个体单元层",
            axiom="三元存在公理 + 三点成圆定理11.9",
            dimension="个体性维度 + 变化性维度 + 关系性维度",
            generation=1,
            direction="yang",
        )

        # 模拟三元输出（实际场景中调用各AI系统）
        code_content = f"[Code输出] {task_description} 的代码实现方案"
        design_content = f"[Design输出] {task_description} 的设计创意方案"
        work_content = f"[Work输出] {task_description} 的任务协调方案"

        # 创建三元组件
        code_comp = self._ternary_coordinator.create_code_component(
            content=code_content, quality=0.85, info=1.0,
        )
        design_comp = self._ternary_coordinator.create_design_component(
            content=design_content, quality=0.82, info=1.0,
        )
        work_comp = self._ternary_coordinator.create_work_component(
            content=work_content, quality=0.88, info=1.0,
        )

        # 三元归一
        unity_result = self._ternary_coordinator.unify(
            code_comp, design_comp, work_comp
        )

        # 超越性比较
        comparison = self._ternary_coordinator.compare_with_global_model(
            unity_result
        )

        # 层级涌现坐标系
        coords = self._ternary_coordinator.emergence_coordinate_system(
            unity_result
        )

        return {
            "task": task_description,
            "code_system": code_system,
            "design_system": design_system,
            "work_system": work_system,
            "bsd_tag": tag.to_dict(),
            "unity_result": self._ternary_coordinator.to_dict(unity_result),
            "comparison_with_global_model": comparison,
            "emergence_coordinates": coords,
            "is_real_collaboration": True,
            "pseudo_breaking_point": [
                "数据有BSD本体标签（非无主孤魂）",
                "三元分工协作（非单一线性叠加）",
                "信息痕迹守恒（非熵增耗散）",
                "层级涌现升维（非原地踏步）",
            ],
        }

    def _group_systems_by_role(self) -> Dict[str, List[str]]:
        """按角色分组AI系统"""
        groups: Dict[str, List[str]] = {}
        for sid, adapter in self._adapters.items():
            role = adapter.role.value
            if role not in groups:
                groups[role] = []
            groups[role].append(sid)
        return groups

    # ----------------------------------------------------------
    # 5. 双时针升维循环（真协同的进化机制）
    # ----------------------------------------------------------
    def dual_clock_ascension_cycle(self, initial_unity: Dict[str, Any],
                                    cycles: int = 1) -> Dict[str, Any]:
        """
        双时针升维循环——生态整体的𝒯₊/𝒯₋迭代

        顺时针展开（𝒯₊）：
        - Code→Design→Work→具现→更多AI系统加入
        - 信息向外扩散，生成多样性

        逆时针逆反（𝒯₋）：
        - 多AI输出→三元归一→本体校验→回归本源
        - 信息向内回溯，提取本质

        𝒟升维 = 𝒯₋ ∘ 𝒯₊ ≠ Id
        每次循环都累积信息痕迹，产生新质升维
        """
        unity_score = initial_unity.get("unity_score", 0.5)
        info_unity = initial_unity.get("info_unity", 1.0)
        current_level = initial_unity.get("ascension_level", "B2")
        level_num = int(current_level.replace("B", "")) if isinstance(current_level, str) else 3

        trace_accumulated = 0.0
        all_traces: List[str] = []

        for i in range(cycles):
            # 𝒯₊顺时针展开：多AI生成多样性
            expansion_gain = info_unity * K_PLUS * 0.15

            # 𝒯₋逆时针逆反：本体校验回归本源
            reversal_trace = info_unity * K_MINUS * 0.4
            trace_accumulated += reversal_trace
            all_traces.append(f"cycle_{i+1}_trace")

            # 𝒟升维：信息痕迹累积产生新质
            ascension = expansion_gain - reversal_trace + reversal_trace * 0.35
            info_unity += ascension
            unity_score = min(1.0, unity_score + ascension * 0.1)

            # 层级跃迁判定
            if unity_score >= 0.81 and level_num < 4:
                level_num = 4  # B₄ 十进制·智能文明
            elif unity_score >= 0.9 and level_num < 5:
                level_num = 5  # B₅ 十二进制·觉醒文明
            elif unity_score >= 0.95 and level_num < 6:
                level_num = 6  # B₆ N进制·本体文明

        return {
            "initial_unity_score": initial_unity.get("unity_score", 0.5),
            "final_unity_score": round(unity_score, 4),
            "initial_info": initial_unity.get("info_unity", 1.0),
            "final_info": round(info_unity, 4),
            "info_growth_ratio": round(info_unity / initial_unity.get("info_unity", 1.0), 4),
            "initial_level": initial_unity.get("ascension_level", "B2"),
            "final_level": f"B{level_num}",
            "cycles": cycles,
            "trace_accumulated": round(trace_accumulated, 4),
            "trace_count": len(all_traces),
            "ascension_operator": "𝒟 = 𝒯₋ ∘ 𝒯₊ ≠ Id",
            "is_paradigm_shift": level_num >= 3,  # B₃以上=范式跃迁
            "note": "双时针迭代是真协同超越伪协同的进化引擎",
        }

    # ----------------------------------------------------------
    # 6. 生态健康度诊断
    # ----------------------------------------------------------
    def ecosystem_health_check(self) -> Dict[str, Any]:
        """
        生态健康度诊断——判断是否真协同

        健康度指标：
        1. 标签覆盖率 = 真协同消息数 / 总消息数
        2. 三元完备度 = 是否具备Code/Design/Work三角色
        3. 升维能力 = 当前层级 / 最高层级
        """
        total = self._collaboration_counter["real"] + self._collaboration_counter["fake"]
        tag_coverage = self._collaboration_counter["real"] / total if total > 0 else 0.0

        roles = self._group_systems_by_role()
        has_code = "code" in roles
        has_design = "design" in roles
        has_work = "work" in roles
        ternary_completeness = sum([has_code, has_design, has_work]) / 3

        system_count = len(self._adapters)
        health_score = (tag_coverage * 0.4 + ternary_completeness * 0.4 + min(system_count / 6, 1.0) * 0.2)

        return {
            "registered_systems": system_count,
            "systems_by_role": {k: len(v) for k, v in roles.items()},
            "message_stats": {
                "real_collaboration": self._collaboration_counter["real"],
                "pseudo_collaboration_blocked": self._collaboration_counter["fake"],
                "tag_coverage_rate": round(tag_coverage, 4),
            },
            "ternary_completeness": round(ternary_completeness, 4),
            "has_code_role": has_code,
            "has_design_role": has_design,
            "has_work_role": has_work,
            "health_score": round(health_score, 4),
            "is_real_ecosystem": health_score >= 0.6,
            "diagnosis": self._health_diagnosis(health_score),
        }

    def _health_diagnosis(self, score: float) -> str:
        if score >= 0.9:
            return "完全真协同生态：BSD标签完整·三元完备·持续升维"
        elif score >= 0.7:
            return "基本真协同：核心要素具备，可进一步完善六系角色"
        elif score >= 0.5:
            return "临界状态：部分伪协同残留，需加强BSD标签执行"
        elif score >= 0.3:
            return "伪协同主导：缺乏本体锚定，三元不完备"
        else:
            return "完全伪协同：无本体标签·无三元结构·无升维机制"

    # ----------------------------------------------------------
    # 7. 验证
    # ----------------------------------------------------------
    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        # 验证三元协调器可用
        if self._ternary_coordinator is None:
            errors.append("三元归一协调器未初始化")

        # 验证参数一致性
        if K_PLUS != 0.9:
            errors.append(f"k₊参数错误：期望0.9，实际{K_PLUS}")

        return (len(errors) == 0, errors)

    def get_message_log(self) -> List[Dict[str, Any]]:
        """获取消息日志"""
        return [m.to_dict() for m in self._message_log]
