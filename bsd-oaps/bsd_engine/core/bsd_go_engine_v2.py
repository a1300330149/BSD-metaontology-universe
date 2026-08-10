"""
BSD围棋AI引擎 V2.0 - 六系协同 + MCTS
============================================
基于BSD六系立系论的围棋AI引擎升级版，核心改进：
1. 蒙特卡洛树搜索(MCTS)：深度搜索变化
2. 六系坐标映射：围棋状态→六系空间锚点
3. 权重动态调配：α₁个体性 + α₂关系性 + α₃变化性
4. 天道系追问：超越计算的棋道意义
5. 启发式评估：基于棋理的局面评估

版本：V2.0 · 2026-08-02
"""

import math
import json
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, defaultdict
import copy
import time


# ============================================================================
# 1. 基础数据结构
# ============================================================================

class Stone(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class GamePhase(Enum):
    OPENING = "opening"
    MIDDLE = "middle"
    ENDGAME = "endgame"


@dataclass
class GoPoint:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, GoPoint):
            return self.x == other.x and self.y == other.y
        return False

    def to_gtp(self) -> str:
        letters = 'ABCDEFGHJKLMNOPQRST'
        return letters[self.x] + str(self.y + 1)


@dataclass
class Move:
    point: GoPoint
    stone: Stone
    move_number: int
    captured: int = 0
    is_ko: bool = False


# ============================================================================
# 2. 围棋棋盘
# ============================================================================

class GoBoard:
    """围棋棋盘"""

    def __init__(self, size: int = 19):
        self.size = size
        self.board = [[Stone.EMPTY for _ in range(size)] for _ in range(size)]
        self.move_history: List[Move] = []
        self.current_player = Stone.BLACK
        self.ko_point: Optional[GoPoint] = None
        self.consecutive_passes = 0
        self.game_over = False

    def clone(self) -> 'GoBoard':
        new_board = GoBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.move_history = self.move_history.copy()
        new_board.current_player = self.current_player
        new_board.ko_point = self.ko_point
        new_board.consecutive_passes = self.consecutive_passes
        new_board.game_over = self.game_over
        return new_board

    def get_neighbors(self, point: GoPoint) -> List[GoPoint]:
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = point.x + dx, point.y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append(GoPoint(nx, ny))
        return neighbors

    def get_group(self, point: GoPoint) -> Tuple[List[GoPoint], List[GoPoint]]:
        color = self.board[point.y][point.x]
        if color == Stone.EMPTY:
            return [], []

        group = []
        liberties = set()
        visited = set()
        queue = deque([point])

        while queue:
            p = queue.popleft()
            if p in visited:
                continue
            visited.add(p)
            group.append(p)

            for neighbor in self.get_neighbors(p):
                if self.board[neighbor.y][neighbor.x] == Stone.EMPTY:
                    liberties.add(neighbor)
                elif self.board[neighbor.y][neighbor.x] == color and neighbor not in visited:
                    queue.append(neighbor)

        return group, list(liberties)

    def is_valid_move(self, point: GoPoint, stone: Stone) -> bool:
        if self.game_over:
            return False
        if self.board[point.y][point.x] != Stone.EMPTY:
            return False
        if self.ko_point and point == self.ko_point:
            return False

        test_board = self.clone()
        test_board.board[point.y][point.x] = stone

        opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        captured = 0
        for neighbor in self.get_neighbors(point):
            if test_board.board[neighbor.y][neighbor.x] == opponent:
                _, libs = test_board.get_group(neighbor)
                if len(libs) == 0:
                    group, _ = test_board.get_group(neighbor)
                    captured += len(group)

        if captured > 0:
            return True

        _, own_libs = test_board.get_group(point)
        return len(own_libs) > 0

    def make_move(self, point: GoPoint, stone: Stone) -> Optional[Move]:
        if not self.is_valid_move(point, stone):
            return None

        self.board[point.y][point.x] = stone
        opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        captured = 0
        captured_points = []

        for neighbor in self.get_neighbors(point):
            if self.board[neighbor.y][neighbor.x] == opponent:
                group, libs = self.get_group(neighbor)
                if len(libs) == 0:
                    captured_points.extend(group)
                    captured += len(group)

        for cp in captured_points:
            self.board[cp.y][cp.x] = Stone.EMPTY

        if captured == 1:
            _, own_libs = self.get_group(point)
            if len(own_libs) == 1:
                self.ko_point = own_libs[0]
            else:
                self.ko_point = None
        else:
            self.ko_point = None

        self.current_player = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        self.consecutive_passes = 0

        move = Move(
            point=point,
            stone=stone,
            move_number=len(self.move_history) + 1,
            captured=captured,
            is_ko=self.ko_point is not None
        )
        self.move_history.append(move)
        return move

    def pass_move(self, stone: Stone) -> bool:
        self.consecutive_passes += 1
        self.current_player = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        self.ko_point = None
        if self.consecutive_passes >= 2:
            self.game_over = True
        return True

    def get_game_phase(self) -> GamePhase:
        move_count = len(self.move_history)
        if move_count <= 60:
            return GamePhase.OPENING
        elif move_count <= 150:
            return GamePhase.MIDDLE
        else:
            return GamePhase.ENDGAME

    def get_score(self, komi: float = 7.5) -> Dict:
        black_stones = sum(1 for y in range(self.size) for x in range(self.size) if self.board[y][x] == Stone.BLACK)
        white_stones = sum(1 for y in range(self.size) for x in range(self.size) if self.board[y][x] == Stone.WHITE)

        black_territory = self._count_territory(Stone.BLACK)
        white_territory = self._count_territory(Stone.WHITE)

        black_total = black_stones + black_territory
        white_total = white_stones + white_territory + komi

        if black_total > white_total:
            return {"black": black_total, "white": white_total, "winner": "black", "margin": black_total - white_total}
        elif white_total > black_total:
            return {"black": black_total, "white": white_total, "winner": "white", "margin": white_total - black_total}
        else:
            return {"black": black_total, "white": white_total, "winner": "draw", "margin": 0}

    def force_end_game(self):
        """强制结束游戏，用于测试"""
        self.game_over = True

    def _count_territory(self, color: Stone) -> int:
        territory = 0
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == Stone.EMPTY:
                    neighbors = self.get_neighbors(GoPoint(x, y))
                    has_black = any(self.board[n.y][n.x] == Stone.BLACK for n in neighbors)
                    has_white = any(self.board[n.y][n.x] == Stone.WHITE for n in neighbors)
                    if color == Stone.BLACK and has_black and not has_white:
                        territory += 1
                    elif color == Stone.WHITE and has_white and not has_black:
                        territory += 1
        return territory

    def get_empty_points(self) -> List[GoPoint]:
        points = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == Stone.EMPTY:
                    points.append(GoPoint(x, y))
        return points


