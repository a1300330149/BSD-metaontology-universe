"""BSD AI vs StrongGoAI 快速测试"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import GoBoard, GoPoint, Stone, BSDMCTSEngine
from katago_gtp_client import StrongGoAI

print("=" * 60)
print("测试BSD AI vs 内置StrongGoAI")
print("=" * 60)

# 初始化
board_size = 9
board = GoBoard(board_size)
bsd_engine = BSDMCTSEngine(board_size=board_size, num_simulations=200)
strong_ai = StrongGoAI(board_size=board_size, strength=3)

print(f"棋盘: {board_size}路")
print(f"BSD MCTS: 200次模拟/步")
print(f"StrongGoAI: 强度3")
print()

# 对弈
move_count = 0
max_moves = 100

while not board.game_over and move_count < max_moves:
    # 奇数手：BSD执黑
    if move_count % 2 == 0:
        stone = Stone.BLACK
        point = bsd_engine.select_move(board, stone)
        if point:
            board.make_move(point, stone)
            move_str = point.to_gtp()
        else:
            board.pass_move(stone)
            move_str = "PASS"
    # 偶数手：StrongAI执白
    else:
        stone = Stone.WHITE
        gtpmove = strong_ai.generate_move("white")
        if gtpmove and gtpmove not in ["PASS", "resign"]:
            letters = "ABCDEFGHJKLMNOPQRST"
            if len(gtpmove) >= 2:
                x = letters.index(gtpmove[0].upper())
                y = int(gtpmove[1:]) - 1
                point = GoPoint(x, y)
                if board.is_valid_move(point, stone):
                    board.make_move(point, stone)
                    move_str = gtpmove
                else:
                    board.pass_move(stone)
                    move_str = "PASS(无效)"
            else:
                board.pass_move(stone)
                move_str = "PASS"
        else:
            board.pass_move(stone)
            move_str = "PASS"

    move_count += 1

    icon = "●" if move_count % 2 == 1 else "○"
    player = "BSD" if move_count % 2 == 1 else "StrongAI"
    print(f"{move_count:3d}. {icon} {player:10s} -> {move_str}")

    if board.consecutive_passes >= 2:
        break

# 结算
score = board.get_score(7.5)
black_score = score.get("black", 0)
white_score = score.get("white", 0)
winner = score.get("winner", "unknown")
margin = score.get("margin", 0)

print()
print("=" * 60)
print("【对局结束】")
print(f"总手数: {move_count}")
print(f"得分: 黑{black_score:.1f} vs 白{white_score:.1f}")
print(f"胜者: {winner}")
print(f"领先: {margin:.1f}目")
print("=" * 60)
