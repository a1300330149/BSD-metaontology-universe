#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋对弈系统 V∞ · 完整版
==============================

整合所有物理化实验版本的可取之处：
    - V1-V5 引擎核心 (已整合到 omega 版)
    - match 系列对弈管理器 (V3/V3Pro/V4/V5)
    - KataGo/外部AI接口
    - 统计分析功能
    - 完整的对弈流程

架构：
    【核心引擎层】 bsd_go_engine_omega.py (终极版引擎)
    【对弈管理层】 本文件 - 完整的对弈系统
    【外部接口层】 katago_gtp_client.py
"""

import os
import sys
import json
import time
import argparse
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_omega import (
    BSDGoEngineOmega, Stone, GamePhase, GoPoint, Move,
    LiuHeCoordinate, TiandaoInsight, DecisionContext,
    DecisionParadigm, GameSituation, GoBoard,
    LiuHeGoMapper, OptimizedEvaluator, ThreatSpaceSearch,
    TiandaoDecisionEngine
)
from katago_gtp_client import (
    KataGoGTPClient, GTPEngineConfig, GoAIInterface, StrongGoAI
)


# ============================================================================
# 【从物理化实验版本提取的可取之处】
# ============================================================================


@dataclass
class MatchConfig:
    """
    对弈配置 - 整合自 match V3/V4/V5
    
    来源：bsd_match_v3.py, bsd_match_v4.py, bsd_match_v5.py
    """
    # 棋盘配置
    board_size: int = 19
    komi: float = 7.5
    max_moves: int = 300
    
    # BSD引擎配置
    bsd_simulations: int = 200
    bsd_search_time: float = 2.0
    bsd_side: str = "black"  # "black" / "white"
    
    # 对手AI配置
    opponent_type: str = "strong"  # "strong" / "katago" / "simple"
    opponent_strength: int = 5
    opponent_name: str = "StrongGoAI"
    
    # KataGo配置
    katago_path: str = "katago"
    model_path: str = ""
    config_path: str = ""
    
    # 功能开关
    enable_tiandao: bool = True
    enable_paradigm_tracking: bool = True
    track_liuhe_analysis: bool = True
    
    # 时间控制
    time_control: int = 30  # 思考时间（秒）


@dataclass
class MatchResult:
    """
    对弈结果 - 整合自 match V3/V4/V5
    
    来源：bsd_match_v3.py, bsd_match_v4.py, bsd_match_v5.py
    """
    # 基础结果
    winner: str = ""  # "BSD" / "Opponent" / "Draw"
    margin: float = 0.0
    total_moves: int = 0
    duration_seconds: float = 0.0
    
    # 详细信息
    game_phase_at_end: str = ""
    final_score: Dict = field(default_factory=dict)
    reasoning: str = ""  # 天道系追问的胜负理由
    
    # 棋谱
    moves_log: List[Dict] = field(default_factory=list)
    
    # 分析数据
    liuhe_analysis: List[Dict] = field(default_factory=list)  # 关键手的六系分析
    paradigm_stats: Dict = field(default_factory=dict)  # 范式使用统计
    tiandao_usage: Dict = field(default_factory=dict)  # 天道追问使用统计
    cycle_events: List[Dict] = field(default_factory=list)  # 循环事件检测
    
    # 三语言涌现统计 (来自V4)
    emergence_summary: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'winner': self.winner,
            'margin': self.margin,
            'total_moves': self.total_moves,
            'duration': self.duration_seconds,
            'reasoning': self.reasoning,
            'liuhe_analysis_count': len(self.liuhe_analysis),
            'paradigm_stats': self.paradigm_stats,
        }


# ============================================================================
# 【完整对弈管理器】
# ============================================================================


class BSDGoMatchManager:
    """
    BSD围棋对弈管理器 - 整合所有版本的对弈功能
    
    来源：bsd_match_v3.py, bsd_match_v3pro.py, bsd_match_v4.py, bsd_match_v5.py, bsd_go_match.py
    
    核心功能：
    1. 完整对弈流程控制
    2. 支持多种对手AI（内置AI、KataGo）
    3. 多引擎版本支持
    4. 详细的统计分析
    5. 天道追问集成
    """
    
    def __init__(self, config: MatchConfig = None):
        self.config = config or MatchConfig()
        
        # 初始化BSD终极引擎
        self.bsd_engine = BSDGoEngineOmega(
            board_size=self.config.board_size,
            num_simulations=self.config.bsd_simulations
        )
        self.bsd_engine.search_time = self.config.bsd_search_time
        
        # 初始化对手AI
        self.opponent_ai = self._init_opponent_ai()
        
        # 共享棋盘
        self.board = GoBoard(self.config.board_size)
        
        # 统计数据
        self.moves_log: List[Dict] = []
        self.paradigm_log: List[Dict] = []
        self.tiandao_events: List[Dict] = []
        self.cycle_events: List[Dict] = []
        self.liuhe_analysis: List[Dict] = []
        
        # 状态
        self.game_started = False
        self.game_ended = False
    
    def _init_opponent_ai(self) -> GoAIInterface:
        """初始化对手AI - 整合自 match 系列"""
        return GoAIInterface(
            use_katago=(self.config.opponent_type == "katago"),
            board_size=self.config.board_size,
            strength=self.config.opponent_strength,
            katago_path=self.config.katago_path,
            model_path=self.config.model_path,
            config_path=self.config.config_path
        )
    
    def play_game(self) -> MatchResult:
        """
        执行完整对弈 - 整合自所有 match 版本
        
        Returns:
            MatchResult: 对弈结果
        """
        print("\n" + "=" * 70)
        print("【BSD 围棋对弈系统 V∞ · 完整版】")
        print("=" * 70)
        print(f"\n  配置:")
        print(f"    - 棋盘: {self.config.board_size}路")
        print(f"    - Komi: {self.config.komi}")
        print(f"    - BSD执: {'黑' if self.config.bsd_side == 'black' else '白'}")
        print(f"    - 对手: {self.config.opponent_name}")
        print()
        
        # 初始化棋盘
        self.board = GoBoard(self.config.board_size)
        self.moves_log = []
        self.paradigm_log = []
        self.tiandao_events = []
        self.cycle_events = []
        self.liuhe_analysis = []
        
        # 重置引擎
        self.bsd_engine = BSDGoEngineOmega(
            board_size=self.config.board_size,
            num_simulations=self.config.bsd_simulations
        )
        self.bsd_engine.search_time = self.config.bsd_search_time
        
        # 确定先后手
        bsd_stone = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE
        opponent_stone = Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK
        
        # 记录开始时间
        start_time = time.time()
        self.game_started = True
        
        # 主循环
        move_count = 0
        game_ended = False
        
        while move_count < self.config.max_moves and not game_ended:
            current_stone = Stone.BLACK if move_count % 2 == 0 else Stone.WHITE
            move_count += 1
            
            # 判断当前玩家
            is_bsd_turn = (current_stone == bsd_stone)
            
            if is_bsd_turn:
                # BSD引擎落子
                point = self._bsd_move(current_stone)
            else:
                # 对手AI落子
                point = self._opponent_move(current_stone)
            
            if point is None:
                print(f"  ⚠️ 手{move_count}: {self._stone_name(current_stone)}方无应手")
                break
            
            # 执行落子
            success, captured = self.board.place_stone(point, current_stone)
            
            if not success:
                # 尝试用另一种方式
                empty_points = self.board.get_empty_points()
                if empty_points:
                    point = empty_points[0]
                    success, captured = self.board.place_stone(point, current_stone)
                    if not success:
                        continue
            
            # 记录棋谱
            move_record = {
                'move_number': move_count,
                'player': 'BSD' if is_bsd_turn else self.config.opponent_name,
                'stone': self._stone_name(current_stone),
                'point': point.to_gtp(),
                'captured': captured,
                'phase': self.board.get_game_phase().value,
                'timestamp': time.time(),
            }
            
            # 记录六系分析
            if self.config.track_liuhe_analysis:
                coord = self.bsd_engine.liuhe_mapper.map_point(point)
                move_record['liuhe_coordinate'] = coord.to_dict()
                
                # 关键手分析
                if captured > 0 or move_count <= 10:
                    self.liuhe_analysis.append({
                        'move': move_count,
                        'point': point.to_gtp(),
                        'coordinate': coord.to_dict(),
                        'type': 'key_move' if captured > 0 else 'opening_move',
                    })
            
            # 记录范式使用
            if is_bsd_turn and self.config.enable_paradigm_tracking:
                paradigm = self.bsd_engine.decision_context.paradigm.value
                self.paradigm_log.append({
                    'move': move_count,
                    'paradigm': paradigm,
                    'situation': self.bsd_engine.decision_context.situation.value,
                    'score_advantage': self.bsd_engine.decision_context.score_advantage,
                })
            
            self.moves_log.append(move_record)
            
            # 打印进度
            if move_count <= 10 or move_count % 20 == 0:
                player_name = 'BSD' if is_bsd_turn else self.config.opponent_name
                gtp = point.to_gtp()
                phase = self.board.get_game_phase().value
                print(f"  手{move_count:3d}: {player_name} → {gtp} (断{captured}) [{phase}]")
            
            # 检查结束条件
            if move_count > 2:
                # 双方连续pass
                if self._check_game_end():
                    game_ended = True
                    break
        
        # 计算结果
        duration = time.time() - start_time
        result = self._calculate_result(bsd_stone, duration)
        
        self.game_started = False
        self.game_ended = True
        
        return result
    
    def _bsd_move(self, stone: Stone) -> Optional[GoPoint]:
        """BSD引擎落子"""
        # 同步棋盘状态到引擎
        self.bsd_engine.board = self.board
        
        # 获取最佳落子
        point = self.bsd_engine.get_best_move(stone)
        
        return point
    
    def _opponent_move(self, stone: Stone) -> Optional[GoPoint]:
        """对手AI落子"""
        color_str = "black" if stone == Stone.BLACK else "white"
        
        # 从所有合法点中选一个
        empty_points = self.board.get_empty_points()
        if not empty_points:
            return None
        
        # 尝试用AI接口
        try:
            point = self.opponent_ai.generate_move(color_str)
            if point:
                # 转换为GoPoint
                return self._parse_move(point)
        except:
            pass
        
        # 回退：随机选择
        import random
        point = random.choice(empty_points)
        return point
    
    def _parse_move(self, move_str: str) -> Optional[GoPoint]:
        """解析落子字符串为GoPoint"""
        move_str = move_str.strip().upper()
        
        if move_str in ['PASS', 'RESIGN']:
            return None
        
        # GTP格式: A1, B2, ...
        letters = 'ABCDEFGHJKLMNOPQRST'  # 跳过I
        if len(move_str) >= 2:
            letter = move_str[0]
            number = int(move_str[1:])
            
            if letter in letters:
                x = letters.index(letter)
                y = number - 1
                return GoPoint(x, y)
        
        return None
    
    def _check_game_end(self) -> bool:
        """检查游戏是否结束"""
        # 简化：检查是否有足够的空点
        empty_points = self.board.get_empty_points()
        if len(empty_points) < 2:
            return True
        
        # 检查是否达到最大手数
        if len(self.board.move_history) >= self.config.max_moves:
            return True
        
        return False
    
    def _calculate_result(self, bsd_stone: Stone, duration: float) -> MatchResult:
        """计算对弈结果"""
        bsd_score = self.board.get_score(bsd_stone)
        opponent_score = self.board.get_score(
            Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK
        )
        
        # 计算胜负
        margin = bsd_score - opponent_score
        if margin > 0:
            winner = "BSD"
        elif margin < 0:
            winner = self.config.opponent_name
        else:
            winner = "Draw"
        
        # 生成结果
        result = MatchResult(
            winner=winner,
            margin=abs(margin),
            total_moves=len(self.moves_log),
            duration_seconds=duration,
            game_phase_at_end=self.board.get_game_phase().value,
            final_score={
                'BSD': bsd_score,
                self.config.opponent_name: opponent_score,
            },
            reasoning=self._generate_reasoning(winner, margin),
            moves_log=self.moves_log,
            liuhe_analysis=self.liuhe_analysis,
            paradigm_stats=self._calculate_paradigm_stats(),
            tiandao_usage=self._calculate_tiandao_usage(),
            cycle_events=self.cycle_events,
        )
        
        return result
    
    def _generate_reasoning(self, winner: str, margin: float) -> str:
        """生成胜负理由 - 来自V5天道追问"""
        if winner == "BSD":
            if margin > 10:
                return f"BSD引擎以 {margin:.1f} 目大胜。计算驱动+天道追问的协同决策发挥了作用。"
            else:
                return f"BSD引擎以 {margin:.1f} 目险胜。多范式动态切换的决策机制有效。"
        elif winner == self.config.opponent_name:
            return f"对手以 {margin:.1f} 目获胜。BSD引擎需要进一步优化评估器和威胁搜索。"
        else:
            return "平局。双方势均力敌。"
    
    def _calculate_paradigm_stats(self) -> Dict:
        """计算范式使用统计 - 来自V5"""
        stats = {}
        for record in self.paradigm_log:
            paradigm = record['paradigm']
            if paradigm not in stats:
                stats[paradigm] = 0
            stats[paradigm] += 1
        return stats
    
    def _calculate_tiandao_usage(self) -> Dict:
        """计算天道追问使用统计 - 来自V5"""
        insights = self.bsd_engine.tiandao_engine.insights
        return {
            'total_insights': len(insights),
            'avg_confidence': sum(i.confidence for i in insights) / max(len(insights), 1),
            'questions_asked': len(set(i.question for i in insights)),
        }
    
    def _stone_name(self, stone: Stone) -> str:
        return "黑" if stone == Stone.BLACK else "白"
    
    def print_game_summary(self, result: MatchResult):
        """打印对局摘要"""
        print("\n" + "=" * 70)
        print("【对局摘要】")
        print("=" * 70)
        
        print(f"\n  结果: {result.winner} 胜 ({result.margin:.1f} 目)")
        print(f"  手数: {result.total_moves}")
        print(f"  用时: {result.duration_seconds:.1f} 秒")
        print(f"  阶段: {result.game_phase_at_end}")
        print(f"  理由: {result.reasoning}")
        
        if result.paradigm_stats:
            print(f"\n  范式使用统计:")
            for paradigm, count in result.paradigm_stats.items():
                print(f"    - {paradigm}: {count} 次")
        
        if result.liuhe_analysis:
            print(f"\n  关键手六系分析: {len(result.liuhe_analysis)} 个关键点")
        
        print("\n" + "=" * 70)


# ============================================================================
# 【批量对弈支持】
# ============================================================================


class BatchMatchRunner:
    """批量对弈运行器"""
    
    def __init__(self, base_config: MatchConfig = None):
        self.base_config = base_config or MatchConfig()
        self.results: List[MatchResult] = []
        self.statistics: Dict = {}
    
    def run_batch(self, num_games: int = 5) -> List[MatchResult]:
        """运行批量对弈"""
        print("\n" + "=" * 70)
        print(f"【批量对弈 · {num_games}局】")
        print("=" * 70)
        
        self.results = []
        
        for i in range(num_games):
            print(f"\n{'='*20} 第 {i+1}/{num_games} 局 {'='*20}")
            
            # 每局切换先手
            config = MatchConfig(
                **{**self.base_config.__dict__, 
                   'bsd_side': 'black' if i % 2 == 0 else 'white'}
            )
            
            manager = BSDGoMatchManager(config)
            result = manager.play_game()
            self.results.append(result)
            
            # 打印单局摘要
            manager.print_game_summary(result)
        
        # 计算统计
        self._calculate_statistics()
        
        return self.results
    
    def _calculate_statistics(self):
        """计算统计数据"""
        if not self.results:
            return
        
        wins = sum(1 for r in self.results if r.winner == "BSD")
        losses = sum(1 for r in self.results if r.winner != "BSD")
        total_moves = sum(r.total_moves for r in self.results)
        total_duration = sum(r.duration_seconds for r in self.results)
        
        self.statistics = {
            'total_games': len(self.results),
            'wins': wins,
            'losses': losses,
            'win_rate': wins / len(self.results),
            'avg_moves': total_moves / len(self.results),
            'avg_duration': total_duration / len(self.results),
        }
        
        print("\n" + "=" * 70)
        print("【批量对弈统计】")
        print("=" * 70)
        print(f"\n  总局数: {self.statistics['total_games']}")
        print(f"  胜: {self.statistics['wins']}")
        print(f"  负: {self.statistics['losses']}")
        print(f"  胜率: {self.statistics['win_rate']:.1%}")
        print(f"  平均手数: {self.statistics['avg_moves']:.0f}")
        print(f"  平均用时: {self.statistics['avg_duration']:.1f} 秒")


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序 - 支持命令行参数"""
    
    parser = argparse.ArgumentParser(
        description='BSD 围棋对弈系统 V∞ · 完整版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python bsd_go_match_omega.py                          # 默认配置
    python bsd_go_match_omega.py --size 19 --games 3      # 19路棋盘，3局
    python bsd_go_match_omega.py --sim 500 --strength 8   # 增加模拟次数
        """
    )
    
    # 对弈配置
    parser.add_argument('--size', type=int, default=9,
                       help='棋盘大小 (9/13/19)，默认9')
    parser.add_argument('--games', type=int, default=1,
                       help='对弈局数，默认1')
    parser.add_argument('--bsd-side', choices=['black', 'white'], default='black',
                       help='BSD引擎执哪方，默认black')
    
    # BSD引擎配置
    parser.add_argument('--sim', type=int, default=200,
                       help='MCTS模拟次数，默认200')
    parser.add_argument('--time', type=float, default=2.0,
                       help='每步思考时间（秒），默认2.0')
    
    # 对手配置
    parser.add_argument('--opponent', choices=['simple', 'strong', 'katago'],
                       default='strong',
                       help='对手类型，默认strong')
    parser.add_argument('--strength', type=int, default=5,
                       help='对手强度(1-10)，默认5')
    
    # KataGo配置
    parser.add_argument('--katago-path', type=str, default='katago',
                       help='KataGo可执行文件路径')
    parser.add_argument('--model', type=str, default='',
                       help='KataGo模型路径')
    
    # 输出配置
    parser.add_argument('--output', type=str, default=None,
                       help='保存结果的JSON文件路径')
    
    args = parser.parse_args()
    
    # 创建配置
    config = MatchConfig(
        board_size=args.size,
        bsd_side=args.bsd_side,
        bsd_simulations=args.sim,
        bsd_search_time=args.time,
        opponent_type=args.opponent,
        opponent_strength=args.strength,
        katago_path=args.katago_path,
        model_path=args.model,
    )
    
    # 运行对弈
    if args.games == 1:
        # 单局对弈
        manager = BSDGoMatchManager(config)
        result = manager.play_game()
        manager.print_game_summary(result)
        
        results = [result]
    else:
        # 批量对弈
        runner = BatchMatchRunner(config)
        results = runner.run_batch(args.games)
    
    # 保存结果
    if args.output:
        output_data = [r.to_dict() for r in results]
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n📁 结果已保存: {args.output}")
    
    return results


if __name__ == '__main__':
    main()