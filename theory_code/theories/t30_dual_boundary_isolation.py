"""
【归属基底：L0_总本源层·全域双界域隔离壁垒本源】
【对应公理：双界域隔离终极公理】

T30 —— 全域双界域隔离壁垒本源
内边界：虚无空白界 VBB
外边界：宇宙可能性场界 CPFB
4稳态 VS 4异化 严格对偶对称
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


STEADY_4 = ["物质实体界", "虚拟模态界", "精神意识界", "社会秩序界"]
ALIEN_4 = ["地府魔界", "神仙公理界", "克苏鲁混沌污染界", "全域统合界"]


class DualBoundaryIsolation(BaseTheoryModule):
    """全域双界域隔离壁垒本源"""

    module_id = "T30"
    module_name = "全域双界域隔离壁垒本源"
    version = "V1.0_终版"
    cosmic_level = 0
    base_belong = "L0_总本源层·全域双界域隔离壁垒本源"
    corresponding_axiom = "双界域隔离终极公理（VBB+CPFB双线边界）"
    is_origin_locked = True
    dependencies = ["T29"]

    def __init__(self):
        super().__init__()
        self._vbb_active = True
        self._cpfb_active = True
        self._contamination_level = 0.0

    def verify_dual_boundary(self) -> Dict[str, any]:
        """验证双界线隔离完整性"""
        vbb_ok = self._verify_vbb()
        cpfb_ok = self._verify_cpfb()
        symmetry_ok = self._verify_symmetry()
        return {
            "vbb_inner_boundary": vbb_ok,
            "cpfb_outer_boundary": cpfb_ok,
            "four_steady_four_alien_symmetry": symmetry_ok,
            "all_boundaries_intact": vbb_ok and cpfb_ok and symmetry_ok,
            "verdict": "双界域隔离完整" if (vbb_ok and cpfb_ok and symmetry_ok) else "存在边界缺陷"
        }

    def _verify_vbb(self) -> bool:
        """验证内边界VBB（虚无空白界）"""
        return self._vbb_active

    def _verify_cpfb(self) -> bool:
        """验证外边界CPFB（宇宙可能性场）"""
        return self._cpfb_active

    def _verify_symmetry(self) -> bool:
        """验证四稳态四异化对偶对称"""
        return len(STEADY_4) == len(ALIEN_4) == 4

    def cross_realm_transfer(self, from_realm: str, to_realm: str, energy: float) -> Dict[str, any]:
        """跨界能量传输（带壁垒检查）"""
        crossing_vbb = self._crosses_vbb(from_realm, to_realm)
        crossing_cpfb = self._crosses_cpfb(to_realm)
        leakage = 0.0
        if crossing_vbb:
            leakage += energy * 0.01
        if crossing_cpfb:
            leakage += energy * 0.05
        actual_transfer = energy - leakage
        self._contamination_level += leakage * 0.001
        return {
            "from": from_realm,
            "to": to_realm,
            "input_energy": energy,
            "leakage": leakage,
            "actual_transfer": actual_transfer,
            "crossed_vbb": crossing_vbb,
            "crossed_cpfb": crossing_cpfb,
            "contamination_increase": leakage * 0.001
        }

    def _crosses_vbb(self, from_r: str, to_r: str) -> bool:
        """判断是否跨越内边界VBB"""
        from_steady = from_r in STEADY_4
        to_steady = to_r in STEADY_4
        return from_steady != to_steady

    def _crosses_cpfb(self, to_r: str) -> bool:
        """判断是否跨出外边界CPFB"""
        return to_r not in STEADY_4 + ALIEN_4 + ["虚无寂灭界"]

    @property
    def contamination_level(self) -> float:
        return self._contamination_level

    def reset_contamination(self):
        """重置污染水平"""
        self._contamination_level = 0.0

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(STEADY_4) != 4:
            errors.append("稳态界必须恰好4个")
        if len(ALIEN_4) != 4:
            errors.append("异化界必须恰好4个")
        return (len(errors) == 0, errors)
