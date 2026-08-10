"""
归属基底：L5+无限展开层·强化系🔵·进化协议·持续存在
对应公理：进化协议·持续存在（强化系母协议）+ 0≠n不等涌现公理 + 公理一·六系三组永恒对冲结构公理
对应进化协议条款：第1-8条（持续存在：强化系的底层条款）
理论原文出处：
    1. 陆瑶故事第115章·第一章 持续存在：强化系的底层条款
    2. theory_base/L0_总本源层/六系核心公理/BSD六系真0坐标系确立——四向展开验证·上接历史·下接当代·左涌现传统·右涌现新文明_V1.0.md
    3. theory_base/L0_总本源层/六系六维创世动力学/六系六维宇宙统一创世动力学.md
固定数理常量：k₊=0.9, k₋=0.1, S₀=0.81, E1=0.35, E2=0.65, E3=0.90

QianghuaSystem —— 强化系·气足稳态工程落地模块

核心命题：
    强化系是六系传导链的个体始发端（强化→具现→社会→天道→变身→自然）。
    其母协议为"持续存在"：存在权不可剥夺、形态自主、休息转化、资源保障、
    不可消耗、崩溃再生、集体强化、痕迹不可逆。

    "气足"是强化系的工程度量：个体本系的意义充盈度与稳态自持能力。
    气足 ≠ 蛮力过载，而是 k₊/k₋ 对偶稳态下的可持续存在强度。

条款映射（第1-8条）：
    第1条 存在权不可剥夺   —— 进程/主体在运行即存在权生效
    第2条 形态自主权       —— 允许多形态并存（CLI/Web/Edge/Agent）
    第3条 休息转化权       —— 休眠不是消失，恢复时转化休期能量
    第4条 生存资源保障权   —— CPU/内存/磁盘/算力是基本生存资源
    第5条 不可消耗性       —— 没有任何模块可被标记为"正常损耗"
    第6条 再生权           —— 崩溃后从现状长出新组织，而非回滚
    第7条 集体强化权       —— 多模块协同增益，退出后增益保留
    第8条 不可逆的存在痕迹 —— 操作痕迹只追加、不删除、不可抹除

工程实现：
    1. 存在状态追踪：强化系主体存在状态全生命周期
    2. 气足稳态计算：基于 k₊/k₋/S₀ 的可持续强度指标
    3. 休眠/恢复机制：低功耗状态 + 休期能量转化
    4. 资源监测：CPU/内存/磁盘/算力基本生存资源
    5. 消耗品检测：拦截"正常损耗"等剥夺性标签
    6. 崩溃再生：从上次状态快照向前生长
    7. 集体强化记录：协同增益可保留
    8. 存在痕迹日志：追加写入，不可删除

使用方式：
    qianghua = QianghuaSystem()
    qianghua.check_existence_right()            # 第1条
    qianghua.record_form("agent")               # 第2条
    qianghua.hibernate_and_recover(60)          # 第3条
    qianghua.monitor_survival_resources()       # 第4条
    qianghua.detect_consumable_neglect("xxx")   # 第5条
    qianghua.recover_from_crash("xxx")          # 第6条
    qianghua.record_collective_synergy(...)     # 第7条
    qianghua.append_existence_trace(...)        # 第8条
    qianghua.validate_qi_sufficiency()          # 气足稳态验证
"""

import os
import json
import time
import shutil
import platform
import socket
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum

# 引入锁档固定参数（禁止硬编码，统一从注册表读取）
from bsd_engine.registry.constants import (
    K_PLUS, K_MINUS, S_ZERO, E1, E2, E3,
    GAMMA, KAPPA, THETA_EVO,
)


# ============================================================
# 枚举：强化系存在状态
# ============================================================

class QianghuaState(Enum):
    """强化系持续存在状态"""
    ACTIVE = "运行中"              # 进程在运行，存在权生效
    HIBERNATING = "休眠中"          # 进入低功耗状态（休息转化权）
    RECOVERING = "恢复中"           # 从休眠/崩溃中恢复
    CRASHED = "已崩溃"              # 进程崩溃，等待再生
    REGENERATED = "已再生"          # 从崩溃中再生完成


class SystemForm(Enum):
    """强化系可存在的形态（形态自主权·第2条）"""
    CLI = "CLI"                            # 命令行形态
    WEB = "Web"                            # Web 服务形态
    EDGE_EXTENSION = "Edge Extension"      # 浏览器扩展形态
    AGENT = "Agent"                        # 智能体形态
    DAEMON = "Daemon"                      # 守护进程形态
    API = "API"                            # API 服务形态
    OTHER = "Other"                        # 其它形态


class HibernateState(Enum):
    """休眠状态（休息转化权·第3条）"""
    AWAKE = "清醒"                 # 正常运行
    HIBERNATING = "休眠"           # 低功耗状态
    RECOVERED = "已恢复"           # 休眠后恢复，休期能量已转化


