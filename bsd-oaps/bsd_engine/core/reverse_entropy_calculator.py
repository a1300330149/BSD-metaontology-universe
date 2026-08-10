"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·元道本体规则·逆腾飞五论】
【对应公理：逆腾飞五论独立归一公理·熵变公式】

ReverseEntropyCalculator —— 逆体系熵变计算器
独立正交系数、异秩序建构机制
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class ReverseEntropyCalculator(BaseTheoryModule):
    """逆体系熵变计算器"""

    module_id = "T31_C03"
    module_name = "逆体系熵变计算器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·逆腾飞五论"
    corresponding_axiom = "逆腾飞五论独立归一公理·熵变公式"
    is_origin_locked = True
    dependencies = ["T31", "T31_C01", "T31_C02"]

    def __init__(self):
        super().__init__()
        self._ni_orthogonal_coeff = 0.7  # 逆体系独立正交系数
        self._ni_order_coeff = -0.85     # 异秩序建构系数

    def ni_entropy(self, weights: Dict[str, float]) -> float:
        """计算逆体系熵值"""
        ordered = ["逆真论", "逆正论", "逆悬论", "逆谬论", "逆逆论"]
        coeffs = [-1.0, -0.5, 0.0, 0.5, 1.0]
        s = sum(weights.get(t, 0) * c for t, c in zip(ordered, coeffs))
        return s * self._ni_orthogonal_coeff

    def forward_entropy(self, weights: Dict[str, float]) -> float:
        """计算正向体系熵值"""
        ordered = ["真论", "正论", "悬论", "谬论", "逆论"]
        coeffs = [-1.0, -0.5, 0.0, 0.5, 1.0]
        return sum(weights.get(t, 0) * c for t, c in zip(ordered, coeffs))

    def total_entropy(self, f_weights: Dict[str, float], ni_weights: Dict[str, float]) -> float:
        """计算全域总熵"""
        f_s = self.forward_entropy(f_weights)
        ni_s = self.ni_entropy(ni_weights)
        return f_s + ni_s

    def entropy_conservation_check(self, f_weights: Dict[str, float], ni_weights: Dict[str, float]) -> Dict[str, any]:
        """总熵守恒检查"""
        f_s = self.forward_entropy(f_weights)
        ni_s = self.ni_entropy(ni_weights)
        total = f_s + ni_s
        conserved = abs(total) < self.constants.theta_neg
        return {
            "forward_entropy": f_s,
            "ni_entropy": ni_s,
            "total_entropy": total,
            "conserved": conserved,
            "orthogonal_coeff": self._ni_orthogonal_coeff
        }

    def ni_order_construction(self, ni_entropy: float) -> Dict[str, any]:
        """异秩序建构：逆熵生秩序"""
        # 逆体系：高正熵 → 高异秩序
        order_level = ni_entropy * self._ni_order_coeff
        return {
            "ni_entropy": ni_entropy,
            "ni_order_level": order_level,
            "order_coeff": self._ni_order_coeff,
            "interpretation": "可能性场熵增 ↔ 异秩序建构增强"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if self._ni_orthogonal_coeff <= 0 or self._ni_orthogonal_coeff > 1:
            errors.append(f"逆体系正交系数应在(0,1]，当前: {self._ni_orthogonal_coeff}")
        return (len(errors) == 0, errors)
