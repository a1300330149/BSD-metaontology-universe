"""最终测试 - 正确同步两个AI的棋盘"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import GoBoard, GoPoint, Stone, BSDMCTSEngine
from katago_gtp_client import StrongGoAI

print("=" * 60)
print("最终测试 - 正确同步版")
print("=" * 60)

board_size = 9
board = GoBoard(board_size)
bsd_engine = BSDMCTSEngine(board_size=board_size, num_simulations=100)
strong_ai = StrongGoAI(board_size=board_size, strength=3)

print(f"棋盘: {board_size}路")
print(f"BSD MCTS: 100次模拟/步")
print()

move_count = 0
max_moves = 81
consecutive_passes = 0

while move_count < max_moves and consecutive_passes < 2:
    # 奇数手：BSD执黑
    if move_count % 2 == 0:
        stone = Stone.BLACK
        point = bsd_engine.select_move(board, stone)
        
        if point and board.is_valid_move(point, stone):
            board.make_move(point, stone)
            strong_ai.play("black", point.to_gtp())  # 同步到StrongAI
            move_str = point.to_gtp()
            consecutive_passes = 0
        else:
            board.pass_move(stone)
            strong_ai.play("black", "PASS")
            move_str = "PASS"
            consecutive_passes += 1

    # 偶数手：StrongAI执白
    else:
        stone = Stone.WHITE
        gtpmove = strong_ai.generate_move("white")
        
        if gtpmove and gtpmove not in ["PASS", "resign"]:
            letters = "ABCDEFGHJKLMNOPQRST"
            if len(gtpmove) >= 2 and gtpmove[0].upper() in letters:
                x = letters.index(gtpmove[0].upper())
                y = int(gtpmove[1:]) - 1
                
                if 0 <= x < board_size and 0 <= y < board_size:
                    point = GoPoint(x, y)
                    
                    if board.is_valid_move(point, stone):
                        board.make_move(point, stone)
                        strong_ai.play("white", gtpmove)  # 同步到StrongAI自己的棋盘
                        move_str = gtpmove
                        consecutive_passes = 0
                    else:
                        board.pass_move(stone)
                        strong_ai.play("white", "PASS")
                        move_str = f"PASS({gtpmove}非法)"
                        consecutive_passes += 1
                else:
                    board.pass_move(stone)
                    strong_ai.play("white", "PASS")
                    move_str = f"PASS({gtpmove}越界)"
                    consecutive_passes += 1
            else:
                board.pass_move(stone)
                strong_ai.play("white", "PASS")
                move_str = "PASS(格式)"
                consecutive_passes += 1
        else:
            board.pass_move(stone)
            strong_ai.play("white", "PASS")
            move_str = "PASS"
            consecutive_passes += 1

    move_count += 1
    icon = "●" if move_count % 2 == 1 else "○"
    player = "BSD" if move_count % 2 == 1 else "StrongAI"
    print(f"{move_count:3d}. {icon} {player:10s} -> {move_str}")

# 结算
board.force_end_game()
score = board.get_score(7.5)
black_score = score.get("black", 0)
white_score = score.get("white", 0)
winner = score.get("winner", "unknown")
margin = score.get("margin", 0)

black_stones = sum(1 for y in range(board.size) for x in range(board.size) if board.board[y][x] == Stone.BLACK)
white_stones = sum(1 for y in range(board.size) for x in range(board.size) if board.board[y][x] == Stone.WHITE)

print()
print("=" * 60)
print("【对局结束】")
print(f"总手数: {move_count}")
print(f"黑棋数: {black_stones} | 白棋数: {white_stones}")
print(f"得分: 黑{black_score:.1f} vs 白{white_score:.1f}")
print(f"胜者: {winner}")
print(f"领先: {margin:.1f}目")
print("=" * 60)
