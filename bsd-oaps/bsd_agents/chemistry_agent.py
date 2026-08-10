"""
归属基底：第3重六阶科研业务基底
对应公理：公理七（系统自进化迭代公理）
对应九维维度：应用维度
理论原文出处：T87第二十七章（化学全域难题BSD统一证明）
固定数理常量：γ=0.92, κ=0.35, α=0.18

化学全域难题验证 Agent（14个难题统一验证）
—— 调用 bsd_verify.chemistry 验证器
   基于 BSD 全域统一理论对 14 个化学难题给出统一验证
"""
from typing import Any, Dict, List

import numpy as np

from bsd_agents.base import BSDAgentBase, AgentMessage
from bsd_engine.registry.constants import GAMMA, KAPPA, ALPHA
from bsd_verify.chemistry import get_all_chemistry_verifiers


TOTAL_PROBLEMS = 14
BASIC_PROBLEMS = [
    "protein_folding",
    "high_tc_superconduct",
    "quantum_many_body",
    "origin_of_life",
    "self_assembly",
    "nonequilibrium_chem",
    "catalysis_mechanism",
]
ENGINEERING_PROBLEMS = [
    "artificial_photo",
    "room_temp_super",
    "inverse_catalyst",
    "carbon_capture",
    "high_energy_battery",
    "green_chemistry",
    "precision_synthesis",
]


