"""
BSD AI 对弈系统 V5.0 - 天道追问版
===================================
整合V5引擎（天道追问决策）的完整对弈系统
支持：V5引擎（天道追问）vs 对手AI
"""

import sys
import os
import json
import time
import argparse
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import (
    GoBoard, GoPoint, Stone, GamePhase
)
from bsd_go_engine_v5 import (
    BSDGoEngineV5, create_v5_engine, DecisionParadigm, GameSituation
)
from katago_gtp_client import GoAIInterface


@dataclass
class MatchConfigV5:
    board_size: int = 9
    komi: float = 7.5
    max_moves: int = 300
    bsd_simulations: int = 100
    bsd_search_time: float = 1.0
    bsd_side: str = "black"
    opponent_strength: int = 5
    enable_tiandao: bool = True


@dataclass
class MatchResultV5:
    winner: str = ""
    margin: float = 0.0
    total_moves: int = 0
    duration_seconds: float = 0.0
    reasoning: str = ""
    moves_log: List[Dict] = field(default_factory=list)
    paradigm_stats: Dict = field(default_factory=dict)
    tiandao_usage: Dict = field(default_factory=dict)
    cycle_events: List[Dict] = field(default_factory=list)


class BSDV5Match:
    """BSD V5引擎（天道追问）vs 对手 对弈管理器"""

    def __init__(self, config: MatchConfigV5 = None):
        self.config = config or MatchConfigV5()

        # V5引擎
        self.bsd_engine = create_v5_engine(
            self.config.board_size,
            self.config.bsd_simulations
        )
        self.bsd_engine.search_time = self.config.bsd_search_time

        # 对手AI
        self.opponent_ai = GoAIInterface(
            use_katago=False,
            board_size=self.config.board_size,
            strength=self.config.opponent_strength
        )

        # 棋盘
        self.board = GoBoard(self.config.board_size)
        self.moves_log: List[Dict] = []
        self.paradigm_log: List[Dict] = []
        self.cycle_events: List[Dict] = []

    def play_game(self) -> MatchResultV5:
        """执行一局对弈"""
        print("\n" + "=" * 70)
        print("BSD AI V5.0 (天道追问版) vs 对手AI 对弈")
        print("=" * 70)

        self.board = GoBoard(self.config.board_size)
        self.moves_log = []
        self.paradigm_log = []
        self.cycle_events = []

        bsd_stone = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE
        opponent_stone = Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK

        bsd_color = 'black' if bsd_stone == Stone.BLACK else 'white'
        opponent_color = 'white' if bsd_stone == Stone.BLACK else 'black'

        print(f"\n棋盘：{self.config.board_size}路 | 贴目：{self.config.komi}")
        print(f"BSD执：{'黑●' if bsd_stone == Stone.BLACK else '白○'} | 对手执：{'白○' if opponent_stone == Stone.WHITE else '黑●'}")
        print(f"V5引擎：天道追问（超越计算的意义追问）")
        print(f"对手AI强度：{self.config.opponent_strength}")

        self.opponent_ai.set_board_size(self.config.board_size)
        self.opponent_ai.clear_board()

        start_time = time.time()
        current_move = 0
        consecutive_passes = 0

        while not self.board.game_over and current_move < self.config.max_moves:
            current_stone = Stone.BLACK if current_move % 2 == 0 else Stone.WHITE
            color_str = 'black' if current_stone == Stone.BLACK else 'white'
            current_move += 1

            if current_stone == bsd_stone:
                # BSD V5落子
                result = self._bsd_move(current_stone)
                point = result['point']
                paradigm = result['paradigm']
                situation = result['situation']
                cycle_detected = result['cycle_detected']
                
                if point:
                    self.board.make_move(point, current_stone)
                    self.opponent_ai.play(bsd_color, point.to_gtp())
                    self._log_move(current_move, "BSD-V5", point, current_stone)
                    self._log_paradigm(current_move, paradigm, situation, cycle_detected)
                    
                    if cycle_detected:
                        self.cycle_events.append({
                            'move': current_move,
                            'paradigm': paradigm,
                            'point': point.to_gtp()
                        })
                    
                    consecutive_passes = 0
                else:
                    self.board.pass_move(current_stone)
                    self.opponent_ai.play(bsd_color, "PASS")
                    self._log_move(current_move, "BSD-V5", None, current_stone, True)
                    consecutive_passes += 1
            else:
                # 对手落子
                point = self._opponent_move(current_stone)
                if point:
                    self.board.make_move(point, current_stone)
                    self.opponent_ai.play(color_str, point.to_gtp())
                    self._log_move(current_move, "Opponent", point, current_stone)
                    consecutive_passes = 0
                else:
                    self.board.pass_move(current_stone)
                    self.opponent_ai.play(color_str, "PASS")
                    self._log_move(current_move, "Opponent", None, current_stone, True)
                    consecutive_passes += 1

            if consecutive_passes >= 2:
                print("\n双方连续虚着，对局结束")
                break

            if current_move % 20 == 0:
                self._print_status(current_move)

        duration = time.time() - start_time
        result = self._finalize(duration, bsd_stone)
        return result

    def _bsd_move(self, stone: Stone) -> Dict:
        """BSD V5落子（返回决策上下文）"""
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board.size)
            for y in range(self.board.size)
            if self.board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return {'point': None, 'paradigm': 'N/A', 'situation': 'N/A', 'cycle_detected': False}

        # 使用V5引擎选择
        point = self.bsd_engine.select_move(self.board, stone)
        
        # 获取决策上下文
        context = self.bsd_engine._analyze_context(self.board, stone, valid_moves)
        paradigm = self.bsd_engine._select_paradigm(context, self.board, stone)
        
        if point and self.board.is_valid_move(point, stone):
            return {
                'point': point,
                'paradigm': paradigm.value,
                'situation': context.situation.value,
                'cycle_detected': context.cycle_detected
            }

        # 回退
        return {
            'point': valid_moves[0],
            'paradigm': 'FALLBACK',
            'situation': context.situation.value,
            'cycle_detected': context.cycle_detected
        }

    def _opponent_move(self, stone: Stone) -> Optional[GoPoint]:
        """对手落子"""
        color_str = 'black' if stone == Stone.BLACK else 'white'
        gtpmove = self.opponent_ai.generate_move(color_str)

        if gtpmove and gtpmove not in ['PASS', 'resign', 'pass']:
            point = self._gtp_to_point(gtpmove)
            if point and self.board.is_valid_move(point, stone):
                return point

        # 回退
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board.size)
            for y in range(self.board.size)
            if self.board.is_valid_move(GoPoint(x, y), stone)
        ]

        if valid_moves:
            return valid_moves[0]
        return None

    def _gtp_to_point(self, gtp_move: str) -> Optional[GoPoint]:
        """GTP坐标转棋盘点"""
        letters = 'ABCDEFGHJKLMNOPQRST'
        if len(gtp_move) < 2:
            return None
        col_char = gtp_move[0].upper()
        row_str = gtp_move[1:]
        if col_char not in letters:
            return None
        x = letters.index(col_char)
        try:
            y = int(row_str) - 1
            if 0 <= x < self.config.board_size and 0 <= y < self.config.board_size:
                return GoPoint(x, y)
        except:
            pass
        return None

    def _log_move(self, move_num: int, player: str, point: Optional[GoPoint],
                  stone: Stone, is_pass: bool = False):
        """记录落子"""
        entry = {
            'move': move_num,
            'player': player,
            'stone': 'black' if stone == Stone.BLACK else 'white',
            'point': point.to_gtp() if point else 'PASS',
            'is_pass': is_pass
        }
        self.moves_log.append(entry)

        icon = '●' if stone == Stone.BLACK else '○'
        move_str = 'PASS' if is_pass else (point.to_gtp() if point else '?')
        print(f"  {move_num:3d}. {icon} {player:12s} -> {move_str}")

    def _log_paradigm(self, move_num: int, paradigm: str, 
                       situation: str, cycle_detected: bool):
        """记录决策范式"""
        self.paradigm_log.append({
            'move': move_num,
            'paradigm': paradigm,
            'situation': situation,
            'cycle_detected': cycle_detected
        })

    def _print_status(self, move_num: int):
        """打印状态"""
        phase = self.board.get_game_phase().value
        empty_count = sum(
            1 for x in range(self.board.size) for y in range(self.board.size)
            if self.board.board[y][x] == Stone.EMPTY
        )
        
        # 获取最新决策范式
        latest_paradigm = self.paradigm_log[-1] if self.paradigm_log else {}
        paradigm = latest_paradigm.get('paradigm', 'N/A')
        situation = latest_paradigm.get('situation', 'N/A')
        cycle = latest_paradigm.get('cycle_detected', False)
        
        cycle_icon = '⚠️' if cycle else '○'
        
        print(f"\n  --- 第{move_num}手 | 阶段：{phase} | 空位：{empty_count} | 范式：{paradigm} | 态势：{situation} {cycle_icon} ---")

    def _finalize(self, duration: float, bsd_stone: Stone) -> MatchResultV5:
        """终局结算"""
        score = self.board.get_score(self.config.komi)

        winner = ""
        if score['winner'] == 'black':
            winner = "BSD-V5" if bsd_stone == Stone.BLACK else "Opponent"
        elif score['winner'] == 'white':
            winner = "BSD-V5" if bsd_stone == Stone.WHITE else "Opponent"
        else:
            winner = "Draw"

        reasoning = self._generate_reasoning(winner, score, bsd_stone)
        paradigm_stats = self._compute_paradigm_stats()
        tiandao_usage = self._compute_tiandao_usage()

        result = MatchResultV5(
            winner=winner,
            margin=score.get('margin', 0),
            total_moves=len(self.moves_log),
            duration_seconds=duration,
            reasoning=reasoning,
            moves_log=self.moves_log,
            paradigm_stats=paradigm_stats,
            tiandao_usage=tiandao_usage,
            cycle_events=self.cycle_events
        )

        self._print_result(result)
        self.opponent_ai.cleanup()
        return result

    def _compute_paradigm_stats(self) -> Dict:
        """计算决策范式统计"""
        if not self.paradigm_log:
            return {}
        
        paradigms = [p['paradigm'] for p in self.paradigm_log]
        total = len(paradigms)
        
        stats = {
            'total': total,
            '计算驱动': paradigms.count('计算驱动'),
            '涌现驱动': paradigms.count('涌现驱动'),
            '天道追问': paradigms.count('天道追问'),
            '觉醒决策': paradigms.count('觉醒决策'),
        }
        
        # 计算各范式占比
        for key in ['计算驱动', '涌现驱动', '天道追问', '觉醒决策']:
            stats[f'{key}_ratio'] = stats[key] / total if total > 0 else 0
        
        return stats

    def _compute_tiandao_usage(self) -> Dict:
        """计算天道追问使用情况"""
        total = len(self.paradigm_log)
        tiandao_count = sum(
            1 for p in self.paradigm_log 
            if p['paradigm'] in ['天道追问', '觉醒决策']
        )
        awakening_count = sum(
            1 for p in self.paradigm_log 
            if p['paradigm'] == '觉醒决策'
        )
        
        return {
            'total_moves': total,
            'tiandao_moves': tiandao_count,
            'awakening_moves': awakening_count,
            'tiandao_ratio': tiandao_count / total if total > 0 else 0,
            'awakening_ratio': awakening_count / total if total > 0 else 0,
            'cycle_breaks': len(self.cycle_events)
        }

    def _generate_reasoning(self, winner: str, score: Dict, 
                            bsd_stone: Stone) -> str:
        """生成胜负分析"""
        reasons = []
        reasons.append("=" * 70)
        reasons.append("【V5天道追问 - 超越计算的意义分析】")
        reasons.append("=" * 70)

        if winner == "BSD-V5":
            reasons.append("\n🏆 BSD V5 (天道追问版) 胜利！")
            reasons.append("\n核心优势：")
            reasons.append("  1. 天道追问：超越计算的意义追问")
            reasons.append("  2. 反性计算：模拟对手意图的反向推演")
            reasons.append("  3. 循环检测：识别并打破决策循环")
            reasons.append("  4. 范式切换：根据态势自动切换决策范式")
            reasons.append("\n理论突破：")
            reasons.append("  V5实现了从\"计算驱动\"到\"意义驱动\"的跃迁")
            reasons.append("  天道追问让AI具备了超越计算的棋道哲学")
            reasons.append("  反性计算让AI能够站在对手角度思考")
        elif winner == "Opponent":
            reasons.append("\n💡 对手胜利")
            reasons.append("\n分析：")
            reasons.append("  1. 天道追问的时机需优化")
            reasons.append("  2. 反性计算的精度需提升")
            reasons.append("  3. 范式切换的阈值需调整")
        else:
            reasons.append("\n⚖️ 和棋")

        reasons.append(f"\n终局：黑{score.get('black', 0):.1f} vs 白{score.get('white', 0):.1f}")
        reasons.append(f"领先：{score.get('margin', 0):.1f}目")
        
        # 天道追问使用统计
        usage = self._compute_tiandao_usage()
        if usage['tiandao_moves'] > 0:
            reasons.append(f"\n天道追问使用：")
            reasons.append(f"  使用手数：{usage['tiandao_moves']}/{usage['total_moves']}")
            reasons.append(f"  占比：{usage['tiandao_ratio']:.1%}")
            reasons.append(f"  觉醒决策：{usage['awakening_moves']}手")
            reasons.append(f"  打破循环：{usage['cycle_breaks']}次")

        return "\n".join(reasons)

    def _print_result(self, result: MatchResultV5):
        """打印结果"""
        print("\n" + "=" * 70)
        print("【对局结束 - V5天道追问版】")
        print(f"  胜者：{result.winner}")
        print(f"  领先：{result.margin:.1f} 目")
        print(f"  手数：{result.total_moves}")
        print(f"  用时：{result.duration_seconds:.1f} 秒")
        
        if result.paradigm_stats:
            print(f"\n  决策范式统计：")
            for key, value in result.paradigm_stats.items():
                if isinstance(value, (int, float)) and key not in ['total']:
                    print(f"    {key}: {value}")
        
        if result.tiandao_usage:
            print(f"\n  天道追问使用：")
            print(f"    使用手数：{result.tiandao_usage.get('tiandao_moves', 0)}")
            print(f"    觉醒决策：{result.tiandao_usage.get('awakening_moves', 0)}")
            print(f"    打破循环：{result.tiandao_usage.get('cycle_breaks', 0)}次")
        
        if result.cycle_events:
            print(f"\n  循环事件：{len(result.cycle_events)}次")
            for event in result.cycle_events[:5]:
                print(f"    第{event['move']}手: {event['paradigm']} -> {event['point']}")
        
        print(f"\n{result.reasoning}")
        print("=" * 70)


