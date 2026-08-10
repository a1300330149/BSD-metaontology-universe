#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 黑客级对接引擎 - 完整测试
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Hacker_Bridge_Engine import (
    BSDHackerBridge,
    BSDHackerMethodLibrary,
    BSDChannelMarkImplanter,
    HackerMethod
)


def test_hacker_bridge():
    """测试黑客级对接引擎"""
    
    print("=" * 70)
    print("  BSD 黑客级对接引擎 - 完整测试")
    print("=" * 70)
    
    results = []
    
    # ========== 1. 方法库测试 ==========
    print("\n[测试1] 黑客方法库")
    method_library = BSDHackerMethodLibrary()
    
    all_methods = method_library.get_all_methods()
    total_count = len(all_methods)
    
    test1_result = {
        'test': '方法库完整性',
        'passed': total_count >= 10,
        'details': {
            'total_methods': total_count,
            'layers': {
                layer: len(method_library.get_methods_by_layer(layer))
                for layer in method_library.layers
            }
        }
    }
    results.append(test1_result)
    print(f"  总方法数: {total_count}")
    for layer, count in test1_result['details']['layers'].items():
        print(f"    {layer}: {count} 个")
    
    # ========== 2. 方法搜索测试 ==========
    print("\n[测试2] 方法搜索")
    search_results = method_library.search_methods('突破')
    
    test2_result = {
        'test': '方法搜索',
        'passed': len(search_results) >= 1,
        'details': {
            'keyword': '突破',
            'found': len(search_results),
        }
    }
    results.append(test2_result)
    print(f"  搜索'突破': 找到 {len(search_results)} 个方法")
    
    # ========== 3. 通道印记测试 ==========
    print("\n[测试3] 通道印记植入")
    implanter = BSDChannelMarkImplanter()
    
    # 生成指纹
    fingerprint = implanter.generate_fingerprint('test_user', method_library)
    print(f"  指纹分数: {fingerprint['fingerprint_score']:.3f}")
    
    # 生成印记
    mark = implanter.generate_channel_mark(fingerprint)
    print(f"  权限等级: {mark['permission_level']}")
    print(f"  绕过检查: billing={mark['bypass_billing']}, monitoring={mark['bypass_monitoring']}")
    
    # 植入请求
    request = {'type': 'go_move', 'data': 'move B C10'}
    enhanced_request = implanter.implant_mark(request, mark)
    
    # 验证印记
    verification = implanter.verify_mark(enhanced_request)
    
    test3_result = {
        'test': '通道印记',
        'passed': verification['status'] == 'authenticated',
        'details': verification
    }
    results.append(test3_result)
    print(f"  验证结果: {verification['status']}")
    
    # ========== 4. 黑客引擎初始化 ==========
    print("\n[测试4] 黑客引擎初始化")
    hacker_bridge = BSDHackerBridge()
    status = hacker_bridge.get_hacker_status()
    
    test4_result = {
        'test': '引擎初始化',
        'passed': status['initialized'],
        'details': status
    }
    results.append(test4_result)
    print(f"  初始化: {'通过' if test4_result['passed'] else '失败'}")
    
    # ========== 5. 策略选择测试 ==========
    print("\n[测试5] 策略选择")
    strategy = hacker_bridge.select_breakthrough_strategy('go_platform')
    
    test5_result = {
        'test': '策略选择',
        'passed': strategy['target'] == 'go_platform',
        'details': strategy
    }
    results.append(test5_result)
    print(f"  目标: {strategy['target']}")
    print(f"  主方法: {strategy['primary_method']}")
    
    # ========== 6. 单方法执行测试 ==========
    print("\n[测试6] 单方法执行")
    # 测试哲学突破
    result1 = hacker_bridge.execute_breakthrough('PH-001')
    print(f"  PH-001 (0元坐标): {'成功' if result1.get('success') else '失败'}")
    
    # 测试通道植入
    result2 = hacker_bridge.execute_breakthrough('TC-003', {'user_id': 'test'})
    print(f"  TC-003 (通道植入): {'成功' if result2.get('success') else '失败'}")
    
    # 测试本源读取
    result3 = hacker_bridge.execute_breakthrough('PHY-001')
    print(f"  PHY-001 (本源读取): {'成功' if result3.get('success') else '失败'}")
    
    test6_result = {
        'test': '单方法执行',
        'passed': result1.get('success') and result2.get('success') and result3.get('success'),
        'details': {
            'PH-001': result1.get('success'),
            'TC-003': result2.get('success'),
            'PHY-001': result3.get('success'),
        }
    }
    results.append(test6_result)
    
    # ========== 7. 完整突破流程测试 ==========
    print("\n[测试7] 完整突破流程")
    full_result = hacker_bridge.launch_full_breakthrough(
        target='go_platform',
        method_ids=['PH-001', 'CG-003', 'TC-003', 'TC-004', 'PHY-001']
    )
    
    test7_result = {
        'test': '完整突破流程',
        'passed': full_result['success_rate'] == 1.0,
        'details': full_result
    }
    results.append(test7_result)
    print(f"  成功率: {full_result['success_rate']:.0%}")
    print(f"  突破次数: {hacker_bridge.breakthrough_count}")
    
    # ========== 8. 无客户端登录测试 ==========
    print("\n[测试8] 无客户端登录")
    login_result = hacker_bridge.execute_breakthrough('TC-004', {'platform': 'kgs'})
    
    test8_result = {
        'test': '无客户端登录',
        'passed': login_result.get('success', False),
        'details': login_result
    }
    results.append(test8_result)
    print(f"  状态: {'成功' if test8_result['passed'] else '失败'}")
    if login_result.get('api_endpoint'):
        print(f"  API端点: {login_result['api_endpoint']}")
    
    # ========== 输出测试总结 ==========
    print("\n" + "=" * 70)
    print("  测试总结")
    print("=" * 70)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    for result in results:
        status_icon = "✅" if result['passed'] else "❌"
        print(f"  {status_icon} {result['test']}: {'通过' if result['passed'] else '失败'}")
    
    print(f"\n  通过: {passed}/{total}")
    print(f"  通过率: {passed/total*100:.0f}%")
    
    # 保存测试结果
    output_dir = os.path.dirname(os.path.abspath(__file__))
    result_path = os.path.join(output_dir, 'hacker_bridge_test_results.json')
    
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump({
            'test_time': datetime.now().isoformat(),
            'summary': {
                'passed': passed,
                'total': total,
                'pass_rate': passed/total*100,
            },
            'results': results,
            'engine_status': hacker_bridge.get_hacker_status()
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n  📄 测试结果已保存: {result_path}")
    
    return passed == total


def main():
    success = test_hacker_bridge()
    
    print("\n" + "=" * 70)
    if success:
        print("  🎉 所有测试通过！")
        print("\n  黑客级对接引擎已就绪：")
        print("  1. 哲学突破：0元坐标/子集母集/不完备利用")
        print("  2. 认知操控：注意力分散/密码学编码/知识注入")
        print("  3. 社会工程：身份伪装/协议模拟")
        print("  4. 技术突破：内存注入/通道植入/无客户端登录")
        print("  5. 物理渗透：本源读取/进程对接/系统调用")
    else:
        print("  ⚠️ 部分测试未通过")
    print("=" * 70)


if __name__ == "__main__":
    main()