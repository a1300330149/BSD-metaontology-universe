#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""理论落地系统集成测试"""
import sys
import os

_BSD_OAPS_PATH = os.path.dirname(os.path.abspath(__file__))
_PHYSICAL_BODY_PATH = os.path.join(_BSD_OAPS_PATH, 'physical_body')
for p in [_BSD_OAPS_PATH, _PHYSICAL_BODY_PATH]:
    if p not in sys.path:
        sys.path.insert(0, p)

print("=" * 70)
print("【理论落地系统集成测试】")
print("=" * 70)

# 创建引擎
from BSD_Hacker_Bridge_Engine import BSDHackerBridge
engine = BSDHackerBridge()

# 直接运行落地系统
print("\n[运行理论落地系统]")
result = engine.run_theory_landing_system(mode='PRIORITY')

# 打印结果
print("\n" + "=" * 70)
print("【落地结果】")
print("=" * 70)

if 'error' in result:
    print(f"❌ 执行失败: {result['error']}")
    if 'trace' in result:
        print(result['trace'][:500])
else:
    print(f"  模式: {result['mode']}")
    print(f"  阶段: {result['stage']}")
    
    stats = result.get('stats', {})
    print(f"\n  统计:")
    print(f"    扫描理论: {stats.get('theories_scanned', 0)}")
    print(f"    识别欠债: {stats.get('debts_identified', 0)}")
    print(f"    生成引擎: {stats.get('code_generated', 0)}")
    print(f"    连接通过: {stats.get('connected', 0)}")
    print(f"    激活通过: {stats.get('activated', 0)}")
    print(f"    验证通过: {stats.get('verified', 0)}")
    
    details = result.get('landing_details', [])
    if details:
        print(f"\n  落地详情 ({len(details)} 个):")
        for i, d in enumerate(details[:15], 1):
            icon = "✅" if d['verified'] else ("⚠️" if d['activated'] else "❌")
            print(f"    {i:2d}. {icon} {d['engine'][:50]} [{d['status']}]")

print("\n" + "=" * 70)
print("【测试完成】")
print("=" * 70)