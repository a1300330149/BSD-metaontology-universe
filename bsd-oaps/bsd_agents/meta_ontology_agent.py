"""
归属基底：第0重元道本源基底
对应公理：0元本体涌现公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35, HASH_SHA256 锁档不变

元本体推演 Agent（L0 锚定）
—— 负责 L0 公理锚定、基底哈希校验、0元本体信息查询与全部 39 条公理检索
   调用 bsd_engine.axioms.* 与 bsd_engine.validators.hash_checker 既有模块
"""
from typing import Any, Dict, List, Optional

from bsd_agents.base import BSDAgentBase, AgentMessage
from bsd_engine.axioms.twelve_bsd_axioms import get_all_axioms as get_bsd_axioms
from bsd_engine.axioms.seven_origin_axioms import get_all_axioms as get_origin_axioms
from bsd_engine.axioms.nine_special_axioms import get_all_axioms as get_special_axioms
from bsd_engine.axioms.three_meaning_axioms import get_all_axioms as get_meaning_axioms
from bsd_engine.axioms.eight_unification_axioms import get_all_axioms as get_unification_axioms
from bsd_engine.validators.hash_checker import verify_core_params
from bsd_engine.theories.t01_meta_origin_foundation import MetaOriginFoundation


# 公理集注册表：名称 → 取数函数
_AXIOM_SETS: Dict[str, Any] = {
    "bsd": get_bsd_axioms,
    "origin": get_origin_axioms,
    "special": get_special_axioms,
    "meaning": get_meaning_axioms,
    "unification": get_unification_axioms,
}

# 各公理集条目数（用于校验）：12 + 7 + 9 + 3 + 8 = 39
_AXIOM_SET_COUNTS: Dict[str, int] = {
    "bsd": 12,
    "origin": 7,
    "special": 9,
    "meaning": 3,
    "unification": 8,
}

TOTAL_AXIOMS = sum(_AXIOM_SET_COUNTS.values())  # 39


class MetaOntologyAgent(BSDAgentBase):
    """
    元本体推演 Agent（L0 锚定）

    职责：
    - L0 公理锚定：检索 5 个公理集共 39 条公理
    - 基底哈希校验：调用 verify_core_params 校验锁档核心参数未被篡改
    - 0元本体信息：基于 T1 元道本源基底理论提供本源属性
    - 公理查询：按 axiom_set + axiom_id 精确查询
    """

    def __init__(self):
        super().__init__(
            name="MetaOntologyAgent",
            description="元本体推演Agent（L0锚定）：公理检索、哈希校验、0元本体信息",
        )
        self._origin_module = MetaOriginFoundation()

    # ------------------------------------------------------------------
    # 公理查询
    # ------------------------------------------------------------------
    def query_axiom(self, axiom_set: str, axiom_id: int) -> Optional[Dict[str, Any]]:
        """
        查询指定公理集的指定公理。

        参数
        ----
        axiom_set : str
            公理集名称，取值：
            - "bsd"          12条BSD基础公理
            - "origin"        7大本源公理
            - "special"       9条特殊公理
            - "meaning"       3条意义公理
            - "unification"   8条统一公理
        axiom_id : int
            公理在所属集内的序号（从1开始）

        返回
        ----
        dict 或 None
            命中时返回 {"name", "description", "formula", "category"}，否则 None
        """
        getter = _AXIOM_SETS.get(axiom_set)
        if getter is None:
            return None
        axioms = getter()
        if not isinstance(axiom_id, int) or axiom_id < 1 or axiom_id > len(axioms):
            return None
        axiom = axioms[axiom_id - 1]
        return {
            "axiom_set": axiom_set,
            "axiom_id": axiom_id,
            "name": axiom.name,
            "description": axiom.description,
            "formula": axiom.formula,
            "category": axiom.category,
        }

    # ------------------------------------------------------------------
    # 哈希校验
    # ------------------------------------------------------------------
    def verify_hash(self) -> Dict[str, Any]:
        """
        执行基底哈希校验（锁档核心参数 + 理论库完整性）。

        返回
        ----
        dict
            {
                "core_params_passed": bool,
                "core_params_errors": List[str],
                "agent": self.name,
            }
        """
        passed, errors = verify_core_params()
        return {
            "core_params_passed": passed,
            "core_params_errors": errors,
            "agent": self.name,
        }

    # ------------------------------------------------------------------
    # 0元本体信息
    # ------------------------------------------------------------------
    def get_origin_info(self) -> Dict[str, Any]:
        """
        获取 0 元本体（元道本源）信息，基于 T1 元道本源基底理论。

        返回元道三重态、本源属性、自证闭环度等结构化信息。
        """
        module = self._origin_module
        info: Dict[str, Any] = {
            "module_id": module.module_id,
            "module_name": module.module_name,
            "base_belong": module.base_belong,
            "corresponding_axiom": module.corresponding_axiom,
            "cosmic_level": module.cosmic_level,
            "is_origin_locked": module.is_origin_locked,
            "meta_states": getattr(module, "meta_states", {}),
            "origin_attributes": {},
        }
        # 调用 T1 既有推演方法（若存在）
        if hasattr(module, "meta_origin_attributes"):
            try:
                info["origin_attributes"] = module.meta_origin_attributes()
            except Exception as exc:  # noqa: BLE001 - 容错保护
                info["origin_attributes"] = {"error": str(exc)}
        return info

    # ------------------------------------------------------------------
    # 列出全部 39 条公理
    # ------------------------------------------------------------------
    def list_all_axioms(self) -> Dict[str, Any]:
        """
        列出全部 39 条公理（5 个公理集）。

        返回
        ----
        dict
            {
                "total": 39,
                "set_counts": {...},
                "axioms": {
                    "bsd": [...],
                    "origin": [...],
                    "special": [...],
                    "meaning": [...],
                    "unification": [...],
                }
            }
        """
        all_axioms: Dict[str, List[Dict[str, Any]]] = {}
        for set_name, getter in _AXIOM_SETS.items():
            all_axioms[set_name] = [
                {
                    "id": idx + 1,
                    "name": a.name,
                    "description": a.description,
                    "formula": a.formula,
                    "category": a.category,
                }
                for idx, a in enumerate(getter())
            ]
        return {
            "total": TOTAL_AXIOMS,
            "set_counts": dict(_AXIOM_SET_COUNTS),
            "axioms": all_axioms,
        }

    # ------------------------------------------------------------------
    # 消息处理
    # ------------------------------------------------------------------
    def process(self) -> List[Dict[str, Any]]:
        """
        处理消息队列中的查询请求。

        支持的 content.action：
        - "query_axiom"      content.axiom_set / content.axiom_id
        - "verify_hash"
        - "get_origin_info"
        - "list_all_axioms"
        """
        results: List[Dict[str, Any]] = []
        while self.message_queue:
            msg: AgentMessage = self.message_queue.pop(0)
            content = msg.content if isinstance(msg.content, dict) else {}
            action = content.get("action", "")
            try:
                if action == "query_axiom":
                    res = self.query_axiom(
                        content.get("axiom_set", ""),
                        int(content.get("axiom_id", 0)),
                    )
                elif action == "verify_hash":
                    res = self.verify_hash()
                elif action == "get_origin_info":
                    res = self.get_origin_info()
                elif action == "list_all_axioms":
                    res = self.list_all_axioms()
                else:
                    res = {"error": f"未知 action: {action}"}
            except Exception as exc:  # noqa: BLE001 - 容错保护
                res = {"error": str(exc), "action": action}
            results.append({
                "message_id": msg.message_id,
                "action": action,
                "result": res,
            })
        return results