# ============================================================================
# 3. MCTS节点
# ============================================================================

@dataclass
class MCTSNode:
    """蒙特卡洛树搜索节点"""
    board: GoBoard
    stone: Stone
    point: Optional[GoPoint] = None
    parent: Optional['MCTSNode'] = None
    children: List['MCTSNode'] = field(default_factory=list)
    visits: int = 0
    wins: float = 0.0
    untried_moves: List[GoPoint] = field(default_factory=list)
    prior: float = 1.0

    def __post_init__(self):
        if not self.untried_moves and self.board:
            self.untried_moves = self._get_legal_moves()

    def _get_legal_moves(self) -> List[GoPoint]:
        moves = []
        empty = self.board.get_empty_points()
        for point in empty:
            if self.board.is_valid_move(point, self.stone):
                moves.append(point)
        return moves[:20]  # 限制候选数

    def ucb1(self, exploration: float = 1.414) -> float:
        if self.visits == 0:
            return float('inf')
        win_rate = self.wins / self.visits
        exploration_term = exploration * math.sqrt(math.log(self.parent.visits) / self.visits)
        return win_rate + exploration_term

    def best_child(self, exploration: float = 1.414) -> 'MCTSNode':
        if not self.children:
            return self
        return max(self.children, key=lambda c: c.ucb1(exploration))

    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        return self.board.game_over or len(self.untried_moves) == 0 and not self.children


# ============================================================================
# 4. 启发式评估
# ============================================================================

