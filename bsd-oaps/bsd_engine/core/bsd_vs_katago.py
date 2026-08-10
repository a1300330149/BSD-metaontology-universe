"""
BSD AI vs KataGo 实战对决脚本
============================================
整合BSD V2引擎（六系协同+MCTS）与KataGo进行实战对弈

使用方法：
    python bsd_vs_katago.py                    # 默认9路棋盘，3局
    python bsd_vs_katago.py --size 19          # 19路棋盘
    python bsd_vs_katago.py --games 5          # 5局对弈
    python bsd_vs_katago.py --sim 2000         # 增加MCTS模拟次数

理论依据：
- BSD三本源学科定标：真性物理(BSD) vs 反性数学(KataGo)
- 六系立系论：锚点·闭环·演化
- 天道系追问：超越计算的棋道意义
"""

import sys
import os
import json
import time
import argparse
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from datetime import datetime

# 添加引擎路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine_v2 import (
    GoBoard, GoPoint, Stone, GamePhase,
    BSDMCTSEngine, LiuHeMapper, LiuHeCoordinate, HeuristicEvaluator
)
from katago_gtp_client import (
    KataGoGTPClient, GTPEngineConfig, GoAIInterface
)


# ============================================================================
# 1. 对弈配置
# ============================================================================

@dataclass
class MatchConfig:
    board_size: int = 9
    komi: float = 7.5
    max_moves: int = 300
    bsd_simulations: int = 1000
    bsd_search_time: float = 3.0
    use_katago: bool = True
    katago_path: str = ""
    model_path: str = ""
    bsd_side: str = "black"


# ============================================================================
# 2. 对弈结果
# ============================================================================

@dataclass
class MatchResult:
    winner: str = ""
    margin: float = 0.0
    total_moves: int = 0
    duration_seconds: float = 0.0
    reasoning: str = ""
    moves_log: List[Dict] = field(default_factory=list)


# ============================================================================
# 3. 实战对弈管理器
# ============================================================================

