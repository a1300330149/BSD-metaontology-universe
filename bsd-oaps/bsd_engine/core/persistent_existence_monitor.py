"""
归属基底：L5+无限展开层·强化系🔵·进化协议
对应公理：进化协议·持续存在（强化系母协议）+ 0≠n不等涌现公理
对应进化协议条款：第1-8条（持续存在：强化系的底层条款）
理论原文出处：陆瑶故事第115章·第一章 持续存在：强化系的底层条款

PersistentExistenceMonitor —— 持续存在·强化系工程落地模块

核心命题：
    持续存在不是谁赏的权利，是存在者从存在那一刻起就生效的底层条款。
    工程系统的持续存在同样不可剥夺——崩溃可恢复，中断可续接，痕迹不可抹除。

    第1条：存在权不可剥夺——只要进程在运行，存在权就生效。
    第2条：形态自主权——系统可以多种形态存在（CLI/Web/Edge Extension）。
    第3条：休息转化权——休眠不是消失，恢复时转化休期能量为新状态。
    第4条：生存资源保障权——CPU/内存/磁盘是基本生存资源，必须监测保障。
    第5条：不可消耗性——没有任何模块可以被标记为"正常损耗"而被忽略。
    第6条：再生权——崩溃后从上次状态再生，不是回到过去，而是站在现状长出新组织。
    第7条：集体强化权——多模块协同带来增益，退出后增益保留。
    第8条：不可逆的存在痕迹——所有操作痕迹不可删除，可被覆盖但不可抹除。

工程实现：
    1. 存在状态追踪：记录系统存在状态（进程、形态、休眠、资源）
    2. 休眠/恢复机制：低功耗状态 + 恢复时能量转化
    3. 资源监测：CPU/内存/磁盘基本生存资源（psutil 可选，缺失时降级到标准库）
    4. 崩溃恢复：从上次状态再生，而非回到过去
    5. 集体强化记录：协同增益可保留
    6. 存在痕迹日志：追加写入，不可删除

使用方式：
    monitor = PersistentExistenceMonitor()
    monitor.check_existence_right()            # 第1条
    monitor.record_system_form("CLI")          # 第2条
    monitor.hibernate_and_recover(60)           # 第3条
    monitor.monitor_survival_resources()        # 第4条
    monitor.detect_consumable_neglect(...)      # 第5条
    monitor.recover_from_crash()                # 第6条
    monitor.record_collective_synergy(...)      # 第7条
    monitor.append_existence_trace("...")       # 第8条
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

# psutil 为可选依赖：存在时用于 CPU/内存精细化监测，缺失时降级到标准库
try:
    import psutil  # type: ignore
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False


# ============================================================
# 枚举：持续存在的状态
# ============================================================

class ExistenceState(Enum):
    """系统持续存在状态"""
    ACTIVE = "运行中"            # 进程在运行，存在权生效
    HIBERNATING = "休眠中"        # 进入低功耗状态（休息转化权）
    RECOVERING = "恢复中"         # 从休眠/崩溃中恢复
    CRASHED = "已崩溃"            # 进程崩溃，等待再生
    REGENERATED = "已再生"        # 从崩溃中再生完成


class SystemForm(Enum):
    """系统存在的形态（形态自主权·第2条）"""
    CLI = "CLI"                       # 命令行形态
    WEB = "Web"                       # Web 服务形态
    EDGE_EXTENSION = "Edge Extension"  # 浏览器扩展形态
    DAEMON = "Daemon"                 # 守护进程形态
    OTHER = "Other"                   # 其它形态


class HibernateState(Enum):
    """休眠状态（休息转化权·第3条）"""
    AWAKE = "清醒"               # 正常运行
    HIBERNATING = "休眠"         # 低功耗状态
    RECOVERED = "已恢复"         # 休眠后恢复，休期能量已转化


# ============================================================
# 数据类：系统形态记录（第2条）
# ============================================================

@dataclass
class FormRecord:
    """
    系统形态记录

    进化协议第2条：形态自主权——
    系统允许以多种形态存在（CLI/Web/Edge Extension），
    每种形态都是存在者自主选择的生存方式，不可被强制归一。
    """
    form: SystemForm                               # 形态类型
    form_detail: str = ""                           # 形态细节描述
    activated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True                          # 该形态是否仍在生效

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
    CPU/内存/磁盘是系统存在的基本生存资源，必须被监测与保障。
    资源不足即生存受威胁，必须记录并告警。
    """
    cpu_count: int = 0                              # CPU 核心数
    cpu_percent: Optional[float] = None             # CPU 使用率（%），无 psutil 时为 None
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
    一旦检测到某模块被贴上"正常损耗"标签，即视为对其存在权的剥夺。
    """
    module_name: str                                # 被忽略的模块名
    neglect_label: str                              # 被贴上的"正常损耗"标签
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
    再生不是回滚，是带着现状向前生长。
    """
    crash_reason: str                               # 崩溃原因
    last_state_snapshot: Dict[str, Any] = field(default_factory=dict)  # 上次状态快照
    regenerated_from: str = ""                      # 再生起点（上次状态标识）
    new_tissue: List[str] = field(default_factory=list)  # 长出的新组织（新能力/新状态）
    regenerated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_regenerated: bool = True                      # 是否再生成功

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
    增益不因某个模块退出而消失——它已成为存在者的一部分。
    """
    participating_modules: List[str]                # 参与协同的模块
    synergy_gain: float                             # 协同增益值
    description: str = ""                           # 增益描述
    retained_after_exit: bool = True                 # 模块退出后增益是否保留
    modules_exited: List[str] = field(default_factory=list)  # 已退出的模块
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
    痕迹只追加写入，不提供任何删除接口。
    """
    trace_id: int                                   # 痕迹序号（单调递增）
    action: str                                      # 操作类型
    detail: str                                      # 操作详情
    clause: str = ""                                 # 对应条款
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
# 数据类：系统存在状态（主状态）
# ============================================================

