"""
归属基底：第1重九界母科基底
对应公理：层级跃迁公理
对应九维维度：九界维度
理论原文出处：theory_base/L1_母科理论层/、theory_base/L2_子层扩展层/
固定数理常量：γ=0.92, κ=0.35, θ_evo=0.002

理论演化 Agent（L1-L2 推导）
—— 从 L0 公理推导 L1 母科理论、L2 子层扩展
   调用 bsd_engine.axioms.* 与 bsd_engine.theories.* 既有模块
"""
from typing import Any, Dict, List, Optional

from bsd_agents.base import BSDAgentBase, AgentMessage
from bsd_engine.axioms.twelve_bsd_axioms import get_all_axioms as get_bsd_axioms
from bsd_engine.axioms.seven_origin_axioms import get_all_axioms as get_origin_axioms
from bsd_engine.axioms.nine_special_axioms import get_all_axioms as get_special_axioms
from bsd_engine.axioms.three_meaning_axioms import get_all_axioms as get_meaning_axioms
from bsd_engine.axioms.eight_unification_axioms import get_all_axioms as get_unification_axioms
from bsd_engine.theories.t01_meta_origin_foundation import MetaOriginFoundation
from bsd_engine.theories.t25_fifty_four_dimension_matrix import FiftyFourDimensionMatrix
from bsd_engine.theories.t26_fifty_four_mother_disciplines import FiftyFourMotherDisciplines
from bsd_engine.core.theory_hub import TheoryHub
from bsd_engine.registry.constants import GAMMA, KAPPA, THETA_EVO


# 公理集取数函数注册表
_AXIOM_GETTERS = {
    "bsd": get_bsd_axioms,
    "origin": get_origin_axioms,
    "special": get_special_axioms,
    "meaning": get_meaning_axioms,
    "unification": get_unification_axioms,
}

# 层级 → 宇宙层级编码（对应 BaseTheoryModule.cosmic_level）
_LEVEL_MAP = {
    "L0": 0,
    "L1": 1,
    "L2": 2,
    "L3": 3,
}


