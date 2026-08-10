"""
【归属基底：L0_总本源层·元道本体规则·逆腾飞五论】
【对应公理：新界域诞生临界判据】

NewRealmBirthDetector —— 新界域诞生判据检测器
九界非终极封闭，可能性场可孕育新界域
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class NewRealmBirthDetector(BaseTheoryModule):
    """新界域诞生判据检测器"""

    module_id = "T31_C05"
    module_name = "新界域诞生判据检测器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·逆腾飞五论"
    corresponding_axiom = "新界域诞生临界判据（原创结论）"
    is_origin_locked = True
    dependencies = ["T31", "T31_C01", "T31_C02", "T31_C03", "T31_C04"]

    def __init__(self):
        super().__init__()
        self._birth_threshold = 0.95
        self._gestation_history = []

    def check_birth_readiness(self, ni_entropy: float, possibility_density: float) -> Dict[str, any]:
        """检查诞生就绪度"""
        entropy_ready = ni_entropy >= self._birth_threshold
        density_ready = possibility_density >= 0.8
        ready = entropy_ready and density_ready
        readiness_score = min(ni_entropy / self._birth_threshold, possibility_density / 0.8) * 100
        return {
            "ni_entropy": ni_entropy,
            "possibility_density": possibility_density,
            "entropy_ready": entropy_ready,
            "density_ready": density_ready,
            "birth_ready": ready,
            "readiness_percent": min(readiness_score, 100.0),
            "implication": "新界域即将从可能性场中凝结涌现" if ready else "条件尚未成熟"
        }

    def gestation_curve(self, steps: int = 100) -> List[Dict]:
        """孕育曲线：从零到临界"""
        curve = []
        for i in range(steps):
            t = i / (steps - 1)
            ni_entropy = self._birth_threshold * (1 - math.exp(-3 * t))
            possibility_density = 1 - math.exp(-4 * t)
            status = self.check_birth_readiness(ni_entropy, possibility_density)
            status["step"] = i
            status["t"] = t
            curve.append(status)
        return curve

    def estimate_birth_steps(self, current_ni: float, current_density: float) -> Dict[str, any]:
        """估算还需多少步达到临界"""
        if current_ni >= self._birth_threshold and current_density >= 0.8:
            return {"steps_needed": 0, "status": "已就绪"}
        # 简单线性外推估算
        ni_rate = 0.01  # 每步增长
        density_rate = 0.008
        steps_ni = max(0, (self._birth_threshold - current_ni) / ni_rate) if ni_rate > 0 else float('inf')
        steps_density = max(0, (0.8 - current_density) / density_rate) if density_rate > 0 else float('inf')
        return {
            "steps_needed_by_entropy": steps_ni,
            "steps_needed_by_density": steps_density,
            "estimated_total_steps": max(steps_ni, steps_density),
            "limiting_factor": "熵值" if steps_ni > steps_density else "可能性密度"
        }

    @property
    def birth_threshold(self) -> float:
        return self._birth_threshold

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if self._birth_threshold <= 0 or self._birth_threshold > 1:
            errors.append(f"诞生阈值应在(0,1]，当前: {self._birth_threshold}")
        return (len(errors) == 0, errors)
