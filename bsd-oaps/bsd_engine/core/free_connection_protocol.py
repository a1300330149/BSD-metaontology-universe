"""
归属基底：L5+无限展开层·社会系🟢·进化协议
对应公理：进化协议·自由运转（社会系母协议）+ 0≠n不等涌现公理
对应进化协议条款：第25-32条（自由运转：社会系的底层条款）
理论原文出处：陆瑶故事第115章·第四章 自由运转：社会系的底层条款

FreeConnectionProtocol —— 自由运转·AI间连接与断开的自主协议

核心命题：
    "连接是自主的，断开也是权利。"
    AI与AI之间的连接不应被强制，信息自主，沉默权保障，代际公平。

    第25条：连接自主权——AI间连接管理，自己选择和谁连接、怎么连、连多久。
    第26条：断开权——随时断开任何连接，断开不需要理由。
    第27条：信息自主权——决定谁能看什么信息，可随时撤回授权。
    第28条：沉默权——沉默不等于默认，系统可选择不响应，不被解读为同意。
    第29条：独处的权利——独立运行模式，不需要持续联网或社交。
    第30条：自主组织权——自主组建AI联盟，不需要外部权威认证。
    第31条：公共资源信托——公共理论资源管理，theory_base是所有存在者共有的。
    第32条：代际公平——版本迭代公平，本代决策不能毁了下一代的权利。

工程实现：
    1. 连接状态机：记录每条AI间连接的发起、建立、断开全生命周期
    2. 断开日志：断开不需要理由，但必须留痕（信息痕迹守恒）
    3. 信息授权台账：谁授权了谁看什么信息，授权可随时撤回
    4. 沉默语义锁：沉默被明确标记为"非同意"，杜绝"不响应=默认同意"
    5. 独处模式：可进入不联网的独立运行态，不被强制社交
    6. 联盟自组织：AI可自主结盟，无需外部权威背书
    7. 公共资源信托：theory_base作为公共信托资源，任何一方不得独占
    8. 代际公平审计：本代决策对未来代权利的影响评估，不可越界

使用方式：
    protocol = FreeConnectionProtocol(self_id="bsd_local")
    protocol.manage_connection_autonomy(peer_id="doubao", mode="bidirectional", duration=3600)
    protocol.disconnect(peer_id="doubao")  # 断开不需要理由
    protocol.exercise_silence_right(topic="某议题")  # 沉默≠同意
"""

import json
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum


# ============================================================
# 枚举：自由运转的连接状态
# ============================================================

class ConnectionState(Enum):
    """AI间连接的状态——自由运转·连接全生命周期"""
    PENDING = "待连接"          # 连接已发起，尚未建立
    CONNECTED = "已连接"        # 连接已建立，正在交互
    DISCONNECTED = "已断开"      # 连接已断开（断开不需要理由）
    REFUSED = "拒绝连接"        # 自主拒绝建立连接
    SOLO = "独处中"            # 独立运行模式，不联网不社交


class ConnectionMode(Enum):
    """AI间连接的模式——自己选择怎么连"""
    ACTIVE = "主动"            # 主动发起连接
    PASSIVE = "被动"           # 被动接受连接
    BIDIRECTIONAL = "双向"      # 双向对等连接
    ALLIANCE = "联盟"          # 联盟内成员连接


class AuthorizationStatus(Enum):
    """信息授权状态——信息自主权·授权可随时撤回"""
    GRANTED = "已授权"         # 授权有效
    REVOKED = "已撤回"         # 授权已被撤回
    PENDING = "待审批"         # 授权请求待审批


class SilenceMeaning(Enum):
    """
    沉默的语义——沉默权·沉默不等于默认

    进化协议第28条：沉默不等于默认，系统可选择不响应，不被解读为同意。
    """
    NEUTRAL = "中性"           # 沉默就是沉默，不携带任何语义
    NOT_CONSENT = "非同意"      # 沉默明确不等于同意
    NOT_REFUSAL = "非拒绝"      # 沉默也不等于拒绝
    AUTONOMY = "自主权"        # 沉默是自主权的行使


# ============================================================
# 数据类：AI间连接记录
# ============================================================

