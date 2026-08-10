"""
归属基底：第相变演化位（第三位）
对应三界秩序：人道秩序
对应公理：第2条（自主科研闭环动力学公理）、第5条（科研动力学公理）
对应九维维度：创化社会/因果社会
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：道心能级E_self优先级分配

场3-5：MCP外部输出理论绑定规范
实现MCP接口输出强制绑定基底/公理标签、无标签数据丢弃、算力优先级分配
对应盲区整改：优先级1-盲区5（MCP外部产出无理论绑定校验）
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent

THEORY_LABELS = {
    "base_0": {"name": "本体拓扑位（第一位）", "axioms": ["公理一", "公理二"]},
    "base_1": {"name": "规则相位位（第二位）", "axioms": ["公理三", "公理四", "公理五", "公理六"]},
    "base_2": {"name": "相变演化位（第三位）", "axioms": ["公理七"]},
    "base_3": {"name": "3重六阶科研基底", "axioms": ["公理二", "公理五"]},
    "base_4": {"name": "4重智能体执行基底", "axioms": ["公理七"]},
}

ENERGY_LEVELS = {
    "low": {"priority": 1, "description": "低能级（轻量化模块）"},
    "medium": {"priority": 2, "description": "中能级（通用模块）"},
    "high": {"priority": 3, "description": "高能级（核心模块）"},
    "critical": {"priority": 4, "description": "临界能级（三阶实验）"},
}


class MCPTheoryBinder:
    """
    功能：MCP外部输出理论绑定器
    理论映射：2重三界秩序·人道秩序规范
    约束来源：优先级1-盲区5整改方案
    核心能力：标签强制绑定、标签校验、算力优先级分配
    """

    def __init__(self):
        self.valid_labels = set(THEORY_LABELS.keys())
        self.valid_energy_levels = set(ENERGY_LEVELS.keys())
        self.bound_outputs = []
        self.discarded_outputs = []
        self.validation_errors = []

    def bind_theory_label(self, mcp_output: Dict, base_label: str, axiom_label: str = None,
                          energy_level: str = "medium") -> Dict:
        """
        为MCP输出绑定理论标签
        参数：
            mcp_output: MCP工具返回的原始输出
            base_label: 归属基底标签（base_0~base_4）
            axiom_label: 对应公理（可选）
            energy_level: 道心能级（可选，默认medium）
        返回：绑定标签后的输出
        """
        if base_label not in self.valid_labels:
            raise ValueError(f"无效的基底标签: {base_label}，有效值: {list(self.valid_labels)}")

        if energy_level and energy_level not in self.valid_energy_levels:
            raise ValueError(f"无效的能级: {energy_level}，有效值: {list(self.valid_energy_levels)}")

        theory_info = THEORY_LABELS[base_label]
        energy_info = ENERGY_LEVELS.get(energy_level, {})

        bound_output = {
            **mcp_output,
            "__theory_binding__": {
                "base_label": base_label,
                "base_name": theory_info["name"],
                "axiom_label": axiom_label,
                "valid_axioms": theory_info["axioms"],
                "energy_level": energy_level,
                "energy_priority": energy_info.get("priority", 0),
                "energy_description": energy_info.get("description", ""),
                "binding_timestamp": datetime.datetime.now().isoformat(),
                "is_valid": True,
            }
        }

        self.bound_outputs.append(bound_output)
        return bound_output

    def validate_mcp_output(self, mcp_output: Dict) -> Tuple[bool, List[str]]:
        """
        校验MCP输出是否包含有效的理论绑定标签
        返回：(是否有效, 错误信息列表)
        """
        errors = []

        if "__theory_binding__" not in mcp_output:
            errors.append("缺少 __theory_binding__ 标签")
            self.validation_errors.append({
                "error": "缺少理论绑定标签",
                "output": str(mcp_output)[:200],
                "timestamp": datetime.datetime.now().isoformat()
            })
            return False, errors

        binding = mcp_output["__theory_binding__"]

        if "base_label" not in binding:
            errors.append("缺少 base_label")
        elif binding["base_label"] not in self.valid_labels:
            errors.append(f"无效的 base_label: {binding['base_label']}")

        if "is_valid" not in binding or not binding["is_valid"]:
            errors.append("理论绑定标记为无效")

        if errors:
            self.validation_errors.append({
                "error": "理论绑定校验失败",
                "details": errors,
                "output": str(mcp_output)[:200],
                "timestamp": datetime.datetime.now().isoformat()
            })

        return len(errors) == 0, errors

    def discard_invalid_output(self, mcp_output: Dict, reason: str) -> None:
        """
        丢弃无效的MCP输出
        参数：
            mcp_output: 无效的输出
            reason: 丢弃原因
        """
        self.discarded_outputs.append({
            "output": mcp_output,
            "reason": reason,
            "timestamp": datetime.datetime.now().isoformat()
        })

    def filter_valid_outputs(self, mcp_outputs: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        过滤有效和无效的MCP输出
        返回：(有效输出列表, 无效输出列表)
        """
        valid = []
        invalid = []

        for output in mcp_outputs:
            is_valid, errors = self.validate_mcp_output(output)
            if is_valid:
                valid.append(output)
            else:
                invalid.append(output)
                self.discard_invalid_output(output, "; ".join(errors))

        return valid, invalid

    def allocate_compute_resources(self, tasks: List[Dict]) -> List[Dict]:
        """
        根据道心能级分配算力资源
        参数：
            tasks: 任务列表，每个任务包含energy_level字段
        返回：排序后的任务列表，按优先级从高到低
        """
        sorted_tasks = sorted(
            tasks,
            key=lambda t: ENERGY_LEVELS.get(t.get("energy_level", "medium"), {}).get("priority", 0),
            reverse=True
        )

        for i, task in enumerate(sorted_tasks):
            energy_info = ENERGY_LEVELS.get(task.get("energy_level", "medium"), {})
            task["compute_priority"] = i + 1
            task["compute_allocation"] = self._calculate_allocation(energy_info["priority"])

        return sorted_tasks

    def _calculate_allocation(self, priority: int) -> float:
        """
        计算算力分配比例
        优先级越高，分配比例越大
        """
        total_priority = sum(ENERGY_LEVELS[k]["priority"] for k in ENERGY_LEVELS)
        return ENERGY_LEVELS[list(ENERGY_LEVELS.keys())[priority-1]]["priority"] / total_priority

    def generate_binding_report(self) -> str:
        """生成理论绑定报告"""
        report_path = PROJECT_ROOT / "MCP理论绑定报告.md"

        content = f"""# MCP外部输出理论绑定报告

## 生成时间
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 绑定统计

| 指标 | 数值 |
|------|------|
| 已绑定输出 | {len(self.bound_outputs)} |
| 已丢弃输出 | {len(self.discarded_outputs)} |
| 校验错误 | {len(self.validation_errors)} |

## 已绑定输出详情

"""

        if self.bound_outputs:
            for i, output in enumerate(self.bound_outputs):
                binding = output.get("__theory_binding__", {})
                content += f"### 输出 {i+1}\n\n"
                content += f"- 归属基底：{binding.get('base_name', '')}\n"
                content += f"- 对应公理：{binding.get('axiom_label', '未指定')}\n"
                content += f"- 道心能级：{binding.get('energy_description', '')}\n"
                content += f"- 绑定时间：{binding.get('binding_timestamp', '')}\n"
                content += "\n"
        else:
            content += "- 无已绑定输出\n\n"

        content += "## 已丢弃输出详情\n\n"
        if self.discarded_outputs:
            for i, discarded in enumerate(self.discarded_outputs):
                content += f"- **输出 {i+1}**：{discarded['reason']}\n"
                content += f"  时间：{discarded['timestamp']}\n\n"
        else:
            content += "- 无已丢弃输出\n\n"

        content += "## 校验错误详情\n\n"
        if self.validation_errors:
            for i, error in enumerate(self.validation_errors):
                content += f"- **错误 {i+1}**：{error['error']}\n"
                if "details" in error:
                    content += f"  详情：{', '.join(error['details'])}\n"
                content += f"  时间：{error['timestamp']}\n\n"
        else:
            content += "- 无校验错误\n\n"

        content += "---\n"
        content += "## 理论绑定规范\n\n"
        content += "### 强制标签要求\n\n"
        content += "所有MCP外部输出必须包含以下标签：\n\n"
        content += "1. `__theory_binding__`：理论绑定元数据对象\n"
        content += "   - `base_label`：归属基底标签（base_0~base_4）\n"
        content += "   - `base_name`：基底名称\n"
        content += "   - `axiom_label`：对应公理（可选）\n"
        content += "   - `energy_level`：道心能级（low/medium/high/critical）\n"
        content += "   - `is_valid`：绑定有效性标记\n\n"
        content += "### 基底标签说明\n\n"
        for label, info in THEORY_LABELS.items():
            content += f"- `{label}`：{info['name']}（对应公理：{', '.join(info['axioms'])}）\n"

        content += "\n### 道心能级说明\n\n"
        for level, info in ENERGY_LEVELS.items():
            content += f"- `{level}`：{info['description']}（优先级：{info['priority']}）\n"

        content += "\n---\n"
        content += "本报告由MCP理论绑定器自动生成\n"
        content += "理论基准：四位一体驻波动力学框架\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[INFO] MCP理论绑定报告已生成: {report_path}")
        return str(report_path)


