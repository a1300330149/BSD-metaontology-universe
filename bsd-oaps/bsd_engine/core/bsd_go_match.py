"""
BSD围棋AI vs 对手 对弈系统
==============================
整合BSD围棋引擎与KataGo/内置AI，实现完整对弈流程
支持：
1. BSD AI（六系协同）vs KataGo（反性数学）
2. BSD AI vs 简单AI
3. 对弈记录与分析

理论依据：
- BSD三本源学科定标：真性物理(BSD) vs 反性数学(KataGo)
- 六系立系论：天道系追问 vs 强化系计算
"""

import sys
import json
import time
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from datetime import datetime
import os

# 添加引擎路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_go_engine import (
    GoBoard, GoPoint, Stone, GamePhase,
    LiuHeGoMapper, LiuHeGoCoordinate,
    BSDGoEngine, Move, MoveEvaluation,
    GameRecord, GoMatchManager
)
from katago_gtp_client import (
    GoAIInterface, GTPEngineConfig
)


# ============================================================================
# 1. 对弈配置
# ============================================================================

@dataclass
class MatchConfig:
    """对弈配置"""
    board_size: int = 19
    komi: float = 7.5
    max_moves: int = 300
    time_control: int = 30  # 思考时间（秒）
    use_katago: bool = False
    katago_path: str = "katago"
    model_path: str = ""
    bsd_side: str = "black"  # BSD执哪方
    opponent_name: str = "KataGo"


# ============================================================================
# 2. 对弈结果
# ============================================================================

@dataclass
class MatchResult:
    """对弈结果"""
    winner: str = ""          # "BSD" / "Opponent" / "Draw"
    margin: float = 0.0
    total_moves: int = 0
    duration_seconds: float = 0.0
    game_phase_at_end: str = ""
    final_score: Dict = field(default_factory=dict)
    reasoning: str = ""      # 天道系追问的胜负理由
    liuhe_analysis: List[Dict] = field(default_factory=list)  # 关键手的六系分析


# ============================================================================
# 3. BSD vs 对手 对弈管理器
# ============================================================================

