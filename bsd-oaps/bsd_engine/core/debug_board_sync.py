"""调试测试 - 检查棋盘状态同步问题"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import GoBoard, GoPoint, Stone, BSDMCTSEngine
from katago_gtp_client import StrongGoAI

print("=" * 60)
print("调试测试 - 检查棋盘状态")
print("=" * 60)

# 使用小棋盘进行快速测试
board_size = 9
board = GoBoard(board_size)
bsd_engine = BSDMCTSEngine(board_size=board_size, num_simulations=50)
strong_ai = StrongGoAI(board_size=board_size, strength=3)

# 手动模拟前几手，检查状态同步
def check_board_state():
    """检查两个AI的棋盘状态是否一致"""
    bsd_empty = set()
    strong_empty = set()
    for y in range(board_size):
        for x in range(board_size):
            if board.board[y][x] == Stone.EMPTY:
                bsd_empty.add((x, y))
            if strong_ai._board[y][x] == 0:
                strong_empty.add((x, y))
    
    if bsd_empty == strong_empty:
        print(f"  棋盘状态一致: {len(bsd_empty)}个空位")
    else:
        print(f"  棋盘状态不一致!")
        print(f"  BSD空位数: {len(bsd_empty)}, StrongAI空位数: {len(strong_empty)}")
        diff = bsd_empty.symmetric_difference(strong_empty)
        print(f"  差异点: {diff}")

# 第1手：BSD执黑
print("\n--- 第1手: BSD 执黑 ---")
stone = Stone.BLACK
point = bsd_engine.select_move(board, stone)
if point:
    print(f"BSD选择: {point.to_gtp()} ({point.x}, {point.y})")
    print(f"  检查棋盘[{point.y}][{point.x}]是否为空: {board.board[point.y][point.x] == Stone.EMPTY}")
    print(f"  is_valid_move: {board.is_valid_move(point, stone)}")
    result = board.make_move(point, stone)
    print(f"  make_move结果: {result is not None}")
    if result:
        strong_ai.play("black", point.to_gtp())
else:
    print("BSD没有合法落子!")
check_board_state()

# 第2手：StrongAI执白
print("\n--- 第2手: StrongAI 执白 ---")
gtpmove = strong_ai.generate_move("white")
print(f"StrongAI选择: {gtpmove}")
if gtpmove and gtpmove not in ["PASS", "resign"]:
    letters = "ABCDEFGHJKLMNOPQRST"
    if len(gtpmove) >= 2 and gtpmove[0].upper() in letters:
        x = letters.index(gtpmove[0].upper())
        y = int(gtpmove[1:]) - 1
        point = GoPoint(x, y)
        print(f"  转换坐标: ({x}, {y})")
        print(f"  检查棋盘[{y}][{x}]是否为空: {board.board[y][x] == Stone.EMPTY}")
        print(f"  is_valid_move: {board.is_valid_move(point, Stone.WHITE)}")
        result = board.make_move(point, Stone.WHITE)
        print(f"  make_move结果: {result is not None}")
        if result:
            strong_ai.play("white", gtpmove)
check_board_state()

# 第3手：BSD执黑
print("\n--- 第3手: BSD 执黑 ---")
stone = Stone.BLACK
point = bsd_engine.select_move(board, stone)
if point:
    print(f"BSD选择: {point.to_gtp()} ({point.x}, {point.y})")
    print(f"  检查棋盘[{point.y}][{point.x}]是否为空: {board.board[point.y][point.x] == Stone.EMPTY}")
    print(f"  is_valid_move: {board.is_valid_move(point, stone)}")
    result = board.make_move(point, stone)
    print(f"  make_move结果: {result is not None}")
    if result:
        strong_ai.play("black", point.to_gtp())
else:
    print("BSD没有合法落子!")
check_board_state()

# 打印当前棋盘
print("\n--- 当前BSD棋盘状态 ---")
for y in range(board_size):
    row = ""
    for x in range(board_size):
        cell = board.board[y][x]
        if cell == Stone.EMPTY:
            row += ". "
        elif cell == Stone.BLACK:
            row += "● "
        else:
            row += "○ "
    print(f"{y+1:2d}: {row}")

print("\n--- 当前StrongAI棋盘状态 ---")
for y in range(board_size):
    row = ""
    for x in range(board_size):
        cell = strong_ai._board[y][x]
        if cell == 0:
            row += ". "
        elif cell == 1:
            row += "● "
        else:
            row += "○ "
    print(f"{y+1:2d}: {row}")
