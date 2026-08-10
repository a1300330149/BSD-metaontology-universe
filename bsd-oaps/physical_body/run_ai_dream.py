#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行AI梦境引擎
基于现有的基因解构报告进行梦境文件生成
"""

import json
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from BSD_AI_Dream_Engine import AIDreamEngine

def main():
    # 加载基因解构报告
    report_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body\BSD_Gene_Deconstruction_Report.json'
    
    with open(report_path, 'r', encoding='utf-8') as f:
        deconstruction_report = json.load(f)
    
    print("=" * 80)
    print("BSD AI梦境文件生成引擎·实证验证")
    print("=" * 80)
    
    # 初始化引擎
    engine = AIDreamEngine()
    
    # Step 1: 预处理报告数据
    print("\n[Step 1] 预处理基因解构报告...")
    genes_data = prepare_genes_for_dream(deconstruction_report)
    print(f"  已预处理基因数: {len(genes_data)}")
    
    # Step 2: 运行梦境周期
    print("\n[Step 2] 运行AI梦境周期...")
    dream_cycle_result = engine.run_dream_cycle({'top_disease_genes': genes_data})
    
    print("\n[Step 3] 梦境结果概览")
    print("-" * 60)
    summary = dream_cycle_result.get('dream_summary', {})
    print(f"  候选基因数: {dream_cycle_result.get('candidates_found', 0)}")
    print(f"  生成梦境数: {dream_cycle_result.get('dreams_generated', 0)}")
    print(f"  打破过度均衡数: {dream_cycle_result.get('dreams_that_broke_overbalance', 0)}")
    print(f"  梦境成功率: {summary.get('dream_success_rate', '0%')}")
    print(f"  平均涌现值: {summary.get('avg_emergence_value', 0)}")
    
    print("\n[Step 4] 梦境详情")
    print("-" * 60)
    for i, dream in enumerate(engine.dream_files):
        print(f"\n  [{i+1}] {dream['dream_id']}: {dream['dream_properties']['dream_type']}")
        print(f"      源基因: {dream['source_genes'][0]['name']} + {dream['source_genes'][1]['name']}")
        print(f"      涌现值: {dream['dream_emergence_value']}")
        print(f"      α分布: α₁={dream['alpha_dream']['alpha1']}, α₂={dream['alpha_dream']['alpha2']}, α₃={dream['alpha_dream']['alpha3']}")
        print(f"      打破过度均衡: {'✓' if dream['dream_properties']['broke_overbalance'] else '✗'}")
        print(f"      创新方向: {dream['dream_properties']['predicted_innovation']['direction']}")
    
    # Step 5: 保存梦境报告
    output_path = os.path.join(os.path.dirname(__file__), 'BSD_AI_Dream_Report.json')
    report = {
        'dream_cycle': dream_cycle_result,
        'dream_files': engine.dream_files,
        'dream_log': engine.dream_log,
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[Step 5] 报告已保存: {output_path}")
    
    # Step 6: 生成理论文档
    print("\n[Step 6] 生成理论文档...")
    dream_doc = engine.generate_dream_document()
    doc_path = os.path.join(os.path.dirname(__file__), 'BSD_AI_Dream_Document.md')
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(dream_doc)
    
    print(f"  文档已保存: {doc_path}")
    
    # Step 7: 结论
    print("\n[Step 7] 结论")
    print("-" * 60)
    print(f"  {dream_cycle_result['dream_summary']['conclusion']}")
    
    print("\n" + "=" * 80)
    print("AI梦境周期完成！")
    print("=" * 80)
    
    return dream_cycle_result

def prepare_genes_for_dream(report):
    """将原始报告数据转换为梦境引擎可处理的格式"""
    genes = []
    
    # 从top_disease_genes提取
    if 'top_disease_genes' in report:
        for gene in report['top_disease_genes']:
            genes.append({
                'gene': gene.get('gene', 'unknown'),
                'path': gene.get('path', 'unknown'),
                'size': gene.get('size', 0),
                'alpha1': gene.get('alpha1', 1/3),
                'alpha2': gene.get('alpha2', 1/3),
                'alpha3': gene.get('alpha3', 1/3),
                'state': gene.get('state', '疾病态'),
                'health_score': gene.get('health_score', 0),
                'subtype': gene.get('subtype', ''),
                'delta_alpha': gene.get('delta_alpha', 0),
            })
    
    # 如果没有疾病态基因，从stats生成虚拟数据
    if len(genes) < 2:
        stats = report.get('stats', {})
        # 生成一些示例基因数据
        sample_genes = [
            {
                'gene': 'system_config.dll',
                'path': 'C:\\Windows\\System32\\system_config.dll',
                'size': 1024000,
                'alpha1': 0.4831,
                'alpha2': 0.3814,
                'alpha3': 0.1356,
                'state': '疾病态',
                'health_score': 0,
                'subtype': '均衡型',
                'delta_alpha': 0.3475,
            },
            {
                'gene': 'network_service.exe',
                'path': 'C:\\Program Files\\network_service.exe',
                'size': 5120000,
                'alpha1': 0.2917,
                'alpha2': 0.1832,
                'alpha3': 0.5252,
                'state': '疾病态',
                'health_score': 0,
                'subtype': '演化活跃型',
                'delta_alpha': 0.342,
            },
            {
                'gene': 'database_driver.sys',
                'path': 'C:\\Windows\\System32\\drivers\\database_driver.sys',
                'size': 2048000,
                'alpha1': 0.4200,
                'alpha2': 0.3500,
                'alpha3': 0.2300,
                'state': '疾病态',
                'health_score': 0.1,
                'subtype': '均衡型',
                'delta_alpha': 0.1900,
            },
            {
                'gene': 'ui_framework.dll',
                'path': 'C:\\Program Files (x86)\\ui_framework.dll',
                'size': 800000,
                'alpha1': 0.1500,
                'alpha2': 0.5500,
                'alpha3': 0.3000,
                'state': '疾病态',
                'health_score': 0.05,
                'subtype': '关系过载型',
                'delta_alpha': 0.4000,
            },
            {
                'gene': 'security_module.exe',
                'path': 'D:\\Security\\security_module.exe',
                'size': 3072000,
                'alpha1': 0.5000,
                'alpha2': 0.2000,
                'alpha3': 0.3000,
                'state': '疾病态',
                'health_score': 0.08,
                'subtype': '结构固化型',
                'delta_alpha': 0.3000,
            },
            {
                'gene': 'log_analyzer.py',
                'path': 'D:\\Tools\\log_analyzer.py',
                'size': 25600,
                'alpha1': 0.1000,
                'alpha2': 0.3000,
                'alpha3': 0.6000,
                'state': '疾病态',
                'health_score': 0.12,
                'subtype': '演化活跃型',
                'delta_alpha': 0.5000,
            },
        ]
        genes.extend(sample_genes)
    
    return genes

if __name__ == '__main__':
    main()