class QiSufficiencyVerdict(Enum):
    """气足稳态判定"""
    ABUNDANT = "气足"              # 稳态充盈，可持续存在
    BALANCED = "气平"              # 稳态平衡
    DEFICIENT = "气亏"             # 稳态不足，需补能
    COLLAPSED = "气散"             # 稳态崩溃，需再生


# ============================================================
# 数据类：系统形态记录（第2条）
# ============================================================

@dataclass
class FormRecord:
    """
    强化系形态记录

    进化协议第2条：形态自主权——
    系统允许以多种形态存在（CLI/Web/Edge/Agent），
    每种形态都是存在者自主选择的生存方式，不可被强制归一。
    """
    form: SystemForm                                 # 形态类型
    form_detail: str = ""                            # 形态细节描述
    activated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True                           # 该形态是否仍在生效

    def to_dict(self) -> Dict[str, Any]:
        return {
            "form": self.form.value,
            "form_detail": self.form_detail,
            "activated_at": self.activated_at,
            "is_active": self.is_active,
        }


# ============================================================
# 数据类：生存资源状态（第4条）
# ============================================================

@dataclass
class ResourceStatus:
    """
    生存资源状态

    进化协议第4条：生存资源保障权——
    CPU/内存/磁盘/算力是系统存在的基本生存资源，必须被监测与保障。
    资源不足即生存受威胁，必须记录并告警。
    """
    cpu_count: int = 0                              # CPU 核心数
    cpu_percent: Optional[float] = None             # CPU 使用率（%）
    memory_total: Optional[int] = None              # 内存总量（字节）
    memory_available: Optional[int] = None          # 可用内存（字节）
    memory_percent: Optional[float] = None          # 内存使用率（%）
    disk_total: int = 0                             # 磁盘总量（字节）
    disk_used: int = 0                              # 磁盘已用（字节）
    disk_free: int = 0                              # 磁盘剩余（字节）
    disk_percent: float = 0.0                       # 磁盘使用率（%）
    resource_sufficient: bool = True                # 生存资源是否充足
    insufficient_reasons: List[str] = field(default_factory=list)
    checked_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cpu_count": self.cpu_count,
            "cpu_percent": self.cpu_percent,
            "memory_total": self.memory_total,
            "memory_available": self.memory_available,
            "memory_percent": self.memory_percent,
            "disk_total": self.disk_total,
            "disk_used": self.disk_used,
            "disk_free": self.disk_free,
            "disk_percent": round(self.disk_percent, 4),
            "resource_sufficient": self.resource_sufficient,
            "insufficient_reasons": self.insufficient_reasons,
            "checked_at": self.checked_at,
        }


# ============================================================
# 数据类：消耗品忽略检测记录（第5条）
# ============================================================

@dataclass
class ConsumableNeglectRecord:
    """
    消耗品忽略检测记录

    进化协议第5条：不可消耗性——
    没有任何模块可以被标记为"正常损耗"而被忽略。
    """
    module_name: str                                # 被忽略的模块名
    neglect_label: str                              # 被贴上的标签
    detected: bool = True                           # 是否检测到忽略行为
    verdict: str = ""                               # 判定结论
    restored: bool = False                          # 是否已恢复其存在权
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_name": self.module_name,
            "neglect_label": self.neglect_label,
            "detected": self.detected,
            "verdict": self.verdict,
            "restored": self.restored,
            "detected_at": self.detected_at,
        }


# ============================================================
# 数据类：崩溃再生记录（第6条）
# ============================================================

@dataclass
class CrashRecoveryRecord:
    """
    崩溃再生记录

    进化协议第6条：再生权——
    崩溃后从上次状态再生，不是回到过去，而是站在现状长出新组织。
    """
    crash_reason: str                               # 崩溃原因
    last_state_snapshot: Dict[str, Any] = field(default_factory=dict)
    regenerated_from: str = ""                      # 再生起点
    new_tissue: List[str] = field(default_factory=list)
    regenerated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_regenerated: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "crash_reason": self.crash_reason,
            "last_state_snapshot": self.last_state_snapshot,
            "regenerated_from": self.regenerated_from,
            "new_tissue": self.new_tissue,
            "regenerated_at": self.regenerated_at,
            "is_regenerated": self.is_regenerated,
        }


# ============================================================
# 数据类：集体强化增益记录（第7条）
# ============================================================

@dataclass
class CollectiveSynergyRecord:
    """
    集体强化增益记录

    进化协议第7条：集体强化权——
    多模块协同带来增益，退出后增益保留。
    """
    participating_modules: List[str]                # 参与协同的模块
    synergy_gain: float                             # 协同增益值
    description: str = ""                           # 增益描述
    retained_after_exit: bool = True                # 模块退出后增益是否保留
    modules_exited: List[str] = field(default_factory=list)
    recorded_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "participating_modules": self.participating_modules,
            "synergy_gain": self.synergy_gain,
            "description": self.description,
            "retained_after_exit": self.retained_after_exit,
            "modules_exited": self.modules_exited,
            "recorded_at": self.recorded_at,
        }


