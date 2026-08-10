"""
【归属基底：L0_总本源层·本源自激相变元机制】
【对应公理：本源自激相变终极公理·阶段二】

DualPolaritySpawner —— 双极裂变动静生成器
动静二分、正反共轭、守恒不破
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class DualPolaritySpawner(BaseTheoryModule):
    """双极裂变动静生成器"""

    module_id = "T29_C02"
    module_name = "双极裂变动静生成器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·本源自激相变元机制"
    corresponding_axiom = "本源自激相变终极公理·阶段二裂变动静"
    is_origin_locked = True
    dependencies = ["T29", "T29_C01"]

    def __init__(self):
        super().__init__()
        self._yang = 0.0  # 动极
        self._yin = 0.0   # 静极
        self._spawned = False

    def spawn(self, potential: float = 1.0, split_ratio: float = 0.5) -> Dict[str, float]:
        """执行动静裂变"""
        if split_ratio < 0 or split_ratio > 1:
            raise ValueError("分裂比例必须在 [0, 1] 范围内")
        self._yang = potential * split_ratio
        self._yin = potential * (1.0 - split_ratio)
        self._spawned = True
        return {
            "yang_dynamic": self._yang,
            "yin_static": self._yin,
            "total": self._yang + self._yin,
            "conservation_error": abs(self._yang + self._yin - potential),
            "spawned": True
        }

    def remerge(self) -> float:
        """动静复归为一（逆过程）"""
        total = self._yang + self._yin
        self._yang = 0.0
        self._yin = 0.0
        self._spawned = False
        return total

    def oscillation(self, omega: float, t: float) -> Dict[str, float]:
        """动静振荡模型"""
        if not self._spawned:
            return {"yang": 0, "yin": 0, "phase": 0}
        total = self._yang + self._yin
        yang_t = total * 0.5 * (1 + math.cos(omega * t))
        yin_t = total * 0.5 * (1 - math.cos(omega * t))
        return {
            "yang": yang_t,
            "yin": yin_t,
            "phase": omega * t,
            "conservation": abs(yang_t + yin_t - total) < 1e-10
        }

    @property
    def yang(self) -> float:
        return self._yang

    @property
    def yin(self) -> float:
        return self._yin

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if self._spawned and abs(self._yang + self._yin) < 1e-10:
            errors.append("裂变后总动静能不应为零")
        return (len(errors) == 0, errors)
