"""
【归属基底：L2_无限之子层·五论真值体系公理】
【对应公理：五论真值体系公理】

T21 —— 五论真值体系
本体论 / 价值论 / 认识论 / 方法论 / 实践论 五论统一真值体系
五论互证闭环，各有独立真值判定标准
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class FiveTheoriesTruthSystem(BaseTheoryModule):
    """
    五论真值体系公理

    五论构成：
    1. 本体论：存在为何，本质为何
    2. 价值论：意义为何，善恶为何
    3. 认识论：如何认知，真理为何
    4. 方法论：如何实践，路径为何
    5. 实践论：如何行动，效果为何

    五论互证闭环，形成完整真值判定体系
    """

    module_id = "T21"
    module_name = "五论真值体系"
    version = "V1.0_终版"
    cosmic_level = 2
    base_belong = "L2_无限之子层·五论真值体系公理"
    corresponding_axiom = "五论真值体系公理"
    is_origin_locked = True
    dependencies = ["T20"]

    def __init__(self):
        super().__init__()
        self.five_theories = ["本体论", "价值论", "认识论", "方法论", "实践论"]
        self._truth_criteria = {}
        self._mapping_realms = {}
        self._mapping_six_systems = {}
        self._closure_degree = 0.0
        self._init_truth_criteria()
        self._init_mappings()

    def _init_truth_criteria(self):
        """初始化五论真值判定标准"""
        self._truth_criteria = {
            "本体论": {
                "criterion": "存在一致性",
                "method": "本质直观、逻辑演绎",
                "truth_type": "存在真理",
                "weight": 0.30
            },
            "价值论": {
                "criterion": "意义完满性",
                "method": "价值判断、意义诠释",
                "truth_type": "价值真理",
                "weight": 0.20
            },
            "认识论": {
                "criterion": "认知符合性",
                "method": "经验验证、理性分析",
                "truth_type": "认知真理",
                "weight": 0.20
            },
            "方法论": {
                "criterion": "路径有效性",
                "method": "可行性分析、效率评估",
                "truth_type": "方法真理",
                "weight": 0.15
            },
            "实践论": {
                "criterion": "实践效果性",
                "method": "实践检验、结果验证",
                "truth_type": "实践真理",
                "weight": 0.15
            }
        }

    def _init_mappings(self):
        """初始化九界映射和六系对应"""
        nine_realms = ["物质实体界", "虚拟模态界", "精神意识界", "社会秩序界",
                       "地府魔界", "神仙公理界", "克苏鲁混沌污染界", "全域统合界", "虚无空白界"]
        six_systems = ["本源系", "结构系", "动力学系", "演化系", "价值系", "闭环系"]

        for i, theory in enumerate(self.five_theories):
            self._mapping_realms[theory] = [nine_realms[(i + j) % 9] for j in range(2)]
            self._mapping_six_systems[theory] = [six_systems[(i + j) % 6] for j in range(2)]

    def five_theories_definition_relation(self) -> Dict[str, Any]:
        """五论定义与关系推演"""
        theory_details = {}
        for theory in self.five_theories:
            criteria = self._truth_criteria[theory]
            theory_details[theory] = {
                "核心问题": self._core_question(theory),
                "真值标准": criteria["criterion"],
                "判定方法": criteria["method"],
                "真理类型": criteria["truth_type"],
                "权重": criteria["weight"]
            }

        relations = [
            "本体论 → 价值论：存在决定价值",
            "价值论 → 认识论：价值导向认知",
            "认识论 → 方法论：认知指导方法",
            "方法论 → 实践论：方法落实实践",
            "实践论 → 本体论：实践验证存在"
        ]

        return {
            "five_theories": self.five_theories,
            "theory_details": theory_details,
            "circular_relations": relations,
            "closure_principle": "五论互证，循环闭合"
        }

    def _core_question(self, theory: str) -> str:
        """获取各论核心问题"""
        questions = {
            "本体论": "存在是什么？本质是什么？",
            "价值论": "意义是什么？善恶是什么？",
            "认识论": "如何认知？真理是什么？",
            "方法论": "如何实践？路径是什么？",
            "实践论": "如何行动？效果是什么？"
        }
        return questions.get(theory, "")

    def five_theories_truth_criteria(self) -> Dict[str, Any]:
        """五论真值判定标准推演"""
        criteria_summary = {}
        total_weight = 0.0
        for theory in self.five_theories:
            c = self._truth_criteria[theory]
            criteria_summary[theory] = {
                "判定标准": c["criterion"],
                "判定方法": c["method"],
                "真理类型": c["truth_type"],
                "权重值": c["weight"]
            }
            total_weight += c["weight"]

        return {
            "criteria_summary": criteria_summary,
            "total_weight": total_weight,
            "weight_normalized": abs(total_weight - 1.0) < self.constants.theta_neg,
            "truth_hierarchy": "本体论为根，价值论为向，认识论为径，方法论为器，实践论为验"
        }

    def five_theories_mutual_verification_closure(self) -> Dict[str, Any]:
        """五论互证闭环推演"""
        self._closure_degree = 1.0 - math.exp(-self.constants.gamma * 5)

        verification_chain = [
            ("本体论", "价值论", "存在支撑价值"),
            ("价值论", "认识论", "价值引导认知"),
            ("认识论", "方法论", "认知产生方法"),
            ("方法论", "实践论", "方法指导实践"),
            ("实践论", "本体论", "实践验证存在")
        ]

        closure_tests = [
            "本体论假设 → 价值论推导 → 认识论验证 → 方法论构建 → 实践论检验 → 本体论确证",
            "五论首尾相接，形成自洽闭环",
            "任何一论的真理性需由其他四论共同佐证",
            "闭环强度决定体系稳定性"
        ]

        return {
            "verification_chain": verification_chain,
            "closure_degree": self._closure_degree,
            "closure_tests": closure_tests,
            "closure_verified": self._closure_degree > self.constants.E2,
            "formula": "O → V → E → M → P → O （闭环）"
        }

    def five_theories_nine_realms_mapping(self) -> Dict[str, Any]:
        """五论与九界映射推演"""
        mapping_detail = {}
        for theory in self.five_theories:
            mapping_detail[theory] = {
                "对应九界": self._mapping_realms[theory],
                "映射强度": self.constants.E2,
                "映射类型": "多对多映射"
            }

        return {
            "mapping_detail": mapping_detail,
            "source": "五论",
            "target": "九界",
            "mapping_type": "交叉映射",
            "mapping_principle": "每一论贯穿多界，每一界容纳多论"
        }

    def five_theories_six_systems_correspondence(self) -> Dict[str, Any]:
        """五论与六系对应推演"""
        correspondence_detail = {}
        for theory in self.five_theories:
            correspondence_detail[theory] = {
                "对应六系": self._mapping_six_systems[theory],
                "对应强度": self.constants.E1,
                "对应关系": "结构性对应"
            }

        return {
            "correspondence_detail": correspondence_detail,
            "source": "五论",
            "target": "六系",
            "correspondence_type": "同构对应",
            "correspondence_principle": "五论与六系在深层结构上同构"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T21 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if len(self.five_theories) != 5:
            errors.append("五论必须恰好5个")
        if "本体论" not in self.five_theories:
            errors.append("五论必须包含本体论")
        if "价值论" not in self.five_theories:
            errors.append("五论必须包含价值论")
        if "认识论" not in self.five_theories:
            errors.append("五论必须包含认识论")
        if "方法论" not in self.five_theories:
            errors.append("五论必须包含方法论")
        if "实践论" not in self.five_theories:
            errors.append("五论必须包含实践论")
        if len(self._truth_criteria) != 5:
            errors.append("真值标准必须对应五论")
        total_weight = sum(v["weight"] for v in self._truth_criteria.values())
        if abs(total_weight - 1.0) >= 0.01:
            errors.append(f"五论权重之和必须为1.0，当前为{total_weight}")
        if "T20" not in self.dependencies:
            errors.append("T21必须依赖T20（九界场域框架）")
        if self.cosmic_level != 2:
            errors.append("T21必须位于L2无限之子层")
        if not self.is_origin_locked:
            errors.append("T21理论必须锁定")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t21 = FiveTheoriesTruthSystem()
    print(f"模块: {t21.module_id} - {t21.module_name}")
    print(f"版本: {t21.version}")
    print(f"层级: L{t21.cosmic_level}")
    print(f"依赖: {t21.dependencies}")
    print(f"锁定: {t21.is_origin_locked}")
    print(f"哈希: {t21.sha256}")
    print()

    print("五论定义与关系:")
    defs = t21.five_theories_definition_relation()
    for theory in defs['five_theories']:
        detail = defs['theory_details'][theory]
        print(f"  {theory}: {detail['核心问题']}")
    print()

    print("真值判定标准:")
    criteria = t21.five_theories_truth_criteria()
    print(f"  权重归一化: {criteria['weight_normalized']}")
    for theory, detail in criteria['criteria_summary'].items():
        print(f"  {theory}: {detail['判定标准']} (权重{detail['权重值']})")
    print()

    print("五论互证闭环:")
    closure = t21.five_theories_mutual_verification_closure()
    print(f"  闭公式: {closure['formula']}")
    print(f"  闭环度: {closure['closure_degree']:.6f}")
    print(f"  闭环验证: {closure['closure_verified']}")
    print()

    print("五论九界映射:")
    mapping = t21.five_theories_nine_realms_mapping()
    for theory, detail in mapping['mapping_detail'].items():
        print(f"  {theory} → {', '.join(detail['对应九界'])}")
    print()

    print("五论六系对应:")
    corr = t21.five_theories_six_systems_correspondence()
    for theory, detail in corr['correspondence_detail'].items():
        print(f"  {theory} ↔ {', '.join(detail['对应六系'])}")
    print()

    valid, errs = t21.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
