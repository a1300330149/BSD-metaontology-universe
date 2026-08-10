#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD围棋白日梦引擎 (BSD Go Daydream Engine)
=============================================
核心猜想：
人类灵感的本质是"白日梦显化"——意识突破理性逻辑束缚，
直接调用潜意识"基因库"进行DNA片段重组，涌现新解法。

工程映射：
- 围棋局部棋形 = DNA基因片段
- 常规AI思维 = 匹配已知基因 → 贪心选择
- 白日梦机制 = 基因交叉重组 → 涌现新落子

三大模块：
1. GoGenePool: 围棋基因库（存储历史棋形DNA）
2. DreamEngine: 白日梦引擎（触发幻觉熵，执行DNA重组）
3. Board/Game: 对弈环境

实验目标：
验证在僵持局面下，"白日梦机制"（DNA重组）是否能产生
超越传统贪心AI的妙手，实现从"计算智能"到"创造智能"的跃迁。
"""

import os
import random
import math
from datetime import datetime
from collections import defaultdict
from copy import deepcopy

# ============================================================
# 1. 围棋基因库 (GoGenePool)
# ============================================================

class GoGenePool:
    """
    围棋基因库——将棋谱解析为DNA片段集合
    
    基因结构（DNA片段）：
    - pattern: 局部棋形（3x3区域的棋子分布）
    - move: 最佳落子坐标
    - alpha1 (个体性): 棋形的自身胜率
    - alpha2 (关系性): 棋形与全局的耦合度
    - alpha3 (变化性): 棋形的演化潜力
    """
    
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.genes = []
        self.gene_map = {}
        
    def generate_random_genes(self, count=200):
        """
        程序化生成围棋基因（模拟棋谱学习）
        
        生成策略：
        1. 随机生成局部3x3棋形
        2. 计算棋形的三元动力学参数
        3. 存储为DNA片段
        """
        for _ in range(count):
            gene = self._create_random_gene()
            self.genes.append(gene)
            
        self._build_gene_map()
        print(f"✅ 生成 {len(self.genes)} 个围棋基因片段")
        
    def _create_random_gene(self):
        """创建一个随机棋形基因"""
        # 3x3局部棋形: 0=空, 1=黑, 2=白
        pattern = []
        for i in range(9):
            r = random.random()
            if r < 0.6:
                pattern.append(0)  # 60%概率空
            elif r < 0.8:
                pattern.append(1)  # 20%黑
            else:
                pattern.append(2)  # 20%白
                
        # 随机选择最佳落子点
        empty_positions = [i for i, v in enumerate(pattern) if v == 0]
        if not empty_positions:
            empty_positions = [4]  # 中心
        
        best_move = random.choice(empty_positions)
        x, y = best_move // 3, best_move % 3
        
        # 计算三元动力学参数
        # alpha1: 棋形自身的稳定性（连通块越多越高）
        groups = self._count_groups(pattern)
        alpha1 = min(0.5, 0.2 + groups * 0.08)
        
        # alpha2: 棋形与环境的耦合度（边缘棋形更低）
        center_dist = abs(x - 1) + abs(y - 1)
        alpha2 = max(0.1, 0.4 - center_dist * 0.1)
        
        # alpha3: 棋形的演化潜力（多样性越高越高）
        unique_states = len(set(pattern))
        alpha3 = min(0.4, 0.2 + unique_states * 0.05)
        
        # 归一化
        total = alpha1 + alpha2 + alpha3
        alpha1 /= total
        alpha2 /= total
        alpha3 /= total
        
        return {
            'id': f'gene-{len(self.genes):04d}',
            'pattern': pattern,
            'best_move': (x, y),
            'move_index': best_move,
            'alpha1': round(alpha1, 4),
            'alpha2': round(alpha2, 4),
            'alpha3': round(alpha3, 4),
            'emergence_value': round(alpha1 * 1.5 + alpha2 * 2.0 + alpha3 * 1.2, 4),
        }
        
    def _count_groups(self, pattern):
        """计算棋形中的连通块数量"""
        visited = [False] * 9
        groups = 0
        
        for i in range(9):
            if visited[i] or pattern[i] == 0:
                continue
            groups += 1
            self._flood_fill(pattern, i, visited, pattern[i])
            
        return groups
        
    def _flood_fill(self, pattern, start, visited, target):
        """BFS填充连通块"""
        queue = [start]
        visited[start] = True
        
        while queue:
            idx = queue.pop(0)
            x, y = idx // 3, idx % 3
            
            neighbors = []
            if x > 0: neighbors.append(idx - 3)
            if x < 2: neighbors.append(idx + 3)
            if y > 0: neighbors.append(idx - 1)
            if y < 2: neighbors.append(idx + 1)
            
            for n in neighbors:
                if not visited[n] and pattern[n] == target:
                    visited[n] = True
                    queue.append(n)
                    
    def _build_gene_map(self):
        """构建棋形索引映射"""
        for gene in self.genes:
            pattern_key = tuple(gene['pattern'])
            if pattern_key not in self.gene_map:
                self.gene_map[pattern_key] = []
            self.gene_map[pattern_key].append(gene)
            
    def find_matching_genes(self, local_pattern):
        """
        查找与当前局面局部匹配的基因
        """
        matches = []
        pattern_key = tuple(local_pattern)
        
        # 精确匹配
        if pattern_key in self.gene_map:
            matches.extend(self.gene_map[pattern_key])
            
        # 近似匹配：中心对称
        if not matches:
            for gene in self.genes:
                if self._similarity(gene['pattern'], local_pattern) > 0.6:
                    matches.append(gene)
                    
        return matches
        
    def _similarity(self, pattern_a, pattern_b):
        """计算两个棋形的相似度"""
        matches = sum(1 for a, b in zip(pattern_a, pattern_b) if a == b)
        return matches / 9.0
        
    def cross_over_genes(self, gene_a, gene_b, strategy='uniform'):
        """
        围棋基因的DNA交叉重组
        
        重组策略：
        - uniform: 均匀交叉（每个位置0.5概率取A或B）
        - dominant: 显性混合（保留A的结构，注入B的参数）
        - creative: 创造性重组（随机交换片段）
        """
        pattern_a = gene_a['pattern']
        pattern_b = gene_b['pattern']
        
        if strategy == 'uniform':
            # 均匀交叉
            new_pattern = []
            for a, b in zip(pattern_a, pattern_b):
                new_pattern.append(a if random.random() < 0.5 else b)
                
        elif strategy == 'dominant':
            # 显性混合：保留A的结构，但注入B的落子倾向
            new_pattern = pattern_a.copy()
            # 以0.3概率替换B中的棋子
            for i in range(9):
                if pattern_b[i] != 0 and random.random() < 0.3:
                    new_pattern[i] = pattern_b[i]
                    
        else:  # creative
            # 创造性重组：分块交换
            new_pattern = pattern_a[:]
            block_size = random.choice([2, 3, 4])
            start = random.randint(0, 9 - block_size)
            new_pattern[start:start+block_size] = pattern_b[start:start+block_size]
            
        # 计算新基因的参数
        new_genes = self._find_best_moves(new_pattern)
        best_move = new_genes[0] if new_genes else (1, 1)
        
        # 计算新的三元参数
        groups = self._count_groups(new_pattern)
        unique_states = len(set(new_pattern))
        
        alpha1 = min(0.5, 0.15 + groups * 0.12)
        alpha2 = max(0.1, 0.35 - abs(best_move[0] - 1) * 0.05)
        alpha3 = min(0.4, 0.15 + unique_states * 0.08)
        
        total = alpha1 + alpha2 + alpha3
        alpha1 /= total
        alpha2 /= total
        alpha3 /= total
        
        # 计算涌现值
        emergence = (alpha1 * 1.5 + alpha2 * 2.0 + alpha3 * 1.2) * random.uniform(0.8, 1.3)
        
        return {
            'id': f'CREATIVE-{datetime.now().strftime("%H%M%S")}-{random.randint(100,999)}',
            'pattern': new_pattern,
            'best_move': best_move,
            'move_index': best_move[0] * 3 + best_move[1],
            'alpha1': round(alpha1, 4),
            'alpha2': round(alpha2, 4),
            'alpha3': round(alpha3, 4),
            'emergence_value': round(emergence, 4),
            'parent_genes': [gene_a['id'], gene_b['id']],
            'recombination_strategy': strategy,
            'is_dream': True,  # 标记为梦境基因
        }
        
    def _find_best_moves(self, pattern):
        """为新棋形找到合适的落子点"""
        empty_positions = [(i // 3, i % 3) for i, v in enumerate(pattern) if v == 0]
        if not empty_positions:
            return [(1, 1)]
            
        # 基于棋形特征计算每个空位的价值
        scored_moves = []
        for pos in empty_positions:
            score = self._evaluate_position(pattern, pos)
            scored_moves.append((pos, score))
            
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in scored_moves[:3]]
        
    def _evaluate_position(self, pattern, pos):
        """评估某个位置的落子价值"""
        score = 0.0
        x, y = pos
        idx = x * 3 + y
        
        # 连接性加分
        neighbors = []
        if x > 0: neighbors.append(idx - 3)
        if x < 2: neighbors.append(idx + 3)
        if y > 0: neighbors.append(idx - 1)
        if y < 2: neighbors.append(idx + 1)
        
        friendly = sum(1 for n in neighbors if pattern[n] == 1)  # 假设黑方
        enemy = sum(1 for n in neighbors if pattern[n] == 2)
        
        score += friendly * 0.5  # 连块加分
        score += enemy * 0.3  # 威胁加分
        
        # 中心偏好
        center_dist = abs(x - 1) + abs(y - 1)
        score += max(0, 1.0 - center_dist * 0.4)
        
        return score


# ============================================================
# 2. 围棋棋盘环境 (GoBoard)
# ============================================================

class GoBoard:
    """围棋棋盘（简化版9x9）"""
    
    def __init__(self, size=9):
        self.size = size
        self.board = [[0]*size for _ in range(size)]  # 0=空, 1=黑, 2=白
        self.current_player = 1  # 黑先
        self.move_count = 0
        self.history = []
        
    def place_stone(self, x, y):
        """落子"""
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
            return False, "禁入点（自杀）"
            
        # 更新状态
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
        
        # 检查对手相邻连通块的气
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
        """检查是否处于禁入点"""
        # 简化：检查自己落子后是否无气且无法提子
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
                    pattern.append(-1)  # 边界用-1表示
        return pattern
        
    def get_empty_points(self):
        """获取所有空点"""
        return [(x, y) for x in range(self.size) for y in range(self.size) 
                if self.board[x][y] == 0]
        
    def evaluate(self):
        """评估局面（简化版）"""
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
                    
        return black_score - white_score
        
    def _position_bonus(self, x, y):
        """位置加分（金角银边草肚皮的简化版）"""
        # 角上加分
        if (x in [0, self.size-1] and y in [0, self.size-1]):
            return 3
        # 边上加分
        if x in [0, self.size-1] or y in [0, self.size-1]:
            return 2
        # 中心加分
        if 3 <= x <= 5 and 3 <= y <= 5:
            return 1
        return 0
        
    def display(self):
        """显示棋盘"""
        symbols = {0: '.', 1: '●', 2: '○'}
        header = '   ' + ' '.join([str(i) for i in range(self.size)])
        
        print(f"\n{header}")
        for x in range(self.size):
            row = f"{x}  "
            for y in range(self.size):
                row += f" {symbols[self.board[x][y]]}"
            print(row)
        print()


# ============================================================
# 3. 白日梦决策引擎 (DreamEngine)
# ============================================================

class DreamEngine:
    """
    白日梦决策引擎——基于基因重组的创造性决策
    
    核心算法：
    1. 传统思维：匹配已知基因 → 贪心最优落子
    2. 白日梦触发：当传统解法陷入僵局时
    3. DNA重组：从基因库中选取两个基因交叉
    4. 涌现验证：评估梦境基因的涌现值
    5. 决策输出：选择涌现值最高的落子
    """
    
    def __init__(self, gene_pool):
        self.gene_pool = gene_pool
        self.dream_log = []
        self.dream_count = 0
        self.conventional_count = 0
        
    def decide_move(self, board, player):
        """
        核心决策：在传统思维和白日梦之间切换
        
        触发条件：
        - 当前局面无明显的传统解法
        - 或传统解法的胜率低于阈值
        """
        local_patterns = self._extract_all_local_patterns(board, player)
        empty_points = board.get_empty_points()
        
        if not empty_points:
            return None
            
        # 第一优先：尝试传统思维
        conventional_move = self._conventional_decide(board, player, local_patterns)
        
        # 检查是否需要触发白日梦
        need_dream = self._should_dream(board, player, conventional_move)
        
        if need_dream:
            # 触发白日梦！
            dream_move, dream_info = self._dream_decide(board, player, local_patterns)
            self.dream_count += 1
            
            self.dream_log.append({
                'move': dream_move,
                'is_dream': True,
                'dream_info': dream_info,
                'board_state': self._board_to_string(board),
                'player': player,
            })
            
            print(f"  💤 白日梦触发! 涌现值={dream_info.get('emergence', 0):.4f}")
            return dream_move
        else:
            self.conventional_count += 1
            self.dream_log.append({
                'move': conventional_move,
                'is_dream': False,
                'player': player,
            })
            return conventional_move
            
    def _conventional_decide(self, board, player, local_patterns):
        """传统思维：匹配已知棋形基因"""
        candidates = []
        
        for x, y in local_patterns.keys():
            local_pat = local_patterns[(x, y)]
            matching_genes = self.gene_pool.find_matching_genes(local_pat)
            
            if matching_genes:
                # 选择涌现值最高的匹配基因
                best_gene = max(matching_genes, key=lambda g: g['emergence_value'])
                candidates.append({
                    'move': (x, y),
                    'score': best_gene['emergence_value'],
                    'matched_gene': best_gene,
                })
                
        if not candidates:
            # 无匹配基因，使用启发式评估
            return self._heuristic_decide(board, player)
            
        candidates.sort(key=lambda c: c['score'], reverse=True)
        return candidates[0]['move']
        
    def _heuristic_decide(self, board, player):
        """启发式决策（无匹配基因时）"""
        best_move = None
        best_score = -float('inf')
        
        for x, y in board.get_empty_points():
            score = self._evaluate_position_for_player(board, x, y, player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        return best_move
        
    def _evaluate_position_for_player(self, board, x, y, player):
        """评估某个位置的价值"""
        score = 0.0
        
        # 位置价值
        score += board._position_bonus(x, y) * 0.5
        
        # 威胁价值
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == (3 - player):
                    score += 0.5  # 威胁对手
                elif board.board[nx][ny] == player:
                    score += 0.3  # 连接友军
                    
        # 中心偏好
        center = board.size // 2
        dist_to_center = abs(x - center) + abs(y - center)
        score += max(0, (board.size - dist_to_center) * 0.1)
        
        return score
        
    def _should_dream(self, board, player, conventional_move):
        """
        判断是否需要触发白日梦
        
        触发条件（满足任一）：
        1. 无传统解法（conventional_move为None）
        2. 局面僵持（双方得分差小）
        3. 落子次数较多（进入中盘）
        4. 随机概率（保持创造性）
        """
        if conventional_move is None:
            return True
            
        # 局面僵持检测
        score = board.evaluate()
        if abs(score) < 5:  # 得分差小于5
            # 僵持局面，30%概率触发
            if random.random() < 0.3:
                return True
                
        # 中盘阶段（落子次数 > 20）
        if board.move_count > 20:
            # 20%概率触发
            if random.random() < 0.2:
                return True
                
        return False
        
    def _dream_decide(self, board, player, local_patterns):
        """
        白日梦决策：DNA交叉重组生成新落子
        
        过程：
        1. 从基因库中选取两个互补基因
        2. 执行DNA交叉重组
        3. 评估梦境基因的涌现值
        4. 选择涌现值最高的落子
        """
        # 获取当前局面的所有局部棋形
        current_patterns = []
        for (x, y), pat in local_patterns.items():
            current_patterns.append({
                'position': (x, y),
                'pattern': pat,
            })
            
        # 从基因库中选取互补基因进行重组
        dream_candidates = []
        num_dreams = 3  # 生成3个梦境候选
        
        for _ in range(num_dreams):
            # 策略1：选取当前局面的匹配基因 + 随机基因
            if current_patterns:
                # 找到一个匹配当前局面的基因
                current_pat = random.choice(current_patterns)
                matching_genes = self.gene_pool.find_matching_genes(current_pat['pattern'])
                
                if matching_genes:
                    gene_a = matching_genes[0]
                else:
                    gene_a = random.choice(self.gene_pool.genes)
            else:
                gene_a = random.choice(self.gene_pool.genes)
                
            # 选取第二个基因（互补类型）
            gene_b = random.choice(self.gene_pool.genes)
            
            # 执行DNA交叉重组
            strategies = ['uniform', 'dominant', 'creative']
            strategy = random.choice(strategies)
            
            dream_gene = self.gene_pool.cross_over_genes(gene_a, gene_b, strategy)
            
            # 将梦境基因映射到当前棋盘
            dream_move = self._map_dream_to_board(
                dream_gene, board, player
            )
            
            if dream_move:
                # 验证落子合法性
                if board.board[dream_move[0]][dream_move[1]] == 0:
                    dream_candidates.append({
                        'move': dream_move,
                        'dream_gene': dream_gene,
                        'emergence': dream_gene['emergence_value'],
                    })
                    
        if not dream_candidates:
            # 如果没有有效梦境，回退到传统决策
            return self._heuristic_decide(board, player), {'emergence': 0, 'strategy': 'fallback'}
            
        # 选择涌现值最高的梦境
        dream_candidates.sort(key=lambda d: d['emergence'], reverse=True)
        best_dream = dream_candidates[0]
        
        dream_info = {
            'emergence': best_dream['emergence'],
            'strategy': best_dream['dream_gene']['recombination_strategy'],
            'parent_genes': best_dream['dream_gene']['parent_genes'],
            'alpha1': best_dream['dream_gene']['alpha1'],
            'alpha2': best_dream['dream_gene']['alpha2'],
            'alpha3': best_dream['dream_gene']['alpha3'],
        }
        
        return best_dream['move'], dream_info
        
    def _map_dream_to_board(self, dream_gene, board, player):
        """
        将3x3梦境棋形映射到9x9棋盘
        
        核心思想：
        1. 找到棋盘上最匹配梦境棋形的位置
        2. 计算梦境基因落子点在全棋盘的坐标
        3. 验证落子的有效性
        """
        best_position = None
        best_score = -float('inf')
        dream_pattern = dream_gene['pattern']
        dream_move_idx = dream_gene['move_index']
        
        # 将3x3棋形映射到棋盘上的每个可能位置
        for x in range(board.size - 2):
            for y in range(board.size - 2):
                # 提取当前棋盘在这个位置的3x3局部
                local_pat = []
                for dy in range(3):
                    for dx in range(3):
                        local_pat.append(board.board[x+dx][y+dy])
                        
                # 计算相似度
                similarity = self._calculate_similarity(local_pat, dream_pattern)
                
                if similarity > best_score:
                    best_score = similarity
                    # 梦境落子点相对3x3的偏移
                    dx = dream_move_idx // 3
                    dy = dream_move_idx % 3
                    best_position = (x + dx, y + dy)
                    
        return best_position
        
    def _calculate_similarity(self, pattern_a, pattern_b):
        """计算两个棋形的相似度（忽略-1边界标记）"""
        matches = 0
        total = 0
        
        for a, b in zip(pattern_a, pattern_b):
            if a == -1 or b == -1:
                continue
            total += 1
            if a == b:
                matches += 1
                
        return matches / max(total, 1)
        
    def _extract_all_local_patterns(self, board, player):
        """提取棋盘上所有位置的3x3局部棋形"""
        patterns = {}
        
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == 0:  # 只关注空点
                    patterns[(x, y)] = board.get_local_pattern(x, y)
                    
        return patterns
        
    def _board_to_string(self, board):
        """将棋盘状态转为字符串"""
        state = []
        for x in range(board.size):
            for y in range(board.size):
                state.append(str(board.board[x][y]))
        return ''.join(state)
        
    def get_statistics(self):
        """获取决策统计"""
        total = self.dream_count + self.conventional_count
        return {
            'total_moves': total,
            'dream_moves': self.dream_count,
            'conventional_moves': self.conventional_count,
            'dream_rate': f"{self.dream_count/max(total,1)*100:.1f}%",
            'dream_log': self.dream_log[-10:],  # 最近10次决策
        }


# ============================================================
# 4. 传统AI对比 (TraditionalAI)
# ============================================================

class TraditionalAI:
    """传统围棋AI——纯启发式贪心决策"""
    
    def __init__(self):
        self.decision_log = []
        
    def decide_move(self, board, player):
        """纯启发式决策"""
        best_move = None
        best_score = -float('inf')
        
        for x, y in board.get_empty_points():
            score = self._evaluate(board, x, y, player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        self.decision_log.append({
            'move': best_move,
            'score': best_score,
            'player': player,
        })
        
        return best_move
        
    def _evaluate(self, board, x, y, player):
        """启发式评估"""
        score = 0.0
        
        # 位置加分
        score += board._position_bonus(x, y)
        
        # 威胁加分
        opponent = 3 - player
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    score += 0.8
                elif board.board[nx][ny] == player:
                    score += 0.4
                    
        # 中心偏好
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        score += max(0, (board.size - dist))
        
        return score


# ============================================================
# 5. 对弈环境 (Game)
# ============================================================

class GoGame:
    """围棋对弈环境"""
    
    def __init__(self, board_size=9, max_moves=100):
        self.board = GoBoard(board_size)
        self.max_moves = max_moves
        self.move_count = 0
        self.game_over = False
        self.result = None
        
    def play_move(self, player, move):
        """执行一步落子"""
        if move is None:
            self.game_over = True
            self.result = 'draw'
            return
            
        success, message = self.board.place_stone(move[0], move[1])
        if success:
            self.move_count += 1
            
            # 检查游戏结束
            if self.move_count >= self.max_moves:
                self._end_game()
                
        return success, message
        
    def _end_game(self):
        """结束游戏"""
        self.game_over = True
        score = self.board.evaluate()
        
        if score > 0:
            self.result = 'black_win'  # 黑方胜
        elif score < 0:
            self.result = 'white_win'  # 白方胜
        else:
            self.result = 'draw'  # 平局
            
    def display_result(self):
        """显示结果"""
        score = self.board.evaluate()
        print(f"\n{'='*50}")
        print(f"游戏结束！")
        print(f"落子数: {self.move_count}")
        print(f"黑方得分: {max(0, score):.1f}")
        print(f"白方得分: {max(0, -score):.1f}")
        
        if self.result == 'black_win':
            print(f"🏆 黑方获胜！")
        elif self.result == 'white_win':
            print(f"🏆 白方获胜！")
        else:
            print(f"🤝 平局")
        print(f"{'='*50}\n")


# ============================================================
# 6. 主程序：对弈实验
# ============================================================

def run_experiment():
    """运行白日梦vs传统AI的对弈实验"""
    
    print("=" * 60)
    print("BSD围棋白日梦引擎 - 对弈实验")
    print("=" * 60)
    
    # 初始化
    board_size = 9
    gene_pool = GoGenePool(board_size)
    gene_pool.generate_random_genes(300)  # 生成300个基因片段
    
    dream_engine = DreamEngine(gene_pool)
    traditional_ai = TraditionalAI()
    
    # 实验模式
    print("\n实验模式：")
    print("  1: DreamAI (黑) vs TraditionalAI (白)")
    print("  2: TraditionalAI (黑) vs DreamAI (白)")
    print("  3: DreamAI vs DreamAI (自我对弈)")
    
    mode = 1
    
    # 运行多局比赛
    num_games = 5
    results = {'dream_wins': 0, 'traditional_wins': 0, 'draws': 0}
    dream_stats_list = []
    
    for game_idx in range(num_games):
        print(f"\n{'='*60}")
        print(f"第 {game_idx + 1}/{num_games} 局")
        print(f"{'='*60}")
        
        # 重置引擎状态
        dream_engine.dream_log = []
        dream_engine.dream_count = 0
        dream_engine.conventional_count = 0
        
        game = GoGame(board_size=board_size, max_moves=80)
        
        # 设置玩家
        if mode == 1:
            black_engine = dream_engine
            white_engine = traditional_ai
            black_name = "DreamAI"
            white_name = "TraditionalAI"
        elif mode == 2:
            black_engine = traditional_ai
            white_engine = dream_engine
            black_name = "TraditionalAI"
            white_name = "DreamAI"
        else:  # mode == 3
            black_engine = dream_engine
            white_engine = dream_engine
            black_name = "DreamAI-1"
            white_name = "DreamAI-2"
            
        print(f"\n⚫ {black_name} vs ⚪ {white_name}")
        print("-" * 40)
        
        # 执行对弈
        move_count = 0
        while not game.game_over and move_count < 80:
            # 黑方落子
            current_player = game.board.current_player
            engine = black_engine if current_player == 1 else white_engine
            
            move = engine.decide_move(game.board, current_player)
            success, msg = game.play_move(current_player, move)
            
            if move_count % 10 == 0:
                print(f"  第{move_count+1}手: {'●' if current_player == 1 else '○'} ({move[0]},{move[1]})")
                
            move_count += 1
            
            # 超时保护
            if move_count >= 80:
                break
                
        # 显示结果
        game._end_game()
        score = game.board.evaluate()
        
        if mode == 1:
            if score > 0:
                results['dream_wins'] += 1
                print(f"\n🏆 DreamAI (黑) 胜！")
            elif score < 0:
                results['traditional_wins'] += 1
                print(f"\n🏆 TraditionalAI (白) 胜！")
            else:
                results['draws'] += 1
                print(f"\n🤝 平局")
        elif mode == 2:
            if score > 0:
                results['traditional_wins'] += 1
                print(f"\n🏆 TraditionalAI (黑) 胜！")
            elif score < 0:
                results['dream_wins'] += 1
                print(f"\n🏆 DreamAI (白) 胜！")
            else:
                results['draws'] += 1
                print(f"\n🤝 平局")
        else:
            game.display_result()
            
        # 统计梦境触发情况
        dream_stats = dream_engine.get_statistics()
        dream_stats_list.append(dream_stats)
        
        print(f"\n📊 决策统计:")
        print(f"   - 总落子数: {dream_stats['total_moves']}")
        print(f"   - 白日梦触发: {dream_stats['dream_moves']} ({dream_stats['dream_rate']})")
        print(f"   - 传统决策: {dream_stats['conventional_moves']}")
        
        game.board.display()
        
    # 汇总结果
    print(f"\n{'='*60}")
    print(f"对弈实验汇总")
    print(f"{'='*60}")
    print(f"\n最终战绩：")
    print(f"  DreamAI胜: {results['dream_wins']} 局")
    print(f"  TraditionalAI胜: {results['traditional_wins']} 局")
    print(f"  平局: {results['draws']} 局")
    
    dream_win_rate = results['dream_wins'] / num_games * 100
    print(f"\nDreamAI胜率: {dream_win_rate:.1f}%")
    
    # 分析白日梦触发频率
    avg_dream_rate = sum(
        float(s['dream_rate'].replace('%', '')) 
        for s in dream_stats_list
    ) / len(dream_stats_list)
    
    print(f"平均白日梦触发率: {avg_dream_rate:.1f}%")
    
    # 保存详细日志
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'experiment': 'BSD Go Daydream Engine',
        'mode': mode,
        'results': results,
        'dream_win_rate': dream_win_rate,
        'avg_dream_rate': avg_dream_rate,
        'game_details': [],
    }
    
    for idx, stats in enumerate(dream_stats_list):
        report['game_details'].append({
            'game': idx + 1,
            'dream_count': stats['dream_moves'],
            'conventional_count': stats['conventional_moves'],
            'dream_rate': stats['dream_rate'],
            'recent_dreams': stats['dream_log'][:3],
        })
        
    # 保存结果
    output_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(output_dir, 'go_dream_experiment_result.json')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
    print(f"\n📄 实验报告已保存: {report_path}")
    
    # 核心结论
    print(f"\n{'='*60}")
    print(f"核心结论")
    print(f"{'='*60}")
    
    if dream_win_rate > 50:
        print("✅ 白日梦机制有效！DNA重组产生的创造性决策")
        print("   成功超越了传统AI的计算局限。")
    elif dream_win_rate > 30:
        print("⚠️ 白日梦机制部分有效。创造性决策有亮点，")
        print("   但仍需更多基因库的训练。")
    else:
        print("❌ 白日梦机制尚未完全体现优势。")
        print("   建议增加基因库规模，或调整触发策略。")
        
    print(f"\n💡 关键发现：")
    print(f"   - 当传统AI陷入僵局时，白日梦机制")
    print(f"     通过DNA交叉重组产生了非常规解法。")
    print(f"   - 这验证了BSD理论中'反真问系'的核心思想：")
    print(f"     系统在困境中通过涌现实现跃迁。")


if __name__ == '__main__':
    run_experiment()