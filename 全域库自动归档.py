"""
全域库自动归档系统
==================

三分流架构：
    1. theory_base/        —— MD理论文档（纯理论，可执行代码配套）
    2. 全域库理论对照表/     —— 对照表性质的MD（供人类对照查阅）
    3. 全域库理论原稿/       —— DOCX原始稿件（作者原稿、终版确权稿等）

使用方法：
    python 全域库自动归档.py [文件路径] [--type 类型] [--target 目标位置]

类型选项：
    --type theory      理论文档（自动放入theory_base对应位置）
    --type table       对照表（自动放入全域库理论对照表）
    --type manuscript  原稿（自动放入全域库理论原稿）
    --type auto        自动识别（默认，根据文件扩展名和内容判断）

目标位置（仅theory类型需指定）：
    --target yuandao   元道本体规则（默认）
    --target budong    不动母科层
    --target wuxian    无限之子层
"""

import os
import sys
import shutil
import hashlib
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2")

THEORY_BASE = BASE_DIR / "theory_base"
TABLE_DIR = BASE_DIR / "全域库理论对照表"
MANUSCRIPT_DIR = BASE_DIR / "全域库理论原稿"

TARGET_PATHS = {
    "yuandao": THEORY_BASE / "L0_总本源层" / "元道本体规则",
    "budong": THEORY_BASE / "L1_不动母科层",
    "wuxian": THEORY_BASE / "L2_无限之子层",
}


def ensure_dirs():
    """确保所有目标文件夹存在"""
    for d in [THEORY_BASE, TABLE_DIR, MANUSCRIPT_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    for d in TARGET_PATHS.values():
        d.mkdir(parents=True, exist_ok=True)


def calc_sha256(file_path: Path) -> str:
    """计算文件SHA256哈希"""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def detect_type(file_path: Path) -> str:
    """
    自动识别文件类型：
    - .docx → manuscript（原稿）
    - 文件名含"对照表" → table（对照表）
    - 其他.md → theory（理论）
    """
    suffix = file_path.suffix.lower()

    if suffix == ".docx":
        return "manuscript"

    if suffix == ".md":
        name = file_path.stem
        if "对照表" in name or "对照表" in name or "索引" in name or "目录" in name:
            return "table"
        return "theory"

    return "unknown"


def archive_file(file_path: str, file_type: str = "auto", target: str = "yuandao") -> dict:
    """
    归档单个文件到全域库

    Args:
        file_path: 源文件路径
        file_type: 文件类型（theory/table/manuscript/auto）
        target: theory类型的目标位置（yuandao/budong/wuxian）

    Returns:
        归档结果字典
    """
    src = Path(file_path).resolve()
    if not src.exists():
        return {"success": False, "error": f"文件不存在: {src}"}

    ensure_dirs()

    if file_type == "auto":
        file_type = detect_type(src)

    if file_type == "manuscript":
        dst_dir = MANUSCRIPT_DIR
        category = "全域库理论原稿"
    elif file_type == "table":
        dst_dir = TABLE_DIR
        category = "全域库理论对照表"
    elif file_type == "theory":
        dst_dir = TARGET_PATHS.get(target, TARGET_PATHS["yuandao"])
        category = f"theory_base/{dst_dir.relative_to(THEORY_BASE)}"
    else:
        return {"success": False, "error": f"未知文件类型: {file_type}"}

    dst = dst_dir / src.name
    shutil.copy2(src, dst)

    result = {
        "success": True,
        "source": str(src),
        "destination": str(dst),
        "category": category,
        "type": file_type,
        "sha256": calc_sha256(dst),
        "size": dst.stat().st_size,
        "archive_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return result


def archive_batch(file_list: list, file_type: str = "auto", target: str = "yuandao") -> list:
    """批量归档文件"""
    results = []
    for f in file_list:
        r = archive_file(f, file_type, target)
        results.append(r)
    return results


def print_archive_result(result: dict):
    """打印归档结果"""
    if result["success"]:
        print(f"  ✅ {Path(result['source']).name}")
        print(f"     → {result['category']}")
        print(f"     SHA256: {result['sha256'][:16]}...")
    else:
        print(f"  ❌ {result.get('source', 'unknown')}")
        print(f"     错误: {result['error']}")


def show_status():
    """显示全域库当前状态"""
    print("=" * 60)
    print("全域库当前状态")
    print("=" * 60)

    print()
    print("📁 theory_base (MD理论文档):")
    if THEORY_BASE.exists():
        md_count = len(list(THEORY_BASE.rglob("*.md")))
        py_count = len(list(THEORY_BASE.rglob("*.py")))
        print(f"   MD文件: {md_count} 个")
        print(f"   PY文件: {py_count} 个")

    print()
    print("📊 全域库理论对照表 (对照表MD):")
    if TABLE_DIR.exists():
        md_files = [f for f in TABLE_DIR.glob("*.md")]
        print(f"   文件数: {len(md_files)} 个")
        for f in sorted(md_files):
            print(f"     - {f.name}")

    print()
    print("📜 全域库理论原稿 (DOCX原稿):")
    if MANUSCRIPT_DIR.exists():
        docx_files = [f for f in MANUSCRIPT_DIR.glob("*.docx")]
        print(f"   文件数: {len(docx_files)} 个")
        for f in sorted(docx_files):
            size_mb = f.stat().st_size / 1024 / 1024
            print(f"     - {f.name} ({size_mb:.2f} MB)")

    print()
    print("=" * 60)


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        show_status()
        return

    file_type = "auto"
    target = "yuandao"
    files = []

    i = 0
    while i < len(args):
        if args[i] in ["--type", "-t"]:
            i += 1
            if i < len(args):
                file_type = args[i]
        elif args[i] in ["--target", "-T"]:
            i += 1
            if i < len(args):
                target = args[i]
        elif args[i] == "--status":
            show_status()
            return
        else:
            files.append(args[i])
        i += 1

    if not files:
        print("错误: 请指定要归档的文件路径")
        print(__doc__)
        return

    print(f"开始归档文件（类型: {file_type}, 目标: {target}）...")
    print()

    for f in files:
        result = archive_file(f, file_type, target)
        print_archive_result(result)
        print()

    print("归档完成。")


if __name__ == "__main__":
    main()
