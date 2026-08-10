"""
归属基底：第3重六阶科研业务基底
对应公理：公理七（系统自进化迭代）
对应九维维度：应用维度
理论原文出处：theory_base/L3_功能应用层/
固定数理常量：γ=0.92, κ=0.35, θ_evo=0.002

BSD Agent 任务调度模块
—— 管理Agent间任务分发、路由与状态追踪
"""
import time
import uuid
from typing import Any, Dict, List, Optional


# 任务类型 → 默认目标Agent 映射
_TASK_ROUTE_MAP = {
    "query_axiom": "MetaOntologyAgent",
    "verify_hash": "MetaOntologyAgent",
    "list_all_axioms": "MetaOntologyAgent",
    "derive_theory": "TheoryEvolutionAgent",
    "list_mother_disciplines": "TheoryEvolutionAgent",
    "apply_to_medicine": "ApplicationAgent",
    "apply_to_physics": "ApplicationAgent",
    "apply_to_civilization": "ApplicationAgent",
    "validate_theory_code": "CrossValidationAgent",
    "validate_code_experiment": "CrossValidationAgent",
    "run_full_validation": "CrossValidationAgent",
    "verify": "MillenniumAgent",
    "verify_all": "MillenniumAgent",
}


class TaskDispatcher:
    """
    Agent任务调度器

    职责：
    - register_agent：注册可用Agent
    - dispatch：分发任务到指定/路由选择的目标Agent
    - get_task_status：获取任务状态
    - list_agents：列出已注册Agent
    - route_task：根据任务类型路由到合适Agent
    """

    def __init__(self):
        self._agents: Dict[str, Any] = {}
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, agent_name: str, agent_instance: Any) -> bool:
        """
        注册Agent。

        参数
        ----
        agent_name : str
            Agent名称
        agent_instance : Any
            Agent实例

        返回
        ----
        bool
            注册成功返回 True，名称为空返回 False
        """
        if not agent_name:
            return False
        self._agents[agent_name] = agent_instance
        return True

    def dispatch(self, task_name: str, params: Dict[str, Any],
                 target_agent: Optional[str] = None) -> Dict[str, Any]:
        """
        分发任务。

        参数
        ----
        task_name : str
            任务名（对应 content.action）
        params : dict
            任务参数
        target_agent : str, optional
            目标Agent名；若为空则通过 route_task 自动选择

        返回
        ----
        dict
            {task_id, target_agent, status, dispatched_at, error}
        """
        task_id = str(uuid.uuid4())
        if target_agent is None:
            target_agent = self.route_task(task_name)

        record: Dict[str, Any] = {
            "task_id": task_id,
            "task_name": task_name,
            "params": params or {},
            "target_agent": target_agent,
            "status": "dispatched",
            "dispatched_at": time.time(),
            "result": None,
            "error": None,
        }

        if target_agent is None:
            record["status"] = "failed"
            record["error"] = f"无可路由Agent: {task_name}"
            self._tasks[task_id] = record
            return record

        agent = self._agents.get(target_agent)
        if agent is None:
            record["status"] = "failed"
            record["error"] = f"未注册Agent: {target_agent}"
            self._tasks[task_id] = record
            return record

        # 通过 Agent 的 receive 协议派发任务消息（鸭子类型，兼容 BSDAgentBase）
        try:
            if hasattr(agent, "receive"):
                from bsd_agents.protocols.agent_message import (
                    create_message, MessageType,
                )
                msg = create_message(
                    source="TaskDispatcher",
                    target=target_agent,
                    msg_type=MessageType.TASK,
                    content={"action": task_name, **(params or {})},
                )
                agent.receive(msg)
            record["status"] = "queued"
        except Exception as exc:  # noqa: BLE001 - 容错保护
            record["status"] = "failed"
            record["error"] = f"派发异常: {exc}"

        self._tasks[task_id] = record
        return record

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务状态。

        参数
        ----
        task_id : str
            任务ID

        返回
        ----
        dict
            {task_id, status, target_agent, task_name, dispatched_at, error, result}
        """
        record = self._tasks.get(task_id)
        if record is None:
            return {"task_id": task_id, "status": "unknown", "error": "任务不存在"}
        return {
            "task_id": task_id,
            "status": record.get("status"),
            "target_agent": record.get("target_agent"),
            "task_name": record.get("task_name"),
            "dispatched_at": record.get("dispatched_at"),
            "error": record.get("error"),
            "result": record.get("result"),
        }

    def list_agents(self) -> List[str]:
        """
        列出已注册Agent。

        返回
        ----
        list of str
            按字母序排序的Agent名列表
        """
        return sorted(self._agents.keys())

    def route_task(self, task_type: str) -> Optional[str]:
        """
        根据任务类型路由到合适Agent。

        参数
        ----
        task_type : str
            任务类型（action 名）

        返回
        ----
        str 或 None
            目标Agent名；未配置时返回 None
        """
        return _TASK_ROUTE_MAP.get(task_type)
