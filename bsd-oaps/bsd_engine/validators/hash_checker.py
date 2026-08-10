"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：公理一（宿命双边界公理）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：哈希SHA256锁档值永久不变
"""
import hashlib
import os
import json


THEORY_BASE_DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    ))),
    "theory_base"
)

CORE_HASH_FILE = os.path.join(os.path.dirname(__file__), "..", "registry", "core_hashes.json")


def compute_file_hash(filepath, algorithm="sha256"):
    """计算单个文件的哈希值"""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_directory_hash(dirpath, extension=".md", algorithm="sha256"):
    """计算目录下所有指定扩展名文件的哈希"""
    hashes = {}
    for root, dirs, files in os.walk(dirpath):
        dirs[:] = sorted([d for d in dirs if not d.startswith("_") and d != "__pycache__"])
        for f in sorted(files):
            if f.endswith(extension):
                rel = os.path.relpath(os.path.join(root, f), dirpath)
                hashes[rel] = compute_file_hash(os.path.join(root, f), algorithm)
    return hashes


def verify_theory_base(theory_base_path=None, algorithm="sha256"):
    """验证theory_base理论库的完整性
    
    返回 (是否通过, 缺失文件, 修改文件)
    """
    if theory_base_path is None:
        theory_base_path = THEORY_BASE_DEFAULT_PATH
    
    if not os.path.isdir(theory_base_path):
        return False, [], [], {
            "total_files": 0,
            "reference_files": 0,
            "missing": 0,
            "modified": 0,
            "error": f"理论库目录不存在: {theory_base_path}",
        }
    
    current_hashes = compute_directory_hash(theory_base_path, ".md", algorithm)
    
    reference_file = os.path.join(theory_base_path, "00_index_navigation",
                                   "新四位一体3.0所有存档哈希.md")
    reference_hashes = {}
    if os.path.isfile(reference_file):
        with open(reference_file, "r", encoding="utf-8") as f:
            content = f.read()
        for line in content.split("\n"):
            if " - " in line and len(line) > 64:
                parts = line.strip().split(" - ", 1)
                if len(parts) == 2 and len(parts[0]) == 64:
                    reference_hashes[parts[1].strip()] = parts[0].strip()
    
    missing = [f for f in reference_hashes if f not in current_hashes]
    modified = []
    for f, ref_hash in reference_hashes.items():
        if f in current_hashes and current_hashes[f] != ref_hash:
            modified.append(f)
    
    passed = len(missing) == 0 and len(modified) == 0
    return passed, missing, modified, {
        "total_files": len(current_hashes),
        "reference_files": len(reference_hashes),
        "missing": len(missing),
        "modified": len(modified),
    }


def verify_core_params():
    """验证锁档核心参数未被篡改（含T90 V1.8新增7参数，共17个数值参数 + HASH）"""
    from bsd_engine.registry.constants import (
        E1, E2, E3, GAMMA, KAPPA, KAPPA_COMPETITION,
        ALPHA, THETA_NEG, THETA_MV, THETA_EVO,
        K_PLUS, K_MINUS, S_ZERO, LAMBDA, LAMBDA_INV, PI_LOCKED, PI_2,
        HASH_SHA256, AUTHOR, AUTHOR_ID,
        EXPECTED_PARAM_VALUES, EXPECTED_HASH_SHA256
    )
    
    actual = {
        "E1": E1, "E2": E2, "E3": E3,
        "GAMMA": GAMMA, "KAPPA": KAPPA, "KAPPA_COMPETITION": KAPPA_COMPETITION,
        "ALPHA": ALPHA, "THETA_NEG": THETA_NEG,
        "THETA_MV": THETA_MV, "THETA_EVO": THETA_EVO,
        # T90 V1.8 新增参数
        "K_PLUS": K_PLUS, "K_MINUS": K_MINUS, "S_ZERO": S_ZERO,
        "LAMBDA": LAMBDA, "LAMBDA_INV": LAMBDA_INV,
        "PI_LOCKED": PI_LOCKED, "PI_2": PI_2,
        # 确权信息
        "AUTHOR": AUTHOR, "AUTHOR_ID": AUTHOR_ID,
    }
    
    errors = []
    for key, val in EXPECTED_PARAM_VALUES.items():
        if actual.get(key) != val:
            errors.append(f"{key}: 期望{val}, 实际{actual.get(key)}")
    
    if HASH_SHA256 != EXPECTED_HASH_SHA256:
        errors.append(f"HASH_SHA256: 期望{EXPECTED_HASH_SHA256}, 实际{HASH_SHA256}")
    
    return len(errors) == 0, errors


def main():
    """主程序：执行完整哈希校验"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 60)
    print("BSD全域统一理论 哈希完整性校验")
    print("=" * 60)
    
    print("\n[1/2] 锁档参数校验...")
    params_ok, params_errors = verify_core_params()
    if params_ok:
        print("  ✓ 全部17个锁档参数+HASH通过校验")
    else:
        print(f"  ✗ 发现 {len(params_errors)} 个参数被篡改:")
        for e in params_errors:
            print(f"    - {e}")
    
    print(f"\n[2/2] 理论库文件校验...")
    passed, missing, modified, stats = verify_theory_base()
    print(f"  文件总数: {stats['total_files']}")
    if passed:
        print("  ✓ 理论库完整性验证通过")
    else:
        if missing:
            print(f"  ✗ 缺失文件: {len(missing)} 个")
            for f in missing[:5]:
                print(f"    - {f}")
        if modified:
            print(f"  ✗ 修改文件: {len(modified)} 个")
            for f in modified[:5]:
                print(f"    - {f}")
    
    print("\n" + "=" * 60)
    overall = params_ok and passed
    print(f"综合结果: {'✓ 全部通过' if overall else '✗ 存在问题'}")
    print("=" * 60)
    return 0 if overall else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
