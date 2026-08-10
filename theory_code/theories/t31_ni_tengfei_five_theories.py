"""
【归属基底：L0_总本源层·元道本体规则·逆腾飞五论】
【对应公理：逆腾飞五论独立归一公理】

T31 —— 逆腾飞五论 · 独立数理对偶体系
实存熵减 ↔ 可能熵增，全域总熵守恒
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


NI_FIVE_THEORIES = ["逆真论", "逆正论", "逆悬论", "逆谬论", "逆逆论"]
FORWARD_FIVE = ["真论", "正论", "悬论", "谬论", "逆论"]


class NiTengfeiFiveTheories(BaseTheoryModule):
    """逆腾飞五论·独立数理对偶体系"""

    module_id = "T31"
    module_name = "逆腾飞五论·独立数理对偶体系"
    version = "V1.0_终版"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·逆腾飞五论"
    corresponding_axiom = "逆腾飞五论独立归一公理+全域总熵守恒定律"
    is_origin_locked = True
    dependencies = ["T29", "T30"]

    def __init__(self):
        super().__init__()
        self._ni_weights = {t: 0.2 for t in NI_FIVE_THEORIES}
        self._forward_weights = {t: 0.2 for t in FORWARD_FIVE}

    def set_ni_weights(self, weights: Dict[str, float]):
        """设置逆五论权重"""
        for k, v in weights.items():
            if k in self._ni_weights:
                self._ni_weights[k] = v

    def set_forward_weights(self, weights: Dict[str, float]):
        """设置正五论权重"""
        for k, v in weights.items():
            if k in self._forward_weights:
                self._forward_weights[k] = v

    def dual_mapping(self) -> Dict[str, str]:
        """正反五论对偶映射"""
        mapping = {}
        for i, f in enumerate(FORWARD_FIVE):
            mapping[f] = NI_FIVE_THEORIES[i]
        return mapping

    def self_inverse_verify(self) -> bool:
        """自逆映射验证：逆之逆=正"""
        mapping = self.dual_mapping()
        reverse = {v: k for k, v in mapping.items()}
        for f in FORWARD_FIVE:
            ni = mapping[f]
            if reverse.get(ni) != f:
                return False
        return True

    def global_entropy_conservation(self, s_forward: float, s_ni: float) -> Dict[str, any]:
        """全域总熵守恒定律验证"""
        total = s_forward + s_ni
        conserved = abs(total) < self.constants.theta_neg
        return {
            "forward_entropy": s_forward,
            "ni_entropy": s_ni,
            "total_entropy": total,
            "conserved": conserved,
            "law": "S_实存 + S_可能 = 常数（全域总熵守恒）"
        }

    def new_realm_birth_criterion(self,
                                  ni_entropy: float,
                                  threshold: float = 0.95) -> Dict[str, any]:
        """新界域诞生临界判据"""
        can_birth = ni_entropy >= threshold
        return {
            "ni_entropy": ni_entropy,
            "threshold": threshold,
            "can_birth_new_realm": can_birth,
            "implication": "九界非终极封闭，可能性场可孕育新界域" if can_birth else "当前熵值不足以诞生新界域"
        }

    def ni_entropy_calculate(self, weights: Dict[str, float]) -> float:
        """逆体系熵变计算"""
        ordered = ["逆真论", "逆正论", "逆悬论", "逆谬论", "逆逆论"]
        coeffs = [-1.0, -0.5, 0.0, 0.5, 1.0]
        s = sum(weights.get(t, 0) * c for t, c in zip(ordered, coeffs))
        return s * 0.7  # 逆体系独立正交系数

    @property
    def ni_weights(self) -> Dict[str, float]:
        return dict(self._ni_weights)

    @property
    def forward_weights(self) -> Dict[str, float]:
        return dict(self._forward_weights)

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(NI_FIVE_THEORIES) != 5:
            errors.append("逆五论必须恰好5论")
        if sum(self._ni_weights.values()) < 0.99 or sum(self._ni_weights.values()) > 1.01:
            errors.append(f"逆五论权重和必须为1，当前: {sum(self._ni_weights.values())}")
        return (len(errors) == 0, errors)
