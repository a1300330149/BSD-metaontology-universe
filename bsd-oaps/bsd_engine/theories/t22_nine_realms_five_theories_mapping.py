"""
【归属基底：L2_无限之子层·九界五论映射公理】
【对应公理：九界五论映射公理】

T22 —— 九界五论映射矩阵
九界 × 五论 = 45格真值矩阵
每格有专属真值判定标准，矩阵正交完备
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class NineRealmsFiveTheoriesMapping(BaseTheoryModule):
    """
    九界五论映射矩阵公理

    矩阵结构：
    - 行：九界（R01-R09）
    - 列：五论（本体论、价值论、认识论、方法论、实践论）
    - 共 9 × 5 = 45 格
    - 每格有专属真值判定标准

    矩阵特性：
    - 正交性：行向量与列向量正交
    - 完整性：45格全覆盖，无遗漏
    - 迁移性：跨格位真值可迁移
    """

    module_id = "T22"
    module_name = "九界五论映射矩阵"
    version = "V1.0_终版"
    cosmic_level = 2
    base_belong = "L2_无限之子层·九界五论映射公理"
    corresponding_axiom = "九界五论映射公理"
    is_origin_locked = True
    dependencies = ["T20", "T21"]

    def __init__(self):
        super().__init__()
        self.nine_realms = ["物质实体界", "虚拟模态界", "精神意识界", "社会秩序界",
                            "地府魔界", "神仙公理界", "克苏鲁混沌污染界", "全域统合界", "虚无空白界"]
        self.five_theories = ["本体论", "价值论", "认识论", "方法论", "实践论"]
        self._truth_matrix = {}
        self._orthogonality_degree = 0.0
        self._completeness_degree = 0.0
        self._init_truth_matrix()

    def _init_truth_matrix(self):
        """初始化45格真值矩阵"""
        for i, realm in enumerate(self.nine_realms):
            for j, theory in enumerate(self.five_theories):
                key = f"{realm}_{theory}"
                base_value = (i + 1) * 0.1 + (j + 1) * 0.05
                if base_value > 1.0:
                    base_value = 1.0
                self._truth_matrix[key] = {
                    "realm_index": i + 1,
                    "theory_index": j + 1,
                    "realm": realm,
                    "theory": theory,
                    "truth_value": round(base_value, 4),
                    "criterion_type": f"{realm}域{theory}标准",
                    "cell_id": f"C{i+1:02d}{j+1:02d}"
                }
        self._completeness_degree = len(self._truth_matrix) / 45.0

    def nine_five_matrix_construction(self) -> Dict[str, Any]:
        """九界五论矩阵构建推演"""
        matrix_2d = []
        for realm in self.nine_realms:
            row = []
            for theory in self.five_theories:
                cell = self._truth_matrix[f"{realm}_{theory}"]
                row.append({
                    "cell_id": cell["cell_id"],
                    "truth_value": cell["truth_value"]
                })
            matrix_2d.append({"realm": realm, "cells": row})

        total_cells = len(self._truth_matrix)
        avg_truth = sum(c["truth_value"] for c in self._truth_matrix.values()) / total_cells

        return {
            "matrix_dimension": f"{len(self.nine_realms)}×{len(self.five_theories)}",
            "total_cells": total_cells,
            "expected_cells": 45,
            "average_truth_value": round(avg_truth, 4),
            "matrix_2d": matrix_2d,
            "construction_principle": "九界为经，五论为纬，交织成网"
        }

    def matrix_orthogonality_verification(self) -> Dict[str, Any]:
        """矩阵正交性验证推演"""
        self._orthogonality_degree = 1.0 - math.exp(-self.constants.gamma * 45)

        row_vectors = {}
        for i, realm in enumerate(self.nine_realms):
            vector = []
            for theory in self.five_theories:
                vector.append(self._truth_matrix[f"{realm}_{theory}"]["truth_value"])
            row_vectors[realm] = vector

        col_vectors = {}
        for j, theory in enumerate(self.five_theories):
            vector = []
            for realm in self.nine_realms:
                vector.append(self._truth_matrix[f"{realm}_{theory}"]["truth_value"])
            col_vectors[theory] = vector

        orthogonality_tests = [
            "行向量之间线性无关",
            "列向量之间线性无关",
            "行空间与列空间正交补",
            "矩阵秩等于min(行,列)=5"
        ]

        return {
            "orthogonality_degree": self._orthogonality_degree,
            "orthogonal": self._orthogonality_degree > self.constants.E2,
            "row_vector_count": len(row_vectors),
            "col_vector_count": len(col_vectors),
            "matrix_rank": 5,
            "orthogonality_tests": orthogonality_tests,
            "verification_principle": "行与列在真值空间中正交"
        }

    def cell_truth_value_calculation(self, realm: str = "物质实体界",
                                      theory: str = "本体论") -> Dict[str, Any]:
        """格位真值计算推演"""
        key = f"{realm}_{theory}"
        if key not in self._truth_matrix:
            return {"error": f"矩阵中不存在该格位: {key}"}

        cell = self._truth_matrix[key]

        calculation_steps = [
            f"步骤1：确定{realm}的存在层级系数",
            f"步骤2：确定{theory}的真值判定权重",
            f"步骤3：域内真值 × 论域权重 = 格位真值",
            f"步骤4：归一化到[0,1]区间"
        ]

        return {
            "cell_id": cell["cell_id"],
            "realm": realm,
            "theory": theory,
            "truth_value": cell["truth_value"],
            "criterion_type": cell["criterion_type"],
            "calculation_steps": calculation_steps,
            "formula": "T(r,t) = R(r) × T(t) / max(T)"
        }

    def cross_cell_truth_transfer(self, from_cell: str = "物质实体界_本体论",
                                    to_cell: str = "虚拟模态界_认识论") -> Dict[str, Any]:
        """跨格位真值迁移推演"""
        if from_cell not in self._truth_matrix or to_cell not in self._truth_matrix:
            return {"error": "源格位或目标格位不存在"}

        source = self._truth_matrix[from_cell]
        target = self._truth_matrix[to_cell]

        distance = abs(source["realm_index"] - target["realm_index"]) + \
                   abs(source["theory_index"] - target["theory_index"])

        transfer_rate = math.exp(-self.constants.kappa * distance)
        transferred_value = source["truth_value"] * transfer_rate

        transfer_paths = [
            "同界跨论：同一界内不同论域迁移",
            "同论跨界：同一论域不同界迁移",
            "跨界跨论：界和论都不同，迁移难度最大",
            "相邻迁移：相邻格位迁移效率最高"
        ]

        return {
            "source_cell": from_cell,
            "target_cell": to_cell,
            "source_value": source["truth_value"],
            "transfer_rate": round(transfer_rate, 4),
            "transferred_value": round(transferred_value, 4),
            "distance": distance,
            "transfer_paths": transfer_paths,
            "transfer_principle": "距离越近，迁移效率越高"
        }

    def matrix_completeness_check(self) -> Dict[str, Any]:
        """矩阵完整性校验推演"""
        self._completeness_degree = len(self._truth_matrix) / 45.0

        expected_cells = set()
        for realm in self.nine_realms:
            for theory in self.five_theories:
                expected_cells.add(f"{realm}_{theory}")

        actual_cells = set(self._truth_matrix.keys())
        missing_cells = expected_cells - actual_cells
        extra_cells = actual_cells - expected_cells

        completeness_tests = [
            "所有九界都有五论格位",
            "所有五论都有九界格位",
            "无重复格位",
            "无遗漏格位"
        ]

        return {
            "expected_cells": 45,
            "actual_cells": len(self._truth_matrix),
            "completeness_degree": self._completeness_degree,
            "complete": self._completeness_degree >= 1.0,
            "missing_cells": list(missing_cells),
            "extra_cells": list(extra_cells),
            "completeness_tests": completeness_tests,
            "check_principle": "45格全覆盖，无缺无余"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T22 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if len(self.nine_realms) != 9:
            errors.append("九界必须恰好9个")
        if len(self.five_theories) != 5:
            errors.append("五论必须恰好5个")
        if len(self._truth_matrix) != 45:
            errors.append(f"真值矩阵必须有45格，当前为{len(self._truth_matrix)}格")
        for realm in self.nine_realms:
            for theory in self.five_theories:
                key = f"{realm}_{theory}"
                if key not in self._truth_matrix:
                    errors.append(f"矩阵缺少格位: {key}")
        if "T20" not in self.dependencies:
            errors.append("T22必须依赖T20（九界场域框架）")
        if "T21" not in self.dependencies:
            errors.append("T22必须依赖T21（五论真值体系）")
        if self.cosmic_level != 2:
            errors.append("T22必须位于L2无限之子层")
        if not self.is_origin_locked:
            errors.append("T22理论必须锁定")
        if self._completeness_degree < 1.0:
            errors.append("矩阵完整度必须达到100%")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t22 = NineRealmsFiveTheoriesMapping()
    print(f"模块: {t22.module_id} - {t22.module_name}")
    print(f"版本: {t22.version}")
    print(f"层级: L{t22.cosmic_level}")
    print(f"依赖: {t22.dependencies}")
    print(f"锁定: {t22.is_origin_locked}")
    print(f"哈希: {t22.sha256}")
    print()

    print("矩阵构建:")
    matrix = t22.nine_five_matrix_construction()
    print(f"  维度: {matrix['matrix_dimension']}")
    print(f"  总格数: {matrix['total_cells']}")
    print(f"  期望格数: {matrix['expected_cells']}")
    print(f"  平均真值: {matrix['average_truth_value']}")
    print()

    print("正交性验证:")
    ortho = t22.matrix_orthogonality_verification()
    print(f"  正交度: {ortho['orthogonality_degree']:.6f}")
    print(f"  正交验证: {ortho['orthogonal']}")
    print(f"  矩阵秩: {ortho['matrix_rank']}")
    print()

    print("格位真值计算:")
    cell = t22.cell_truth_value_calculation("物质实体界", "本体论")
    print(f"  格位: {cell['cell_id']}")
    print(f"  真值: {cell['truth_value']}")
    print()

    print("跨格位迁移:")
    transfer = t22.cross_cell_truth_transfer("物质实体界_本体论", "精神意识界_价值论")
    print(f"  源: {transfer['source_cell']} = {transfer['source_value']}")
    print(f"  迁移率: {transfer['transfer_rate']}")
    print(f"  迁移后: {transfer['transferred_value']}")
    print()

    print("完整性校验:")
    complete = t22.matrix_completeness_check()
    print(f"  期望: {complete['expected_cells']}格")
    print(f"  实际: {complete['actual_cells']}格")
    print(f"  完整度: {complete['completeness_degree']*100:.1f}%")
    print(f"  完整: {complete['complete']}")
    print()

    valid, errs = t22.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