class HeuristicEvaluator:
    """启发式局面评估器"""

    @staticmethod
    def evaluate(board: GoBoard, stone: Stone) -> float:
        """评估局面对指定颜色的价值 (-1 到 1)"""
        score = 0.0

        # 1. 棋子数量对比
        own_stones = sum(1 for y in range(board.size) for x in range(board.size) if board.board[y][x] == stone)
        opp_stones = sum(1 for y in range(board.size) for x in range(board.size) if board.board[y][x] != stone and board.board[y][x] != Stone.EMPTY)
        total = own_stones + opp_stones
        if total > 0:
            score += 0.3 * (own_stones - opp_stones) / total

        # 2. 气数评估
        own_libs = HeuristicEvaluator._count_total_liberties(board, stone)
        opp_stone = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        opp_libs = HeuristicEvaluator._count_total_liberties(board, opp_stone)
        if own_libs + opp_libs > 0:
            score += 0.2 * (own_libs - opp_libs) / (own_libs + opp_libs)

        # 3. 领地评估
        own_territory = board._count_territory(stone)
        opp_territory = board._count_territory(opp_stone)
        if own_territory + opp_territory > 0:
            score += 0.3 * (own_territory - opp_territory) / (own_territory + opp_territory)

        # 4. 位置价值
        score += 0.2 * HeuristicEvaluator._position_value(board, stone)

        return max(-1.0, min(1.0, score))

    @staticmethod
    def _count_total_liberties(board: GoBoard, stone: Stone) -> int:
        total_libs = 0
        visited = set()
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] == stone and GoPoint(x, y) not in visited:
                    group, libs = board.get_group(GoPoint(x, y))
                    for p in group:
                        visited.add(p)
                    total_libs += len(libs)
        return total_libs

    @staticmethod
    def _position_value(board: GoBoard, stone: Stone) -> float:
        center = board.size / 2
        value = 0.0
        count = 0

        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] == stone:
                    dist_center = abs(x - center) + abs(y - center)
                    max_dist = 2 * center
                    center_val = 1.0 - dist_center / max_dist
                    value += center_val
                    count += 1

        return value / count if count > 0 else 0.0


# ============================================================================
# 5. 六系围棋映射
# ============================================================================

@dataclass
class LiuHeCoordinate:
    qh: float = 0.0
    zr: float = 0.0
    jx: float = 0.0
    bs: float = 0.0
    sh: float = 0.0
    td: float = 0.0

    def to_vector(self) -> List[float]:
        return [self.qh, self.zr, self.jx, self.bs, self.sh, self.td]

    def dominant_system(self) -> str:
        systems = {'强化系': self.qh, '自然系': self.zr, '具现系': self.jx,
                   '变身系': self.bs, '社会系': self.sh, '天道系': self.td}
        return max(systems, key=systems.get)


class LiuHeMapper:
    """围棋→六系映射器"""

    @staticmethod
    def map(board: GoBoard, stone: Stone) -> LiuHeCoordinate:
        qh = LiuHeMapper._qh(board, stone)
        zr = LiuHeMapper._zr(board, stone)
        jx = LiuHeMapper._jx(board, stone)
        bs = LiuHeMapper._bs(board, stone)
        sh = LiuHeMapper._sh(board, stone)
        td = LiuHeMapper._td(board, stone)
        return LiuHeCoordinate(qh=qh, zr=zr, jx=jx, bs=bs, sh=sh, td=td)

    @staticmethod
    def _qh(board, stone):
        total = board.size ** 2
        own = sum(1 for y in range(board.size) for x in range(board.size) if board.board[y][x] == stone)
        return min(1.0, own / total * 2)

    @staticmethod
    def _zr(board, stone):
        own_points = [(x, y) for y in range(board.size) for x in range(board.size) if board.board[y][x] == stone]
        if not own_points:
            return 0.5
        star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        score = 0
        for px, py in own_points:
            for cx, cy in star_points:
                dist = abs(px - cx) + abs(py - cy)
                if dist <= 2:
                    score += 1.0 / (1.0 + dist)
        return min(1.0, score / len(own_points))

    @staticmethod
    def _jx(board, stone):
        valid = sum(1 for y in range(board.size) for x in range(board.size)
                    if board.is_valid_move(GoPoint(x, y), stone))
        return min(1.0, valid / (board.size ** 2) * 3)

    @staticmethod
    def _bs(board, stone):
        lib_counts = []
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] == stone:
                    _, libs = board.get_group(GoPoint(x, y))
                    lib_counts.append(len(libs))
        if not lib_counts:
            return 0.5
        return min(1.0, len(set(lib_counts)) / 6.0)

    @staticmethod
    def _sh(board, stone):
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        opp_libs = []
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] == opp:
                    _, libs = board.get_group(GoPoint(x, y))
                    opp_libs.append(len(libs))
        if not opp_libs:
            return 0.5
        return max(0.0, min(1.0, 1.0 - sum(opp_libs) / len(opp_libs) / 5.0))

    @staticmethod
    def _td(board, stone):
        phase = board.get_game_phase()
        move_count = len(board.move_history)
        weights = {GamePhase.OPENING: 0.3, GamePhase.MIDDLE: 0.5, GamePhase.ENDGAME: 0.8}
        base = weights.get(phase, 0.5)
        progress = min(1.0, move_count / 300)
        return base * (1.0 + progress * 0.5)


