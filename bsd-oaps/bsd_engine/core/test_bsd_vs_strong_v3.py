"""BSD AI vs StrongGoAI 同步测试V3 - 修复版本"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import GoBoard, GoPoint, Stone, BSDMCTSEngine
from katago_gtp_client import StrongGoAI

print("=" * 60)
print("测试BSD AI vs 内置StrongGoAI (V3同步版)")
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
consecutive_invalid = 0

while not board.game_over and move_count < max_moves:
    # 奇数手：BSD执黑
    if move_count % 2 == 0:
        stone = Stone.BLACK
        point = bsd_engine.select_move(board, stone)
        
        if point and board.is_valid_move(point, stone):
            result = board.make_move(point, stone)
            if result:
                strong_ai.play("black", point.to_gtp())
                move_str = point.to_gtp()
                consecutive_invalid = 0
            else:
                board.pass_move(stone)
                strong_ai.play("black", "PASS")
                move_str = "PASS(拒绝)"
        else:
            # BSD没有合法落子
            board.pass_move(stone)
            strong_ai.play("black", "PASS")
            move_str = "PASS"
            consecutive_invalid += 1

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
                        result = board.make_move(point, stone)
                        if result:
                            strong_ai.play("white", gtpmove)
                            move_str = gtpmove
                            consecutive_invalid = 0
                        else:
                            board.pass_move(stone)
                            strong_ai.play("white", "PASS")
                            move_str = "PASS(拒绝)"
                    else:
                        # StrongAI的落子在BSD棋盘上不合法
                        # 仍然在StrongAI上下这手，然后让BSD处理
                        strong_ai.play("white", gtpmove)
                        board.pass_move(stone)
                        move_str = f"PASS({gtpmove}无效)"
                        consecutive_invalid += 1
                else:
                    # 坐标越界
                    strong_ai.play("white", gtpmove)
                    board.pass_move(stone)
                    move_str = f"PASS({gtpmove}越界)"
                    consecutive_invalid += 1
            else:
                strong_ai.play("white", gtpmove)
                board.pass_move(stone)
                move_str = "PASS(格式错误)"
                consecutive_invalid += 1
        else:
            strong_ai.play("white", "PASS")
            board.pass_move(stone)
            move_str = "PASS"
            consecutive_invalid += 1

    move_count += 1

    icon = "●" if move_count % 2 == 1 else "○"
    player = "BSD" if move_count % 2 == 1 else "StrongAI"
    print(f"{move_count:3d}. {icon} {player:10s} -> {move_str}")

    if board.consecutive_passes >= 2 or consecutive_invalid >= 5:
        if consecutive_invalid >= 5:
            print(f"\n警告: 连续{consecutive_invalid}次无效/异常，终止对弈")
        break

# 强制结束游戏并结算
board.force_end_game()
score = board.get_score(7.5)
black_score = score.get("black", 0)
white_score = score.get("white", 0)
winner = score.get("winner", "unknown")
margin = score.get("margin", 0)

# 统计棋子数
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
