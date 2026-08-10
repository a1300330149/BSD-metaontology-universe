"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·本源自激相变元机制】
【对应公理：本源自激相变终极公理·阶段四】

EntropyZeroPointRegression —— 熵归零点回溯器
所有证空无，熵归零点，完成自证闭环
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class EntropyZeroPointRegression(BaseTheoryModule):
    """熵归零点回溯器"""

    module_id = "T29_C04"
    module_name = "熵归零点回溯器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·本源自激相变元机制"
    corresponding_axiom = "本源自激相变终极公理·阶段四熵归零点"
    is_origin_locked = True
    dependencies = ["T29", "T29_C01", "T29_C02", "T29_C03"]

    def __init__(self):
        super().__init__()
        self._initial_entropy = 0.0
        self._current_entropy = 0.0
        self._regression_rate = 0.0

    def set_initial_state(self, order_entropy: float):
        """设置初始秩序熵值"""
        self._initial_entropy = order_entropy
        self._current_entropy = order_entropy

    def regress_step(self, dt: float = 0.01) -> float:
        """单步熵归"""
        alpha = self.constants.alpha
        self._regression_rate = alpha * abs(self._current_entropy)
        if self._current_entropy < 0:
            self._current_entropy += self._regression_rate * dt
        elif self._current_entropy > 0:
            self._current_entropy -= self._regression_rate * dt
        return self._current_entropy

    def regress_to_zero(self, max_steps: int = 10000) -> Dict[str, float]:
        """回归到零点"""
        steps = 0
        for _ in range(max_steps):
            steps += 1
            self.regress_step()
            if abs(self._current_entropy) < self.constants.theta_neg:
                break
        return {
            "steps": steps,
            "final_entropy": self._current_entropy,
            "reached_zero": abs(self._current_entropy) < self.constants.theta_neg,
            "zero_threshold": self.constants.theta_neg
        }

    def full_cycle_test(self, initial_order: float = -0.92) -> Dict[str, any]:
        """完整周期测试：秩序→熵归→零点"""
        self.set_initial_state(initial_order)
        result = self.regress_to_zero()
        result["initial_entropy"] = initial_order
        result["closure_verified"] = result["reached_zero"]
        return result

    @property
    def current_entropy(self) -> float:
        return self._current_entropy

    @property
    def at_zero_point(self) -> bool:
        return abs(self._current_entropy) < self.constants.theta_neg

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if self._regression_rate < 0:
            errors.append("回归速率不应为负")
        return (len(errors) == 0, errors)
