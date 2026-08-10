"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：全部39条公理合规性
对应九维维度：元理天道、天道原理
理论原文出处：theory_base/L0_总本源层/全域理论全集
固定数理常量：γ=0.92, κ=0.35
"""
from typing import Dict, List, Tuple


def check_axiom_completeness() -> Tuple[bool, Dict]:
    """检查39条公理完整性（五大公理集齐全）
    
    返回 (是否完整, 统计信息)
    """
    stats = {}
    
    try:
        from bsd_engine.axioms.seven_origin_axioms import get_all_axioms as origin_get
        origin_axioms = origin_get()
        stats["origin_axioms"] = len(origin_axioms)
    except Exception as e:
        stats["origin_error"] = str(e)
        stats["origin_axioms"] = 0
        origin_axioms = []
    
    try:
        from bsd_engine.axioms.three_meaning_axioms import get_all_axioms as meaning_get
        meaning_axioms = meaning_get()
        stats["meaning_axioms"] = len(meaning_axioms)
    except Exception as e:
        stats["meaning_error"] = str(e)
        stats["meaning_axioms"] = 0
        meaning_axioms = []
    
    try:
        from bsd_engine.axioms.twelve_bsd_axioms import get_all_axioms as bsd_get
        bsd_axioms = bsd_get()
        stats["bsd_axioms"] = len(bsd_axioms)
    except Exception as e:
        stats["bsd_error"] = str(e)
        stats["bsd_axioms"] = 0
        bsd_axioms = []
    
    try:
        from bsd_engine.axioms.nine_special_axioms import get_all_axioms as special_get
        special_axioms = special_get()
        stats["special_axioms"] = len(special_axioms)
    except Exception as e:
        stats["special_error"] = str(e)
        stats["special_axioms"] = 0
        special_axioms = []
    
    try:
        from bsd_engine.axioms.eight_unification_axioms import get_all_axioms as unif_get
        unif_axioms = unif_get()
        stats["unification_axioms"] = len(unif_axioms)
    except Exception as e:
        stats["unification_error"] = str(e)
        stats["unification_axioms"] = 0
        unif_axioms = []
    
    total = stats["origin_axioms"] + stats["meaning_axioms"] + stats["bsd_axioms"] \
            + stats["special_axioms"] + stats["unification_axioms"]
    stats["total_axioms"] = total
    
    expected = 7 + 3 + 12 + 9 + 8
    stats["expected_total"] = expected
    stats["complete"] = total >= expected
    
    return stats["complete"], stats


def check_equation_completeness() -> Tuple[bool, Dict]:
    """检查11个方程求解器完整性
    
    返回 (是否完整, 统计信息)
    """
    equations = [
        "standing_wave",
        "phase_transition",
        "emergence",
        "kappa_phase",
        "four_force_unification",
        "entropy_flow",
        "steady_state_potential",
        "global_coherence",
        "structural_entropy",
        "cosmological_constant",
        "life_steady_state",
    ]
    
    found = []
    missing = []
    function_counts = {}
    
    for eq_name in equations:
        try:
            mod = __import__(f"bsd_engine.equations.{eq_name}", fromlist=[""])
            found.append(eq_name)
            function_counts[eq_name] = len(
                [x for x in dir(mod) if not x.startswith("_") and callable(getattr(mod, x))]
            )
        except Exception as e:
            missing.append(eq_name)
    
    stats = {
        "expected": 11,
        "found": len(found),
        "missing": missing,
        "function_counts": function_counts,
        "complete": len(missing) == 0,
    }
    return stats["complete"], stats


def check_registry_compliance() -> Tuple[bool, Dict]:
    """检查注册表合规性
    
    返回 (是否合规, 统计信息)
    """
    issues = []
    stats = {}
    
    try:
        from bsd_engine.registry.constants import (
            E1, E2, E3, GAMMA, KAPPA,
            verify_params
        )
        stats["constants_loaded"] = True
        
        try:
            result = verify_params()
            stats["immutable_check"] = result
            if not result:
                issues.append("参数可变性校验失败")
        except Exception as e:
            issues.append(f"参数可变性校验异常: {e}")
        
        if E1 != 0.35:
            issues.append(f"E1={E1} ≠ 0.35")
        if E2 != 0.65:
            issues.append(f"E2={E2} ≠ 0.65")
        if E3 != 0.90:
            issues.append(f"E3={E3} ≠ 0.90")
        if GAMMA != 0.92:
            issues.append(f"GAMMA={GAMMA} ≠ 0.92")
        if KAPPA != 0.35:
            issues.append(f"KAPPA={KAPPA} ≠ 0.35")
    except Exception as e:
        issues.append(f"注册加载失败: {e}")
        stats["constants_loaded"] = False
    
    stats["issues"] = issues
    return len(issues) == 0, stats


def run_full_compliance_check() -> Dict:
    """运行完整合规性检查"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    results = {}
    
    print("=" * 60)
    print("BSD全域统一理论 合规性检查")
    print("=" * 60)
    
    print("\n[1/3] 公理完整性校验...")
    axiom_ok, axiom_stats = check_axiom_completeness()
    results["axioms"] = axiom_stats
    print(f"  本源公理: {axiom_stats.get('origin_axioms', 0)}/7")
    print(f"  意义公理: {axiom_stats.get('meaning_axioms', 0)}/3")
    print(f"  BSD基础: {axiom_stats.get('bsd_axioms', 0)}/12")
    print(f"  专项公理: {axiom_stats.get('special_axioms', 0)}/9")
    print(f"  统一公理: {axiom_stats.get('unification_axioms', 0)}/8")
    print(f"  总计: {axiom_stats.get('total_axioms', 0)}/{axiom_stats.get('expected_total', 39)}")
    print(f"  结果: {'✓ 通过' if axiom_ok else '✗ 不通过'}")
    
    print("\n[2/3] 方程求解器完整性校验...")
    eq_ok, eq_stats = check_equation_completeness()
    results["equations"] = eq_stats
    print(f"  找到 {eq_stats['found']}/11 个求解器")
    for eq_name, count in eq_stats.get("function_counts", {}).items():
        print(f"    {eq_name}: {count} 个函数")
    if eq_stats["missing"]:
        print(f"  缺失: {eq_stats['missing']}")
    print(f"  结果: {'✓ 通过' if eq_ok else '✗ 不通过'}")
    
    print("\n[3/3] 注册参数合规性校验...")
    reg_ok, reg_stats = check_registry_compliance()
    results["registry"] = reg_stats
    if reg_ok:
        print("  ✓ 所有锁档参数合规")
    else:
        print(f"  ✗ 发现 {len(reg_stats.get('issues', []))} 个问题:")
        for issue in reg_stats.get("issues", []):
            print(f"    - {issue}")
    
    overall = axiom_ok and eq_ok and reg_ok
    results["overall_pass"] = overall
    
    print("\n" + "=" * 60)
    print(f"综合结果: {'✓ 全部合规' if overall else '✗ 存在不合规项'}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    import sys
    results = run_full_compliance_check()
    sys.exit(0 if results["overall_pass"] else 1)
