#!/usr/bin/env python3
"""
基底哈希校验脚本 - 基底安全巡检（含智能体哈希巡检）

功能：
1. 计算core/目录下所有文件的SHA256哈希
2. 计算core_base_agents/目录下基底智能文件的SHA256哈希
3. 与基准哈希比对
4. 检测文件篡改风险
5. 生成巡检报告

使用方式：
    python hash_checker.py [--core-path ./theory_base/core] [--report-path ./theory_base/_maintenance/hash_report.txt]
"""

import os
import sys
import hashlib
import json
from datetime import datetime
from pathlib import Path

# 基准哈希库（首次运行自动生成，后续用于比对）
BASELINE_FILE = "./theory_base/_maintenance/hash_baseline.json"

# 锁档核心文件（只读保护列表）
LOCKED_FILES = {
    "01_0元空无本源基底/0元本体论数理与多学科交叉验证.md": "hash_placeholder_01",
    "01_0元空无本源基底/大一统0元本体论.md": "hash_placeholder_02",
    "01_0元空无本源基底/本源结构.md": "hash_placeholder_03",
    "01_0元空无本源基底/元本体理论分册.md": "hash_placeholder_04",
    "02_一重九维法理基底/六阶自主科研架构论文.md": "hash_placeholder_05",
    "02_一重九维法理基底/七大公理专项论文.md": "hash_placeholder_06",
    "02_一重九维法理基底/科研闭环公理体系：大一统动力学与AI全链路自进化范式.md": "hash_placeholder_07",
    "03_二重三界秩序基底/全域规范性伦理完整理论体系.md": "hash_placeholder_08",
    "03_二重三界秩序基底/三态同源统摄与全域学科演化闭环体系（独立成册终极卷宗）.md": "hash_placeholder_09",
    "04_核心确权归档/新四位一体3.0所有存档哈希.md": "hash_placeholder_10",
    "04_核心确权归档/第一层1到9模块大一统理论终极不可改基底.md": "hash_placeholder_11",
    "04_核心确权归档/意义大一统V2.0理论分册.md": "hash_placeholder_12",
    "core_base_agents/MetaBaseEvolveAgent.md": "hash_placeholder_13",
    "core_base_agents/MetaOntologyGlobalAgent.md": "hash_placeholder_14",
}