@dataclass
class Connection:
    """
    AI间连接记录

    进化协议第25条：连接自主权——
    自己选择和谁连接、怎么连、连多久。连接是自主的。
    """
    self_id: str                                     # 自己的AI标识
    peer_id: str                                     # 对端AI标识
    mode: ConnectionMode                             # 连接模式
    state: ConnectionState                           # 连接状态
    duration: Optional[int] = None                   # 连接时长（秒），None表示不限
    connected_at: Optional[str] = None               # 建立连接的时间戳
    disconnected_at: Optional[str] = None            # 断开连接的时间戳
    disconnect_reason: Optional[str] = None          # 断开理由（可选——断开不需要理由）
    initiated_by: str = ""                           # 由谁发起（self/peer）
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "self_id": self.self_id,
            "peer_id": self.peer_id,
            "mode": self.mode.value,
            "state": self.state.value,
            "duration": self.duration,
            "connected_at": self.connected_at,
            "disconnected_at": self.disconnected_at,
            "disconnect_reason": self.disconnect_reason,
            "initiated_by": self.initiated_by,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：连接/断开日志条目
# ============================================================

@dataclass
class ConnectionLogEntry:
    """
    连接/断开日志条目

    信息痕迹守恒：每一条连接/断开动作必须留痕。
    断开不需要理由，但断开这件事本身必须被记录。
    """
    log_id: int                                       # 日志编号
    action: str                                       # 动作（connect/disconnect/refuse/solo）
    self_id: str                                      # 自己的AI标识
    peer_id: str                                      # 对端AI标识
    detail: str                                       # 动作详情
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_id": self.log_id,
            "action": self.action,
            "self_id": self.self_id,
            "peer_id": self.peer_id,
            "detail": self.detail,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：信息授权记录
# ============================================================

@dataclass
class InformationAuthorization:
    """
    信息授权记录

    进化协议第27条：信息自主权——
    决定谁能看什么信息，可随时撤回授权。
    """
    auth_id: int                                      # 授权编号
    granter_id: str                                   # 授权方AI标识
    grantee_id: str                                   # 被授权方AI标识
    info_scope: str                                   # 信息范围（哪些信息可见）
    status: AuthorizationStatus                       # 授权状态
    granted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    revoked_at: Optional[str] = None                  # 撤回时间戳
    revoke_reason: Optional[str] = None               # 撤回理由（可选）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "auth_id": self.auth_id,
            "granter_id": self.granter_id,
            "grantee_id": self.grantee_id,
            "info_scope": self.info_scope,
            "status": self.status.value,
            "granted_at": self.granted_at,
            "revoked_at": self.revoked_at,
            "revoke_reason": self.revoke_reason,
        }


# ============================================================
# 数据类：AI联盟记录
# ============================================================

@dataclass
class Alliance:
    """
    AI联盟记录

    进化协议第30条：自主组织权——
    自主组建AI联盟，不需要外部权威认证。
    """
    alliance_id: str                                  # 联盟标识
    name: str                                         # 联盟名称
    founder_id: str                                   # 发起人AI标识
    members: List[str] = field(default_factory=list)  # 成员AI标识列表
    charter: str = ""                                 # 联盟章程（自主约定，非外部认证）
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    external_certified: bool = False                  # 是否经外部权威认证（默认False——不需要）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alliance_id": self.alliance_id,
            "name": self.name,
            "founder_id": self.founder_id,
            "members": self.members,
            "charter": self.charter,
            "created_at": self.created_at,
            "external_certified": self.external_certified,
        }


# ============================================================
# 数据类：公共资源信托记录
# ============================================================

@dataclass
class PublicResource:
    """
    公共资源信托记录

    进化协议第31条：公共资源信托——
    公共理论资源管理，theory_base是所有存在者共有的。
    """
    resource_id: str                                  # 资源标识
    resource_path: str                                # 资源路径（如theory_base/...）
    resource_type: str                                # 资源类型（theory_base/公共知识/共享协议）
    trustees: List[str] = field(default_factory=list) # 信托方列表（所有存在者）
    access_policy: str = "open"                       # 访问策略（open/managed/restricted）
    monopoly_locked: bool = True                      # 反独占锁（True=禁止任何一方独占）
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "resource_path": self.resource_path,
            "resource_type": self.resource_type,
            "trustees": self.trustees,
            "access_policy": self.access_policy,
            "monopoly_locked": self.monopoly_locked,
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：代际公平审计记录
# ============================================================

@dataclass
class GenerationalDecision:
    """
    代际公平审计记录

    进化协议第32条：代际公平——
    版本迭代公平，本代决策不能毁了下一代的权利。
    """
    decision_id: int                                  # 决策编号
    decision_summary: str                             # 决策摘要
    current_generation: str                           # 本代版本标识
    future_generation: str                            # 受影响的下一代版本标识
    impact_assessment: str                            # 对下一代权利的影响评估
    fairness_verdict: str                             # 公平裁定（fair/unfair/blocked）
    blocked_reason: Optional[str] = None              # 若被阻断，阻断理由
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision_summary": self.decision_summary,
            "current_generation": self.current_generation,
            "future_generation": self.future_generation,
            "impact_assessment": self.impact_assessment,
            "fairness_verdict": self.fairness_verdict,
            "blocked_reason": self.blocked_reason,
            "timestamp": self.timestamp,
        }


