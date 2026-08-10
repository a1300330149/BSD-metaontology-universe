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
【对应公理：双界域隔离终极公理·外边界CPFB】

CPFBOuterContainer —— 外边界宇宙可能性场容器
九界实存全集 / 超界无限可能 的全域容器
"""

import math
from typing import Dict, List, Set, Tuple
from ..core.base_theory_module import BaseTheoryModule


class CPFBOuterContainer(BaseTheoryModule):
    """外边界CPFB容器"""

    module_id = "T30_C02"
    module_name = "外边界CPFB宇宙可能性场容器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·全域双界域隔离壁垒本源"
    corresponding_axiom = "双界域隔离终极公理·外边界宇宙可能性场"
    is_origin_locked = True
    dependencies = ["T30", "T30_C01"]

    def __init__(self):
        super().__init__()
        self._inner_realms: Set[str] = set()
        self._possibility_density = 1.0
        self._cpfb_permeability = 0.001  # 极低渗透率

    def set_inner_realms(self, realms: List[str]):
        """设置内域九界"""
        self._inner_realms = set(realms)

    def is_within_cpfb(self, realm_name: str) -> bool:
        """判断是否在CPFB内部"""
        return realm_name in self._inner_realms

    def possibility_injection(self, inner_energy: float) -> Dict[str, float]:
        """可能性注入：从可能性场向内域注入"""
        injected = inner_energy * self._cpfb_permeability
        return {
            "inner_energy": inner_energy,
            "possibility_injected": injected,
            "permeability": self._cpfb_permeability,
            "new_inner_energy": inner_energy + injected
        }

    def leak_to_possibility(self, inner_energy: float) -> Dict[str, float]:
        """内域能量泄露至可能性场"""
        leaked = inner_energy * self._cpfb_permeability
        return {
            "inner_energy": inner_energy,
            "leaked": leaked,
            "permeability": self._cpfb_permeability,
            "remaining_inner": inner_energy - leaked
        }

    def cpfb_expansion(self, expansion_factor: float) -> Dict[str, float]:
        """CPFB膨胀：可能性场扩张"""
        new_density = self._possibility_density / expansion_factor
        self._possibility_density = new_density
        return {
            "expansion_factor": expansion_factor,
            "old_density": self._possibility_density * expansion_factor,
            "new_density": new_density
        }

    @property
    def possibility_density(self) -> float:
        return self._possibility_density

    @property
    def inner_realm_count(self) -> int:
        return len(self._inner_realms)

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if self._cpfb_permeability < 0 or self._cpfb_permeability > 1:
            errors.append("CPFB渗透率必须在 [0, 1] 范围内")
        return (len(errors) == 0, errors)