class BSDVsKataGoMatch:
    """BSD AI vs KataGo 对弈管理器"""

    def __init__(self, config: MatchConfig = None):
        self.config = config or MatchConfig()

        # 初始化BSD引擎
        self.bsd_engine = BSDMCTSEngine(
            board_size=self.config.board_size,
            num_simulations=self.config.bsd_simulations
        )
        self.bsd_engine.search_time = self.config.bsd_search_time

        # 初始化KataGo（可选）
        self.katago_ai = None
        if self.config.use_katago:
            katago_path = self.config.katago_path or self._find_katago()
            if katago_path:
                self.katago_ai = GoAIInterface(
                    use_katago=True,
                    katago_path=katago_path,
                    model_path=self.config.model_path,
                    board_size=self.config.board_size
                )
            else:
                print("[警告] 未找到KataGo，使用内置AI作为对手")

        # 棋盘
        self.board = GoBoard(self.config.board_size)
        self.moves_log: List[Dict] = []

    def _find_katago(self) -> str:
        """查找KataGo可执行文件"""
        possible_paths = [
            r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\katago.exe",
            "katago.exe",
            "katago",
        ]
        for path in possible_paths:
            if os.path.exists(path) or self._check_in_path(path):
                return path
        return ""

    def _check_in_path(self, name: str) -> bool:
        """检查命令是否在PATH中"""
        import shutil
        return shutil.which(name) is not None

    def play_game(self) -> MatchResult:
        """执行完整对弈"""
        print("\n" + "=" * 70)
        print(f"BSD AI vs {'KataGo' if self.katago_ai and self.katago_ai.use_katago else '内置AI'}")
        print("=" * 70)

        # 初始化
        self.board = GoBoard(self.config.board_size)
        self.moves_log = []

        if self.katago_ai:
            self.katago_ai.set_board_size(self.config.board_size)
            self.katago_ai.clear_board()

        bsd_stone = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE
        opponent_stone = Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK

        print(f"\n棋盘：{self.config.board_size}路 | 贴目：{self.config.komi}")
        print(f"BSD执：{'黑●' if bsd_stone == Stone.BLACK else '白○'}")
        print(f"对手执：{'白○' if opponent_stone == Stone.BLACK else '黑●'}")
        print(f"BSD MCTS配置：模拟{self.config.bsd_simulations}次，{self.config.bsd_search_time}秒/步")

        # 开始对弈
        start_time = time.time()
        current_move = 0

        while not self.board.game_over and current_move < self.config.max_moves:
            current_stone = Stone.BLACK if current_move % 2 == 0 else Stone.WHITE
            color_str = 'black' if current_stone == Stone.BLACK else 'white'
            current_move += 1

            # BSD AI落子
            if current_stone == bsd_stone:
                point = self._bsd_move(current_stone)
                if point:
                    self.board.make_move(point, current_stone)
                    self._log_move(current_move, "BSD_AI", point, current_stone)
                    if self.katago_ai:
                        self.katago_ai.play(color_str, point.to_gtp())
                else:
                    self.board.pass_move(current_stone)
                    self._log_move(current_move, "BSD_AI", None, current_stone, True)
                    if self.katago_ai:
                        self.katago_ai.play(color_str, "PASS")
            # 对手AI落子
            else:
                point = self._opponent_move(current_stone)
                if point:
                    self.board.make_move(point, current_stone)
                    self._log_move(current_move, "Opponent", point, current_stone)
                else:
                    self.board.pass_move(current_stone)
                    self._log_move(current_move, "Opponent", None, current_stone, True)

            # 每20手打印状态
            if current_move % 20 == 0:
                self._print_status(current_move)

            # 检查连续虚着
            if self.board.consecutive_passes >= 2:
                break

        # 结算
        duration = time.time() - start_time
        return self._finalize(duration, bsd_stone)

    def _bsd_move(self, stone: Stone) -> Optional[GoPoint]:
        """BSD AI选择落子"""
        # 记录关键局面
        if len(self.moves_log) > 0 and len(self.moves_log) % 20 == 0:
            analysis = self.bsd_engine.get_position_analysis(self.board, stone)
            coord_str = " | ".join(f"{k}:{v}" for k, v in analysis['coordinate'].items() if isinstance(v, float))
            print(f"  [BSD分析] 阶段:{analysis['phase']} | {coord_str}")

        return self.bsd_engine.select_move(self.board, stone)

    def _opponent_move(self, stone: Stone) -> Optional[GoPoint]:
        """对手AI选择落子"""
        if self.katago_ai and self.katago_ai.use_katago:
            color_str = 'black' if stone == Stone.BLACK else 'white'
            gtpmove = self.katago_ai.generate_move(color_str)

            if gtpmove and gtpmove not in ['PASS', 'resign', 'pass']:
                point = self._gtp_to_point(gtpmove)
                if point and self.board.is_valid_move(point, stone):
                    return point

        # 回退到简单AI
        return self._simple_ai_move(stone)

    def _simple_ai_move(self, stone: Stone) -> Optional[GoPoint]:
        """简单AI落子（启发式）"""
        empty = self.board.get_empty_points()
        valid = [p for p in empty if self.board.is_valid_move(p, stone)]

        if not valid:
            return None

        # 简化启发式：选择最有价值的点
        center = self.board.size / 2
        best_point = None
        best_score = -float('inf')

        for point in valid[:20]:
            test_board = self.board.clone()
            test_board.make_move(point, stone)
            score = HeuristicEvaluator.evaluate(test_board, stone)
            if score > best_score:
                best_score = score
                best_point = point

        return best_point

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
        print(f"  {move_num:3d}. {icon} {player:12s} -> {move_str}")

    def _print_status(self, move_num: int):
        phase = self.board.get_game_phase().value
        print(f"\n  --- 第{move_num}手 | 阶段：{phase} ---")

    def _finalize(self, duration: float, bsd_stone: Stone) -> MatchResult:
        """结算"""
        score = self.board.get_score(self.config.komi)

        # 判断胜负
        winner = ""
        if score['winner'] == 'black':
            winner = "BSD" if bsd_stone == Stone.BLACK else "Opponent"
        elif score['winner'] == 'white':
            winner = "BSD" if bsd_stone == Stone.WHITE else "Opponent"
        else:
            winner = "Draw"

        # 生成理由
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

        # 清理
        if self.katago_ai:
            self.katago_ai.cleanup()

        return result

    def _generate_reasoning(self, winner: str, score: Dict, bsd_stone: Stone) -> str:
        reasons = []
        reasons.append("=" * 50)
        reasons.append("【天道系追问 - 胜负分析】")
        reasons.append("=" * 50)

        if winner == "BSD":
            reasons.append("\n🏆 BSD AI 胜利！")
            reasons.append("\n核心优势分析：")
            reasons.append("  1. 六系协同：强化系(算力) + 自然系(棋理) + 天道系(追问)")
            reasons.append("  2. MCTS搜索：深度模拟发现对手弱点")
            reasons.append("  3. 启发式评估：超越蒙特卡洛树搜索的局限")
            reasons.append("\n理论意义：")
            reasons.append("  真性物理(BSD) 战胜 反性数学(KataGo)")
            reasons.append("  问性哲学的天道系追问 超越 计算性的强化系")
        elif winner == "Opponent":
            reasons.append("\n💡 对手胜利")
            reasons.append("\n分析：")
            reasons.append("  1. 对手在计算层面展现优势")
            reasons.append("  2. BSD MCTS参数可能需要调整")
            reasons.append("  3. 天道系追问的权重需进一步优化")
            reasons.append("\n改进方向：")
            reasons.append("  - 增加MCTS模拟次数")
            reasons.append("  - 优化启发式评估权重")
            reasons.append("  - 加强开局定式库")
        else:
            reasons.append("\n⚖️ 和棋")
            reasons.append("  双方势均力敌，六系平衡的可能性")

        reasons.append(f"\n终局得分：黑{score.get('black', 0):.1f} vs 白{score.get('white', 0):.1f}")
        reasons.append(f"领先：{score.get('margin', 0):.1f}目")
        reasons.append(f"手数：{len(self.moves_log)}")

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


