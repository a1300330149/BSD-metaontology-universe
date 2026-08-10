"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：宿命双边界公理（理论-代码双向绑定）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：绑定关系永久有效
"""
import os
import re
import hashlib


THEORY_BASE_DEFAULT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )))),
    "theory_base"
)

BSD_HEADER_RE = re.compile(r'"""\s*\n归属基底：(.+?)\n对应三界秩序：(.+?)\n对应公理：(.+?)\n对应九维维度：(.+?)\n理论原文出处：(.+?)\n固定数理常量：(.+?)\n"""', re.DOTALL)


def extract_bsd_header(filepath):
    """从Python文件提取BSD标注头
    
    返回 dict 或 None
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        m = BSD_HEADER_RE.search(content)
        if m:
            return {
                "归属基底": m.group(1).strip(),
                "对应三界秩序": m.group(2).strip(),
                "对应公理": m.group(3).strip(),
                "对应九维维度": m.group(4).strip(),
                "理论原文出处": m.group(5).strip(),
                "固定数理常量": m.group(6).strip(),
            }
    except Exception:
        pass
    return None


def scan_all_source_files(engine_path=None):
    """扫描所有源码文件，提取BSD标注
    
    返回 {相对路径: header_dict}
    """
    if engine_path is None:
        engine_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    result = {}
    for root, dirs, files in os.walk(engine_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, os.path.dirname(engine_path))
                header = extract_bsd_header(full)
                if header:
                    result[rel] = header
    return result


def verify_theory_references(theory_base_path=None):
    """验证理论引用的有效性（引用的理论文件是否真实存在）
    
    返回 (全部有效, 有效引用数, 无效引用列表)
    """
    if theory_base_path is None:
        theory_base_path = THEORY_BASE_DEFAULT
    
    headers = scan_all_source_files()
    invalid = []
    valid_count = 0
    
    for filepath, header in headers.items():
        ref = header.get("理论原文出处", "")
        if ref.startswith("theory_base/"):
            rel = ref[len("theory_base/"):]
            target = os.path.join(theory_base_path, rel)
            if not os.path.exists(target):
                invalid.append((filepath, ref))
            else:
                valid_count += 1
        elif ref:
            valid_count += 1
    
    return len(invalid) == 0, valid_count, invalid


def check_bsd_annotation_coverage():
    """检查BSD标注覆盖率
    
    返回 (覆盖率, 已标注文件数, 总文件数)
    """
    engine_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    all_py = []
    for root, dirs, files in os.walk(engine_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                all_py.append(os.path.join(root, f))
    
    annotated = 0
    for f in all_py:
        if extract_bsd_header(f):
            annotated += 1
    
    coverage = annotated / len(all_py) if all_py else 0.0
    return coverage, annotated, len(all_py)


def theory_code_binding_report():
    """生成理论-代码绑定报告"""
    print("=" * 60)
    print("BSD全域统一理论 理论-代码双向绑定校验")
    print("=" * 60)
    
    print("\n[1/4] 扫描BSD标注...")
    headers = scan_all_source_files()
    print(f"  已标注BSD标准头的文件: {len(headers)} 个")
    
    print("\n[2/4] 理论引用有效性校验...")
    ref_ok, valid_count, invalid = verify_theory_references()
    print(f"  有效引用: {valid_count} 个")
    if invalid:
        print(f"  无效引用: {len(invalid)} 个")
        for fp, ref in invalid:
            print(f"    {fp} -> {ref}")
    else:
        print("  ✓ 全部引用有效")
    
    print("\n[3/4] BSD标注覆盖率...")
    coverage, annotated, total = check_bsd_annotation_coverage()
    print(f"  已标注: {annotated}/{total} 个文件")
    print(f"  覆盖率: {coverage*100:.1f}%")
    if coverage >= 0.8:
        print("  ✓ 覆盖率达标 (≥80%)")
    else:
        print("  ✗ 覆盖率不足 80%")
    
    print("\n[4/4] 绑定关系清单...")
    for fp, h in sorted(headers.items()):
        print(f"\n  文件: {fp}")
        print(f"    归属基底: {h['归属基底']}")
        print(f"    对应公理: {h['对应公理']}")
        print(f"    九维维度: {h['对应九维维度']}")
        print(f"    理论出处: {h['理论原文出处']}")
    
    overall = ref_ok and coverage >= 0.8
    print("\n" + "=" * 60)
    print(f"综合结果: {'✓ 双向绑定有效' if overall else '✗ 绑定关系存在缺陷'}")
    print("=" * 60)
    
    return {
        "annotated_files": len(headers),
        "valid_references": valid_count,
        "invalid_references": len(invalid),
        "coverage": coverage,
        "overall_pass": overall,
    }


if __name__ == "__main__":
    import sys
    result = theory_code_binding_report()
    sys.exit(0 if result["overall_pass"] else 1)
