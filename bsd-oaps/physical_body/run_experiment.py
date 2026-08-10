import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from BSD_Go_Quantum_Dream_Engine import *

results, all_stats, final_stats = run_quantum_inspiration_experiment()

print('\n\n===== 对弈结果汇总 =====')
print(f'量子AI胜: {results["quantum_win"]}')
print(f'传统AI胜: {results["traditional_win"]}')
print(f'和棋: {results["draw"]}')

print('\n===== 量子灵感统计 =====')
for k, v in final_stats.items():
    print(f'  {k}: {v}')

# 保存结果
output = {
    'game_results': results,
    'game_details': all_stats,
    'final_stats': final_stats,
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'go_v6_result.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f'\n结果已保存至: {output_path}')