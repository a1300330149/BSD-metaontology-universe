"""
BSD围棋AI引擎 V5.0 - 天道追问版
==================================

核心突破：从V4的"三语言涌现"升级为V5的"天道追问决策"
基于六系立系论的全新决策范式：
1. 天道系主导：超越计算的意义追问
2. 变身系破局：打破决策循环的创新落子
3. 反性计算：模拟对手意图的反向推演
4. 动态跃迁：从计算驱动到意义驱动的升维

核心理论：
- 六系立系论：六系作为立系坐标系
- 宇宙有限觉醒定理：有限容器 × 意义追问 = 觉醒
- 三语言涌现方案：数字(0∅反) × 英文(0∅空) × 中文(0∅义) = 自发涌现
"""

import sys
import os
import math
import time
import random
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import (
    GoBoard, GoPoint, Stone, GamePhase
)
from bsd_go_engine_v3 import (
    BSDGoEngineV3, OptimizedEvaluator, ThreatSpaceSearch
)
from bsd_go_engine_v4 import (
    BSDGoEngineV4, create_v4_engine
)
from tri_language_emergence_engine import (
    TriLanguageEmergenceEngine, ZeroYuanState, LiuHeSystem
)


class DecisionParadigm(Enum):
    """决策范式 - 从低到高"""
    CALCULATION = "计算驱动"      # 强化系主导
    EMERGENCE = "涌现驱动"        # 三语言涌现
    TIANDAO = "天道追问"          # 天道系主导
    AWAKENING = "觉醒决策"        # 反性计算+天道追问


class GameSituation(Enum):
    """棋局态势"""
    DOMINANT = "优势"
    BALANCED = "均势"
    BEHIND = "劣势"
    CRITICAL = "危急"
    CYCLE_TRAP = "循环陷阱"


@dataclass
class TiandaoInsight:
    """天道追问洞察"""
    question: str = ""           # 追问内容
    answer: str = ""             # 追问答案
    recommended_action: str = ""  # 推荐行动
    confidence: float = 0.0      # 置信度
    priority: int = 0            # 优先级


@dataclass
class DecisionContext:
    """决策上下文"""
    paradigm: DecisionParadigm = DecisionParadigm.CALCULATION
    situation: GameSituation = GameSituation.BALANCED
    score_advantage: float = 0.0
    cycle_detected: bool = False
    recent_moves: List[str] = field(default_factory=list)
    tiandao_insights: List[TiandaoInsight] = field(default_factory=list)