class ChemistryVerificationAgent(BSDAgentBase):
    """
    化学全域难题验证 Agent

    职责：
    - verify：验证指定化学难题
    - verify_all：验证全部 14 个化学难题
    - verify_category：验证指定类别（basic/engineering）
    - get_summary：获取验证摘要
    """

    def __init__(self):
        super().__init__(
            name="ChemistryVerificationAgent",
            description="化学全域难题验证Agent：14个化学难题基于BSD统一理论的统一验证",
        )
        self._verifiers = get_all_chemistry_verifiers()
        self._last_results: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # 单难题验证入口
    # ------------------------------------------------------------------
    def verify(self, problem_name: str) -> Dict[str, Any]:
        """
        验证指定化学难题。

        参数
        ----
        problem_name : str
            难题名：protein_folding / high_tc_superconduct / quantum_many_body /
            origin_of_life / self_assembly / nonequilibrium_chem / catalysis_mechanism /
            artificial_photo / room_temp_super / inverse_catalyst / carbon_capture /
            high_energy_battery / green_chemistry / precision_synthesis

        返回
        ----
        dict
            {problem, verdict, proof_chain, key_equation, confidence, ...}
        """
        key = problem_name.strip().lower()
        if key not in self._verifiers:
            return {
                "problem": problem_name,
                "verdict": "unknown",
                "proof_chain": [],
                "key_equation": "",
                "confidence": 0.0,
                "error": f"未知化学难题: {problem_name}",
                "valid_problems": list(self._verifiers.keys()),
            }
        try:
            verifier = self._verifiers[key]
            result = verifier.verify()
            self._last_results[key] = result
            return {
                "problem": key,
                "verdict": result.verdict,
                "confidence": result.confidence,
                "proof_chain": result.proof_chain,
                "key_equation": result.key_equation,
                "numerical_evidence": result.numerical_evidence,
                "verification_time": result.verification_time,
                "bsd_path": verifier.bsd_derivation_path,
                "category": verifier.category,
                "nobel_prize_related": verifier.nobel_prize_related,
                "industry_value": verifier.industry_value,
            }
        except Exception as exc:
            return {
                "problem": key,
                "verdict": "error",
                "proof_chain": [],
                "key_equation": "",
                "confidence": 0.0,
                "error": str(exc),
            }

    # ------------------------------------------------------------------
    # 全部难题验证
    # ------------------------------------------------------------------
    def verify_all(self) -> Dict[str, Any]:
        """
        验证全部 14 个化学难题。

        返回
        ----
        dict
            {total, passed, results: {problem: result}, overall_confidence, ...}
        """
        results: Dict[str, Any] = {}
        passed = 0
        confidences: List[float] = []
        for key in self._verifiers.keys():
            r = self.verify(key)
            results[key] = r
            if r.get("verdict") == "verified":
                passed += 1
            confidences.append(float(r.get("confidence", 0.0)))
        overall_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return {
            "total": TOTAL_PROBLEMS,
            "passed": passed,
            "results": results,
            "overall_confidence": overall_conf,
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
            "basic_count": len(BASIC_PROBLEMS),
            "engineering_count": len(ENGINEERING_PROBLEMS),
        }

    # ------------------------------------------------------------------
    # 按类别验证
    # ------------------------------------------------------------------
    def verify_category(self, category: str) -> Dict[str, Any]:
        """
        验证指定类别的化学难题。

        参数
        ----
        category : str
            类别："basic"（基础理论类）或 "engineering"（工程悬赏类）

        返回
        ----
        dict
            {category, total, passed, results, overall_confidence}
        """
        cat = category.strip().lower()
        if cat == "basic":
            problem_list = BASIC_PROBLEMS
        elif cat == "engineering":
            problem_list = ENGINEERING_PROBLEMS
        else:
            return {
                "category": category,
                "total": 0,
                "passed": 0,
                "results": {},
                "overall_confidence": 0.0,
                "error": f"未知类别: {category}, 有效类别: basic, engineering",
            }

        results: Dict[str, Any] = {}
        passed = 0
        confidences: List[float] = []
        for key in problem_list:
            r = self.verify(key)
            results[key] = r
            if r.get("verdict") == "verified":
                passed += 1
            confidences.append(float(r.get("confidence", 0.0)))
        overall_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return {
            "category": cat,
            "total": len(problem_list),
            "passed": passed,
            "results": results,
            "overall_confidence": overall_conf,
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
        }

    # ------------------------------------------------------------------
    # 获取摘要
    # ------------------------------------------------------------------
    def get_summary(self) -> Dict[str, Any]:
        """
        获取化学难题验证摘要。

        返回
        ----
        dict
            包含总数、通过数、各类别统计、整体置信度等
        """
        if not self._last_results:
            return {
                "total": TOTAL_PROBLEMS,
                "passed": 0,
                "overall_confidence": 0.0,
                "basic": {"total": len(BASIC_PROBLEMS), "passed": 0, "confidence": 0.0},
                "engineering": {"total": len(ENGINEERING_PROBLEMS), "passed": 0, "confidence": 0.0},
                "status": "not_run",
            }

        basic_confidences = []
        basic_passed = 0
        for key in BASIC_PROBLEMS:
            if key in self._last_results:
                r = self._last_results[key]
                basic_confidences.append(r.confidence)
                if r.verdict == "verified":
                    basic_passed += 1

        eng_confidences = []
        eng_passed = 0
        for key in ENGINEERING_PROBLEMS:
            if key in self._last_results:
                r = self._last_results[key]
                eng_confidences.append(r.confidence)
                if r.verdict == "verified":
                    eng_passed += 1

        all_confs = basic_confidences + eng_confidences
        all_passed = basic_passed + eng_passed

        return {
            "total": TOTAL_PROBLEMS,
            "passed": all_passed,
            "overall_confidence": sum(all_confs) / len(all_confs) if all_confs else 0.0,
            "basic": {
                "total": len(BASIC_PROBLEMS),
                "passed": basic_passed,
                "confidence": sum(basic_confidences) / len(basic_confidences) if basic_confidences else 0.0,
            },
            "engineering": {
                "total": len(ENGINEERING_PROBLEMS),
                "passed": eng_passed,
                "confidence": sum(eng_confidences) / len(eng_confidences) if eng_confidences else 0.0,
            },
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # 消息处理
    # ------------------------------------------------------------------
    def process(self) -> List[Dict[str, Any]]:
        """
        处理消息队列中的化学难题验证请求。

        支持的 content.action：
        - "verify"           content.problem_name
        - "verify_all"
        - "verify_category"  content.category
        - "get_summary"
        """
        results: List[Dict[str, Any]] = []
        while self.message_queue:
            msg: AgentMessage = self.message_queue.pop(0)
            content = msg.content if isinstance(msg.content, dict) else {}
            action = content.get("action", "")
            try:
                if action == "verify":
                    res = self.verify(content.get("problem_name", ""))
                elif action == "verify_all":
                    res = self.verify_all()
                elif action == "verify_category":
                    res = self.verify_category(content.get("category", ""))
                elif action == "get_summary":
                    res = self.get_summary()
                else:
                    res = {"error": f"未知 action: {action}"}
            except Exception as exc:
                res = {"error": str(exc), "action": action}
            results.append({
                "message_id": msg.message_id,
                "action": action,
                "result": res,
            })
        return results