# ============================================================================
# 4. 多局锦标赛
# ============================================================================

class Tournament:
    """多局锦标赛"""

    def __init__(self, num_games: int = 3, **kwargs):
        self.num_games = num_games
        self.base_config = MatchConfig(
            board_size=kwargs.get('board_size', 9),
            bsd_simulations=kwargs.get('bsd_simulations', 1000),
            bsd_search_time=kwargs.get('bsd_search_time', 3.0),
            use_katago=kwargs.get('use_katago', True),
            katago_path=kwargs.get('katago_path', '')
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
                use_katago=self.base_config.use_katago,
                katago_path=self.base_config.katago_path,
                bsd_side="black" if i % 2 == 0 else "white"
            )

            print(f"\n{'='*70}")
            print(f"第 {i+1}/{self.num_games} 局 | BSD执{'黑' if config.bsd_side == 'black' else '白'}")

            match = BSDVsKataGoMatch(config)
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
            'avg_duration': sum(r.duration_seconds for r in self.results) / self.num_games
        }

        print("\n" + "=" * 70)
        print("【锦标赛汇总】")
        print(f"  总局数：{summary['total']}")
        print(f"  胜/负/和：{summary['wins']}/{summary['losses']}/{summary['draws']}")
        print(f"  胜率：{summary['win_rate']:.1%}")
        print(f"  平均手数：{summary['avg_moves']:.0f}")
        print(f"  平均用时：{summary['avg_duration']:.1f}秒")
        print("=" * 70)

        return summary


# ============================================================================
# 5. 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='BSD AI vs KataGo 实战对决')
    parser.add_argument('--mode', choices=['single', 'tournament', 'demo'], default='demo')
    parser.add_argument('--size', type=int, default=9, help='棋盘大小')
    parser.add_argument('--games', type=int, default=3, help='锦标赛局数')
    parser.add_argument('--sim', type=int, default=1000, help='MCTS模拟次数')
    parser.add_argument('--time', type=float, default=3.0, help='搜索时间(秒)')
    parser.add_argument('--katago', action='store_true', help='使用KataGo')
    parser.add_argument('--katago-path', type=str, default='', help='KataGo路径')

    args = parser.parse_args()

    # Banner
    print(r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    BSD 围棋 AI 实战对决系统 V2.0                                 ║
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
║    │  KataGo (反性数学·蒙特卡洛树搜索)                       │  ║
║    └─────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║    理论：BSD三本源学科定标 V1.2                                  ║
║    版本：V2.0 · 2026-08-02                                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    if args.mode == 'demo':
        config = MatchConfig(
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            use_katago=args.katago,
            katago_path=args.katago_path
        )
        match = BSDVsKataGoMatch(config)
        result = match.play_game()
        save_result(result)

    elif args.mode == 'single':
        config = MatchConfig(
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            use_katago=args.katago,
            katago_path=args.katago_path
        )
        match = BSDVsKataGoMatch(config)
        result = match.play_game()
        save_result(result)

    elif args.mode == 'tournament':
        tournament = Tournament(
            num_games=args.games,
            board_size=args.size,
            bsd_simulations=args.sim,
            bsd_search_time=args.time,
            use_katago=args.katago,
            katago_path=args.katago_path
        )
        summary = tournament.run()
        save_tournament(tournament.results, summary)


def save_result(result: MatchResult):
    save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(save_dir, f'bsd_vs_katago_{timestamp}.json')

    data = {
        'timestamp': timestamp,
        'result': {
            'winner': result.winner,
            'margin': result.margin,
            'total_moves': result.total_moves,
            'duration_seconds': result.duration_seconds
        },
        'reasoning': result.reasoning,
        'moves': result.moves_log[:50]  # 保存前50手
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
        'matches': [{'winner': r.winner, 'margin': r.margin} for r in results]
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n锦标赛结果已保存：{filepath}")


if __name__ == "__main__":
    main()