# ============================================================================
# 6. BSD MCTS围棋引擎
# ============================================================================

class BSDMCTSEngine:
    """BSD MCTS围棋引擎 - 六系协同+蒙特卡洛树搜索"""

    def __init__(self, board_size: int = 19, num_simulations: int = 1000):
        self.board_size = board_size
        self.num_simulations = num_simulations
        self.mapper = LiuHeMapper()
        self.evaluator = HeuristicEvaluator()
        self.alpha_ind = 0.33
        self.alpha_rel = 0.33
        self.alpha_chg = 0.34
        self.search_time = 5.0  # 搜索时间（秒）

    def select_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        """使用MCTS选择最佳落子"""
        # 初始化根节点
        root = MCTSNode(board=board, stone=stone)

        # 如果没有合法落子
        if not root.untried_moves and not root.children:
            return None

        # 过滤掉当前棋盘上已非法的落子
        valid_moves = [m for m in root.untried_moves if board.is_valid_move(m, stone)]
        if not valid_moves:
            return None
        root.untried_moves = valid_moves

        # 时间限制搜索
        start_time = time.time()
        iterations = 0

        while time.time() - start_time < self.search_time and iterations < self.num_simulations:
            # 1. 选择
            node = self._select(root)

            # 2. 扩展
            if not node.board.game_over and node.untried_moves:
                node = self._expand(node)

            # 3. 模拟
            result = self._simulate(node)

            # 4. 回传
            self._backpropagate(node, result, stone)

            iterations += 1

        # 选择访问次数最多的子节点
        best_point = None
        if root.children:
            # 从子节点中选择访问次数最多且在当前棋盘上合法的
            valid_children = [c for c in root.children if board.is_valid_move(c.point, stone)]
            if valid_children:
                best_child = max(valid_children, key=lambda c: c.visits)
                best_point = best_child.point
        
        if best_point is None and root.untried_moves:
            # 从剩余的合法落子中选择
            for m in root.untried_moves:
                if board.is_valid_move(m, stone):
                    best_point = m
                    break
        
        return best_point

    def _select(self, node: MCTSNode) -> MCTSNode:
        """选择阶段：使用UCB1选择节点"""
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        return node

    def _expand(self, node: MCTSNode) -> MCTSNode:
        """扩展阶段：创建新子节点"""
        if not node.untried_moves:
            return node

        # 优先选择六系评分高的落子
        best_move = self._select_expand_move(node)
        if best_move is None:
            return node

        # 创建新节点
        new_board = node.board.clone()
        new_board.make_move(best_move, node.stone)
        child_stone = Stone.WHITE if node.stone == Stone.BLACK else Stone.BLACK

        child = MCTSNode(
            board=new_board,
            stone=child_stone,
            point=best_move,
            parent=node
        )

        node.children.append(child)
        node.untried_moves.remove(best_move)
        return child

    def _select_expand_move(self, node: MCTSNode) -> Optional[GoPoint]:
        """选择扩展落子 - 使用六系评估"""
        if not node.untried_moves:
            return None

        # 评估每个候选落子
        scored_moves = []
        for point in node.untried_moves[:15]:  # 限制数量
            test_board = node.board.clone()
            test_board.make_move(point, node.stone)

            # 六系评估
            coord = self.mapper.map(test_board, node.stone)
            liuhe_score = (
                self.alpha_ind * coord.qh +
                self.alpha_rel * (coord.zr + coord.sh) / 2 +
                self.alpha_chg * (coord.bs + coord.td) / 2
            )

            # 启发式评估
            heuristic = self.evaluator.evaluate(test_board, node.stone)

            # 综合评分
            score = 0.4 * liuhe_score + 0.6 * heuristic
            scored_moves.append((point, score))

        # 排序并加入随机性
        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # 在前5个中随机选择
        if len(scored_moves) > 5:
            return random.choice(scored_moves[:5])[0]
        elif scored_moves:
            return scored_moves[0][0]
        return None

    def _simulate(self, node: MCTSNode) -> float:
        """模拟阶段：快速对局评估"""
        board = node.board.clone()
        current = node.stone
        root_stone = Stone.WHITE if current == Stone.BLACK else Stone.BLACK
        max_steps = 50

        for _ in range(max_steps):
            if board.game_over:
                break

            # 启发式选择落子
            move = self._heuristic_move(board, current)
            if move:
                board.make_move(move, current)
            else:
                board.pass_move(current)

            current = Stone.WHITE if current == Stone.BLACK else Stone.BLACK

            if board.consecutive_passes >= 2:
                break

        # 评估结果
        return self.evaluator.evaluate(board, root_stone)

    def _heuristic_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        """启发式落子选择"""
        valid_moves = board.get_empty_points()
        valid_moves = [p for p in valid_moves if board.is_valid_move(p, stone)]

        if not valid_moves:
            return None

        # 评估每个合法落子
        scored_moves = []
        for point in valid_moves[:10]:  # 限制数量
            test_board = board.clone()
            test_board.make_move(point, stone)
            score = self.evaluator.evaluate(test_board, stone)
            scored_moves.append((point, score))

        if not scored_moves:
            return None

        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # 加入随机性
        if len(scored_moves) > 3:
            return random.choice(scored_moves[:3])[0]
        return scored_moves[0][0]

    def _backpropagate(self, node: MCTSNode, result: float, root_stone: Stone):
        """回传阶段：更新节点统计"""
        while node is not None:
            node.visits += 1

            # 如果当前节点的玩家是根节点玩家，加上胜利值
            if node.stone == root_stone:
                node.wins += result
            else:
                node.wins += (1.0 - result)

            node = node.parent

    def get_position_analysis(self, board: GoBoard, stone: Stone) -> Dict:
        """获取位置分析"""
        coord = self.mapper.map(board, stone)
        return {
            'move_number': len(board.move_history),
            'phase': board.get_game_phase().value,
            'coordinate': {
                '强化系': round(coord.qh, 3),
                '自然系': round(coord.zr, 3),
                '具现系': round(coord.jx, 3),
                '变身系': round(coord.bs, 3),
                '社会系': round(coord.sh, 3),
                '天道系': round(coord.td, 3),
                '主导系': coord.dominant_system()
            }
        }


