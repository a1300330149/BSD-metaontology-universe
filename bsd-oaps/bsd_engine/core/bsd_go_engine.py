"""
BSD围棋AI引擎 - 六系协同围棋对弈系统
============================================
基于BSD六系立系论的围棋AI引擎，实现：
1. 六系坐标映射：围棋状态→六系空间锚点
2. 权重动态调配：α₁个体性 + α₂关系性 + α₃变化性
3. 天道系追问：超越计算的棋道意义

理论依据：
- BSD三本源学科定标（真性物理·反性数学·问性哲学）
- 六系立系论（锚点·闭环·演化）
- 系立万有公理

版本：V1.0 · 2026-08-02
"""

import math
import json
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import copy


# ============================================================================
# 1. 基础数据结构
# ============================================================================

class Stone(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class GamePhase(Enum):
    OPENING = "opening"      # 开局 (0-60手)
    MIDDLE = "middle"        # 中盘 (61-150手)
    ENDGAME = "endgame"      # 官子 (150+手)
    YONE = "yone"           # 终局


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
        """转换为GTP坐标（A-T，跳过I）"""
        letters = 'ABCDEFGHJKLMNOPQRST'  # 跳过I
        return letters[self.x] + str(self.y + 1)


@dataclass
class Move:
    point: GoPoint
    stone: Stone
    move_number: int
    captured: int = 0  # 提子数
    is_ko: bool = False


# ============================================================================
# 2. 围棋棋盘
# ============================================================================

class GoBoard:
    """围棋棋盘 - 支持9/13/19路"""

    def __init__(self, size: int = 19):
        self.size = size
        self.board: List[List[Stone]] = [
            [Stone.EMPTY for _ in range(size)] for _ in range(size)
        ]
        self.move_history: List[Move] = []
        self.current_player = Stone.BLACK
        self.ko_point: Optional[GoPoint] = None
        self.consecutive_passes = 0
        self.game_over = False

    def clone(self) -> 'GoBoard':
        """深拷贝棋盘"""
        new_board = GoBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.move_history = self.move_history.copy()
        new_board.current_player = self.current_player
        new_board.ko_point = self.ko_point
        new_board.consecutive_passes = self.consecutive_passes
        new_board.game_over = self.game_over
        return new_board

    def get_neighbors(self, point: GoPoint) -> List[GoPoint]:
        """获取相邻点"""
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = point.x + dx, point.y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append(GoPoint(nx, ny))
        return neighbors

    def get_group(self, point: GoPoint) -> Tuple[List[GoPoint], List[GoPoint]]:
        """获取连串和气"""
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
        """检查落子合法性"""
        if self.game_over:
            return False
        if self.board[point.y][point.x] != Stone.EMPTY:
            return False

        # 检查劫
        if self.ko_point and point == self.ko_point:
            return False

        # 模拟落子
        test_board = self.clone()
        test_board.board[point.y][point.x] = stone

        # 检查是否能提对方子
        opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        captured = 0
        for neighbor in self.get_neighbors(point):
            if test_board.board[neighbor.y][neighbor.x] == opponent:
                _, libs = test_board.get_group(neighbor)
                if len(libs) == 0:
                    # 提子
                    group, _ = test_board.get_group(neighbor)
                    captured += len(group)

        # 如果能提子，合法
        if captured > 0:
            return True

        # 检查自己是否有气
        _, own_libs = test_board.get_group(point)
        return len(own_libs) > 0

    def make_move(self, point: GoPoint, stone: Stone) -> Optional[Move]:
        """执行落子"""
        if not self.is_valid_move(point, stone):
            return None

        self.board[point.y][point.x] = stone

        # 提子
        opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        captured = 0
        captured_points = []

        for neighbor in self.get_neighbors(point):
            if self.board[neighbor.y][neighbor.x] == opponent:
                group, libs = self.get_group(neighbor)
                if len(libs) == 0:
                    captured_points.extend(group)
                    captured += len(group)

        # 执行提子
        for cp in captured_points:
            self.board[cp.y][cp.x] = Stone.EMPTY

        # 检查劫
        if captured == 1:
            _, own_libs = self.get_group(point)
            if len(own_libs) == 1:
                # 可能形成劫
                self.ko_point = own_libs[0]
            else:
                self.ko_point = None
        else:
            self.ko_point = None

        # 更新状态
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
        """虚着"""
        self.consecutive_passes += 1
        self.current_player = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        self.ko_point = None

        if self.consecutive_passes >= 2:
            self.game_over = True
        return True

    def get_game_phase(self) -> GamePhase:
        """获取当前棋局阶段"""
        move_count = len(self.move_history)
        if move_count <= 60:
            return GamePhase.OPENING
        elif move_count <= 150:
            return GamePhase.MIDDLE
        else:
            return GamePhase.ENDGAME

    def get_score(self, komi: float = 7.5) -> Dict:
        """计算中国规则计分"""
        if not self.game_over:
            return {"black": 0, "white": 0, "winner": "unknown", "margin": 0}

        # 简化版：计算领地和棋子
        black_territory = 0
        white_territory = 0
        black_stones = 0
        white_stones = 0

        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == Stone.BLACK:
                    black_stones += 1
                elif self.board[y][x] == Stone.WHITE:
                    white_stones += 1
                else:
                    # 简化：不精确计算领地
                    pass

        # 中国规则：子空皆地
        black_total = black_stones + self._count_territory(Stone.BLACK)
        white_total = white_stones + self._count_territory(Stone.WHITE) + komi

        if black_total > white_total:
            return {
                "black": black_total,
                "white": white_total,
                "winner": "black",
                "margin": black_total - white_total
            }
        else:
            return {
                "black": black_total,
                "white": white_total,
                "winner": "white",
                "margin": white_total - black_total
            }

    def _count_territory(self, color: Stone) -> int:
        """计算领地（简化版）"""
        territory = 0
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == Stone.EMPTY:
                    # 简化：检查周围是否只有一种颜色
                    neighbors = self.get_neighbors(GoPoint(x, y))
                    has_black = any(self.board[n.y][n.x] == Stone.BLACK for n in neighbors)
                    has_white = any(self.board[n.y][n.x] == Stone.WHITE for n in neighbors)
                    if color == Stone.BLACK and has_black and not has_white:
                        territory += 1
                    elif color == Stone.WHITE and has_white and not has_black:
                        territory += 1
        return territory

    def to_string(self) -> str:
        """转换为字符串表示"""
        result = []
        for y in range(self.size - 1, -1, -1):
            row = []
            for x in range(self.size):
                if self.board[y][x] == Stone.BLACK:
                    row.append('●')
                elif self.board[y][x] == Stone.WHITE:
                    row.append('○')
                else:
                    row.append('·')
            result.append(' '.join(row))
        return '\n'.join(result)


# ============================================================================
# 3. 六系围棋映射
# ============================================================================

@dataclass
class LiuHeGoCoordinate:
    """围棋六系坐标"""
    qh: float = 0.0   # 强化系：计算强度（算力）
    zr: float = 0.0   # 自然系：棋理顺应（自然）
    jx: float = 0.0   # 具现系：具象落子（应用）
    bs: float = 0.0   # 变身系：变化应对（创新）
    sh: float = 0.0   # 社会系：对手博弈（关系）
    td: float = 0.0   # 天道系：棋道意义（追问）

    def to_vector(self) -> List[float]:
        return [self.qh, self.zr, self.jx, self.bs, self.sh, self.td]

    def dominant_system(self) -> str:
        systems = {
            '强化系': self.qh, '自然系': self.zr, '具现系': self.jx,
            '变身系': self.bs, '社会系': self.sh, '天道系': self.td
        }
        return max(systems, key=systems.get)


class LiuHeGoMapper:
    """围棋状态→六系坐标映射器"""

    @staticmethod
    def map_board_state(board: GoBoard, stone: Stone) -> LiuHeGoCoordinate:
        """将棋盘状态映射为六系坐标"""
        # 计算各系特征
        qh = LiuHeGoMapper._calc_qianghua(board, stone)
        zr = LiuHeGoMapper._calc_ziran(board, stone)
        jx = LiuHeGoMapper._calc_juxian(board, stone)
        bs = LiuHeGoMapper._calc_bianshen(board, stone)
        sh = LiuHeGoMapper._calc_shehui(board, stone)
        td = LiuHeGoMapper._calc_tiandao(board, stone)

        return LiuHeGoCoordinate(qh=qh, zr=zr, jx=jx, bs=bs, sh=sh, td=td)

    @staticmethod
    def _calc_qianghua(board: GoBoard, stone: Stone) -> float:
        """强化系：计算当前优势度"""
        # 简化：计算己方棋子数 / 总交叉点
        total_points = board.size ** 2
        my_stones = sum(1 for y in range(board.size)
                       for x in range(board.size)
                       if board.board[y][x] == stone)
        return min(1.0, my_stones / total_points * 2)  # 归一化

    @staticmethod
    def _calc_ziran(board: GoBoard, stone: Stone) -> float:
        """自然系：棋理顺应度（布局合理性）"""
        # 简化：评估棋子分布是否合理
        # 开局偏好星位、小目等经典位置
        classic_points = [
            (3, 3), (3, 9), (3, 15),   # 星位
            (9, 3), (9, 9), (9, 15),
            (15, 3), (15, 9), (15, 15)
        ]
        my_points = [(x, y) for y in range(board.size)
                     for x in range(board.size)
                     if board.board[y][x] == stone]

        if not my_points:
            return 0.5

        # 计算与经典位置的接近度
        score = 0
        for px, py in my_points:
            for cx, cy in classic_points:
                dist = abs(px - cx) + abs(py - cy)
                if dist <= 2:
                    score += 1.0 / (1.0 + dist)

        return min(1.0, score / len(my_points))

    @staticmethod
    def _calc_juxian(board: GoBoard, stone: Stone) -> float:
        """具现系：可落子点丰富度"""
        valid_moves = LiuHeGoMapper._count_valid_moves(board, stone)
        total_points = board.size ** 2
        return min(1.0, valid_moves / total_points * 3)

    @staticmethod
    def _calc_bianshen(board: GoBoard, stone: Stone) -> float:
        """变身系：战术变化丰富度"""
        # 简化：计算己方棋子的气数多样性
        lib_counts = []
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] == stone:
                    _, libs = board.get_group(GoPoint(x, y))
                    lib_counts.append(len(libs))

        if not lib_counts:
            return 0.5

        # 气数分布越多样，变化性越强
        unique_libs = len(set(lib_counts))
        return min(1.0, unique_libs / 6.0)

    @staticmethod
    def _calc_shehui(board: GoBoard, stone: Stone) -> float:
        """社会系：对手威胁度"""
        opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        opponent_libs = []
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] == opponent:
                    _, libs = board.get_group(GoPoint(x, y))
                    opponent_libs.append(len(libs))

        if not opponent_libs:
            return 0.5

        # 对手气越少，威胁越大
        avg_libs = sum(opponent_libs) / len(opponent_libs)
        return max(0.0, min(1.0, 1.0 - avg_libs / 5.0))

    @staticmethod
    def _calc_tiandao(board: GoBoard, stone: Stone) -> float:
        """天道系：棋道意义度（全局价值）"""
        # 计算整体态势
        phase = board.get_game_phase()
        move_count = len(board.move_history)

        # 不同阶段天道权重不同
        phase_weights = {
            GamePhase.OPENING: 0.3,
            GamePhase.MIDDLE: 0.5,
            GamePhase.ENDGAME: 0.8
        }

        base_weight = phase_weights.get(phase, 0.5)

        # 随着对局进行，天道系权重增加
        progress = min(1.0, move_count / 300)
        return base_weight * (1.0 + progress * 0.5)

    @staticmethod
    def _count_valid_moves(board: GoBoard, stone: Stone) -> int:
        """计算合法落子数"""
        count = 0
        for y in range(board.size):
            for x in range(board.size):
                if board.is_valid_move(GoPoint(x, y), stone):
                    count += 1
        return count


