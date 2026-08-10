"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·元道本体规则·平行本源体系】
【对应公理：一构多源·多本源耦合公理】

MultiOriginCoupler —— 多本源耦合控制器
多套平行本源同步演化、互不干涉
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class MultiOriginCoupler(BaseTheoryModule):
    """多本源耦合控制器"""

    module_id = "T33_C02"
    module_name = "多本源耦合控制器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·平行本源体系"
    corresponding_axiom = "一构多源·多本源耦合公理"
    is_origin_locked = True
    dependencies = ["T33", "T33_C01"]

    def __init__(self):
        super().__init__()
        self._origins = {}
        self._coupling_matrix = {}

    def add_origin(self, name: str, properties: Dict[str, any]):
        """添加本源"""
        self._origins[name] = properties
        self._coupling_matrix[name] = {}
        for other in self._origins:
            self._coupling_matrix[name][other] = 0.0
            self._coupling_matrix[other][name] = 0.0

    def set_coupling(self, origin_a: str, origin_b: str, strength: float):
        """设置本源间耦合强度"""
        if origin_a in self._coupling_matrix and origin_b in self._coupling_matrix:
            self._coupling_matrix[origin_a][origin_b] = strength
            self._coupling_matrix[origin_b][origin_a] = strength

    def verify_isolation(self, origin_a: str, origin_b: str) -> Dict[str, any]:
        """验证两本源互不干涉"""
        coupling = self._coupling_matrix.get(origin_a, {}).get(origin_b, 0.0)
        isolated = coupling < self.constants.theta_neg
        return {
            "origin_a": origin_a,
            "origin_b": origin_b,
            "coupling_strength": coupling,
            "mutually_isolated": isolated,
            "threshold": self.constants.theta_neg
        }

    def synchronous_evolution(self, dt: float = 0.01) -> Dict[str, any]:
        """多本源同步演化"""
        results = {}
        for name in self._origins:
            # 简化演化模型
            base_entropy = self._origins[name].get("entropy", 0.0)
            coupling_term = sum(
                self._coupling_matrix[name][other] * self._origins[other].get("entropy", 0.0)
                for other in self._origins if other != name
            )
            new_entropy = base_entropy + self.constants.alpha * coupling_term * dt
            results[name] = {
                "old_entropy": base_entropy,
                "new_entropy": new_entropy,
                "coupling_effect": coupling_term
            }
        return results

    def total_origins(self) -> int:
        return len(self._origins)

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        # 允许初始空状态，运行时再检查
        return (len(errors) == 0, errors)
