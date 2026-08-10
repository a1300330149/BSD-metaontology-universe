import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from BSD_Go_Quantum_Dream_Engine import *

metrics = run_learning_mode()

print('\n\n===== 学习指标汇总 =====')
for k, v in metrics.items():
    print(f'  {k}: {v}')