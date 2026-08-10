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
【对应公理：全域总熵守恒定律】

GlobalEntropyConservationJudge —— 全域总熵守恒判定器
S_实存 + S_可能 = 常数
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class GlobalEntropyConservationJudge(BaseTheoryModule):
    """全域总熵守恒判定器"""

    module_id = "T31_C04"
    module_name = "全域总熵守恒判定器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·逆腾飞五论"
    corresponding_axiom = "全域总熵守恒定律（核心原创）"
    is_origin_locked = True
    dependencies = ["T31", "T31_C01", "T31_C02", "T31_C03"]

    def __init__(self):
        super().__init__()
        self._global_constant = 0.0  # 全域总熵常数
        self._history = []

    def set_global_constant(self, value: float):
        """设置全域总熵常数"""
        self._global_constant = value

    def verify_conservation(self, s_forward: float, s_ni: float) -> Dict[str, any]:
        """验证总熵守恒"""
        total = s_forward + s_ni
        diff = abs(total - self._global_constant)
        conserved = diff < self.constants.theta_neg
        result = {
            "forward_entropy": s_forward,
            "ni_entropy": s_ni,
            "total_entropy": total,
            "global_constant": self._global_constant,
            "deviation": diff,
            "conserved": conserved,
            "law_expression": "S_实存 + S_可能 = 常数"
        }
        self._history.append(result)
        return result

    def forward_decrease_ni_increase(self, s_f: float, s_ni: float, delta: float) -> Dict[str, any]:
        """实存熵减 → 可能熵增 守恒过程"""
        new_f = s_f - delta
        new_ni = s_ni + delta
        return self.verify_conservation(new_f, new_ni)

    def evolution_cycle(self, initial_f: float, initial_ni: float, steps: int = 10) -> List[Dict]:
        """演化周期：实存与可能交替涨落"""
        history = []
        f, ni = initial_f, initial_ni
        for i in range(steps):
            delta = 0.05 * math.sin(i * 0.5)
            f -= delta
            ni += delta
            result = self.verify_conservation(f, ni)
            result["step"] = i
            history.append(result)
        return history

    def get_conservation_rate(self) -> float:
        """获取历史守恒率"""
        if not self._history:
            return 0.0
        conserved = sum(1 for h in self._history if h["conserved"])
        return conserved / len(self._history)

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