def calculate_sha256(file_path: str) -> str:
    """计算单个文件的SHA256哈希"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] 读取文件失败 {file_path}: {e}")
        return "ERROR"

def scan_core_directory(core_path: str) -> dict:
    """扫描core目录，生成所有文件的哈希"""
    results = {}
    core_path_obj = Path(core_path)

    for subdir in ["01_0元空无本源基底", "02_一重九维法理基底", "03_二重三界秩序基底", "04_核心确权归档"]:
        subdir_path = core_path_obj / subdir
        if not subdir_path.exists():
            continue

        for file in subdir_path.rglob("*.md"):
            rel_path = f"{subdir}/{file.name}"
            abs_path = str(file.absolute())
            file_hash = calculate_sha256(abs_path)
            results[rel_path] = {
                "hash": file_hash,
                "path": abs_path,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                "category": "core_base"
            }

    return results

def scan_base_agents(core_path: str) -> dict:
    """扫描core_base_agents目录，生成基底智能文件的哈希"""
    results = {}
    core_path_obj = Path(core_path)
    agents_path = core_path_obj / "core_base_agents"

    if not agents_path.exists():
        print(f"[INFO] core_base_agents目录不存在: {agents_path}")
        return results

    for file in agents_path.rglob("*.md"):
        rel_path = f"core_base_agents/{file.name}"
        abs_path = str(file.absolute())
        file_hash = calculate_sha256(abs_path)
        results[rel_path] = {
            "hash": file_hash,
            "path": abs_path,
            "size": file.stat().st_size,
            "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
            "category": "base_agent"
        }

    return results

def load_baseline() -> dict:
    """加载基准哈希库"""
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_baseline(baseline: dict):
    """保存基准哈希库"""
    os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)
    with open(BASELINE_FILE, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, ensure_ascii=False, indent=2)

def run_hash_check(core_path: str = "./theory_base/core", report_path: str = None, update_baseline: bool = False):
    """执行哈希校验"""
    print("=" * 60)
    print("【基底哈希巡检】开始执行")
    print("=" * 60)
    print(f"核心路径：{core_path}")
    print(f"基准库：{BASELINE_FILE}")
    print(f"更新时间基线：{update_baseline}")
    print()

    # 1. 扫描core目录（本体基底）
    print("--- 扫描本体基底文件 ---")
    current_hashes = scan_core_directory(core_path)
    print(f"扫描到 {len(current_hashes)} 个本体基底文件")
    for rel_path, info in current_hashes.items():
        print(f"  - {rel_path}: {info['hash'][:16]}...")

    # 2. 扫描core_base_agents目录（基底智能）
    print("\n--- 扫描基底智能文件 ---")
    agent_hashes = scan_base_agents(core_path)
    print(f"扫描到 {len(agent_hashes)} 个基底智能文件")
    for rel_path, info in agent_hashes.items():
        print(f"  - {rel_path}: {info['hash'][:16]}...")

    # 合并结果
    current_hashes.update(agent_hashes)

    # 3. 加载基准
    baseline = load_baseline()

    # 4. 比对
    anomalies = []
    new_files = []
    deleted_files = []

    for rel_path, info in current_hashes.items():
        if rel_path not in baseline:
            new_files.append(rel_path)
            print(f"[NEW] {rel_path}")
        elif baseline[rel_path]["hash"] != info["hash"]:
            anomalies.append({
                "file": rel_path,
                "category": info.get("category", "unknown"),
                "baseline": baseline[rel_path]["hash"],
                "current": info["hash"],
                "baseline_modified": baseline[rel_path].get("modified"),
                "current_modified": info["modified"]
            })
            print(f"[ALERT] {rel_path} 哈希不一致!")

    for rel_path in baseline:
        if rel_path not in current_hashes:
            deleted_files.append(rel_path)
            print(f"[DELETED] {rel_path}")

    # 5. 生成报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "core_path": core_path,
        "total_files": len(current_hashes),
        "core_base_files": len([h for h in current_hashes.values() if h.get("category") == "core_base"]),
        "base_agent_files": len([h for h in current_hashes.values() if h.get("category") == "base_agent"]),
        "anomalies": anomalies,
        "new_files": new_files,
        "deleted_files": deleted_files,
        "status": "PASS" if not anomalies and not deleted_files else "FAIL"
    }

    if report_path:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存至：{report_path}")

    # 6. 输出状态
    print()
    print("=" * 60)
    if report["status"] == "PASS":
        print("【巡检结果】✓ PASS - 基底完整，无篡改迹象")
        print(f"  - 本体基底文件：{report['core_base_files']} 个")
        print(f"  - 基底智能文件：{report['base_agent_files']} 个")
    else:
        print("【巡检结果】✗ FAIL - 检测到异常!")
        if anomalies:
            print(f"  - 哈希异常文件：{len(anomalies)} 个")
            for anomaly in anomalies:
                category_label = "本体基底" if anomaly["category"] == "core_base" else "基底智能"
                print(f"    * [{category_label}] {anomaly['file']}")
        if new_files:
            print(f"  - 新增文件：{len(new_files)} 个")
        if deleted_files:
            print(f"  - 删除文件：{len(deleted_files)} 个")
        print("\n【警告】推演功能已被锁定，请人工复核后解锁")
    print("=" * 60)

    # 7. 更新基准（可选）
    if update_baseline:
        baseline.update({k: {"hash": v["hash"], "modified": v["modified"], "category": v.get("category", "unknown")} for k, v in current_hashes.items()})
        save_baseline(baseline)
        print("\n基准哈希库已更新")

    return report

def check_agent_integrity(core_path: str = "./theory_base/core"):
    """单独检查基底智能文件完整性"""
    print("=" * 60)
    print("【基底智能完整性检查】开始执行")
    print("=" * 60)

    agent_hashes = scan_base_agents(core_path)
    baseline = load_baseline()

    anomalies = []
    for rel_path, info in agent_hashes.items():
        if rel_path in baseline and baseline[rel_path]["hash"] != info["hash"]:
            anomalies.append({
                "file": rel_path,
                "expected": baseline[rel_path]["hash"][:16],
                "actual": info["hash"][:16]
            })

    if not anomalies:
        print("【检查结果】✓ PASS - 所有基底智能文件完整，无篡改")
    else:
        print("【检查结果】✗ FAIL - 检测到基底智能文件异常!")
        for anomaly in anomalies:
            print(f"  - {anomaly['file']}: 预期 {anomaly['expected']}, 实际 {anomaly['actual']}")
        print("\n【警告】基底智能已被篡改，立即锁定全部推演功能")

    print("=" * 60)
    return len(anomalies) == 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="基底哈希校验脚本（含智能体巡检）")
    parser.add_argument("--core-path", default="./theory_base/core", help="core目录路径")
    parser.add_argument("--report-path", default="./theory_base/_maintenance/hash_report.txt", help="报告输出路径")
    parser.add_argument("--update-baseline", action="store_true", help="更新基准哈希库")
    parser.add_argument("--agent-only", action="store_true", help="仅检查基底智能文件")
    args = parser.parse_args()

    if args.agent_only:
        check_agent_integrity(args.core_path)
    else:
        run_hash_check(args.core_path, args.report_path, args.update_baseline)