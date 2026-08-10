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
【对应公理：逆腾飞五论独立归一公理·权重归一】

DualWeightNormalizer —— 双体系权重归一器
正向五论 + 逆向五论 = 全域十论权重归一
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class DualWeightNormalizer(BaseTheoryModule):
    """双体系权重归一器"""

    module_id = "T31_C01"
    module_name = "双体系权重归一器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·逆腾飞五论"
    corresponding_axiom = "逆腾飞五论独立归一公理·权重归一"
    is_origin_locked = True
    dependencies = ["T31"]

    def __init__(self):
        super().__init__()
        self._forward_weights = {}
        self._ni_weights = {}

    def set_weights(self, forward: Dict[str, float], ni: Dict[str, float]):
        """设置双体系权重"""
        self._forward_weights = dict(forward)
        self._ni_weights = dict(ni)

    def normalize_forward(self) -> Dict[str, float]:
        """归一化正向权重"""
        total = sum(self._forward_weights.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in self._forward_weights.items()}

    def normalize_ni(self) -> Dict[str, float]:
        """归一化逆向权重"""
        total = sum(self._ni_weights.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in self._ni_weights.items()}

    def normalize_global(self) -> Dict[str, float]:
        """全域十论归一化"""
        combined = {}
        for k, v in self._forward_weights.items():
            combined[f"正·{k}"] = v
        for k, v in self._ni_weights.items():
            combined[f"逆·{k}"] = v
        total = sum(combined.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in combined.items()}

    def verify_normalization(self, weights: Dict[str, float]) -> Dict[str, any]:
        """验证归一化"""
        total = sum(weights.values())
        normalized = abs(total - 1.0) < self.constants.theta_neg
        return {
            "total_weight": total,
            "normalized": normalized,
            "tolerance": self.constants.theta_neg
        }

    def dual_balance(self) -> Dict[str, any]:
        """正反体系平衡检查"""
        f_total = sum(self._forward_weights.values())
        n_total = sum(self._ni_weights.values())
        g_total = f_total + n_total
        ratio = n_total / f_total if f_total > 0 else float('inf')
        return {
            "forward_total": f_total,
            "ni_total": n_total,
            "global_total": g_total,
            "ni_forward_ratio": ratio,
            "balanced": abs(ratio - 1.0) < 0.1
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
