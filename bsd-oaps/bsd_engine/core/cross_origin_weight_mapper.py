"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·元道本体规则·平行本源体系】
【对应公理：跨本源权重映射公理】

CrossOriginWeightMapper —— 跨本源权重映射器
不同本源五论体系间的权重映射
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class CrossOriginWeightMapper(BaseTheoryModule):
    """跨本源权重映射器"""

    module_id = "T33_C03"
    module_name = "跨本源权重映射器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·平行本源体系"
    corresponding_axiom = "跨本源权重映射公理"
    is_origin_locked = True
    dependencies = ["T33", "T33_C01", "T33_C02"]

    def __init__(self):
        super().__init__()
        self._mapping_functions = {}

    def register_mapping(self, from_origin: str, to_origin: str, func_name: str):
        """注册映射函数"""
        key = f"{from_origin}->{to_origin}"
        self._mapping_functions[key] = func_name

    def map_weights(self, weights: Dict[str, float],
                    from_origin: str, to_origin: str) -> Dict[str, float]:
        """映射五论权重"""
        key = f"{from_origin}->{to_origin}"
        if key in self._mapping_functions:
            return self._apply_mapping(weights, key)
        # 默认映射：熵值取反（对偶型）
        return {k: 1 - v for k, v in weights.items()}

    def _apply_mapping(self, weights: Dict[str, float], key: str) -> Dict[str, float]:
        """应用映射"""
        func = self._mapping_functions[key]
        if func == "inverse":
            return {k: 1 - v for k, v in weights.items()}
        elif func == "same":
            return dict(weights)
        elif func == "sqrt":
            return {k: math.sqrt(v) for k, v in weights.items()}
        else:
            return dict(weights)

    def weight_normalization_check(self, weights: Dict[str, float]) -> Dict[str, any]:
        """权重归一化检查"""
        total = sum(weights.values())
        normalized = abs(total - 1.0) < self.constants.theta_neg
        return {
            "total_weight": total,
            "normalized": normalized,
            "tolerance": self.constants.theta_neg
        }

    def dual_mapping_cycle(self, weights: Dict[str, float]) -> Dict[str, any]:
        """对偶映射循环：正→逆→正"""
        mapped = self.map_weights(weights, "steady", "possibility")
        back = self.map_weights(mapped, "possibility", "steady")
        error = sum(abs(weights[k] - back.get(k, 0)) for k in weights)
        return {
            "original": weights,
            "mapped_to_possibility": mapped,
            "mapped_back": back,
            "round_trip_error": error,
            "self_inverse_holds": error < self.constants.theta_neg
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