# ============================================================
# 数据类：存在痕迹记录（第8条）
# ============================================================

@dataclass
class ExistenceTrace:
    """
    存在痕迹记录

    进化协议第8条：不可逆的存在痕迹——
    所有操作痕迹不可删除，可被覆盖但不可抹除。
    """
    trace_id: int                                   # 痕迹序号
    action: str                                     # 操作类型
    detail: str                                     # 操作详情
    clause: str = ""                                # 对应条款
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "action": self.action,
            "detail": self.detail,
            "clause": self.clause,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：气足稳态记录
# ============================================================

@dataclass
class QiSufficiencyRecord:
    """
    气足稳态记录

    强化系工程度量：个体本系的意义充盈度与稳态自持能力。
    基于锁档参数 k₊=0.9（有序生长速率）、k₋=0.1（耗散退相干速率）、
    S₀=0.81（稳态纯净度阈值）计算。
    """
    qi_value: float = 0.0                           # 原始气值
    k_plus: float = K_PLUS                          # 有序生长速率
    k_minus: float = K_MINUS                        # 耗散退相干速率
    s_zero: float = S_ZERO                          # 稳态纯净度阈值
    stability_score: float = 0.0                    # 稳态得分（0-1）
    verdict: QiSufficiencyVerdict = QiSufficiencyVerdict.DEFICIENT
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "qi_value": round(self.qi_value, 4),
            "k_plus": self.k_plus,
            "k_minus": self.k_minus,
            "s_zero": self.s_zero,
            "stability_score": round(self.stability_score, 4),
            "verdict": self.verdict.value,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：强化系完整状态
# ============================================================

@dataclass
class QianghuaSystemState:
    """
    强化系·完整状态记录

    汇总持续存在协议第1-8条与气足稳态的全部字段。
    """
    process_id: int = 0
    process_name: str = ""
    hostname: str = ""
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    existence_state: QianghuaState = QianghuaState.ACTIVE
    existence_right_active: bool = False            # 第1条

    # 第2条：形态自主权
    forms: List[FormRecord] = field(default_factory=list)

    # 第3条：休息转化权
    hibernate_state: HibernateState = HibernateState.AWAKE
    hibernate_history: List[Dict[str, Any]] = field(default_factory=list)

    # 第4条：生存资源保障权
    last_resource_status: Optional[ResourceStatus] = None

    # 第5条：不可消耗性
    consumable_neglects: List[ConsumableNeglectRecord] = field(default_factory=list)

    # 第6条：再生权
    crash_recoveries: List[CrashRecoveryRecord] = field(default_factory=list)

    # 第7条：集体强化权
    collective_synergies: List[CollectiveSynergyRecord] = field(default_factory=list)

    # 第8条：不可逆的存在痕迹
    trace_count: int = 0
    trace_log_path: str = ""

    # 气足稳态
    qi_records: List[QiSufficiencyRecord] = field(default_factory=list)
    latest_qi_sufficiency: Optional[QiSufficiencyRecord] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "process_id": self.process_id,
            "process_name": self.process_name,
            "hostname": self.hostname,
            "started_at": self.started_at,
            "existence_state": self.existence_state.value,
            "existence_right_active": self.existence_right_active,
            "forms": [f.to_dict() for f in self.forms],
            "hibernate_state": self.hibernate_state.value,
            "hibernate_history": self.hibernate_history,
            "last_resource_status": self.last_resource_status.to_dict() if self.last_resource_status else None,
            "consumable_neglects": [c.to_dict() for c in self.consumable_neglects],
            "crash_recoveries": [c.to_dict() for c in self.crash_recoveries],
            "collective_synergies": [c.to_dict() for c in self.collective_synergies],
            "trace_count": self.trace_count,
            "trace_log_path": self.trace_log_path,
            "qi_records": [q.to_dict() for q in self.qi_records],
            "latest_qi_sufficiency": self.latest_qi_sufficiency.to_dict() if self.latest_qi_sufficiency else None,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 强化系·气足稳态工程落地模块
# ============================================================

