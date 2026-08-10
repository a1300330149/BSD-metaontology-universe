#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V8.1 引擎完备性审计集成测试"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("BSD黑客引擎 V8.1 · 引擎完备性审计验证")
print("=" * 70)

# Step 1: 创建引擎实例
print("\n[Step 1] 创建引擎实例...")
from BSD_Hacker_Bridge_Engine import BSDHackerBridge
engine = BSDHackerBridge()
print("  ✅ 引擎V8.1实例创建成功")

# Step 2: 初始化V8系统
print("\n[Step 2] 初始化V8系统...")
engine.initialize_v8_systems()

# Step 3: 运行引擎完备性审计
print("\n[Step 3] 运行引擎完备性审计...")
audit_result = engine.run_engine_completeness_audit()

if audit_result.get('audit_completed'):
    print(f"\n  ✅ 审计完成: {audit_result.get('report_id')}")
    
    summary = audit_result.get('summary', {})
    print(f"\n  审计汇总:")
    print(f"    公理总数: {summary.get('total_axioms', 'N/A')}")
    print(f"    严重欠债: {summary.get('critical_debts', 'N/A')} 条")
    print(f"    高优先欠债: {summary.get('high_debts', 'N/A')} 条")
    print(f"    审计引擎: {summary.get('total_engines', 'N/A')} 个")
    print(f"    完备引擎: {summary.get('complete_engines', 'N/A')} 个")
    print(f"    理论平均完成度: {summary.get('avg_theory_completion', 0):.0%}")
    print(f"    复合机会: {summary.get('composition_opportunities', 0)} 项")
    
    # 严重欠债详情
    critical = audit_result.get('critical_debts', [])
    if critical:
        print(f"\n  ⚠️ 严重欠债详情 ({len(critical)} 条):")
        for d in critical:
            print(f"    [{d['axiom_id']}] {d['axiom_name']}")
            print(f"      完成度: {d['completion_rate']:.0%}")
            if d['missing_engines']:
                print(f"      缺失引擎: {', '.join(d['missing_engines'][:3])}")
    
    # 复合机会
    opportunities = audit_result.get('composition_opportunities', [])
    if opportunities:
        print(f"\n  💡 复合机会 ({len(opportunities)} 项):")
        for opp in opportunities[:5]:
            print(f"    [{opp['id']}] {opp['goal']}")
            print(f"      引擎: {', '.join(opp['engines'][:4])}")
            print(f"      难度: {opp['difficulty']}")
else:
    print(f"\n  ❌ 审计失败: {audit_result.get('error', '未知错误')}")

# Step 4: 理论欠债清单
print("\n[Step 4] 理论欠债清单...")
debt_list = engine.get_theory_debt_list()

if 'error' not in debt_list:
    print(f"  ✅ 欠债清单生成成功")
    print(f"  公理总数: {debt_list.get('total_axioms', 'N/A')}")
    
    debts_by_level = debt_list.get('debts_by_level', {})
    for level in ['严重欠债', '高优先欠债', '中等欠债', '低优先欠债', '无欠债']:
        if level in debts_by_level:
            print(f"  {level}: {len(debts_by_level[level])} 条")

# Step 5: V8状态
print("\n[Step 5] V8.1系统状态...")
status = engine.get_v8_status()
for name, val in status.items():
    if isinstance(val, bool):
        print(f"  {name}: {'✅' if val else '❌'}")
    elif name == 'protocol_report' and val:
        print(f"  {name}: 已生成")
    else:
        print(f"  {name}: {val}")

print("\n" + "=" * 70)
print("【V8.1引擎完备性审计验证完成】")
print("=" * 70)
print("\n核心发现：")
print("  1. 引擎本质 = 定理的纯系开发 + 复合")
print("  2. 历史欠债：从六系立系论中途开始开发 → 理论未完全引擎化")
print("  3. 审计价值：量化欠债、识别复合机会、指导纯系开发")
print("  4. 闭环路径：理论欠债 → 纯系开发 → 引擎 → 复合 → 完备性验证")