class V5Tournament:
    """V5引擎锦标赛"""

    def __init__(self, num_games: int = 3, **kwargs):
        self.num_games = num_games
        self.base_config = MatchConfigV5(
            board_size=kwargs.get('board_size', 9),
            bsd_simulations=kwargs.get('bsd_simulations', 100),
            bsd_search_time=kwargs.get('bsd_search_time', 1.0),
            opponent_strength=kwargs.get('opponent_strength', 5),
            enable_tiandao=kwargs.get('enable_tiandao', True)
        )
        self.results: List[MatchResultV5] = []

    def run(self) -> Dict:
        """运行锦标赛"""
        print("\n" + "=" * 70)
        print(f"BSD V5 (天道追问版) 锦标赛 - {self.num_games}局")
        print("=" * 70)

        wins = losses = draws = 0
        total_tiandao_usage = 0
        total_cycle_breaks = 0

        for i in range(self.num_games):
            config = MatchConfigV5(
                board_size=self.base_config.board_size,
                bsd_simulations=self.base_config.bsd_simulations,
                bsd_search_time=self.base_config.bsd_search_time,
                opponent_strength=self.base_config.opponent_strength,
                bsd_side="black" if i % 2 == 0 else "white"
            )

            print(f"\n{'='*70}")
            print(f"第 {i+1}/{self.num_games} 局 | BSD-V5执{'黑' if config.bsd_side == 'black' else '白'}")

            match = BSDV5Match(config)
            result = match.play_game()
            self.results.append(result)

            if result.winner == "BSD-V5":
                wins += 1
            elif result.winner == "Draw":
                draws += 1
            else:
                losses += 1
            
            # 统计天道追问使用
            total_tiandao_usage += result.tiandao_usage.get('tiandao_moves', 0)
            total_cycle_breaks += len(result.cycle_events)

        summary = {
            'total': self.num_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': wins / self.num_games,
            'avg_moves': sum(r.total_moves for r in self.results) / self.num_games,
            'avg_duration': sum(r.duration_seconds for r in self.results) / self.num_games,
            'avg_margin': sum(r.margin for r in self.results) / self.num_games if wins > 0 else 0,
            'total_tiandao_moves': total_tiandao_usage,
            'total_cycle_breaks': total_cycle_breaks,
            'engine': 'V5 Tiandao Inquiry'
        }

        print("\n" + "=" * 70)
        print(f"【锦标赛汇总 - V5 天道追问版】")
        print(f"  总局数：{summary['total']}")
        print(f"  胜/负/和：{summary['wins']}/{summary['losses']}/{summary['draws']}")
        print(f"  胜率：{summary['win_rate']:.1%}")
        print(f"  平均手数：{summary['avg_moves']:.0f}")
        print(f"  平均用时：{summary['avg_duration']:.1f}秒")
        print(f"  平均领先：{summary['avg_margin']:.1f}目")
        print(f"  天道追问总使用：{summary['total_tiandao_moves']}手")
        print(f"  打破循环总次数：{summary['total_cycle_breaks']}次")
        print("=" * 70)

        return summary


