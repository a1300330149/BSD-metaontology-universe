#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：分析AI和对手的落子差异
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Go_Unified_Engine import UnifiedGoAI, TraditionalAI, UnifiedBoard

def debug_game():
    """调试一局对弈"""
    print()
    print("=" * 60)
    print("  调试模式：AI vs TraditionalAI-S3")
    print("=" * 60)
    print()
    
    ai = UnifiedGoAI(auto_connect=False)
    opponent = TraditionalAI(strength=3)
    board = UnifiedBoard(9)
    
    print("初始棋盘:")
    board.display()
    print()
    
    for move_num in range(10):
        # AI落子
        ai_move = ai.decide_move(board, 1)
        if ai_move:
            board.place(*ai_move)
            print(f"手{move_num*2+1}: AI(黑) 落子 {ai_move}")
        else:
            print(f"手{move_num*2+1}: AI 无棋可下")
            break
        
        # 对手落子
        opp_move = opponent.decide(board, 2)
        if opp_move:
            board.place(*opp_move)
            print(f"手{move_num*2+2}: 对手(白) 落子 {opp_move}")
        else:
            print(f"手{move_num*2+2}: 对手 无棋可下")
            break
    
    print()
    print("当前棋盘状态:")
    board.display()
    
    print(f"\n当前得分: {board.score()}")
    
    # 分析AI的评估函数
    print("\n" + "=" * 60)
    print("  AI评估分析")
    print("=" * 60)
    
    ai_player = 1
    opponent_player = 2
    
    # 分析AI可能选择的前5个最佳落子
    empty = board.empty()
    evaluations = []
    
    for x, y in empty[:20]:
        score = ai.engine._simple_eval(board, x, y, ai_player)
        evaluations.append({
            'move': (x, y),
            'score': score,
        })
    
    evaluations.sort(key=lambda e: e['score'], reverse=True)
    
    print("\nAI评估的Top 5落子:")
    for i, ev in enumerate(evaluations[:5]):
        print(f"  {i+1}. 位置{ev['move']}: 得分={ev['score']:.4f}")
    
    # 分析对手的评估函数
    print("\n对手评估的Top 5落子:")
    opp_evaluations = []
    
    for x, y in empty[:20]:
        score = opponent._basic_eval(board, x, y, opponent_player)
        opp_evaluations.append({
            'move': (x, y),
            'score': score,
        })
    
    opp_evaluations.sort(key=lambda e: e['score'], reverse=True)
    
    for i, ev in enumerate(opp_evaluations[:5]):
        print(f"  {i+1}. 位置{ev['move']}: 得分={ev['score']:.4f}")
    
    print()
    
    # 对比分析
    ai_top3 = [e['move'] for e in evaluations[:3]]
    opp_top3 = [e['move'] for e in opp_evaluations[:3]]
    
    overlap = set(ai_top3) & set(opp_top3)
    print(f"AI和对手Top3落子重叠: {len(overlap)} 个")
    print(f"AI Top3: {ai_top3}")
    print(f"对手 Top3: {opp_top3}")
    
    print()
    
    # 模拟更多手
    print("=" * 60)
    print("  完整对弈模拟")
    print("=" * 60)
    
    board2 = UnifiedBoard(9)
    move_count = 0
    ai_score = 0
    opp_score = 0
    
    while move_count < 81:
        ai_move = ai.decide_move(board2, 1)
        if ai_move is None:
            break
        board2.place(*ai_move)
        move_count += 1
        
        opp_move = opponent.decide(board2, 2)
        if opp_move is None:
            break
        board2.place(*opp_move)
        move_count += 1
    
    print(f"\n总手数: {move_count}")
    
    # 计算得分
    for x in range(9):
        for y in range(9):
            if board2.board[x][y] == 1:
                ai_score += 1
            elif board2.board[x][y] == 2:
                opp_score += 1
            else:
                ai_score += 0.5
                opp_score += 0.5
    
    opp_score += 7.5  # 贴目
    print(f"AI得分: {ai_score:.1f}")
    print(f"对手得分(含贴目): {opp_score:.1f}")
    
    if ai_score > opp_score:
        print("🎉 AI获胜！")
    else:
        print("💀 AI失败")
    
    # 分析AI的评估逻辑
    print()
    print("=" * 60)
    print("  AI评估函数验证")
    print("=" * 60)
    
    # 在空棋盘上测试
    empty_board = UnifiedBoard(9)
    center = 4
    
    print("\n在空棋盘上对不同位置的评估:")
    test_positions = [
        (center, center, "天元"),
        (center-1, center, "星位左"),
        (center, center-1, "星位上"),
        (center-2, center-2, "高目"),
        (0, 0, "角部"),
        (1, 1, "小目"),
    ]
    
    for x, y, name in test_positions:
        score = ai.engine._simple_eval(empty_board, x, y, 1)
        opp_score_val = opponent._basic_eval(empty_board, x, y, 2)
        print(f"  {name}({x},{y}): AI评估={score:.4f}, 对手评估={opp_score_val:.4f}")


if __name__ == '__main__':
    debug_game()