class BSDVsOpponentMatch:
    """BSD围棋AI vs 对手 对弈管理器"""

    def __init__(self, config: MatchConfig = None):
        self.config = config or MatchConfig()
        self.bsd_engine = BSDGoEngine(self.config.board_size)
        self.opponent_ai = GoAIInterface(use_katago=self.config.use_katago,
                                         katago_path=self.config.katago_path,
                                         model_path=self.config.model_path,
                                         board_size=self.config.board_size)
        self.bsd_board = GoBoard(self.config.board_size)
        self.move_log: List[Dict] = []
        self.liuhe_analyses: List[Dict] = []
        self.start_time: float = 0

    def play_game(self) -> MatchResult:
        """执行完整对弈"""
        print("=" * 70)
        print(f"BSD围棋AI vs {self.config.opponent_name}")
        print("=" * 70)

        # 初始化
        self._init_game()
        self.start_time = time.time()

        bsd_stone = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE
        opponent_stone = Stone.WHITE if bsd_stone == Stone.BLACK else Stone.BLACK

        print(f"\n棋盘：{self.config.board_size}路 | 贴目：{self.config.komi}")
        print(f"BSD执：{'黑' if bsd_stone == Stone.BLACK else '白'} | 对手执：{'白' if opponent_stone == Stone.BLACK else '黑'}")

        # 设置对手AI
        self.opponent_ai.set_board_size(self.config.board_size)
        self.opponent_ai.clear_board()

        current_move = 0
        while not self.bsd_board.game_over and current_move < self.config.max_moves:
            current_stone = Stone.BLACK if current_move % 2 == 0 else Stone.WHITE
            color_str = 'black' if current_stone == Stone.BLACK else 'white'
            current_move += 1

            # 选择落子
            if current_stone == bsd_stone:
                # BSD AI落子
                point = self._bsd_move(current_stone)
                if point:
                    self.bsd_board.make_move(point, current_stone)
                    self._log_move(current_move, "BSD", point, current_stone)
                    # 同步到对手AI
                    gtpmove = point.to_gtp()
                    self.opponent_ai.play(color_str, gtpmove)
                else:
                    self.bsd_board.pass_move(current_stone)
                    self.opponent_ai.play(color_str, "PASS")
                    self._log_move(current_move, "BSD", None, current_stone, is_pass=True)
            else:
                # 对手AI落子
                gtpmove = self.opponent_ai.generate_move(color_str)
                if gtpmove and gtpmove not in ['PASS', 'resign', 'pass']:
                    point = self._gtp_to_point(gtpmove)
                    if point and self.bsd_board.is_valid_move(point, current_stone):
                        self.bsd_board.make_move(point, current_stone)
                        self._log_move(current_move, self.config.opponent_name, point, current_stone)
                    else:
                        # 如果无效，BSD自己选择
                        point = self._bsd_move(current_stone)
                        if point:
                            self.bsd_board.make_move(point, current_stone)
                            self._log_move(current_move, self.config.opponent_name + '(fallback)', point, current_stone)
                else:
                    self.bsd_board.pass_move(current_stone)
                    self._log_move(current_move, self.config.opponent_name, None, current_stone, is_pass=True)

            # 检查连续虚着
            if self.bsd_board.consecutive_passes >= 2:
                break

            # 每50手打印状态
            if current_move % 50 == 0:
                self._print_status(current_move)

        # 结算
        return self._finalize()

    def _init_game(self):
        """初始化对局"""
        self.bsd_board = GoBoard(self.config.board_size)
        self.move_log = []
        self.liuhe_analyses = []

    def _bsd_move(self, stone: Stone) -> Optional[GoPoint]:
        """BSD AI选择落子"""
        # 获取当前局面的六系坐标
        coord = LiuHeGoMapper.map_board_state(self.bsd_board, stone)

        # 记录关键局面分析
        if self.bsd_board.get_game_phase() != GamePhase.OPENING or len(self.move_log) > 60:
            self.liuhe_analyses.append({
                'move': len(self.move_log) + 1,
                'phase': self.bsd_board.get_game_phase().value,
                'coordinate': {
                    '强化系': coord.qh, '自然系': coord.zr,
                    '具现系': coord.jx, '变身系': coord.bs,
                    '社会系': coord.sh, '天道系': coord.td
                },
                'dominant': coord.dominant_system()
            })

        # 选择落子
        return self.bsd_engine.select_move(self.bsd_board, stone)

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
        """记录落子"""
        entry = {
            'move': move_num,
            'player': player,
            'stone': 'black' if stone == Stone.BLACK else 'white',
            'point': point.to_gtp() if point else 'PASS',
            'is_pass': is_pass
        }
        self.move_log.append(entry)

        # 打印
        stone_icon = '●' if stone == Stone.BLACK else '○'
        move_str = 'PASS' if is_pass else point.to_gtp()
        print(f"  {move_num:3d}. {stone_icon} {player:12s} -> {move_str}")

    def _print_status(self, move_num: int):
        """打印状态"""
        phase = self.bsd_board.get_game_phase().value
        analysis = self.bsd_engine.mapper.map_board_state(
            self.bsd_board, self.bsd_board.current_player
        )
        print(f"\n  --- 第{move_num}手 | 阶段：{phase} | 主导系：{analysis.dominant_system()} ---")

    def _finalize(self) -> MatchResult:
        """结算对局"""
        duration = time.time() - self.start_time
        score = self.bsd_board.get_score(self.config.komi)

        bsd_stone_enum = Stone.BLACK if self.config.bsd_side == "black" else Stone.WHITE

        # 判断胜负
        winner = ""
        if score['winner'] == 'black':
            winner = "BSD" if bsd_stone_enum == Stone.BLACK else self.config.opponent_name
        elif score['winner'] == 'white':
            winner = "BSD" if bsd_stone_enum == Stone.WHITE else self.config.opponent_name
        else:
            winner = "Draw"

        # 生成天道系理由
        reasoning = self._generate_reasoning(winner, score)

        result = MatchResult(
            winner=winner,
            margin=score.get('margin', 0),
            total_moves=len(self.move_log),
            duration_seconds=duration,
            game_phase_at_end=self.bsd_board.get_game_phase().value,
            final_score=score,
            reasoning=reasoning,
            liuhe_analysis=self.liuhe_analyses[-10:]  # 最后10个关键分析
        )

        # 打印结果
        self._print_result(result)

        # 清理对手AI
        self.opponent_ai.cleanup()

        return result

    def _generate_reasoning(self, winner: str, score: Dict) -> str:
        """生成天道系追问的胜负理由"""
        reasons = []

        if winner == "BSD":
            reasons.append("【BSD胜利分析】")
            reasons.append("  天道系显化：BSD不仅在计算上超越对手，更在意义层面把握了棋道")
            reasons.append("  六系协同：强化系(算力) + 自然系(棋理) + 天道系(追问) 的完整闭环")
            reasons.append("  核心优势：超越了传统AI仅依赖反性数学（蒙特卡洛树搜索）的局限")
        elif winner == self.config.opponent_name:
            reasons.append("【对手胜利分析】")
            reasons.append("  本局对手在计算层面展现优势")
            reasons.append("  BSD天道系追问已启动，但需进一步强化权重动态调整")
            reasons.append("  理论意义：反性数学(算力) vs 问性哲学(意义) 的博弈仍在继续")
        else:
            reasons.append("【和棋分析】")
            reasons.append("  双方势均力敌，体现了六系平衡的可能性")

        return "\n".join(reasons)

    def _print_result(self, result: MatchResult):
        """打印结果"""
        print("\n" + "=" * 70)
        print("【对局结束】")
        print(f"  胜者：{result.winner}")
        print(f"  领先：{result.margin:.1f} 目")
        print(f"  手数：{result.total_moves}")
        print(f"  用时：{result.duration_seconds:.1f} 秒")
        print(f"  结束阶段：{result.game_phase_at_end}")
        print(f"\n【胜负分析】")
        print(result.reasoning)
        print("\n【关键手六系分析】")
        for analysis in result.liuhe_analysis[-5:]:
            print(f"  第{analysis['move']}手 | {analysis['phase']} | 主导：{analysis['dominant']}")
            coord_str = " | ".join(f"{k}:{v:.3f}" for k, v in analysis['coordinate'].items())
            print(f"    {coord_str}")
        print("=" * 70)


