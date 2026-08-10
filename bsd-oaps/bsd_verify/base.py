"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理10·闭递归公理 / 公理8·意义守恒公理
对应九维维度：元理维·逻辑维·验证维·时间流·命运维
理论出处：theory_base/L0_总本源层/全域大一统理论/BSD千禧年难题验证框架
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD千禧年难题验证器基类
—— 七大千禧年难题+Beal猜想统一验证框架的核心抽象基类
"""

import time
import traceback
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


@dataclass
class VerificationResult:
    problem_name: str
    verdict: str
    confidence: float
    proof_chain: List[Dict[str, Any]] = field(default_factory=list)
    key_equation: str = ""
    numerical_evidence: Dict[str, Any] = field(default_factory=dict)
    verification_time: float = 0.0
    error_message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "problem_name": self.problem_name,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "proof_chain": self.proof_chain,
            "key_equation": self.key_equation,
            "numerical_evidence": self.numerical_evidence,
            "verification_time": self.verification_time,
            "error_message": self.error_message,
        }


class MillenniumVerifierBase(ABC):
    problem_name: str = "Base Millennium Problem"
    bsd_derivation_path: str = "L0_总本源层"

    def __init__(self):
        self._proof_chain: List[Dict[str, Any]] = []
        self._numerical_evidence: Dict[str, Any] = {}
        self._key_equation: str = ""
        self._last_result: Optional[VerificationResult] = None

    def verify(self, **kwargs) -> VerificationResult:
        start_time = time.time()
        try:
            result = self._do_verify(**kwargs)
            elapsed = time.time() - start_time
            result.verification_time = elapsed
            self._last_result = result
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            result = VerificationResult(
                problem_name=self.problem_name,
                verdict="error",
                confidence=0.0,
                proof_chain=self._proof_chain.copy(),
                key_equation=self._key_equation,
                numerical_evidence=self._numerical_evidence.copy(),
                verification_time=elapsed,
                error_message=f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}",
            )
            self._last_result = result
            return result

    @abstractmethod
    def _do_verify(self, **kwargs) -> VerificationResult:
        pass

    def get_proof_chain(self) -> List[Dict[str, Any]]:
        return self._proof_chain.copy()

    def get_summary(self) -> Dict[str, Any]:
        if self._last_result is not None:
            r = self._last_result
            return {
                "problem_name": r.problem_name,
                "verdict": r.verdict,
                "confidence": r.confidence,
                "time_s": r.verification_time,
                "bsd_path": self.bsd_derivation_path,
                "proof_chain_length": len(r.proof_chain),
                "key_equation": r.key_equation,
                "error": r.error_message if r.verdict == "error" else "",
            }
        return {
            "problem_name": self.problem_name,
            "verdict": "not_run",
            "confidence": 0.0,
            "time_s": 0.0,
            "bsd_path": self.bsd_derivation_path,
            "proof_chain_length": len(self._proof_chain),
            "key_equation": self._key_equation,
            "error": "",
        }

    def _add_proof_step(self, step: int, title: str, description: str, equation: str = "", evidence: Dict[str, Any] = None):
        self._proof_chain.append({
            "step": step,
            "title": title,
            "description": description,
            "equation": equation,
            "evidence": evidence or {},
        })

    def _set_key_equation(self, equation: str):
        self._key_equation = equation

    def _add_numerical_evidence(self, key: str, value: Any):
        self._numerical_evidence[key] = value