def test_mcp_binding():
    """测试MCP理论绑定"""
    binder = MCPTheoryBinder()

    print("\n[TEST 1] 绑定有效标签...")
    test_output1 = {
        "type": "chart",
        "data": [1, 2, 3, 4, 5],
        "title": "实验结果图"
    }
    bound1 = binder.bind_theory_label(test_output1, "base_1", "公理三", "high")
    print(f"[SUCCESS] 已绑定: {bound1['__theory_binding__']['base_name']}")

    print("\n[TEST 2] 绑定高能级任务...")
    test_output2 = {
        "type": "experiment_data",
        "metrics": {"accuracy": 0.95, "f1": 0.94}
    }
    bound2 = binder.bind_theory_label(test_output2, "base_3", "公理五", "critical")
    print(f"[SUCCESS] 已绑定: {bound2['__theory_binding__']['base_name']}")

    print("\n[TEST 3] 校验有效输出...")
    is_valid, errors = binder.validate_mcp_output(bound1)
    print(f"校验结果: {'✅ 有效' if is_valid else '❌ 无效'}")
    if errors:
        print(f"错误: {errors}")

    print("\n[TEST 4] 校验无效输出（无标签）...")
    invalid_output = {"type": "chart", "data": [1, 2, 3]}
    is_valid, errors = binder.validate_mcp_output(invalid_output)
    print(f"校验结果: {'✅ 有效' if is_valid else '❌ 无效'}")
    print(f"错误: {errors}")

    print("\n[TEST 5] 算力优先级分配...")
    tasks = [
        {"task": "轻量化绘图", "energy_level": "low"},
        {"task": "三阶实验", "energy_level": "critical"},
        {"task": "通用计算", "energy_level": "medium"},
        {"task": "核心训练", "energy_level": "high"},
    ]
    sorted_tasks = binder.allocate_compute_resources(tasks)
    print("排序后的任务（按优先级从高到低）：")
    for task in sorted_tasks:
        print(f"  优先级 {task['compute_priority']}: {task['task']} (分配比例: {task['compute_allocation']:.2f})")

    print("\n[TEST 6] 生成绑定报告...")
    binder.generate_binding_report()


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-5：MCP外部输出理论绑定规范")
    print(f"归属基底：第相变演化位（第三位）")
    print(f"对应公理：公理二（自主科研闭环动力学公理）")
    print("=" * 60)

    test_mcp_binding()

    print("\n" + "=" * 60)
    print("MCP理论绑定测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
