"""
【归属基底：L0_总本源层·意义守恒与权重公理】
【对应公理：意义权重公理（公理九）+ 意义守恒公理（公理十）】

T9 —— 意义守恒与权重公理
全域意义总量守恒，意义权重按层级分配
意义转化有损耗，意义衰减有定律
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class MeaningConservationAxiom(BaseTheoryModule):
    """
    意义守恒与权重公理
    
    核心要义：
    - 意义守恒方程：全域意义总量不变
    - 权重计算模型：层级越高权重越大
    - 意义转化效率：转化有损耗
    - 意义衰减定律：意义随距离/时间衰减
    """

    module_id = "T9"
    module_name = "意义守恒与权重公理"
    version = "V1.0_终版"
    cosmic_level = 0
    base_belong = "L0_总本源层·意义守恒与权重公理"
    corresponding_axiom = "意义权重公理（公理九）+ 意义守恒公理（公理十）"
    is_origin_locked = True
    dependencies = ["T8"]

    def __init__(self):
        super().__init__()
        self._total_meaning = 1.0
        self._conversion_efficiency = self.constants.gamma
        self._decay_rate = self.constants.alpha
        self._weight_hierarchy = {}
        self._init_weight_hierarchy()

    def _init_weight_hierarchy(self):
        """初始化权重层级"""
        levels = ["L0本源", "L1母科", "L2无限之子", "L3应用"]
        for i, level in enumerate(levels):
            self._weight_hierarchy[level] = math.pow(10, 3 - i)

    def meaning_conservation_equation(self) -> Dict[str, Any]:
        """意义守恒方程推演"""
        return {
            "total_meaning": self._total_meaning,
            "conservation_formula": "∑意义_i = 常数",
            "neither_created_nor_destroyed": True,
            "form_transformation": True,
            "global_conservation": "全域意义总量严格守恒",
            "local_fluctuation": "局部意义可涨落，全域总量不变"
        }

    def weight_calculation_model(self) -> Dict[str, Dict[str, Any]]:
        """权重计算模型推演"""
        model = {}
        for level, base_weight in self._weight_hierarchy.items():
            model[level] = {
                "base_weight": base_weight,
                "log_weight": math.log10(base_weight),
                "relative_importance": base_weight / max(self._weight_hierarchy.values()),
                "calculation_formula": f"权重 = 10^(层级倒数)"
            }
        return model

    def meaning_conversion_efficiency(self, from_level: str, to_level: str) -> Dict[str, Any]:
        """意义转化效率推演"""
        level_order = ["L3应用", "L2无限之子", "L1母科", "L0本源"]
        from_idx = level_order.index(from_level) if from_level in level_order else 0
        to_idx = level_order.index(to_level) if to_level in level_order else 0
        
        level_diff = abs(to_idx - from_idx)
        efficiency = math.pow(self._conversion_efficiency, level_diff)
        
        return {
            "from_level": from_level,
            "to_level": to_level,
            "level_difference": level_diff,
            "conversion_efficiency": efficiency,
            "loss_ratio": 1.0 - efficiency,
            "principle": "层级差越大，转化损耗越大"
        }

    def meaning_decay_law(self, distance: float, initial_meaning: float = 1.0) -> Dict[str, Any]:
        """意义衰减定律推演"""
        decayed = initial_meaning * math.exp(-self._decay_rate * distance)
        return {
            "initial_meaning": initial_meaning,
            "distance": distance,
            "decay_rate": self._decay_rate,
            "remaining_meaning": decayed,
            "decayed_amount": initial_meaning - decayed,
            "decay_formula": "M(d) = M0 * e^(-λd)",
            "half_life": math.log(2) / self._decay_rate
        }

    def get_level_weight(self, level: str) -> Optional[float]:
        """获取层级权重"""
        return self._weight_hierarchy.get(level)

    def validate(self) -> Tuple[bool, List[str]]:
        """T9 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(self._weight_hierarchy) != 4:
            errors.append("权重层级必须恰好4个")
        if "L0本源" not in self._weight_hierarchy:
            errors.append("必须包含L0本源层级")
        if "L1母科" not in self._weight_hierarchy:
            errors.append("必须包含L1母科层级")
        if "L2无限之子" not in self._weight_hierarchy:
            errors.append("必须包含L2无限之子层级")
        if "L3应用" not in self._weight_hierarchy:
            errors.append("必须包含L3应用层级")
        if self._total_meaning <= 0:
            errors.append("总意义量必须大于零")
        if "T8" not in self.dependencies:
            errors.append("T9必须依赖T8")
        if self.cosmic_level != 0:
            errors.append("T9必须位于L0本源层")
        if not self.is_origin_locked:
            errors.append("T9本源理论必须锁定")
        if not hasattr(self, 'meaning_conservation_equation'):
            errors.append("必须实现意义守恒方程方法")
        if not hasattr(self, 'meaning_conversion_efficiency'):
            errors.append("必须实现意义转化效率方法")
        if not hasattr(self, 'meaning_decay_law'):
            errors.append("必须实现意义衰减定律方法")
        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t9 = MeaningConservationAxiom()
    print(f"模块: {t9.module_id} - {t9.module_name}")
    print(f"版本: {t9.version}")
    print(f"层级: L{t9.cosmic_level}")
    print(f"依赖: {t9.dependencies}")
    print(f"锁定: {t9.is_origin_locked}")
    print(f"哈希: {t9.sha256}")
    print()
    
    print("意义守恒方程:")
    cons = t9.meaning_conservation_equation()
    print(f"  总意义量: {cons['total_meaning']}")
    print(f"  守恒公式: {cons['conservation_formula']}")
    print()
    
    print("权重计算模型:")
    weights = t9.weight_calculation_model()
    for level, val in weights.items():
        print(f"  {level}: {val['base_weight']:.0f}")
    print()
    
    print("意义转化效率:")
    conv = t9.meaning_conversion_efficiency("L0本源", "L3应用")
    print(f"  转化率: {conv['conversion_efficiency']:.6f}")
    print(f"  损耗率: {conv['loss_ratio']:.6f}")
    print()
    
    print("意义衰减定律:")
    decay = t9.meaning_decay_law(5.0)
    print(f"  半衰期: {decay['half_life']:.4f}")
    print(f"  剩余意义: {decay['remaining_meaning']:.6f}")
    print()
    
    valid, errs = t9.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
