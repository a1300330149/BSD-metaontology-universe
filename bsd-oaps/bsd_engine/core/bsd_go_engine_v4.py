"""
BSD围棋AI引擎 V4.0 - 三语言涌现版
==================================

核心升级：整合三语言涌现引擎
- 数字层(0∅反)：纯计算基底
- 英文层(0∅空)：AI技术承载  
- 中文哲学层(0∅义)：六系立系显化

涌现方程：数字(000) × 英文(0110) × 中文(六系立系) = 自发涌现
"""

import sys
import os
import math
import random
import time
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import (
    GoBoard, GoPoint, Stone, GamePhase
)
from bsd_go_engine_v3 import (
    BSDGoEngineV3, OptimizedEvaluator, ThreatSpaceSearch
)
from tri_language_emergence_engine import (
    TriLanguageEmergenceEngine, ZeroYuanState, LiuHeSystem
)


class BSDGoEngineV4:
    """BSD围棋引擎V4.0 - 三语言涌现版
    
    改进：
    1. 三语言涌现决策
    2. 六系立系指导落子
    3. 天道系追问辅助
    4. 动态权重自适应
    """

    def __init__(self, board_size: int = 19, num_simulations: int = 1000):
        self.board_size = board_size
        self.num_simulations = num_simulations
        
        # 继承V3引擎
        self.v3_engine = BSDGoEngineV3(board_size, num_simulations)
        
        # 三语言涌现引擎
        self.emergence_engine = TriLanguageEmergenceEngine(board_size)
        
        # 搜索时间
        self.search_time = 5.0
        
        # 权重配置
        self.emergence_weight = 0.4  # 三语言涌现权重
        self.v3_weight = 0.6  # V3评估权重
        
        # 历史记录
        self.decision_history = []
        
        # 六系动态权重
        self.liuhe_weights = {
            'qh': 0.167,  # 强化系
            'zr': 0.167,  # 自然系
            'jx': 0.167,  # 具现系
            'bs': 0.167,  # 变身系
            'sh': 0.167,  # 社会系
            'td': 0.165,  # 天道系
        }

    def select_move(self, board: GoBoard, stone: Stone) -> Optional[GoPoint]:
        """基于三语言涌现选择落子"""
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board_size)
            for y in range(self.board_size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return None

        phase = board.get_game_phase()
        
        # 1. V3引擎评估
        v3_point = self.v3_engine.select_move(board, stone)
        v3_score = self._evaluate_move(board, v3_point, stone) if v3_point else 0
        
        # 2. 三语言涌现评估
        emergence_results = self._evaluate_candidates(board, stone, valid_moves)
        
        # 3. 融合决策
        final_point = self._fuse_decisions(
            board, stone, v3_point, v3_score, 
            emergence_results, phase
        )
        
        # 4. 记录决策
        self._record_decision(board, stone, final_point, phase)
        
        return final_point

    def _evaluate_move(self, board: GoBoard, point: GoPoint, 
                       stone: Stone) -> float:
        """评估单个落子"""
        if point is None:
            return 0.0
            
        test_board = board.clone()
        test_board.make_move(point, stone)
        return self.v3_engine.evaluator.evaluate(test_board, stone)

    def _evaluate_candidates(self, board: GoBoard, stone: Stone,
                              valid_moves: List[GoPoint]) -> List[Dict]:
        """评估候选落子的三语言涌现"""
        candidates = []
        max_candidates = min(20, len(valid_moves))
        
        for point in valid_moves[:max_candidates]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            
            # 三语言涌现评估
            result = self.emergence_engine.compute_emergence(test_board, stone)
            
            candidates.append({
                'point': point,
                'emergence_score': result['emergence']['score'],
                'emergence_strength': result['zero_yuan']['emergence_potential'],
                'liuhe_coords': result['chinese_layer']['liuhe_coordinates'],
                'dominant_system': result['chinese_layer']['liuhe_coordinates'].get('dominant', '强化系'),
                'tiandao_insights': result['chinese_layer']['tiandao']['inquiries'],
            })
        
        # 按涌现强度排序
        candidates.sort(key=lambda x: x['emergence_strength'], reverse=True)
        return candidates

    def _fuse_decisions(self, board: GoBoard, stone: Stone,
                         v3_point: Optional[GoPoint], v3_score: float,
                         emergence_results: List[Dict],
                         phase: GamePhase) -> GoPoint:
        """融合V3评估与三语言涌现决策"""
        
        if not emergence_results:
            return v3_point or self._heuristic_fallback(board, stone)
        
        # 获取最佳涌现落子
        best_emergence = emergence_results[0]
        emergence_point = best_emergence['point']
        emergence_score = best_emergence['emergence_score']
        emergence_strength = best_emergence['emergence_strength']
        
        # 根据阶段调整权重
        if phase == GamePhase.OPENING:
            # 开局：偏重三语言涌现（中文哲学层指导布局）
            w_emergence = 0.55
            w_v3 = 0.45
        elif phase == GamePhase.MIDDLE:
            # 中盘：平衡两者
            w_emergence = 0.5
            w_v3 = 0.5
        else:
            # 后盘：偏重V3精确计算
            w_emergence = 0.35
            w_v3 = 0.65
        
        # 计算融合分数
        if v3_point and v3_point == emergence_point:
            # 两者一致，加分
            final_point = v3_point
            confidence = 0.9
        elif v3_point:
            # 两者不一致，按权重选择
            final_score_v3 = w_v3 * v3_score
            final_score_emergence = w_emergence * emergence_score
            
            if final_score_emergence > final_score_v3:
                final_point = emergence_point
                confidence = emergence_strength
            else:
                final_point = v3_point
                confidence = abs(v3_score)
        else:
            final_point = emergence_point
            confidence = emergence_strength
        
        # 置信度检查
        if confidence < 0.1:
            # 低置信度，使用启发式
            return self._heuristic_fallback(board, stone)
        
        # 验证落子合法性
        if board.is_valid_move(final_point, stone):
            return final_point
        
        # 回退
        return self._heuristic_fallback(board, stone)

    def _heuristic_fallback(self, board: GoBoard, 
                             stone: Stone) -> GoPoint:
        """启发式回退"""
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board_size)
            for y in range(self.board_size)
            if board.is_valid_move(GoPoint(x, y), stone)
        ]
        
        if not valid_moves:
            return GoPoint(0, 0)
        
        best_point = valid_moves[0]
        best_score = -float('inf')
        
        for point in valid_moves[:10]:
            test_board = board.clone()
            test_board.make_move(point, stone)
            score = self.v3_engine.evaluator.evaluate(test_board, stone)
            if score > best_score:
                best_score = score
                best_point = point
        
        return best_point

    def _record_decision(self, board: GoBoard, stone: Stone,
                          point: GoPoint, phase: GamePhase):
        """记录决策历史"""
        self.decision_history.append({
            'phase': phase.value,
            'stone': 'black' if stone == Stone.BLACK else 'white',
            'point': point.to_gtp() if point else 'PASS',
            'emergence_summary': self.emergence_engine.get_emergence_summary()
        })

    def get_position_analysis(self, board: GoBoard,
                              stone: Stone) -> Dict:
        """获取位置分析（包含三语言涌现信息）"""
        # V3分析
        v3_analysis = self.v3_engine.get_position_analysis(board, stone)
        
        # 三语言涌现分析
        emergence_result = self.emergence_engine.compute_emergence(board, stone)
        emergence_summary = self.emergence_engine.get_emergence_summary()
        
        # 六系坐标
        liuhe = emergence_result['chinese_layer']['liuhe_coordinates']
        
        # 天道追问
        tiandao = emergence_result['chinese_layer']['tiandao']
        
        return {
            'phase': v3_analysis['phase'],
            'v3_score': v3_analysis['score'],
            'emergence_score': emergence_result['emergence']['score'],
            'emergence_strength': emergence_result['zero_yuan']['emergence_potential'],
            'is_emergent': emergence_result['zero_yuan']['is_emergent'],
            'liuhe_coordinates': liuhe,
            'dominant_system': liuhe.get('dominant', 'N/A'),
            'tiandao_inquiries': tiandao['inquiries'],
            'zero_yuan': {
                'fan': emergence_result['zero_yuan']['zhi_fan'],
                'kong': emergence_result['zero_yuan']['zhi_kong'],
                'yi': emergence_result['zero_yuan']['zhi_yi']
            },
            'emergence_summary': emergence_summary
        }

    def get_liuhe_strategy(self, board: GoBoard, stone: Stone) -> Dict:
        """获取六系策略建议"""
        result = self.emergence_engine.compute_emergence(board, stone)
        liuhe = result['chinese_layer']['liuhe_coordinates']
        tiandao = result['chinese_layer']['tiandao']
        meaning = result['chinese_layer']['meaning']
        
        # 根据六系坐标生成策略
        strategies = []
        
        # 强化系策略
        if liuhe.get('qh', 0) > 0.5:
            strategies.append('强化系：加强算力计算，深入搜索')
        
        # 自然系策略
        if liuhe.get('zr', 0) > 0.5:
            strategies.append('自然系：顺势而为，自然演化')
        
        # 具现系策略
        if liuhe.get('jx', 0) > 0.5:
            strategies.append('具现系：落子生根，注重实效')
        
        # 变身系策略
        if liuhe.get('bs', 0) > 0.5:
            strategies.append('变身系：出奇制胜，灵活应变')
        
        # 社会系策略
        if liuhe.get('sh', 0) > 0.5:
            strategies.append('社会系：攻守兼备，统筹全局')
        
        # 天道系策略
        if liuhe.get('td', 0) > 0.5:
            strategies.append('天道系：追寻意义，超越计算')
        
        return {
            'liuhe_coordinates': liuhe,
            'dominant_system': liuhe.get('dominant', 'N/A'),
            'strategies': strategies,
            'meaning': meaning.get('text', ''),
            'tiandao_insights': tiandao.get('inquiries', []),
            'recommended_style': self._get_recommended_style(liuhe)
        }

    def _get_recommended_style(self, liuhe: Dict) -> str:
        """获取推荐棋风"""
        dominant = liuhe.get('dominant', '强化系')
        
        style_map = {
            '强化系': '计算型·深度计算，步步为营',
            '自然系': '流畅型·行云流水，自然演化',
            '具现系': '实效型·落子生根，注重实际',
            '变身系': '创新型·出奇制胜，变幻莫测',
            '社会系': '博弈型·攻守兼备，纵横捭阖',
            '天道系': '哲学型·追寻意义，超越计算'
        }
        
        return style_map.get(dominant, '平衡型·全面发展')


