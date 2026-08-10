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
【对应公理：本源自激相变终极公理·阶段三】

NineRealmsEmergence —— 九界涌现生成器
秩序生成，九界从虚空中逐层涌现
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


REALM_NAMES = [
    "虚无寂灭界(V0)",
    "地府魔界(H-)",
    "物质实体界(R+)",
    "虚拟模态界(M+)",
    "精神意识界(C+)",
    "社会秩序界(S+)",
    "全域统合界(A+)",
    "神仙公理界(A++)",
    "克苏鲁混沌污染界(H?)"
]

REALM_RADIUS_BASE = [0.1, 0.25, 0.4, 0.55, 0.7, 0.82, 0.9, 0.97, 1.0]


class NineRealmsEmergence(BaseTheoryModule):
    """九界涌现生成器"""

    module_id = "T29_C03"
    module_name = "九界涌现生成器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·本源自激相变元机制"
    corresponding_axiom = "本源自激相变终极公理·阶段三衍秩序生九界"
    is_origin_locked = True
    dependencies = ["T29", "T29_C01", "T29_C02"]

    def __init__(self):
        super().__init__()
        self._emerged_realms = []
        self._order_level = 0.0

    def emerge_all(self, potential: float = 1.0) -> Dict[str, any]:
        """逐层涌现全部九界"""
        self._emerged_realms = []
        for i in range(self.constants.NUM_REALMS):
            realm = self._emerge_single(i, potential)
            self._emerged_realms.append(realm)
        self._order_level = self._compute_order_level()
        return {
            "total_realms": len(self._emerged_realms),
            "order_level": self._order_level,
            "realms": self._emerged_realms
        }

    def _emerge_single(self, index: int, potential: float) -> Dict:
        """涌现单个界域"""
        radius = REALM_RADIUS_BASE[index] * potential
        energy = radius * self.constants.gamma
        return {
            "index": index,
            "name": REALM_NAMES[index],
            "radius": radius,
            "energy_density": energy,
            "emerged": True
        }

    def _compute_order_level(self) -> float:
        """计算秩序水平"""
        if not self._emerged_realms:
            return 0.0
        total_energy = sum(r["energy_density"] for r in self._emerged_realms)
        return self.constants.gamma * total_energy / len(self._emerged_realms)

    def get_realm(self, name_or_index):
        """获取指定界域"""
        if isinstance(name_or_index, int):
            if 0 <= name_or_index < len(self._emerged_realms):
                return self._emerged_realms[name_or_index]
        elif isinstance(name_or_index, str):
            for r in self._emerged_realms:
                if name_or_index in r["name"]:
                    return r
        return None

    def get_order_entropy(self) -> float:
        """获取秩序熵值（负值代表秩序）"""
        return -self._order_level

    @property
    def emerged_count(self) -> int:
        return len(self._emerged_realms)

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(REALM_NAMES) != self.constants.NUM_REALMS:
            errors.append(f"九界数量必须为 {self.constants.NUM_REALMS}")
        if len(REALM_RADIUS_BASE) != self.constants.NUM_REALMS:
            errors.append(f"九界半径数组长度必须为 {self.constants.NUM_REALMS}")
        return (len(errors) == 0, errors)
