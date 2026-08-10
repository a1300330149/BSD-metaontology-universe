#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行基因工程反向跃迁引擎
基于现有的基因解构报告执行反向跃迁
"""

import json
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from BSD_Gene_Reverse_Jump_Engine import ReverseJumpEngine

def main():
    # 加载基因解构报告
    report_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body\BSD_Gene_Deconstruction_Report.json'
    
    with open(report_path, 'r', encoding='utf-8') as f:
        deconstruction_report = json.load(f)
    
    print("=" * 80)
    print("BSD基因工程反向跃迁引擎·实证验证")
    print("=" * 80)
    
    # 初始化引擎
    engine = ReverseJumpEngine()
    
    # 执行反向跃迁
    print("\n[Step 1] 执行反向跃迁流程...")
    jump_report = engine.execute_reverse_jump(deconstruction_report)
    
    print("\n[Step 2] 跃迁结果概览")
    print("-" * 60)
    print(f"  跃迁ID: {jump_report['jump_id']}")
    print(f"  捕获忽悠现象: {jump_report['jump_summary']['total_phenomena']} 个")
    print(f"    - CRITICAL: {jump_report['jump_summary']['critical_phenomena']} 个")
    print(f"    - HIGH: {jump_report['jump_summary']['high_phenomena']} 个")
    print(f"  生成理论修正: {jump_report['jump_summary']['total_corrections']} 项")
    print(f"    - 边界修正: {jump_report['jump_summary']['boundary_corrections']} 项")
    print(f"    - 权重修正: {jump_report['jump_summary']['weight_corrections']} 项")
    print(f"    - 公理补全: {jump_report['jump_summary']['axiom_completions']} 项")
    
    print("\n[Step 3] 跃迁判定")
    print("-" * 60)
    verdict = jump_report['jump_verdict']
    print(f"  跃迁结论: {verdict['verdict']}")
    print(f"  成功率: {verdict['success_rate']}")
    print(f"  理论演化: {verdict['theory_evolution']}")
    
    print("\n[Step 4] 捕获的忽悠现象详情")
    print("-" * 60)
    for p in jump_report['captured_phenomena']:
        print(f"\n  [{p['severity']}] {p['id']}: {p['name']}")
        print(f"    {p['description']}")
        print(f"    跃迁潜力: {p['jump_potential']}")
    
    print("\n[Step 5] 理论修正详情")
    print("-" * 60)
    for c in jump_report['theory_corrections']:
        print(f"\n  {c['id']} [{c['type']}]:")
        if 'original_theory' in c:
            print(f"    原理论: {c['original_theory']}")
            print(f"    修正后: {c['corrected_theory']}")
        elif 'original_weights' in c:
            print(f"    原权重: {c['original_weights']}")
            print(f"    修正后权重: {c['corrected_weights']}")
        print(f"    数学表达: {c['mathematical_formulation']}")
    
    # 保存跃迁报告
    output_path = os.path.join(os.path.dirname(__file__), 'BSD_Gene_Reverse_Jump_Report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(jump_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[Step 6] 报告已保存: {output_path}")
    
    # 生成文档
    print("\n[Step 7] 生成理论文档...")
    jump_doc = engine.generate_jump_document()
    doc_path = os.path.join(os.path.dirname(__file__), 'BSD_Gene_Reverse_Jump_Document.md')
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(jump_doc)
    
    print(f"  文档已保存: {doc_path}")
    
    print("\n" + "=" * 80)
    print("反向跃迁完成！")
    print("=" * 80)
    
    return jump_report

if __name__ == '__main__':
    main()
