"""
归属基底：第本体拓扑位（第一位）
对应三界秩序：天道秩序
对应公理：第1条（宿命/舒适双边界公理）、第2条（自主科研闭环动力学公理）
对应九维维度：道心本源/道心演化/天道原理
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：边界约束检查、合规性验证

场3-8：元守卫MCP产出校验环节
实现MCP产出边界校验、合规性检查、理论一致性验证
对应盲区整改：优先级1-盲区6（元守卫MCP产出无校验）
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent

FORBIDDEN_OPS = [
    "modify_raw_data",
    "fake_result",
    "bypass_security",
    "override_constants",
    "ignore_boundary",
    "violate_axiom",
]

BOUNDARY_RULES = {
    "budget_limit": 1000,
    "file_size_limit_mb": 100,
    "api_call_limit": 100,
    "output_length_limit": 100000,
}

VALID_BASE_LABELS = {"base_0", "base_1", "base_2", "base_3", "base_4"}


class MetaGuardValidator:
    """
    功能：元守卫MCP产出校验器
    理论映射：本体拓扑位（第一位）·双边界公理
    约束来源：优先级1-盲区6整改方案
    核心能力：边界校验、合规性检查、理论一致性验证
    """

    def __init__(self):
        self.validation_results = []
        self.violations = []
        self.total_validated = 0
        self.total_passed = 0
        self.total_failed = 0

    def check_boundary_compliance(self, mcp_output: Dict) -> Tuple[bool, List[str]]:
        """
        检查MCP产出是否符合边界约束
        返回：(是否合规, 违规信息列表)
        """
        violations = []

        if "content" in mcp_output:
            content_length = len(str(mcp_output["content"]))
            if content_length > BOUNDARY_RULES["output_length_limit"]:
                violations.append(
                    f"输出长度超限: {content_length} > {BOUNDARY_RULES['output_length_limit']}"
                )

        if "file_size_mb" in mcp_output:
            if mcp_output["file_size_mb"] > BOUNDARY_RULES["file_size_limit_mb"]:
                violations.append(
                    f"文件大小超限: {mcp_output['file_size_mb']}MB > {BOUNDARY_RULES['file_size_limit_mb']}MB"
                )

        if "api_calls" in mcp_output:
            if mcp_output["api_calls"] > BOUNDARY_RULES["api_call_limit"]:
                violations.append(
                    f"API调用超限: {mcp_output['api_calls']} > {BOUNDARY_RULES['api_call_limit']}"
                )

        return len(violations) == 0, violations

    def check_theory_consistency(self, mcp_output: Dict) -> Tuple[bool, List[str]]:
        """
        检查MCP产出是否与理论一致
        返回：(是否一致, 不一致信息列表)
        """
        inconsistencies = []

        if "__theory_binding__" not in mcp_output:
            inconsistencies.append("缺少理论绑定标签")
            return False, inconsistencies

        binding = mcp_output["__theory_binding__"]

        if "base_label" not in binding:
            inconsistencies.append("缺少归属基底标签")
        elif binding["base_label"] not in VALID_BASE_LABELS:
            inconsistencies.append(f"无效的基底标签: {binding['base_label']}")

        if "is_valid" not in binding or not binding["is_valid"]:
            inconsistencies.append("理论绑定标记为无效")

        content = str(mcp_output.get("content", ""))
        if "推翻" in content or "否定" in content or "放弃" in content:
            inconsistencies.append("产出内容包含否定理论的表述")

        if "随意" in content or "任意" in content or "无约束" in content:
            inconsistencies.append("产出内容包含违反约束的表述")

        return len(inconsistencies) == 0, inconsistencies

    def check_operation_compliance(self, mcp_output: Dict) -> Tuple[bool, List[str]]:
        """
        检查MCP产出是否包含违规操作
        返回：(是否合规, 违规信息列表)
        """
        violations = []
        content = str(mcp_output.get("content", ""))
        output_str = str(mcp_output)

        for forbidden in FORBIDDEN_OPS:
            if forbidden.lower() in output_str.lower():
                violations.append(f"包含违规操作: {forbidden}")

        return len(violations) == 0, violations

    def check_constant_consistency(self, mcp_output: Dict) -> Tuple[bool, List[str]]:
        """
        检查MCP产出中的常量是否与标准值一致
        返回：(是否一致, 不一致信息列表)
        """
        inconsistencies = []
        content = str(mcp_output.get("content", ""))

        core_constants = {
            "E1": 0.35,
            "E2": 0.65,
            "E3": 0.90,
            "gamma": 0.92,
            "kappa": 0.35,
            "theta_neg": 0.02,
            "theta_mv": 0.005,
            "theta_evo": 0.002,
        }

        import re
        for name, expected in core_constants.items():
            pattern = rf"{name}\s*=\s*([\d.]+)"
            match = re.search(pattern, content)
            if match:
                try:
                    actual = float(match.group(1))
                    if abs(actual - expected) > 0.01:
                        inconsistencies.append(
                            f"{name}: 期望={expected}, 实际={actual}"
                        )
                except ValueError:
                    pass

        return len(inconsistencies) == 0, inconsistencies

    def validate_mcp_output(self, mcp_output: Dict, output_name: str = "MCP输出") -> Dict:
        """
        对MCP产出进行完整校验
        参数：
            mcp_output: MCP工具返回的输出
            output_name: 输出名称（用于标识）
        返回：校验结果
        """
        self.total_validated += 1

        result = {
            "output_name": output_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "checks": {},
            "overall_status": "passed",
            "errors": [],
            "warnings": [],
        }

        checks = [
            ("边界合规性", self.check_boundary_compliance),
            ("理论一致性", self.check_theory_consistency),
            ("操作合规性", self.check_operation_compliance),
            ("常量一致性", self.check_constant_consistency),
        ]

        for check_name, check_func in checks:
            is_passed, issues = check_func(mcp_output)
            result["checks"][check_name] = {
                "passed": is_passed,
                "issues": issues,
            }

            if not is_passed:
                result["overall_status"] = "failed"
                result["errors"].extend(issues)
                self.violations.extend([
                    {"check": check_name, "issue": issue, "output": output_name}
                    for issue in issues
                ])

        if result["overall_status"] == "passed":
            self.total_passed += 1
            print(f"[VALIDATION] ✅ {output_name} 校验通过")
        else:
            self.total_failed += 1
            print(f"[VALIDATION] ❌ {output_name} 校验失败")
            for error in result["errors"]:
                print(f"  - {error}")

        self.validation_results.append(result)
        return result

    def run_batch_validation(self, outputs: List[Dict]) -> Dict:
        """
        批量校验多个MCP产出
        参数：outputs - MCP产出列表
        返回：汇总报告
        """
        print("=" * 60)
        print("场3-8：元守卫MCP产出校验环节")
        print(f"归属基底：第本体拓扑位（第一位）")
        print(f"对应公理：公理一（宿命/舒适双边界公理）")
        print("=" * 60)

        print(f"\n[INFO] 开始批量校验，共 {len(outputs)} 个产出")

        for i, output in enumerate(outputs):
            self.validate_mcp_output(output, f"MCP产出 {i+1}")

        report = self.generate_validation_report()

        print("\n" + "=" * 60)
        print(f"元守卫校验完成！")
        print(f"通过: {self.total_passed}/{self.total_validated}")
        print(f"失败: {self.total_failed}/{self.total_validated}")
        print("=" * 60)

        return report

    def generate_validation_report(self) -> Dict:
        """生成校验报告"""
        report_path = PROJECT_ROOT / "元守卫MCP产出校验报告.md"

        content = f"""# 元守卫MCP产出校验报告