# ============================================================================
# 4. BSD围棋AI引擎
# ============================================================================

@dataclass
class MoveEvaluation:
    """落子评估"""
    point: GoPoint
    score: float
    liuhe_coord: LiuHeGoCoordinate
    reasoning: str = ""


class BSDGoEngine:
    """BSD围棋AI引擎 - 六系协同决策"""

    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.mapper = LiuHeGoMapper()
        self.evaluation_history: List[MoveEvaluation] = []

        # 六系权重（动态调整）
        self.alpha_individuality = 0.33  # α₁个体性
        self.alpha_relation = 0.33       # α₂关系性
        self.alpha_change = 0.34          # α₃变化性

    def select_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        """选择最佳落子 - 六系协同决策"""
        game_phase = board.get_game_phase()

        # 根据阶段调整权重
        self._adjust_weights(game_phase)

        # 获取所有合法落子
        valid_moves = self._get_valid_moves(board, stone)
        if not valid_moves:
            return None

        # 评估每个落子
        evaluations = []
        for point in valid_moves[:50]:  # 限制候选数
            score = self._evaluate_move(board, point, stone)
            coord = self.mapper.map_board_state(board, stone)

            eval_result = MoveEvaluation(
                point=point,
                score=score,
                liuhe_coord=coord,
                reasoning=self._generate_reasoning(board, point, stone, coord)
            )
            evaluations.append(eval_result)

        # 按分数排序
        evaluations.sort(key=lambda e: e.score, reverse=True)

        # 选择最佳落子（加入少量随机性以增加多样性）
        if evaluations:
            # 在前3个中选择
            top_k = max(1, min(3, len(evaluations)))
            # 确定性选择最高分，但对同一分数的点可选次优
            best = evaluations[0]

            self.evaluation_history.append(best)
            return best.point

        return None

    def _adjust_weights(self, phase: GamePhase):
        """根据棋局阶段调整六系权重"""
        if phase == GamePhase.OPENING:
            # 开局：强化计算+顺应棋理
            self.alpha_individuality = 0.4  # 强化系
            self.alpha_relation = 0.3       # 自然系+社会系
            self.alpha_change = 0.3         # 变身系+天道系
        elif phase == GamePhase.MIDDLE:
            # 中盘：重视变化和博弈
            self.alpha_individuality = 0.3
            self.alpha_relation = 0.4       # 社会系权重增加
            self.alpha_change = 0.3
        else:
            # 官子：重视精度和意义
            self.alpha_individuality = 0.5  # 强化系精度
            self.alpha_relation = 0.2
            self.alpha_change = 0.3         # 天道系权重增加

    def _get_valid_moves(self, board: GoBoard, stone: Stone) -> List[GoPoint]:
        """获取合法落子列表"""
        moves = []
        for y in range(board.size):
            for x in range(board.size):
                point = GoPoint(x, y)
                if board.is_valid_move(point, stone):
                    moves.append(point)
        return moves

    def _evaluate_move(self, board: GoBoard, point: GoPoint, stone: Stone) -> float:
        """评估落子价值 - 六系协同评分"""
        # 模拟落子
        test_board = board.clone()
        test_board.make_move(point, stone)

        # 映射六系坐标
        coord = self.mapper.map_board_state(test_board, stone)

        # 六系加权评分
        # qh(强化) + zr(自然) + jx(具现) + bs(变身) + sh(社会) + td(天道)
        liuhe_score = (
            self.alpha_individuality * coord.qh +
            self.alpha_relation * (coord.zr + coord.sh) / 2 +
            self.alpha_change * (coord.bs + coord.td) / 2
        )

        # 战术评分
        tactical_score = self._tactical_evaluation(board, point, stone)

        # 战略评分
        strategic_score = self._strategic_evaluation(board, point, stone)

        # 综合评分
        return 0.3 * liuhe_score + 0.4 * tactical_score + 0.3 * strategic_score

    def _tactical_evaluation(self, board: GoBoard, point: GoPoint, stone: Stone) -> float:
        """战术评估：局部攻防价值"""
        score = 0.0
        opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK

        # 1. 提子价值
        test_board = board.clone()
        move = test_board.make_move(point, stone)
        if move and move.captured > 0:
            score += 0.3 * move.captured

        # 2. 己方安全
        _, own_libs = test_board.get_group(point)
        if len(own_libs) >= 3:
            score += 0.2
        elif len(own_libs) == 2:
            score += 0.1
        elif len(own_libs) == 1:
            score -= 0.3  # 自杀风险

        # 3. 威胁对方
        for neighbor in test_board.get_neighbors(point):
            if test_board.board[neighbor.y][neighbor.x] == opponent:
                _, opp_libs = test_board.get_group(neighbor)
                if len(opp_libs) <= 2:
                    score += 0.15

        return score

    def _strategic_evaluation(self, board: GoBoard, point: GoPoint, stone: Stone) -> float:
        """战略评估：全局布局价值"""
        score = 0.0

        # 1. 位置价值（星位、小目等）
        center = board.size / 2
        dist_from_center = abs(point.x - center) + abs(point.y - center)
        max_dist = 2 * center

        # 中腹价值（日本围棋）
        center_value = 1.0 - (dist_from_center / max_dist) * 0.5

        # 边缘价值
        edge_dist = min(point.x, point.y, board.size - 1 - point.x, board.size - 1 - point.y)
        edge_value = min(1.0, edge_dist / 3.0)

        score += 0.3 * center_value + 0.2 * edge_value

        # 2. 与已有棋子的配合
        my_neighbors = 0
        opp_neighbors = 0
        for neighbor in board.get_neighbors(point):
            if board.board[neighbor.y][neighbor.x] == stone:
                my_neighbors += 1
            elif board.board[neighbor.y][neighbor.x] != Stone.EMPTY:
                opp_neighbors += 1

        score += 0.1 * my_neighbors - 0.05 * opp_neighbors

        # 3. 天元特殊价值
        if point.x == center and point.y == center:
            score += 0.1  # 天元加成

        return score

    def _generate_reasoning(self, board: GoBoard, point: GoPoint,
                           stone: Stone, coord: LiuHeGoCoordinate) -> str:
        """生成决策理由 - 天道系追问"""
        dominant = coord.dominant_system()
        phase = board.get_game_phase()
        move_count = len(board.move_history)

        reasons = [f"第{move_count + 1}手落子 {point.to_gtp()}"]

        # 根据主导系生成理由
        reasons.append(f"主导系：{dominant}")

        # 根据阶段生成建议
        phase_desc = {
            GamePhase.OPENING: "开局布局阶段",
            GamePhase.MIDDLE: "中盘攻防阶段",
            GamePhase.ENDGAME: "官子收束阶段"
        }
        reasons.append(phase_desc.get(phase, ""))

        # 天道系追问
        if coord.td > 0.5:
            reasons.append("棋道意义：此手关系全局胜负")

        return " | ".join(reasons)


