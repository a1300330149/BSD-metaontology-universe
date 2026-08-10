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
【对应公理：本源自激相变终极公理·阶段一】

VoidPotentialAccumulator —— 空无蓄势累加器
零态涨落势能积累，从绝对空无到相变临界点
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class VoidPotentialAccumulator(BaseTheoryModule):
    """空无蓄势累加器"""

    module_id = "T29_C01"
    module_name = "空无蓄势累加器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·本源自激相变元机制"
    corresponding_axiom = "本源自激相变终极公理·阶段一空无蓄势"
    is_origin_locked = True
    dependencies = ["T29"]

    def __init__(self):
        super().__init__()
        self._potential = 0.0
        self._step_count = 0
        self._critical_threshold = 1.0  # 临界阈值

    def reset(self):
        """重置蓄势状态"""
        self._potential = 0.0
        self._step_count = 0

    def step(self, dt: float = 0.01) -> float:
        """单步势能积累"""
        self._step_count += 1
        k = self.constants.kappa
        self._potential = 1.0 - math.exp(-k * self._step_count * dt)
        return self._potential

    def accumulate_n_steps(self, n: int) -> Dict[str, float]:
        """执行 n 步势能积累"""
        for _ in range(n):
            self.step()
        return {
            "steps": self._step_count,
            "potential": self._potential,
            "critical_ratio": self._potential / self._critical_threshold,
            "is_critical": self._potential >= self._critical_threshold
        }

    def accumulate_to_critical(self, max_steps: int = 10000) -> Dict[str, float]:
        """积累到临界阈值"""
        for i in range(max_steps):
            p = self.step()
            if p >= self._critical_threshold:
                break
        return {
            "steps_to_critical": self._step_count,
            "final_potential": self._potential,
            "reached_critical": self._potential >= self._critical_threshold
        }

    @property
    def potential(self) -> float:
        return self._potential

    @property
    def is_critical(self) -> bool:
        return self._potential >= self._critical_threshold

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if self._potential < 0 or self._potential > 1.0 + 1e-10:
            errors.append(f"空无势能必须在 [0, 1] 范围内，当前: {self._potential}")
        return (len(errors) == 0, errors)