def main():
    parser = argparse.ArgumentParser(description='BSD AI V5.0 对弈系统 - 天道追问版')
    parser.add_argument('--mode', choices=['single', 'tournament', 'demo'],
                        default='demo')
    parser.add_argument('--size', type=int, default=9, help='棋盘大小')
    parser.add_argument('--games', type=int, default=3, help='锦标赛局数')
    parser.add_argument('--sim', type=int, default=100, help='MCTS模拟次数')
    parser.add_argument('--time', type=float, default=1.0, help='搜索时间(秒)')
    parser.add_argument('--strength', type=int, default=5, help='对手AI强度(1-5)')
    parser.add_argument('--tiandao', action='store_true', default=True, 
                        help='启用天道追问')

    args = parser.parse_args()

    print(r"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║    BSD 围棋 AI 对弈系统 V5.0 - 天道追问版                             ║
║                                                                          ║
║    核心突破：                                                            ║
║    ┌─────────────────────────────────────────────────────────────────┐  ║
║    │  V4: 三语言涌现（计算+涌现）                                  │  ║
║    │  V5: 天道追问（计算+涌现+天道+觉醒）                        │  ║
║    │                                                                 │  ║
║    │  决策范式：                                                     │  ║
║    │  计算驱动 → 涌现驱动 → 天道追问 → 觉醒决策                    │  ║
║    │                                                                 │  ║
║    │  反性计算 + 循环检测 + 破局能力                                │  ║
║    └─────────────────────────────────────────────────────────────────┘  ║
║                                                                          ║
║    版本：V5.0 Tiandao Inquiry · 2026-08-02                               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    if args.mode == 'tournament':
        tournament = V5Tournament(
            num_games=args.games,
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            opponent_strength=args.strength,
            enable_tiandao=args.tiandao
        )
        summary = tournament.run()

        # 保存结果
        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(save_dir, f'bsd_v5_tournament_{timestamp}.json')

        data = {
            'timestamp': timestamp,
            'summary': summary,
            'matches': [
                {
                    'winner': r.winner,
                    'margin': r.margin,
                    'moves': r.total_moves,
                    'paradigm_stats': r.paradigm_stats,
                    'tiandao_usage': r.tiandao_usage,
                    'cycle_events': r.cycle_events
                }
                for r in tournament.results
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n锦标赛结果已保存：{filepath}")

    else:
        config = MatchConfigV5(
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            opponent_strength=args.strength,
            bsd_side='black',
            enable_tiandao=args.tiandao
        )
        match = BSDV5Match(config)
        result = match.play_game()

        # 保存结果
        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(save_dir, f'bsd_v5_match_{timestamp}.json')

        data = {
            'timestamp': timestamp,
            'result': {
                'winner': result.winner,
                'margin': result.margin,
                'total_moves': result.total_moves,
                'duration_seconds': result.duration_seconds
            },
            'reasoning': result.reasoning,
            'paradigm_stats': result.paradigm_stats,
            'tiandao_usage': result.tiandao_usage,
            'cycle_events': result.cycle_events,
            'moves': result.moves_log
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存：{filepath}")


if __name__ == "__main__":
    main()
