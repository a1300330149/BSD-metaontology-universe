"""
BSD围棋引擎 V3.0 - 增强版
=======================
核心改进：
1. 增强评估器：棋形识别、攻击意识、领土精确计算
2. MCTS优化：威胁空间搜索、动态剪枝、六系指导
3. 终局锁定：中后盘精确模式
4. 六系协同：动态权重调整

理论依据：
- 六系层级涌现定理：十二级纵向涌现链
- 三本源学科：真性物理(BSD) vs 反性数学 vs 问性哲学
- 天道系追问：超越计算的棋道意义
"""

import sys
import os
import math
import random
import time
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import (
    GoBoard, GoPoint, Stone, GamePhase,
    LiuHeCoordinate
)


class OptimizedEvaluator:
    """优化版评估器 - 高性能+高准确度"""

    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self._eval_cache = {}
        self._cache_hits = 0
        self._cache_misses = 0

    def evaluate(self, board: GoBoard, stone: Stone,
                 phase: GamePhase = None) -> float:
        if phase is None:
            phase = board.get_game_phase()

        cache_key = (id(board), stone, phase)
        if cache_key in self._eval_cache:
            self._cache_hits += 1
            return self._eval_cache[cache_key]

        self._cache_misses += 1
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK

        scores = []
        
        s_shape = self._eval_shape_fast(board, stone, opp)
        s_attack = self._eval_attack_fast(board, stone, opp)
        s_territory = self._eval_territory_fast(board, stone, opp, phase)
        s_thickness = self._eval_thickness_fast(board, stone, opp)
        s_threat = self._eval_threat_fast(board, stone, opp)
        s_mobility = self._eval_mobility_fast(board, stone, opp)

        if phase == GamePhase.OPENING:
            weights = [0.25, 0.20, 0.15, 0.20, 0.10, 0.10]
        elif phase == GamePhase.MIDDLE:
            weights = [0.15, 0.25, 0.25, 0.10, 0.15, 0.10]
        else:
            weights = [0.10, 0.15, 0.40, 0.05, 0.15, 0.15]

        for s, w in zip([s_shape, s_attack, s_territory, s_thickness, s_threat, s_mobility], weights):
            scores.append(w * s)

        total = max(-1.0, min(1.0, sum(scores)))
        self._eval_cache[cache_key] = total
        return total

    def _eval_shape_fast(self, board: GoBoard, stone: Stone, opp: Stone) -> float:
        score = 0.0
        count = 0

        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] != stone:
                    continue

                count += 1
                neighbors = self._get_neighbors_fast(board, x, y)
                
                own = sum(1 for nx, ny in neighbors 
                         if board.board[ny][nx] == stone)
                opp_count = sum(1 for nx, ny in neighbors 
                              if board.board[ny][nx] == opp)

                if own >= 2 and opp_count <= 1:
                    score += 0.15
                elif own >= 3:
                    score += 0.10

        denom = max(count, 1)
        return max(-1.0, min(1.0, score / denom * 2))

    def _eval_attack_fast(self, board: GoBoard, stone: Stone, opp: Stone) -> float:
        weak_opp = 0
        weak_own = 0

        opp_groups = self._get_all_groups(board, opp)
        for group, libs in opp_groups:
            if len(libs) <= 2:
                weak_opp += len(group)

        own_groups = self._get_all_groups(board, stone)
        for group, libs in own_groups:
            if len(libs) <= 2:
                weak_own += len(group)

        total = len(opp_groups) + len(own_groups) + 1
        return max(-1.0, min(1.0, (weak_opp - weak_own) / total * 0.8))

    def _eval_territory_fast(self, board: GoBoard, stone: Stone, opp: Stone, 
                             phase: GamePhase) -> float:
        own_claim = 0
        opp_claim = 0
        own_stones = 0
        opp_stones = 0

        for y in range(self.board_size):
            for x in range(self.board_size):
                cell = board.board[y][x]
                if cell == Stone.EMPTY:
                    n = self._get_neighbor_counts_fast(board, x, y)
                    if n.get(stone, 0) >= 2 and n.get(opp, 0) == 0:
                        own_claim += 1
                    elif n.get(opp, 0) >= 2 and n.get(stone, 0) == 0:
                        opp_claim += 1
                elif cell == stone:
                    own_stones += 1
                elif cell == opp:
                    opp_stones += 1

        total_claim = own_claim + opp_claim + 1
        claim_score = (own_claim - opp_claim) / total_claim

        total_stones = own_stones + opp_stones + 1
        stone_score = (own_stones - opp_stones) / total_stones

        return max(-1.0, min(1.0, claim_score * 0.7 + stone_score * 0.3))

    def _eval_thickness_fast(self, board: GoBoard, stone: Stone, opp: Stone) -> float:
        score = 0.0

        own_groups = self._get_all_groups(board, stone)
        for group, libs in own_groups:
            if len(group) >= 5:
                score += 0.25
            elif len(group) >= 3:
                score += 0.15
            if len(libs) >= 5:
                score += 0.2
            elif len(libs) >= 3:
                score += 0.1

        opp_groups = self._get_all_groups(board, opp)
        for group, libs in opp_groups:
            if len(group) >= 5:
                score -= 0.2
            if len(libs) <= 1:
                score += 0.15

        total = len(own_groups) + len(opp_groups) + 1
        return max(-1.0, min(1.0, score / total * 1.5))

    def _eval_threat_fast(self, board: GoBoard, stone: Stone, opp: Stone) -> float:
        opp_libs_total = 0
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                point = GoPoint(x, y)
                if board.board[y][x] == opp and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    opp_libs_total += len(libs)

        own_libs_total = 0
        visited.clear()
        for y in range(self.board_size):
            for x in range(self.board_size):
                point = GoPoint(x, y)
                if board.board[y][x] == stone and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    own_libs_total += len(libs)

        total = opp_libs_total + own_libs_total + 1
        return max(-1.0, min(1.0, (own_libs_total - opp_libs_total) / total))

    def _eval_mobility_fast(self, board: GoBoard, stone: Stone, opp: Stone) -> float:
        own_moves = self._count_valid_moves_fast(board, stone)
        opp_moves = self._count_valid_moves_fast(board, opp)
        total = own_moves + opp_moves + 1
        return max(-1.0, min(1.0, (own_moves - opp_moves) / total))

    def _get_neighbors_fast(self, board: GoBoard, x: int, y: int) -> List[Tuple[int, int]]:
        result = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                result.append((nx, ny))
        return result

    def _get_neighbor_counts_fast(self, board: GoBoard, x: int, y: int) -> Dict:
        counts = {Stone.EMPTY: 0, Stone.BLACK: 0, Stone.WHITE: 0}
        for nx, ny in self._get_neighbors_fast(board, x, y):
            s = board.board[ny][nx]
            counts[s] = counts.get(s, 0) + 1
        return counts

    def _get_all_groups(self, board: GoBoard, stone: Stone) -> List[Tuple[List[GoPoint], List[GoPoint]]]:
        groups = []
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                point = GoPoint(x, y)
                if board.board[y][x] == stone and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    groups.append((group, libs))
        return groups

    def _count_valid_moves_fast(self, board: GoBoard, stone: Stone) -> int:
        count = 0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == Stone.EMPTY:
                    if board.is_valid_move(GoPoint(x, y), stone):
                        count += 1
        return count

    def clear_cache(self):
        self._eval_cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0


