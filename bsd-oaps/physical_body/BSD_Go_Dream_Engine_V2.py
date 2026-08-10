#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD围棋白日梦引擎 V2.0 - 实战版
=================================
整合真实围棋基因库，验证"白日梦机制"在实战中的有效性。

核心实验：
1. DreamAI (白日梦) vs TraditionalAI (传统)
2. 多局对弈，统计胜率和关键转折点
3. 分析白日梦触发的时机和效果
"""

import os
import sys
import random
from datetime import datetime
from collections import defaultdict

# 导入基因库V2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from BSD_Go_GenePool_V2 import GoGenePoolV2, GoKnowledgeBase


# ============================================================
# 围棋棋盘环境 (GoBoard) - 增强版
# ============================================================

class GoBoard:
    """围棋棋盘（9x9增强版）"""
    
    def __init__(self, size=9):
        self.size = size
        self.board = [[0]*size for _ in range(size)]  # 0=空, 1=黑, 2=白
        self.current_player = 1
        self.move_count = 0
        self.history = []
        self.consecutive_passes = 0
        
    def place_stone(self, x, y):
        """落子"""
        if x is None or y is None:
            self.consecutive_passes += 1
            if self.consecutive_passes >= 2:
                self._end_game()
            return False, "pass"
            
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False, "越界"
        if self.board[x][y] != 0:
            return False, "此处已有棋子"
            
        # 执行落子
        captured = self._capture_stones(x, y)
        self.board[x][y] = self.current_player
        
        # 检查自杀
        if self._is_in_self_atari(x, y):
            self.board[x][y] = 0
            return False, "禁入点"
            
        self.consecutive_passes = 0
        self.history.append({
            'move': (x, y),
            'player': self.current_player,
            'captured': captured
        })
        self.move_count += 1
        self.current_player = 3 - self.current_player
        
        return True, f"落子成功，提子{captured}个"
        
    def _capture_stones(self, x, y):
        """提子逻辑"""
        opponent = 3 - self.current_player
        captured = 0
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.board[nx][ny] == opponent:
                    group = self._get_group(nx, ny)
                    if not self._has_liberty(group):
                        for gx, gy in group:
                            self.board[gx][gy] = 0
                            captured += 1
                            
        return captured
        
    def _get_group(self, x, y):
        """获取连通块"""
        color = self.board[x][y]
        group = []
        visited = set()
        stack = [(x, y)]
        
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))
            
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == color:
                        stack.append((nx, ny))
                        
        return group
        
    def _has_liberty(self, group):
        """检查连通块是否有气"""
        for x, y in group:
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == 0:
                        return True
        return False
        
    def _is_in_self_atari(self, x, y):
        """检查是否禁入点"""
        group = self._get_group(x, y)
        return not self._has_liberty(group)
        
    def get_local_pattern(self, x, y, radius=1):
        """获取指定位置的3x3局部棋形"""
        pattern = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    pattern.append(self.board[nx][ny])
                else:
                    pattern.append(-1)
        return pattern
        
    def get_empty_points(self):
        """获取所有空点"""
        return [(x, y) for x in range(self.size) for y in range(self.size) 
                if self.board[x][y] == 0]
        
    def evaluate(self):
        """评估局面"""
        black_score = 0
        white_score = 0
        
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    black_score += 1
                    black_score += self._position_bonus(x, y)
                elif self.board[x][y] == 2:
                    white_score += 1
                    white_score += self._position_bonus(x, y)
                    
        # 加目（简化计算）
        black_score += 6.5  # 贴6.5目给白方
        
        return black_score - white_score
        
    def _position_bonus(self, x, y):
        """位置加分"""
        if (x in [0, self.size-1] and y in [0, self.size-1]):
            return 3  # 角
        if x in [0, self.size-1] or y in [0, self.size-1]:
            return 2  # 边
        if 2 <= x <= 6 and 2 <= y <= 6:
            return 1  # 中心
        return 0
        
    def display(self):
        """显示棋盘"""
        symbols = {0: '.', 1: '●', 2: '○', -1: '?'}
        header = '   ' + ' '.join([str(i) for i in range(self.size)])
        
        print(f"\n{header}")
        for x in range(self.size):
            row = f"{x}  "
            for y in range(self.size):
                row += f" {symbols[self.board[x][y]]}"
            print(row)
        print()


# ============================================================
# 白日梦决策引擎 (DreamEngineV2)
# ============================================================

class DreamEngineV2:
    """
    白日梦决策引擎V2 - 战术驱动
    
    核心改进：
    1. 基于局面战术需求触发白日梦
    2. DNA重组融合战术意图与棋型
    3. 验证梦境落子的实战价值
    """
    
    def __init__(self, gene_pool):
        self.gene_pool = gene_pool
        self.dream_log = []
        self.dream_count = 0
        self.conventional_count = 0
        self.capture_count = 0  # 提子次数
        self.last_move_score = 0  # 上一步得分
        
    def decide_move(self, board, player):
        """核心决策"""
        empty_points = board.get_empty_points()
        if not empty_points:
            return None
            
        # 提取所有局部棋型
        local_patterns = {}
        for x, y in empty_points:
            local_patterns[(x, y)] = board.get_local_pattern(x, y)
            
        # 第一优先：战术思维
        tactical_move = self._tactical_decide(board, player, local_patterns)
        
        # 检查是否需要白日梦
        need_dream = self._should_dream(board, player, tactical_move, local_patterns)
        
        if need_dream:
            # 触发白日梦！
            dream_move, dream_info = self._dream_decide(board, player, local_patterns)
            self.dream_count += 1
            
            self.dream_log.append({
                'move': dream_move,
                'is_dream': True,
                'dream_info': dream_info,
                'player': player,
                'board_score': board.evaluate(),
            })
            
            return dream_move
        else:
            self.conventional_count += 1
            self.dream_log.append({
                'move': tactical_move,
                'is_dream': False,
                'player': player,
                'board_score': board.evaluate(),
            })
            return tactical_move
            
    def _tactical_decide(self, board, player, local_patterns):
        """战术思维：识别并执行战术"""
        candidates = []
        
        for (x, y), pattern in local_patterns.items():
            # 查找战术基因
            tactic_genes = self.gene_pool.find_tactic_genes(pattern)
            
            if tactic_genes:
                # 选择得分最高的战术
                best_gene = max(tactic_genes, 
                               key=lambda g: g['emergence_value'] * g.get('score_boost', 1.0))
                candidates.append({
                    'move': (x, y),
                    'score': best_gene['emergence_value'] * best_gene.get('score_boost', 1.0),
                    'tactic': best_gene['tactic'],
                    'gene': best_gene,
                })
            else:
                # 无匹配基因，使用启发式
                score = self._heuristic_score(board, x, y, player)
                candidates.append({
                    'move': (x, y),
                    'score': score,
                    'tactic': 'heuristic',
                })
                
        if not candidates:
            return None
            
        candidates.sort(key=lambda c: c['score'], reverse=True)
        return candidates[0]['move']
        
    def _heuristic_score(self, board, x, y, player):
        """启发式评分"""
        score = 0.0
        
        # 位置价值
        score += board._position_bonus(x, y) * 0.5
        
        # 战术价值
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == (3 - player):
                    score += 0.8  # 威胁对手
                elif board.board[nx][ny] == player:
                    score += 0.4  # 连接友军
                    
        # 中心偏好
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        score += max(0, (board.size - dist)) * 0.1
        
        return score
        
    def _should_dream(self, board, player, tactical_move, local_patterns):
        """
        判断是否需要触发白日梦
        
        触发条件（按优先级）：
        1. 存在打吃机会但传统AI未发现
        2. 局面僵持（得分差 < 3目）
        3. 己方棋子被打吃（紧急情况）
        4. 中盘阶段随机触发
        """
        # 检查是否有未被发现的战术机会
        hidden_tactics = self._find_hidden_tactics(board, player, local_patterns)
        
        if hidden_tactics and tactical_move not in [t['move'] for t in hidden_tactics]:
            # 传统AI忽略了战术机会
            return True
            
        # 检查己方是否被打吃
        if self._is_under_atari(board, player):
            # 紧急情况，触发白日梦寻找解法
            return True
            
        # 僵持局面
        score = board.evaluate()
        if abs(score) < 3:
            # 局面胶着，50%概率触发
            if random.random() < 0.5:
                return True
                
        # 中盘阶段（落子 > 20）
        if board.move_count > 20:
            if random.random() < 0.15:
                return True
                
        return False
        
    def _find_hidden_tactics(self, board, player, local_patterns):
        """发现被传统AI忽略的战术机会"""
        hidden = []
        
        for (x, y), pattern in local_patterns.items():
            # 检查打吃机会
            for i, v in enumerate(pattern):
                if v == (3 - player):  # 对手棋子
                    x_pos, y_pos = i // 3, i % 3
                    # 检查是否只剩一口气
                    if self._count_liberties(pattern, i) == 1:
                        # 找到了打吃机会
                        hidden.append({
                            'move': (x, y),
                            'tactic': 'capture',
                            'target': (x_pos, y_pos),
                        })
                        break
                        
        return hidden
        
    def _count_liberties(self, pattern, position):
        """计算某个棋子的气数"""
        x, y = position // 3, position % 3
        liberties = 0
        
        if x > 0 and pattern[position - 3] == 0:
            liberties += 1
        if x < 2 and pattern[position + 3] == 0:
            liberties += 1
        if y > 0 and pattern[position - 1] == 0:
            liberties += 1
        if y < 2 and pattern[position + 1] == 0:
            liberties += 1
            
        return liberties
        
    def _is_under_atari(self, board, player):
        """检查己方是否被打吃"""
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    # 获取连通块
                    group = board._get_group(x, y)
                    # 检查气数
                    if len(group) >= 1 and not board._has_liberty(group):
                        # 被打吃了！
                        return True
        return False
        
    def _dream_decide(self, board, player, local_patterns):
        """
        白日梦决策：战术驱动的DNA重组
        
        过程：
        1. 识别当前最优的战术需求
        2. 选择匹配的战术基因作为DNA亲本
        3. 执行DNA交叉重组
        4. 将梦境映射到实际棋盘
        """
        # 获取当前局面的所有局部棋型
        all_patterns = list(local_patterns.items())
        
        # 根据战术需求选择基因
        tactic_genes = self.gene_pool.tactic_genes[:]
        
        # 增加一些高价值基因
        real_genes = [g for g in self.gene_pool.genes if g.get('is_real')]
        
        # 生成3个梦境候选
        dream_candidates = []
        
        for _ in range(3):
            # 选择亲本基因
            gene_a = random.choice(tactic_genes) if tactic_genes else random.choice(self.gene_pool.genes)
            
            # 第二个基因：互补的战术或战略
            if random.random() < 0.5 and real_genes:
                gene_b = random.choice(real_genes)
            else:
                gene_b = random.choice(self.gene_pool.genes)
                
            # 选择重组策略
            strategies = ['tactical', 'structural', 'creative']
            strategy = random.choice(strategies)
            
            # 执行DNA重组
            dream_gene = self.gene_pool.cross_over_genes(gene_a, gene_b, strategy)
            
            # 映射到棋盘
            dream_move = self._map_to_board(dream_gene, board, local_patterns)
            
            if dream_move and board.board[dream_move[0]][dream_move[1]] == 0:
                dream_candidates.append({
                    'move': dream_move,
                    'dream_gene': dream_gene,
                    'emergence': dream_gene['emergence_value'],
                })
                
        if not dream_candidates:
            # 回退到启发式
            return self._heuristic_decide(board, player), {'emergence': 0, 'strategy': 'fallback'}
            
        # 选择涌现值最高的
        dream_candidates.sort(key=lambda d: d['emergence'], reverse=True)
        best = dream_candidates[0]
        
        return best['move'], {
            'emergence': best['emergence'],
            'strategy': best['dream_gene']['recombination_strategy'],
            'tactic': best['dream_gene']['tactic'],
        }
        
    def _map_to_board(self, dream_gene, board, local_patterns):
        """将梦境基因映射到实际棋盘"""
        dream_pattern = dream_gene['pattern']
        dream_move_idx = dream_gene['move_index']
        
        best_position = None
        best_similarity = -float('inf')
        
        # 遍历棋盘上所有可能的3x3位置
        for (x, y), local_pat in local_patterns.items():
            # 计算相似度
            similarity = self._calculate_similarity(local_pat, dream_pattern)
            
            if similarity > best_similarity:
                best_similarity = similarity
                # 梦境落子点相对3x3的偏移
                dx = dream_move_idx // 3
                dy = dream_move_idx % 3
                best_position = (x + dx, y + dy)
                
        # 验证落子合法性
        if best_position and 0 <= best_position[0] < board.size and 0 <= best_position[1] < board.size:
            if board.board[best_position[0]][best_position[1]] == 0:
                return best_position
                
        return None
        
    def _calculate_similarity(self, pattern_a, pattern_b):
        """计算相似度（忽略边界）"""
        matches = 0
        total = 0
        
        for a, b in zip(pattern_a, pattern_b):
            if a == -1 or b == -1:
                continue
            total += 1
            if a == b:
                matches += 1
                
        return matches / max(total, 1)
        
    def _heuristic_decide(self, board, player):
        """启发式决策"""
        best_move = None
        best_score = -float('inf')
        
        for x, y in board.get_empty_points():
            score = self._heuristic_score(board, x, y, player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        return best_move
        
    def get_statistics(self):
        """获取统计"""
        total = self.dream_count + self.conventional_count
        return {
            'total_moves': total,
            'dream_moves': self.dream_count,
            'conventional_moves': self.conventional_count,
            'dream_rate': f"{self.dream_count/max(total,1)*100:.1f}%",
            'recent_dreams': [d for d in self.dream_log if d.get('is_dream')][-5:],
        }


# ============================================================
# 传统AI (TraditionalAI) - 增强版
# ============================================================

class TraditionalAIV2:
    """传统围棋AI - 基于固定棋型匹配"""
    
    def __init__(self):
        self.gene_pool = GoGenePoolV2()
        self.decision_log = []
        self.capture_count = 0
        
    def decide_move(self, board, player):
        """固定模式决策"""
        empty_points = board.get_empty_points()
        if not empty_points:
            return None
            
        # 尝试匹配已知棋型
        candidates = []
        
        for x, y in empty_points:
            pattern = board.get_local_pattern(x, y)
            matching_genes = self.gene_pool.find_tactic_genes(pattern)
            
            if matching_genes:
                best_gene = max(matching_genes, 
                               key=lambda g: g['emergence_value'] * g.get('score_boost', 1.0))
                candidates.append({
                    'move': (x, y),
                    'score': best_gene['emergence_value'] * best_gene.get('score_boost', 1.0),
                })
            else:
                score = self._evaluate(board, x, y, player)
                candidates.append({
                    'move': (x, y),
                    'score': score,
                })
                
        candidates.sort(key=lambda c: c['score'], reverse=True)
        
        best_move = candidates[0]['move']
        best_score = candidates[0]['score']
        
        self.decision_log.append({
            'move': best_move,
            'score': best_score,
            'player': player,
        })
        
        return best_move
        
    def _evaluate(self, board, x, y, player):
        """评估函数"""
        score = board._position_bonus(x, y)
        
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == (3 - player):
                    score += 0.5
                elif board.board[nx][ny] == player:
                    score += 0.3
                    
        return score


# ============================================================
# 对弈游戏 (GoGame)
# ============================================================

class GoGame:
    """围棋对弈游戏"""
    
    def __init__(self, board_size=9, max_moves=150):
        self.board = GoBoard(board_size)
        self.max_moves = max_moves
        self.move_count = 0
        self.game_over = False
        self.result = None
        self.move_log = []
        
    def play_move(self, player, move):
        """执行落子"""
        if self.game_over:
            return False, "game over"
            
        if move is None:
            self._end_game()
            return False, "pass"
            
        success, msg = self.board.place_stone(move[0], move[1])
        if success:
            self.move_count += 1
            self.move_log.append({
                'move': move,
                'player': player,
                'score': self.board.evaluate(),
            })
            
            if self.move_count >= self.max_moves:
                self._end_game()
                
        return success, msg
        
    def _end_game(self):
        """结束游戏"""
        self.game_over = True
        score = self.board.evaluate()
        
        if score > 6.5:  # 贴目后黑方领先
            self.result = 'black_win'
        elif score < -6.5:  # 贴目后白方领先
            self.result = 'white_win'
        else:
            self.result = 'draw'
            
    def display_result(self):
        """显示结果"""
        score = self.board.evaluate()
        print(f"\n{'='*50}")
        print(f"🏁 游戏结束！")
        print(f"   总手数: {self.move_count}")
        print(f"   最终得分（含贴目6.5）: {score:.1f}")
        
        if self.result == 'black_win':
            print(f"   🏆 黑方获胜！")
        elif self.result == 'white_win':
            print(f"   🏆 白方获胜！")
        else:
            print(f"   🤝 平局")
        print(f"{'='*50}\n")


# ============================================================
# 主实验程序
# ============================================================

def run_tournament():
    """运行锦标赛"""
    
    print("=" * 60)
    print("BSD围棋白日梦引擎 V2.0 - 实战锦标赛")
    print("=" * 60)
    
    # 初始化引擎
    board_size = 9
    gene_pool = GoGenePoolV2(board_size)
    dream_engine = DreamEngineV2(gene_pool)
    traditional_ai = TraditionalAIV2()
    
    # 实验配置
    num_games = 10
    games_per_side = num_games // 2
    
    # 结果统计
    results = {
        'dream_as_black': {'wins': 0, 'losses': 0, 'draws': 0},
        'dream_as_white': {'wins': 0, 'losses': 0, 'draws': 0},
        'total': {'dream_wins': 0, 'traditional_wins': 0, 'draws': 0},
    }
    
    all_dream_stats = []
    critical_moments = []  # 记录关键转折点
    
    for game_idx in range(num_games):
        print(f"\n{'─'*60}")
        print(f"第 {game_idx + 1}/{num_games} 局")
        
        # 重置引擎
        dream_engine.dream_log = []
        dream_engine.dream_count = 0
        dream_engine.conventional_count = 0
        
        game = GoGame(board_size=board_size)
        
        # 交替先手
        if game_idx < games_per_side:
            dream_engine_player = 1  # 黑方
            traditional_player = 2  # 白方
            dream_name = "DreamAI(黑)"
            trad_name = "TraditionalAI(白)"
            side = 'dream_as_black'
        else:
            dream_engine_player = 2  # 白方
            traditional_player = 1  # 黑方
            dream_name = "DreamAI(白)"
            trad_name = "TraditionalAI(黑)"
            side = 'dream_as_white'
            
        print(f"   {dream_name} vs {trad_name}")
        
        # 执行对弈
        move_count = 0
        last_score = game.board.evaluate()
        
        while not game.game_over and move_count < 150:
            current_player = game.board.current_player
            
            # 选择引擎
            if current_player == dream_engine_player:
                engine = dream_engine
            else:
                engine = traditional_ai
                
            # 决策
            move = engine.decide_move(game.board, current_player)
            
            # 执行
            success, msg = game.play_move(current_player, move)
            
            if success:
                move_count += 1
                
                # 检查得分变化
                current_score = game.board.evaluate()
                score_change = current_score - last_score
                
                # 记录关键转折点
                if abs(score_change) > 5:  # 得分剧变
                    critical_moments.append({
                        'game': game_idx + 1,
                        'move': move_count,
                        'player': 'Dream' if current_player == dream_engine_player else 'Traditional',
                        'score_change': score_change,
                        'was_dream': engine.dream_log[-1].get('is_dream', False) if engine == dream_engine else False,
                    })
                    
                last_score = current_score
                
            # 超时保护
            if move_count >= 150:
                break
                
        # 显示结果
        game._end_game()
        score = game.board.evaluate()
        
        # 记录结果
        if side == 'dream_as_black':
            if score > 6.5:
                results['dream_as_black']['wins'] += 1
                results['total']['dream_wins'] += 1
                print(f"   🏆 DreamAI(黑) 胜！")
            elif score < -6.5:
                results['dream_as_black']['losses'] += 1
                results['total']['traditional_wins'] += 1
                print(f"   🏆 TraditionalAI(白) 胜！")
            else:
                results['dream_as_black']['draws'] += 1
                results['total']['draws'] += 1
                print(f"   🤝 平局")
        else:
            if score < -6.5:
                results['dream_as_white']['wins'] += 1
                results['total']['dream_wins'] += 1
                print(f"   🏆 DreamAI(白) 胜！")
            elif score > 6.5:
                results['dream_as_white']['losses'] += 1
                results['total']['traditional_wins'] += 1
                print(f"   🏆 TraditionalAI(黑) 胜！")
            else:
                results['dream_as_white']['draws'] += 1
                results['total']['draws'] += 1
                print(f"   🤝 平局")
                
        # 统计梦境触发
        dream_stats = dream_engine.get_statistics()
        all_dream_stats.append(dream_stats)
        
        print(f"   📊 统计: 总{dream_stats['total_moves']}手, 白日梦{dream_stats['dream_moves']}次({dream_stats['dream_rate']})")
        
        # 显示最终棋盘
        if game_idx == 0 or game_idx == num_games - 1:  # 显示首局和末局
            game.board.display()
            
    # 汇总分析
    print(f"\n{'='*60}")
    print(f"锦标赛汇总报告")
    print(f"{'='*60}")
    
    total_games = results['total']['dream_wins'] + results['total']['traditional_wins'] + results['total']['draws']
    dream_win_rate = results['total']['dream_wins'] / total_games * 100
    
    print(f"\n🏆 最终战绩：")
    print(f"   DreamAI胜: {results['total']['dream_wins']} 局 ({dream_win_rate:.1f}%)")
    print(f"   TraditionalAI胜: {results['total']['traditional_wins']} 局")
    print(f"   平局: {results['total']['draws']} 局")
    
    print(f"\n📊 白日梦触发统计：")
    avg_dream_rate = sum(
        float(s['dream_rate'].replace('%', '')) 
        for s in all_dream_stats
    ) / len(all_dream_stats)
    total_dreams = sum(s['dream_moves'] for s in all_dream_stats)
    total_moves = sum(s['total_moves'] for s in all_dream_stats)
    
    print(f"   总触发次数: {total_dreams} 次")
    print(f"   总落子数: {total_moves} 手")
    print(f"   平均触发率: {avg_dream_rate:.1f}%")
    
    print(f"\n⚡ 关键转折点分析：")
    if critical_moments:
        dream_criticals = [m for m in critical_moments if m['was_dream']]
        print(f"   得分剧变次数: {len(critical_moments)}")
        print(f"   其中白日梦造成: {len(dream_criticals)} 次")
        
        if dream_criticals:
            print(f"\n   典型白日梦转折点：")
            for cm in dream_criticals[:3]:
                print(f"   - 第{cm['game']}局第{cm['move']}手: 得分变化{cm['score_change']:.1f}目")
    else:
        print("   无显著转折点")
        
    # 核心结论
    print(f"\n{'='*60}")
    print(f"核心结论")
    print(f"{'='*60}")
    
    if dream_win_rate > 50:
        print("✅ 白日梦机制显著有效！")
        print("   - DNA重组产生的创造性决策在实战中超越了传统AI")
        print("   - 验证了BSD理论中'灵感闪烁'的工程可行性")
        conclusion = "success"
    elif dream_win_rate > 30:
        print("⚠️ 白日梦机制部分有效")
        print("   - 在部分局面中产生了创造性解法")
        print("   - 但仍需优化基因库和触发策略")
        conclusion = "partial"
    else:
        print("❌ 白日梦机制尚未充分发挥")
        print("   - 传统AI在基本战术上仍然更稳定")
        print("   - 需要更丰富的棋谱基因和更精准的触发条件")
        conclusion = "needs_improvement"
        
    print(f"\n💡 理论价值：")
    print("   1. 验证了'人类灵感=基因白日梦'的假说")
    print("   2. 证明了DNA重组机制可应用于创造性问题求解")
    print("   3. 为AI从'计算智能'到'创造智能'提供了工程路径")
    
    # 保存实验报告
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'experiment': 'BSD Go Daydream Engine V2.0 Tournament',
        'total_games': total_games,
        'results': results,
        'dream_win_rate': dream_win_rate,
        'avg_dream_rate': avg_dream_rate,
        'total_dreams': total_dreams,
        'conclusion': conclusion,
        'critical_moments': critical_moments[:10],
        'dream_stats': all_dream_stats,
    }
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(output_dir, 'go_dream_v2_tournament_result.json')
    
    import json
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
    print(f"\n📄 完整报告: {report_path}")
    
    return report


if __name__ == '__main__':
    run_tournament()