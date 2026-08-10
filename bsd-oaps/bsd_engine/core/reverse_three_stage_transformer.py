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
【对应公理：T5 三阶变身对偶定理】

ReverseThreeStageTransformer —— 逆三阶变身能级计算器
E_i* = 1 - E_i，镜像对称，能量守恒
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class ReverseThreeStageTransformer(BaseTheoryModule):
    """逆三阶变身能级计算器"""

    module_id = "T32_C03"
    module_name = "逆三阶变身能级计算器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·对偶性体系"
    corresponding_axiom = "T5 三阶变身对偶定理（E_i*=1-E_i）"
    is_origin_locked = True
    dependencies = ["T32", "T31"]

    def __init__(self):
        super().__init__()
        self._forward_thresholds = [
            self.constants.E1,
            self.constants.E2,
            self.constants.E3
        ]
        self._reverse_thresholds = [
            1 - self.constants.E1,
            1 - self.constants.E2,
            1 - self.constants.E3
        ]

    @property
    def forward_thresholds(self) -> List[float]:
        return list(self._forward_thresholds)

    @property
    def reverse_thresholds(self) -> List[float]:
        return list(self._reverse_thresholds)

    def get_stage(self, energy_level: float, reverse: bool = False) -> Dict[str, any]:
        """获取当前阶段"""
        thresholds = self._reverse_thresholds if reverse else self._forward_thresholds
        names = ["一阶(E1)", "二阶(E2)", "三阶(E3)"] if not reverse else ["逆一阶(E1*)", "逆二阶(E2*)", "逆三阶(E3*)"]
        stage = 0
        for i, th in enumerate(thresholds):
            if energy_level >= th:
                stage = i + 1
        return {
            "energy_level": energy_level,
            "stage": stage,
            "stage_name": names[stage - 1] if stage > 0 else "未变身",
            "is_reverse": reverse
        }

    def mirror_symmetry_verify(self) -> Dict[str, any]:
        """镜像对称验证"""
        results = []
        for i in range(3):
            f = self._forward_thresholds[i]
            r = self._reverse_thresholds[i]
            results.append({
                f"E{i+1}": f,
                f"E{i+1}*": r,
                "sum": f + r,
                "symmetric": abs(f + r - 1.0) < 1e-10
            })
        all_sym = all(r["symmetric"] for r in results)
        return {
            "pairs": results,
            "all_symmetric": all_sym,
            "expression": "E_i + E_i* = 1"
        }

    def energy_conservation_check(self, f_energy: float, r_energy: float) -> Dict[str, any]:
        """能量守恒检查"""
        total = f_energy + r_energy
        return {
            "forward_energy": f_energy,
            "reverse_energy": r_energy,
            "total": total,
            "conserved": abs(total - 1.0) < 1e-10
        }

    def six_stage_overview(self) -> Dict[str, any]:
        """六阶变身总览"""
        return {
            "forward_stages": [
                {"name": "一阶蓝光", "threshold": self._forward_thresholds[0]},
                {"name": "二阶青光", "threshold": self._forward_thresholds[1]},
                {"name": "三阶金光", "threshold": self._forward_thresholds[2]},
            ],
            "reverse_stages": [
                {"name": "逆一阶红光", "threshold": self._reverse_thresholds[0]},
                {"name": "逆二阶紫光", "threshold": self._reverse_thresholds[1]},
                {"name": "逆三阶白光", "threshold": self._reverse_thresholds[2]},
            ],
            "total_stages": 6,
            "mirror_symmetric": True
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        for i in range(3):
            if abs(self._forward_thresholds[i] + self._reverse_thresholds[i] - 1.0) > 1e-10:
                errors.append(f"第{i+1}阶不满足镜像对称 E_i + E_i* = 1")
        return (len(errors) == 0, errors)
