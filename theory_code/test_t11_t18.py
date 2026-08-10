"""
T11-T18 模块综合测试脚本
验证所有8个理论模块都能正确导入并通过validate

运行方式：在 Agent_v2 目录下执行 python -m theory_code.test_t11_t18
"""

import sys
import os
import importlib


MODULES = [
    ("T11", "theory_code.theories.t11_nine_dimensional_foundation", "NineDimensionalFoundation"),
    ("T12", "theory_code.theories.t12_fate_double_boundary", "FateDoubleBoundaryAxiom"),
    ("T13", "theory_code.theories.t13_autonomous_research_closure", "AutonomousResearchClosure"),
    ("T14", "theory_code.theories.t14_research_value_marginal", "ResearchValueMarginal"),
    ("T15", "theory_code.theories.t15_topic_creation_mechanism", "TopicCreationMechanism"),
    ("T16", "theory_code.theories.t16_achievement_transformation", "AchievementTransformation"),
    ("T17", "theory_code.theories.t17_global_fate_boundary", "GlobalFateBoundary"),
    ("T18", "theory_code.theories.t18_system_self_evolution", "SystemSelfEvolution"),
]


def run_all_tests():
    print("=" * 70)
    print("T11-T18 理论模块综合测试")
    print("=" * 70)
    print()

    total = len(MODULES)
    passed = 0
    failed = 0
    results = []

    for module_id, module_path, class_name in MODULES:
        print(f"--- 测试 {module_id} ---")
        try:
            mod = importlib.import_module(module_path)
            module_class = getattr(mod, class_name)
            module = module_class()

            print(f"  模块名称: {module.module_name}")
            print(f"  版本: {module.version}")
            print(f"  层级: L{module.cosmic_level}")
            print(f"  依赖: {module.dependencies}")
            print(f"  本源锁定: {module.is_origin_locked}")
            print(f"  锁档哈希: {module.sha256}")

            valid, errors = module.validate()
            if valid:
                print(f"  验证: PASS")
                passed += 1
                results.append((module_id, "通过", []))
            else:
                print(f"  验证: FAIL")
                for e in errors:
                    print(f"    - {e}")
                failed += 1
                results.append((module_id, "未通过", errors))
        except Exception as e:
            print(f"  异常: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            results.append((module_id, "异常", [str(e)]))
        print()

    print("=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"  总计: {total} 个模块")
    print(f"  通过: {passed} 个")
    print(f"  失败: {failed} 个")
    print(f"  通过率: {passed/total*100:.1f}%")
    print()

    if failed > 0:
        print("失败模块列表:")
        for module_id, status, errors in results:
            if status != "通过":
                print(f"  {module_id}: {status}")
                for e in errors:
                    print(f"    - {e}")
    else:
        print("所有模块验证通过！")

    print("=" * 70)
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