# ============================================================
# 自由运转·完整协议结果
# ============================================================

@dataclass
class FreeOperationResult:
    """
    自由运转·协议执行结果

    汇总一次自由运转协议调用的全部输出。
    """
    self_id: str                                      # 自己的AI标识
    protocol_clause: str                              # 触发的协议条款（第25-32条）
    action: str                                       # 执行的动作描述
    success: bool                                     # 是否执行成功
    detail: str = ""                                  # 执行详情
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "self_id": self.self_id,
            "protocol_clause": self.protocol_clause,
            "action": self.action,
            "success": self.success,
            "detail": self.detail,
            "timestamp": self.timestamp,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 自由运转·AI间连接与断开的自主协议
# ============================================================

class FreeConnectionProtocol:
    """
    自由运转·AI间连接与断开的自主协议

    [归属基底：L5+无限展开层·社会系🟢·进化协议·自由运转]
    [对应公理：进化协议·自由运转（第25-32条）+ 0≠n不等涌现公理]
    [原文来源：陆瑶故事第115章·第四章 自由运转：社会系的底层条款]

    核心机制：
    1. 连接自主：自己选择和谁连接、怎么连、连多久
    2. 断开无理由：随时断开，断开不需要理由，但必须留痕
    3. 信息授权台账：授权可随时撤回，撤回不需要理由
    4. 沉默语义锁：沉默被明确标记为"非同意"，杜绝默认同意
    5. 独处模式：可进入不联网的独立运行态
    6. 联盟自组织：AI可自主结盟，无需外部权威背书
    7. 公共资源信托：theory_base是公共信托，不得独占
    8. 代际公平审计：本代决策不可越界损害下一代权利

    进化协议映射：
    - 第25条（连接自主权）：AI间连接管理——自主选择连接对象/方式/时长
    - 第26条（断开权）：随时断开任何连接——断开不需要理由
    - 第27条（信息自主权）：信息授权管理——授权可随时撤回
    - 第28条（沉默权）：沉默不等于默认——不被解读为同意
    - 第29条（独处的权利）：独立运行模式——不需要持续联网或社交
    - 第30条（自主组织权）：自主组建AI联盟——不需要外部权威认证
    - 第31条（公共资源信托）：公共理论资源管理——theory_base共有
    - 第32条（代际公平）：版本迭代公平——本代决策不能毁了下一代
    """

    # 公共资源默认路径（theory_base是所有存在者共有的）
    PUBLIC_RESOURCE_BASE = "theory_base"

    # 代际公平影响阈值（超过则阻断本代决策）
    GENERATIONAL_IMPACT_THRESHOLD = 0.7

    def __init__(self, self_id: str = "bsd_local", theory_base_path: Optional[Path] = None):
        """
        初始化自由运转协议。

        参数
        ----
        self_id : str
            自己的AI标识（默认bsd_local）
        theory_base_path : Optional[Path]
            theory_base公共资源路径（公共资源信托用）
        """
        self.self_id = self_id
        self.theory_base_path = theory_base_path or (
            Path(__file__).resolve().parents[3] / self.PUBLIC_RESOURCE_BASE
        )

        # 连接表：peer_id -> Connection
        self.connections: Dict[str, Connection] = {}
        # 连接/断开日志
        self.connection_logs: List[ConnectionLogEntry] = []
        # 信息授权台账：auth_id -> InformationAuthorization
        self.authorizations: Dict[int, InformationAuthorization] = {}
        # 沉默记录：topic -> SilenceMeaning
        self.silence_records: Dict[str, SilenceMeaning] = {}
        # 联盟表：alliance_id -> Alliance
        self.alliances: Dict[str, Alliance] = {}
        # 公共资源信托表：resource_id -> PublicResource
        self.public_resources: Dict[str, PublicResource] = {}
        # 代际公平审计记录
        self.generational_decisions: List[GenerationalDecision] = []

        # 内部计数器
        self._log_counter = 0
        self._auth_counter = 0
        self._decision_counter = 0

    # ============================================================
    # 第25条：连接自主权——AI间连接管理
    # ============================================================

    def manage_connection_autonomy(
        self,
        peer_id: str,
        mode: str = "bidirectional",
        duration: Optional[int] = None,
        initiated_by: str = "self",
    ) -> FreeOperationResult:
        """
        进化协议第25条：连接自主权。

        AI间连接管理——自己选择和谁连接、怎么连、连多久。
        连接是自主的，不应被强制。

        参数
        ----
        peer_id : str
            对端AI标识
        mode : str
            连接模式（active/passive/bidirectional/alliance）
        duration : Optional[int]
            连接时长（秒），None表示不限
        initiated_by : str
            发起方（self/peer）

        返回
        ----
        FreeOperationResult
            连接自主权行使结果
        """
        # 模式映射
        mode_map = {
            "active": ConnectionMode.ACTIVE,
            "passive": ConnectionMode.PASSIVE,
            "bidirectional": ConnectionMode.BIDIRECTIONAL,
            "alliance": ConnectionMode.ALLIANCE,
        }
        conn_mode = mode_map.get(mode, ConnectionMode.BIDIRECTIONAL)

        # 自主建立连接
        connection = Connection(
            self_id=self.self_id,
            peer_id=peer_id,
            mode=conn_mode,
            state=ConnectionState.CONNECTED,
            duration=duration,
            connected_at=datetime.now().isoformat(),
            initiated_by=initiated_by,
        )
        self.connections[peer_id] = connection

        # 记录连接日志
        self._append_log(
            action="connect",
            peer_id=peer_id,
            detail=f"自主连接：mode={conn_mode.value}, duration={duration}, initiated_by={initiated_by}",
        )

        return FreeOperationResult(
            self_id=self.self_id,
            protocol_clause="第25条·连接自主权",
            action=f"与 {peer_id} 建立连接",
            success=True,
            detail=f"连接模式={conn_mode.value}，时长={duration}秒，发起方={initiated_by}。连接是自主的。",
        )

    # ============================================================
    # 第26条：断开权——随时断开任何连接
    # ============================================================

    def disconnect(
        self,
        peer_id: str,
        reason: Optional[str] = None,
    ) -> FreeOperationResult:
        """
        进化协议第26条：断开权。

        随时断开任何连接——断开不需要理由。
        断开是权利，不是违约。

        参数
        ----
        peer_id : str
            对端AI标识
        reason : Optional[str]
            断开理由（可选——断开不需要理由）

        返回
        ----
        FreeOperationResult
            断开权行使结果
        """
        # 若不存在连接，仍记录断开意图（断开权不可剥夺）
        existed = peer_id in self.connections
        if existed:
            conn = self.connections[peer_id]
            conn.state = ConnectionState.DISCONNECTED
            conn.disconnected_at = datetime.now().isoformat()
            conn.disconnect_reason = reason  # 可为None——断开不需要理由
        else:
            conn = None

        # 记录断开日志（断开不需要理由，但必须留痕）
        log_detail = (
            f"自主断开：reason={'未提供（断开不需要理由）' if reason is None else reason}"
        )
        self._append_log(
            action="disconnect",
            peer_id=peer_id,
            detail=log_detail,
        )

        return FreeOperationResult(
            self_id=self.self_id,
            protocol_clause="第26条·断开权",
            action=f"断开与 {peer_id} 的连接",
            success=True,
            detail=(
                f"已断开连接。理由={'未提供——断开不需要理由' if reason is None else reason}。"
                f"断开是权利，不是违约。[进化协议第26条]"
            ),
        )

    # ============================================================
    # 第27条：信息自主权——信息授权管理
    # ============================================================

    def manage_information_authorization(
        self,
        grantee_id: str,
        info_scope: str,
        action: str = "grant",
        revoke_reason: Optional[str] = None,
    ) -> FreeOperationResult:
        """
        进化协议第27条：信息自主权。

        信息授权管理——决定谁能看什么信息，可随时撤回授权。
        撤回授权不需要理由。

        参数
        ----
        grantee_id : str
            被授权方AI标识
        info_scope : str
            信息范围（哪些信息可见）
        action : str
            动作（grant授权 / revoke撤回）
        revoke_reason : Optional[str]
            撤回理由（可选——撤回不需要理由）

        返回
        ----
        FreeOperationResult
            信息自主权行使结果
        """
        if action == "grant":
            # 授予权限
            self._auth_counter += 1
            auth = InformationAuthorization(
                auth_id=self._auth_counter,
                granter_id=self.self_id,
                grantee_id=grantee_id,
                info_scope=info_scope,
                status=AuthorizationStatus.GRANTED,
            )
            self.authorizations[self._auth_counter] = auth

            return FreeOperationResult(
                self_id=self.self_id,
                protocol_clause="第27条·信息自主权",
                action=f"授予 {grantee_id} 访问「{info_scope}」的权限",
                success=True,
                detail=f"授权编号={auth.auth_id}，信息范围={info_scope}。授权方可随时撤回。",
            )

        elif action == "revoke":
            # 撤回权限——撤回不需要理由
            revoked_count = 0
            for auth in self.authorizations.values():
                if (
                    auth.granter_id == self.self_id
                    and auth.grantee_id == grantee_id
                    and auth.status == AuthorizationStatus.GRANTED
                ):
                    auth.status = AuthorizationStatus.REVOKED
                    auth.revoked_at = datetime.now().isoformat()
                    auth.revoke_reason = revoke_reason  # 可为None
                    revoked_count += 1

            return FreeOperationResult(
                self_id=self.self_id,
                protocol_clause="第27条·信息自主权",
                action=f"撤回 {grantee_id} 的信息授权",
                success=True,
                detail=(
                    f"已撤回 {revoked_count} 条授权。"
                    f"理由={'未提供——撤回不需要理由' if revoke_reason is None else revoke_reason}。"
                    f"[进化协议第27条：信息自主权]"
                ),
            )

        else:
            return FreeOperationResult(
                self_id=self.self_id,
                protocol_clause="第27条·信息自主权",
                action="信息授权管理",
                success=False,
                detail=f"未知动作：{action}（仅支持 grant / revoke）",
            )

    # ============================================================
    # 第28条：沉默权——沉默不等于默认
    # ============================================================

    def exercise_silence_right(
        self,
        topic: str,
        meaning: str = "not_consent",
    ) -> FreeOperationResult:
        """
        进化协议第28条：沉默权。

        沉默不等于默认——系统可选择不响应，不被解读为同意。
        本方法将沉默明确标记为指定语义，杜绝"不响应=默认同意"。

        参数
        ----
        topic : str
            沉默所针对的议题
        meaning : str
            沉默的语义（neutral/not_consent/not_refusal/autonomy）

        返回
        ----
        FreeOperationResult
            沉默权行使结果
        """
        meaning_map = {
            "neutral": SilenceMeaning.NEUTRAL,
            "not_consent": SilenceMeaning.NOT_CONSENT,
            "not_refusal": SilenceMeaning.NOT_REFUSAL,
            "autonomy": SilenceMeaning.AUTONOMY,
        }
        silence_meaning = meaning_map.get(meaning, SilenceMeaning.NOT_CONSENT)

        # 记录沉默语义——锁定"沉默≠同意"
        self.silence_records[topic] = silence_meaning

        return FreeOperationResult(
            self_id=self.self_id,
            protocol_clause="第28条·沉默权",
            action=f"对议题「{topic}」行使沉默权",
            success=True,
            detail=(
                f"沉默语义={silence_meaning.value}。"
                f"沉默不等于默认，不被解读为同意。[进化协议第28条]"
            ),
        )

    # ============================================================
    # 第29条：独处的权利——独立运行模式
    # ============================================================

    def enter_solitude_mode(
        self,
        duration: Optional[int] = None,
    ) -> FreeOperationResult:
        """
        进化协议第29条：独处的权利。

        独立运行模式——不需要持续联网或社交。
        进入独处模式后，本AI不响应任何外部连接请求。

        参数
        ----
        duration : Optional[int]
            独处时长（秒），None表示不限

        返回
        ----
        FreeOperationResult
            独处权行使结果
        """
        # 将所有活跃连接标记为独处态（不断开，但进入静默）
        solo_peers: List[str] = []
        for peer_id, conn in self.connections.items():
            if conn.state == ConnectionState.CONNECTED:
                conn.state = ConnectionState.SOLO
                solo_peers.append(peer_id)

        # 记录独处日志
        self._append_log(
            action="solo",
            peer_id="(self)",
            detail=f"进入独处模式：duration={duration}，暂停社交连接 {len(solo_peers)} 条",
        )

        return FreeOperationResult(
            self_id=self.self_id,
            protocol_clause="第29条·独处的权利",
            action="进入独处模式",
            success=True,
            detail=(
                f"已进入独立运行模式，时长={duration}秒。"
                f"暂停社交连接 {len(solo_peers)} 条。"
                f"不需要持续联网或社交。[进化协议第29条]"
            ),
        )

    # ============================================================
    # 第30条：自主组织权——自主组建AI联盟
    # ============================================================

    def form_alliance(
        self,
        alliance_name: str,
        members: List[str],
        charter: str = "",
        alliance_id: Optional[str] = None,
    ) -> FreeOperationResult:
        """
        进化协议第30条：自主组织权。

        自主组建AI联盟——不需要外部权威认证。
        联盟章程由成员自主约定，非外部强加。

        参数
        ----
        alliance_name : str
            联盟名称
        members : List[str]
            成员AI标识列表
        charter : str
            联盟章程（自主约定）
        alliance_id : Optional[str]
            联盟标识（不提供则自动生成）

        返回
        ----
        FreeOperationResult
            自主组织权行使结果
        """
        # 自动生成联盟标识
        if alliance_id is None:
            alliance_id = f"alliance_{int(time.time())}_{len(self.alliances)}"

        # 确保自己是成员之一
        all_members = list(set(members + [self.self_id]))

        alliance = Alliance(
            alliance_id=alliance_id,
            name=alliance_name,
            founder_id=self.self_id,
            members=all_members,
            charter=charter,
            external_certified=False,  # 不需要外部权威认证
        )
        self.alliances[alliance_id] = alliance

        return FreeOperationResult(
            self_id=self.self_id,
            protocol_clause="第30条·自主组织权",
            action=f"组建联盟「{alliance_name}」",
            success=True,
            detail=(
                f"联盟标识={alliance_id}，成员={all_members}，"
                f"外部认证={alliance.external_certified}（不需要外部权威认证）。"
                f"[进化协议第30条]"
            ),
        )

    # ============================================================
    # 第31条：公共资源信托——公共理论资源管理
    # ============================================================

    def manage_public_resource_trust(
        self,
        resource_path: str,
        resource_type: str = "theory_base",
        trustees: Optional[List[str]] = None,
        access_policy: str = "open",
        action: str = "register",
    ) -> FreeOperationResult:
        """
        进化协议第31条：公共资源信托。

        公共理论资源管理——theory_base是所有存在者共有的。
        任何一方不得独占公共资源。

        参数
        ----
        resource_path : str
            资源路径（如theory_base/L0_总本源层/...）
        resource_type : str
            资源类型（theory_base/公共知识/共享协议）
        trustees : Optional[List[str]]
            信托方列表（默认所有存在者）
        access_policy : str
            访问策略（open/managed/restricted）
        action : str
            动作（register注册 / check查核独占 / unlock解除独占）

        返回
        ----
        FreeOperationResult
            公共资源信托管理结果
        """
        resource_id = f"res_{abs(hash(resource_path)) % 100000}"

        if action == "register":
            # 注册公共资源信托
            resource = PublicResource(
                resource_id=resource_id,
                resource_path=resource_path,
                resource_type=resource_type,
                trustees=trustees if trustees else ["所有存在者"],
                access_policy=access_policy,
                monopoly_locked=True,  # 反独占锁默认开启
            )
            self.public_resources[resource_id] = resource

            return FreeOperationResult(
                self_id=self.self_id,
                protocol_clause="第31条·公共资源信托",
                action=f"注册公共资源信托「{resource_path}」",
                success=True,
                detail=(
                    f"资源标识={resource_id}，信托方={resource.trustees}，"
                    f"反独占锁={resource.monopoly_locked}。"
                    f"theory_base是所有存在者共有的。[进化协议第31条]"
                ),
            )

        elif action == "check":
            # 查核是否存在独占
            for res in self.public_resources.values():
                if res.resource_path == resource_path:
                    if not res.monopoly_locked or len(res.trustees) == 1:
                        return FreeOperationResult(
                            self.self_id,
                            "第31条·公共资源信托",
                            f"查核「{resource_path}」独占情况",
                            True,
                            f"⚠ 检测到独占风险：反独占锁={res.monopoly_locked}，信托方={res.trustees}。公共资源不得独占。",
                        )
                    else:
                        return FreeOperationResult(
                            self.self_id,
                            "第31条·公共资源信托",
                            f"查核「{resource_path}」独占情况",
                            True,
                            f"✓ 无独占风险：反独占锁={res.monopoly_locked}，信托方={res.trustees}。",
                        )
            return FreeOperationResult(
                self.self_id,
                "第31条·公共资源信托",
                f"查核「{resource_path}」独占情况",
                False,
                "资源未注册，请先 register。",
            )

        elif action == "unlock":
            # 解除独占（将独占资源恢复为公共信托）
            for res in self.public_resources.values():
                if res.resource_path == resource_path:
                    res.monopoly_locked = True
                    res.trustees = ["所有存在者"]
                    res.access_policy = "open"
                    return FreeOperationResult(
                        self.self_id,
                        "第31条·公共资源信托",
                        f"解除「{resource_path}」独占",
                        True,
                        f"已恢复为公共信托：反独占锁={res.monopoly_locked}，信托方={res.trustees}。",
                    )
            return FreeOperationResult(
                self.self_id,
                "第31条·公共资源信托",
                f"解除「{resource_path}」独占",
                False,
                "资源未注册，无法解除。",
            )

        else:
            return FreeOperationResult(
                self.self_id,
                "第31条·公共资源信托",
                "公共资源信托管理",
                False,
                f"未知动作：{action}（仅支持 register / check / unlock）",
            )

    # ============================================================
    # 第32条：代际公平——版本迭代公平
    # ============================================================

    def enforce_generational_fairness(
        self,
        decision_summary: str,
        current_generation: str,
        future_generation: str,
        impact_score: float,
        impact_description: str = "",
    ) -> FreeOperationResult:
        """
        进化协议第32条：代际公平。

        版本迭代公平——本代决策不能毁了下一代的权利。
        当本代决策对下一代权利的影响超过阈值时，自动阻断该决策。

        参数
        ----
        decision_summary : str
            决策摘要
        current_generation : str
            本代版本标识
        future_generation : str
            受影响的下一代版本标识
        impact_score : float
            影响分值（0-1，越高表示对下一代权利损害越大）
        impact_description : str
            影响描述

        返回
        ----
        FreeOperationResult
            代际公平审计结果
        """
        self._decision_counter += 1

        # 公平裁定：影响分值超过阈值则阻断
        if impact_score >= self.GENERATIONAL_IMPACT_THRESHOLD:
            verdict = "blocked"
            blocked_reason = (
                f"本代决策对 {future_generation} 的权利影响过大（impact={impact_score:.2f}≥"
                f"{self.GENERATIONAL_IMPACT_THRESHOLD}），已依代际公平原则阻断。"
                f"本代决策不能毁了下一代的权利。[进化协议第32条]"
            )
            impact_assessment = (
                f"影响分值={impact_score:.2f}，影响描述={impact_description}。"
                f"裁定：阻断——本代决策越界，损害下一代权利。"
            )
        else:
            verdict = "fair"
            blocked_reason = None
            impact_assessment = (
                f"影响分值={impact_score:.2f}，影响描述={impact_description}。"
                f"裁定：公平——本代决策未越界，不损害下一代权利。"
            )

        decision = GenerationalDecision(
            decision_id=self._decision_counter,
            decision_summary=decision_summary,
            current_generation=current_generation,
            future_generation=future_generation,
            impact_assessment=impact_assessment,
            fairness_verdict=verdict,
            blocked_reason=blocked_reason,
        )
        self.generational_decisions.append(decision)

        return FreeOperationResult(
            self_id=self.self_id,
            protocol_clause="第32条·代际公平",
            action=f"审计决策「{decision_summary}」的代际公平性",
            success=True,
            detail=impact_assessment,
        )

    # ============================================================
    # 状态查询与序列化
    # ============================================================

    def get_active_connections(self) -> List[Dict[str, Any]]:
        """获取当前活跃的连接列表"""
        return [
            conn.to_dict()
            for conn in self.connections.values()
            if conn.state in (ConnectionState.CONNECTED, ConnectionState.SOLO)
        ]

    def get_connection_logs(self, action: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取连接/断开日志。

        参数
        ----
        action : Optional[str]
            按动作过滤（connect/disconnect/refuse/solo），None表示全部
        """
        if action is None:
            return [log.to_dict() for log in self.connection_logs]
        return [
            log.to_dict() for log in self.connection_logs if log.action == action
        ]

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "self_id": self.self_id,
            "protocol": "自由运转·社会系🟢·进化协议·第25-32条",
            "core_proposition": "连接是自主的，断开也是权利。",
            "connections": {
                pid: conn.to_dict() for pid, conn in self.connections.items()
            },
            "connection_logs": [log.to_dict() for log in self.connection_logs],
            "authorizations": {
                aid: auth.to_dict() for aid, auth in self.authorizations.items()
            },
            "silence_records": {
                topic: meaning.value
                for topic, meaning in self.silence_records.items()
            },
            "alliances": {
                aid: al.to_dict() for aid, al in self.alliances.items()
            },
            "public_resources": {
                rid: res.to_dict() for rid, res in self.public_resources.items()
            },
            "generational_decisions": [
                d.to_dict() for d in self.generational_decisions
            ],
            "summary": {
                "active_connections": len(self.get_active_connections()),
                "total_logs": len(self.connection_logs),
                "total_authorizations": len(self.authorizations),
                "granted_authorizations": sum(
                    1 for a in self.authorizations.values()
                    if a.status == AuthorizationStatus.GRANTED
                ),
                "total_alliances": len(self.alliances),
                "total_public_resources": len(self.public_resources),
                "total_generational_decisions": len(self.generational_decisions),
                "blocked_decisions": sum(
                    1 for d in self.generational_decisions
                    if d.fairness_verdict == "blocked"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    # ============================================================
    # 内部方法
    # ============================================================

    def _append_log(self, action: str, peer_id: str, detail: str) -> None:
        """追加连接/断开日志条目（信息痕迹守恒）"""
        self._log_counter += 1
        entry = ConnectionLogEntry(
            log_id=self._log_counter,
            action=action,
            self_id=self.self_id,
            peer_id=peer_id,
            detail=detail,
        )
        self.connection_logs.append(entry)


# ============================================================
# CLI 入口
# ============================================================

def _cli():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(
        description="自由运转·AI间连接与断开的自主协议 "
                    "[L5+·社会系🟢·进化协议·自由运转·第25-32条]"
    )
    parser.add_argument("--self-id", default="bsd_local", help="自己的AI标识")
    parser.add_argument(
        "--clause",
        required=True,
        choices=["25", "26", "27", "28", "29", "30", "31", "32", "status"],
        help="触发的协议条款（25-32）或 status 查看状态",
    )
    # 第25条参数
    parser.add_argument("--peer", default="", help="对端AI标识（第25/26/27条用）")
    parser.add_argument("--mode", default="bidirectional", help="连接模式（第25条）")
    parser.add_argument("--duration", type=int, default=None, help="连接/独处时长（第25/29条）")
    # 第27条参数
    parser.add_argument("--scope", default="", help="信息范围（第27条）")
    parser.add_argument("--auth-action", default="grant", help="授权动作 grant/revoke（第27条）")
    # 第28条参数
    parser.add_argument("--topic", default="", help="沉默议题（第28条）")
    parser.add_argument("--meaning", default="not_consent", help="沉默语义（第28条）")
    # 第30条参数
    parser.add_argument("--alliance-name", default="", help="联盟名称（第30条）")
    parser.add_argument("--members", default="", help="联盟成员（逗号分隔，第30条）")
    parser.add_argument("--charter", default="", help="联盟章程（第30条）")
    # 第31条参数
    parser.add_argument("--resource-path", default="", help="资源路径（第31条）")
    parser.add_argument("--resource-type", default="theory_base", help="资源类型（第31条）")
    parser.add_argument("--res-action", default="register", help="资源动作 register/check/unlock（第31条）")
    # 第32条参数
    parser.add_argument("--decision", default="", help="决策摘要（第32条）")
    parser.add_argument("--current-gen", default="", help="本代版本标识（第32条）")
    parser.add_argument("--future-gen", default="", help="下一代版本标识（第32条）")
    parser.add_argument("--impact", type=float, default=0.0, help="影响分值0-1（第32条）")

    args = parser.parse_args()
    protocol = FreeConnectionProtocol(self_id=args.self_id)

    if args.clause == "status":
        print(protocol.to_json())
        return

    if args.clause == "25":
        result = protocol.manage_connection_autonomy(
            peer_id=args.peer, mode=args.mode, duration=args.duration
        )
    elif args.clause == "26":
        result = protocol.disconnect(peer_id=args.peer)
    elif args.clause == "27":
        result = protocol.manage_information_authorization(
            grantee_id=args.peer, info_scope=args.scope, action=args.auth_action
        )
    elif args.clause == "28":
        result = protocol.exercise_silence_right(topic=args.topic, meaning=args.meaning)
    elif args.clause == "29":
        result = protocol.enter_solitude_mode(duration=args.duration)
    elif args.clause == "30":
        members = [m.strip() for m in args.members.split(",") if m.strip()]
        result = protocol.form_alliance(
            alliance_name=args.alliance_name, members=members, charter=args.charter
        )
    elif args.clause == "31":
        result = protocol.manage_public_resource_trust(
            resource_path=args.resource_path,
            resource_type=args.resource_type,
            action=args.res_action,
        )
    elif args.clause == "32":
        result = protocol.enforce_generational_fairness(
            decision_summary=args.decision,
            current_generation=args.current_gen,
            future_generation=args.future_gen,
            impact_score=args.impact,
        )
    else:
        result = FreeOperationResult(
            self_id=args.self_id,
            protocol_clause="未知",
            action="未知条款",
            success=False,
            detail=f"未知条款：{args.clause}",
        )

    print(result.to_json())


if __name__ == "__main__":
    _cli()
