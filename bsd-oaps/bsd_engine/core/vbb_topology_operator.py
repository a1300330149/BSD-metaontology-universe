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
【对应公理：双界域隔离终极公理·内边界VBB】

VBBTopologyOperator —— 内边界虚无空白界拓扑算子
稳态/异化的平衡隔离转轴
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class VBBTopologyOperator(BaseTheoryModule):
    """内边界VBB拓扑算子"""

    module_id = "T30_C01"
    module_name = "内边界VBB拓扑算子"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·全域双界域隔离壁垒本源"
    corresponding_axiom = "双界域隔离终极公理·内边界虚无空白界"
    is_origin_locked = True
    dependencies = ["T30"]

    def __init__(self):
        super().__init__()
        self._vbb_radius = 0.0
        self._steady_side_entropy = 0.0
        self._alien_side_entropy = 0.0

    def set_vbb_radius(self, radius: float):
        """设置VBB半径"""
        self._vbb_radius = radius

    def balance_check(self) -> Dict[str, any]:
        """平衡检查：稳态侧 vs 异化侧"""
        diff = abs(self._steady_side_entropy - self._alien_side_entropy)
        balanced = diff < self.constants.theta_neg
        return {
            "steady_side_entropy": self._steady_side_entropy,
            "alien_side_entropy": self._alien_side_entropy,
            "entropy_diff": diff,
            "balanced": balanced,
            "vbb_radius": self._vbb_radius
        }

    def set_entropy(self, steady: float, alien: float):
        """设置两侧熵值"""
        self._steady_side_entropy = steady
        self._alien_side_entropy = alien

    def vbb_reflection(self, incoming_energy: float) -> Dict[str, float]:
        """VBB反射：零态界面能量反射/透射"""
        reflectivity = 0.99  # 99% 反射
        transmitted = incoming_energy * (1 - reflectivity)
        reflected = incoming_energy * reflectivity
        return {
            "incoming": incoming_energy,
            "reflected": reflected,
            "transmitted": transmitted,
            "reflectivity": reflectivity
        }

    def zero_point_rotation(self, angle: float) -> Dict[str, float]:
        """零点转轴旋转"""
        steady_new = self._steady_side_entropy * math.cos(angle) - self._alien_side_entropy * math.sin(angle)
        alien_new = self._steady_side_entropy * math.sin(angle) + self._alien_side_entropy * math.cos(angle)
        return {
            "angle_rad": angle,
            "steady_after": steady_new,
            "alien_after": alien_new,
            "rotation_conservation": abs(steady_new + alien_new - self._steady_side_entropy - self._alien_side_entropy) < 1e-10
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
