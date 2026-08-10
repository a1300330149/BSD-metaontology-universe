"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·元道本体规则·对偶性体系】
【对应公理：T3 相变对偶定理】

BidirectionalPhaseTransition —— 双向相变闭环控制器
正向：空无→所有  逆向：所有→空无
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class BidirectionalPhaseTransition(BaseTheoryModule):
    """双向相变闭环控制器"""

    module_id = "T32_C02"
    module_name = "双向相变闭环控制器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·对偶性体系"
    corresponding_axiom = "T3 相变对偶定理（双向闭环）"
    is_origin_locked = True
    dependencies = ["T32", "T29"]

    def __init__(self):
        super().__init__()
        self._direction = "forward"  # forward / reverse
        self._cycle_count = 0

    def forward_phase(self, steps: int = 100) -> List[Dict]:
        """正向相变：空无 → 所有"""
        self._direction = "forward"
        history = []
        for i in range(steps):
            t = i / (steps - 1)
            potential = 1 - math.exp(-3 * t)
            history.append({"step": i, "t": t, "potential": potential, "direction": "forward"})
        self._cycle_count += 1
        return history

    def reverse_phase(self, steps: int = 100) -> List[Dict]:
        """逆向相变：所有 → 空无"""
        self._direction = "reverse"
        history = []
        for i in range(steps):
            t = i / (steps - 1)
            potential = math.exp(-3 * t)
            history.append({"step": i, "t": t, "potential": potential, "direction": "reverse"})
        return history

    def full_cycle(self, steps_per_phase: int = 100) -> Dict[str, any]:
        """完整双向循环：正→逆→正"""
        fwd = self.forward_phase(steps_per_phase)
        rev = self.reverse_phase(steps_per_phase)
        total_entropy_fwd = sum(h["potential"] for h in fwd)
        total_entropy_rev = sum(1 - h["potential"] for h in rev)
        return {
            "forward_steps": len(fwd),
            "reverse_steps": len(rev),
            "total_cycles": self._cycle_count,
            "entropy_conservation": abs(total_entropy_fwd - total_entropy_rev) < 1e-6,
            "theorem": "ΔS_正 + ΔS_逆 = 0"
        }

    def oscillation(self, omega: float, t: float) -> Dict[str, float]:
        """振荡模型：正反相变周期性交替"""
        potential = 0.5 * (1 + math.sin(omega * t))
        direction = "forward" if math.cos(omega * t) > 0 else "reverse"
        return {
            "t": t,
            "potential": potential,
            "direction": direction,
            "omega": omega
        }

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