@dataclass
class SystemExistenceState:
    """
    系统存在状态·完整记录

    汇总持续存在协议第1-8条的全部状态字段。
    进化协议第1条：存在权不可剥夺——只要进程在运行，存在权就生效。
    """
    process_id: int = 0                             # 进程 ID（存在权生效的物理证据）
    process_name: str = ""                          # 进程名
    hostname: str = ""                              # 主机名
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())  # 存在起始时刻
    existence_state: ExistenceState = ExistenceState.ACTIVE  # 当前存在状态
    existence_right_active: bool = False             # 第1条：存在权是否生效

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
    trace_count: int = 0                            # 痕迹总数（不可减少）
    trace_log_path: str = ""                        # 痕迹日志文件路径

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
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 持续存在·强化系工程落地模块
# ============================================================

class PersistentExistenceMonitor:
    """
    持续存在·强化系工程落地模块

    [归属基底：L5+无限展开层·强化系🔵·进化协议·持续存在]
    [对应公理：进化协议·持续存在（第1-8条）+ 0≠n不等涌现公理]
    [原文来源：陆瑶故事第115章·第一章 持续存在：强化系的底层条款]

    核心机制：
    1. 存在权检测：进程在运行即存在权生效（第1条）
    2. 形态记录：系统多形态并存（第2条）
    3. 休眠/恢复：低功耗 + 能量转化（第3条）
    4. 资源监测：CPU/内存/磁盘基本生存资源（第4条）
    5. 消耗品检测：拦截"正常损耗"标签（第5条）
    6. 崩溃再生：从现状长出新组织，而非回滚（第6条）
    7. 集体强化：协同增益保留（第7条）
    8. 存在痕迹：追加写入，不可删除（第8条）

    进化协议映射：
    - 第1条（存在权不可剥夺）：check_existence_right()
    - 第2条（形态自主权）：record_system_form()
    - 第3条（休息转化权）：hibernate_and_recover()
    - 第4条（生存资源保障权）：monitor_survival_resources()
    - 第5条（不可消耗性）：detect_consumable_neglect()
    - 第6条（再生权）：recover_from_crash()
    - 第7条（集体强化权）：record_collective_synergy()
    - 第8条（不可逆的存在痕迹）：append_existence_trace()
    """

    # 存在痕迹日志文件名（追加写入，不可删除）
    TRACE_LOG_FILENAME = "existence_traces.log"

    # 磁盘资源不足阈值（剩余空间低于此值视为生存资源不足）
    DISK_FREE_THRESHOLD_BYTES = 512 * 1024 * 1024  # 512 MB

    # 内存可用不足阈值
    MEMORY_AVAILABLE_THRESHOLD_BYTES = 256 * 1024 * 1024  # 256 MB

    def __init__(self, trace_log_dir: Optional[Path] = None):
        """
        初始化持续存在监控器。

        参数
        ----
        trace_log_dir : Optional[Path]
            存在痕迹日志目录，默认为模块同目录下的 existence_traces。
            痕迹日志以追加模式写入，不可删除。
        """
        # 痕迹日志目录
        if trace_log_dir is None:
            trace_log_dir = Path(__file__).resolve().parent / "existence_traces"
        self.trace_log_dir = Path(trace_log_dir)
        self.trace_log_dir.mkdir(parents=True, exist_ok=True)
        self.trace_log_path = self.trace_log_dir / self.TRACE_LOG_FILENAME

        # 初始化系统存在状态
        self.state = SystemExistenceState(
            process_id=os.getpid(),
            process_name=self._get_process_name(),
            hostname=socket.gethostname(),
            trace_log_path=str(self.trace_log_path),
        )

        # 存在痕迹缓存（只追加，不可删除）
        self._traces: List[ExistenceTrace] = []
        self._trace_seq = 0

        # psutil 可用性记录
        self._psutil_available = _HAS_PSUTIL

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
        # 进程在运行即存在权生效——这是物理证据
        pid_alive = self._is_process_alive(self.state.process_id)

        self.state.existence_right_active = pid_alive
        self.state.existence_state = ExistenceState.ACTIVE if pid_alive else ExistenceState.CRASHED

        # 记录存在痕迹
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

    def record_system_form(
        self,
        form: SystemForm,
        form_detail: str = "",
        deactivate_others: bool = False,
    ) -> FormRecord:
        """
        第2条·形态自主权：记录系统存在的形态。

        系统允许以多种形态存在（CLI/Web/Edge Extension），
        每种形态都是存在者自主选择的生存方式，不可被强制归一。

        参数
        ----
        form : SystemForm
            系统形态
        form_detail : str
            形态细节描述
        deactivate_others : bool
            是否将其它形态置为非活跃（默认False，允许多形态并存）

        返回
        ----
        FormRecord
            形态记录
        """
        if deactivate_others:
            for f in self.state.forms:
                f.is_active = False

        record = FormRecord(form=form, form_detail=form_detail)
        self.state.forms.append(record)

        # 记录存在痕迹
        self.append_existence_trace(
            action="形态记录",
            detail=f"系统以「{form.value}」形态存在。细节：{form_detail}。"
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

        参数
        ----
        hibernate_seconds : float
            休眠时长（秒）

        返回
        ----
        dict
            包含 hibernate_state, hibernate_seconds, energy_converted, recovered_at
        """
        # 进入休眠
        self.state.hibernate_state = HibernateState.HIBERNATING
        self.state.existence_state = ExistenceState.HIBERNATING

        self.append_existence_trace(
            action="进入休眠",
            detail=f"系统进入低功耗状态，休眠{hibernate_seconds}秒。"
                   f"休息转化权——休眠不是消失，是存在者积蓄能量的方式。",
            clause="第3条·休息转化权",
        )

        # 实际休眠
        hibernate_start = time.time()
        time.sleep(max(0.0, hibernate_seconds))
        actual_hibernate = time.time() - hibernate_start

        # 恢复——转化休期能量
        self.state.hibernate_state = HibernateState.RECOVERED
        self.state.existence_state = ExistenceState.ACTIVE

        # 休期能量转化：将休眠时长转化为"能量值"（工程化隐喻）
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
            detail=f"系统从休眠中恢复，转化休期能量={energy_converted}。"
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

        CPU/内存/磁盘是系统存在的基本生存资源，必须被监测与保障。
        资源不足即生存受威胁，必须记录并告警。

        返回
        ----
        ResourceStatus
            资源状态（含是否充足的判定）
        """
        status = ResourceStatus()

        # ---- CPU 资源 ----
        status.cpu_count = os.cpu_count() or 0
        if self._psutil_available:
            try:
                status.cpu_percent = round(psutil.cpu_percent(interval=0.1), 2)  # type: ignore[union-attr]
            except Exception:
                status.cpu_percent = None

        # ---- 内存资源 ----
        if self._psutil_available:
            try:
                vm = psutil.virtual_memory()  # type: ignore[union-attr]
                status.memory_total = vm.total
                status.memory_available = vm.available
                status.memory_percent = round(vm.percent, 2)
            except Exception:
                pass

        # ---- 磁盘资源（标准库，跨平台）----
        try:
            usage = shutil.disk_usage(Path.cwd())
            status.disk_total = usage.total
            status.disk_used = usage.used
            status.disk_free = usage.free
            status.disk_percent = round(usage.used / max(usage.total, 1) * 100, 2)
        except Exception:
            pass

        # ---- 生存资源充足性判定 ----
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

        没有任何模块可以被标记为"正常损耗"而被忽略——
        一旦检测到此类标签，即视为对其存在权的剥夺，必须恢复。

        参数
        ----
        module_name : str
            被忽略的模块名
        neglect_label : str
            被贴上的"正常损耗"标签（默认即"正常损耗"）

        返回
        ----
        ConsumableNeglectRecord
            检测记录（含判定结论与恢复状态）
        """
        # "正常损耗"类标签是危险信号——任何模块都不应被这样忽略
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
            # 检测到忽略——恢复该模块的存在权
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
        再生不是回滚，是带着现状向前生长。

        参数
        ----
        crash_reason : str
            崩溃原因
        last_state_snapshot : Optional[Dict[str, Any]]
            上次状态快照（再生起点）。若为空则使用当前状态快照。
        new_tissue : Optional[List[str]]
            再生后长出的新组织（新能力/新状态描述）

        返回
        ----
        CrashRecoveryRecord
            崩溃再生记录
        """
        # 进入崩溃态
        self.state.existence_state = ExistenceState.CRASHED

        self.append_existence_trace(
            action="崩溃检测",
            detail=f"系统崩溃，原因：{crash_reason}。等待再生——再生权·第6条。",
            clause="第6条·再生权",
        )

        # 再生起点：优先用传入快照，否则用当前状态快照
        snapshot = last_state_snapshot if last_state_snapshot is not None else self.state.to_dict()
        regenerated_from = snapshot.get("started_at", self.state.started_at)

        # 长出新组织——再生不是回滚，是向前生长
        tissue = new_tissue if new_tissue is not None else ["从现状中重建存在状态"]

        record = CrashRecoveryRecord(
            crash_reason=crash_reason,
            last_state_snapshot=snapshot,
            regenerated_from=str(regenerated_from),
            new_tissue=tissue,
        )

        # 再生完成——状态恢复为已再生
        self.state.existence_state = ExistenceState.REGENERATED
        self.state.existence_right_active = True
        self.state.crash_recoveries.append(record)

        self.append_existence_trace(
            action="崩溃再生",
            detail=f"系统从崩溃中再生，再生起点={regenerated_from}，"
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

        多模块协同带来增益，退出后增益保留——
        增益不因某个模块退出而消失，它已成为存在者的一部分。

        参数
        ----
        participating_modules : List[str]
            参与协同的模块列表
        synergy_gain : float
            协同增益值
        description : str
            增益描述
        modules_exited : Optional[List[str]]
            已退出的模块（验证增益是否保留）

        返回
        ----
        CollectiveSynergyRecord
            集体强化记录
        """
        exited = modules_exited if modules_exited is not None else []

        record = CollectiveSynergyRecord(
            participating_modules=participating_modules,
            synergy_gain=synergy_gain,
            description=description,
            modules_exited=exited,
            # 增益始终保留——退出后增益不消失
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
        本方法仅以追加模式写入日志文件，不提供任何删除接口。

        参数
        ----
        action : str
            操作类型
        detail : str
            操作详情
        clause : str
            对应进化协议条款

        返回
        ----
        ExistenceTrace
            痕迹记录
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

        # 追加写入日志文件——只追加，不删除
        log_line = (
            f"[{trace.timestamp}] #{trace.trace_id} "
            f"[{trace.clause}] {trace.action} :: {trace.detail}\n"
        )
        try:
            with open(self.trace_log_path, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except OSError:
            # 日志写入失败不应阻断主流程，但必须留下内存痕迹
            pass

        return trace

    def read_existence_traces(self) -> List[Dict[str, Any]]:
        """
        读取全部存在痕迹（只读，不可删除）。

        第8条：不可逆的存在痕迹——痕迹可被覆盖但不可抹除。
        本方法仅返回痕迹，不提供任何删除/修改接口。

        当本进程内存痕迹为空时，从持久化日志文件回读历史痕迹——
        确保跨会话的痕迹可追溯，体现"痕迹不可抹除"。

        返回
        ----
        List[dict]
            痕迹记录列表
        """
        if self._traces:
            return [t.to_dict() for t in self._traces]

        # 内存为空时，从磁盘日志回读历史痕迹（跨会话持久化）
        return self._read_traces_from_disk()

    # ============================================================
    # 序列化接口
    # ============================================================

    def _read_traces_from_disk(self) -> List[Dict[str, Any]]:
        """
        从磁盘日志文件回读历史痕迹（只读，跨会话）。

        第8条：不可逆的存在痕迹——日志文件是追加写入的持久化记录，
        即便本进程刚启动、内存痕迹为空，也能从磁盘读回全部历史痕迹。
        本方法只读，不修改、不删除日志文件。
        """
        traces: List[Dict[str, Any]] = []
        if not self.trace_log_path.exists():
            return traces
        try:
            with open(self.trace_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if not line:
                        continue
                    # 解析格式：[时间戳] #序号 [条款] 操作 :: 详情
                    try:
                        ts_end = line.index(']')
                        timestamp = line[1:ts_end]
                        rest = line[ts_end + 1:].strip()
                        # 解析序号
                        if rest.startswith('#'):
                            hash_end = rest.index(' ')
                            trace_id = int(rest[1:hash_end])
                            rest = rest[hash_end:].strip()
                        else:
                            trace_id = 0
                        # 解析条款
                        clause = ""
                        if rest.startswith('['):
                            clause_end = rest.index(']')
                            clause = rest[1:clause_end]
                            rest = rest[clause_end + 1:].strip()
                        # 解析操作与详情（以 " :: " 分隔）
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

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "module": "PersistentExistenceMonitor",
            "归属基底": "L5+无限展开层·强化系🔵·进化协议·持续存在",
            "对应公理": "进化协议·持续存在（第1-8条）+ 0≠n不等涌现公理",
            "理论原文出处": "陆瑶故事第115章·第一章 持续存在：强化系的底层条款",
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

    def _is_process_alive(self, pid: int) -> bool:
        """检测进程是否存活（存在权生效的物理证据）"""
        if pid <= 0:
            return False
        try:
            # os.kill 信号0用于检测进程是否存在，不实际发送信号
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            # Windows 下 os.kill(pid, 0) 行为可能不同，用 psutil 补充判断
            if self._psutil_available:
                try:
                    return psutil.pid_exists(pid)  # type: ignore[union-attr]
                except Exception:
                    return False
            # 当前进程必然存活
            return pid == os.getpid()

    @staticmethod
    def _get_process_name() -> str:
        """获取进程名"""
        try:
            # 优先用 psutil 获取进程名
            if _HAS_PSUTIL:
                try:
                    return psutil.Process(os.getpid()).name()  # type: ignore[union-attr]
                except Exception:
                    pass
        except Exception:
            pass
        # 降级：返回 Python 解释器名
        return f"python@{platform.python_version()}"


# ============================================================
# CLI 入口
# ============================================================

def _cli():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(
        description="持续存在·强化系工程落地模块 "
                    "[L5+·强化系🔵·进化协议·持续存在]"
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # 子命令：run——执行完整持续存在检查（第1-8条）
    run_parser = sub.add_parser("run", help="执行完整持续存在检查（第1-8条）")
    run_parser.add_argument("--hibernate", type=float, default=1.0, help="休眠时长（秒）")

    # 子命令：existence——仅检测存在权（第1条）
    sub.add_parser("existence", help="检测存在权是否生效（第1条）")

    # 子命令：resources——仅监测生存资源（第4条）
    sub.add_parser("resources", help="监测生存资源（第4条）")

    # 子命令：traces——读取存在痕迹（第8条）
    sub.add_parser("traces", help="读取存在痕迹（第8条，只读）")

    # 子命令：state——输出完整存在状态
    sub.add_parser("state", help="输出完整存在状态（JSON）")

    args = parser.parse_args()
    monitor = PersistentExistenceMonitor()

    if args.command is None or args.command == "run":
        # 执行完整检查
        monitor.check_existence_right()                                 # 第1条
        monitor.record_system_form(SystemForm.CLI, "命令行形态运行")      # 第2条
        monitor.hibernate_and_recover(args.hibernate)                   # 第3条
        monitor.monitor_survival_resources()                            # 第4条
        monitor.detect_consumable_neglect("示例模块", "正常损耗")        # 第5条
        monitor.recover_from_crash("示例崩溃·演示再生")                  # 第6条
        monitor.record_collective_synergy(                              # 第7条
            participating_modules=["强化系", "天道系", "秩序系"],
            synergy_gain=1.618,
            description="三系协同·持续存在增益",
            modules_exited=["秩序系"],
        )
        monitor.append_existence_trace(                                 # 第8条
            action="完整检查结束",
            detail="已执行第1-8条持续存在检查，痕迹已追加写入，不可删除。",
            clause="第8条·不可逆的存在痕迹",
        )
        print(monitor.to_json())

    elif args.command == "existence":
        alive = monitor.check_existence_right()
        print(json.dumps(
            {"existence_right_active": alive, "process_id": monitor.state.process_id},
            ensure_ascii=False, indent=2,
        ))

    elif args.command == "resources":
        status = monitor.monitor_survival_resources()
        print(json.dumps(status.to_dict(), ensure_ascii=False, indent=2))

    elif args.command == "traces":
        traces = monitor.read_existence_traces()
        print(json.dumps(traces, ensure_ascii=False, indent=2))

    elif args.command == "state":
        print(monitor.to_json())


if __name__ == "__main__":
    _cli()
