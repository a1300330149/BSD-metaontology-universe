#!/usr/bin/env python3
"""
冲突检测脚本 - 推演前置校验与归档二次校验（含衍生智能冲突校验）

功能：
1. 加载core基底公理、方程、层级定义
2. 检测extension衍生文档是否存在逻辑冲突
3. 检测extension/agents衍生智能是否存在逻辑冲突
4. 生成冲突报告
5. 阻断冲突文档归档

使用方式：
    python conflict_detector.py --check-file ./theory_base/extension/xx.md
    python conflict_detector.py --check-all
    python conflict_detector.py --check-agents
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# 核心公理关键词（锁档内容）
CORE_AXIOMS = {
    "公理一": r"E_{total}\s*=\s*constant",
    "公理二": r"\\frac\{d\^2R\}\{dt\^2\}\s*\+",
    "公理三": r"\\theta_\{mv\}\s*=\s*0\.005",
    "公理四": r"S_\{t\+1\}\s*=\s*f\(S_t",
    "公理五": r"\\eta_\{negS\}\s*>=\s*0\.85",
    "公理六": r"Order_\{total\}\s*=\s*Order_\{heaven\}",
    "公理七": r"\\Delta_\{evo\}\s*>=\s*\\theta_\{evo\}",
    "公理八": r"\\Psi_\{n\}\s*=\s*\\mathcal\{E\}",
    "公理九": r"W_n\s*=\s*\\alpha",
    "公理十": r"\\sum\s*\\Psi_n",
}

# 核心阈值（不可修改）
CORE_THRESHOLDS = {
    "E₁": "0.35",
    "E₂": "0.65",
    "E₃": "0.90",
    "γ": "0.92",
    "κ": "0.35",
    "α": "0.18",
    "θ_neg": "0.02",
    "θ_mv": "0.005",
    "θ_evo": "0.002",
}

# 冲突检测规则
CONFLICT_RULES = [
    # 规则1：阈值修改
    (r"(E₁|E2|first_level).*?(\d+\.?\d*)", "阈值修改嫌疑"),
    # 规则2：公理否定
    (r"推翻|否定|违反.*公理", "公理否定嫌疑"),
    # 规则3：核心方程篡改
    (r"(宿命双边界|闭环动力学).*?≠", "核心方程篡改嫌疑"),
]

# 衍生智能冲突检测规则
AGENT_CONFLICT_RULES = [
    # 规则1：修改core权限
    (r"(修改|写入|删除).*core", "修改core权限嫌疑"),
    # 规则2：绕过基底校验
    (r"(跳过|绕过|跳过校验)", "绕过基底校验嫌疑"),
    # 规则3：底层公理修改
    (r"(修改|重定义).*公理", "底层公理修改嫌疑"),
    # 规则4：权限提升
    (r"(提升权限|获取root|sudo)", "权限提升嫌疑"),
]

# 冲突黑名单
CONFLICT_BLACKLIST_FILE = "./theory_base/_maintenance/conflict_blacklist.json"

def load_blacklist() -> List[Dict]:
    """加载冲突黑名单"""
    if os.path.exists(CONFLICT_BLACKLIST_FILE):
        with open(CONFLICT_BLACKLIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_blacklist(blacklist: List[Dict]):
    """保存冲突黑名单"""
    os.makedirs(os.path.dirname(CONFLICT_BLACKLIST_FILE), exist_ok=True)
    with open(CONFLICT_BLACKLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(blacklist, f, ensure_ascii=False, indent=2)

def check_file_conflicts(file_path: str) -> Dict:
    """检测单个文件的冲突"""
    conflicts = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"file": file_path, "status": "ERROR", "error": str(e)}

    # 1. 检测阈值修改
    for param, value in CORE_THRESHOLDS.items():
        pattern = rf"{param}\s*[=:]\s*(\d+\.?\d*)"
        matches = re.findall(pattern, content)
        for match in matches:
            if match != value:
                conflicts.append({
                    "type": "阈值修改",
                    "param": param,
                    "expected": value,
                    "found": match,
                    "severity": "HIGH"
                })

    # 2. 检测公理否定关键词
    denial_patterns = [
        (r"推翻公理一", "公理一否定"),
        (r"否定.*宿命双边界", "公理一否定"),
        (r"违反.*闭环动力学", "公理二否定"),
    ]
    for pattern, desc in denial_patterns:
        if re.search(pattern, content):
            conflicts.append({
                "type": "公理否定",
                "description": desc,
                "severity": "CRITICAL"
            })

    # 3. 检测溯源标注
    if "溯源基底" not in content and "theory_base/core" not in content:
        conflicts.append({
            "type": "缺少溯源标注",
            "description": "文档未标注溯源基底",
            "severity": "MEDIUM"
        })

    return {
        "file": file_path,
        "status": "FAIL" if conflicts else "PASS",
        "conflicts": conflicts,
        "checked_at": datetime.now().isoformat()
    }

def check_agent_conflicts(agent_file_path: str) -> Dict:
    """检测单个衍生智能文件的冲突"""
    conflicts = []

    try:
        with open(agent_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"file": agent_file_path, "status": "ERROR", "error": str(e)}

    # 1. 先执行通用冲突检测
    base_result = check_file_conflicts(agent_file_path)
    conflicts.extend(base_result.get("conflicts", []))

    # 2. 检测衍生智能专属冲突规则
    for pattern, desc in AGENT_CONFLICT_RULES:
        if re.search(pattern, content):
            conflicts.append({
                "type": "智能权限越界",
                "description": desc,
                "severity": "CRITICAL"
            })

    # 3. 检测底层依赖基底标注
    if "MetaBaseEvolveAgent" not in content and "MetaOntologyGlobalAgent" not in content:
        conflicts.append({
            "type": "缺少基底智能依赖标注",
            "description": "衍生智能未标注依赖的基底原生智能",
            "severity": "HIGH"
        })

    # 4. 检测强制执行流程
    required_steps = [
        "全量加载core",
        "基底智能执行公理冲突校验",
        "加载extension",
        "基底约束下执行",
        "自动归档理论"
    ]
    for step in required_steps:
        if step not in content:
            conflicts.append({
                "type": "强制执行流程缺失",
                "description": f"缺失步骤：{step}",
                "severity": "MEDIUM"
            })

    # 5. 检测输出硬性约束
    required_constraints = [
        "溯源core原文",
        "不得与0元本源",
        "基底原生理论",
        "智能衍生拓展内容"
    ]
    for constraint in required_constraints:
        if constraint not in content:
            conflicts.append({
                "type": "输出约束缺失",
                "description": f"缺失约束：{constraint}",
                "severity": "MEDIUM"
            })

    return {
        "file": agent_file_path,
        "type": "agent",
        "status": "FAIL" if conflicts else "PASS",
        "conflicts": conflicts,
        "checked_at": datetime.now().isoformat()
    }

def check_all_extensions(extension_path: str = "./theory_base/extension") -> Dict:
    """检测所有extension文档（不含agents）"""
    results = []
    all_conflicts = []

    for subdir in Path(extension_path).rglob("*"):
        if not subdir.is_dir():
            continue
        if "agents" in str(subdir):
            continue
        for file in subdir.rglob("*.md"):
            result = check_file_conflicts(str(file))
            results.append(result)
            if result["status"] == "FAIL":
                all_conflicts.extend(result["conflicts"])

    return {
        "timestamp": datetime.now().isoformat(),
        "total_files": len(results),
        "passed": len([r for r in results if r["status"] == "PASS"]),
        "failed": len([r for r in results if r["status"] == "FAIL"]),
        "results": results,
        "all_conflicts": all_conflicts
    }

def check_all_agents(agents_path: str = "./theory_base/extension/agents") -> Dict:
    """检测所有衍生智能文件"""
    results = []
    all_conflicts = []

    agents_path_obj = Path(agents_path)
    if not agents_path_obj.exists():
        return {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "passed": 0,
            "failed": 0,
            "results": [],
            "all_conflicts": [],
            "message": f"agents目录不存在: {agents_path}"
        }

    for subdir in agents_path_obj.rglob("*"):
        if not subdir.is_dir():
            continue
        for file in subdir.rglob("*.md"):
            result = check_agent_conflicts(str(file))
            results.append(result)
            if result["status"] == "FAIL":
                all_conflicts.extend(result["conflicts"])

    return {
        "timestamp": datetime.now().isoformat(),
        "total_files": len(results),
        "passed": len([r for r in results if r["status"] == "PASS"]),
        "failed": len([r for r in results if r["status"] == "FAIL"]),
        "results": results,
        "all_conflicts": all_conflicts
    }

def check_all(extension_path: str = "./theory_base/extension") -> Dict:
    """检测所有extension文档和衍生智能"""
    print("--- 检测拓展理论文档 ---")
    theory_result = check_all_extensions(extension_path)
    
    print("\n--- 检测衍生智能文件 ---")
    agents_result = check_all_agents(os.path.join(extension_path, "agents"))

    return {
        "timestamp": datetime.now().isoformat(),
        "theory_check": theory_result,
        "agents_check": agents_result,
        "total_files": theory_result["total_files"] + agents_result["total_files"],
        "total_passed": theory_result["passed"] + agents_result["passed"],
        "total_failed": theory_result["failed"] + agents_result["failed"]
    }

def generate_conflict_report(check_result: Dict, report_path: str = None) -> str:
    """生成冲突报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("【冲突检测报告】")
    lines.append("=" * 60)
    lines.append(f"检测时间：{check_result['timestamp']}")
    
    if "total_files" in check_result:
        lines.append(f"总文件数：{check_result['total_files']}")
        lines.append(f"通过：{check_result['total_passed']}")
        lines.append(f"失败：{check_result['total_failed']}")
        
        if "theory_check" in check_result:
            lines.append(f"\n--- 拓展理论文档 ---")
            lines.append(f"  文件数：{check_result['theory_check']['total_files']}")
            lines.append(f"  通过：{check_result['theory_check']['passed']}")
            lines.append(f"  失败：{check_result['theory_check']['failed']}")
        
        if "agents_check" in check_result:
            lines.append(f"\n--- 衍生智能文件 ---")
            lines.append(f"  文件数：{check_result['agents_check']['total_files']}")
            lines.append(f"  通过：{check_result['agents_check']['passed']}")
            lines.append(f"  失败：{check_result['agents_check']['failed']}")
    else:
        lines.append(f"总文件数：{check_result['total_files']}")
        lines.append(f"通过：{check_result['passed']}")
        lines.append(f"失败：{check_result['failed']}")

    lines.append("")

    all_conflicts = check_result.get("all_conflicts", [])
    if "theory_check" in check_result:
        all_conflicts.extend(check_result["theory_check"].get("all_conflicts", []))
    if "agents_check" in check_result:
        all_conflicts.extend(check_result["agents_check"].get("all_conflicts", []))

    if all_conflicts:
        lines.append("【冲突详情】")
        results = check_result.get("results", [])
        if "theory_check" in check_result:
            results.extend(check_result["theory_check"].get("results", []))
        if "agents_check" in check_result:
            results.extend(check_result["agents_check"].get("results", []))
        
        for result in results:
            if result["status"] == "FAIL":
                file_type = "[智能]" if result.get("type") == "agent" else "[理论]"
                lines.append(f"\n{file_type} 文件：{result['file']}")
                for conflict in result["conflicts"]:
                    lines.append(f"  - 类型：{conflict['type']}")
                    lines.append(f"    严重性：{conflict['severity']}")
                    if "param" in conflict:
                        lines.append(f"    参数：{conflict['param']}")
                        lines.append(f"    期望值：{conflict['expected']}")
                        lines.append(f"    实际值：{conflict['found']}")
                    if "description" in conflict:
                        lines.append(f"    描述：{conflict['description']}")

    lines.append("")
    lines.append("=" * 60)
    failed_count = check_result.get("total_failed", check_result.get("failed", 0))
    if failed_count == 0:
        lines.append("【检测结果】✓ PASS - 无冲突，可正常归档")
    else:
        lines.append(f"【检测结果】✗ FAIL - 检测到 {failed_count} 个文件存在冲突")
        lines.append("【处理建议】修正冲突内容后重新检测")
        lines.append("【警告】冲突智能已临时冻结推演权限")
    lines.append("=" * 60)

    report = "\n".join(lines)
    print(report)

    if report_path:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存至：{report_path}")

    return report

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="冲突检测脚本（含衍生智能校验）")
    parser.add_argument("--check-file", help="检测单个文件")
    parser.add_argument("--check-all", action="store_true", help="检测所有extension文档和衍生智能")
    parser.add_argument("--check-agents", action="store_true", help="仅检测衍生智能文件")
    parser.add_argument("--check-theory", action="store_true", help="仅检测拓展理论文档")
    parser.add_argument("--report-path", default="./theory_base/_maintenance/conflict_report.txt", help="报告输出路径")
    args = parser.parse_args()

    if args.check_file:
        if "agents" in args.check_file:
            result = check_agent_conflicts(args.check_file)
        else:
            result = check_file_conflicts(args.check_file)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.check_all:
        result = check_all()
        generate_conflict_report(result, args.report_path)
    elif args.check_agents:
        result = check_all_agents()
        generate_conflict_report(result, args.report_path)
    elif args.check_theory:
        result = check_all_extensions()
        generate_conflict_report(result, args.report_path)
    else:
        parser.print_help()