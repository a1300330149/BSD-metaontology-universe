import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from BSD_Go_Unified_Engine import *

output = run_learning_then_experiment()

print('\n\n===== 完整结果汇总 =====')
print(f"胜场: 统一AI={output['game_results']['unified_win']}, 传统AI={output['game_results']['traditional_win']}, 和棋={output['game_results']['draw']}")
print(f"胜率: {output['win_rate']:.1f}%")
print(f"基因库: {output['final_stats']['gene_pool']['total_genes']} 个基因")