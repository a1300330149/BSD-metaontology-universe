#!/usr/bin/env python3
"""
索引自动更新脚本 - total_index.md自动刷新（含智能体索引、跨锚点映射、版本迭代）

功能：
1. 扫描core和extension目录
2. 扫描core_base_agents和extension/agents目录
3. 自动更新total_index.md内容
4. 同步哈希校验值
5. 更新跨锚点映射表
6. 版本迭代管理
7. 批量推演归档支持

使用方式：
    python index_updater.py [--full] [--core-only] [--agents-only] [--refresh-trigger]
"""

import os
import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# 固定配置
CORE_DIR = "./theory_base/core"
EXTENSION_DIR = "./theory_base/extension"
INDEX_FILE = "./theory_base/total_index.md"
CORE_INDEX_FILE = "./theory_base/core/index_core.md"
EXTENSION_INDEX_FILE = "./theory_base/extension/index_extension.md"
HASH_BASELINE_FILE = "./theory_base/_maintenance/hash_baseline.json"
SETTINGS_FILE = "./.trae/settings.json"

# 十大公理映射
AXIOM_MAP = {
    "公理一": {"name": "宿命双边界公理", "formula": "$E_{total} = constant$", "core": "01_0元空无本源基底"},
    "公理二": {"name": "自主科研闭环动力学公理", "formula": "$\\frac{d^2R}{dt^2} + \\gamma \\frac{dR}{dt} + \\kappa R = F$", "core": "02_一重九维法理基底"},
    "公理三": {"name": "科研价值边际判定公理", "formula": "$\\theta_{mv} = 0.005$", "core": "02_一重九维法理基底"},
    "公理四": {"name": "选题创化生成机制", "formula": "$S_{t+1} = f(S_t, \\nabla S_t)$", "core": "02_一重九维法理基底"},
    "公理五": {"name": "成果落地转化范式", "formula": "$\\eta_{negS} \\ge 0.85$", "core": "02_一重九维法理基底"},
    "公理六": {"name": "全局宿命边界统摄理论", "formula": "$Order_{total} = Order_{heaven} \\otimes Order_{nature} \\otimes Order_{human}$", "core": "03_二重三界秩序基底"},
    "公理七": {"name": "系统自进化迭代公理", "formula": "$\\Delta_{evo} \\ge \\theta_{evo}$", "core": "02_一重九维法理基底"},
    "公理八": {"name": "意义涌现公理", "formula": "$\\Psi_{n} = \\mathcal{E}(\\Psi_{n-1}, ..., \\Psi_{0})$", "core": "04_核心确权归档"},
    "公理九": {"name": "意义权重公理", "formula": "$W_{n} = \\alpha \\cdot C_{n} + \\beta \\cdot S_{n} + \\gamma \\cdot P_{n}$", "core": "04_核心确权归档"},
    "公理十": {"name": "意义守恒公理", "formula": "$\\sum \\Psi_{n} \\cdot W_{n} = const$", "core": "04_核心确权归档"},
}

# 核心关键词映射
KEYWORD_MAP = {
    "0元空无": {"core": "0元本体论数理与多学科交叉验证.md", "extension": []},
    "六维流转矩阵": {"core": "六阶自主科研架构论文.md", "extension": []},
    "意义涌现算子": {"core": "意义大一统V2.0理论分册.md", "extension": []},
    "四层场论": {"core": "意义大一统V2.0理论分册.md", "extension": []},
    "M7流转": {"core": "六阶自主科研架构论文.md", "extension": []},
    "三重具现": {"core": "三态同源统摄与全域学科演化闭环体系.md", "extension": []},
    "天道/自然/人道": {"core": "全域规范性伦理完整理论体系.md", "extension": []},
    "E₁/E₂/E₃能级": {"core": "七大公理专项论文.md", "extension": []},
    "γ/κ/α系数": {"core": "七大公理专项论文.md", "extension": []},
}