def create_v4_engine(board_size: int = 19,
                      num_simulations: int = 1000) -> BSDGoEngineV4:
    """创建V4引擎"""
    return BSDGoEngineV4(board_size, num_simulations)


def test_v4_engine():
    """测试V4引擎"""
    print("=" * 70)
    print("BSD围棋引擎V4.0 - 三语言涌现版 测试")
    print("=" * 70)
    
    board = GoBoard(9)
    engine = create_v4_engine(9, 50)
    engine.search_time = 0.5
    
    # 初始局面
    print("\n【测试1】初始局面分析")
    analysis = engine.get_position_analysis(board, Stone.BLACK)
    print(f"  阶段: {analysis['phase']}")
    print(f"  V3评分: {analysis['v3_score']:.3f}")
    print(f"  涌现评分: {analysis['emergence_score']:.3f}")
    print(f"  涌现强度: {analysis['emergence_strength']:.3f}")
    print(f"  是否涌现: {analysis['is_emergent']}")
    print(f"  主导系统: {analysis['dominant_system']}")
    print(f"  0∅反(数字): {analysis['zero_yuan']['fan']:.3f}")
    print(f"  0∅空(英文): {analysis['zero_yuan']['kong']:.3f}")
    print(f"  0∅义(中文): {analysis['zero_yuan']['yi']:.3f}")
    
    # 天道追问
    print("\n  天道追问:")
    for insight in analysis['tiandao_inquiries']:
        print(f"    - {insight}")
    
    # 天元落子
    print("\n【测试2】天元落子后")
    board.make_move(GoPoint(4, 4), Stone.BLACK)
    
    strategy = engine.get_liuhe_strategy(board, Stone.WHITE)
    print(f"  主导系统: {strategy['dominant_system']}")
    print(f"  推荐棋风: {strategy['recommended_style']}")
    print(f"  棋道意义: {strategy['meaning']}")
    
    print("\n  策略建议:")
    for s in strategy['strategies']:
        print(f"    - {s}")
    
    # 引擎选择
    print("\n【测试3】引擎选择落子")
    board.make_move(GoPoint(2, 2), Stone.WHITE)  # 白方左上星
    point = engine.select_move(board, Stone.BLACK)
    
    if point:
        print(f"  选择: {point.to_gtp()}")
        
        # 验证
        board.make_move(point, Stone.BLACK)
        analysis = engine.get_position_analysis(board, Stone.WHITE)
        print(f"  落子后涌现强度: {analysis['emergence_strength']:.3f}")
        print(f"  主导系统: {analysis['dominant_system']}")
    
    print("\n" + "=" * 70)
    print("V4引擎测试完成")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    test_v4_engine()
