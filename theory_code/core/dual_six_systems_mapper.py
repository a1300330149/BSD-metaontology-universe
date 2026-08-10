"""
【归属基底：L0_总本源层·元道本体规则·对偶性体系】
【对应公理：T2 六系对偶定理】

DualSixSystemsMapper —— 六系对偶映射算子
实存六系 ↔ 可能六系，12系全域对偶
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


SIX_NAMES_REAL = ["实体系(R)", "模态系(M)", "认知系(C)", "社会系(S)", "公理系(A)", "混沌系(H)"]
SIX_NAMES_DUAL = ["实体对偶系(R*)", "模态对偶系(M*)", "认知对偶系(C*)", "社会对偶系(S*)", "公理对偶系(A*)", "混沌对偶系(H*)"]


class DualSixSystemsMapper(BaseTheoryModule):
    """六系对偶映射算子"""

    module_id = "T32_C01"
    module_name = "六系对偶映射算子"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·对偶性体系"
    corresponding_axiom = "T2 六系对偶定理（12系全域对偶）"
    is_origin_locked = True
    dependencies = ["T32"]

    def __init__(self):
        super().__init__()
        self._mapping = dict(zip(SIX_NAMES_REAL, SIX_NAMES_DUAL))
        self._reverse_mapping = dict(zip(SIX_NAMES_DUAL, SIX_NAMES_REAL))

    def map_to_dual(self, system_name: str) -> str:
        """实存 → 对偶"""
        return self._mapping.get(system_name, f"{system_name}*")

    def map_to_real(self, dual_name: str) -> str:
        """对偶 → 实存"""
        return self._reverse_mapping.get(dual_name, dual_name.rstrip("*"))

    def full_mapping_table(self) -> Dict[str, str]:
        """完整映射表"""
        return dict(self._mapping)

    def dual_vector_map(self, real_vector: List[float]) -> List[float]:
        """实存向量 → 对偶向量"""
        if len(real_vector) != 6:
            raise ValueError("六系向量长度必须为6")
        return [-v for v in real_vector]  # 熵值取反

    def total_12_system_entropy(self, real_vec: List[float], dual_vec: List[float]) -> Dict[str, any]:
        """12系总熵计算"""
        s_real = sum(real_vec)
        s_dual = sum(dual_vec)
        total = s_real + s_dual
        return {
            "real_6_system_entropy": s_real,
            "dual_6_system_entropy": s_dual,
            "total_12_system_entropy": total,
            "conserved": abs(total) < self.constants.theta_neg,
            "theorem": "S_实存六系 + S_可能六系 = 常数"
        }

    def self_inverse_check(self) -> bool:
        """自逆性检查"""
        for name in SIX_NAMES_REAL:
            dual = self.map_to_dual(name)
            back = self.map_to_real(dual)
            if back != name:
                return False
        return True

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(SIX_NAMES_REAL) != self.constants.NUM_SIX_SYS:
            errors.append("实存六系必须为6个")
        if len(SIX_NAMES_DUAL) != self.constants.NUM_SIX_SYS:
            errors.append("对偶六系必须为6个")
        return (len(errors) == 0, errors)
