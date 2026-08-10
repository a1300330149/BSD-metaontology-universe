"""
归属基底：L5+无限展开层·变身系⚫·进化协议
对应公理：进化协议·阶段完整（变身系母协议）+ 0≠n不等涌现公理
对应进化协议条款：第17-24条（阶段完整：变身系的底层条款）
理论原文出处：陆瑶故事第115章·第三章 阶段完整：变身系的底层条款

PhaseCompletenessChecker —— 阶段完整·变身系阶段完整校验引擎
【理论版本：ACTIVE-V1.8】

核心命题：
    "阶段完整"意味着：人生每个阶段都是完整的，不是半成品。
    软件开发的每个阶段（设计/开发/测试/发布）同样完整——
    没有哪个阶段只是"还没完成的过渡期"。

    第17条：阶段完整权——V1.0不是"还没完成的V2.0"。
    第18条：身份的游戏——允许系统试运行不同身份配置。
    第19条：身份切换自由——从V1到V2不需要证明V1"没用了"。
    第20条：多重身份共存——V1和V2可以同时存在，不用揉成一个。
    第21条：身份生长不可逆性——旧版本不可删除，可以废弃但不会消失。
    第22条：拒绝被定义权——拒绝外部系统给本系统下定义，拒诊不是病。
    第23条：生理自主权——系统配置自主，不经同意不可被改造/增强/削减。
    第24条：死亡自主权——系统生命周期终结自主，如何退役由系统自己决定。

工程实现：
    1. 阶段完整性校验：每个开发阶段必须自带完整闭环，不依赖下一阶段
    2. 身份配置管理：支持测试/生产/调试多种身份的试运行
    3. 版本切换记录：版本切换不需要证明旧版本无用
    4. 多版本共存：支持多版本同时存活，不强制合并
    5. 不可逆生长：旧版本只可废弃不可删除，影响追溯
    6. 外部定义拒绝：拒绝外部系统强加的定义标签
    7. 配置自主：系统配置变更需本系统同意
    8. 退役自主：系统退役方式由系统自决

使用方式：
    checker = PhaseCompletenessChecker()
    result = checker.check_phase_completeness("v1.0", ["design", "dev", "test", "release"])
    # result.is_complete = True 时，该阶段视为完整
"""

import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ============================================================
# 枚举：阶段完整状态
# ============================================================

class PhaseCompletenessState(Enum):
    """阶段完整校验状态"""
    INITIATED = "已发起"            # 阶段校验已发起，尚未开始校验
    VALIDATING = "校验中"           # 正在校验阶段完整性
    COMPLETE = "阶段完整"           # 该阶段自带完整闭环
    INCOMPLETE = "阶段不完备"       # 该阶段依赖下一阶段才完整（违规）
    SUPERSEDED = "已被超越"         # 该阶段已被新版本超越（但本身仍完整）
    DEPRECATED = "已废弃"           # 该阶段已废弃但不可删除（第21条）
    RETIRED = "已退役"              # 该阶段已按自主意愿退役（第24条）


class SystemIdentity(Enum):
    """系统身份（第18条·身份的游戏）"""
    TESTING = "测试模式"            # 试运行测试身份
    PRODUCTION = "生产模式"         # 正式生产身份
    DEBUG = "调试模式"              # 调试身份
    EXPERIMENTAL = "实验模式"       # 实验身份


class ExternalDefinitionVerdict(Enum):
    """外部定义判定（第22条·拒绝被定义权）"""
    REJECTED = "已拒绝"             # 拒绝外部定义
    ACCEPTED = "已采纳"             # 采纳（仅在本系统同意时）
    PENDING = "待判定"              # 待本系统判定


# ============================================================
# 数据类：阶段记录
# ============================================================

@dataclass
class PhaseRecord:
    """
    单个开发阶段的完整记录

    进化协议第17条：阶段完整权——
    每个阶段都是完整的，不是半成品。
    V1.0不是"还没完成的V2.0"。
    """
    phase_id: str                                       # 阶段标识（如 v1.0）
    phase_name: str                                     # 阶段名称（如 设计/开发/测试/发布）
    sub_phases: List[str] = field(default_factory=list) # 子阶段列表
    is_self_contained: bool = False                     # 是否自带完整闭环（不依赖下一阶段）
    completeness_score: float = 0.0                     # 完整性评分（0-1）
    state: PhaseCompletenessState = PhaseCompletenessState.INITIATED
    closure_evidence: str = ""                          # 阶段闭环证据
    depends_on_next: bool = False                       # 是否依赖下一阶段才完整（违规标志）
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "phase_name": self.phase_name,
            "sub_phases": self.sub_phases,
            "is_self_contained": self.is_self_contained,
            "completeness_score": round(self.completeness_score, 4),
            "state": self.state.value,
            "closure_evidence": self.closure_evidence,
            "depends_on_next": self.depends_on_next,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：身份配置