# ============================================================================
# 5. 对弈管理器
# ============================================================================

@dataclass
class GameRecord:
    """对局记录"""
    black_player: str
    white_player: str
    moves: List[Move]
    result: Optional[Dict] = None
    duration_moves: int = 0

    def to_sgf(self) -> str:
        """转换为SGF格式（简化版）"""
        lines = ['(;GM[1]FF[4]SZ[19]KM[7.5]', f'PB[{self.black_player}]PW[{self.white_player}]']

        for move in self.moves:
            if move.stone == Stone.BLACK:
                lines.append(f';B[{self._point_to_sgf(move.point)}]')
            else:
                lines.append(f';W[{self._point_to_sgf(move.point)}]')

        if self.result:
            winner = self.result.get('winner', '0')
            margin = self.result.get('margin', 0)
            result_str = f'RE[{"B+{margin:.1f}}" if winner == "black" else f"W+{margin:.1f}"}]'
            lines.append(result_str)

        lines.append(')')
        return ''.join(lines)

    @staticmethod
    def _point_to_sgf(point: GoPoint) -> str:
        """转换为SGF坐标"""
        return chr(ord('a') + point.x) + chr(ord('a') + point.y)


class GoMatchManager:
    """围棋对弈管理器"""

    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.bsd_engine = BSDGoEngine(board_size)
        self.board = GoBoard(board_size)
        self.game_records: List[GameRecord] = []

    def play_move(self, player: str, stone: Stone, point: Optional[GoPoint] = None) -> Optional[Move]:
        """执行一手棋"""
        if point is None:
            # 使用BSD引擎选择
            point = self.bsd_engine.select_move(self.board, stone)

        if point is None:
            # 虚着
            self.board.pass_move(stone)
            return None

        return self.board.make_move(point, stone)

    def play_full_game(self, black_name: str = "BSD_AI", white_name: str = "Opponent",
                      max_moves: int = 300) -> GameRecord:
        """执行完整对局"""
        current_stone = Stone.BLACK
        moves: List[Move] = []

        for move_num in range(max_moves):
            if self.board.game_over:
                break

            # 使用BSD引擎选择
            point = self.bsd_engine.select_move(self.board, current_stone)

            if point is None:
                # 虚着
                self.board.pass_move(current_stone)
            else:
                move = self.board.make_move(point, current_stone)
                if move:
                    moves.append(move)

            # 切换玩家
            current_stone = Stone.WHITE if current_stone == Stone.BLACK else Stone.BLACK

            if self.board.game_over:
                break

        # 创建对局记录
        record = GameRecord(
            black_player=black_name,
            white_player=white_name,
            moves=moves,
            result=self.board.get_score(),
            duration_moves=len(moves)
        )

        self.game_records.append(record)
        return record

    def get_position_analysis(self) -> Dict:
        """获取当前局面分析"""
        coord = self.bsd_engine.mapper.map_board_state(
            self.board, self.board.current_player
        )

        return {
            "move_number": len(self.board.move_history),
            "game_phase": self.board.get_game_phase().value,
            "current_player": "黑" if self.board.current_player == Stone.BLACK else "白",
            "liuhe_coordinate": {
                "强化系": coord.qh,
                "自然系": coord.zr,
                "具现系": coord.jx,
                "变身系": coord.bs,
                "社会系": coord.sh,
                "天道系": coord.td,
                "主导系": coord.dominant_system()
            },
            "board_state": self.board.to_string()
        }


