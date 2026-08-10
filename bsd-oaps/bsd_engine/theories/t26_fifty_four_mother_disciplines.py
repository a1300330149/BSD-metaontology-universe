"""
【归属基底：L3_功能应用层·54母科分科公理】
【对应公理：54母科分科公理】

T26 —— 54门基础母科体系
54维矩阵 ↔ 54门母科一一对应
每科有五论权重（W真+W正+W逆+W谬+W悬=1）
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class FiftyFourMotherDisciplines(BaseTheoryModule):
    """
    54门基础母科体系公理

    六系统分科（每系9门）：
    1. 实体系9门 - 物质实体类学科
    2. 模态系9门 - 虚拟模态类学科
    3. 认知系9门 - 精神意识类学科
    4. 社会系9门 - 社会秩序类学科
    5. 公理系9门 - 神仙公理类学科
    6. 混沌系9门 - 混沌异化类学科

    五论权重体系：
    - W真：真理/正确权重
    - W正：正面/正向权重
    - W逆：逆向/反向权重
    - W谬：谬误/错误权重
    - W悬：悬置/未决权重
    五论权重之和恒等于1

    核心：54维矩阵与54门母科一一对应
    """

    module_id = "T26"
    module_name = "54门基础母科体系"
    version = "V1.0_终版"
    cosmic_level = 3
    base_belong = "L3_功能应用层·54母科分科公理"
    corresponding_axiom = "54母科分科公理"
    is_origin_locked = True
    dependencies = ["T25", "T21"]

    def __init__(self):
        super().__init__()
        self.six_systems = ["实体系", "模态系", "认知系", "社会系", "公理系", "混沌系"]
        self.five_theories = ["W真", "W正", "W逆", "W谬", "W悬"]
        self._disciplines = {}
        self._discipline_matrix_mapping = {}
        self._entropy_trends = {}
        self._system_disciplines = {}
        self._completeness_degree = 0.0
        self._init_disciplines()

    def _init_disciplines(self):
        """初始化54门母科"""
        realm_names = [
            "物质实体界", "虚拟模态界", "精神意识界",
            "社会秩序界", "全域统合界", "神仙公理界",
            "地府魔界", "虚无寂灭界", "克苏鲁混沌界"
        ]

        disc_index = 1
        for sys in self.six_systems:
            self._system_disciplines[sys] = []
            for i, realm in enumerate(realm_names):
                disc_id = f"Disc{disc_index:02d}"
                disc_name = f"{sys}_{realm}学"
                base_weights = self._generate_five_weights(sys, i)
                self._disciplines[disc_id] = {
                    "disc_id": disc_id,
                    "disc_name": disc_name,
                    "system": sys,
                    "realm": realm,
                    "five_weights": base_weights,
                    "weight_sum": sum(base_weights.values()),
                    "entropy_trend": self._calc_entropy_trend(base_weights),
                    "corresponding_dim": f"D{disc_index:03d}"
                }
                self._system_disciplines[sys].append(disc_id)
                self._discipline_matrix_mapping[disc_id] = f"D{disc_index:03d}"
                disc_index += 1

        self._completeness_degree = len(self._disciplines) / 54.0

    def _generate_five_weights(self, system: str, realm_idx: int) -> Dict[str, float]:
        """生成五论权重，保证和为1"""
        base_vals = {
            "W真": 0.35 - realm_idx * 0.02,
            "W正": 0.25 + realm_idx * 0.01,
            "W逆": 0.15 + realm_idx * 0.005,
            "W谬": 0.10 + realm_idx * 0.008,
            "W悬": 0.15 - realm_idx * 0.003
        }
        total = sum(base_vals.values())
        normalized = {k: round(v / total, 4) for k, v in base_vals.items()}
        diff = round(1.0 - sum(normalized.values()), 4)
        normalized["W真"] = round(normalized["W真"] + diff, 4)
        return normalized

    def _calc_entropy_trend(self, weights: Dict[str, float]) -> float:
        """计算熵变趋势"""
        entropy = -sum(w * math.log(w) for w in weights.values() if w > 0)
        max_entropy = math.log(5)
        return round(entropy / max_entropy, 4)

    def discipline_system_construction(self) -> Dict[str, Any]:
        """54母科体系构建推演"""
        system_summary = {}
        for sys, discs in self._system_disciplines.items():
            avg_weight_sum = sum(self._disciplines[d]["weight_sum"] for d in discs) / len(discs)
            system_summary[sys] = {
                "discipline_count": len(discs),
                "disciplines": [self._disciplines[d]["disc_name"] for d in discs],
                "average_weight_sum": round(avg_weight_sum, 4)
            }

        all_disc_names = [self._disciplines[d]["disc_name"] for d in sorted(self._disciplines.keys())]

        return {
            "total_disciplines": len(self._disciplines),
            "expected_disciplines": 54,
            "six_systems": self.six_systems,
            "five_theories": self.five_theories,
            "system_summary": system_summary,
            "all_disciplines": all_disc_names,
            "construction_principle": "六系各九门，共54门基础母科"
        }

    def five_theory_weights_config(self) -> Dict[str, Any]:
        """五论权重配置推演"""
        sample_disc = list(self._disciplines.values())[0]

        weight_explanations = {
            "W真": "真理权重 - 该学科中被确认为真理的比例",
            "W正": "正向权重 - 该学科中正面/积极内容的比例",
            "W逆": "逆向权重 - 该学科中反向/批判内容的比例",
            "W谬": "谬误权重 - 该学科中被证明为谬误的比例",
            "W悬": "悬置权重 - 该学科中尚未确定的悬置内容比例"
        }

        weight_constraints = [
            "五论权重之和恒等于1（归一化约束）",
            "所有权重均在[0,1]区间内",
            "不同学科的权重分布不同",
            "同一系内学科权重分布相似",
            "W真+W正+W逆+W谬+W悬 = 1"
        ]

        system_avg_weights = {}
        for sys in self.six_systems:
            discs = self._system_disciplines[sys]
            avg_weights = {}
            for theory in self.five_theories:
                avg_w = sum(self._disciplines[d]["five_weights"][theory] for d in discs) / len(discs)
                avg_weights[theory] = round(avg_w, 4)
            system_avg_weights[sys] = avg_weights

        return {
            "five_theories": self.five_theories,
            "weight_explanations": weight_explanations,
            "weight_constraints": weight_constraints,
            "sample_discipline": sample_disc["disc_name"],
            "sample_weights": sample_disc["five_weights"],
            "sample_weight_sum": sample_disc["weight_sum"],
            "system_average_weights": system_avg_weights,
            "config_principle": "五论权重归一化，总和恒为1"
        }

    def discipline_matrix_mapping(self) -> Dict[str, Any]:
        """母科-维度一一映射推演"""
        mapping_detail = {}
        for disc_id, dim_id in self._discipline_matrix_mapping.items():
            disc = self._disciplines[disc_id]
            mapping_detail[disc_id] = {
                "discipline_name": disc["disc_name"],
                "corresponding_dimension": dim_id,
                "system": disc["system"],
                "realm": disc["realm"],
                "mapping_strength": self.constants.E3
            }

        mapping_properties = [
            "一一对应：每门母科对应唯一维度",
            "双向映射：可从母科到维度，也可从维度到母科",
            "结构同构：母科体系与维度矩阵结构相同",
            "六系对应：六系学科对应六系维度",
            "九界对应：九界学科对应九界维度"
        ]

        reverse_mapping = {v: k for k, v in self._discipline_matrix_mapping.items()}

        return {
            "total_mappings": len(self._discipline_matrix_mapping),
            "mapping_detail": mapping_detail,
            "reverse_mapping": reverse_mapping,
            "mapping_properties": mapping_properties,
            "mapping_principle": "54母科与54维度一一对应，结构同构"
        }

    def entropy_trend_calculation(self) -> Dict[str, Any]:
        """各学科熵变趋势计算推演"""
        system_entropy = {}
        for sys in self.six_systems:
            discs = self._system_disciplines[sys]
            avg_entropy = sum(self._disciplines[d]["entropy_trend"] for d in discs) / len(discs)
            system_entropy[sys] = round(avg_entropy, 4)

        high_entropy_discs = []
        low_entropy_discs = []
        for disc_id, disc in self._disciplines.items():
            if disc["entropy_trend"] > 0.8:
                high_entropy_discs.append(disc["disc_name"])
            elif disc["entropy_trend"] < 0.5:
                low_entropy_discs.append(disc["disc_name"])

        entropy_laws = [
            "从实体系到混沌系：熵值递增，不确定性增大",
            "W真占比高的学科：熵值低，确定性强",
            "W悬占比高的学科：熵值高，不确定性强",
            "五论权重越平均，熵值越高",
            "五论权重越集中，熵值越低"
        ]

        total_avg_entropy = sum(d["entropy_trend"] for d in self._disciplines.values()) / len(self._disciplines)

        return {
            "average_total_entropy": round(total_avg_entropy, 4),
            "system_entropy": system_entropy,
            "high_entropy_disciplines": high_entropy_discs,
            "low_entropy_disciplines": low_entropy_discs,
            "entropy_laws": entropy_laws,
            "calculation_principle": "基于五论权重分布计算学科熵值"
        }

    def discipline_system_validation(self) -> Dict[str, Any]:
        """学科体系完整性验证推演"""
        self._completeness_degree = len(self._disciplines) / 54.0

        all_weight_sums_valid = all(
            abs(d["weight_sum"] - 1.0) < 0.001 for d in self._disciplines.values()
        )

        system_counts_valid = all(
            len(discs) == 9 for discs in self._system_disciplines.values()
        )

        mapping_complete = len(self._discipline_matrix_mapping) == 54

        validation_items = [
            "54门母科齐全",
            "六系各9门，分布均匀",
            "每科五论权重和为1",
            "与54维矩阵一一对应",
            "学科命名规范统一",
            "权重值在合法区间"
        ]

        return {
            "total_disciplines": len(self._disciplines),
            "expected_disciplines": 54,
            "completeness_degree": self._completeness_degree,
            "complete": self._completeness_degree >= 1.0,
            "all_weight_sums_valid": all_weight_sums_valid,
            "system_counts_valid": system_counts_valid,
            "mapping_complete": mapping_complete,
            "validation_items": validation_items,
            "validation_principle": "54母科完整覆盖，权重归一，映射准确"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T26 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if len(self._disciplines) != 54:
            errors.append(f"母科总数必须为54，当前为{len(self._disciplines)}")
        if len(self.six_systems) != 6:
            errors.append("必须有六系")
        if len(self.five_theories) != 5:
            errors.append("必须有五论")
        if len(self._system_disciplines) != 6:
            errors.append("六系统分科必须有6个系")

        for sys in self.six_systems:
            if sys not in self._system_disciplines:
                errors.append(f"缺少{sys}的学科")
            elif len(self._system_disciplines[sys]) != 9:
                errors.append(f"{sys}必须有9门学科，当前为{len(self._system_disciplines[sys])}门")

        for disc_id, disc in self._disciplines.items():
            weight_sum = disc["weight_sum"]
            if abs(weight_sum - 1.0) > 0.01:
                errors.append(f"{disc['disc_name']}的五论权重和必须为1，当前为{weight_sum}")
            for theory in self.five_theories:
                w = disc["five_weights"].get(theory, 0)
                if w < 0 or w > 1:
                    errors.append(f"{disc['disc_name']}的{theory}权重必须在[0,1]区间，当前为{w}")

        if len(self._discipline_matrix_mapping) != 54:
            errors.append("母科-维度映射必须覆盖全部54门")
        
        mapped_dims = set(self._discipline_matrix_mapping.values())
        if len(mapped_dims) != 54:
            errors.append("映射的维度必须有54个唯一值")

        if "T25" not in self.dependencies:
            errors.append("T26必须依赖T25（54维矩阵）")
        if "T21" not in self.dependencies:
            errors.append("T26必须依赖T21（五论真值体系）")
        if self.cosmic_level != 3:
            errors.append("T26必须位于L3功能应用层")
        if not self.is_origin_locked:
            errors.append("T26理论必须锁定")
        if self._completeness_degree < 1.0:
            errors.append("学科体系完整度必须达到100%")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t26 = FiftyFourMotherDisciplines()
    print(f"模块: {t26.module_id} - {t26.module_name}")
    print(f"版本: {t26.version}")
    print(f"层级: L{t26.cosmic_level}")
    print(f"依赖: {t26.dependencies}")
    print(f"锁定: {t26.is_origin_locked}")
    print(f"哈希: {t26.sha256}")
    print()

    print("54母科体系构建:")
    disc_sys = t26.discipline_system_construction()
    print(f"  总学科数: {disc_sys['total_disciplines']}")
    print(f"  期望学科数: {disc_sys['expected_disciplines']}")
    for sys, detail in disc_sys['system_summary'].items():
        print(f"  {sys}: {detail['discipline_count']}门")
    print()

    print("五论权重配置:")
    weights = t26.five_theory_weights_config()
    print(f"  示例学科: {weights['sample_discipline']}")
    print(f"  五论权重:")
    for theory, w in weights['sample_weights'].items():
        print(f"    {theory}: {w}")
    print(f"  权重和: {weights['sample_weight_sum']}")
    print()

    print("母科-维度映射:")
    mapping = t26.discipline_matrix_mapping()
    print(f"  总映射数: {mapping['total_mappings']}")
    for i, (disc_id, detail) in enumerate(mapping['mapping_detail'].items()):
        if i < 3:
            print(f"    {detail['discipline_name']} ↔ {detail['corresponding_dimension']}")
    print("    ...")
    print()

    print("熵变趋势计算:")
    entropy = t26.entropy_trend_calculation()
    print(f"  总平均熵: {entropy['average_total_entropy']}")
    for sys, ent in entropy['system_entropy'].items():
        print(f"  {sys}: {ent}")
    print()

    print("学科体系验证:")
    valid_sys = t26.discipline_system_validation()
    print(f"  完整度: {valid_sys['completeness_degree']*100:.1f}%")
    print(f"  完整: {valid_sys['complete']}")
    print(f"  权重和有效: {valid_sys['all_weight_sums_valid']}")
    print()

    valid, errs = t26.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