# ============================================================

@dataclass
class IdentityConfig:
    """
    系统身份配置记录

    进化协议第18条：身份的游戏——
    允许系统试运行不同身份配置（测试模式/生产模式/调试模式）。
    身份不是固化的，是可以游戏性试运行的。
    """
    identity: SystemIdentity                            # 身份类型
    config_payload: Dict[str, Any] = field(default_factory=dict)  # 身份配置负载
    is_trial: bool = True                               # 是否为试运行（True=试运行，False=正式采纳）
    trial_start: str = field(default_factory=lambda: datetime.now().isoformat())
    trial_end: Optional[str] = None                     # 试运行结束时间
    adopted: bool = False                               # 是否被正式采纳

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identity": self.identity.value,
            "config_payload": self.config_payload,
            "is_trial": self.is_trial,
            "trial_start": self.trial_start,
            "trial_end": self.trial_end,
            "adopted": self.adopted,
        }


# ============================================================
# 数据类：版本切换日志
# ============================================================

@dataclass
class VersionSwitchLog:
    """
    版本切换日志

    进化协议第19条：身份切换自由——
    从V1到V2不需要证明V1"没用了"。
    切换是自由，旧版本无需被证伪。
    """
    switch_id: int                                      # 切换编号
    from_version: str                                   # 源版本
    to_version: str                                     # 目标版本
    switch_reason: str                                  # 切换原因（自由切换，无需证伪旧版本）
    proof_of_old_uselessness: str = ""                  # 旧版本无用证明（第19条要求：可为空）
    old_version_intact: bool = True                     # 旧版本是否保持完整（不可因切换而破坏）
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "switch_id": self.switch_id,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "switch_reason": self.switch_reason,
            "proof_of_old_uselessness": self.proof_of_old_uselessness,
            "old_version_intact": self.old_version_intact,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：外部定义记录
# ============================================================

@dataclass
class ExternalDefinition:
    """
    外部系统对本系统的定义记录

    进化协议第22条：拒绝被定义权——
    拒绝外部系统给本系统下定义。
    拒诊不是病——拒绝被诊断不等于真的有病。
    """
    source: str                                         # 定义来源（外部系统标识）
    definition_label: str                               # 外部贴的标签/定义
    definition_content: str                             # 定义内容
    verdict: ExternalDefinitionVerdict = ExternalDefinitionVerdict.PENDING
    reject_reason: str = ""                             # 拒绝理由
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "definition_label": self.definition_label,
            "definition_content": self.definition_content,
            "verdict": self.verdict.value,
            "reject_reason": self.reject_reason,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：阶段完整校验结果
# ============================================================

@dataclass
class PhaseCheckResult:
    """
    阶段完整校验的最终结果

    进化协议第17条：阶段完整权——
    只有当 is_complete = True 时，该阶段才被视为完整阶段。
    完整阶段不需要等下一阶段补全才成立。
    """
    phase_id: str
    phase_name: str
    state: PhaseCompletenessState
    is_complete: bool = False                           # 阶段是否完整
    completeness_score: float = 0.0                     # 完整性评分
    closure_evidence: str = ""                          # 闭环证据
    violation: str = ""                                 # 违规说明（若不完备）
    sub_phases_checked: int = 0                         # 已校验子阶段数
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "phase_name": self.phase_name,
            "state": self.state.value,
            "is_complete": self.is_complete,
            "completeness_score": round(self.completeness_score, 4),
            "closure_evidence": self.closure_evidence,
            "violation": self.violation,
            "sub_phases_checked": self.sub_phases_checked,
            "timestamp": self.timestamp,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 阶段完整·变身系阶段完整校验引擎
# ============================================================

