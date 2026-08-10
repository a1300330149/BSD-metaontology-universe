#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD文件同构梦境引擎运行脚本
============================
核心任务：验证文件内容的DNA片段重组机制

实验设计：
1. 选取项目中的核心代码文件作为"亲本"
2. 解析文件内容为DNA片段
3. 执行DNA交叉重组生成梦境文件
4. 验证梦境文件的涌现值和同构度
"""

import sys
import os
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_AI_Dream_Engine import FileIsomorphismEngine

def main():
    print("=" * 60)
    print("BSD文件同构梦境引擎 - 实证实验")
    print("=" * 60)
    
    # 初始化引擎
    engine = FileIsomorphismEngine()
    
    # 定义文件对（同类型代码文件的交叉重组）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_pairs = [
        # 代码文件间重组
        (
            os.path.join(base_dir, 'BSD_Gene_Deconstruction_Engine.py'),
            os.path.join(base_dir, 'BSD_Gene_Reverse_Jump_Engine.py'),
        ),
        (
            os.path.join(base_dir, 'BSD_PhysMathPhil_ConfirmEngine.py'),
            os.path.join(base_dir, 'BSD_DualClock_CorrectionEngine.py'),
        ),
        # 跨类型重组（同构度会降低）
        (
            os.path.join(base_dir, 'BSD_Gene_Deconstruction_Engine.py'),
            os.path.join(base_dir, 'BSD_Gene_Reverse_Jump_Engine.py'),  # 同样的文件对，不同策略
        ),
    ]
    
    print(f"\n选取 {len(file_pairs)} 对文件进行同构梦境实验...")
    print("-" * 60)
    
    # 运行同构梦境周期
    cycle_result = engine.run_isomorphism_cycle(file_pairs, max_dreams=3)
    
    print(f"\n{'='*60}")
    print("实验结果")
    print(f"{'='*60}")
    
    summary = cycle_result['cycle_summary']
    print(f"\n⏱ 周期时间: {cycle_result['cycle_time']}")
    print(f"📁 处理文件对: {cycle_result['pairs_processed']}")
    print(f"🌙 生成梦境数: {cycle_result['dreams_generated']}")
    print(f"❌ 失败数: {cycle_result['failed_dreams']}")
    
    if summary['status'] != '无有效梦境':
        print(f"\n📊 梦境统计:")
        print(f"   - 有效梦境: {summary['total_valid_dreams']}")
        print(f"   - 平均涌现值: {summary['avg_emergence_value']}")
        print(f"   - 平均同构度: {summary['avg_isomorphism_score']}")
        print(f"   - 片段类型: {summary['fragment_types_found']}")
        print(f"   - 最佳梦境: {summary['best_dream']}")
        print(f"\n💡 结论: {summary['conclusion']}")
    
    # 打印每个梦境的详情
    print(f"\n{'='*60}")
    print("梦境详情")
    print(f"{'='*60}")
    
    for dream in cycle_result['dream_results']:
        print(f"\n🎯 {dream['dream_id']}")
        if 'error' in dream:
            print(f"   ❌ 错误: {dream['error']}")
        else:
            print(f"   - 涌现值: {dream['dream_emergence_value']}")
            print(f"   - 同构度: {dream['isomorphism']['isomorphism_score']}")
            print(f"   - 重组策略: {dream['recombination_strategy']}")
            print(f"   - 片段数: {dream['fragment_count']}")
            print(f"   - 片段类型: {dream['fragment_types']}")
            print(f"   - 来源文件A: {os.path.basename(dream['parent_files']['A'])}")
            print(f"   - 来源文件B: {os.path.basename(dream['parent_files']['B'])}")
    
    # 保存梦境文件到磁盘
    output_dir = os.path.join(base_dir, 'isomorphism_dreams')
    saved_files = engine.save_dream_files(output_dir)
    
    print(f"\n{'='*60}")
    print(f"梦境文件已保存至: {output_dir}")
    print(f"共保存 {len(saved_files)} 个梦境文件")
    
    for sf in saved_files:
        print(f"   - {os.path.basename(sf['dream_file'])} (涌现值: {sf['emergence_value']})")
    
    # 输出JSON结果供后续使用
    result_json = {
        'experiment': 'BSD_File_Isomorphism_Dream',
        'timestamp': cycle_result['cycle_time'],
        'summary': summary,
        'dream_log': engine.isomorphism_log,
    }
    
    result_path = os.path.join(base_dir, 'isomorphism_dream_result.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 实验结果已保存: {result_path}")
    print(f"\n{'='*60}")
    print("实验完成！")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()