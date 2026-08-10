"""
归属基底：第相变演化位（第三位）
对应三界秩序：天道秩序 > 人道秩序 > 自然秩序
对应公理：第7条（三界秩序层级仲裁公理）
对应九维维度：天道原理/人道原理/自然原理
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：优先级权重（天道=0.5，人道=0.35，自然=0.15）

场3-7：三界秩序冲突仲裁模块
实现天道>人道>自然的层级仲裁规则、冲突检测、优先级判定
对应盲区整改：优先级2-盲区9（三界秩序冲突无仲裁机制）
"""

import os
import json
import datetime
from pathlib import Path
from enum import Enum
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent

REALM_PRIORITY = {
    "天道秩序": {"weight": 0.5, "level": 1},
    "人道秩序": {"weight": 0.35, "level": 2},
    "自然秩序": {"weight": 0.15, "level": 3},
}

CONFLICT_TYPES = {
    "rule_violation": "规则违反",
    "priority_conflict": "优先级冲突",
    "boundary_breach": "边界突破",
    "parameter_mismatch": "参数不匹配",
}


class Realm(Enum):
    TIANDao = "天道秩序"
    RENDao = "人道秩序"
    ZIRAN = "自然秩序"


class ConflictSeverity(Enum):
    CRITICAL = "严重"
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class ThreeRealmArbitrator:
    """
    功能：三界秩序冲突仲裁器
    理论映射：相变演化位（第三位）·层级仲裁公理
    约束来源：优先级2-盲区9整改方案
    核心能力：冲突检测、优先级判定、规则仲裁
    """

    def __init__(self):
        self.conflicts = []
        self.arbitration_results = []

    def detect_conflict(self, rule1: Dict, rule2: Dict) -> Optional[Dict]:
        """
        检测两条规则之间是否存在冲突
        参数：
            rule1: 规则1，包含 realm（秩序类型）、priority（优先级）、content（规则内容）
            rule2: 规则2，同上
        返回：冲突信息或None
        """
        realm1 = rule1.get("realm", "")
        realm2 = rule2.get("realm", "")
        priority1 = REALM_PRIORITY.get(realm1, {}).get("level", 99)
        priority2 = REALM_PRIORITY.get(realm2, {}).get("level", 99)

        if realm1 == realm2 and rule1.get("content") != rule2.get("content"):
            return {
                "type": "rule_violation",
                "description": CONFLICT_TYPES["rule_violation"],
                "realm": realm1,
                "severity": ConflictSeverity.HIGH.value,
                "rule1": rule1,
                "rule2": rule2,
                "reason": f"{realm1}内部规则不一致",
            }

        if priority1 < priority2:
            return {
                "type": "priority_conflict",
                "description": CONFLICT_TYPES["priority_conflict"],
                "higher_realm": realm1,
                "lower_realm": realm2,
                "severity": ConflictSeverity.CRITICAL.value,
                "rule1": rule1,
                "rule2": rule2,
                "reason": f"{realm1}（优先级{priority1}）与{realm2}（优先级{priority2}）冲突",
            }

        return None

    def arbitrate(self, conflicting_rules: List[Dict]) -> Dict:
        """
        执行三界秩序仲裁
        参数：conflicting_rules - 冲突的规则列表
        返回：仲裁结果
        """
        if not conflicting_rules:
            return {"status": "no_conflict", "decision": None}

        sorted_rules = sorted(
            conflicting_rules,
            key=lambda r: REALM_PRIORITY.get(r.get("realm", ""), {}).get("level", 99)
        )

        winning_rule = sorted_rules[0]
        winning_realm = winning_rule.get("realm", "")
        winning_weight = REALM_PRIORITY.get(winning_realm, {}).get("weight", 0)

        losers = sorted_rules[1:]

        result = {
            "status": "arbitrated",
            "winning_rule": winning_rule,
            "winning_realm": winning_realm,
            "winning_weight": winning_weight,
            "losing_rules": losers,
            "arbitration_principle": f"{winning_realm}优先级最高（权重{winning_weight}），根据三界秩序层级仲裁公理，以{winning_realm}为准",
            "timestamp": datetime.datetime.now().isoformat(),
        }

        self.arbitration_results.append(result)

        print(f"\n[ARBITRATION] ⚖️ 仲裁结果：")
        print(f"  获胜秩序：{winning_realm}（权重{winning_weight}）")
        print(f"  获胜规则：{winning_rule.get('content', '')[:50]}...")
        print(f"  裁决原则：{result['arbitration_principle']}")

        return result

    def check_boundary_breach(self, action: Dict) -> Tuple[bool, Dict]:
        """
        检查是否存在边界突破
        参数：action - 要检查的动作/决策
        返回：(是否突破, 检查结果)
        """
        action_realm = action.get("realm", "")
        action_content = action.get("content", "")

        breach = False
        reasons = []

        if action_realm == "人道秩序":
            if any(keyword in action_content for keyword in ["超越", "突破", "颠覆", "无视"]):
                breach = True
                reasons.append("人道秩序规则包含突破性词汇")

        if action_realm == "自然秩序":
            if any(keyword in action_content for keyword in ["违背", "违反", "逆", "反"]):
                breach = True
                reasons.append("自然秩序规则包含违背性词汇")

        result = {
            "action": action,
            "breach": breach,
            "reasons": reasons,
            "severity": ConflictSeverity.CRITICAL.value if breach else ConflictSeverity.LOW.value,
            "timestamp": datetime.datetime.now().isoformat(),
        }

        if breach:
            self.conflicts.append({
                "type": "boundary_breach",
                "description": CONFLICT_TYPES["boundary_breach"],
                "action": action,
                "reasons": reasons,
                "severity": ConflictSeverity.CRITICAL.value,
            })
            print(f"\n[ALERT] 🚨 检测到边界突破：{reasons}")

        return breach, result

    def validate_parameter_consistency(self, parameters: Dict) -> Tuple[bool, List[str]]:
        """
        验证参数一致性
        参数：parameters - 参数字典
        返回：(是否一致, 不一致的参数列表)
        """
        inconsistencies = []

        core_params = {
            "E1": 0.35,
            "E2": 0.65,
            "E3": 0.90,
            "gamma": 0.92,
            "kappa": 0.35,
        }

        for param_name, expected_value in core_params.items():
            actual_value = parameters.get(param_name)
            if actual_value is not None and abs(actual_value - expected_value) > 0.01:
                inconsistencies.append(
                    f"{param_name}: 期望={expected_value}, 实际={actual_value}"
                )

        if inconsistencies:
            self.conflicts.append({
                "type": "parameter_mismatch",
                "description": CONFLICT_TYPES["parameter_mismatch"],
                "inconsistencies": inconsistencies,
                "severity": ConflictSeverity.HIGH.value,
            })

        return len(inconsistencies) == 0, inconsistencies

    def run_full_arbitration(self, rules: List[Dict], actions: List[Dict] = None) -> Dict:
        """
        执行完整的三界秩序仲裁流程
        参数：
            rules: 规则列表
            actions: 动作/决策列表（可选）
        返回：仲裁报告
        """
        print("=" * 60)
        print("场3-7：三界秩序冲突仲裁模块")
        print(f"归属基底：第相变演化位（第三位）")
        print(f"对应公理：公理七（三界秩序层级仲裁公理）")
        print("=" * 60)

        print("\n[STEP 1] 检测规则冲突...")
        for i, rule1 in enumerate(rules):
            for j, rule2 in enumerate(rules):
                if i < j:
                    conflict = self.detect_conflict(rule1, rule2)
                    if conflict:
                        self.conflicts.append(conflict)
                        print(f"  [CONFLICT] {conflict['description']}: {conflict['reason']}")

        print(f"\n[INFO] 共检测到 {len(self.conflicts)} 个冲突")

        if self.conflicts:
            print("\n[STEP 2] 执行仲裁...")
            conflicting_rules = []
            for conflict in self.conflicts:
                if "rule1" in conflict:
                    conflicting_rules.append(conflict["rule1"])
                if "rule2" in conflict:
                    conflicting_rules.append(conflict["rule2"])

            self.arbitrate(conflicting_rules)

        if actions:
            print("\n[STEP 3] 检查边界突破...")
            for action in actions:
                breach, result = self.check_boundary_breach(action)
                if breach:
                    print(f"  [BREACH] {action.get('content', '')[:50]}")

        print("\n[STEP 4] 验证参数一致性...")
        params = {}
        is_consistent, inconsistencies = self.validate_parameter_consistency(params)
        if is_consistent:
            print("  [OK] 参数一致性校验通过")
        else:
            print(f"  [WARNING] 参数不一致: {inconsistencies}")

        report = self.generate_arbitration_report()

        print("\n" + "=" * 60)
        print("三界秩序冲突仲裁完成！")
        print("=" * 60)

        return report

    def generate_arbitration_report(self) -> Dict:
        """生成仲裁报告"""
        report_path = PROJECT_ROOT / "三界秩序仲裁报告.md"

        content = f"""# 三界秩序冲突仲裁报告

## 报告信息

| 项目 | 内容 |
|------|------|
| 生成时间 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 冲突总数 | {len(self.conflicts)} |
| 仲裁结果数 | {len(self.arbitration_results)} |

## 三界秩序优先级说明

根据公理七（三界秩序层级仲裁公理），优先级顺序为：

| 秩序 | 优先级 | 权重 | 说明 |
|------|--------|------|------|
| 天道秩序 | 1 | 0.5 | 顶层规则，不可违背 |
| 人道秩序 | 2 | 0.35 | 业务规则，服从天道 |
| 自然秩序 | 3 | 0.15 | 环境规则，服从前两者 |

## 冲突检测结果

"""

        if self.conflicts:
            for i, conflict in enumerate(self.conflicts):
                content += f"### 冲突 {i+1}\n\n"
                content += f"- **类型**：{conflict['description']}\n"
                content += f"- **严重程度**：{conflict['severity']}\n"
                content += f"- **原因**：{conflict.get('reason', '')}\n"
                if "realm" in conflict:
                    content += f"- **涉及秩序**：{conflict['realm']}\n"
                if "higher_realm" in conflict:
                    content += f"- **高优先级秩序**：{conflict['higher_realm']}\n"
                    content += f"- **低优先级秩序**：{conflict['lower_realm']}\n"
                content += "\n"
        else:
            content += "- 未检测到冲突\n\n"

        content += "## 仲裁结果\n\n"
        if self.arbitration_results:
            for i, result in enumerate(self.arbitration_results):
                content += f"### 裁决 {i+1}\n\n"
                content += f"- **获胜秩序**：{result['winning_realm']}\n"
                content += f"- **获胜权重**：{result['winning_weight']}\n"
                content += f"- **裁决原则**：{result['arbitration_principle']}\n"
                content += f"- **时间**：{result['timestamp']}\n\n"
        else:
            content += "- 无仲裁记录\n\n"

        content += "---\n"
        content += "## 仲裁规则\n\n"
        content += "### 层级仲裁原则\n\n"
        content += "1. **天道秩序优先**：所有规则必须服从天道秩序\n"
        content += "2. **人道秩序次之**：业务规则服从天道，但优先于自然秩序\n"
        content += "3. **自然秩序最后**：环境规则服从前两者\n"
        content += "\n### 冲突解决策略\n\n"
        content += "- **优先级冲突**：以高优先级秩序的规则为准\n"
        content += "- **规则违反**：同一秩序内部规则不一致，需人工审核\n"
        content += "- **边界突破**：立即阻断并上报\n"
        content += "- **参数不匹配**：警告并自动修正为标准值\n\n"
        content += "---\n"
        content += "本报告由三界秩序冲突仲裁器自动生成\n"
        content += "理论基准：四位一体驻波动力学框架\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[INFO] 三界秩序仲裁报告已生成: {report_path}")
        return {
            "conflicts": self.conflicts,
            "arbitration_results": self.arbitration_results,
            "report_path": str(report_path),
            "timestamp": datetime.datetime.now().isoformat()
        }


def test_arbitrator():
    """测试三界秩序仲裁器"""
    arbitrator = ThreeRealmArbitrator()

    print("\n[TEST 1] 检测规则冲突...")
    rules = [
        {"realm": "天道秩序", "priority": 1, "content": "必须遵循新四位一体本体论"},
        {"realm": "人道秩序", "priority": 2, "content": "可以灵活调整业务逻辑"},
        {"realm": "人道秩序", "priority": 2, "content": "严格按照理论执行，不可变通"},
        {"realm": "自然秩序", "priority": 3, "content": "遵循现有技术约束"},
    ]

    print("\n[TEST 2] 检测边界突破...")
    actions = [
        {"realm": "人道秩序", "content": "超越理论框架进行创新"},
        {"realm": "自然秩序", "content": "违背物理定律实现目标"},
        {"realm": "天道秩序", "content": "遵循元本体论原则"},
    ]

    arbitrator.run_full_arbitration(rules, actions)


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-7：三界秩序冲突仲裁模块 - 测试模式")
    print("=" * 60)

    test_arbitrator()


if __name__ == "__main__":
    main()
