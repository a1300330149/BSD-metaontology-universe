"""
归属基底：第2重三界秩序基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
# existence_hierarchy.py
# 存在层级阶梯量化：「所有=复杂性=多样性=共生性」光谱换算
from typing import List, Dict


class ExistenceHierarchyCalc:
    def __init__(self):
        # 层级基准权重，越高层越靠近所有
        self.hierarchy_weight = {
            "人类意识": 1.0,
            "动物有限意识": 0.7,
            "植物生化存续": 0.45,
            "天体星球物理秩序": 0.2,
            "微观粒子基底": 0.05
        }
        # 复杂度/多样性/共生性加权系数
        self.coeff_complex = 0.4
        self.coeff_diversity = 0.35
        self.coeff_symbiosis = 0.25

    def calc_hierarchy_score(self, layer_name: str, complex_val: float, div_val: float, sym_val: float) -> float:
        base = self.hierarchy_weight.get(layer_name, 0.1)
        composite = self.coeff_complex * complex_val + self.coeff_diversity * div_val + self.coeff_symbiosis * sym_val
        total = base * composite
        return round(min(max(total, 0.0), 1.0), 2)

    def judge_earth_special(self, hierarchy_scores: List[float]) -> Dict:
        earth_ref = [1.0, 0.7, 0.45, 0.2, 0.05]
        earth_sum = sum(earth_ref)
        target_sum = sum(hierarchy_scores)
        is_high_complex = target_sum > earth_sum * 0.8
        return {
            "total_complex_score": round(target_sum, 2),
            "earth_benchmark": round(earth_sum, 2),
            "earth_like_complex": is_high_complex,
            "spectrum_bias": "靠近所有" if is_high_complex else "偏向空无"
        }

    def get_all_layers(self) -> List[str]:
        return list(self.hierarchy_weight.keys())