# 衍生智能分类目录
AGENT_CATEGORIES = [
    "01_数理推演类衍生智能",
    "02_量子物理类衍生智能",
    "03_文明演化类衍生智能",
    "04_AI仿真工程智能",
    "05_版权文书智能",
    "06_自定义全域奇迹推演智能"
]

def calculate_sha256(file_path: str) -> str:
    """计算文件哈希"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return "ERROR"

def scan_core() -> List[Dict]:
    """扫描core目录"""
    files = []
    for subdir in ["01_0元空无本源基底", "02_一重九维法理基底", "03_二重三界秩序基底", "04_核心确权归档"]:
        subdir_path = Path(CORE_DIR) / subdir
        if not subdir_path.exists():
            continue
        for file in subdir_path.rglob("*.md"):
            rel_path = f"{subdir}/{file.name}"
            file_hash = calculate_sha256(str(file))
            files.append({
                "path": rel_path,
                "name": file.name,
                "hash": file_hash,
                "subdir": subdir,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "category": "core_base"
            })
    return files

def scan_base_agents() -> List[Dict]:
    """扫描core_base_agents目录"""
    files = []
    agents_path = Path(CORE_DIR) / "core_base_agents"
    if not agents_path.exists():
        return files

    for file in agents_path.rglob("*.md"):
        rel_path = f"core_base_agents/{file.name}"
        file_hash = calculate_sha256(str(file))
        files.append({
            "path": rel_path,
            "name": file.name,
            "hash": file_hash,
            "subdir": "core_base_agents",
            "size": file.stat().st_size,
            "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "category": "base_agent",
            "type": "基底原生智能"
        })
    return files

def scan_extension() -> List[Dict]:
    """扫描extension目录"""
    files = []
    for subdir in ["01_数理增量拓展", "02_跨尺度衍生理论", "03_工程落地分支", "04_创世世界观分支", "05_哲学交叉分支", "06_期刊学术分支", "07_空白拓展预留区"]:
        subdir_path = Path(EXTENSION_DIR) / subdir
        if not subdir_path.exists():
            continue
        for file in subdir_path.rglob("*.md"):
            # 解析版本信息
            version = "V1.0"
            version_match = re.search(r'_V(\d+\.\d+)_', file.name)
            if version_match:
                version = f"V{version_match.group(1)}"

            files.append({
                "path": str(file.relative_to(EXTENSION_DIR)),
                "name": file.name,
                "subdir": subdir,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "category": "extension_theory",
                "version": version
            })
    return files

def scan_derived_agents() -> List[Dict]:
    """扫描extension/agents目录"""
    files = []
    agents_path = Path(EXTENSION_DIR) / "agents"
    if not agents_path.exists():
        return files

    for category in AGENT_CATEGORIES:
        category_path = agents_path / category
        if not category_path.exists():
            continue
        for file in category_path.rglob("*.md"):
            files.append({
                "path": str(file.relative_to(agents_path)),
                "name": file.name,
                "subdir": category,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "category": "derived_agent",
                "type": "衍生智能"
            })
    return files

def extract_keywords(file_path: str) -> List[str]:
    """从文件中提取关键词"""
    keywords = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for keyword in KEYWORD_MAP.keys():
            if keyword in content:
                keywords.append(keyword)
    except:
        pass
    return keywords

def update_keyword_map(extension_files: List[Dict]):
    """更新跨锚点检索映射表"""
    for keyword in KEYWORD_MAP:
        KEYWORD_MAP[keyword]["extension"] = []

    for f in extension_files:
        file_path = Path(EXTENSION_DIR) / f["path"]
        keywords = extract_keywords(str(file_path))
        for keyword in keywords:
            if f["name"] not in KEYWORD_MAP[keyword]["extension"]:
                KEYWORD_MAP[keyword]["extension"].append(f["name"])

def generate_core_index(core_files: List[Dict], agent_files: List[Dict]) -> str:
    """生成core/index_core.md"""
    lines = ["# theory_base/core 基底全局索引", "", f"**最后更新**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "", "---", ""]

    # 本体基底
    for subdir in ["01_0元空无本源基底", "02_一重九维法理基底", "03_二重三界秩序基底", "04_核心确权归档"]:
        lines.append(f"## {subdir}")
        lines.append("")
        files_in_subdir = [f for f in core_files if f["subdir"] == subdir]
        if files_in_subdir:
            lines.append("| 文件名 | 哈希 | 最后修改 |")
            lines.append("|--------|------|---------|")
            for f in files_in_subdir:
                lines.append(f"| {f['name']} | `{f['hash'][:16]}...` | {f['modified']} |")
        lines.append("")

    # 基底智能
    lines.append("## core_base_agents 基底原生智能")
    lines.append("")
    if agent_files:
        lines.append("| 智能体名称 | 哈希 | 状态 |")
        lines.append("|-----------|------|------|")
        for f in agent_files:
            lines.append(f"| {f['name']} | `{f['hash'][:16]}...` | 永久锁死 |")
    else:
        lines.append("（暂无基底智能）")
    lines.append("")

    return "\n".join(lines)

def generate_extension_index(extension_files: List[Dict], derived_agent_files: List[Dict]) -> str:
    """生成extension/index_extension.md"""
    lines = ["# theory_base/extension 拓展总索引", "", f"**最后更新**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "", "---", ""]

    # 拓展理论
    for subdir in ["01_数理增量拓展", "02_跨尺度衍生理论", "03_工程落地分支", "04_创世世界观分支", "05_哲学交叉分支", "06_期刊学术分支", "07_空白拓展预留区"]:
        lines.append(f"## {subdir}")
        files_in_subdir = [f for f in extension_files if f["subdir"] == subdir]
        if files_in_subdir:
            lines.append("")
            lines.append(f"共 {len(files_in_subdir)} 个文档：")
            for f in files_in_subdir:
                lines.append(f"- {f['name']} ({f['version']})")
        else:
            lines.append("")
            lines.append("（暂无归档）")
        lines.append("")

    # 衍生智能
    lines.append("## agents 衍生智能")
    lines.append("")
    for category in AGENT_CATEGORIES:
        files_in_category = [f for f in derived_agent_files if f["subdir"] == category]
        lines.append(f"### {category}")
        if files_in_category:
            lines.append(f"共 {len(files_in_category)} 个智能：")
            for f in files_in_category:
                lines.append(f"- {f['name']}")
        else:
            lines.append("（暂无衍生智能）")
        lines.append("")

    return "\n".join(lines)

def generate_keyword_map_section() -> str:
    """生成跨锚点检索映射表"""
    lines = ["### 跨锚点检索映射表", "", "| 核心关键词 | 匹配Core原文 | 关联Extension衍生理论 |", "|-----------|------------|---------------------|"]

    for keyword, info in KEYWORD_MAP.items():
        ext_links = ", ".join(info["extension"]) if info["extension"] else "-"
        lines.append(f"| {keyword} | {info['core']} | {ext_links} |")

    return "\n".join(lines)

def check_refresh_triggers() -> Dict:
    """检查索引刷新触发时机"""
    triggers = {
        "on_new_theory_archive": False,
        "on_agent_task_complete": False,
        "on_session_start": False,
        "daily_silent_check": False,
        "manual_refresh_command": False
    }

    # 检查是否有新文件
    if os.path.exists(HASH_BASELINE_FILE):
        with open(HASH_BASELINE_FILE, 'r', encoding='utf-8') as f:
            baseline = json.load(f)

        current_files = scan_extension()
        for f in current_files:
            if f["path"] not in baseline:
                triggers["on_new_theory_archive"] = True
                break

    return triggers

def manage_version_iteration(file_name: str, extension_dir: str) -> str:
    """管理版本迭代"""
    # 解析当前版本
    version_match = re.search(r'_V(\d+\.\d+)_', file_name)
    if not version_match:
        return file_name

    current_version = float(version_match.group(1))
    base_name = file_name.replace(f'_V{version_match.group(1)}_', '_V')

    # 查找同目录下同名的所有版本
    dir_path = Path(extension_dir)
    existing_versions = []
    for f in dir_path.rglob("*.md"):
        if base_name.replace('_V', '_V') in f.name:
            v_match = re.search(r'_V(\d+\.\d+)_', f.name)
            if v_match:
                existing_versions.append(float(v_match.group(1)))

    # 计算新版本
    if existing_versions:
        new_version = max(existing_versions) + 0.1
    else:
        new_version = 1.0

    # 生成新文件名
    new_file_name = file_name.replace(f'_V{version_match.group(1)}_', f'_V{new_version:.1f}_')
    return new_file_name

def update_total_index_timestamp():
    """更新total_index.md的时间戳"""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # 更新时间戳
        new_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = re.sub(r'\*\*最后更新\*\*：.*', f'**最后更新**：{new_timestamp}', content)

        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

def run_full_update():
    """执行完整更新"""
    print("=" * 60)
    print("【索引自动更新】开始执行")
    print("=" * 60)
    print(f"时间：{datetime.now().isoformat()}")
    print()

    # 1. 扫描
    print("[1/6] 扫描core目录...")
    core_files = scan_core()
    print(f"      扫描到 {len(core_files)} 个本体基底文件")

    print("[2/6] 扫描core_base_agents目录...")
    base_agent_files = scan_base_agents()
    print(f"      扫描到 {len(base_agent_files)} 个基底智能文件")

    print("[3/6] 扫描extension目录...")
    extension_files = scan_extension()
    print(f"      扫描到 {len(extension_files)} 个拓展理论文件")

    print("[4/6] 扫描extension/agents目录...")
    derived_agent_files = scan_derived_agents()
    print(f"      扫描到 {len(derived_agent_files)} 个衍生智能文件")

    # 2. 更新跨锚点映射
    print("[5/6] 更新跨锚点检索映射表...")
    update_keyword_map(extension_files)
    print("      映射表更新完成")

    # 3. 更新分索引
    print("[6/6] 更新索引文件...")
    core_index_content = generate_core_index(core_files, base_agent_files)
    with open(CORE_INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(core_index_content)
    print("      core/index_core.md 更新完成")

    ext_index_content = generate_extension_index(extension_files, derived_agent_files)
    with open(EXTENSION_INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(ext_index_content)
    print("      extension/index_extension.md 更新完成")

    # 4. 更新总索引时间戳
    update_total_index_timestamp()
    print("      total_index.md 时间戳更新完成")

    # 5. 输出统计
    print()
    print("=" * 60)
    print("【索引自动更新】完成")
    print("=" * 60)
    print(f"本体基底文件：{len(core_files)}")
    print(f"基底智能文件：{len(base_agent_files)}")
    print(f"拓展理论文件：{len(extension_files)}")
    print(f"衍生智能文件：{len(derived_agent_files)}")
    print(f"总文件数：{len(core_files) + len(base_agent_files) + len(extension_files) + len(derived_agent_files)}")

def run_quick_refresh():
    """快速刷新（仅更新时间戳）"""
    print("=" * 60)
    print("【索引快速刷新】开始执行")
    print("=" * 60)

    update_total_index_timestamp()
    print("total_index.md 时间戳已更新")

    print("=" * 60)
    print("【索引快速刷新】完成")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="索引自动更新脚本（含智能体索引、跨锚点映射、版本迭代）")
    parser.add_argument("--full", action="store_true", help="完整更新（包括重新扫描）")
    parser.add_argument("--core-only", action="store_true", help="仅更新core索引")
    parser.add_argument("--agents-only", action="store_true", help="仅更新智能体索引")
    parser.add_argument("--quick", action="store_true", help="快速刷新（仅更新时间戳）")
    parser.add_argument("--refresh-trigger", action="store_true", help="检查索引刷新触发时机")
    args = parser.parse_args()

    if args.quick:
        run_quick_refresh()
    elif args.refresh_trigger:
        triggers = check_refresh_triggers()
        print("索引刷新触发状态：")
        for trigger, status in triggers.items():
            print(f"  - {trigger}: {'需要刷新' if status else '无需刷新'}")
    else:
        run_full_update()