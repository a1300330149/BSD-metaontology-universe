"""
KataGo GTP客户端 - 通过GTP协议连接KataGo引擎
============================================
实现与KataGo等围棋AI引擎的通信，支持：
1. GTP 2.0协议通信
2. 棋力等级调整
3. 分析与评估

使用方法：
    client = KataGoGTPClient()
    client.connect()
    client.set_board_size(19)
    move = client.generate_move("black")
"""

import subprocess
import threading
import time
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
import sys
import os
import ctypes


def _init_windows_sockets():
    """在Windows上初始化Winsock，确保子进程可以正常工作"""
    if sys.platform == 'win32':
        try:
            ws2_32 = ctypes.windll.ws2_32
            wsa_startup = ws2_32.WSAStartup
            # MAKEWORD(2, 2) = 0x0202
            wsa_startup(0x0202, ctypes.byref(ctypes.c_void_p()))
            return True
        except Exception:
            return False
    return True


# ============================================================================
# 1. GTP协议常量
# ============================================================================

class GTPCommand:
    """GTP指令常量"""
    PROTOCOL_VERSION = "protocol_version"
    NAME = "name"
    VERSION = "version"
    KNOWN_COMMAND = "known_command"
    LIST_COMMANDS = "list_commands"
    QUIT = "quit"
    BOARDSIZE = "boardsize"
    CLEAR_BOARD = "clear_board"
    KOMI = "komi"
    PLAY = "play"
    GENMOVE = "genmove"
    GENMOVE_ANALYSIS = "lzgenmove"
    SHOWBOARD = "showboard"
    FINAL_SCORE = "final_score"
    FINAL_STATUS = "final_status"
    TIME_SETTINGS = "time_settings"
    TIME_LEFT = "time_left"
    OBSERVE = "observe"
    REGISTER = "register"


# ============================================================================
# 2. GTP客户端
# ============================================================================

@dataclass
class GTPEngineConfig:
    """GTP引擎配置"""
    executable_path: str = "katago"
    model_path: str = ""
    config_path: str = ""
    board_size: int = 19
    komi: float = 7.5
    time_control: int = 30  # 每步思考时间（秒）
    extra_args: List[str] = None

    def __post_init__(self):
        if self.extra_args is None:
            self.extra_args = []


class KataGoGTPClient:
    """KataGo GTP客户端"""

    def __init__(self, config: GTPEngineConfig = None):
        self.config = config or GTPEngineConfig()
        self.process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._request_id = 0
        self._connected = False
        self._command_handlers: Dict[str, Callable] = {}

    def connect(self) -> bool:
        """连接到KataGo引擎"""
        if self._connected:
            return True

        try:
            # 在Windows上初始化Winsock
            _init_windows_sockets()
            
            # 构建命令行参数 - 使用gtp子命令
            cmd = [self.config.executable_path, "gtp"]

            if self.config.model_path:
                cmd.extend(["-model", self.config.model_path])

            if self.config.config_path:
                cmd.extend(["-config", self.config.config_path])
            
            # 使用override-config禁用日志到stderr，减少干扰
            cmd.extend(["-override-config", "logToStderr=false"])

            # 添加额外参数
            cmd.extend(self.config.extra_args)

            # 启动进程 - 不使用CREATE_NO_WINDOW以避免网络初始化问题
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # 等待引擎启动
            time.sleep(1.0)

            # 检查进程是否存活
            if self.process.poll() is not None:
                error_output = self._read_error()
                print(f"[KataGo] 引擎启动失败: {error_output}")
                return False

            # 初始化协议
            self._connected = True
            self._init_protocol()

            print(f"[KataGo] 已连接到引擎")
            return True

        except FileNotFoundError:
            print(f"[KataGo] 找不到可执行文件: {self.config.executable_path}")
            print("请先下载KataGo: https://github.com/lightvector/KataGo/releases")
            return False
        except Exception as e:
            print(f"[KataGo] 连接错误: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.process:
            try:
                self._send_command(GTPCommand.QUIT)
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            finally:
                self.process = None
                self._connected = False
                print("[KataGo] 已断开连接")

    def _init_protocol(self):
        """初始化GTP协议"""
        # 设置棋盘大小
        self.set_board_size(self.config.board_size)
        # 设置贴目
        self.set_komi(self.config.komi)

    def _send_command(self, command: str, args: str = "") -> str:
        """发送GTP命令并获取响应"""
        with self._lock:
            self._request_id += 1
            cmd_line = f"{self._request_id} {command} {args}".strip()

            try:
                # 发送命令
                self.process.stdin.write(cmd_line + "\n")
                self.process.stdin.flush()

                # 读取响应
                response_lines = []
                while True:
                    line = self.process.stdout.readline()
                    if not line:
                        break

                    line = line.rstrip('\n\r')

                    # 跳过确认行
                    if line.startswith(f"{self._request_id}"):
                        continue

                    # 空行表示响应结束
                    if line == "":
                        break

                    response_lines.append(line)

                return "\n".join(response_lines)

            except Exception as e:
                print(f"[KataGo] 命令发送错误: {e}")
                return ""

    def _read_error(self) -> str:
        """读取错误输出"""
        try:
            if self.process and self.process.stderr:
                import select
                if hasattr(select, 'select'):
                    ready, _, _ = select.select([self.process.stderr], [], [], 1.0)
                    if ready:
                        return self.process.stderr.readline().strip()
            return ""
        except:
            return ""

    # ========================================================================
    # 基本GTP命令
    # ========================================================================

    def get_protocol_version(self) -> str:
        """获取协议版本"""
        return self._send_command(GTPCommand.PROTOCOL_VERSION)

    def get_name(self) -> str:
        """获取引擎名称"""
        return self._send_command(GTPCommand.NAME)

    def get_version(self) -> str:
        """获取引擎版本"""
        return self._send_command(GTPCommand.VERSION)

    def list_commands(self) -> List[str]:
        """列出所有支持的命令"""
        response = self._send_command(GTPCommand.LIST_COMMANDS)
        return [cmd.strip() for cmd in response.split('\n') if cmd.strip()]

    def known_command(self, command: str) -> bool:
        """检查是否支持某命令"""
        response = self._send_command(GTPCommand.KNOWN_COMMAND, command)
        return response.strip() == "true"

    def quit(self):
        """退出引擎"""
        self._send_command(GTPCommand.QUIT)
        self._connected = False

    # ========================================================================
    # 棋盘操作
    # ========================================================================

    def set_board_size(self, size: int):
        """设置棋盘大小"""
        self.config.board_size = size
        self._send_command(GTPCommand.BOARDSIZE, str(size))

    def clear_board(self):
        """清空棋盘"""
        self._send_command(GTPCommand.CLEAR_BOARD)

    def set_komi(self, komi: float):
        """设置贴目"""
        self.config.komi = komi
        self._send_command(GTPCommand.KOMI, str(komi))

    def play(self, color: str, move: str) -> bool:
        """执行落子
        color: 'black' 或 'white'
        move: GTP坐标如 'D4', 'PASS', 'resign'
        """
        response = self._send_command(GTPCommand.PLAY, f"{color} {move}")
        return response.strip() == "" or "ok" in response.lower()

    def generate_move(self, color: str, analysis: bool = False) -> Optional[str]:
        """生成落子
        color: 'black' 或 'white'
        analysis: 是否返回分析信息
        """
        if analysis:
            response = self._send_command(GTPCommand.GENMOVE_ANALYSIS, color)
            # 解析分析响应
            return self._parse_analysis_response(response)
        else:
            response = self._send_command(GTPCommand.GENMOVE, color)
            move = response.strip()
            return move if move and move not in ["resign", "pass"] else move

    def _parse_analysis_response(self, response: str) -> Optional[str]:
        """解析分析响应"""
        try:
            # 查找PV行（主变化）
            for line in response.split('\n'):
                if line.startswith("PV "):
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]  # 返回推荐走法
            # 如果没有PV，返回第一个坐标
            for line in response.split('\n'):
                line = line.strip()
                if line and len(line) >= 2 and line[0].isalpha():
                    return line
        except:
            pass
        return None

    def show_board(self) -> str:
        """获取棋盘显示"""
        return self._send_command(GTPCommand.SHOWBOARD)

    def get_final_score(self) -> str:
        """获取最终得分"""
        return self._send_command(GTPCommand.FINAL_SCORE)

    def get_final_status(self) -> str:
        """获取最终状态"""
        return self._send_command(GTPCommand.FINAL_STATUS)

    # ========================================================================
    # 时间控制
    # ========================================================================

    def set_time_settings(self, main_time: int, byoyomi_time: int, byoyomi_stones: int):
        """设置时间控制"""
        self._send_command(
            GTPCommand.TIME_SETTINGS,
            f"{main_time} {byoyomi_time} {byoyomi_stones}"
        )

    def set_time_left(self, color: str, time: int, stones: int):
        """设置剩余时间"""
        self._send_command(GTPCommand.TIME_LEFT, f"{color} {time} {stones}")