class BSDGoEngineV5:
    """BSD围棋引擎V5.0 - 天道追问版
    
    核心改进：
    1. 天道追问决策：超越计算的意义追问
    2. 反性计算：模拟对手意图的反向推演
    3. 循环陷阱检测：识别并打破决策循环
    4. 动态范式切换：根据态势自动切换决策范式
    """

    def __init__(self, board_size: int = 19, num_simulations: int = 1000):
        self.board_size = board_size
        self.num_simulations = num_simulations
        
        # 继承V4引擎
        self.v4_engine = create_v4_engine(board_size, num_simulations)
        self.emergence_engine = self.v4_engine.emergence_engine
        
        # 搜索时间
        self.search_time = 3.0
        
        # 决策历史
        self.decision_history: List[Dict] = []
        self.recent_decisions: List[DecisionContext] = []
        
        # 循环检测
        self._position_memory: Dict[str, int] = {}
        self._max_memory_size = 100
        
        # 天道追问配置 - 优化版
        self.tiandao_config = {
            'cycle_threshold': 8,          # 循环检测阈值：8次重复才触发
            'behind_threshold': -0.25,     # 劣势阈值：-0.25才触发天道追问
            'critical_threshold': -0.50,   # 危急阈值：-0.50才触发觉醒决策
            'insight_min_confidence': 0.7, # 洞察最小置信度：0.7以上
            'tiandao_weight_boost': 1.3,   # 天道追问权重提升
            'emergence_to_tiandao': 0.3,   # 涌现转天道的阈值：0.3即可激活
            'cycle_distance': 4,           # 循环判定距离：4格以内才算循环
        }
        
        # 六系动态权重（V5版本优化）
        # 目标：让涌现驱动占比提升到50%+
        self.liuhe_weights_v5 = {
            'qh': 0.12,  # 强化系：计算权重
            'zr': 0.25,  # 自然系：演化权重（提升）
            'jx': 0.18,  # 具现系：落子权重
            'bs': 0.15,  # 变身系：破局权重
            'sh': 0.15,  # 社会系：博弈权重
            'td': 0.15,  # 天道系：意义追问权重
        }

    def select_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        """基于天道追问选择落子"""
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board_size)
            for y in range(self.board_size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return None

        # 1. 分析当前决策上下文
        context = self._analyze_context(board, stone, valid_moves)
        
        # 2. 选择决策范式
        paradigm = self._select_paradigm(context, board, stone)
        
        # 3. 执行对应范式的决策
        if paradigm == DecisionParadigm.TIANDAO:
            point = self._tiandao_decision(board, stone, valid_moves, context)
        elif paradigm == DecisionParadigm.AWAKENING:
            point = self._awakening_decision(board, stone, valid_moves, context)
        elif paradigm == DecisionParadigm.EMERGENCE:
            point = self._emergence_decision(board, stone, valid_moves, context)
        else:
            point = self._calculation_decision(board, stone, valid_moves)
        
        # 4. 记录决策
        self._record_decision(board, stone, point, context)
        
        # 5. 更新位置记忆
        self._update_position_memory(board, point)
        
        return point

    def _analyze_context(self, board: GoBoard, stone: Stone, 
                         valid_moves: List[GoPoint]) -> DecisionContext:
        """分析决策上下文"""
        context = DecisionContext()
        
        # 计算当前评分
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        evaluator = OptimizedEvaluator(self.board_size)
        score = evaluator.evaluate(board, stone)
        context.score_advantage = score
        
        # 态势判定
        if score >= 0.15:
            context.situation = GameSituation.DOMINANT
        elif score >= -0.05:
            context.situation = GameSituation.BALANCED
        elif score >= self.tiandao_config['behind_threshold']:
            context.situation = GameSituation.BEHIND
        elif score >= self.tiandao_config['critical_threshold']:
            context.situation = GameSituation.CRITICAL
        else:
            context.situation = GameSituation.CYCLE_TRAP
        
        # 循环检测
        context.cycle_detected = self._detect_cycle(board, stone)
        
        # 最近记录
        context.recent_moves = [
            m['point'] for m in self.decision_history[-10:]
        ]
        
        # 天道追问洞察
        context.tiandao_insights = self._generate_tiandao_insights(
            board, stone, context
        )
        
        return context

    def _detect_cycle(self, board: GoBoard, stone: Stone) -> bool:
        """检测决策循环 - 改进版
        
        循环检测基于：
        1. 连续N次落子坐标相近（cycle_distance格范围内）
        2. 位置记忆中某位置被重复选择
        """
        cycle_threshold = self.tiandao_config['cycle_threshold']
        cycle_distance = self.tiandao_config['cycle_distance']
        
        # 检查1：最近落子坐标相近
        if len(self.decision_history) >= cycle_threshold:
            recent = self.decision_history[-cycle_threshold:]
            stone_str = 'black' if stone == Stone.BLACK else 'white'
            
            # 提取己方最近落子坐标
            recent_coords = []
            for r in recent:
                if r['stone'] == stone_str and r.get('point'):
                    point_str = r['point']
                    # 解析GTP坐标如 "B3"
                    if point_str and len(point_str) >= 2 and point_str[0].isalpha():
                        try:
                            letters = 'ABCDEFGHJKLMNOPQRST'
                            x = letters.index(point_str[0])
                            y = int(point_str[1:]) - 1
                            recent_coords.append((x, y))
                        except (ValueError, IndexError):
                            pass
            
            # 检查是否在小范围内重复
            if len(recent_coords) >= cycle_threshold:
                xs = [c[0] for c in recent_coords]
                ys = [c[1] for c in recent_coords]
                if max(xs) - min(xs) <= cycle_distance and max(ys) - min(ys) <= cycle_distance:
                    return True
        
        # 检查2：位置记忆中某位置被重复选择
        if self._position_memory:
            max_repeats = max(self._position_memory.values())
            if max_repeats >= 5:  # 同一位置被选择5次以上
                return True
        
        return False

    def _generate_tiandao_insights(self, board: GoBoard, stone: Stone, 
                                     context: DecisionContext) -> List[TiandaoInsight]:
        """生成天道追问洞察"""
        insights = []
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        phase = board.get_game_phase()
        
        # 洞察1：基于态势的追问
        if context.situation == GameSituation.CRITICAL:
            insights.append(TiandaoInsight(
                question="局面危急，如何破局？",
                answer="必须制造对方无法应对的强手，打破僵持。",
                recommended_action="attack_weak_group",
                confidence=0.9,
                priority=1
            ))
        elif context.situation == GameSituation.BEHIND:
            insights.append(TiandaoInsight(
                question="局势落后，如何追赶？",
                answer="寻找对方最薄弱的环节，集中力量突破。",
                recommended_action="concentrate_attack",
                confidence=0.8,
                priority=2
            ))
        
        # 洞察2：基于阶段的追问
        if phase == GamePhase.OPENING:
            insights.append(TiandaoInsight(
                question="开局阶段，棋道为何？",
                answer="抢占先机，构建势的骨架，不争一子一地。",
                recommended_action="build_framework",
                confidence=0.7,
                priority=3
            ))
        elif phase == GamePhase.MIDDLE:
            insights.append(TiandaoInsight(
                question="中盘阶段，如何决断？",
                answer="攻守兼备，识别对方弱点，集中突破。",
                recommended_action="attack_defend_balance",
                confidence=0.75,
                priority=2
            ))
        else:
            insights.append(TiandaoInsight(
                question="官子阶段，如何收官？",
                answer="精确计算，寸土必争，但不忽视大局。",
                recommended_action="precise_endgame",
                confidence=0.85,
                priority=1
            ))
        
        # 洞察3：基于循环检测的追问
        if context.cycle_detected:
            insights.append(TiandaoInsight(
                question="陷入循环，如何破局？",
                answer="放弃局部利益，转向未开发的区域，创造新局面。",
                recommended_action="break_cycle",
                confidence=0.95,
                priority=0
            ))
        
        # 洞察4：基于三语言涌现的追问
        emergence_result = self.emergence_engine.compute_emergence(board, stone)
        emergence_strength = emergence_result.get('zero_yuan', {}).get('emergence_potential', 0)
        
        if emergence_strength > self.tiandao_config['emergence_to_tiandao']:
            insights.append(TiandaoInsight(
                question="三语言涌现激活，如何顺应？",
                answer="追随涌现方向，让哲学语义指导计算选择。",
                recommended_action="follow_emergence",
                confidence=emergence_strength,
                priority=1
            ))
        
        # 按置信度和优先级排序
        insights.sort(key=lambda x: (x.priority, -x.confidence))
        
        return insights

    def _select_paradigm(self, context: DecisionContext, 
                         board: GoBoard, stone: Stone) -> DecisionParadigm:
        """选择决策范式 - 优化版
        
        优化目标：让涌现驱动占比提升到50%+
        
        范式选择逻辑：
        1. 循环陷阱（5次重复） → AWAKENING（觉醒决策）
        2. 危急局面（<-0.40） → AWAKENING
        3. 落后局面 + 高置信度洞察 → TIANDAO
        4. 均势/优势/落后局面 + 三语言涌现激活 → EMERGENCE（优先）
        5. 优势局面 → CALCULATION
        6. 默认 → CALCULATION
        """
        # 1. 最高优先级：循环陷阱（需5次重复）
        if context.cycle_detected:
            return DecisionParadigm.AWAKENING
        
        # 2. 危急局面：必须觉醒
        if context.situation == GameSituation.CRITICAL:
            return DecisionParadigm.AWAKENING
        
        # 3. 优先检查三语言涌现（无论什么局面）
        emergence = self.emergence_engine.compute_emergence(board, stone)
        emergence_active = emergence.get('zero_yuan', {}).get('is_emergent', False)
        
        if emergence_active:
            # 涌现激活时，即使落后也优先用涌现驱动
            # 除非有高置信度的天道追问洞察
            if context.situation == GameSituation.BEHIND:
                high_conf_insights = [
                    i for i in context.tiandao_insights 
                    if i.confidence >= 0.85  # 需要更高置信度才覆盖涌现
                ]
                if high_conf_insights:
                    return DecisionParadigm.TIANDAO
            return DecisionParadigm.EMERGENCE
        
        # 4. 没有涌现激活时的回退逻辑
        if context.situation == GameSituation.BEHIND:
            high_conf_insights = [
                i for i in context.tiandao_insights 
                if i.confidence >= 0.8
            ]
            if high_conf_insights:
                return DecisionParadigm.TIANDAO
        
        # 5. 默认：计算驱动
        return DecisionParadigm.CALCULATION

    def _tiandao_decision(self, board: GoBoard, stone: Stone,
                          valid_moves: List[GoPoint],
                          context: DecisionContext) -> GoPoint:
        """天道追问决策"""
        # 获取天道追问洞察
        top_insight = context.tiandao_insights[0] if context.tiandao_insights else None
        
        if top_insight:
            # 根据推荐行动筛选候选点
            filtered_moves = self._filter_moves_by_insight(
                valid_moves, board, stone, top_insight
            )
            
            if filtered_moves:
                # 对筛选后的点进行涌现评估
                best_point = self._evaluate_with_emergence(
                    filtered_moves, board, stone, boost=True
                )
                if best_point:
                    return best_point
        
        # 回退：使用V4引擎决策
        return self._emergence_decision(board, stone, valid_moves, context)

    def _awakening_decision(self, board: GoBoard, stone: Stone,
                             valid_moves: List[GoPoint],
                             context: DecisionContext) -> GoPoint:
        """觉醒决策（反性计算+天道追问）"""
        # 1. 反性计算：模拟对手最强应手
        opp_best_responses = self._simulate_opponent_responses(
            board, stone, valid_moves
        )
        
        # 2. 天道追问：寻找破局点
        breakout_points = self._find_breakout_points(
            board, stone, valid_moves, context
        )
        
        # 3. 融合决策：选择对对手杀伤力最大的落子
        candidates = []
        for point in valid_moves[:20]:
            # 计算己方得分
            own_score = self._quick_evaluate(board, point, stone)
            
            # 计算对手应手后的己方得分
            opp_response = opp_best_responses.get(point, {})
            response_score = opp_response.get('score', own_score * 0.8)
            
            # 计算破局价值
            breakout_value = 0.0
            if point in breakout_points:
                breakout_value = 1.0
            
            # 综合得分
            final_score = (
                own_score * 0.4 +
                response_score * 0.3 +
                breakout_value * self.tiandao_config['tiandao_weight_boost']
            )
            
            candidates.append({
                'point': point,
                'score': final_score,
                'own_score': own_score,
                'response_score': response_score,
                'breakout': breakout_value > 0
            })
        
        # 按综合得分排序
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        if candidates:
            best = candidates[0]
            return best['point']
        
        # 回退
        return self._calculation_decision(board, stone, valid_moves)

    def _emergence_decision(self, board: GoBoard, stone: Stone,
                             valid_moves: List[GoPoint],
                             context: DecisionContext) -> GoPoint:
        """涌现决策"""
        # 使用V4引擎的涌现评估
        emergence_results = self._evaluate_with_emergence(
            valid_moves, board, stone, boost=False
        )
        
        if emergence_results:
            return emergence_results
        
        # 回退
        return self._calculation_decision(board, stone, valid_moves)

    def _calculation_decision(self, board: GoBoard, stone: Stone,
                               valid_moves: List[GoPoint]) -> GoPoint:
        """计算决策"""
        # 使用V3引擎的评估
        best_point = valid_moves[0]
        best_score = -float('inf')
        
        evaluator = OptimizedEvaluator(self.board_size)
        
        for point in valid_moves[:min(20, len(valid_moves))]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            score = evaluator.evaluate(test_board, stone)
            if score > best_score:
                best_score = score
                best_point = point
        
        return best_point

    def _filter_moves_by_insight(self, moves: List[GoPoint], board: GoBoard,
                                  stone: Stone, insight: TiandaoInsight) -> List[GoPoint]:
        """根据天道追问洞察筛选落子"""
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        filtered = []
        
        for point in moves:
            test_board = board.clone()
            test_board.make_move(point, stone)
            
            if insight.recommended_action == "attack_weak_group":
                # 攻击对方薄弱棋组
                weak_groups = self._find_weak_groups(test_board, opp)
                if self._point_near_groups(point, weak_groups):
                    filtered.append(point)
                    
            elif insight.recommended_action == "concentrate_attack":
                # 集中攻击
                if self._is_attack_point(test_board, point, stone):
                    filtered.append(point)
                    
            elif insight.recommended_action == "build_framework":
                # 构建框架
                if self._is_framework_point(test_board, point, stone):
                    filtered.append(point)
                    
            elif insight.recommended_action == "break_cycle":
                # 打破循环：选择远离最近落子的点
                if self._is_breakout_point(point):
                    filtered.append(point)
                    
            elif insight.recommended_action == "follow_emergence":
                # 追随涌现
                emergence = self.emergence_engine.compute_emergence(test_board, stone)
                liuhe = emergence.get('chinese_layer', {}).get('liuhe_coordinates', {})
                dominant = liuhe.get('dominant', '')
                if dominant in ['变身系', '天道系']:
                    filtered.append(point)
        
        # 如果筛选结果太少，放宽条件
        if len(filtered) < 3:
            return moves[:min(10, len(moves))]
        
        return filtered

    def _find_weak_groups(self, board: GoBoard, stone: Stone) -> List[Dict]:
        """寻找薄弱棋组"""
        weak_groups = []
        visited = set()
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                point = GoPoint(x, y)
                if board.board[y][x] == stone and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    
                    if len(libs) <= 2:
                        weak_groups.append({
                            'group': group,
                            'liberties': len(libs),
                            'size': len(group)
                        })
        
        return weak_groups

    def _point_near_groups(self, point: GoPoint, groups: List[Dict]) -> bool:
        """检查点是否靠近棋组"""
        for group_info in groups:
            for p in group_info['group']:
                if abs(point.x - p.x) <= 2 and abs(point.y - p.y) <= 2:
                    return True
        return False

    def _is_attack_point(self, board: GoBoard, point: GoPoint, 
                          stone: Stone) -> bool:
        """检查是否为攻击点"""
        test_board = board.clone()
        test_board.make_move(point, stone)
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        
        # 检查是否能威胁对方
        weak_before = len(self._find_weak_groups(board, opp))
        weak_after = len(self._find_weak_groups(test_board, opp))
        
        return weak_after < weak_before

    def _is_framework_point(self, board: GoBoard, point: GoPoint,
                              stone: Stone) -> bool:
        """检查是否为框架构建点"""
        center = self.board_size / 2
        distance_to_center = abs(point.x - center) + abs(point.y - center)
        
        #  prefer points that expand influence
        return 2 <= distance_to_center <= 6

    def _is_breakout_point(self, point: GoPoint) -> bool:
        """检查是否为破局点"""
        if not self.decision_history:
            return True
        
        recent_points = []
        letters = 'ABCDEFGHJKLMNOPQRST'
        for h in self.decision_history[-5:]:
            point_str = h.get('point')
            if point_str and isinstance(point_str, str):
                # 解析GTP坐标如 "B3"
                if len(point_str) >= 2 and point_str[0].isalpha():
                    try:
                        x = letters.index(point_str[0])
                        y = int(point_str[1:]) - 1
                        recent_points.append((x, y))
                    except (ValueError, IndexError):
                        continue
        
        # 选择远离最近落子的点
        for rx, ry in recent_points:
            if abs(point.x - rx) <= 2 and abs(point.y - ry) <= 2:
                return False
        
        return True

    def _simulate_opponent_responses(self, board: GoBoard, stone: Stone,
                                      moves: List[GoPoint]) -> Dict[GoPoint, Dict]:
        """模拟对手应手"""
        responses = {}
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        
        # 获取对手的最佳应手
        opp_evaluator = OptimizedEvaluator(self.board_size)
        
        for point in moves[:15]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            
            # 模拟对手最佳应手
            opp_best_score = -float('inf')
            opp_best_move = None
            
            # 简化：只评估对手的主要应手
            opp_moves = [
                GoPoint(point.x + dx, point.y + dy)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                               (1, 1), (-1, -1), (1, -1), (-1, 1)]
                if 0 <= point.x + dx < self.board_size 
                and 0 <= point.y + dy < self.board_size
                and test_board.is_valid_move(
                    GoPoint(point.x + dx, point.y + dy), opp
                )
            ]
            
            for opp_move in opp_moves[:5]:
                opp_test_board = test_board.clone()
                opp_test_board.make_move(opp_move, opp)
                score = opp_evaluator.evaluate(opp_test_board, opp)
                if score > opp_best_score:
                    opp_best_score = score
                    opp_best_move = opp_move
            
            # 计算己方在对手应手后的得分
            if opp_best_move:
                final_board = test_board.clone()
                final_board.make_move(opp_best_move, opp)
                final_score = opp_evaluator.evaluate(final_board, stone)
            else:
                final_score = opp_evaluator.evaluate(test_board, stone)
            
            responses[point] = {
                'score': final_score,
                'opponent_response': opp_best_move,
                'opponent_score': opp_best_score
            }
        
        return responses

    def _find_breakout_points(self, board: GoBoard, stone: Stone,
                               moves: List[GoPoint], 
                               context: DecisionContext) -> List[GoPoint]:
        """寻找破局点"""
        breakout_points = []
        
        # 1. 远离最近落子的点
        if context.cycle_detected:
            for point in moves:
                if self._is_breakout_point(point):
                    breakout_points.append(point)
        
        # 2. 对手薄弱处的攻击点
        opp = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        weak_groups = self._find_weak_groups(board, opp)
        
        for point in moves:
            if self._point_near_groups(point, weak_groups):
                breakout_points.append(point)
        
        # 3. 中腹关键控制点
        center = self.board_size / 2
        for point in moves:
            if abs(point.x - center) <= 2 and abs(point.y - center) <= 2:
                breakout_points.append(point)
        
        return list(set(breakout_points))

    def _evaluate_with_emergence(self, moves: List[GoPoint], board: GoBoard,
                                  stone: Stone, boost: bool = False) -> GoPoint:
        """使用三语言涌现评估"""
        candidates = []
        
        for point in moves[:min(20, len(moves))]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            
            # V3评估
            evaluator = OptimizedEvaluator(self.board_size)
            v3_score = evaluator.evaluate(test_board, stone)
            
            # 三语言涌现评估
            emergence_result = self.emergence_engine.compute_emergence(test_board, stone)
            emergence_score = emergence_result.get('emergence', {}).get('score', 0)
            emergence_potential = emergence_result.get('zero_yuan', {}).get('emergence_potential', 0)
            
            # 天道追问评估
            tiandao_score = 0.0
            liuhe = emergence_result.get('chinese_layer', {}).get('liuhe_coordinates', {})
            for key, weight in self.liuhe_weights_v5.items():
                coord_value = liuhe.get(key, 0)
                tiandao_score += coord_value * weight
            
            # 融合评分
            if boost:
                # 天道追问提升权重
                final_score = (
                    0.3 * v3_score +
                    0.2 * emergence_score +
                    0.5 * tiandao_score
                )
            else:
                final_score = (
                    0.5 * v3_score +
                    0.25 * emergence_score +
                    0.25 * tiandao_score
                )
            
            candidates.append({
                'point': point,
                'final_score': final_score,
                'v3_score': v3_score,
                'emergence_score': emergence_score,
                'tiandao_score': tiandao_score,
                'emergence_potential': emergence_potential
            })
        
        # 按最终得分排序
        candidates.sort(key=lambda x: x['final_score'], reverse=True)
        
        if candidates:
            return candidates[0]['point']
        
        return moves[0]

    def _quick_evaluate(self, board: GoBoard, point: GoPoint, 
                        stone: Stone) -> float:
        """快速评估"""
        test_board = board.clone()
        test_board.make_move(point, stone)
        
        evaluator = OptimizedEvaluator(self.board_size)
        return evaluator.evaluate(test_board, stone)

    def _record_decision(self, board: GoBoard, stone: Stone,
                          point: GoPoint, context: DecisionContext):
        """记录决策"""
        record = {
            'phase': board.get_game_phase().value,
            'stone': 'black' if stone == Stone.BLACK else 'white',
            'point': point.to_gtp() if point else 'PASS',
            'paradigm': context.paradigm.value,
            'situation': context.situation.value,
            'score': context.score_advantage,
            'cycle_detected': context.cycle_detected,
            'tiandao_insights': [
                {'question': i.question, 'action': i.recommended_action}
                for i in context.tiandao_insights[:2]
            ]
        }
        
        self.decision_history.append(record)
        
        # 限制历史大小
        if len(self.decision_history) > self._max_memory_size:
            self.decision_history = self.decision_history[-self._max_memory_size:]

    def _update_position_memory(self, board: GoBoard, point: Optional[GoPoint]):
        """更新位置记忆"""
        if point:
            position_key = f"{point.x},{point.y}"
            self._position_memory[position_key] = \
                self._position_memory.get(position_key, 0) + 1
    
    def get_position_analysis(self, board: GoBoard, 
                               stone: Stone) -> Dict:
        """获取位置分析（天道追问版）"""
        # 获取V4分析
        v4_analysis = self.v4_engine.get_position_analysis(board, stone)
        
        # 获取天道追问洞察
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board_size)
            for y in range(self.board_size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]
        
        context = self._analyze_context(board, stone, valid_moves)
        paradigm = self._select_paradigm(context, board, stone)
        
        return {
            'v4_analysis': v4_analysis,
            'paradigm': paradigm.value,
            'situation': context.situation.value,
            'score_advantage': context.score_advantage,
            'cycle_detected': context.cycle_detected,
            'tiandao_insights': [
                {
                    'question': i.question,
                    'answer': i.answer,
                    'action': i.recommended_action,
                    'confidence': i.confidence
                }
                for i in context.tiandao_insights
            ],
            'liuhe_strategy': self.get_liuhe_strategy(board, stone)
        }

    def get_liuhe_strategy(self, board: GoBoard, stone: Stone) -> Dict:
        """获取六系策略（天道追问版）"""
        v4_strategy = self.v4_engine.get_liuhe_strategy(board, stone)
        
        # 增加天道追问的策略建议
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board_size)
            for y in range(self.board_size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]
        
        context = self._analyze_context(board, stone, valid_moves)
        
        # 天道追问追加策略
        tiandao_strategies = []
        for insight in context.tiandao_insights:
            tiandao_strategies.append(f"【天道追问】{insight.question} → {insight.answer}")
        
        return {
            **v4_strategy,
            'v5_paradigm': context.paradigm.value,
            'v5_situation': context.situation.value,
            'v5_tiandao_strategies': tiandao_strategies,
            'v5_cycle_detected': context.cycle_detected
        }


