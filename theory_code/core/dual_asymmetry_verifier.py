"""
【归属基底：L0_总本源层·全域双界域隔离壁垒本源】
【对应公理：双界域隔离终极公理·对偶对称验算】

DualAsymmetryVerifier —— 四稳态四异化对偶对称验算器
严丝合缝的对偶对称验证
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class DualAsymmetryVerifier(BaseTheoryModule):
    """四稳态四异化对偶对称验算器"""

    module_id = "T30_C03"
    module_name = "对偶对称验算器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·全域双界域隔离壁垒本源"
    corresponding_axiom = "双界域隔离终极公理·对偶对称验算"
    is_origin_locked = True
    dependencies = ["T30", "T30_C01", "T30_C02"]

    def __init__(self):
        super().__init__()
        self._steady_weights = {}
        self._alien_weights = {}

    def set_weights(self, steady: Dict[str, float], alien: Dict[str, float]):
        """设置两侧权重"""
        self._steady_weights = steady
        self._alien_weights = alien

    def verify_count_symmetry(self) -> bool:
        """数量对称验证"""
        return len(self._steady_weights) == len(self._alien_weights) == 4

    def verify_total_weight_symmetry(self) -> Dict[str, any]:
        """总权重对称验证"""
        s_total = sum(self._steady_weights.values())
        a_total = sum(self._alien_weights.values())
        diff = abs(s_total - a_total)
        return {
            "steady_total": s_total,
            "alien_total": a_total,
            "diff": diff,
            "symmetric": diff < self.constants.theta_neg
        }

    def verify_pairwise_symmetry(self) -> Dict[str, any]:
        """逐对对称验证"""
        pairs = {
            "物质实体界↔地府魔界": ("物质实体界", "地府魔界"),
            "虚拟模态界↔神仙公理界": ("虚拟模态界", "神仙公理界"),
            "精神意识界↔克苏鲁混沌污染界": ("精神意识界", "克苏鲁混沌污染界"),
            "社会秩序界↔全域统合界": ("社会秩序界", "全域统合界"),
        }
        results = {}
        all_symmetric = True
        for pair_name, (s, a) in pairs.items():
            sw = self._steady_weights.get(s, 0)
            aw = self._alien_weights.get(a, 0)
            sym = abs(sw - aw) < self.constants.theta_neg
            results[pair_name] = {"steady": sw, "alien": aw, "symmetric": sym}
            if not sym:
                all_symmetric = False
        return {"pairs": results, "all_symmetric": all_symmetric}

    def full_verification(self) -> Dict[str, any]:
        """完整对偶对称验证"""
        count_ok = self.verify_count_symmetry()
        weight_result = self.verify_total_weight_symmetry()
        pairwise_result = self.verify_pairwise_symmetry()
        all_pass = count_ok and weight_result["symmetric"] and pairwise_result["all_symmetric"]
        return {
            "count_symmetry": count_ok,
            "total_weight_symmetry": weight_result,
            "pairwise_symmetry": pairwise_result,
            "all_verified": all_pass,
            "verdict": "对偶完全对称" if all_pass else "存在不对称"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