# ============================================================================
# 4. 多局对弈
# ============================================================================

class MultiMatchTournament:
    """多局对弈锦标赛"""

    def __init__(self, num_games: int = 10, **kwargs):
        self.num_games = num_games
        self.configs = [
            MatchConfig(
                board_size=kwargs.get('board_size', 9),
                use_katago=kwargs.get('use_katago', False),
                komi=kwargs.get('komi', 7.5)
            ) for _ in range(num_games)
        ]
        # 交替先后手
        for i, config in enumerate(self.configs):
            config.bsd_side = "black" if i % 2 == 0 else "white"

        self.results: List[MatchResult] = []

    def run(self) -> Dict:
        """运行锦标赛"""
        print("\n" + "=" * 70)
        print(f"BSD围棋AI 锦标赛 - {self.num_games}局")
        print("=" * 70)

        wins = 0
        losses = 0
        draws = 0

        for i, config in enumerate(self.configs):
            print(f"\n{'='*70}")
            print(f"第 {i+1}/{self.num_games} 局 | BSD执{'黑' if config.bsd_side == 'black' else '白'}")
            print("=" * 70)

            match = BSDVsOpponentMatch(config)
            result = match.play_game()
            self.results.append(result)

            if result.winner == "BSD":
                wins += 1
            elif result.winner == "Draw":
                draws += 1
            else:
                losses += 1

        # 汇总
        summary = {
            'total_games': self.num_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': wins / self.num_games,
            'avg_moves': sum(r.total_moves for r in self.results) / self.num_games,
            'avg_duration': sum(r.duration_seconds for r in self.results) / self.num_games
        }

        print("\n" + "=" * 70)
        print("【锦标赛汇总】")
        print(f"  总局数：{summary['total_games']}")
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
    """主程序入口"""
    import argparse

    parser = argparse.ArgumentParser(description='BSD围棋AI对弈系统')
    parser.add_argument('--mode', choices=['single', 'tournament', 'demo'],
                        default='demo', help='运行模式')
    parser.add_argument('--size', type=int, default=9, help='棋盘大小')
    parser.add_argument('--games', type=int, default=5, help='锦标赛局数')
    parser.add_argument('--katago', action='store_true', help='使用KataGo引擎')
    parser.add_argument('--katago-path', type=str, default='katago', help='KataGo路径')
    parser.add_argument('--model', type=str, default='', help='KataGo模型路径')

    args = parser.parse_args()

    if args.mode == 'demo':
        # 演示模式
        print("""
╔══════════════════════════════════════════════════════════════╗
║          BSD围棋AI 演示系统 V1.0                             ║
║          基于六系立系论的围棋对弈引擎                         ║
╠══════════════════════════════════════════════════════════════╣
║  架构：                                                      ║
║  ┌─────────────────────────────────────────────────────┐   ║
║  │  BSD AI (六系协同决策)                              │   ║
║  │  ├── 强化系 (算力)  ├── 自然系 (棋理)               │   ║
║  │  ├── 具现系 (落子)  ├── 变身系 (变化)               │   ║
║  │  └── 社会系 (博弈)  └── 天道系 (追问)               │   ║
║  └─────────────────────────────────────────────────────┘   ║
║                          vs                                 ║
║  ┌─────────────────────────────────────────────────────┐   ║
║  │  对手 AI (反性数学)                                 │   ║
║  │  └── KataGo / SimpleGoAI                            │   ║
║  └─────────────────────────────────────────────────────┘   ║
║                                                              ║
║  核心理论：                                                  ║
║  - 三本源学科：真性物理(BSD) vs 反性数学(AI)                ║
║  - 六系立系论：锚点·闭环·演化                               ║
║  - 天道系追问：超越计算的棋道意义                            ║
╚══════════════════════════════════════════════════════════════╝
        """)

        # 运行演示
        demo_config = MatchConfig(
            board_size=args.size,
            use_katago=args.katago,
            katago_path=args.katago_path,
            model_path=args.model,
            bsd_side='black'
        )
        match = BSDVsOpponentMatch(demo_config)
        result = match.play_game()

        # 保存结果
        save_result(result)

    elif args.mode == 'single':
        # 单局模式
        config = MatchConfig(
            board_size=args.size,
            use_katago=args.katago,
            katago_path=args.katago_path,
            model_path=args.model
        )
        match = BSDVsOpponentMatch(config)
        result = match.play_game()
        save_result(result)

    elif args.mode == 'tournament':
        # 锦标赛模式
        tournament = MultiMatchTournament(
            num_games=args.games,
            board_size=args.size,
            use_katago=args.katago,
            katago_path=args.katago_path,
            model_path=args.model
        )
        summary = tournament.run()

        # 保存锦标赛结果
        save_tournament_result(tournament.results, summary)


def save_result(result: MatchResult):
    """保存单局结果"""
    save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(save_dir, f'bsd_go_match_{timestamp}.json')

    data = {
        'timestamp': timestamp,
        'winner': result.winner,
        'margin': result.margin,
        'total_moves': result.total_moves,
        'duration_seconds': result.duration_seconds,
        'reasoning': result.reasoning,
        'liuhe_analysis': result.liuhe_analysis
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至：{filepath}")


def save_tournament_result(results: List[MatchResult], summary: Dict):
    """保存锦标赛结果"""
    save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'match_results')
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(save_dir, f'bsd_go_tournament_{timestamp}.json')

    data = {
        'timestamp': timestamp,
        'summary': summary,
        'matches': [
            {
                'winner': r.winner,
                'margin': r.margin,
                'total_moves': r.total_moves,
                'reasoning': r.reasoning
            }
            for r in results
        ]
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n锦标赛结果已保存至：{filepath}")


if __name__ == "__main__":
    main()