class ThreatSpaceSearch:
    """威胁空间搜索 - 只在关键区域进行精确搜索"""

    def __init__(self, board_size: int = 19):
        self.board_size = board_size

    def get_threat_points(self, board: GoBoard, stone: Stone,
                          max_points: int = 20) -> List[GoPoint]:
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        threat_points = []
        scores = []

        for y in range(board.size):
            for x in range(board.size):
                point = GoPoint(x, y)
                if board.board[y][x] != Stone.EMPTY:
                    continue
                if not board.is_valid_move(point, stone):
                    continue

                score = self._compute_threat_score(board, point, stone, opp)
                if score > 0:
                    scores.append((point, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [p for p, s in scores[:max_points]]

    def _compute_threat_score(self, board: GoBoard, point: GoPoint,
                              stone: Stone, opp: Stone) -> float:
        score = 0.0
        center = self.board_size / 2

        test_board = board.clone()
        test_board.make_move(point, stone)

        libs_before = self._count_libs(board, opp)
        libs_after = self._count_libs(test_board, opp)
        if libs_after < libs_before:
            score += 0.3

        own_libs_before = self._count_libs(board, stone)
        own_libs_after = self._count_libs(test_board, stone)
        if own_libs_after >= own_libs_before:
            score += 0.15

        captures_before = self._count_captures(board, stone)
        captures_after = self._count_captures(test_board, stone)
        if captures_after > captures_before:
            score += 0.4

        dist_center = abs(point.x - center) + abs(point.y - center)
        score += 0.1 * (2 * center - dist_center) / (2 * center)

        neighbors = self._get_neighbors(point)
        for n in neighbors:
            if board.board[n.y][n.x] == stone:
                score += 0.1
            elif board.board[n.y][n.x] == opp:
                score += 0.05

        return score

    def _get_neighbors(self, point: GoPoint) -> List[GoPoint]:
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = point.x + dx, point.y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                neighbors.append(GoPoint(nx, ny))
        return neighbors

    def _count_libs(self, board: GoBoard, stone: Stone) -> int:
        total = 0
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                point = GoPoint(x, y)
                if board.board[y][x] == stone and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    total += len(libs)
        return total

    def _count_captures(self, board: GoBoard, stone: Stone) -> int:
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        count = 0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == Stone.EMPTY:
                    point = GoPoint(x, y)
                    for n in self._get_neighbors(point):
                        if board.board[n.y][n.x] == opp:
                            group, libs = board.get_group(n)
                            fake_libs = [l for l in libs 
                                       if l != point and board.board[l.y][l.x] == Stone.EMPTY]
                            if len(fake_libs) == 0:
                                count += len(group)
        return count


@dataclass
class EnhancedMCTSNode:
    """增强版MCTS节点 - 支持威胁空间搜索"""
    board: GoBoard
    stone: Stone
    point: Optional[GoPoint] = None
    parent: Optional['EnhancedMCTSNode'] = None
    children: List['EnhancedMCTSNode'] = field(default_factory=list)
    visits: int = 0
    wins: float = 0.0
    untried_moves: List[GoPoint] = field(default_factory=list)
    prior: float = 1.0
    threat_score: float = 0.0

    def __post_init__(self):
        if not self.untried_moves and self.board:
            self.untried_moves = self._get_legal_moves()

    def _get_legal_moves(self) -> List[GoPoint]:
        moves = []
        for y in range(self.board.size):
            for x in range(self.board.size):
                point = GoPoint(x, y)
                if self.board.is_valid_move(point, self.stone):
                    moves.append(point)
        return moves[:30]

    def ucb1(self, exploration: float = 1.414) -> float:
        if self.visits == 0:
            return float('inf')
        win_rate = self.wins / self.visits
        exploration_term = exploration * math.sqrt(math.log(self.parent.visits) / self.visits)
        exploitation = win_rate
        if self.threat_score > 0:
            exploitation += self.threat_score * 0.1
        return exploitation + exploration_term

    def best_child(self, exploration: float = 1.414) -> 'EnhancedMCTSNode':
        if not self.children:
            return self
        return max(self.children, key=lambda c: c.ucb1(exploration))

    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        return self.board.game_over or (len(self.untried_moves) == 0 and not self.children)


class BSDGoEngineV3:
    """BSD围棋引擎V3.0 - 增强版

    核心改进：
    1. 优化评估器：棋形+攻击+领土+厚度+威胁+机动性
    2. 威胁空间搜索：只在关键区域展开
    3. 动态六系权重：根据阶段调整
    4. 中后盘精确模式
    """

    def __init__(self, board_size: int = 19, num_simulations: int = 1000):
        self.board_size = board_size
        self.num_simulations = num_simulations
        self.evaluator = OptimizedEvaluator(board_size)
        self.tss = ThreatSpaceSearch(board_size)
        self.search_time = 5.0

        self.alpha_ind = 0.33
        self.alpha_rel = 0.33
        self.alpha_chg = 0.34

        self._positions_evaluated = 0
        self._moves_count = 0

    def select_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        valid_moves = [
            GoPoint(x, y)
            for x in range(board.size)
            for y in range(board.size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return None

        phase = board.get_game_phase()

        if phase == GamePhase.ENDGAME and len(valid_moves) <= 30:
            return self._endgame_select(board, stone, valid_moves)

        root = EnhancedMCTSNode(board=board, stone=stone)
        root.untried_moves = self._filter_moves(root.untried_moves, board, stone)

        if not root.untried_moves:
            return None

        threat_points = self.tss.get_threat_points(board, stone, max_points=15)
        if threat_points:
            for tp in threat_points:
                if tp in root.untried_moves:
                    root.untried_moves.remove(tp)
                    root.untried_moves.insert(0, tp)

        start_time = time.time()
        iterations = 0

        while time.time() - start_time < self.search_time and iterations < self.num_simulations:
            node = self._select(root)
            if not node.board.game_over and node.untried_moves:
                node = self._expand(node, stone)
            result = self._simulate(node, stone)
            self._backpropagate(node, result, stone)
            iterations += 1

        best_point = self._select_final_move(root, board, stone)

        if best_point and board.is_valid_move(best_point, stone):
            self._moves_count += 1
            return best_point

        return self._heuristic_select(board, stone, valid_moves)

    def _endgame_select(self, board: GoBoard, stone: Stone,
                        valid_moves: List[GoPoint]) -> Optional[GoPoint]:
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        best_point = None
        best_score = -float('inf')

        for point in valid_moves[:10]:
            test_board = board.clone()
            test_board.make_move(point, stone)

            own_territory = test_board._count_territory(stone)
            opp_territory = test_board._count_territory(opp)
            score = (own_territory - opp_territory) * 2.0

            score += 0.3 * self.evaluator.evaluate(test_board, stone, GamePhase.ENDGAME)

            if score > best_score:
                best_score = score
                best_point = point

        return best_point

    def _filter_moves(self, moves: List[GoPoint], board: GoBoard,
                      stone: Stone) -> List[GoPoint]:
        valid = [m for m in moves if board.is_valid_move(m, stone)]
        if len(valid) <= 20:
            return valid

        scored = []
        for point in valid[:25]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            score = self.evaluator.evaluate(test_board, stone)
            scored.append((point, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [p for p, s in scored[:15]]

    def _select(self, node: EnhancedMCTSNode) -> EnhancedMCTSNode:
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        return node

    def _expand(self, node: EnhancedMCTSNode,
               root_stone: Stone) -> EnhancedMCTSNode:
        if not node.untried_moves:
            return node

        move_scores = []
        for point in node.untried_moves[:10]:
            test_board = node.board.clone()
            test_board.make_move(point, node.stone)

            eval_score = self.evaluator.evaluate(test_board, node.stone)
            threat = self._quick_threat_score(node.board, test_board, point, node.stone)
            combined = 0.6 * eval_score + 0.4 * threat
            move_scores.append((point, combined))

        move_scores.sort(key=lambda x: x[1], reverse=True)

        best_move = move_scores[0][0]
        new_board = node.board.clone()
        new_board.make_move(best_move, node.stone)
        child_stone = Stone.WHITE if node.stone == Stone.BLACK else Stone.BLACK

        child = EnhancedMCTSNode(
            board=new_board,
            stone=child_stone,
            point=best_move,
            parent=node
        )
        child.threat_score = move_scores[0][1]

        node.children.append(child)
        node.untried_moves.remove(best_move)
        return child

    def _quick_threat_score(self, before: GoBoard, after: GoBoard,
                            point: GoPoint, stone: Stone) -> float:
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK

        opp_libs_before = self._count_total_liberties(before, opp)
        opp_libs_after = self._count_total_liberties(after, opp)

        if opp_libs_after < opp_libs_before:
            return 0.4

        own_libs_before = self._count_total_liberties(before, stone)
        own_libs_after = self._count_total_liberties(after, stone)

        if own_libs_after > own_libs_before:
            return 0.2

        return 0.0

    def _simulate(self, node: EnhancedMCTSNode, root_stone: Stone) -> float:
        board = node.board.clone()
        current = node.stone
        max_steps = 30

        for _ in range(max_steps):
            if board.game_over:
                break

            move = self._smart_move(board, current)
            if move:
                board.make_move(move, current)
            else:
                board.pass_move(current)

            current = Stone.WHITE if current == Stone.BLACK else Stone.BLACK

            if board.consecutive_passes >= 2:
                break

        return self.evaluator.evaluate(board, root_stone)

    def _smart_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        valid_moves = [
            GoPoint(x, y)
            for x in range(board.size)
            for y in range(board.size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return None

        scored = []
        for point in valid_moves[:8]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            score = self.evaluator.evaluate(test_board, stone)
            scored.append((point, score))

        if not scored:
            return None

        scored.sort(key=lambda x: x[1], reverse=True)

        if len(scored) > 2 and random.random() < 0.3:
            return random.choice(scored[:3])[0]
        return scored[0][0]

    def _backpropagate(self, node: EnhancedMCTSNode, result: float,
                       root_stone: Stone):
        while node is not None:
            node.visits += 1
            if node.stone == root_stone:
                node.wins += result
            else:
                node.wins -= result
            node = node.parent

    def _select_final_move(self, root: EnhancedMCTSNode, board: GoBoard,
                           stone: Stone) -> Optional[GoPoint]:
        if root.children:
            valid_children = [c for c in root.children
                             if board.is_valid_move(c.point, stone)]
            if valid_children:
                best = max(valid_children,
                          key=lambda c: c.visits * (1 + c.wins / max(c.visits, 1)))
                return best.point

        if root.untried_moves:
            for m in root.untried_moves:
                if board.is_valid_move(m, stone):
                    return m

        return None

    def _heuristic_select(self, board: GoBoard, stone: Stone,
                          valid_moves: List[GoPoint]) -> Optional[GoPoint]:
        best_point = None
        best_score = -float('inf')

        for point in valid_moves[:15]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            score = self.evaluator.evaluate(test_board, stone)
            if score > best_score:
                best_score = score
                best_point = point

        return best_point

    def _count_total_liberties(self, board: GoBoard, stone: Stone) -> int:
        total = 0
        visited = set()
        for y in range(board.size):
            for x in range(board.size):
                point = GoPoint(x, y)
                if board.board[y][x] == stone and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    total += len(libs)
        return total

    def get_position_analysis(self, board: GoBoard,
                              stone: Stone) -> Dict:
        phase = board.get_game_phase()
        score = self.evaluator.evaluate(board, stone, phase)

        return {
            'phase': phase.value,
            'score': score,
            'moves_count': len(board.move_history),
            'board_size': board.size,
            'empty_points': len([
                (x, y) for x in range(board.size) for y in range(board.size)
                if board.board[y][x] == Stone.EMPTY
            ])
        }


def create_board(size: int = 19) -> GoBoard:
    return GoBoard(size)


def create_engine(board_size: int = 19,
                  num_simulations: int = 1000) -> BSDGoEngineV3:
    return BSDGoEngineV3(board_size, num_simulations)
