#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD围棋白日梦引擎 V2.1 - 快速测试版
====================================
简化版用于快速验证核心机制
"""

import os
import sys
import random
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 简化版棋盘
# ============================================================

class SimpleBoard:
    """简化版围棋棋盘"""
    
    def __init__(self, size=9):
        self.size = size
        self.board = [[0]*size for _ in range(size)]
        self.current_player = 1
        self.move_count = 0
        
    def place_stone(self, x, y):
        if x is None or y is None:
            return False
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        if self.board[x][y] != 0:
            return False
            
        # 简化版不做提子和自杀检查
        self.board[x][y] = self.current_player
        self.move_count += 1
        self.current_player = 3 - self.current_player
        return True
        
    def get_local_pattern(self, x, y, radius=1):
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
        return [(x, y) for x in range(self.size) for y in range(self.size) 
                if self.board[x][y] == 0]
        
    def evaluate(self):
        score = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    score += 1
                    score += self._position_bonus(x, y)
                elif self.board[x][y] == 2:
                    score -= 1
                    score -= self._position_bonus(x, y)
        return score
        
    def _position_bonus(self, x, y):
        if (x in [0, self.size-1] and y in [0, self.size-1]):
            return 3
        if x in [0, self.size-1] or y in [0, self.size-1]:
            return 2
        return 1


# ============================================================
# 简化版基因库
# ============================================================

class SimpleGenePool:
    """简化版基因库"""
    
    def __init__(self):
        self.genes = []
        self._init_genes()
        
    def _init_genes(self):
        """初始化基因"""
        # 基础棋型基因
        base_patterns = [
            {'p': [0,0,0, 0,0,0, 0,0,1], 'm': (2,2), 'v': 0.9},  # 星位
            {'p': [0,0,0, 0,0,0, 0,1,0], 'm': (2,1), 'v': 0.8},  # 小目
            {'p': [0,0,0, 0,1,0, 0,0,0], 'm': (1,1), 'v': 0.85}, # 高目
            # 战术基因
            {'p': [0,2,0, 2,0,0, 0,1,0], 'm': (1,1), 'v': 1.5}, # 打吃
            {'p': [0,0,0, 0,1,0, 0,2,0], 'm': (0,1), 'v': 1.2}, # 长气
            {'p': [1,0,1, 0,0,0, 0,0,0], 'm': (0,1), 'v': 1.3}, # 连接
            {'p': [2,0,2, 0,1,0, 0,0,0], 'm': (0,1), 'v': 1.4}, # 断
            # 战略基因
            {'p': [0,0,0, 0,1,0, 0,0,0], 'm': (0,1), 'v': 1.0}, # 扩张
            {'p': [0,1,0, 0,2,0, 0,0,0], 'm': (2,1), 'v': 0.9}, # 防守
            {'p': [0,2,0, 0,0,0, 1,0,0], 'm': (0,1), 'v': 1.1}, # 进攻
        ]
        
        for i, bp in enumerate(base_patterns):
            self.genes.append({
                'id': f'gene-{i}',
                'pattern': bp['p'],
                'best_move': bp['m'],
                'move_index': bp['m'][0] * 3 + bp['m'][1],
                'value': bp['v'],
            })
            
        # 添加随机基因
        for i in range(50):
            pattern = [random.choice([0,0,0,0,1,2]) for _ in range(9)]
            empty = [j for j, v in enumerate(pattern) if v == 0]
            if not empty:
                empty = [4]
            move = random.choice(empty)
            self.genes.append({
                'id': f'random-{i}',
                'pattern': pattern,
                'best_move': (move//3, move%3),
                'move_index': move,
                'value': random.uniform(0.5, 1.5),
            })
            
    def find_matches(self, pattern):
        """查找匹配基因"""
        matches = []
        for gene in self.genes:
            sim = self._similarity(gene['pattern'], pattern)
            if sim > 0.5:
                gene_copy = gene.copy()
                gene_copy['sim'] = sim
                matches.append(gene_copy)
        return sorted(matches, key=lambda g: g['sim'], reverse=True)
        
    def _similarity(self, a, b):
        matches = sum(1 for x, y in zip(a, b) if x == y and x != -1)
        total = sum(1 for x, y in zip(a, b) if x != -1 and y != -1)
        return matches / max(total, 1)
        
    def cross_over(self, gene_a, gene_b, strategy='mixed'):
        """DNA交叉"""
        new_pattern = gene_a['pattern'][:]
        
        if strategy == 'swap':
            # 交换基因
            new_pattern = gene_b['pattern'][:]
            move = gene_b['best_move']
            value = (gene_a['value'] + gene_b['value']) / 2 * 1.2
        elif strategy == 'mix':
            # 混合
            for i in range(9):
                if random.random() < 0.5:
                    new_pattern[i] = gene_b['pattern'][i]
            empty = [j for j, v in enumerate(new_pattern) if v == 0]
            if not empty:
                empty = [4]
            move_idx = random.choice(empty)
            move = (move_idx // 3, move_idx % 3)
            value = (gene_a['value'] + gene_b['value']) / 2 * 1.1
        else:  # tactical
            # 战术融合
            new_pattern = gene_a['pattern'][:]
            move = gene_b['best_move']  # 使用B的战术意图
            value = max(gene_a['value'], gene_b['value']) * 1.3  # 战术加成
            
        return {
            'id': f'dream-{datetime.now().strftime("%H%M%S")}-{random.randint(100,999)}',
            'pattern': new_pattern,
            'best_move': move,
            'move_index': move[0] * 3 + move[1],
            'value': value,
            'strategy': strategy,
            'is_dream': True,
        }


# ============================================================
# 简化版白日梦引擎
# ============================================================

class DreamEngineLite:
    """简化版白日梦引擎"""
    
    def __init__(self, gene_pool):
        self.gene_pool = gene_pool
        self.dream_count = 0
        self.conventional_count = 0
        self.dream_log = []
        
    def decide_move(self, board, player):
        empty = board.get_empty_points()
        if not empty:
            return None
            
        # 提取局部棋型
        patterns = {}
        for x, y in empty:
            patterns[(x,y)] = board.get_local_pattern(x, y)
            
        # 传统决策
        conv_move = self._conventional_decide(board, player, patterns)
        
        # 检查是否需要白日梦
        if self._need_dream(board, player):
            # 触发白日梦
            dream_move, info = self._dream_decide(board, player, patterns)
            self.dream_count += 1
            self.dream_log.append({'move': dream_move, 'is_dream': True, 'info': info})
            return dream_move
        else:
            self.conventional_count += 1
            self.dream_log.append({'move': conv_move, 'is_dream': False})
            return conv_move
            
    def _conventional_decide(self, board, player, patterns):
        """传统决策"""
        best_move = None
        best_score = -float('inf')
        
        for (x, y), pattern in patterns.items():
            matches = self.gene_pool.find_matches(pattern)
            if matches:
                score = matches[0]['value'] * matches[0]['sim']
            else:
                score = self._heuristic(board, x, y, player)
                
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        return best_move
        
    def _heuristic(self, board, x, y, player):
        """启发式评分"""
        score = board._position_bonus(x, y) * 0.5
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == (3-player):
                    score += 0.5
                elif board.board[nx][ny] == player:
                    score += 0.3
        center = board.size // 2
        dist = abs(x-center) + abs(y-center)
        score += max(0, board.size - dist) * 0.05
        return score
        
    def _need_dream(self, board, player):
        """判断是否需要白日梦"""
        score = board.evaluate()
        # 僵持局面
        if abs(score) < 5 and random.random() < 0.4:
            return True
        # 中盘随机
        if board.move_count > 15 and random.random() < 0.2:
            return True
        return False
        
    def _dream_decide(self, board, player, patterns):
        """白日梦决策"""
        # 选择亲本基因
        gene_a = random.choice(self.gene_pool.genes)
        gene_b = random.choice(self.gene_pool.genes)
        
        # 执行DNA交叉
        strategies = ['swap', 'mix', 'tactical']
        strategy = random.choice(strategies)
        dream_gene = self.gene_pool.cross_over(gene_a, gene_b, strategy)
        
        # 映射到棋盘
        best_pos = None
        best_sim = -float('inf')
        dream_pattern = dream_gene['pattern']
        dream_idx = dream_gene['move_index']
        
        for (x, y), local_pat in patterns.items():
            sim = self._calc_sim(local_pat, dream_pattern)
            if sim > best_sim:
                best_sim = sim
                dx, dy = dream_idx // 3, dream_idx % 3
                best_pos = (x + dx, y + dy)
                
        if best_pos and 0 <= best_pos[0] < board.size and 0 <= best_pos[1] < board.size:
            if board.board[best_pos[0]][best_pos[1]] == 0:
                return best_pos, {'value': dream_gene['value'], 'strategy': strategy}
                
        # 回退
        return self._heuristic_decide(board, player), {'value': 0, 'strategy': 'fallback'}
        
    def _calc_sim(self, a, b):
        matches = sum(1 for x, y in zip(a, b) if x == y and x != -1)
        total = sum(1 for x, y in zip(a, b) if x != -1 and y != -1)
        return matches / max(total, 1)
        
    def _heuristic_decide(self, board, player):
        """启发式"""
        best_move = None
        best_score = -float('inf')
        for x, y in board.get_empty_points():
            score = self._heuristic(board, x, y, player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move
        
    def get_stats(self):
        total = self.dream_count + self.conventional_count
        return {
            'total': total,
            'dreams': self.dream_count,
            'rate': f"{self.dream_count/max(total,1)*100:.1f}%"
        }


# ============================================================
# 简化版传统AI
# ============================================================

class SimpleTraditionalAI:
    """简化版传统AI"""
    
    def __init__(self):
        self.gene_pool = SimpleGenePool()
        
    def decide_move(self, board, player):
        empty = board.get_empty_points()
        if not empty:
            return None
            
        best_move = None
        best_score = -float('inf')
        
        for x, y in empty:
            pattern = board.get_local_pattern(x, y)
            matches = self.gene_pool.find_matches(pattern)
            
            if matches:
                score = matches[0]['value'] * matches[0]['sim']
            else:
                score = self._simple_eval(board, x, y, player)
                
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        return best_move
        
    def _simple_eval(self, board, x, y, player):
        score = board._position_bonus(x, y) * 0.4
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == (3-player):
                    score += 0.4
                elif board.board[nx][ny] == player:
                    score += 0.2
        return score


# ============================================================
# 快速测试
# ============================================================

def quick_test():
    """快速测试"""
    print("=" * 50)
    print("BSD围棋白日梦引擎 - 快速测试")
    print("=" * 50)
    
    board_size = 9
    gene_pool = SimpleGenePool()
    dream_engine = DreamEngineLite(gene_pool)
    traditional = SimpleTraditionalAI()
    
    # 运行5局
    results = {'dream': 0, 'traditional': 0, 'draw': 0}
    total_dreams = 0
    
    for game in range(5):
        board = SimpleBoard(board_size)
        dream_engine.dream_count = 0
        dream_engine.conventional_count = 0
        
        # 交替先手
        if game < 3:
            black_engine = dream_engine
            white_engine = traditional
        else:
            black_engine = traditional
            white_engine = dream_engine
            
        # 运行一局
        for move in range(50):
            if move % 2 == 0:
                engine = black_engine
            else:
                engine = white_engine
                
            player = board.current_player
            move_pos = engine.decide_move(board, player)
            
            if move_pos:
                board.place_stone(move_pos[0], move_pos[1])
                
        # 计分
        score = board.evaluate()
        if game < 3:
            # DreamAI执黑
            if score > 0:
                results['dream'] += 1
            elif score < 0:
                results['traditional'] += 1
            else:
                results['draw'] += 0.5
        else:
            # DreamAI执白
            if score < 0:
                results['dream'] += 1
            elif score > 0:
                results['traditional'] += 1
            else:
                results['draw'] += 0.5
                
        total_dreams += dream_engine.dream_count
        
        print(f"\n第{game+1}局: DreamAI胜={score < 0 if game >= 3 else score > 0} | 白日梦触发={dream_engine.dream_count}次")
        
    # 汇总
    print(f"\n{'='*50}")
    print(f"测试结果：")
    print(f"   DreamAI胜: {results['dream']} 局")
    print(f"   TraditionalAI胜: {results['traditional']} 局")
    dream_rate = results['dream'] / 5 * 100
    print(f"   DreamAI胜率: {dream_rate:.1f}%")
    print(f"   总白日梦触发: {total_dreams} 次")
    print(f"   平均每局触发: {total_dreams/5:.1f} 次")
    
    # 结论
    print(f"\n{'='*50}")
    if dream_rate >= 50:
        print("✅ 白日梦机制验证成功！")
    elif dream_rate >= 30:
        print("⚠️ 白日梦机制部分有效")
    else:
        print("❌ 需要优化基因库")
        
    return results

if __name__ == '__main__':
    quick_test()