# ============================================================================
# 7. 演示
# ============================================================================

def demo():
    print("=" * 60)
    print("BSD围棋AI引擎 V2.0 - MCTS + 六系协同")
    print("=" * 60)

    engine = BSDMCTSEngine(board_size=9, num_simulations=500)
    print(f"\n引擎配置：")
    print(f"  棋盘：{engine.board_size}路")
    print(f"  模拟次数：{engine.num_simulations}")
    print(f"  搜索时间：{engine.search_time}秒/步")

    # 开局演示
    print("\n【开局演示 - 9路棋盘】")
    board = GoBoard(9)
    current = Stone.BLACK

    for i in range(30):
        if board.game_over:
            break

        point = engine.select_move(board, current)
        if point:
            move = board.make_move(point, current)
            if move:
                p = "●" if current == Stone.BLACK else "○"
                print(f"  {i+1:2d}. {p} {point.to_gtp()}", end="")
                if move.captured > 0:
                    print(f" (×{move.captured})", end="")
                print()

        current = Stone.WHITE if current == Stone.BLACK else Stone.BLACK

    # 局面分析
    print("\n【局面分析】")
    analysis = engine.get_position_analysis(board, board.current_player)
    for k, v in analysis['coordinate'].items():
        print(f"  {k}：{v}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