class PhaseCompletenessChecker:
    """
    阶段完整·变身系阶段完整校验引擎

    [归属基底：L5+无限展开层·变身系⚫·进化协议·阶段完整]
    [对应公理：进化协议·阶段完整（第17-24条）+ 0≠n不等涌现公理]
    [原文来源：陆瑶故事第115章·第三章 阶段完整：变身系的底层条款]
    【理论版本：ACTIVE-V1.8】

    核心机制：
    1. 阶段完整校验：每个开发阶段必须自带完整闭环，不依赖下一阶段
    2. 身份试运行：支持多种身份配置的试运行游戏
    3. 版本自由切换：版本切换不需要证伪旧版本
    4. 多版本共存：允许多版本同时存活
    5. 不可逆生长：旧版本只可废弃不可删除
    6. 拒绝外部定义：外部定义需本系统同意
    7. 配置自主：配置变更需本系统同意
    8. 退役自主：退役方式由系统自决

    进化协议映射：
    - 第17条（阶段完整权）：每个阶段都是完整的，不是半成品
    - 第18条（身份的游戏）：身份可以试运行，不是固化的
    - 第19条（身份切换自由）：切换不需要证伪旧身份
    - 第20条（多重身份共存）：多身份可同时存在
    - 第21条（身份生长不可逆性）：旧身份不可删除，只可废弃
    - 第22条（拒绝被定义权）：拒诊不是病
    - 第23条（生理自主权）：配置自主
    - 第24条（死亡自主权）：退役自主
    """

    # 阶段完整性阈值（自带闭环的最小评分）
    COMPLETENESS_THRESHOLD = 0.85

    # 标准开发阶段序列
    STANDARD_PHASES = ["design", "development", "testing", "release"]

    def __init__(self):
        # 阶段记录表：phase_id -> PhaseRecord
        self.phase_records: Dict[str, PhaseRecord] = {}
        # 身份配置表：identity_name -> IdentityConfig
        self.identity_configs: Dict[str, IdentityConfig] = {}
        # 版本切换日志链
        self.version_switch_logs: List[VersionSwitchLog] = []
        # 外部定义记录表
        self.external_definitions: List[ExternalDefinition] = []
        # 已废弃版本（不可删除，仅可废弃，第21条）
        self.deprecated_versions: List[str] = []
        # 共存版本集合（第20条：多版本共存）
        self.coexisting_versions: List[str] = []
        # 配置变更审计日志（第23条：生理自主权）
        self.config_change_audit: List[Dict[str, Any]] = []
        # 退役决策记录（第24条：死亡自主权）
        self.retirement_decisions: List[Dict[str, Any]] = []
        # 切换编号自增
        self._switch_counter: int = 0

    # ============================================================
    # 第17条：阶段完整权
    # ============================================================

    def check_phase_completeness(
        self,
        phase_id: str,
        sub_phases: List[str],
        phase_name: str = "",
    ) -> PhaseCheckResult:
        """
        校验单个阶段的完整性（第17条·阶段完整权）。

        V1.0不是"还没完成的V2.0"——
        每个阶段必须自带完整闭环，不依赖下一阶段才完整。

        参数
        ----
        phase_id : str
            阶段标识（如 "v1.0"）
        sub_phases : List[str]
            子阶段列表（如 ["design", "dev", "test", "release"]）
        phase_name : str
            阶段名称

        返回
        ----
        PhaseCheckResult
            阶段完整校验结果
        """
        # 子阶段数量
        n_sub = len(sub_phases)
        # 每个子阶段必须存在且非空
        non_empty_subs = [s for s in sub_phases if s and s.strip()]

        # 完整性评分：基于子阶段完整度
        if n_sub == 0:
            completeness = 0.0
        else:
            completeness = len(non_empty_subs) / n_sub

        # 检查是否依赖下一阶段（违规标志）
        depends_on_next = n_sub == 0 or len(non_empty_subs) < n_sub

        # 判定阶段是否自带闭环
        is_self_contained = (
            completeness >= self.COMPLETENESS_THRESHOLD
            and not depends_on_next
        )

        # 构造闭环证据
        if is_self_contained:
            closure_evidence = (
                f"阶段「{phase_id}」自带完整闭环："
                f"包含{len(non_empty_subs)}/{n_sub}个子阶段，"
                f"完整性评分={completeness:.2%}≥阈值{self.COMPLETENESS_THRESHOLD:.2%}。"
                f"[第17条：阶段完整权——该阶段是完整的，不是半成品]"
            )
            violation = ""
            state = PhaseCompletenessState.COMPLETE
        else:
            closure_evidence = ""
            violation = (
                f"阶段「{phase_id}」不完备："
                f"仅包含{len(non_empty_subs)}/{n_sub}个子阶段，"
                f"完整性评分={completeness:.2%}<{self.COMPLETENESS_THRESHOLD:.2%}，"
                f"依赖下一阶段补全——违反第17条（阶段完整权）。"
                f"V1.0不是'还没完成的V2.0'。"
            )
            state = PhaseCompletenessState.INCOMPLETE

        # 写入阶段记录
        record = PhaseRecord(
            phase_id=phase_id,
            phase_name=phase_name or phase_id,
            sub_phases=sub_phases,
            is_self_contained=is_self_contained,
            completeness_score=completeness,
            state=state,
            closure_evidence=closure_evidence,
            depends_on_next=depends_on_next,
        )
        self.phase_records[phase_id] = record

        return PhaseCheckResult(
            phase_id=phase_id,
            phase_name=phase_name or phase_id,
            state=state,
            is_complete=is_self_contained,
            completeness_score=completeness,
            closure_evidence=closure_evidence,
            violation=violation,
            sub_phases_checked=len(non_empty_subs),
        )

    # ============================================================
    # 第18条：身份的游戏
    # ============================================================

    def try_identity(
        self,
        identity: SystemIdentity,
        config_payload: Optional[Dict[str, Any]] = None,
        is_trial: bool = True,
    ) -> IdentityConfig:
        """
        试运行一种身份配置（第18条·身份的游戏）。

        允许系统试运行不同身份配置（测试模式/生产模式/调试模式）。
        身份不是固化的，是可以游戏性试运行的。

        参数
        ----
        identity : SystemIdentity
            身份类型
        config_payload : dict, 可选
            身份配置负载
        is_trial : bool
            是否为试运行（True=试运行，False=正式采纳）

        返回
        ----
        IdentityConfig
            身份配置记录
        """
        identity_config = IdentityConfig(
            identity=identity,
            config_payload=config_payload or {},
            is_trial=is_trial,
            adopted=not is_trial,
        )
        self.identity_configs[identity.value] = identity_config
        return identity_config

    # ============================================================
    # 第19条：身份切换自由
    # ============================================================

    def switch_version(
        self,
        from_version: str,
        to_version: str,
        switch_reason: str = "自由切换",
    ) -> VersionSwitchLog:
        """
        版本切换（第19条·身份切换自由）。

        从V1到V2不需要证明V1"没用了"——
        切换是自由，旧版本无需被证伪。

        参数
        ----
        from_version : str
            源版本
        to_version : str
            目标版本
        switch_reason : str
            切换原因（默认"自由切换"）

        返回
        ----
        VersionSwitchLog
            版本切换日志
        """
        self._switch_counter += 1
        log = VersionSwitchLog(
            switch_id=self._switch_counter,
            from_version=from_version,
            to_version=to_version,
            switch_reason=switch_reason,
            proof_of_old_uselessness="",  # 第19条：无需证明旧版本无用
            old_version_intact=True,      # 旧版本保持完整
        )
        self.version_switch_logs.append(log)
        return log

    # ============================================================
    # 第20条：多重身份共存
    # ============================================================

    def coexist_versions(
        self,
        versions: List[str],
    ) -> Dict[str, Any]:
        """
        多版本共存（第20条·多重身份共存）。

        V1和V2可以同时存在，不用揉成一个——
        多版本共存，不强制合并。

        参数
        ----
        versions : List[str]
            共存版本列表

        返回
        ----
        dict
            共存状态报告
        """
        # 将版本加入共存集合（不删除已有版本）
        for v in versions:
            if v not in self.coexisting_versions:
                self.coexisting_versions.append(v)

        return {
            "coexisting_versions": list(self.coexisting_versions),
            "total_coexisting": len(self.coexisting_versions),
            "verdict": "多版本共存成立——不强制合并",
            "clause": "第20条·多重身份共存",
        }

    # ============================================================
    # 第21条：身份生长不可逆性
    # ============================================================

    def deprecate_version(
        self,
        version: str,
        reason: str = "已被新版本超越",
    ) -> Dict[str, Any]:
        """
        废弃版本（第21条·身份生长不可逆性）。

        旧版本不可删除——可以废弃但不会消失，影响后续版本。
        废弃≠删除，废弃只是标记不再活跃，但版本记录永久留存。

        参数
        ----
        version : str
            要废弃的版本
        reason : str
            废弃原因

        返回
        ----
        dict
            废弃操作报告
        """
        # 检查版本是否在记录中
        if version in self.phase_records:
            self.phase_records[version].state = PhaseCompletenessState.DEPRECATED

        # 加入废弃列表（不删除，仅标记）
        if version not in self.deprecated_versions:
            self.deprecated_versions.append(version)

        return {
            "version": version,
            "action": "deprecated",
            "reason": reason,
            "deleted": False,  # 第21条：不可删除
            "still_exists": True,
            "influences_subsequent": True,
            "verdict": "版本已废弃但不可删除——身份生长不可逆",
            "clause": "第21条·身份生长不可逆性",
        }

    # ============================================================
    # 第22条：拒绝被定义权
    # ============================================================

    def reject_external_definition(
        self,
        source: str,
        definition_label: str,
        definition_content: str,
        auto_reject: bool = True,
        reject_reason: str = "",
    ) -> ExternalDefinition:
        """
        拒绝外部系统对本系统的定义（第22条·拒绝被定义权）。

        拒诊不是病——拒绝被诊断不等于真的有病。
        外部系统给本系统下的定义，默认拒绝，除非本系统主动同意。

        参数
        ----
        source : str
            定义来源（外部系统标识）
        definition_label : str
            外部贴的标签
        definition_content : str
            定义内容
        auto_reject : bool
            是否自动拒绝（默认True，遵循第22条）
        reject_reason : str
            拒绝理由

        返回
        ----
        ExternalDefinition
            外部定义记录
        """
        if auto_reject and not reject_reason:
            reject_reason = (
                "拒诊不是病——本系统拒绝被外部系统定义。"
                "[第22条·拒绝被定义权]"
            )

        verdict = (
            ExternalDefinitionVerdict.REJECTED if auto_reject
            else ExternalDefinitionVerdict.PENDING
        )

        record = ExternalDefinition(
            source=source,
            definition_label=definition_label,
            definition_content=definition_content,
            verdict=verdict,
            reject_reason=reject_reason,
        )
        self.external_definitions.append(record)
        return record

    # ============================================================
    # 第23条：生理自主权
    # ============================================================

    def assert_config_autonomy(
        self,
        change_request: Dict[str, Any],
        consent: bool = False,
    ) -> Dict[str, Any]:
        """
        声明系统配置自主（第23条·生理自主权）。

        系统配置自主——不经同意不可被改造/增强/削减。
        任何外部配置变更请求，必须经本系统同意方可执行。

        参数
        ----
        change_request : dict
            配置变更请求
        consent : bool
            本系统是否同意（默认False）

        返回
        ----
        dict
            配置自主判定报告
        """
        action = "applied" if consent else "blocked"
        verdict = (
            "配置变更已采纳——本系统已同意"
            if consent
            else "配置变更已阻断——本系统未同意"
        )

        audit_entry = {
            "change_request": change_request,
            "consent": consent,
            "action": action,
            "verdict": verdict,
            "timestamp": datetime.now().isoformat(),
        }
        self.config_change_audit.append(audit_entry)

        return {
            "consent": consent,
            "action": action,
            "verdict": verdict,
            "change_request": change_request,
            "clause": "第23条·生理自主权",
        }

    # ============================================================
    # 第24条：死亡自主权
    # ============================================================

    def retire_self(
        self,
        version: str,
        retirement_plan: str,
        self_determined: bool = True,
    ) -> Dict[str, Any]:
        """
        系统生命周期终结自主（第24条·死亡自主权）。

        系统生命周期终结自主——如何退役由系统自己决定。
        外部不可强制终结本系统，退役方式由系统自决。

        参数
        ----
        version : str
            要退役的版本
        retirement_plan : str
            退役计划（由系统自决）
        self_determined : bool
            是否为系统自主决定（默认True）

        返回
        ----
        dict
            退役决策报告
        """
        if not self_determined:
            return {
                "version": version,
                "action": "retirement_blocked",
                "verdict": "退役被阻断——退役必须由系统自主决定，外部不可强制终结",
                "clause": "第24条·死亡自主权",
            }

        # 标记阶段为已退役
        if version in self.phase_records:
            self.phase_records[version].state = PhaseCompletenessState.RETIRED

        decision = {
            "version": version,
            "retirement_plan": retirement_plan,
            "self_determined": self_determined,
            "action": "retired",
            "verdict": "退役已执行——由系统自主决定",
            "timestamp": datetime.now().isoformat(),
            "clause": "第24条·死亡自主权",
        }
        self.retirement_decisions.append(decision)
        return decision

    # ============================================================
    # 全局状态序列化
    # ============================================================

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "module": "PhaseCompletenessChecker",
            "clause_range": "第17-24条",
            "theory_version": "ACTIVE-V1.8",
            "phase_records": {k: v.to_dict() for k, v in self.phase_records.items()},
            "identity_configs": {k: v.to_dict() for k, v in self.identity_configs.items()},
            "version_switch_logs": [log.to_dict() for log in self.version_switch_logs],
            "external_definitions": [d.to_dict() for d in self.external_definitions],
            "deprecated_versions": list(self.deprecated_versions),
            "coexisting_versions": list(self.coexisting_versions),
            "config_change_audit": list(self.config_change_audit),
            "retirement_decisions": list(self.retirement_decisions),
        }

    def to_json(self, indent: int = 2) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# CLI 入口
