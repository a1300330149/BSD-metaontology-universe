"""
【归属基底：L0_总本源层·四元本体结构公理】
【对应公理：四元本体结构公理】

T4 —— 四元本体结构
自在、自性、共在、生成 四元本体完备结构
三元存在 + 生成维度 = 四元完备本体
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class FourElementOntologyStructure(BaseTheoryModule):
    """
    四元本体结构
    
    核心要义：
    - 四元：自在、自性、共在、生成
    - 三元存在为体，生成为用
    - 四元关系矩阵，相生相克
    - 四元闭环，自洽圆满
    """

    module_id = "T4"
    module_name = "四元本体结构"
    version = "V1.0_终版"
    cosmic_level = 0
    base_belong = "L0_总本源层·四元本体结构公理"
    corresponding_axiom = "四元本体结构公理"
    is_origin_locked = True
    dependencies = ["T3"]

    def __init__(self):
        super().__init__()
        self.four_elements = {
            "zi_zai": "自在",
            "zi_xing": "自性",
            "gong_zai": "共在",
            "sheng_cheng": "生成"
        }
        self._relation_matrix = {}
        self._closure_degree = 0.0
        self._init_relation_matrix()

    def _init_relation_matrix(self):
        """初始化四元关系矩阵"""
        elements = list(self.four_elements.keys())
        for i, e1 in enumerate(elements):
            self._relation_matrix[e1] = {}
            for j, e2 in enumerate(elements):
                if i == j:
                    self._relation_matrix[e1][e2] = "自同"
                elif (i + 1) % 4 == j:
                    self._relation_matrix[e1][e2] = "相生"
                elif (i - 1) % 4 == j:
                    self._relation_matrix[e1][e2] = "相克"
                else:
                    self._relation_matrix[e1][e2] = "互摄"

    def four_element_definition(self) -> Dict[str, Dict[str, Any]]:
        """四元结构定义推演"""
        return {
            "zi_zai": {
                "name": "自在",
                "role": "存在之体",
                "nature": "静",
                "position": "体"
            },
            "zi_xing": {
                "name": "自性",
                "role": "存在之性",
                "nature": "理",
                "position": "性"
            },
            "gong_zai": {
                "name": "共在",
                "role": "存在之缘",
                "nature": "动",
                "position": "相"
            },
            "sheng_cheng": {
                "name": "生成",
                "role": "存在之用",
                "nature": "化",
                "position": "用"
            }
        }

    def four_element_relation_matrix(self) -> Dict[str, Dict[str, str]]:
        """四元关系矩阵推演"""
        return self._relation_matrix

    def four_element_generation_restraint(self) -> Dict[str, Any]:
        """四元相生相克推演"""
        generation_chain = ["zi_zai", "zi_xing", "gong_zai", "sheng_cheng", "zi_zai"]
        restraint_chain = ["zi_zai", "gong_zai", "zi_xing", "sheng_cheng", "zi_zai"]
        return {
            "generation_chain": [self.four_elements[e] for e in generation_chain],
            "restraint_chain": [self.four_elements[e] for e in restraint_chain],
            "generation_rule": "自在生自性，自性生共在，共生生成，生成生自在",
            "restraint_rule": "自在克共在，共在克自性，自性克生成，生成克自在",
            "balance_mechanism": "相生相克，动态平衡"
        }

    def four_element_closure(self) -> Dict[str, Any]:
        """四元闭环推演"""
        self._closure_degree = 1.0 - math.exp(-self.constants.gamma * 9)
        return {
            "closure_degree": self._closure_degree,
            "self_consistent": True,
            "mutually_supporting": True,
            "circular_complete": True,
            "closure_verified": self._closure_degree > self.constants.E2
        }

    def get_element_role(self, element_key: str) -> Optional[str]:
        """获取四元角色"""
        elems = self.four_element_definition()
        if element_key in elems:
            return elems[element_key]["role"]
        return None

    def validate(self) -> Tuple[bool, List[str]]:
        """T4 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(self.four_elements) != 4:
            errors.append("四元本体必须恰好4个元素")
        if "zi_zai" not in self.four_elements:
            errors.append("必须包含自在")
        if "zi_xing" not in self.four_elements:
            errors.append("必须包含自性")
        if "gong_zai" not in self.four_elements:
            errors.append("必须包含共在")
        if "sheng_cheng" not in self.four_elements:
            errors.append("必须包含生成")
        if "T3" not in self.dependencies:
            errors.append("T4必须依赖T3")
        if self.cosmic_level != 0:
            errors.append("T4必须位于L0本源层")
        if not self.is_origin_locked:
            errors.append("T4本源理论必须锁定")
        if not hasattr(self, 'four_element_relation_matrix'):
            errors.append("必须实现四元关系矩阵方法")
        if not hasattr(self, 'four_element_generation_restraint'):
            errors.append("必须实现四元相生相克方法")
        if not hasattr(self, 'four_element_closure'):
            errors.append("必须实现四元闭环方法")
        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t4 = FourElementOntologyStructure()
    print(f"模块: {t4.module_id} - {t4.module_name}")
    print(f"版本: {t4.version}")
    print(f"层级: L{t4.cosmic_level}")
    print(f"依赖: {t4.dependencies}")
    print(f"锁定: {t4.is_origin_locked}")
    print(f"哈希: {t4.sha256}")
    print()
    
    print("四元定义:")
    defs = t4.four_element_definition()
    for key, val in defs.items():
        print(f"  {val['name']}: {val['role']}")
    print()
    
    print("四元相生相克:")
    gr = t4.four_element_generation_restraint()
    print(f"  相生链: {'→'.join(gr['generation_chain'])}")
    print(f"  相克链: {'→'.join(gr['restraint_chain'])}")
    print()
    
    print("四元闭环:")
    closure = t4.four_element_closure()
    print(f"  闭环度: {closure['closure_degree']:.6f}")
    print(f"  闭环验证: {closure['closure_verified']}")
    print()
    
    valid, errs = t4.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
