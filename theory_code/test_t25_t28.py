"""
T25-T28 模块综合测试脚本
验证所有4个理论模块都能正确导入并通过validate

运行方式：在 Agent_v2 目录下执行 python -m theory_code.test_t25_t28
"""

import sys
import os
import importlib


MODULES = [
    ("T25", "theory_code.theories.t25_fifty_four_dimension_matrix", "FiftyFourDimensionMatrix"),
    ("T26", "theory_code.theories.t26_fifty_four_mother_disciplines", "FiftyFourMotherDisciplines"),
    ("T27", "theory_code.theories.t27_three_interface_systems", "ThreeInterfaceSystems"),
    ("T28", "theory_code.theories.t28_earth_fractal_embedding", "EarthFractalEmbedding"),
]


def run_all_tests():
    print("=" * 70)
    print("T25-T28 理论模块综合测试")
    print("=" * 70)
    print()
    
    total = len(MODULES)
    passed = 0
    failed = 0
    results = []
    
    for module_id, module_path, class_name in MODULES:
        print("--- 测试 " + module_id + " ---")
        try:
            mod = importlib.import_module(module_path)
            module_class = getattr(mod, class_name)
            module = module_class()
            
            print("  模块名称: " + module.module_name)
            print("  版本: " + module.version)
            print("  层级: L" + str(module.cosmic_level))
            print("  依赖: " + str(module.dependencies))
            print("  本源锁定: " + str(module.is_origin_locked))
            print("  锁档哈希: " + str(module.sha256))
            
            valid, errors = module.validate()
            if valid:
                print("  验证: 通过")
                passed += 1
                results.append((module_id, True, []))
            else:
                print("  验证: 失败")
                print("  错误列表:")
                for e in errors:
                    print("    - " + e)
                failed += 1
                results.append((module_id, False, errors))
        except Exception as e:
            print("  异常: " + str(e))
            import traceback
            traceback.print_exc()
            failed += 1
            results.append((module_id, False, [str(e)]))
        print()
    
    print("=" * 70)
    print("测试总结")
    print("=" * 70)
    print("  总模块数: " + str(total))
    print("  通过: " + str(passed))
    print("  失败: " + str(failed))
    print("  通过率: " + str(round(passed/total*100, 1)) + "%")
    print()
    
    if failed == 0:
        print("所有模块测试通过!")
    else:
        print("存在失败模块，请检查错误信息")
    
    return passed == total, results


if __name__ == "__main__":
    success, _ = run_all_tests()
    sys.exit(0 if success else 1)
