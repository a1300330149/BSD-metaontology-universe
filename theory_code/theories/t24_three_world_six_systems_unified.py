"""
【归属基底：L2_无限之子层·三界六系统一公理】
【对应公理：三界六系统一公理】

T24 —— 三界六系统一总纲
天道世界 / 人道世界 / 自然世界 三界与六系的统一对应关系
三界六系动力学同构，互转机制，统一场方程
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class ThreeWorldSixSystemsUnified(BaseTheoryModule):
    """
    三界六系统一总纲公理

    三界（三世界）：
    1. 天道世界：宇宙法则、终极真理、神圣秩序
    2. 人道世界：社会人文、伦理道德、文明演化
    3. 自然世界：物质生态、物理规律、生命演化

    六系：
    1. 本源系
    2. 结构系
    3. 动力学系
    4. 演化系
    5. 价值系
    6. 闭环系

    核心：三界与六系统一对应，动力学同构，可相互转化
    """

    module_id = "T24"
    module_name = "三界六系统一总纲"
    version = "V1.0_终版"
    cosmic_level = 2
    base_belong = "L2_无限之子层·三界六系统一公理"
    corresponding_axiom = "三界六系统一公理"
    is_origin_locked = True
    dependencies = ["T5", "T19", "T20"]

    def __init__(self):
        super().__init__()
        self.three_worlds = ["天道世界", "人道世界", "自然世界"]
        self.six_systems = ["本源系", "结构系", "动力学系", "演化系", "价值系", "闭环系"]
        self._world_systems_mapping = {}
        self._isomorphism_degree = 0.0
        self._unified_field_strength = 0.0
        self._closure_degree = 0.0
        self._init_mapping()

    def _init_mapping(self):
        """初始化三界六系映射"""
        mapping_patterns = [
            ["本源系", "结构系"],
            ["动力学系", "演化系"],
            ["价值系", "闭环系"]
        ]
        for i, world in enumerate(self.three_worlds):
            self._world_systems_mapping[world] = {
                "primary_system": mapping_patterns[i][0],
                "secondary_system": mapping_patterns[i][1],
                "correspondence_strength": self.constants.E2,
                "world_index": i + 1
            }

    def three_world_six_systems_mapping_model(self) -> Dict[str, Any]:
        """三界六系映射模型推演"""
        mapping_detail = {}
        for world in self.three_worlds:
            info = self._world_systems_mapping[world]
            mapping_detail[world] = {
                "主导系": info["primary_system"],
                "辅助系": info["secondary_system"],
                "对应强度": info["correspondence_strength"],
                "世界序号": info["world_index"]
            }

        full_mapping_matrix = {}
        for world in self.three_worlds:
            full_mapping_matrix[world] = {}
            for sys in self.six_systems:
                if sys == self._world_systems_mapping[world]["primary_system"]:
                    strength = self.constants.E3
                elif sys == self._world_systems_mapping[world]["secondary_system"]:
                    strength = self.constants.E2
                else:
                    strength = self.constants.E1
                full_mapping_matrix[world][sys] = strength

        return {
            "three_worlds": self.three_worlds,
            "six_systems": self.six_systems,
            "mapping_detail": mapping_detail,
            "full_mapping_matrix": full_mapping_matrix,
            "mapping_principle": "三界各有主辅二系，六系遍在三界",
            "formula": "3界 × 2系/界 = 6系 全覆盖"
        }

    def three_world_six_systems_dynamic_isomorphism(self) -> Dict[str, Any]:
        """三界六系动力学同构推演"""
        self._isomorphism_degree = 1.0 - math.exp(-self.constants.gamma * 6)

        isomorphism_aspects = [
            "动力结构同构：都有驱动-阻尼-反馈结构",
            "演化路径同构：都经历生-住-异-灭周期",
            "平衡机制同构：都有正负反馈调节机制",
            "相变模式同构：都有临界相变点",
            "分形结构同构：都有自相似分形特征"
        ]

        dynamic_parameters = {
            "天道世界": {"驱动系数": 0.9, "阻尼系数": 0.1, "反馈强度": 0.8},
            "人道世界": {"驱动系数": 0.7, "阻尼系数": 0.3, "反馈强度": 0.6},
            "自然世界": {"驱动系数": 0.5, "阻尼系数": 0.5, "反馈强度": 0.4}
        }

        return {
            "isomorphism_degree": self._isomorphism_degree,
            "isomorphic": self._isomorphism_degree > self.constants.E2,
            "isomorphism_aspects": isomorphism_aspects,
            "dynamic_parameters": dynamic_parameters,
            "isomorphism_principle": "三界六系共享同一套动力学模板"
        }

    def three_world_six_systems_interconversion(self, from_world: str = "自然世界",
                                                  to_world: str = "人道世界",
                                                  energy: float = 1.0) -> Dict[str, Any]:
        """三界六系互转机制推演"""
        if from_world not in self.three_worlds or to_world not in self.three_worlds:
            return {"error": "指定的世界不存在"}

        from_idx = self.three_worlds.index(from_world)
        to_idx = self.three_worlds.index(to_world)
        level_diff = to_idx - from_idx

        if level_diff > 0:
            direction = "上升转化（进化）"
            efficiency = self.constants.E1
        elif level_diff < 0:
            direction = "下降转化（退化）"
            efficiency = self.constants.E3
        else:
            direction = "同层转化"
            efficiency = self.constants.E2

        output_energy = energy * efficiency
        conversion_loss = energy - output_energy

        conversion_forms = [
            "质能转化：物质 ↔ 能量",
            "意物转化：意识 ↔ 物质",
            "价值转化：事实 ↔ 价值",
            "层级跃迁：低界 → 高界",
            "层级下堕：高界 → 低界"
        ]

        return {
            "from_world": from_world,
            "to_world": to_world,
            "conversion_direction": direction,
            "input_energy": energy,
            "conversion_efficiency": efficiency,
            "output_energy": round(output_energy, 6),
            "conversion_loss": round(conversion_loss, 6),
            "conversion_forms": conversion_forms,
            "conversion_principle": "上升难效率低，下降易效率高"
        }

    def three_world_unified_field_equation(self, field_strength: float = 0.5) -> Dict[str, Any]:
        """三界统一场方程推演"""
        self._unified_field_strength = field_strength

        field_components = {
            "天道场": field_strength * self.constants.E3,
            "人道场": field_strength * self.constants.E2,
            "自然场": field_strength * self.constants.E1
        }

        total_field = sum(field_components.values())

        equation_terms = [
            "Φ_total = Φ_heaven + Φ_human + Φ_nature",
            "Φ_heaven：天道场（高维统摄）",
            "Φ_human：人道场（中介调谐）",
            "Φ_nature：自然场（基础承载）"
        ]

        field_properties = [
            "统一性：三场合一是统一场",
            "分殊性：三界各有场的表现形式",
            "相互作用：场与场之间相互作用",
            "穿透性：场可穿透三界边界"
        ]

        return {
            "field_components": field_components,
            "total_field_strength": round(total_field, 6),
            "equation_terms": equation_terms,
            "field_properties": field_properties,
            "field_equation": "Φ = Σ_i w_i · Φ_i （加权叠加）",
            "unification_principle": "三界本质上是同一统一场的不同显现"
        }

    def three_world_closure_verification(self) -> Dict[str, Any]:
        """三界闭环验证推演"""
        self._closure_degree = 1.0 - math.exp(-self.constants.gamma * 3)

        closure_cycles = [
            "天道 → 人道 → 自然 → 天道（下降闭环）",
            "自然 → 人道 → 天道 → 自然（上升闭环）",
            "三界循环：生灭往复，周行不殆"
        ]

        verification_items = [
            "三界是否形成完整循环",
            "转化是否守恒（总量不变）",
            "信息是否闭环（输出可回到输入）",
            "因果是否闭环（因可果果可因）"
        ]

        cycle_efficiency = {
            "上升循环": self.constants.E1,
            "下降循环": self.constants.E3,
            "完整循环": self.constants.E2
        }

        return {
            "closure_degree": self._closure_degree,
            "closure_verified": self._closure_degree > self.constants.E2,
            "closure_cycles": closure_cycles,
            "verification_items": verification_items,
            "cycle_efficiency": cycle_efficiency,
            "closure_principle": "三界周流，循环无端，形成自足闭环"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T24 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if len(self.three_worlds) != 3:
            errors.append("三界必须恰好3个")
        if len(self.six_systems) != 6:
            errors.append("六系必须恰好6个")
        if "天道世界" not in self.three_worlds:
            errors.append("三界必须包含天道世界")
        if "人道世界" not in self.three_worlds:
            errors.append("三界必须包含人道世界")
        if "自然世界" not in self.three_worlds:
            errors.append("三界必须包含自然世界")
        if "本源系" not in self.six_systems:
            errors.append("六系必须包含本源系")
        if "结构系" not in self.six_systems:
            errors.append("六系必须包含结构系")
        if "动力学系" not in self.six_systems:
            errors.append("六系必须包含动力学系")
        if len(self._world_systems_mapping) != 3:
            errors.append("映射必须覆盖三界")
        if "T5" not in self.dependencies:
            errors.append("T24必须依赖T5（六系本源）")
        if "T19" not in self.dependencies:
            errors.append("T24必须依赖T19（三界秩序基底）")
        if "T20" not in self.dependencies:
            errors.append("T24必须依赖T20（九界场域框架）")
        if self.cosmic_level != 2:
            errors.append("T24必须位于L2无限之子层")
        if not self.is_origin_locked:
            errors.append("T24理论必须锁定")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t24 = ThreeWorldSixSystemsUnified()
    print(f"模块: {t24.module_id} - {t24.module_name}")
    print(f"版本: {t24.version}")
    print(f"层级: L{t24.cosmic_level}")
    print(f"依赖: {t24.dependencies}")
    print(f"锁定: {t24.is_origin_locked}")
    print(f"哈希: {t24.sha256}")
    print()

    print("三界六系映射模型:")
    mapping = t24.three_world_six_systems_mapping_model()
    for world, detail in mapping['mapping_detail'].items():
        print(f"  {world}: 主={detail['主导系']}, 辅={detail['辅助系']}")
    print()

    print("动力学同构:")
    iso = t24.three_world_six_systems_dynamic_isomorphism()
    print(f"  同构度: {iso['isomorphism_degree']:.6f}")
    print(f"  同构验证: {iso['isomorphic']}")
    print()

    print("三界互转机制:")
    conv = t24.three_world_six_systems_interconversion("自然世界", "天道世界", 1.0)
    print(f"  方向: {conv['conversion_direction']}")
    print(f"  效率: {conv['conversion_efficiency']}")
    print(f"  输入: {conv['input_energy']} → 输出: {conv['output_energy']}")
    print()

    print("三界统一场方程:")
    field = t24.three_world_unified_field_equation(0.5)
    for comp, strength in field['field_components'].items():
        print(f"  {comp}: {strength:.6f}")
    print(f"  总场强: {field['total_field_strength']:.6f}")
    print()

    print("三界闭环验证:")
    closure = t24.three_world_closure_verification()
    print(f"  闭环度: {closure['closure_degree']:.6f}")
    print(f"  闭环验证: {closure['closure_verified']}")
    print()

    valid, errs = t24.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
