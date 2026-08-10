#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD Unified Go Engine V8.0 验证实验
理论依据：六系立系论·定理五十九~六十一·定理六十九
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Go_Unified_Engine import UnifiedGoAI, TraditionalAI, PlayTest

def main():
    print()
    print("=" * 60)
    print("  BSD Unified Go Engine V8.0 验证实验")
    print("  理论依据：六系立系论·定理五十九~六十一·六十九")
    print("=" * 60)
    print()
    
    ai = UnifiedGoAI(auto_connect=True)
    
    print()
    print("开始锦标赛测试...")
    print()
    
    tournament = PlayTest()
    summary, results = tournament.run_tournament(
        ai,
        opponent_strengths=[3, 4, 6, 8],
        games_per_strength=3
    )
    
    print()
    print("=" * 60)
    print("  最终实验结果")
    print("=" * 60)
    
    total_wins = sum(1 for r in results if r['winner'] == 'ai')
    total_games = len(results)
    win_rate = total_wins / total_games * 100
    
    print(f"  总对局: {total_games}")
    print(f"  AI胜局: {total_wins}")
    print(f"  总胜率: {win_rate:.1f}%")
    print()
    
    if win_rate >= 100:
        print("  🎉🎉🎉 100% 胜率达成！")
        print("     验证了六系立系论中围棋工程的理论预测")
        print("     定理五十九~六十一均已通过工程验证")
    elif win_rate >= 80:
        print("  ✅ 高胜率达成，基本验证理论")
    else:
        print("  ⚠️ 胜率待提升，需进一步优化")
    
    print()
    print("  各强度对手胜率:")
    for strength in [3, 4, 6, 8]:
        if strength in summary:
            s = summary[strength]
            print(f"     强度={strength}: {s['wins']}/{s['total']} = {s['win_rate']:.0f}%")
    
    print()
    stats = ai.get_stats()
    print("  引擎统计:")
    print(f"     版本: {stats['version']}")
    print(f"     基因池: {stats['gene_pool']['total_genes']} 个基因")
    print(f"     白日梦落子: {stats['engine']['dream_moves']}")
    print(f"     天道追问: {stats['engine']['tiandao_moves']}")
    
    version_info = ai.get_version_info()
    print()
    print("  集成引擎:", ', '.join(version_info['integrated_engines']))
    print("  核心突破:", version_info['core_breakthrough'])
    print()


if __name__ == '__main__':
    main()