class TheoryEvolutionAgent(BSDAgentBase):
    """
    理论演化 Agent（L1-L2 推导）

    职责：
    - derive_theory：从指定公理集推导目标层级的理论
    - list_mother_disciplines：列出 54 门母科（六系各九门）
    - get_theory_chain：获取理论推导依赖链
    - extend_theory：在基础理论上扩展子层分支
    """

    def __init__(self):
        super().__init__(
            name="TheoryEvolutionAgent",
            description="理论演化Agent（L1-L2推导）：从L0公理推导母科理论与子层扩展",
        )
        self._hub = TheoryHub()
        # 注册关键理论模块作为推导基底
        self._register_core_modules()

    def _register_core_modules(self) -> None:
        """注册核心理论模块到 TheoryHub。"""
        core_modules = [
            MetaOriginFoundation(),       # T1  L0 元道本源
            FiftyFourDimensionMatrix(),   # T25 L3 54维矩阵
            FiftyFourMotherDisciplines(), # T26 L3 54门母科
        ]
        for m in core_modules:
            try:
                self._hub.register(m)
            except Exception:
                # 重复注册或注册失败时静默跳过，保证流程不中断
                pass

    # ------------------------------------------------------------------
    # 公理 → 理论推导
    # ------------------------------------------------------------------
    def derive_theory(self, source_axioms: str, target_level: str) -> Dict[str, Any]:
        """
        从公理集推导目标层级的理论。

        参数
        ----
        source_axioms : str
            源公理集名称（bsd/origin/special/meaning/unification）
        target_level : str
            目标层级标签："L0"/"L1"/"L2"/"L3"

        返回
        ----
        dict
            {
                "source_axioms": str,
                "axiom_count": int,
                "target_level": str,
                "level_code": int,
                "derived_theories": [...],   # 该层级已注册理论
                "derivation_constants": {...},
            }
        """
        getter = _AXIOM_GETTERS.get(source_axioms)
        if getter is None:
            return {
                "error": f"未知公理集: {source_axioms}",
                "valid_sets": list(_AXIOM_GETTERS.keys()),
            }
        level_code = _LEVEL_MAP.get(target_level)
        if level_code is None:
            return {
                "error": f"未知目标层级: {target_level}",
                "valid_levels": list(_LEVEL_MAP.keys()),
            }

        axioms = getter()
        # 按 cosmic_level 取该层级理论
        try:
            level_modules = self._hub.get_by_level(level_code)
        except Exception:
            level_modules = []

        derived = [
            {
                "module_id": m.module_id,
                "module_name": getattr(m, "module_name", ""),
                "base_belong": getattr(m, "base_belong", ""),
                "corresponding_axiom": getattr(m, "corresponding_axiom", ""),
                "dependencies": list(getattr(m, "dependencies", []) or []),
            }
            for m in level_modules
        ]

        return {
            "source_axioms": source_axioms,
            "axiom_count": len(axioms),
            "axiom_names": [a.name for a in axioms],
            "target_level": target_level,
            "level_code": level_code,
            "derived_theories": derived,
            "derivation_constants": {
                "GAMMA": GAMMA,
                "KAPPA": KAPPA,
                "THETA_EVO": THETA_EVO,
            },
        }

    # ------------------------------------------------------------------
    # 列出 54 门母科
    # ------------------------------------------------------------------
    def list_mother_disciplines(self) -> Dict[str, Any]:
        """
        列出 54 门母科（六系各九门）。

        返回 T26 推演出的 54 母科体系结构。
        """
        module = FiftyFourMotherDisciplines()
        try:
            construction = module.discipline_system_construction()
        except Exception as exc:  # noqa: BLE001 - 容错保护
            construction = {"error": str(exc)}
        return {
            "total_disciplines": construction.get("total_disciplines", 54),
            "expected_disciplines": construction.get("expected_disciplines", 54),
            "six_systems": construction.get("six_systems", module.six_systems),
            "five_theories": construction.get("five_theories", module.five_theories),
            "system_summary": construction.get("system_summary", {}),
            "all_disciplines": construction.get("all_disciplines", []),
        }

    # ------------------------------------------------------------------
    # 获取理论推导链
    # ------------------------------------------------------------------
    def get_theory_chain(self, theory_id: str) -> Dict[str, Any]:
        """
        获取指定理论的推导依赖链。

        参数
        ----
        theory_id : str
            理论模块 ID，如 "T1"/"T25"/"T26"

        返回
        ----
        dict
            {
                "theory_id": str,
                "found": bool,
                "chain": [{"module_id","module_name","dependencies"}, ...],
            }
        """
        module = self._hub.get(theory_id)
        if module is None:
            return {
                "theory_id": theory_id,
                "found": False,
                "chain": [],
                "error": f"未注册理论: {theory_id}",
            }

        chain: List[Dict[str, Any]] = []
        visited = set()

        def _walk(mod: Any, depth: int) -> None:
            if mod.module_id in visited:
                return
            visited.add(mod.module_id)
            chain.append({
                "module_id": mod.module_id,
                "module_name": getattr(mod, "module_name", ""),
                "cosmic_level": getattr(mod, "cosmic_level", -1),
                "dependencies": list(getattr(mod, "dependencies", []) or []),
                "depth": depth,
            })
            for dep_id in (getattr(mod, "dependencies", None) or []):
                dep_mod = self._hub.get(dep_id)
                if dep_mod is not None:
                    _walk(dep_mod, depth + 1)

        _walk(module, 0)
        return {
            "theory_id": theory_id,
            "found": True,
            "chain": chain,
        }

    # ------------------------------------------------------------------
    # 扩展理论分支
    # ------------------------------------------------------------------
    def extend_theory(self, base_theory: str, extension_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        在基础理论上扩展子层分支。

        参数
        ----
        base_theory : str
            基础理论模块 ID（如 "T26"）
        extension_params : dict
            扩展参数，可包含：
            - branch_name : 分支名称
            - target_level : 目标子层（L1/L2/L3）
            - extra_dimensions : 附加维度列表
            - notes : 备注

        返回
        ----
        dict
            扩展分支记录（含基理论信息与扩展参数合并结果）
        """
        base_module = self._hub.get(base_theory)
        if base_module is None:
            return {
                "base_theory": base_theory,
                "success": False,
                "error": f"未注册基础理论: {base_theory}",
            }

        branch_name = extension_params.get("branch_name", "unnamed_branch")
        target_level = extension_params.get("target_level", "L2")
        level_code = _LEVEL_MAP.get(target_level, 2)

        extension_record = {
            "base_theory": base_theory,
            "base_name": getattr(base_module, "module_name", ""),
            "base_cosmic_level": getattr(base_module, "cosmic_level", -1),
            "branch_name": branch_name,
            "target_level": target_level,
            "target_level_code": level_code,
            "extra_dimensions": extension_params.get("extra_dimensions", []),
            "notes": extension_params.get("notes", ""),
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "THETA_EVO": THETA_EVO},
            "success": True,
        }
        return extension_record

    # ------------------------------------------------------------------
    # 消息处理
    # ------------------------------------------------------------------
    def process(self) -> List[Dict[str, Any]]:
        """
        处理消息队列中的推导请求。

        支持的 content.action：
        - "derive_theory"          content.source_axioms / content.target_level
        - "list_mother_disciplines"
        - "get_theory_chain"       content.theory_id
        - "extend_theory"          content.base_theory / content.extension_params
        """
        results: List[Dict[str, Any]] = []
        while self.message_queue:
            msg: AgentMessage = self.message_queue.pop(0)
            content = msg.content if isinstance(msg.content, dict) else {}
            action = content.get("action", "")
            try:
                if action == "derive_theory":
                    res = self.derive_theory(
                        content.get("source_axioms", ""),
                        content.get("target_level", ""),
                    )
                elif action == "list_mother_disciplines":
                    res = self.list_mother_disciplines()
                elif action == "get_theory_chain":
                    res = self.get_theory_chain(content.get("theory_id", ""))
                elif action == "extend_theory":
                    res = self.extend_theory(
                        content.get("base_theory", ""),
                        content.get("extension_params", {}) or {},
                    )
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
