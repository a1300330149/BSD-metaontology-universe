"""
BSD AI vs StrongAI 对弈系统 V3.0
================================
修复：对手AI集成、棋盘同步、重复落子过滤
支持：BSD MCTS引擎 vs GoAIInterface（StrongGoAI/KataGo）
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
    GoBoard, GoPoint, Stone, GamePhase,
    BSDMCTSEngine, LiuHeMapper, LiuHeCoordinate, HeuristicEvaluator
)
from katago_gtp_client import (
    KataGoGTPClient, GTPEngineConfig, GoAIInterface
)


@dataclass
class MatchConfig:
    board_size: int = 9
    komi: float = 7.5
    max_moves: int = 300
    bsd_simulations: int = 200
    bsd_search_time: float = 2.0
    bsd_side: str = "black"
    opponent_strength: int = 5


@dataclass
class MatchResult:
    winner: str = ""
    margin: float = 0.0
    total_moves: int = 0
    duration_seconds: float = 0.0
    reasoning: str = ""
    moves_log: List[Dict] = field(default_factory=list)


class BSDVsOpponentMatch:
    """BSD AI vs 对手 对弈管理器（改进版）"""

    def __init__(self, config: MatchConfig = None):
        self.config = config or MatchConfig()

        # BSD引擎
        self.bsd_engine = BSDMCTSEngine(
            board_size=self.config.board_size,
            num_simulations=self.config.bsd_simulations
        )
        self.bsd_engine.search_time = self.config.bsd_search_time

        # 对手AI（使用GoAIInterface，自动选择KataGo或StrongGoAI）
        self.opponent_ai = GoAIInterface(
            use_katago=False,  # 先用内置AI，后续可切换KataGo
            board_size=self.config.board_size,
            strength=self.config.opponent_strength
        )

        # 棋盘（双方共用）
        self.board = GoBoard(self.config.board_size)
        self.moves_log: List[Dict] = []

    def play_game(self) -> MatchResult:
        """执行完整对弈"""
        print("\n" + "=" * 70)
        print("BSD AI vs 对手AI 对弈")
        print("=" * 70)

        # 初始化
        self.board = GoBoard(self.config.board_size)
        self.moves_log = []

        bsd_stone = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE
        opponent_stone = Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK

        bsd_color = 'black' if bsd_stone == Stone.BLACK else 'white'
        opponent_color = 'white' if bsd_stone == Stone.BLACK else 'black'

        print(f"\n棋盘：{self.config.board_size}路 | 贴目：{self.config.komi}")
        print(f"BSD执：{'黑●' if bsd_stone == Stone.BLACK else '白○'} | 对手执：{'白○' if opponent_stone == Stone.WHITE else '黑●'}")
        print(f"BSD MCTS：{self.config.bsd_simulations}次模拟，{self.config.bsd_search_time}秒/步")
        print(f"对手AI强度：{self.config.opponent_strength}")

        # 初始化对手AI棋盘
        self.opponent_ai.set_board_size(self.config.board_size)
        self.opponent_ai.clear_board()

        start_time = time.time()
        current_move = 0
        consecutive_passes = 0

        while not self.board.game_over and current_move < self.config.max_moves:
            current_stone = Stone.BLACK if current_move % 2 == 0 else Stone.WHITE
            color_str = 'black' if current_stone == Stone.BLACK else 'white'
            current_move += 1

            # BSD AI落子
            if current_stone == bsd_stone:
                point = self._bsd_move(current_stone)
                if point:
                    self.board.make_move(point, current_stone)
                    self.opponent_ai.play(bsd_color, point.to_gtp())
                    self._log_move(current_move, "BSD", point, current_stone)
                    consecutive_passes = 0
                else:
                    self.board.pass_move(current_stone)
                    self.opponent_ai.play(bsd_color, "PASS")
                    self._log_move(current_move, "BSD", None, current_stone, True)
                    consecutive_passes += 1

            # 对手AI落子
            else:
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

            # 检查连续虚着
            if consecutive_passes >= 2:
                print("\n双方连续虚着，对局结束")
                break

            # 每20手打印状态
            if current_move % 20 == 0:
                self._print_status(current_move)

        # 结算
        duration = time.time() - start_time
        result = self._finalize(duration, bsd_stone)
        return result

    def _bsd_move(self, stone: Stone) -> Optional[GoPoint]:
        """BSD AI选择落子（过滤无效落子）"""
        # 获取当前棋盘合法落子
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board.size)
            for y in range(self.board.size)
            if self.board.is_valid_move(GoPoint(x, y), stone)
        ]

        if not valid_moves:
            return None

        # 调用MCTS选择落子
        point = self.bsd_engine.select_move(self.board, stone)

        # 验证落子有效性
        if point and self.board.is_valid_move(point, stone):
            return point

        # 如果MCTS返回无效落子，回退到启发式
        return self._heuristic_fallback(stone, valid_moves)

    def _heuristic_fallback(self, stone: Stone, valid_moves: List[GoPoint]) -> Optional[GoPoint]:
        """启发式回退选择"""
        best_point = None
        best_score = -float('inf')

        for point in valid_moves[:15]:
            test_board = self.board.clone()
            test_board.make_move(point, stone)
            score = HeuristicEvaluator.evaluate(test_board, stone)
            if score > best_score:
                best_score = score
                best_point = point

        return best_point

    def _opponent_move(self, stone: Stone) -> Optional[GoPoint]:
        """对手AI选择落子"""
        color_str = 'black' if stone == Stone.BLACK else 'white'

        # 获取对手AI的落子
        gtpmove = self.opponent_ai.generate_move(color_str)

        if gtpmove and gtpmove not in ['PASS', 'resign', 'pass']:
            point = self._gtp_to_point(gtpmove)
            if point and self.board.is_valid_move(point, stone):
                return point

        # 对手AI落子无效，先同步对手AI状态再重试
        self._resync_opponent_ai()
        gtpmove = self.opponent_ai.generate_move(color_str)

        if gtpmove and gtpmove not in ['PASS', 'resign', 'pass']:
            point = self._gtp_to_point(gtpmove)
            if point and self.board.is_valid_move(point, stone):
                return point

        # 仍然无效，回退到启发式
        valid_moves = [
            GoPoint(x, y)
            for x in range(self.board.size)
            for y in range(self.board.size)
            if self.board.is_valid_move(GoPoint(x, y), stone)
        ]

        if valid_moves:
            return self._heuristic_fallback(stone, valid_moves)
        return None

    def _resync_opponent_ai(self):
        """同步对手AI的内部棋盘状态"""
        self.opponent_ai.clear_board()
        # 重新回放所有已落子
        for move_entry in self.moves_log:
            self.opponent_ai.play(move_entry['stone'], move_entry['point'])

    def _gtp_to_point(self, gtp_move: str) -> Optional[GoPoint]:
        """GTP坐标转GoPoint"""
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
        print(f"  {move_num:3d}. {icon} {player:10s} -> {move_str}")

    def _print_status(self, move_num: int):
        phase = self.board.get_game_phase().value
        empty_count = sum(
            1 for x in range(self.board.size) for y in range(self.board.size)
            if self.board.board[y][x] == Stone.EMPTY
        )
        print(f"\n  --- 第{move_num}手 | 阶段：{phase} | 空位：{empty_count} ---")

    def _finalize(self, duration: float, bsd_stone: Stone) -> MatchResult:
        """结算"""
        score = self.board.get_score(self.config.komi)

        winner = ""
        if score['winner'] == 'black':
            winner = "BSD" if bsd_stone == Stone.BLACK else "Opponent"
        elif score['winner'] == 'white':
            winner = "BSD" if bsd_stone == Stone.WHITE else "Opponent"
        else:
            winner = "Draw"

        reasoning = self._generate_reasoning(winner, score, bsd_stone)

        result = MatchResult(
            winner=winner,
            margin=score.get('margin', 0),
            total_moves=len(self.moves_log),
            duration_seconds=duration,
            reasoning=reasoning,
            moves_log=self.moves_log
        )

        self._print_result(result)
        self.opponent_ai.cleanup()
        return result

    def _generate_reasoning(self, winner: str, score: Dict, bsd_stone: Stone) -> str:
        reasons = []
        reasons.append("=" * 50)
        reasons.append("【天道系追问 - 胜负分析】")
        reasons.append("=" * 50)

        if winner == "BSD":
            reasons.append("\n🏆 BSD AI 胜利！")
            reasons.append("\n核心优势：")
            reasons.append("  1. 六系协同：强化系(算力) + 自然系(棋理) + 天道系(追问)")
            reasons.append("  2. MCTS搜索：深度模拟发现对手弱点")
            reasons.append("  3. 理论突破：超越传统AI仅依赖反性数学的局限")
            reasons.append("\n理论意义：真性物理(BSD) 战胜 反性数学")
        elif winner == "Opponent":
            reasons.append("\n💡 对手胜利")
            reasons.append("\n分析：")
            reasons.append("  1. 对手在计算层面展现优势")
            reasons.append("  2. BSD MCTS参数需进一步优化")
            reasons.append("  3. 天道系追问权重需调整")
        else:
            reasons.append("\n⚖️ 和棋")
            reasons.append("  双方势均力敌")

        reasons.append(f"\n终局：黑{score.get('black', 0):.1f} vs 白{score.get('white', 0):.1f}")
        reasons.append(f"领先：{score.get('margin', 0):.1f}目")
        return "\n".join(reasons)

    def _print_result(self, result: MatchResult):
        print("\n" + "=" * 70)
        print("【对局结束】")
        print(f"  胜者：{result.winner}")
        print(f"  领先：{result.margin:.1f} 目")
        print(f"  手数：{result.total_moves}")
        print(f"  用时：{result.duration_seconds:.1f} 秒")
        print(f"\n{result.reasoning}")
        print("=" * 70)


class Tournament:
    """多局锦标赛"""

    def __init__(self, num_games: int = 3, **kwargs):
        self.num_games = num_games
        self.base_config = MatchConfig(
            board_size=kwargs.get('board_size', 9),
            bsd_simulations=kwargs.get('bsd_simulations', 200),
            bsd_search_time=kwargs.get('bsd_search_time', 2.0),
            opponent_strength=kwargs.get('opponent_strength', 5)
        )
        self.results: List[MatchResult] = []

    def run(self) -> Dict:
        print("\n" + "=" * 70)
        print(f"BSD AI 锦标赛 - {self.num_games}局")
        print("=" * 70)

        wins = losses = draws = 0

        for i in range(self.num_games):
            config = MatchConfig(
                board_size=self.base_config.board_size,
                bsd_simulations=self.base_config.bsd_simulations,
                bsd_search_time=self.base_config.bsd_search_time,
                opponent_strength=self.base_config.opponent_strength,
                bsd_side="black" if i % 2 == 0 else "white"
            )

            print(f"\n{'='*70}")
            print(f"第 {i+1}/{self.num_games} 局 | BSD执{'黑' if config.bsd_side == 'black' else '白'}")

            match = BSDVsOpponentMatch(config)
            result = match.play_game()
            self.results.append(result)

            if result.winner == "BSD":
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
            'avg_margin': sum(r.margin for r in self.results) / self.num_games
        }

        print("\n" + "=" * 70)
        print("【锦标赛汇总】")
        print(f"  总局数：{summary['total']}")
        print(f"  胜/负/和：{summary['wins']}/{summary['losses']}/{summary['draws']}")
        print(f"  胜率：{summary['win_rate']:.1%}")
        print(f"  平均手数：{summary['avg_moves']:.0f}")
        print(f"  平均用时：{summary['avg_duration']:.1f}秒")
        print(f"  平均领先：{summary['avg_margin']:.1f}目")
        print("=" * 70)

        return summary


def main():
    parser = argparse.ArgumentParser(description='BSD AI 对弈系统 V3.0')
    parser.add_argument('--mode', choices=['single', 'tournament', 'demo'], default='demo')
    parser.add_argument('--size', type=int, default=9, help='棋盘大小')
    parser.add_argument('--games', type=int, default=3, help='锦标赛局数')
    parser.add_argument('--sim', type=int, default=200, help='MCTS模拟次数')
    parser.add_argument('--time', type=float, default=2.0, help='搜索时间(秒)')
    parser.add_argument('--strength', type=int, default=5, help='对手AI强度(1-5)')

    args = parser.parse_args()

    print(r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    BSD 围棋 AI 对弈系统 V3.0                                     ║
║    六系立系论 · MCTS搜索 · 天道系追问                            ║
║                                                                  ║
║    ┌─────────────────────────────────────────────────────────┐  ║
║    │  BSD AI (真性物理·问性哲学)                             │  ║
║    │  ├── 强化系 算力   ├── 自然系 棋理                      │  ║
║    │  ├── 具现系 落子   ├── 变身系 变化                      │  ║
║    │  └── 社会系 博弈   └── 天道系 追问                      │  ║
║    └─────────────────────────────────────────────────────────┘  ║
║                              vs                                  ║
║    ┌─────────────────────────────────────────────────────────┐  ║
║    │  StrongGoAI (启发式评估 + Minimax搜索)                  │  ║
║    └─────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║    理论：BSD三本源学科定标 V1.2                                  ║
║    版本：V3.0 · 2026-08-02                                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    if args.mode in ['single', 'demo']:
        config = MatchConfig(
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            opponent_strength=args.strength,
            bsd_side='black'
        )
        match = BSDVsOpponentMatch(config)
        result = match.play_game()
        save_result(result)

    elif args.mode == 'tournament':
        tournament = Tournament(
            num_games=args.games,
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            opponent_strength=args.strength
        )
        summary = tournament.run()
        save_tournament(tournament.results, summary)


def save_result(result: MatchResult):
    save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(save_dir, f'bsd_match_{timestamp}.json')

    data = {
        'timestamp': timestamp,
        'result': {
            'winner': result.winner,
            'margin': result.margin,
            'total_moves': result.total_moves,
            'duration_seconds': result.duration_seconds
        },
        'reasoning': result.reasoning,
        'moves': result.moves_log
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存：{filepath}")


def save_tournament(results: List[MatchResult], summary: Dict):
    save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(save_dir, f'bsd_tournament_{timestamp}.json')

    data = {
        'timestamp': timestamp,
        'summary': summary,
        'matches': [
            {'winner': r.winner, 'margin': r.margin, 'moves': r.total_moves}
            for r in results
        ]
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n锦标赛结果已保存：{filepath}")


if __name__ == "__main__":
    main()