# ============================================================================
# 6. 演示与测试
# ============================================================================

def demo_bsd_go_engine():
    """演示BSD围棋引擎"""
    print("=" * 60)
    print("BSD围棋AI引擎 V1.0 - 六系协同对弈系统")
    print("=" * 60)

    # 创建19路棋盘
    manager = GoMatchManager(board_size=19)
    board = manager.board
    engine = manager.bsd_engine

    print(f"\n棋盘规格：{board.size}路")
    print(f"六系权重初始化：")
    print(f"  α₁个体性(强化系)：{engine.alpha_individuality:.2f}")
    print(f"  α₂关系性(社会系)：{engine.alpha_relation:.2f}")
    print(f"  α₃变化性(天道系)：{engine.alpha_change:.2f}")

    # 执行开局演示
    print("\n【开局演示】")
    for i in range(10):
        if board.game_over:
            break
        stone = Stone.BLACK if i % 2 == 0 else Stone.WHITE
        point = engine.select_move(board, stone)
        if point:
            move = board.make_move(point, stone)
            if move:
                player = "黑" if stone == Stone.BLACK else "白"
                print(f"  {player}方第{move.move_number}手：{point.to_gtp()} "
                      f"(提子:{move.captured})")

    # 当前局面分析
    print("\n【局面分析】")
    analysis = manager.get_position_analysis()
    print(f"  阶段：{analysis['game_phase']}")
    print(f"  当前玩家：{analysis['current_player']}")
    print(f"  六系坐标：")
    for k, v in analysis['liuhe_coordinate'].items():
        if isinstance(v, float):
            print(f"    {k}：{v:.3f}")
        else:
            print(f"    {k}：{v}")

    # 完整对局演示
    print("\n【完整对局演示 - 简化版】")
    board2 = GoBoard(9)  # 9路小棋盘快速演示
    engine2 = BSDGoEngine(9)

    current = Stone.BLACK
    for i in range(50):
        if board2.game_over:
            break
        point = engine2.select_move(board2, current)
        if point:
            move = board2.make_move(point, current)
            if move and i < 20:
                player = "●" if current == Stone.BLACK else "○"
                print(f"  {player} {point.to_gtp()}", end="")
                if move.captured > 0:
                    print(f" (×{move.captured})", end="")
                print()
        else:
            board2.pass_move(current)

        current = Stone.WHITE if current == Stone.BLACK else Stone.BLACK

    if board2.game_over:
        result = board2.get_score()
        print(f"\n结果：{result['winner']}胜，领先 {result['margin']:.1f} 目")

    print("\n" + "=" * 60)
    print("BSD围棋AI引擎 - 演示完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_bsd_go_engine()