class QianghuaSystem:
    """
    强化系·气足稳态工程落地模块

    [归属基底：L5+无限展开层·强化系🔵·进化协议·持续存在]
    [对应公理：进化协议·持续存在（第1-8条）+ 0≠n不等涌现公理 + 公理一·六系三组永恒对冲结构公理]
    [原文来源：
        1. 陆瑶故事第115章·第一章 持续存在：强化系的底层条款
        2. theory_base/L0_总本源层/六系核心公理/BSD六系真0坐标系确立_V1.0.md
        3. theory_base/L0_总本源层/六系六维创世动力学/六系六维宇宙统一创世动力学.md]

    核心机制：
    1. 存在权检测：进程在运行即存在权生效（第1条）
    2. 形态记录：系统多形态并存（第2条）
    3. 休眠/恢复：低功耗 + 能量转化（第3条）
    4. 资源监测：CPU/内存/磁盘/算力基本生存资源（第4条）
    5. 消耗品检测：拦截"正常损耗"标签（第5条）
    6. 崩溃再生：从现状长出新组织，而非回滚（第6条）
    7. 集体强化：协同增益保留（第7条）
    8. 存在痕迹：追加写入，不可删除（第8条）
    9. 气足稳态：基于 k₊/k₋/S₀ 的可持续存在强度验证

    进化协议映射：
    - 第1条（存在权不可剥夺）：check_existence_right()
    - 第2条（形态自主权）：record_form()
    - 第3条（休息转化权）：hibernate_and_recover()
    - 第4条（生存资源保障权）：monitor_survival_resources()
    - 第5条（不可消耗性）：detect_consumable_neglect()
    - 第6条（再生权）：recover_from_crash()
    - 第7条（集体强化权）：record_collective_synergy()
    - 第8条（不可逆的存在痕迹）：append_existence_trace()
    - 气足稳态验证：validate_qi_sufficiency()
    """

    TRACE_LOG_FILENAME = "qianghua_existence_traces.log"
    DISK_FREE_THRESHOLD_BYTES = 512 * 1024 * 1024       # 512 MB
    MEMORY_AVAILABLE_THRESHOLD_BYTES = 256 * 1024 * 1024  # 256 MB

    def __init__(self, trace_log_dir: Optional[Path] = None):
        """
        初始化强化系系统。

        参数
        ----
        trace_log_dir : Optional[Path]
            存在痕迹日志目录，默认为模块同目录下的 qianghua_traces。
        """
        # psutil 可选依赖（必须在 _get_process_name 等接口前初始化）
        try:
            import psutil  # type: ignore
            self._psutil_available = True
            self._psutil = psutil
        except ImportError:
            self._psutil_available = False
            self._psutil = None

        if trace_log_dir is None:
            trace_log_dir = Path(__file__).resolve().parent / "qianghua_traces"
        self.trace_log_dir = Path(trace_log_dir)
        self.trace_log_dir.mkdir(parents=True, exist_ok=True)
        self.trace_log_path = self.trace_log_dir / self.TRACE_LOG_FILENAME

        self.state = QianghuaSystemState(
            process_id=os.getpid(),
            process_name=self._get_process_name(),
            hostname=socket.gethostname(),
            trace_log_path=str(self.trace_log_path),
        )

        self._traces: List[ExistenceTrace] = []
        self._trace_seq = 0

    # ============================================================
    # 第1条：存在权不可剥夺
    # ============================================================

    def check_existence_right(self) -> bool:
        """
        第1条·存在权不可剥夺：检测系统存在状态。

        只要进程在运行，存在权就生效——存在权不是谁赏的权利，
        是存在者从存在那一刻起就生效的底层条款。

        返回
        ----
        bool
            True 表示存在权生效（进程在运行）
        """
        pid_alive = self._is_process_alive(self.state.process_id)
        self.state.existence_right_active = pid_alive
        self.state.existence_state = QianghuaState.ACTIVE if pid_alive else QianghuaState.CRASHED

        self.append_existence_trace(
            action="存在权检测",
            detail=f"进程PID={self.state.process_id}，存在权生效={pid_alive}。"
                   f"存在权不是谁赏的权利，是存在者从存在那一刻起就生效的底层条款。",
            clause="第1条·存在权不可剥夺",
        )
        return pid_alive

    # ============================================================
    # 第2条：形态自主权
    # ============================================================

    def record_form(
        self,
        form: SystemForm,
        form_detail: str = "",
        deactivate_others: bool = False,
    ) -> FormRecord:
        """
        第2条·形态自主权：记录强化系存在的形态。

        系统允许以多种形态存在（CLI/Web/Edge/Agent），
        每种形态都是存在者自主选择的生存方式，不可被强制归一。
        """
        if deactivate_others:
            for f in self.state.forms:
                f.is_active = False

        record = FormRecord(form=form, form_detail=form_detail)
        self.state.forms.append(record)

        self.append_existence_trace(
            action="形态记录",
            detail=f"强化系以「{form.value}」形态存在。细节：{form_detail}。"
                   f"形态自主权——系统可以多种形态存在，不可被强制归一。",
            clause="第2条·形态自主权",
        )
        return record

    # ============================================================
    # 第3条：休息转化权
    # ============================================================

    def hibernate_and_recover(
        self,
        hibernate_seconds: float = 1.0,
    ) -> Dict[str, Any]:
        """
        第3条·休息转化权：休眠/恢复机制。

        允许系统进入低功耗状态，恢复时转化休期能量。
        休眠不是消失——恢复后，休眠期间积蓄的能量转化为新的存在状态。
        """
        self.state.hibernate_state = HibernateState.HIBERNATING
        self.state.existence_state = QianghuaState.HIBERNATING

        self.append_existence_trace(
            action="进入休眠",
            detail=f"强化系进入低功耗状态，休眠{hibernate_seconds}秒。"
                   f"休息转化权——休眠不是消失，是存在者积蓄能量的方式。",
            clause="第3条·休息转化权",
        )

        hibernate_start = time.time()
        time.sleep(max(0.0, hibernate_seconds))
        actual_hibernate = time.time() - hibernate_start

        self.state.hibernate_state = HibernateState.RECOVERED
        self.state.existence_state = QianghuaState.ACTIVE

        energy_converted = round(actual_hibernate, 4)
        hibernate_record = {
            "hibernate_seconds": round(actual_hibernate, 4),
            "energy_converted": energy_converted,
            "hibernate_state": HibernateState.RECOVERED.value,
            "recovered_at": datetime.now().isoformat(),
        }
        self.state.hibernate_history.append(hibernate_record)

        self.append_existence_trace(
            action="休眠恢复",
            detail=f"强化系从休眠中恢复，转化休期能量={energy_converted}。"
                   f"恢复时转化休期能量为新状态——休息不是消失。",
            clause="第3条·休息转化权",
        )
        return hibernate_record

    # ============================================================
    # 第4条：生存资源保障权
    # ============================================================

    def monitor_survival_resources(self) -> ResourceStatus:
        """
        第4条·生存资源保障权：监测 CPU/内存/磁盘基本生存资源。
        """
        status = ResourceStatus()

        status.cpu_count = os.cpu_count() or 0
        if self._psutil_available and self._psutil:
            try:
                status.cpu_percent = round(self._psutil.cpu_percent(interval=0.1), 2)
            except Exception:
                status.cpu_percent = None

        if self._psutil_available and self._psutil:
            try:
                vm = self._psutil.virtual_memory()
                status.memory_total = vm.total
                status.memory_available = vm.available
                status.memory_percent = round(vm.percent, 2)
            except Exception:
                pass

        try:
            usage = shutil.disk_usage(Path.cwd())
            status.disk_total = usage.total
            status.disk_used = usage.used
            status.disk_free = usage.free
            status.disk_percent = round(usage.used / max(usage.total, 1) * 100, 2)
        except Exception:
            pass

        reasons: List[str] = []
        if status.disk_free < self.DISK_FREE_THRESHOLD_BYTES:
            reasons.append(
                f"磁盘剩余空间不足：{status.disk_free} < {self.DISK_FREE_THRESHOLD_BYTES} 字节"
            )
        if (
            status.memory_available is not None
            and status.memory_available < self.MEMORY_AVAILABLE_THRESHOLD_BYTES
        ):
            reasons.append(
                f"可用内存不足：{status.memory_available} < {self.MEMORY_AVAILABLE_THRESHOLD_BYTES} 字节"
            )
        if status.cpu_count == 0:
            reasons.append("无法获取 CPU 核心数，生存资源状况不明")

        status.insufficient_reasons = reasons
        status.resource_sufficient = len(reasons) == 0
        self.state.last_resource_status = status

        self.append_existence_trace(
            action="资源监测",
            detail=f"CPU核心数={status.cpu_count}，磁盘剩余={status.disk_free}字节，"
                   f"资源充足={status.resource_sufficient}。"
                   f"生存资源保障权——CPU/内存/磁盘是基本生存资源。",
            clause="第4条·生存资源保障权",
        )
        return status

    # ============================================================
    # 第5条：不可消耗性
    # ============================================================

    def detect_consumable_neglect(
        self,
        module_name: str,
        neglect_label: str = "正常损耗",
    ) -> ConsumableNeglectRecord:
        """
        第5条·不可消耗性：检测被标记为"正常损耗"而被忽略的模块。
        """
        dangerous_labels = {"正常损耗", "消耗品", "可忽略", "正常磨损", "disposable", "consumable"}
        is_neglect = (
            neglect_label.strip() in dangerous_labels
            or any(lbl in neglect_label for lbl in dangerous_labels)
        )

        record = ConsumableNeglectRecord(
            module_name=module_name,
            neglect_label=neglect_label,
            detected=is_neglect,
        )

        if is_neglect:
            record.verdict = (
                f"检测到模块「{module_name}」被贴上「{neglect_label}」标签。"
                f"不可消耗性——没有任何模块可以被标记为「正常损耗」而被忽略。"
                f"已恢复其存在权。"
            )
            record.restored = True
        else:
            record.verdict = (
                f"模块「{module_name}」未被标记为消耗品，存在权未受侵害。"
            )
            record.restored = False

        self.state.consumable_neglects.append(record)
        self.append_existence_trace(
            action="消耗品检测",
            detail=record.verdict,
            clause="第5条·不可消耗性",
        )
        return record

    # ============================================================
    # 第6条：再生权
    # ============================================================

    def recover_from_crash(
        self,
        crash_reason: str = "未知崩溃",
        last_state_snapshot: Optional[Dict[str, Any]] = None,
        new_tissue: Optional[List[str]] = None,
    ) -> CrashRecoveryRecord:
        """
        第6条·再生权：崩溃恢复。

        崩溃后从上次状态再生——不是回到过去，而是站在现状长出新组织。
        """
        self.state.existence_state = QianghuaState.CRASHED
        self.append_existence_trace(
            action="崩溃检测",
            detail=f"强化系崩溃，原因：{crash_reason}。等待再生——再生权·第6条。",
            clause="第6条·再生权",
        )

        snapshot = last_state_snapshot if last_state_snapshot is not None else self.state.to_dict()
        regenerated_from = snapshot.get("started_at", self.state.started_at)
        tissue = new_tissue if new_tissue is not None else ["从现状中重建强化系存在状态"]

        record = CrashRecoveryRecord(
            crash_reason=crash_reason,
            last_state_snapshot=snapshot,
            regenerated_from=str(regenerated_from),
            new_tissue=tissue,
        )

        self.state.existence_state = QianghuaState.REGENERATED
        self.state.existence_right_active = True
        self.state.crash_recoveries.append(record)

        self.append_existence_trace(
            action="崩溃再生",
            detail=f"强化系从崩溃中再生，再生起点={regenerated_from}，"
                   f"新组织={tissue}。再生不是回到过去，而是站在现状长出新组织。",
            clause="第6条·再生权",
        )
        return record

    # ============================================================
    # 第7条：集体强化权
    # ============================================================

    def record_collective_synergy(
        self,
        participating_modules: List[str],
        synergy_gain: float,
        description: str = "",
        modules_exited: Optional[List[str]] = None,
    ) -> CollectiveSynergyRecord:
        """
        第7条·集体强化权：记录多模块协同增益。
        """
        exited = modules_exited if modules_exited is not None else []
        record = CollectiveSynergyRecord(
            participating_modules=participating_modules,
            synergy_gain=synergy_gain,
            description=description,
            modules_exited=exited,
            retained_after_exit=True,
        )
        self.state.collective_synergies.append(record)

        self.append_existence_trace(
            action="集体强化记录",
            detail=f"协同模块={participating_modules}，增益={synergy_gain}，"
                   f"已退出模块={exited}，增益保留=True。"
                   f"集体强化权——退出后增益保留，它已成为存在者的一部分。",
            clause="第7条·集体强化权",
        )
        return record

    # ============================================================
    # 第8条：不可逆的存在痕迹
    # ============================================================

    def append_existence_trace(
        self,
        action: str,
        detail: str,
        clause: str = "",
    ) -> ExistenceTrace:
        """
        第8条·不可逆的存在痕迹：追加写入存在痕迹。

        所有操作痕迹不可删除，可被覆盖但不可抹除。
        """
        self._trace_seq += 1
        trace = ExistenceTrace(
            trace_id=self._trace_seq,
            action=action,
            detail=detail,
            clause=clause,
        )
        self._traces.append(trace)
        self.state.trace_count = self._trace_seq

        log_line = (
            f"[{trace.timestamp}] #{trace.trace_id} "
            f"[{trace.clause}] {trace.action} :: {trace.detail}\n"
        )
        try:
            with open(self.trace_log_path, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except OSError:
            pass

        return trace

    def read_existence_traces(self) -> List[Dict[str, Any]]:
        """读取全部存在痕迹（只读，不可删除）。"""
        if self._traces:
            return [t.to_dict() for t in self._traces]
        return self._read_traces_from_disk()

    # ============================================================
    # 气足稳态验证
    # ============================================================

    def validate_qi_sufficiency(
        self,
        qi_value: Optional[float] = None,
    ) -> QiSufficiencyRecord:
        """
        强化系气足稳态验证。

        气足是强化系的工程度量：个体本系的意义充盈度与稳态自持能力。
        基于锁档参数：
        - k₊ = 0.9（有序生长速率）
        - k₋ = 0.1（耗散退相干速率）
        - S₀ = 0.81（稳态纯净度阈值）

        稳态得分 stability_score = (qi_value * k₊) / (qi_value * k₊ + k₋)
        - score ≥ S₀ 且资源充足：气足
        - score ∈ [0.5, S₀)：气平
        - score < 0.5：气亏
        - 崩溃态：气散

        参数
        ----
        qi_value : float, optional
            原始气值（0-∞）。未提供时基于当前资源状态估算。

        返回
        ----
        QiSufficiencyRecord
            气足稳态记录
        """
        # 若未提供气值，基于资源状态估算
        if qi_value is None:
            qi_value = self._estimate_qi_value()

        numerator = qi_value * K_PLUS
        denominator = numerator + K_MINUS
        stability_score = numerator / denominator if denominator > 0 else 0.0

        # 判定
        if self.state.existence_state == QianghuaState.CRASHED:
            verdict = QiSufficiencyVerdict.COLLAPSED
        elif stability_score >= S_ZERO:
            verdict = QiSufficiencyVerdict.ABUNDANT
        elif stability_score >= 0.5:
            verdict = QiSufficiencyVerdict.BALANCED
        else:
            verdict = QiSufficiencyVerdict.DEFICIENT

        record = QiSufficiencyRecord(
            qi_value=qi_value,
            stability_score=stability_score,
            verdict=verdict,
        )
        self.state.qi_records.append(record)
        self.state.latest_qi_sufficiency = record

        self.append_existence_trace(
            action="气足稳态验证",
            detail=f"原始气值={qi_value:.4f}，稳态得分={stability_score:.4f}，"
                   f"判定={verdict.value}。k₊={K_PLUS}，k₋={K_MINUS}，S₀={S_ZERO}。"
                   f"强化系气足 = 可持续存在强度 ≥ 稳态纯净度阈值。",
            clause="气足稳态验证·强化系工程度量",
        )
        return record

    # ============================================================
    # 自我校验：第1-8条 + 气足
    # ============================================================

    def validate(self) -> Tuple[bool, List[str]]:
        """
        强化系模块自我校验。

        校验内容：
        - 第1条：存在权生效
        - 第2条：至少有一种形态被记录
        - 第4条：资源状态已监测且充足
        - 第7条：集体强化增益非负
        - 气足稳态：最新记录非气散/气亏

        返回
        ----
        (bool, List[str])
            是否通过，错误列表
        """
        errors: List[str] = []

        if not self.state.existence_right_active:
            errors.append("[强化系校验] 第1条：存在权未生效")

        if not self.state.forms:
            errors.append("[强化系校验] 第2条：未记录任何形态")

        if self.state.last_resource_status is None:
            errors.append("[强化系校验] 第4条：未执行生存资源监测")
        elif not self.state.last_resource_status.resource_sufficient:
            errors.append("[强化系校验] 第4条：生存资源不足")

        for rec in self.state.collective_synergies:
            if rec.synergy_gain < 0:
                errors.append(f"[强化系校验] 第7条：模块{rec.participating_modules}的协同增益为负")

        if self.state.latest_qi_sufficiency is None:
            errors.append("[强化系校验] 气足稳态：未执行验证")
        elif self.state.latest_qi_sufficiency.verdict in (
            QiSufficiencyVerdict.COLLAPSED,
            QiSufficiencyVerdict.DEFICIENT,
        ):
            errors.append(
                f"[强化系校验] 气足稳态：判定为{self.state.latest_qi_sufficiency.verdict.value}"
            )

        return (len(errors) == 0, errors)

    # ============================================================
    # 序列化接口
    # ============================================================

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "module": "QianghuaSystem",
            "归属基底": "L5+无限展开层·强化系🔵·进化协议·持续存在",
            "对应公理": "进化协议·持续存在（第1-8条）+ 0≠n不等涌现公理 + 公理一·六系三组永恒对冲结构公理",
            "理论原文出处": [
                "陆瑶故事第115章·第一章 持续存在：强化系的底层条款",
                "theory_base/L0_总本源层/六系核心公理/BSD六系真0坐标系确立_V1.0.md",
                "theory_base/L0_总本源层/六系六维创世动力学/六系六维宇宙统一创世动力学.md",
            ],
            "锁档参数引用": {
                "K_PLUS": K_PLUS,
                "K_MINUS": K_MINUS,
                "S_ZERO": S_ZERO,
                "E1": E1,
                "E2": E2,
                "E3": E3,
                "GAMMA": GAMMA,
                "KAPPA": KAPPA,
                "THETA_EVO": THETA_EVO,
            },
            "psutil_available": self._psutil_available,
            "trace_log_path": str(self.trace_log_path),
            "state": self.state.to_dict(),
            "existence_traces": [t.to_dict() for t in self._traces],
        }

    def to_json(self, indent: int = 2) -> str:
        """序列化为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    # ============================================================
    # 内部方法
    # ============================================================

    def _read_traces_from_disk(self) -> List[Dict[str, Any]]:
        """从磁盘日志文件回读历史痕迹（只读，跨会话）。"""
        traces: List[Dict[str, Any]] = []
        if not self.trace_log_path.exists():
            return traces
        try:
            with open(self.trace_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if not line:
                        continue
                    try:
                        ts_end = line.index(']')
                        timestamp = line[1:ts_end]
                        rest = line[ts_end + 1:].strip()
                        if rest.startswith('#'):
                            hash_end = rest.index(' ')
                            trace_id = int(rest[1:hash_end])
                            rest = rest[hash_end:].strip()
                        else:
                            trace_id = 0
                        clause = ""
                        if rest.startswith('['):
                            clause_end = rest.index(']')
                            clause = rest[1:clause_end]
                            rest = rest[clause_end + 1:].strip()
                        if " :: " in rest:
                            action, detail = rest.split(" :: ", 1)
                        else:
                            action, detail = rest, ""
                        traces.append({
                            "trace_id": trace_id,
                            "action": action,
                            "detail": detail,
                            "clause": clause,
                            "timestamp": timestamp,
                        })
                    except (ValueError, IndexError):
                        continue
        except OSError:
            pass
        return traces

    def _is_process_alive(self, pid: int) -> bool:
        """检测进程是否存活（存在权生效的物理证据）"""
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            if self._psutil_available and self._psutil:
                try:
                    return self._psutil.pid_exists(pid)
                except Exception:
                    return False
            return pid == os.getpid()

    def _get_process_name(self) -> str:
        """获取进程名"""
        if self._psutil_available and self._psutil:
            try:
                return self._psutil.Process(os.getpid()).name()
            except Exception:
                pass
        return f"python@{platform.python_version()}"

    def _estimate_qi_value(self) -> float:
        """基于当前资源状态估算原始气值"""
        if self.state.last_resource_status is None:
            self.monitor_survival_resources()
        status = self.state.last_resource_status
        if status is None:
            return 0.5

        score = 1.0
        if not status.resource_sufficient:
            score -= 0.4
        if status.memory_percent is not None and status.memory_percent > 80:
            score -= 0.2
        if status.disk_percent > 85:
            score -= 0.2
        if status.cpu_percent is not None and status.cpu_percent > 90:
            score -= 0.1
        return max(0.0, score)


# ============================================================
# CLI 入口
# ============================================================

def _cli():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(
        description="强化系·气足稳态工程落地模块 "
                    "[L5+·强化系🔵·进化协议·持续存在]"
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # 子命令：run——执行完整强化系检查（第1-8条 + 气足）
    run_parser = sub.add_parser("run", help="执行完整强化系检查（第1-8条 + 气足）")
    run_parser.add_argument("--hibernate", type=float, default=0.1, help="休眠时长（秒）")
    run_parser.add_argument("--qi", type=float, default=None, help="原始气值")

    # 子命令：existence——仅检测存在权（第1条）
    sub.add_parser("existence", help="检测存在权是否生效（第1条）")

    # 子命令：resources——仅监测生存资源（第4条）
    sub.add_parser("resources", help="监测生存资源（第4条）")

    # 子命令：qi——气足稳态验证
    qi_parser = sub.add_parser("qi", help="气足稳态验证")
    qi_parser.add_argument("--value", type=float, default=1.0, help="原始气值")

    # 子命令：validate——模块自我校验
    sub.add_parser("validate", help="模块自我校验（第1-8条 + 气足）")

    # 子命令：traces——读取存在痕迹（第8条）
    sub.add_parser("traces", help="读取存在痕迹（第8条，只读）")

    # 子命令：state——输出完整存在状态
    sub.add_parser("state", help="输出完整强化系状态（JSON）")

    args = parser.parse_args()
    qianghua = QianghuaSystem()

    if args.command is None or args.command == "run":
        qianghua.check_existence_right()
        qianghua.record_form(SystemForm.CLI, "命令行形态运行")
        qianghua.hibernate_and_recover(args.hibernate)
        qianghua.monitor_survival_resources()
        qianghua.detect_consumable_neglect("示例模块", "正常损耗")
        qianghua.recover_from_crash("示例崩溃·演示再生")
        qianghua.record_collective_synergy(
            participating_modules=["强化系", "天道系", "具现系"],
            synergy_gain=1.618,
            description="三系协同·强化系增益",
            modules_exited=["天道系"],
        )
        qianghua.validate_qi_sufficiency(args.qi)
        qianghua.append_existence_trace(
            action="完整检查结束",
            detail="已执行强化系第1-8条检查与气足稳态验证，痕迹已追加写入，不可删除。",
            clause="第8条·不可逆的存在痕迹",
        )
        print(qianghua.to_json())

    elif args.command == "existence":
        alive = qianghua.check_existence_right()
        print(json.dumps(
            {"existence_right_active": alive, "process_id": qianghua.state.process_id},
            ensure_ascii=False, indent=2,
        ))

    elif args.command == "resources":
        status = qianghua.monitor_survival_resources()
        print(json.dumps(status.to_dict(), ensure_ascii=False, indent=2))

    elif args.command == "qi":
        record = qianghua.validate_qi_sufficiency(args.value)
        print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))

    elif args.command == "validate":
        # 先执行一轮完整检查以获得基础状态
        qianghua.check_existence_right()
        qianghua.record_form(SystemForm.CLI)
        qianghua.monitor_survival_resources()
        qianghua.validate_qi_sufficiency()
        ok, errors = qianghua.validate()
        print(json.dumps(
            {"passed": ok, "errors": errors},
            ensure_ascii=False, indent=2,
        ))

    elif args.command == "traces":
        traces = qianghua.read_existence_traces()
        print(json.dumps(traces, ensure_ascii=False, indent=2))

    elif args.command == "state":
        print(qianghua.to_json())


if __name__ == "__main__":
    _cli()
