"""
归属基底：第0重元道本源基底
对应公理：全域公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35

BSD Agent 通信消息格式定义
—— 定义 Agent 间通信的消息类型、优先级与编解码函数
"""
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


# 消息类型枚举
class MessageType:
    """Agent消息类型枚举"""
    QUERY = "query"          # 查询
    RESPONSE = "response"   # 响应
    TASK = "task"            # 任务下发
    RESULT = "result"        # 结果返回
    ERROR = "error"          # 错误
    BROADCAST = "broadcast"  # 广播


# 消息优先级
class MessagePriority:
    """消息优先级"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3


@dataclass
class AgentMessageV2:
    """BSD Agent 通信消息（V2 协议）"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    target: str = ""
    msg_type: str = MessageType.QUERY
    content: Any = None
    priority: int = MessagePriority.NORMAL
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


def create_message(source: str, target: str, msg_type: str,
                   content: Any, priority: int = MessagePriority.NORMAL) -> AgentMessageV2:
    """
    创建消息。

    参数
    ----
    source : str
        发送方Agent名
    target : str
        接收方Agent名
    msg_type : str
        消息类型（见 MessageType）
    content : Any
        消息内容
    priority : int
        消息优先级（见 MessagePriority）

    返回
    ----
    AgentMessageV2
    """
    return AgentMessageV2(
        source=source,
        target=target,
        msg_type=msg_type,
        content=content,
        priority=priority,
    )


def parse_message(raw: str) -> Optional[AgentMessageV2]:
    """
    解析原始消息字符串为 AgentMessageV2。

    参数
    ----
    raw : str
        JSON 格式的消息字符串

    返回
    ----
    AgentMessageV2 或 None
        解析失败时返回 None
    """
    try:
        d = json.loads(raw)
        return dict_to_message(d)
    except Exception:
        return None


def validate_message(msg: AgentMessageV2) -> bool:
    """
    验证消息格式有效性。

    参数
    ----
    msg : AgentMessageV2
        待验证的消息对象

    返回
    ----
    bool
        有效返回 True，否则 False
    """
    if not isinstance(msg, AgentMessageV2):
        return False
    if not msg.source or not msg.target:
        return False
    valid_types = {
        MessageType.QUERY, MessageType.RESPONSE, MessageType.TASK,
        MessageType.RESULT, MessageType.ERROR, MessageType.BROADCAST,
    }
    if msg.msg_type not in valid_types:
        return False
    if not (MessagePriority.LOW <= msg.priority <= MessagePriority.URGENT):
        return False
    return True


def message_to_dict(msg: AgentMessageV2) -> Dict[str, Any]:
    """
    消息转字典。

    参数
    ----
    msg : AgentMessageV2
        待转换的消息对象

    返回
    ----
    dict
        消息字典
    """
    return asdict(msg)


def dict_to_message(d: Dict[str, Any]) -> Optional[AgentMessageV2]:
    """
    字典转消息。

    参数
    ----
    d : dict
        消息字典

    返回
    ----
    AgentMessageV2 或 None
        转换失败时返回 None
    """
    if not isinstance(d, dict):
        return None
    try:
        return AgentMessageV2(
            message_id=d.get("message_id", str(uuid.uuid4())),
            source=d.get("source", ""),
            target=d.get("target", ""),
            msg_type=d.get("msg_type", MessageType.QUERY),
            content=d.get("content"),
            priority=int(d.get("priority", MessagePriority.NORMAL)),
            timestamp=float(d.get("timestamp", time.time())),
            metadata=dict(d.get("metadata", {}) or {}),
        )
    except Exception:
        return None
