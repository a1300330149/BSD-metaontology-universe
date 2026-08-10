#!/usr/bin/env python3
"""快速运行验证并提取关键指标"""
import os, sys, json

agent_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2'
physical_path = os.path.join(agent_path, 'bsd-oaps', 'physical_body')
os.chdir(physical_path)
sys.path.insert(0, physical_path)

from bsd_v23_validator import BSDV23Validator

print('正在运行验证引擎...')
validator = BSDV23Validator()
results = validator.run_full_validation()

# 保存完整结果
with open('repair_validation_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 提取关键指标
soc = results.get('phases', {}).get('G_SOC', {})
summary = results.get('summary', {})

print('\n' + '=' * 60)
print('修复后关键指标')
print('=' * 60)

soc_score = soc.get('SOC实证计算', {}).get('综合评估', {}).get('SOC综合得分', 'N/A')
print(f'SOC序参量: {soc_score}')

fractal = soc.get('分形维度计算', {}).get('综合分形维度', 'N/A')
print(f'分形维度: {fractal}')

edges = soc.get('引用网络拓扑分析', {}).get('边数', 'N/A')
print(f'引用边数: {edges}')

density = soc.get('引用网络拓扑分析', {}).get('密度', 'N/A')
print(f'网络密度: {density}')

print(f'总评级: {summary.get("总体评级", "N/A")}')
print(f'忽悠现象: {len(results.get("hongxuan", []))} 个')

print('\n报告已保存: repair_validation_result.json')
