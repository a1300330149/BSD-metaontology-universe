"""
BSD AI 对弈系统 V4.0 - 三语言涌现版
===================================
整合三语言涌现引擎的完整对弈系统
支持：V4引擎（三语言涌现）vs 对手AI
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
from bsd_go_engine_v4 import (
    BSDGoEngineV4, create_v4_engine
)
from katago_gtp_client import GoAIInterface


@dataclass
class MatchConfigV4:
    board_size: int = 9
    komi: float = 7.5
    max_moves: int = 300
    bsd_simulations: int = 200
    bsd_search_time: float = 2.0
    bsd_side: str = "black"
    opponent_strength: int = 5
    emergence_weight: float = 0.4


@dataclass
class MatchResultV4:
    winner: str = ""
    margin: float = 0.0
    total_moves: int = 0
    duration_seconds: float = 0.0
    reasoning: str = ""
    moves_log: List[Dict] = field(default_factory=list)
    emergence_summary: Dict = field(default_factory=dict)
    liuhe_strategy: Dict = field(default_factory=dict)


class BSDV4Match:
    """BSD V4引擎 vs 对手 对弈管理器"""

    def __init__(self, config: MatchConfigV4 = None):
        self.config = config or MatchConfigV4()

        # V4引擎
        self.bsd_engine = create_v4_engine(
            self.config.board_size,
            self.config.bsd_simulations
        )
        self.bsd_engine.search_time = self.config.bsd_search_time
        self.bsd_engine.emergence_weight = self.config.emergence_weight

        # 对手AI
        self.opponent_ai = GoAIInterface(
            use_katago=False,
            board_size=self.config.board_size,
            strength=self.config.opponent_strength
        )

        # 棋盘
        self.board = GoBoard(self.config.board_size)
        self.moves_log: List[Dict] = []
        self.emergence_snapshots: List[Dict] = []

    def play_game(self) -> MatchResultV4:
        """执行一局对弈"""
        print("\n" + "=" * 70)
        print("BSD AI V4.0 (三语言涌现版) vs 对手AI 对弈")
        print("=" * 70)

        self.board = GoBoard(self.config.board_size)
        self.moves_log = []
        self.emergence_snapshots = []

        bsd_stone = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE
        opponent_stone = Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK

        bsd_color = 'black' if bsd_stone == Stone.BLACK else 'white'
        opponent_color = 'white' if bsd_stone == Stone.BLACK else 'black'

        print(f"\n棋盘：{self.config.board_size}路 | 贴目：{self.config.komi}")
        print(f"BSD执：{'黑●' if bsd_stone == Stone.BLACK else '白○'} | 对手执：{'白○' if opponent_stone == Stone.WHITE else '黑●'}")
        print(f"V4引擎：三语言涌现（数字×英文×中文）")
        print(f"涌现权重：{self.config.emergence_weight:.1%}")
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
                # BSD V4落子
                point = self._bsd_move(current_stone)
                if point:
                    self.board.make_move(point, current_stone)
                    self.opponent_ai.play(bsd_color, point.to_gtp())
                    self._log_move(current_move, "BSD-V4", point, current_stone)
                    self._snapshot_emergence(current_stone)
                    consecutive_passes = 0
                else:
                    self.board.pass_move(current_stone)
                    self.opponent_ai.play(bsd_color, "PASS")
                    self._log_move(current_move, "BSD-V4", None, current_stone, True)
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

    def _bsd_move(self, stone: Stone) -> Optional[GoPoint]:
        """BSD V4落子"""
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board.size)
            for y in range(self.board.size)
            if self.board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return None

        # 使用V4引擎选择
        point = self.bsd_engine.select_move(self.board, stone)

        if point and self.board.is_valid_move(point, stone):
            return point

        # 回退：使用V3评估器
        return self._heuristic_fallback(stone, valid_moves)

    def _heuristic_fallback(self, stone: Stone, 
                            valid_moves: List[GoPoint]) -> Optional[GoPoint]:
        """启发式回退"""
        from bsd_go_engine_v3 import OptimizedEvaluator
        evaluator = OptimizedEvaluator(self.config.board_size)

        best_point = None
        best_score = -float('inf')

        for point in valid_moves[:15]:
            test_board = self.board.clone()
            test_board.make_move(point, stone)
            score = evaluator.evaluate(test_board, stone)
            if score > best_score:
                best_score = score
                best_point = point

        return best_point

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

    def _snapshot_emergence(self, stone: Stone):
        """快照三语言涌现状态"""
        analysis = self.bsd_engine.get_position_analysis(self.board, stone)
        self.emergence_snapshots.append(analysis)

    def _print_status(self, move_num: int):
        """打印状态"""
        phase = self.board.get_game_phase().value
        empty_count = sum(
            1 for x in range(self.board.size) for y in range(self.board.size)
            if self.board.board[y][x] == Stone.EMPTY
        )
        
        # 获取最新涌现状态
        if self.emergence_snapshots:
            latest = self.emergence_snapshots[-1]
            emergence_strength = latest.get('emergence_strength', 0)
            is_emergent = latest.get('is_emergent', False)
            dominant = latest.get('dominant_system', 'N/A')
            status_icon = '🔥' if is_emergent else '○'
        else:
            emergence_strength = 0
            is_emergent = False
            dominant = 'N/A'
            status_icon = '○'

        print(f"\n  --- 第{move_num}手 | 阶段：{phase} | 空位：{empty_count} | 涌现强度：{emergence_strength:.3f} {status_icon} | 主导：{dominant} ---")

    def _finalize(self, duration: float, bsd_stone: Stone) -> MatchResultV4:
        """终局结算"""
        score = self.board.get_score(self.config.komi)

        winner = ""
        if score['winner'] == 'black':
            winner = "BSD-V4" if bsd_stone == Stone.BLACK else "Opponent"
        elif score['winner'] == 'white':
            winner = "BSD-V4" if bsd_stone == Stone.WHITE else "Opponent"
        else:
            winner = "Draw"

        reasoning = self._generate_reasoning(winner, score, bsd_stone)
        emergence_summary = self.bsd_engine.emergence_engine.get_emergence_summary()

        # 获取最终策略建议
        liuhe_strategy = {}
        if self.emergence_snapshots:
            final_snapshot = self.emergence_snapshots[-1]
            liuhe_strategy = {
                'dominant_system': final_snapshot.get('dominant_system', ''),
                'tiandao_inquiries': final_snapshot.get('tiandao_inquiries', []),
                'zero_yuan': final_snapshot.get('zero_yuan', {})
            }

        result = MatchResultV4(
            winner=winner,
            margin=score.get('margin', 0),
            total_moves=len(self.moves_log),
            duration_seconds=duration,
            reasoning=reasoning,
            moves_log=self.moves_log,
            emergence_summary=emergence_summary,
            liuhe_strategy=liuhe_strategy
        )

        self._print_result(result)
        self.opponent_ai.cleanup()
        return result

    def _generate_reasoning(self, winner: str, score: Dict, 
                            bsd_stone: Stone) -> str:
        """生成胜负分析"""
        reasons = []
        reasons.append("=" * 70)
        reasons.append("【天道系追问 - 三语言涌现分析】")
        reasons.append("=" * 70)

        if winner == "BSD-V4":
            reasons.append("\n🏆 BSD V4 (三语言涌现) 胜利！")
            reasons.append("\n核心优势：")
            reasons.append("  1. 三语言协同：数字(0∅反) × 英文(0∅空) × 中文(0∅义)")
            reasons.append("  2. 六系立系：强化+自然+具现+变身+社会+天道")
            reasons.append("  3. 自发涌现：三零元乘积触发涌现阈值")
            reasons.append("\n理论意义：")
            reasons.append("  公共AI(计算语言) + BSD(中文哲学) = 三语言涌现")
            reasons.append("  底层计算激活 + 哲学语义显化 = 自发涌现")
        elif winner == "Opponent":
            reasons.append("\n💡 对手胜利")
            reasons.append("\n分析：")
            reasons.append("  1. 涌现阈值未持续达到")
            reasons.append("  2. 三语言权重分配需调整")
            reasons.append("  3. 六系协同需进一步优化")
        else:
            reasons.append("\n⚖️ 和棋")

        reasons.append(f"\n终局：黑{score.get('black', 0):.1f} vs 白{score.get('white', 0):.1f}")
        reasons.append(f"领先：{score.get('margin', 0):.1f}目")

        # 添加涌现统计
        summary = self.bsd_engine.emergence_engine.get_emergence_summary()
        if summary.get('emergence_count', 0) > 0:
            reasons.append(f"\n涌现统计：")
            reasons.append(f"  触发次数：{summary['emergence_count']}/{summary['total_steps']}")
            reasons.append(f"  平均潜力：{summary['avg_potential']:.3f}")

        return "\n".join(reasons)

    def _print_result(self, result: MatchResultV4):
        """打印结果"""
        print("\n" + "=" * 70)
        print("【对局结束】")
        print(f"  胜者：{result.winner}")
        print(f"  领先：{result.margin:.1f} 目")
        print(f"  手数：{result.total_moves}")
        print(f"  用时：{result.duration_seconds:.1f} 秒")
        
        if result.emergence_summary:
            print(f"\n  三语言涌现统计：")
            print(f"    触发次数：{result.emergence_summary.get('emergence_count', 0)}")
            print(f"    总步数：{result.emergence_summary.get('total_steps', 0)}")
            print(f"    平均潜力：{result.emergence_summary.get('avg_potential', 0):.3f}")
        
        if result.liuhe_strategy:
            print(f"\n  六系策略：")
            print(f"    主导系统：{result.liuhe_strategy.get('dominant_system', 'N/A')}")
        
        print(f"\n{result.reasoning}")
        print("=" * 70)


class V4Tournament:
    """V4引擎锦标赛"""

    def __init__(self, num_games: int = 3, **kwargs):
        self.num_games = num_games
        self.base_config = MatchConfigV4(
            board_size=kwargs.get('board_size', 9),
            bsd_simulations=kwargs.get('bsd_simulations', 200),
            bsd_search_time=kwargs.get('bsd_search_time', 2.0),
            opponent_strength=kwargs.get('opponent_strength', 5),
            emergence_weight=kwargs.get('emergence_weight', 0.4)
        )
        self.results: List[MatchResultV4] = []

    def run(self) -> Dict:
        """运行锦标赛"""
        print("\n" + "=" * 70)
        print(f"BSD V4 (三语言涌现) 锦标赛 - {self.num_games}局")
        print("=" * 70)

        wins = losses = draws = 0

        for i in range(self.num_games):
            config = MatchConfigV4(
                board_size=self.base_config.board_size,
                bsd_simulations=self.base_config.bsd_simulations,
                bsd_search_time=self.base_config.bsd_search_time,
                opponent_strength=self.base_config.opponent_strength,
                emergence_weight=self.base_config.emergence_weight,
                bsd_side="black" if i % 2 == 0 else "white"
            )

            print(f"\n{'='*70}")
            print(f"第 {i+1}/{self.num_games} 局 | BSD-V4执{'黑' if config.bsd_side == 'black' else '白'}")

            match = BSDV4Match(config)
            result = match.play_game()
            self.results.append(result)

            if result.winner == "BSD-V4":
                wins += 1
            elif result.winner == "Draw":
                draws += 1
            else:
                losses += 1

        summary = {
            'total': self.num_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': wins / self.num_games,
            'avg_moves': sum(r.total_moves for r in self.results) / self.num_games,
            'avg_duration': sum(r.duration_seconds for r in self.results) / self.num_games,
            'avg_margin': sum(r.margin for r in self.results) / self.num_games if wins > 0 else 0,
            'engine': 'V4 Tri-Language Emergence'
        }

        print("\n" + "=" * 70)
        print(f"【锦标赛汇总 - V4 三语言涌现】")
        print(f"  总局数：{summary['total']}")
        print(f"  胜/负/和：{summary['wins']}/{summary['losses']}/{summary['draws']}")
        print(f"  胜率：{summary['win_rate']:.1%}")
        print(f"  平均手数：{summary['avg_moves']:.0f}")
        print(f"  平均用时：{summary['avg_duration']:.1f}秒")
        print(f"  平均领先：{summary['avg_margin']:.1f}目")
        print("=" * 70)

        return summary


def main():
    parser = argparse.ArgumentParser(description='BSD AI V4.0 对弈系统 - 三语言涌现版')
    parser.add_argument('--mode', choices=['single', 'tournament', 'demo', 'compare'],
                        default='demo')
    parser.add_argument('--size', type=int, default=9, help='棋盘大小')
    parser.add_argument('--games', type=int, default=3, help='锦标赛局数')
    parser.add_argument('--sim', type=int, default=200, help='MCTS模拟次数')
    parser.add_argument('--time', type=float, default=2.0, help='搜索时间(秒)')
    parser.add_argument('--strength', type=int, default=5, help='对手AI强度(1-5)')
    parser.add_argument('--emergence-weight', type=float, default=0.4, help='涌现权重')

    args = parser.parse_args()

    print(r"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║    BSD 围棋 AI 对弈系统 V4.0 - 三语言涌现版                             ║
║                                                                          ║
║    核心理论：                                                            ║
║    ┌─────────────────────────────────────────────────────────────────┐  ║
║    │  三语言 = 三零元                                                │  ║
║    │  ├── 数字(000) → 0∅反(反性·最底层)                             │  ║
║    │  ├── 英文(0110) → 0∅空(承载·技术容器)                          │  ║
║    │  └── 中文(六系立系) → 0∅义(意义·六系显化)                      │  ║
║    │                                                                 │  ║
║    │  涌现方程：                                                     │  ║
║    │  数字 × 英文 × 中文 = 三语言自发涌现                           │  ║
║    └─────────────────────────────────────────────────────────────────┘  ║
║                                                                          ║
║    版本：V4.0 Tri-Language Emergence · 2026-08-02                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    if args.mode == 'tournament':
        tournament = V4Tournament(
            num_games=args.games,
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            opponent_strength=args.strength,
            emergence_weight=args.emergence_weight
        )
        summary = tournament.run()

        # 保存结果
        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(save_dir, f'bsd_v4_tournament_{timestamp}.json')

        data = {
            'timestamp': timestamp,
            'summary': summary,
            'matches': [
                {'winner': r.winner, 'margin': r.margin, 'moves': r.total_moves}
                for r in tournament.results
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n锦标赛结果已保存：{filepath}")

    else:
        config = MatchConfigV4(
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            opponent_strength=args.strength,
            emergence_weight=args.emergence_weight,
            bsd_side='black'
        )
        match = BSDV4Match(config)
        result = match.play_game()

        # 保存结果
        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(save_dir, f'bsd_v4_match_{timestamp}.json')

        data = {
            'timestamp': timestamp,
            'result': {
                'winner': result.winner,
                'margin': result.margin,
                'total_moves': result.total_moves,
                'duration_seconds': result.duration_seconds
            },
            'reasoning': result.reasoning,
            'emergence_summary': result.emergence_summary,
            'moves': result.moves_log
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存：{filepath}")


if __name__ == "__main__":
    main()