# ============================================================================
# 3. 内置围棋AI（无KataGo时使用的增强版）
# ============================================================================

class StrongGoAI:
    """增强版内置围棋AI - 基于六系立系论的强化系+自然系+社会系实现
    
    基于BSD六系立系论的对手AI增强：
    - 强化系🔵：算力计算·局面评估·深度搜索
    - 自然系🟠：演化趋势·棋形分析·领地预测
    - 社会系🟢：博弈关系·攻防态势·对手建模
    """

    def __init__(self, board_size: int = 19, strength: int = 3):
        self.board_size = board_size
        self.strength = strength  # 1-5, 越高越强
        
        # 六系权重（对手AI版本）
        self.liuhe_weights = {
            'qh': 0.35,  # 强化系：算力权重
            'zr': 0.30,  # 自然系：演化权重
            'sh': 0.20,  # 社会系：博弈权重
            'bs': 0.10,  # 变身系：创新权重
            'jx': 0.05,  # 具现系：落子权重
            'td': 0.00,  # 天道系：缺失（传统AI缺陷）
        }
        
        self._board = [[0] * board_size for _ in range(board_size)]
        self._current_player = 1  # 1=黑, 2=白
        self._move_count = 0
        self._max_candidates = min(board_size * board_size, 60)
        
        # 对手建模（社会系）
        self._opponent_model = {
            'last_moves': [],  # 对手最近落子
            'preferred_patterns': [],  # 对手偏好棋形
        }
        
        # 棋形评估缓存
        self._shape_cache = {}
        
        # 搜索时间限制
        self._search_time = min(0.5 + strength * 0.2, 2.0)  # 秒

    def set_board_size(self, size: int):
        self.board_size = size
        self._max_candidates = min(size * size, 50)
        self.clear_board()

    def clear_board(self):
        self._board = [[0] * self.board_size for _ in range(self.board_size)]
        self._current_player = 1
        self._move_count = 0

    def play(self, color: str, move: str) -> bool:
        """执行落子"""
        point = self._parse_move(move)
        if point is None:
            return move.lower() in ['pass', 'resign']

        x, y = point
        player = 1 if color == 'black' else 2

        if self._board[y][x] != 0:
            return False

        self._board[y][x] = player
        self._move_count += 1
        
        # 检查并移除被吃的棋子
        self._check_captures(x, y, player)
        
        self._current_player = 2 if player == 1 else 1
        return True

    def generate_move(self, color: str) -> Optional[str]:
        """生成落子 - 基于六系立系论的强化系+自然系+社会系决策
        
        六系协同决策：
        1. 强化系🔵：算力计算·局面评估·领地计算
        2. 自然系🟠：演化趋势·棋形分析·分形评估
        3. 社会系🟢：博弈关系·对手建模·攻防态势
        """
        player = 1 if color == 'black' else 2
        opponent = 3 - player

        # 更新对手模型（社会系）
        self._update_opponent_model(player)

        # 获取候选落子点（六系增强筛选）
        candidates = self._get_liuhe_candidates(player, opponent)

        if not candidates:
            return "PASS"

        # 根据强度选择搜索深度（强化系算力）
        # strength 1-2: 深度1, 3-4: 深度2, 5: 深度3
        search_depth = min((self.strength + 1) // 2, 3)
        
        # 六系评估每个候选点
        best_score = -float('inf')
        best_move = None

        # 评估前N个候选点
        top_n = min(len(candidates), 8 + self.strength * 2)
        
        for x, y in candidates[:top_n]:
            if not self._is_valid_move(x, y, player):
                continue
                
            # 模拟落子
            test_board = [row[:] for row in self._board]
            test_board[y][x] = player
            
            # 移除被吃棋子
            self._simulate_captures(test_board, x, y, player)
            
            # 六系融合评估
            qh_score = self._evaluate_qh(test_board, player, opponent)  # 强化系
            zr_score = self._evaluate_zr(test_board, player, opponent)  # 自然系
            sh_score = self._evaluate_sh(test_board, player, opponent, x, y)  # 社会系
            
            # 六系加权融合
            score = (
                self.liuhe_weights['qh'] * qh_score +
                self.liuhe_weights['zr'] * zr_score +
                self.liuhe_weights['sh'] * sh_score
            )
            
            # 深度搜索（强化系延伸）
            if search_depth > 0:
                search_score = self._alpha_beta_search(
                    test_board, player, opponent, search_depth, -float('inf'), float('inf')
                )
                score += search_score * 0.3
            
            if score > best_score:
                best_score = score
                best_move = (x, y)

        if best_move:
            # 记录对手落子用于建模
            self._opponent_model['last_moves'].append((best_move[0], best_move[1]))
            if len(self._opponent_model['last_moves']) > 20:
                self._opponent_model['last_moves'] = self._opponent_model['last_moves'][-20:]
            return self._to_gtp_coord(best_move[0], best_move[1])
        return "PASS"
    
    def _update_opponent_model(self, player: int):
        """更新对手模型（社会系）"""
        # 基于当前局面分析对手可能的偏好
        opponent = 3 - player
        
        # 统计对手棋形
        opponent_stones = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self._board[y][x] == opponent:
                    opponent_stones.append((x, y))
        
        # 分析对手偏好区域
        if opponent_stones:
            center_x = sum(s[0] for s in opponent_stones) / len(opponent_stones)
            center_y = sum(s[1] for s in opponent_stones) / len(opponent_stones)
            self._opponent_model['preferred_patterns'] = [center_x, center_y]
    
    def _evaluate_qh(self, board: List[List[int]], player: int, opponent: int) -> float:
        """强化系评估：算力计算·局面评估·领地计算"""
        score = 0.0
        
        # 1. 棋子数量（基础算力）
        player_stones = sum(row.count(player) for row in board)
        opponent_stones = sum(row.count(opponent) for row in board)
        score += (player_stones - opponent_stones) * 0.5
        
        # 2. 领地计算（强化系核心）
        territory = self._calculate_territory(board, player, opponent)
        score += territory * 1.0
        
        # 3. 棋形强度（算力评估）
        shape_score = self._evaluate_shapes(board, player) - self._evaluate_shapes(board, opponent)
        score += shape_score * 2.0
        
        # 4. 棋组安全性
        safety_score = self._evaluate_safety(board, player) - self._evaluate_safety(board, opponent)
        score += safety_score * 1.5
        
        return score
    
    def _evaluate_zr(self, board: List[List[int]], player: int, opponent: int) -> float:
        """自然系评估：演化趋势·棋形分析·分形评估"""
        score = 0.0
        
        # 1. 棋形演化潜力
        shape_potential = self._calculate_shape_potential(board, player)
        opponent_potential = self._calculate_shape_potential(board, opponent)
        score += (shape_potential - opponent_potential) * 1.5
        
        # 2. 中腹发展潜力
        center = self.board_size / 2
        player_center = 0
        opponent_center = 0
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                dist = abs(x - center) + abs(y - center)
                if board[y][x] == player and dist <= self.board_size / 2:
                    player_center += 1
                elif board[y][x] == opponent and dist <= self.board_size / 2:
                    opponent_center += 1
        
        score += (player_center - opponent_center) * 0.3
        
        # 3. 外势潜力
        player_outside = self._calculate_outside_influence(board, player)
        opponent_outside = self._calculate_outside_influence(board, opponent)
        score += (player_outside - opponent_outside) * 0.8
        
        return score
    
    def _evaluate_sh(self, board: List[List[int]], player: int, opponent: int, 
                     move_x: int, move_y: int) -> float:
        """社会系评估：博弈关系·对手建模·攻防态势"""
        score = 0.0
        
        # 1. 攻击潜力
        attack_score = self._calculate_attack_potential(board, player, opponent, move_x, move_y)
        score += attack_score * 1.2
        
        # 2. 防守稳固度
        defense_score = self._calculate_defense_stability(board, player)
        opponent_defense = self._calculate_defense_stability(board, opponent)
        score += (defense_score - opponent_defense) * 0.8
        
        # 3. 对手应手预测（社会系核心）
        opponent_response = self._predict_opponent_response(board, player, opponent, move_x, move_y)
        score -= opponent_response * 0.5
        
        return score
    
    def _get_liuhe_candidates(self, player: int, opponent: int) -> List[tuple]:
        """六系增强候选点筛选"""
        candidates = []
        center = self.board_size / 2
        
        # 1. 优先检查能吃子的点（强化系攻击）
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self._board[y][x] == 0:
                    if self._would_capture(x, y, player, opponent):
                        candidates.append((x, y))
        
        # 2. 检查攻击对手薄弱棋组的点（社会系博弈）
        if len(candidates) < self._max_candidates:
            weak_points = self._find_weak_group_points(player, opponent)
            candidates.extend(weak_points)
        
        # 3. 检查构建棋形的点（自然系演化）
        if len(candidates) < self._max_candidates:
            shape_points = self._find_shape_building_points(player)
            candidates.extend(shape_points)
        
        # 4. 检查相邻己方棋子的点（强化系延伸）
        if len(candidates) < self._max_candidates:
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self._board[y][x] == 0:
                        if self._has_friendly_neighbor(x, y, player):
                            candidates.append((x, y))
        
        # 5. 检查邻近对方棋子的点（社会系攻防）
        if len(candidates) < self._max_candidates:
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self._board[y][x] == 0:
                        if self._has_enemy_neighbor(x, y, opponent):
                            candidates.append((x, y))
        
        # 6. 补充中心点（自然系布局）
        if len(candidates) < self._max_candidates:
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self._board[y][x] == 0:
                        dist = abs(x - center) + abs(y - center)
                        if dist < self.board_size * 0.75:
                            candidates.append((x, y))
        
        # 去重、验证合法性并限制数量
        seen = set()
        unique = []
        for x, y in candidates:
            if (x, y) not in seen and self._is_valid_move(x, y, player):
                seen.add((x, y))
                unique.append((x, y))
                if len(unique) >= self._max_candidates:
                    break
        
        return unique
    
    def _find_weak_group_points(self, player: int, opponent: int) -> List[tuple]:
        """寻找攻击对手薄弱棋组的点"""
        points = []
        visited = set()
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self._board[y][x] == opponent and (x, y) not in visited:
                    group = self._get_group(x, y, opponent)
                    group_libs = self._count_group_liberties(group, opponent)
                    
                    # 气数少的棋组是攻击目标
                    if len(group_libs) <= 3:
                        # 攻击点：棋组周围
                        for gx, gy in group:
                            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                ax, ay = gx + dx, gy + dy
                                if 0 <= ax < self.board_size and 0 <= ay < self.board_size:
                                    if self._board[ay][ax] == 0:
                                        points.append((ax, ay))
                    
                    for p in group:
                        visited.add(p)
        
        return points[:20]  # 限制数量
    
    def _find_shape_building_points(self, player: int) -> List[tuple]:
        """寻找构建棋形的点"""
        points = []
        
        # 寻找可以形成二线、三线的点
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self._board[y][x] == 0:
                    # 检查周围是否有己方棋子
                    friendly_count = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                                   (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            if self._board[ny][nx] == player:
                                friendly_count += 1
                    
                    # 有2-3个邻近己方棋子是构建棋形的好点
                    if 2 <= friendly_count <= 3:
                        points.append((x, y))
        
        return points[:15]
    
    def _calculate_territory(self, board: List[List[int]], player: int, opponent: int) -> float:
        """领地计算"""
        territory = 0.0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == 0:
                    player_neighbors = 0
                    opponent_neighbors = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            if board[ny][nx] == player:
                                player_neighbors += 1
                            elif board[ny][nx] == opponent:
                                opponent_neighbors += 1
                    
                    if player_neighbors > opponent_neighbors:
                        territory += 1.0
                    elif opponent_neighbors > player_neighbors:
                        territory -= 1.0
        return territory
    
    def _evaluate_shapes(self, board: List[List[int]], player: int) -> float:
        """棋形评估"""
        score = 0.0
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player:
                    # 检查横向棋形
                    count_h = self._count_line_improved(board, x, y, 1, 0, player)
                    # 检查纵向棋形
                    count_v = self._count_line_improved(board, x, y, 0, 1, player)
                    # 检查斜线棋形
                    count_d1 = self._count_line_improved(board, x, y, 1, 1, player)
                    count_d2 = self._count_line_improved(board, x, y, 1, -1, player)
                    
                    max_line = max(count_h, count_v, count_d1, count_d2)
                    
                    # 棋形价值函数
                    if max_line >= 5:
                        score += 5.0  # 成五
                    elif max_line == 4:
                        score += 2.0  # 活四
                    elif max_line == 3:
                        score += 1.0  # 活三
                    elif max_line == 2:
                        score += 0.3  # 活二
        
        return score
    
    def _count_line_improved(self, board: List[List[int]], x: int, y: int, 
                             dx: int, dy: int, player: int) -> int:
        """改进的线上同色棋子计数"""
        count = 1
        
        # 正向
        cx, cy = x + dx, y + dy
        while 0 <= cx < self.board_size and 0 <= cy < self.board_size:
            if board[cy][cx] == player:
                count += 1
                cx += dx
                cy += dy
            else:
                break
        
        # 反向
        cx, cy = x - dx, y - dy
        while 0 <= cx < self.board_size and 0 <= cy < self.board_size:
            if board[cy][cx] == player:
                count += 1
                cx -= dx
                cy -= dy
            else:
                break
        
        return count
    
    def _evaluate_safety(self, board: List[List[int]], player: int) -> float:
        """棋组安全性评估"""
        score = 0.0
        visited = set()
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player and (x, y) not in visited:
                    group = self._get_group(x, y, player)
                    liberties = self._count_group_liberties(group, player)
                    
                    for p in group:
                        visited.add(p)
                    
                    # 气数评估
                    lib_count = len(liberties)
                    group_size = len(group)
                    
                    if lib_count == 1:
                        score -= group_size * 3.0  # 只有1气，非常危险
                    elif lib_count == 2:
                        score -= group_size * 0.5  # 2气，较危险
                    elif lib_count == 3:
                        score += group_size * 0.2  # 3气，基本安全
                    elif lib_count >= 4:
                        score += group_size * 0.5  # 4+气，很安全
        
        return score
    
    def _calculate_shape_potential(self, board: List[List[int]], player: int) -> float:
        """棋形演化潜力"""
        potential = 0.0
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == 0:
                    # 检查空位周围的己方棋子
                    friendly = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                                   (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            if board[ny][nx] == player:
                                friendly += 1
                    
                    # 有2+己方棋子邻近的空位有演化潜力
                    if friendly >= 2:
                        potential += friendly * 0.5
        
        return potential
    
    def _calculate_outside_influence(self, board: List[List[int]], player: int) -> float:
        """外势计算"""
        influence = 0.0
        center = self.board_size / 2
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player:
                    # 距离棋盘中心越远，外势价值越高
                    dist_to_center = abs(x - center) + abs(y - center)
                    influence += dist_to_center * 0.1
        
        return influence
    
    def _calculate_attack_potential(self, board: List[List[int]], player: int, 
                                    opponent: int, move_x: int, move_y: int) -> float:
        """攻击潜力计算"""
        potential = 0.0
        
        # 检查落子后是否能攻击对手棋组
        test_board = [row[:] for row in board]
        test_board[move_y][move_x] = player
        self._simulate_captures(test_board, move_x, move_y, player)
        
        # 统计对手被削弱的棋组数
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                if test_board[y][x] == opponent and (x, y) not in visited:
                    group = self._get_group_on_board(test_board, x, y, opponent)
                    liberties = self._count_group_liberties_on_board(test_board, group, opponent)
                    
                    for p in group:
                        visited.add(p)
                    
                    if len(liberties) <= 2:
                        potential += len(group) * 2.0  # 被攻击的棋组
        
        return potential
    
    def _calculate_defense_stability(self, board: List[List[int]], player: int) -> float:
        """防守稳固度计算"""
        stability = 0.0
        visited = set()
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player and (x, y) not in visited:
                    group = self._get_group(x, y, player)
                    liberties = self._count_group_liberties(group, player)
                    
                    for p in group:
                        visited.add(p)
                    
                    # 棋组越大越稳固
                    stability += len(group) * len(liberties) * 0.3
        
        return stability
    
    def _predict_opponent_response(self, board: List[List[int]], player: int, 
                                    opponent: int, move_x: int, move_y: int) -> float:
        """预测对手应手"""
        # 简化版：检查对手可能的最佳应手位置
        response_score = 0.0
        
        test_board = [row[:] for row in board]
        test_board[move_y][move_x] = player
        
        # 预测对手的主要应手点
        response_points = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                       (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nx, ny = move_x + dx, move_y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if test_board[ny][nx] == 0:
                    response_points.append((nx, ny))
        
        # 评估对手应手后的局势
        for rx, ry in response_points[:3]:
            opponent_board = [row[:] for row in test_board]
            opponent_board[ry][rx] = opponent
            
            # 对手应手后，己方得分
            opp_libs = self._count_all_liberties(opponent_board, opponent)
            my_libs = self._count_all_liberties(opponent_board, player)
            
            if my_libs > opp_libs:
                response_score -= 0.5  # 对手应手后我方仍占优
            else:
                response_score += 1.0  # 对手应手后我方不利
        
        return response_score
    
    def _count_all_liberties(self, board: List[List[int]], player: int) -> int:
        """计算所有棋组的总气数"""
        total_libs = 0
        visited = set()
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player and (x, y) not in visited:
                    group = self._get_group_on_board(board, x, y, player)
                    liberties = self._count_group_liberties_on_board(board, group, player)
                    
                    for p in group:
                        visited.add(p)
                    
                    total_libs += len(liberties)
        
        return total_libs
    
    def _get_group(self, x: int, y: int, player: int) -> List[tuple]:
        """获取棋组"""
        return self._get_group_on_board(self._board, x, y, player)
    
    def _get_group_on_board(self, board: List[List[int]], x: int, y: int, 
                             player: int) -> List[tuple]:
        """从指定棋盘获取棋组"""
        group = []
        visited = set()
        queue = [(x, y)]
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[ny][nx] == player and (nx, ny) not in visited:
                        queue.append((nx, ny))
        
        return group
    
    def _count_group_liberties(self, group: List[tuple], player: int) -> set:
        """计算棋组气数"""
        return self._count_group_liberties_on_board(self._board, group, player)
    
    def _count_group_liberties_on_board(self, board: List[List[int]], group: List[tuple], 
                                          player: int) -> set:
        """从指定棋盘计算棋组气数"""
        liberties = set()
        
        for gx, gy in group:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = gx + dx, gy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[ny][nx] == 0:
                        liberties.add((nx, ny))
        
        return liberties
    
    def _alpha_beta_search(self, board: List[List[int]], current_player: int,
                            opponent: int, depth: int, alpha: float, 
                            beta: float) -> float:
        """Alpha-Beta剪枝搜索"""
        if depth <= 0:
            return self._quick_evaluate(board, current_player, opponent)
        
        # 优化：限制搜索分支数
        candidates = self._get_search_candidates(board, current_player)
        
        if not candidates:
            return self._quick_evaluate(board, current_player, opponent)
        
        # 对候选点排序（简单启发式）
        scored_candidates = []
        for x, y in candidates[:10]:
            test_board = [row[:] for row in board]
            test_board[y][x] = current_player
            self._simulate_captures(test_board, x, y, current_player)
            score = self._quick_evaluate(test_board, current_player, opponent)
            scored_candidates.append((score, x, y))
        
        scored_candidates.sort(reverse=True)
        
        if current_player == 1:  # 最大化节点
            max_eval = -float('inf')
            for _, x, y in scored_candidates[:5]:
                test_board = [row[:] for row in board]
                test_board[y][x] = current_player
                self._simulate_captures(test_board, x, y, current_player)
                
                eval_score = self._alpha_beta_search(
                    test_board, 2, 1, depth - 1, alpha, beta
                )
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break
            
            return max_eval
        else:  # 最小化节点
            min_eval = float('inf')
            for _, x, y in scored_candidates[:5]:
                test_board = [row[:] for row in board]
                test_board[y][x] = current_player
                self._simulate_captures(test_board, x, y, current_player)
                
                eval_score = self._alpha_beta_search(
                    test_board, 1, 2, depth - 1, alpha, beta
                )
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break
            
            return min_eval
    
    def _get_search_candidates(self, board: List[List[int]], player: int) -> List[tuple]:
        """获取搜索候选点"""
        candidates = []
        opponent = 3 - player
        
        # 只考虑对手和己方附近的点
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == 0:
                    is_candidate = False
                    
                    # 邻近己方棋子
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            if board[ny][nx] == player:
                                is_candidate = True
                                break
                    
                    # 邻近对手棋子
                    if not is_candidate:
                        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                                if board[ny][nx] == opponent:
                                    is_candidate = True
                                    break
                    
                    if is_candidate and self._simulate_is_valid(board, x, y, player):
                        candidates.append((x, y))
        
        return candidates[:15]

    def _would_capture(self, x: int, y: int, player: int, opponent: int) -> bool:
        """检查落子后是否能吃子"""
        test_board = [row[:] for row in self._board]
        test_board[y][x] = player
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if test_board[ny][nx] == opponent:
                    if not self._group_has_liberty(test_board, nx, ny, opponent):
                        return True
        return False

    def _has_friendly_neighbor(self, x: int, y: int, player: int) -> bool:
        """检查是否有邻近己方棋子"""
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self._board[ny][nx] == player:
                    return True
        return False

    def _has_enemy_neighbor(self, x: int, y: int, opponent: int) -> bool:
        """检查是否有邻近对方棋子"""
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self._board[ny][nx] == opponent:
                    return True
        return False

    def _quick_evaluate(self, board: List[List[int]], player: int, opponent: int) -> float:
        """快速评估局面"""
        score = 0.0
        
        # 1. 棋子数
        player_stones = sum(row.count(player) for row in board)
        opponent_stones = sum(row.count(opponent) for row in board)
        score += (player_stones - opponent_stones) * 0.3
        
        # 2. 简单领地估算
        territory = self._quick_territory_estimate(board, player, opponent)
        score += territory * 0.5
        
        # 3. 棋型价值
        shape_score = self._quick_shape_score(board, player) - self._quick_shape_score(board, opponent)
        score += shape_score * 1.0
        
        # 4. 安全性
        safety = self._quick_safety_score(board, player) - self._quick_safety_score(board, opponent)
        score += safety * 1.5
        
        return score

    def _quick_territory_estimate(self, board: List[List[int]], player: int, opponent: int) -> float:
        """快速领地估算"""
        territory = 0.0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == 0:
                    # 简单检查：邻近谁的棋子多
                    player_neighbors = 0
                    opponent_neighbors = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            if board[ny][nx] == player:
                                player_neighbors += 1
                            elif board[ny][nx] == opponent:
                                opponent_neighbors += 1
                    
                    if player_neighbors > opponent_neighbors:
                        territory += 1.0
                    elif opponent_neighbors > player_neighbors:
                        territory -= 1.0
        return territory

    def _quick_shape_score(self, board: List[List[int]], player: int) -> float:
        """快速棋型评估"""
        score = 0.0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player:
                    # 检查横向
                    count_h = self._count_line(board, x, y, 1, 0, player)
                    # 检查纵向
                    count_v = self._count_line(board, x, y, 0, 1, player)
                    score += max(count_h, count_v) * 0.5
        return score

    def _count_line(self, board: List[List[int]], x: int, y: int, 
                    dx: int, dy: int, player: int) -> int:
        """计算线上同色棋子数"""
        count = 1
        # 正向
        cx, cy = x + dx, y + dy
        while 0 <= cx < self.board_size and 0 <= cy < self.board_size:
            if board[cy][cx] == player:
                count += 1
                cx += dx
                cy += dy
            else:
                break
        # 反向
        cx, cy = x - dx, y - dy
        while 0 <= cx < self.board_size and 0 <= cy < self.board_size:
            if board[cy][cx] == player:
                count += 1
                cx -= dx
                cy -= dy
            else:
                break
        return count

    def _quick_safety_score(self, board: List[List[int]], player: int) -> float:
        """快速安全性评估"""
        score = 0.0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == player:
                    liberties = self._count_local_liberties(board, x, y, player)
                    if liberties == 1:
                        score -= 3.0
                    elif liberties == 2:
                        score -= 0.5
                    elif liberties >= 3:
                        score += 0.5
        return score

    def _count_local_liberties(self, board: List[List[int]], x: int, y: int, player: int) -> int:
        """计算局部气数（简化版）"""
        liberties = set()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if board[ny][nx] == 0:
                    liberties.add((nx, ny))
                elif board[ny][nx] == player:
                    # 检查相邻同色棋子的气
                    for dx2, dy2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nnx, nny = nx + dx2, ny + dy2
                        if 0 <= nnx < self.board_size and 0 <= nny < self.board_size:
                            if board[nny][nnx] == 0:
                                liberties.add((nnx, nny))
        return len(liberties)

    def _minimax_search(self, board: List[List[int]], current_player: int, 
                        opponent: int, depth: int) -> float:
        """Minimax搜索"""
        if depth <= 0:
            return 0.0
        
        # 获取有限的候选点
        candidates = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == 0:
                    if self._simulate_is_valid(board, x, y, current_player):
                        candidates.append((x, y))
                        if len(candidates) >= 8:
                            break
            if len(candidates) >= 8:
                break
        
        if not candidates:
            return 0.0
        
        best_score = -float('inf')
        
        for x, y in candidates[:5]:
            test_board = [row[:] for row in board]
            test_board[y][x] = current_player
            self._simulate_captures(test_board, x, y, current_player)
            
            # 评估对手的最佳回应
            opponent_score = self._evaluate_opponent_response(test_board, opponent, current_player)
            
            score = self._quick_evaluate(test_board, current_player, opponent)
            score -= opponent_score * 0.5
            
            if depth > 1:
                score += self._minimax_search(test_board, opponent, current_player, depth - 1) * 0.3
            
            best_score = max(best_score, score)
        
        return best_score

    def _evaluate_opponent_response(self, board: List[List[int]], opponent: int, 
                                    current_player: int) -> float:
        """评估对手的最佳回应"""
        best_score = -float('inf')
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x] == 0:
                    if self._simulate_is_valid(board, x, y, opponent):
                        test_board = [row[:] for row in board]
                        test_board[y][x] = opponent
                        score = self._quick_evaluate(test_board, opponent, current_player)
                        best_score = max(best_score, score)
                        if best_score > 0:
                            break
            if best_score > 0:
                break
        
        return best_score

    def _get_legal_moves(self, player: int) -> List[tuple]:
        """获取所有合法落子点（保留用于兼容）"""
        return self._get_smart_candidates(player, 3 - player)

    def _count_potential_captures(self, board: List[List[int]], x: int, y: int, 
                                    player: int) -> int:
        """计算潜在吃子数"""
        captured = 0
        opponent = 3 - player
        
        # 检查周围对手棋子是否会被吃
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if board[ny][nx] == opponent:
                    # 检查该组是否只有1气
                    if self._group_has_one_liberty(board, nx, ny, opponent):
                        captured += self._group_size(board, nx, ny, opponent)
        
        return captured

    def _group_has_one_liberty(self, board: List[List[int]], x: int, y: int, player: int) -> bool:
        """检查一组棋子是否只有一口气"""
        liberties = set()
        visited = set()
        queue = [(x, y)]
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[ny][nx] == 0:
                        liberties.add((nx, ny))
                    elif board[ny][nx] == player and (nx, ny) not in visited:
                        queue.append((nx, ny))
        
        return len(liberties) == 1

    def _group_size(self, board: List[List[int]], x: int, y: int, player: int) -> int:
        """获取一组棋子的大小"""
        visited = set()
        queue = [(x, y)]
        size = 0
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            size += 1
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[ny][nx] == player and (nx, ny) not in visited:
                        queue.append((nx, ny))
        
        return size

    def _check_captures(self, x: int, y: int, player: int):
        """检查并移除被吃的棋子"""
        opponent = 3 - player
        captured = 0
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self._board[ny][nx] == opponent:
                    # 检查该组是否没有气
                    if not self._group_has_liberty(self._board, nx, ny, opponent):
                        # 移除该组
                        captured += self._remove_group(nx, ny, opponent)
        
        return captured

    def _simulate_captures(self, board: List[List[int]], x: int, y: int, player: int):
        """模拟吃子"""
        opponent = 3 - player
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if board[ny][nx] == opponent:
                    if not self._group_has_liberty(board, nx, ny, opponent):
                        self._remove_group_from_board(board, nx, ny, opponent)

    def _group_has_liberty(self, board: List[List[int]], x: int, y: int, player: int) -> bool:
        """检查一组棋子是否有气"""
        liberties = set()
        visited = set()
        queue = [(x, y)]
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[ny][nx] == 0:
                        liberties.add((nx, ny))
                    elif board[ny][nx] == player and (nx, ny) not in visited:
                        queue.append((nx, ny))
        
        return len(liberties) > 0

    def _remove_group(self, x: int, y: int, player: int) -> int:
        """移除一组棋子"""
        count = 0
        visited = set()
        queue = [(x, y)]
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            
            self._board[cy][cx] = 0
            count += 1
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self._board[ny][nx] == player and (nx, ny) not in visited:
                        queue.append((nx, ny))
        
        return count

    def _remove_group_from_board(self, board: List[List[int]], x: int, y: int, player: int):
        """从棋盘上移除一组棋子"""
        visited = set()
        queue = [(x, y)]
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            
            board[cy][cx] = 0
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[ny][nx] == player and (nx, ny) not in visited:
                        queue.append((nx, ny))

    def _is_valid_move(self, x: int, y: int, player: int) -> bool:
        """检查落子是否合法"""
        if self._board[y][x] != 0:
            return False
        
        # 模拟落子
        test_board = [row[:] for row in self._board]
        test_board[y][x] = player
        
        # 检查是否能吃到对方棋子（如果有，就是合法的）
        opponent = 3 - player
        can_capture = False
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if test_board[ny][nx] == opponent:
                    if not self._group_has_liberty(test_board, nx, ny, opponent):
                        can_capture = True
                        break
        
        if can_capture:
            return True
        
        # 检查落子后自己是否有气
        return self._group_has_liberty(test_board, x, y, player)

    def _simulate_is_valid(self, board: List[List[int]], x: int, y: int, player: int) -> bool:
        """在模拟棋盘上检查落子是否合法"""
        if board[y][x] != 0:
            return False
        
        test_board = [row[:] for row in board]
        test_board[y][x] = player
        
        opponent = 3 - player
        can_capture = False
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if test_board[ny][nx] == opponent:
                    if not self._group_has_liberty(test_board, nx, ny, opponent):
                        can_capture = True
                        break
        
        if can_capture:
            return True
        
        return self._group_has_liberty(test_board, x, y, player)

    def _parse_move(self, move: str) -> Optional[tuple]:
        """解析GTP坐标"""
        if move.upper() in ['PASS', 'RESIGN']:
            return None

        letters = 'ABCDEFGHJKLMNOPQRST'
        if len(move) < 2:
            return None

        col_char = move[0].upper()
        row_str = move[1:]

        if col_char not in letters:
            return None

        x = letters.index(col_char)
        try:
            y = int(row_str) - 1
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                return (x, y)
        except:
            pass

        return None

    def _to_gtp_coord(self, x: int, y: int) -> str:
        """转换为GTP坐标"""
        letters = 'ABCDEFGHJKLMNOPQRST'
        return f"{letters[x]}{y + 1}"


# 保留SimpleGoAI作为兼容别名
SimpleGoAI = StrongGoAI


# ============================================================================
# 4. 统一围棋AI接口
# ============================================================================

class GoAIInterface:
    """统一围棋AI接口 - 支持KataGo和内置AI"""

    def __init__(self, use_katago: bool = False, **kwargs):
        self.use_katago = use_katago
        self.katago_client: Optional[KataGoGTPClient] = None
        self.simple_ai: Optional[StrongGoAI] = None
        self.board_size = kwargs.get('board_size', 19)
        self.strength = kwargs.get('strength', 3)

        if use_katago:
            config = GTPEngineConfig(
                executable_path=kwargs.get('katago_path', 'katago'),
                model_path=kwargs.get('model_path', ''),
                config_path=kwargs.get('config_path', ''),
                board_size=self.board_size,
                komi=kwargs.get('komi', 7.5)
            )
            self.katago_client = KataGoGTPClient(config)
            self._connected = self.katago_client.connect()

            if not self._connected:
                print("[GoAI] KataGo连接失败，使用内置AI")
                self.use_katago = False
                self.simple_ai = StrongGoAI(self.board_size, self.strength)
        else:
            self.simple_ai = StrongGoAI(self.board_size, self.strength)

    @property
    def is_connected(self) -> bool:
        return self._connected if hasattr(self, '_connected') else False

    def set_board_size(self, size: int):
        self.board_size = size
        if self.use_katago and self.katago_client:
            self.katago_client.set_board_size(size)
        elif self.simple_ai:
            self.simple_ai.set_board_size(size)

    def clear_board(self):
        if self.use_katago and self.katago_client:
            self.katago_client.clear_board()
        elif self.simple_ai:
            self.simple_ai.clear_board()

    def play(self, color: str, move: str) -> bool:
        if self.use_katago and self.katago_client:
            return self.katago_client.play(color, move)
        elif self.simple_ai:
            return self.simple_ai.play(color, move)
        return False

    def generate_move(self, color: str) -> Optional[str]:
        if self.use_katago and self.katago_client:
            return self.katago_client.generate_move(color)
        elif self.simple_ai:
            return self.simple_ai.generate_move(color)
        return None

    def get_engine_info(self) -> Dict:
        if self.use_katago and self.katago_client:
            return {
                'type': 'KataGo',
                'name': self.katago_client.get_name(),
                'version': self.katago_client.get_version(),
                'connected': self.is_connected
            }
        elif self.simple_ai:
            return {
                'type': 'SimpleGoAI',
                'name': 'Built-in Go AI',
                'version': '1.0',
                'connected': True
            }
        return {'type': 'Unknown', 'connected': False}

    def cleanup(self):
        if self.use_katago and self.katago_client:
            self.katago_client.disconnect()


# ============================================================================
# 5. 演示
# ============================================================================

def demo_katago_client():
    """演示KataGo客户端"""
    print("=" * 60)
    print("KataGo GTP客户端 - 演示")
    print("=" * 60)

    # 尝试连接KataGo（如果已安装）
    print("\n[尝试连接KataGo...]")
    ai = GoAIInterface(use_katago=True)

    engine_info = ai.get_engine_info()
    print(f"引擎类型：{engine_info['type']}")
    print(f"引擎名称：{engine_info.get('name', 'N/A')}")

    if engine_info['type'] == 'SimpleGoAI':
        print("\n提示：KataGo未安装，使用内置简单围棋AI")
        print("安装KataGo: https://github.com/lightvector/KataGo/releases")

    # 演示对弈
    print("\n[演示对弈...]")
    ai.set_board_size(9)
    ai.clear_board()

    color = 'black'
    for i in range(20):
        move = ai.generate_move(color)
        if move and move not in ['PASS', 'resign']:
            ai.play(color, move)
            print(f"  {color[:1].upper()}: {move}")
        else:
            print(f"  {color[:1].upper()}: pass/resign")

        color = 'white' if color == 'black' else 'black'

    ai.cleanup()
    print("\n" + "=" * 60)
    print("演示完成")


if __name__ == "__main__":
    demo_katago_client()
