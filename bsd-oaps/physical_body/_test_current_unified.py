#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速测试当前统一引擎的胜率"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Go_Unified_Engine import UnifiedGoAI, UnifiedBoard, TraditionalAI, PlayTest

def main():
    print("=" * 50)
    print("  当前统一引擎快速测试")
    print("=" * 50)
    
    ai = UnifiedGoAI(auto_connect=False)
    
    # 测试不同强度对手
    for strength in [3, 4, 6, 8]:
        opponent = TraditionalAI(strength=strength)
        wins = 0
        total = 3
        
        for i in range(total):
            result = PlayTest().play_game(
                ai, opponent, 
                board_size=9, 
                komi=7.5, 
                ai_first=(i % 2 == 0)
            )
            if result['winner'] == 'ai':
                wins += 1
            print(f"  强度={strength} 第{i+1}局: {result['winner']} ({result['ai_score']:.1f} vs {result['opponent_score']:.1f})")
        
        win_rate = wins / total * 100
        print(f"  => 胜率: {wins}/{total} = {win_rate:.0f}%")
        print()
    
    print("=" * 50)
    print("  引擎统计:")
    stats = ai.get_stats()
    print(f"    版本: {stats['version']}")
    print(f"    基因池: {stats['gene_pool']['total_genes']} 个基因")
    print(f"    总落子: {stats['total_moves']}")

if __name__ == '__main__':
    main()
