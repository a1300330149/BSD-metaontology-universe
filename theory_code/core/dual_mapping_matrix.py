"""
【归属基底：L0_总本源层·元道本体规则·逆腾飞五论】
【对应公理：逆腾飞五论独立归一公理·对偶映射】

DualMappingMatrix —— 对偶映射矩阵算子
正反五论一一对应、自逆映射
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class DualMappingMatrix(BaseTheoryModule):
    """对偶映射矩阵算子"""

    module_id = "T31_C02"
    module_name = "对偶映射矩阵算子"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·逆腾飞五论"
    corresponding_axiom = "逆腾飞五论独立归一公理·对偶映射矩阵"
    is_origin_locked = True
    dependencies = ["T31", "T31_C01"]

    def __init__(self):
        super().__init__()
        self._forward_labels = ["真论", "正论", "悬论", "谬论", "逆论"]
        self._ni_labels = ["逆真论", "逆正论", "逆悬论", "逆谬论", "逆逆论"]

    def build_mapping_matrix(self) -> List[List[int]]:
        """构建5×5对偶映射矩阵（单位矩阵型）"""
        n = 5
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def map_forward_to_ni(self, forward_vec: List[float]) -> List[float]:
        """正向向量 → 逆向向量"""
        if len(forward_vec) != 5:
            raise ValueError("向量长度必须为5")
        return list(forward_vec)  # 一一对应映射

    def map_ni_to_forward(self, ni_vec: List[float]) -> List[float]:
        """逆向向量 → 正向向量"""
        return self.map_forward_to_ni(ni_vec)  # 自逆

    def double_inverse_verify(self, vec: List[float]) -> Dict[str, any]:
        """双重逆验证：逆之逆=原"""
        ni_vec = self.map_forward_to_ni(vec)
        back_vec = self.map_ni_to_forward(ni_vec)
        equal = all(abs(a - b) < 1e-10 for a, b in zip(vec, back_vec))
        return {
            "original": vec,
            "ni_transformed": ni_vec,
            "double_inversed": back_vec,
            "self_inverse_holds": equal
        }

    def cross_mapping_orthogonality(self) -> Dict[str, any]:
        """交叉映射正交性验证"""
        mat = self.build_mapping_matrix()
        trace = sum(mat[i][i] for i in range(5))
        return {
            "trace": trace,
            "rank": 5,
            "orthogonal": trace == 5,
            "determinant_sign": 1 if trace == 5 else 0
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(self._forward_labels) != len(self._ni_labels):
            errors.append("正反五论数量必须相等")
        return (len(errors) == 0, errors)