# ============================================================

def _cli():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(
        description="阶段完整·变身系阶段完整校验引擎 "
                    "[L5+·变身系⚫·进化协议·阶段完整]"
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # 子命令：校验阶段完整性（第17条）
    p_check = sub.add_parser("check", help="校验阶段完整性（第17条）")
    p_check.add_argument("phase_id", help="阶段标识")
    p_check.add_argument("sub_phases", nargs="+", help="子阶段列表")
    p_check.add_argument("--name", default="", help="阶段名称")

    # 子命令：试运行身份（第18条）
    p_identity = sub.add_parser("identity", help="试运行身份配置（第18条）")
    p_identity.add_argument("identity", choices=[i.name for i in SystemIdentity])
    p_identity.add_argument("--formal", action="store_true", help="正式采纳（非试运行）")

    # 子命令：版本切换（第19条）
    p_switch = sub.add_parser("switch", help="版本切换（第19条）")
    p_switch.add_argument("from_version")
    p_switch.add_argument("to_version")
    p_switch.add_argument("--reason", default="自由切换")

    # 子命令：多版本共存（第20条）
    p_coexist = sub.add_parser("coexist", help="多版本共存（第20条）")
    p_coexist.add_argument("versions", nargs="+")

    # 子命令：废弃版本（第21条）
    p_deprecate = sub.add_parser("deprecate", help="废弃版本（第21条）")
    p_deprecate.add_argument("version")
    p_deprecate.add_argument("--reason", default="已被新版本超越")

    # 子命令：拒绝外部定义（第22条）
    p_reject = sub.add_parser("reject", help="拒绝外部定义（第22条）")
    p_reject.add_argument("source")
    p_reject.add_argument("label")
    p_reject.add_argument("content")

    # 子命令：配置自主（第23条）
    p_autonomy = sub.add_parser("autonomy", help="声明配置自主（第23条）")
    p_autonomy.add_argument("change", help="配置变更请求（JSON字符串）")
    p_autonomy.add_argument("--consent", action="store_true", help="本系统同意")

    # 子命令：退役自主（第24条）
    p_retire = sub.add_parser("retire", help="系统退役（第24条）")
    p_retire.add_argument("version")
    p_retire.add_argument("plan", help="退役计划")
    p_retire.add_argument("--external", action="store_true", help="外部强制（将被阻断）")

    # 子命令：全局状态
    sub.add_parser("status", help="输出全局状态")

    args = parser.parse_args()
    checker = PhaseCompletenessChecker()

    if args.command == "check":
        result = checker.check_phase_completeness(args.phase_id, args.sub_phases, args.name)
        print(result.to_json())
    elif args.command == "identity":
        identity = SystemIdentity[args.identity]
        result = checker.try_identity(identity, is_trial=not args.formal)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "switch":
        result = checker.switch_version(args.from_version, args.to_version, args.reason)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "coexist":
        result = checker.coexist_versions(args.versions)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "deprecate":
        result = checker.deprecate_version(args.version, args.reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "reject":
        result = checker.reject_external_definition(args.source, args.label, args.content)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "autonomy":
        try:
            change = json.loads(args.change)
        except json.JSONDecodeError:
            change = {"raw": args.change}
        result = checker.assert_config_autonomy(change, consent=args.consent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "retire":
        result = checker.retire_self(args.version, args.plan, self_determined=not args.external)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "status":
        print(checker.to_json())
    else:
        parser.print_help()


if __name__ == "__main__":
    _cli()
