"""
归属基底：第3重六阶科研业务基底
对应公理：公理七（系统自进化迭代公理） / 制度净驻波公理
对应九维维度：应用维度·制度维·经济维
理论原文出处：T88制度经济学理论篇
固定数理常量：γ=0.92, κ=0.35, α=0.18

制度经济学验证 Agent（5个验证器统一验证）
—— 调用 bsd_verify.economics 验证器
   基于 BSD 全域统一理论对制度经济学理论体系给出统一验证
"""
from typing import Any, Dict, List

import numpy as np

from bsd_agents.base import BSDAgentBase, AgentMessage
from bsd_engine.registry.constants import GAMMA, KAPPA, ALPHA
from bsd_verify.economics import get_all_economics_verifiers


TOTAL_VERIFIERS = 5
INSTITUTIONAL_VERIFIERS = [
    "institutional_paradigm",
    "standing_wave",
    "industrial_policy",
    "tariff_policy",
    "quality_assessment",
]


class InstitutionalEconomicsAgent(BSDAgentBase):
    """
    制度经济学验证 Agent

    职责：
    - verify_all：验证全部制度经济学理论
    - verify_paradigm：验证三元制度范式
    - analyze_wave：分析制度驻波动力学
    - get_summary：获取验证摘要
    """

    def __init__(self):
        super().__init__(
            name="InstitutionalEconomicsAgent",
            description="制度经济学验证Agent：基于BSD统一理论的制度经济学理论体系验证",
        )
        self._verifiers = get_all_economics_verifiers()
        self._last_results: Dict[str, Any] = {}

    def verify_all(self) -> Dict[str, Any]:
        """
        验证全部制度经济学理论。

        返回
        ----
        dict
            {total, passed, results: {verifier: result}, overall_confidence, ...}
        """
        results: Dict[str, Any] = {}
        passed = 0
        confidences: List[float] = []
        for key in self._verifiers.keys():
            r = self._verify_single(key)
            results[key] = r
            if r.get("verdict") == "verified":
                passed += 1
            confidences.append(float(r.get("confidence", 0.0)))
        overall_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return {
            "total": TOTAL_VERIFIERS,
            "passed": passed,
            "results": results,
            "overall_confidence": overall_conf,
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
            "verifier_list": INSTITUTIONAL_VERIFIERS,
        }

    def verify_paradigm(self) -> Dict[str, Any]:
        """
        验证三元制度范式。

        返回
        ----
        dict
            {verifier, verdict, confidence, proof_chain, numerical_evidence, ...}
        """
        return self._verify_single("institutional_paradigm")

    def analyze_wave(self) -> Dict[str, Any]:
        """
        分析制度驻波动力学。

        返回
        ----
        dict
            {verifier, verdict, confidence, numerical_evidence, stability_level, ...}
        """
        standing_wave = self._verify_single("standing_wave")
        industrial_policy = self._verify_single("industrial_policy")
        tariff_policy = self._verify_single("tariff_policy")
        
        return {
            "standing_wave": standing_wave,
            "industrial_policy": industrial_policy,
            "tariff_policy": tariff_policy,
            "wave_summary": {
                "standing_wave_psi_net": standing_wave.get("numerical_evidence", {}).get("final_psi_net", 0),
                "industrial_policy_phase3_psi": industrial_policy.get("numerical_evidence", {}).get("phase3_psi_net", 0),
                "tariff_policy_phase2_psi": tariff_policy.get("numerical_evidence", {}).get("phase2_psi_net", 0),
                "overall_wave_direction": "正向" if standing_wave.get("numerical_evidence", {}).get("final_psi_net", 0) > 0 else "负向",
            },
            "overall_confidence": (
                standing_wave.get("confidence", 0) + 
                industrial_policy.get("confidence", 0) + 
                tariff_policy.get("confidence", 0)
            ) / 3,
        }

    def get_summary(self) -> Dict[str, Any]:
        """
        获取制度经济学验证摘要。

        返回
        ----
        dict
            包含总数、通过数、整体置信度等
        """
        if not self._last_results:
            return {
                "total": TOTAL_VERIFIERS,
                "passed": 0,
                "overall_confidence": 0.0,
                "status": "not_run",
                "verifier_list": INSTITUTIONAL_VERIFIERS,
            }

        all_confs = []
        all_passed = 0
        for key in INSTITUTIONAL_VERIFIERS:
            if key in self._last_results:
                r = self._last_results[key]
                all_confs.append(r.confidence)
                if r.verdict == "verified":
                    all_passed += 1

        return {
            "total": TOTAL_VERIFIERS,
            "passed": all_passed,
            "overall_confidence": sum(all_confs) / len(all_confs) if all_confs else 0.0,
            "verifier_list": INSTITUTIONAL_VERIFIERS,
            "status": "completed",
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
        }

    def _verify_single(self, verifier_name: str) -> Dict[str, Any]:
        """验证单个验证器"""
        key = verifier_name.strip().lower()
        if key not in self._verifiers:
            return {
                "verifier": verifier_name,
                "verdict": "unknown",
                "proof_chain": [],
                "key_equation": "",
                "confidence": 0.0,
                "error": f"未知验证器: {verifier_name}",
                "valid_verifiers": list(self._verifiers.keys()),
            }
        try:
            verifier = self._verifiers[key]
            result = verifier.verify()
            self._last_results[key] = result
            return {
                "verifier": key,
                "verdict": result.verdict,
                "confidence": result.confidence,
                "proof_chain": result.proof_chain,
                "key_equation": result.key_equation,
                "numerical_evidence": result.numerical_evidence,
                "verification_time": result.verification_time,
                "bsd_path": verifier.bsd_derivation_path,
                "category": getattr(verifier, "category", "institutional"),
            }
        except Exception as exc:
            return {
                "verifier": key,
                "verdict": "error",
                "proof_chain": [],
                "key_equation": "",
                "confidence": 0.0,
                "error": str(exc),
            }

    def process(self) -> List[Dict[str, Any]]:
        """
        处理消息队列中的制度经济学验证请求。

        支持的 content.action：
        - "verify_all"
        - "verify_paradigm"
        - "analyze_wave"
        - "get_summary"
        """
        results: List[Dict[str, Any]] = []
        while self.message_queue:
            msg: AgentMessage = self.message_queue.pop(0)
            content = msg.content if isinstance(msg.content, dict) else {}
            action = content.get("action", "")
            try:
                if action == "verify_all":
                    res = self.verify_all()
                elif action == "verify_paradigm":
                    res = self.verify_paradigm()
                elif action == "analyze_wave":
                    res = self.analyze_wave()
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