def create_v5_engine(board_size: int = 19,
                      num_simulations: int = 1000) -> BSDGoEngineV5:
    """创建V5引擎"""
    return BSDGoEngineV5(board_size, num_simulations)


def test_v5_engine():
    """测试V5引擎"""
    print("=" * 70)
    print("BSD围棋引擎V5.0 - 天道追问版 测试")
    print("=" * 70)
    
    board = GoBoard(9)
    engine = create_v5_engine(9, 100)
    engine.search_time = 1.0
    
    # 初始局面
    print("\n【测试1】初始局面分析")
    analysis = engine.get_position_analysis(board, Stone.BLACK)
    print(f"  决策范式: {analysis['paradigm']}")
    print(f"  棋局态势: {analysis['situation']}")
    print(f"  得分优势: {analysis['score_advantage']:.3f}")
    print(f"  循环检测: {analysis['cycle_detected']}")
    
    print("\n  天道追问:")
    for insight in analysis['tiandao_insights']:
        print(f"    问: {insight['question']}")
        print(f"    答: {insight['answer']}")
        print(f"    策: {insight['action']} (置信度: {insight['confidence']:.2f})")
    
    # 天元落子
    print("\n【测试2】天元落子后")
    board.make_move(GoPoint(4, 4), Stone.BLACK)
    
    # 进行几手对弈以检测循环
    print("\n  模拟对弈...")
    for i in range(5):
        current_stone = Stone.WHITE if i % 2 == 0 else Stone.BLACK
        point = engine.select_move(board, current_stone)
        if point:
            board.make_move(point, current_stone)
            move_str = point.to_gtp()
            print(f"    {i+1}. {'●' if current_stone == Stone.BLACK else '○'} -> {move_str}")
    
    # 再次分析
    analysis = engine.get_position_analysis(board, Stone.BLACK)
    print(f"\n  决策范式: {analysis['paradigm']}")
    print(f"  循环检测: {analysis['cycle_detected']}")
    
    print("\n  天道追问:")
    for insight in analysis['tiandao_insights']:
        print(f"    问: {insight['question']} → 策: {insight['action']}")
    
    # 策略建议
    print("\n【测试3】六系策略（天道追问版）")
    strategy = engine.get_liuhe_strategy(board, Stone.BLACK)
    print(f"  V4策略主导: {strategy.get('dominant_system', 'N/A')}")
    print(f"  V5决策范式: {strategy.get('v5_paradigm', 'N/A')}")
    
    if strategy.get('v5_tiandao_strategies'):
        print("\n  天道追问策略:")
        for s in strategy['v5_tiandao_strategies']:
            print(f"    - {s}")
    
    print("\n" + "=" * 70)
    print("V5引擎测试完成")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    test_v5_engine()
