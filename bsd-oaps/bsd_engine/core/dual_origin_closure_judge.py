"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·全域双界域隔离壁垒本源】
【对应公理：双界域隔离终极公理·双本源协同闭环】

DualOriginClosureJudge —— 双本源协同闭环判定器
本源自激相变 + 双界域隔离 = 终局三角闭环之二
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class DualOriginClosureJudge(BaseTheoryModule):
    """双本源协同闭环判定器"""

    module_id = "T30_C05"
    module_name = "双本源协同闭环判定器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·全域双界域隔离壁垒本源"
    corresponding_axiom = "双界域隔离终极公理·双本源协同闭环"
    is_origin_locked = True
    dependencies = ["T29", "T30", "T30_C01", "T30_C02", "T30_C03", "T30_C04"]

    def __init__(self):
        super().__init__()
        self._closure_history = []

    def judge_dual_closure(self,
                           phase_transition_ok: bool,
                           boundary_ok: bool,
                           symmetry_ok: bool,
                           contamination_low: bool) -> Dict[str, any]:
        """判定双本源协同闭环"""
        checks = {
            "本源自激相变闭环": phase_transition_ok,
            "双界域隔离完整": boundary_ok,
            "四稳态四异化对偶对称": symmetry_ok,
            "跨界污染可控": contamination_low
        }
        all_pass = all(checks.values())
        score = sum(1 for v in checks.values() if v) / len(checks)
        judgment = {
            "checks": checks,
            "all_passed": all_pass,
            "closure_score": score,
            "closure_level": self._level(score),
            "verdict": "双本源协同闭环成立" if all_pass else "双本源协同闭环不成立"
        }
        self._closure_history.append(judgment)
        return judgment

    def _level(self, score: float) -> str:
        if score >= 1.0:
            return "完美协同（E3级）"
        elif score >= 0.85:
            return "高阶协同（E2级）"
        elif score >= 0.6:
            return "基础协同（E1级）"
        else:
            return "协同不足"

    def judge_triangle_closure(self,
                               origin_ok: bool,
                               boundary_ok: bool,
                               ni_theory_ok: bool) -> Dict[str, any]:
        """终局三角闭环判定（相变+壁垒+逆五论）"""
        checks = {
            "本源自激相变（启动）": origin_ok,
            "双界域隔离壁垒（约束）": boundary_ok,
            "逆腾飞五论（转化）": ni_theory_ok
        }
        all_pass = all(checks.values())
        return {
            "triangle_checks": checks,
            "triangle_closed": all_pass,
            "verdict": "终局三角闭环成立" if all_pass else "终局三角闭环不成立"
        }

    def get_history(self) -> List[Dict]:
        return list(self._closure_history)

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
