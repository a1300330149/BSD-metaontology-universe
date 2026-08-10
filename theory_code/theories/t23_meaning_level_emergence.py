"""
【归属基底：L2_无限之子层·意义层级涌现公理】
【对应公理：意义层级涌现公理】

T23 —— 四层意义层级涌现
量子物理意义 → 宏观物理化学意义 → 生态生物意义 → 意识文化意义
四层意义逐级涌现，层级不可逆，跨层级传导
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class MeaningLevelEmergence(BaseTheoryModule):
    """
    意义层级涌现公理

    四层意义：
    L1 量子物理意义：量子涨落、粒子相互作用、基本力
    L2 宏观物理化学意义：物质结构、化学反应、热力学
    L3 生态生物意义：生命现象、生态系统、演化规律
    L4 意识文化意义：精神意识、文化艺术、价值意义

    核心特性：
    - 逐级涌现：低层为高层奠基
    - 层级不可逆：高层不能还原为低层
    - 跨层级传导：意义可跨层级传递
    - 意义守恒：总量守恒，形态转化
    """

    module_id = "T23"
    module_name = "四层意义层级涌现"
    version = "V1.0_终版"
    cosmic_level = 2
    base_belong = "L2_无限之子层·意义层级涌现公理"
    corresponding_axiom = "意义层级涌现公理"
    is_origin_locked = True
    dependencies = ["T8", "T20"]

    def __init__(self):
        super().__init__()
        self.meaning_levels = [
            "量子物理意义",
            "宏观物理化学意义",
            "生态生物意义",
            "意识文化意义"
        ]
        self._level_properties = {}
        self._emergence_thresholds = {}
        self._irreversibility_degree = 0.0
        self._conservation_degree = 0.0
        self._init_level_properties()

    def _init_level_properties(self):
        """初始化各层意义属性"""
        level_names = ["量子物理意义", "宏观物理化学意义", "生态生物意义", "意识文化意义"]
        descriptions = [
            "量子涨落、粒子相互作用、基本力",
            "物质结构、化学反应、热力学",
            "生命现象、生态系统、演化规律",
            "精神意识、文化艺术、价值意义"
        ]
        carriers = [
            "基本粒子、量子场",
            "原子、分子、化合物",
            "细胞、有机体、生态系统",
            "大脑、意识、文化符号"
        ]

        for i, (name, desc, carrier) in enumerate(zip(level_names, descriptions, carriers)):
            self._level_properties[name] = {
                "level": i + 1,
                "description": desc,
                "carrier": carrier,
                "complexity": (i + 1) * 0.25,
                "meaning_density": 1.0 / (i + 1)
            }
            self._emergence_thresholds[name] = self.constants.E1 + i * 0.2

    def four_meaning_levels_definition(self) -> Dict[str, Any]:
        """四层意义定义推演"""
        level_details = {}
        for level in self.meaning_levels:
            props = self._level_properties[level]
            level_details[level] = {
                "层级": f"L{props['level']}",
                "描述": props["description"],
                "承载者": props["carrier"],
                "复杂度": props["complexity"],
                "意义密度": round(props["meaning_density"], 4)
            }

        return {
            "total_levels": len(self.meaning_levels),
            "bottom_level": self.meaning_levels[0],
            "top_level": self.meaning_levels[-1],
            "level_details": level_details,
            "definition_principle": "从微观到宏观，从物质到精神"
        }

    def meaning_emergence_conditions_mechanism(self, start_level: int = 1) -> Dict[str, Any]:
        """意义涌现条件与机制推演"""
        if start_level < 1 or start_level >= len(self.meaning_levels):
            return {"error": "起始层级必须在1到3之间"}

        lower_level = self.meaning_levels[start_level - 1]
        higher_level = self.meaning_levels[start_level]

        threshold = self._emergence_thresholds[higher_level]
        emergence_probability = 1.0 - math.exp(-self.constants.gamma * threshold * 10)

        conditions = [
            f"低层（{lower_level}）复杂度积累到临界值",
            f"低层要素相互作用达到阈值 {threshold}",
            "系统开放性：与环境有物质能量交换",
            "反馈机制：正反馈放大涨落",
            "自组织：系统自发形成有序结构"
        ]

        mechanism_steps = [
            "步骤1：低层系统充分发展，复杂度积累",
            "步骤2：涨落触发，临界相变点临近",
            "步骤3：自组织发生，新层级结构涌现",
            "步骤4：新层级稳定化，形成独立规则",
            "步骤5：高层对低层产生下向因果作用"
        ]

        return {
            "from_level": lower_level,
            "to_level": higher_level,
            "emergence_threshold": threshold,
            "emergence_probability": round(emergence_probability, 4),
            "conditions": conditions,
            "mechanism_steps": mechanism_steps,
            "emergence_principle": "量变引起质变，低层涌现高层"
        }

    def meaning_level_irreversibility(self) -> Dict[str, Any]:
        """意义层级不可逆性推演"""
        self._irreversibility_degree = 1.0 - math.exp(-self.constants.kappa * 4)

        irreversibility_evidence = [
            "高层性质不能完全还原为低层性质",
            "高层具有低层没有的涌现属性",
            "下向因果：高层可影响低层，反之不可",
            "时间箭头：涌现方向单向，不可倒退",
            "信息损失：高层描述会损失低层细节"
        ]

        reduction_limits = {
            "意识→生物": "意识体验不能完全还原为神经活动",
            "生物→化学": "生命现象不能完全还原为化学反应",
            "化学→物理": "分子性质不能完全还原为粒子物理"
        }

        return {
            "irreversibility_degree": self._irreversibility_degree,
            "irreversible": self._irreversibility_degree > self.constants.E2,
            "evidence": irreversibility_evidence,
            "reduction_limits": reduction_limits,
            "principle": "层级涌现是单向的，高层不可完全还原为低层"
        }

    def meaning_cross_level_conduction(self, from_level: str = "量子物理意义",
                                        to_level: str = "意识文化意义",
                                        intensity: float = 1.0) -> Dict[str, Any]:
        """意义跨层级传导推演"""
        if from_level not in self._level_properties or to_level not in self._level_properties:
            return {"error": "指定的意义层级不存在"}

        from_idx = self._level_properties[from_level]["level"]
        to_idx = self._level_properties[to_level]["level"]
        level_diff = abs(to_idx - from_idx)

        if level_diff == 0:
            conduction_efficiency = 1.0
        else:
            conduction_efficiency = math.exp(-self.constants.alpha * level_diff)

        conducted_meaning = intensity * conduction_efficiency

        if to_idx > from_idx:
            direction = "上行传导（向上涌现）"
        elif to_idx < from_idx:
            direction = "下行传导（下向因果）"
        else:
            direction = "同层传导"

        conduction_paths = [
            "直接传导：相邻层级直接传递",
            "级联传导：逐层传递经过中间层",
            "共振传导：跨层级共振增强",
            "衰减传导：距离越远衰减越大"
        ]

        return {
            "from_level": from_level,
            "to_level": to_level,
            "level_difference": level_diff,
            "direction": direction,
            "input_intensity": intensity,
            "conduction_efficiency": round(conduction_efficiency, 4),
            "output_meaning": round(conducted_meaning, 4),
            "conduction_paths": conduction_paths,
            "principle": "跨层级传导随距离指数衰减"
        }

    def meaning_conservation_verification(self) -> Dict[str, Any]:
        """意义守恒验证推演"""
        total_meaning = 0.0
        level_contributions = {}

        for level in self.meaning_levels:
            props = self._level_properties[level]
            contribution = props["complexity"] * props["meaning_density"]
            level_contributions[level] = round(contribution, 4)
            total_meaning += contribution

        self._conservation_degree = 1.0 - abs(total_meaning - 1.0)
        if self._conservation_degree < 0:
            self._conservation_degree = 0.0

        conservation_forms = [
            "形态转化：意义可在不同层级间转化",
            "总量守恒：意义总量保持不变",
            "局部增减：某层意义可增可减，但总量守恒",
            "质量守恒：高意义密度对应低复杂度，反之亦然"
        ]

        return {
            "level_contributions": level_contributions,
            "total_meaning": round(total_meaning, 4),
            "conservation_degree": self._conservation_degree,
            "conserved": self._conservation_degree > self.constants.E3,
            "conservation_forms": conservation_forms,
            "verification_principle": "意义不生不灭，只转化形态"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T23 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if len(self.meaning_levels) != 4:
            errors.append("意义层级必须恰好4层")
        if "量子物理意义" not in self.meaning_levels:
            errors.append("必须包含量子物理意义层")
        if "宏观物理化学意义" not in self.meaning_levels:
            errors.append("必须包含宏观物理化学意义层")
        if "生态生物意义" not in self.meaning_levels:
            errors.append("必须包含生态生物意义层")
        if "意识文化意义" not in self.meaning_levels:
            errors.append("必须包含意识文化意义层")
        if self.meaning_levels[0] != "量子物理意义":
            errors.append("最底层必须是量子物理意义")
        if self.meaning_levels[-1] != "意识文化意义":
            errors.append("最高层必须是意识文化意义")
        if len(self._level_properties) != 4:
            errors.append("层级属性必须对应4层")
        if "T8" not in self.dependencies:
            errors.append("T23必须依赖T8（意义涌现公理）")
        if "T20" not in self.dependencies:
            errors.append("T23必须依赖T20（九界场域框架）")
        if self.cosmic_level != 2:
            errors.append("T23必须位于L2无限之子层")
        if not self.is_origin_locked:
            errors.append("T23理论必须锁定")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t23 = MeaningLevelEmergence()
    print(f"模块: {t23.module_id} - {t23.module_name}")
    print(f"版本: {t23.version}")
    print(f"层级: L{t23.cosmic_level}")
    print(f"依赖: {t23.dependencies}")
    print(f"锁定: {t23.is_origin_locked}")
    print(f"哈希: {t23.sha256}")
    print()

    print("四层意义定义:")
    defs = t23.four_meaning_levels_definition()
    for level in defs['level_details']:
        detail = defs['level_details'][level]
        print(f"  {detail['层级']} {level}: {detail['描述']}")
    print()

    print("意义涌现机制:")
    emergence = t23.meaning_emergence_conditions_mechanism(2)
    print(f"  从: {emergence['from_level']}")
    print(f"  到: {emergence['to_level']}")
    print(f"  涌现阈值: {emergence['emergence_threshold']:.4f}")
    print(f"  涌现概率: {emergence['emergence_probability']:.4f}")
    print()

    print("层级不可逆性:")
    irrev = t23.meaning_level_irreversibility()
    print(f"  不可逆度: {irrev['irreversibility_degree']:.6f}")
    print(f"  不可逆: {irrev['irreversible']}")
    print()

    print("跨层级传导:")
    cond = t23.meaning_cross_level_conduction("量子物理意义", "生态生物意义", 1.0)
    print(f"  方向: {cond['direction']}")
    print(f"  层级差: {cond['level_difference']}")
    print(f"  传导效率: {cond['conduction_efficiency']}")
    print()

    print("意义守恒验证:")
    cons = t23.meaning_conservation_verification()
    print(f"  总意义量: {cons['total_meaning']}")
    print(f"  守恒度: {cons['conservation_degree']:.6f}")
    print(f"  守恒: {cons['conserved']}")
    print()

    valid, errs = t23.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