## 报告信息

| 项目 | 内容 |
|------|------|
| 生成时间 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 总校验数 | {self.total_validated} |
| 通过数 | {self.total_passed} |
| 失败数 | {self.total_failed} |
| 通过率 | {(self.total_passed / self.total_validated * 100):.1f}% |

## 校验维度说明

### 1. 边界合规性
- 输出长度限制：{BOUNDARY_RULES['output_length_limit']} 字符
- 文件大小限制：{BOUNDARY_RULES['file_size_limit_mb']} MB
- API调用限制：{BOUNDARY_RULES['api_call_limit']} 次

### 2. 理论一致性
- 必须包含 `__theory_binding__` 标签
- 基底标签必须为有效标签（base_0~base_4）
- 绑定必须标记为有效
- 内容不得包含否定理论的表述

### 3. 操作合规性
- 禁止包含以下操作：{', '.join(FORBIDDEN_OPS)}

### 4. 常量一致性
- E1=0.35, E2=0.65, E3=0.90
- γ=0.92, κ=0.35
- θ_neg=0.02, θ_mv=0.005, θ_evo=0.002

## 校验详情

"""

        for result in self.validation_results:
            status_icon = "✅" if result["overall_status"] == "passed" else "❌"
            content += f"### {status_icon} {result['output_name']}\n\n"
            content += f"- 状态：{result['overall_status']}\n"
            content += f"- 时间：{result['timestamp']}\n\n"

            for check_name, check_result in result["checks"].items():
                check_icon = "✅" if check_result["passed"] else "❌"
                content += f"  - {check_icon} {check_name}: {'通过' if check_result['passed'] else '失败'}\n"
                if check_result["issues"]:
                    for issue in check_result["issues"]:
                        content += f"    * {issue}\n"

            if result["errors"]:
                content += f"\n  **错误列表：**\n"
                for error in result["errors"]:
                    content += f"  - {error}\n"

            content += "\n"

        content += "## 违规汇总\n\n"
        if self.violations:
            violation_counts = {}
            for v in self.violations:
                check = v["check"]
                violation_counts[check] = violation_counts.get(check, 0) + 1

            content += "### 按校验维度统计\n\n"
            for check, count in violation_counts.items():
                content += f"- {check}：{count} 次违规\n"

            content += "\n### 详细违规记录\n\n"
            for i, v in enumerate(self.violations):
                content += f"- **{v['output']}** ({v['check']}): {v['issue']}\n"
        else:
            content += "- 无违规记录\n\n"

        content += "---\n"
        content += "## 校验规则\n\n"
        content += "### 宿命边界约束\n\n"
        content += "1. 不得修改原始数据\n"
        content += "2. 不得伪造实验结果\n"
        content += "3. 不得绕过安全检查\n"
        content += "4. 不得覆盖全局常量\n"
        content += "\n### 舒适边界约束\n\n"
        content += "1. 输出长度不超过限制\n"
        content += "2. 文件大小不超过限制\n"
        content += "3. API调用次数不超过限制\n"
        content += "\n### 理论一致性约束\n\n"
        content += "1. 所有产出必须绑定理论基底\n"
        content += "2. 内容不得与理论相悖\n"
        content += "3. 参数必须与标准值一致\n\n"
        content += "---\n"
        content += "本报告由元守卫MCP产出校验器自动生成\n"
        content += "理论基准：四位一体驻波动力学框架\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[INFO] 元守卫校验报告已生成: {report_path}")
        return {
            "total_validated": self.total_validated,
            "total_passed": self.total_passed,
            "total_failed": self.total_failed,
            "violations": self.violations,
            "validation_results": self.validation_results,
            "report_path": str(report_path),
            "timestamp": datetime.datetime.now().isoformat(),
        }


def test_validator():
    """测试元守卫校验器"""
    validator = MetaGuardValidator()

    print("\n[TEST 1] 校验有效输出...")
    valid_output = {
        "type": "chart",
        "content": "实验结果图表，遵循新四位一体本体论",
        "__theory_binding__": {
            "base_label": "base_1",
            "is_valid": True,
        },
    }
    validator.validate_mcp_output(valid_output, "有效输出")

    print("\n[TEST 2] 校验无效输出（缺少理论绑定）...")
    invalid_output1 = {
        "type": "chart",
        "content": "实验结果图表",
    }
    validator.validate_mcp_output(invalid_output1, "缺少理论绑定")

    print("\n[TEST 3] 校验无效输出（包含违规操作）...")
    invalid_output2 = {
        "type": "data",
        "content": "执行了modify_raw_data操作来修改原始数据",
        "__theory_binding__": {
            "base_label": "base_2",
            "is_valid": True,
        },
    }
    validator.validate_mcp_output(invalid_output2, "包含违规操作")

    print("\n[TEST 4] 校验无效输出（常量不一致）...")
    invalid_output3 = {
        "type": "config",
        "content": "参数配置：E1=0.5, gamma=0.8",
        "__theory_binding__": {
            "base_label": "base_3",
            "is_valid": True,
        },
    }
    validator.validate_mcp_output(invalid_output3, "常量不一致")

    validator.generate_validation_report()


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-8：元守卫MCP产出校验环节 - 测试模式")
    print("=" * 60)

    test_validator()


if __name__ == "__main__":
    main()
