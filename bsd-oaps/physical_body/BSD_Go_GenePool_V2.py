#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD围棋白日梦引擎 V2.0 (BSD Go Daydream Engine)
=============================================
核心升级：
1. 引入真实围棋定式基因（星位、小目、高目等）
2. 引入战术基因（打吃、长气、双叫吃等）
3. DNA重组不仅随机，更基于战术意图
4. 白日梦机制在实战僵持中触发

实验目标：
验证当传统AI陷入战术死局时，"白日梦机制"（DNA重组）
能否生成突破常规的战术组合，实现真正的"灵感闪烁"。
"""

import os
import random
import math
from datetime import datetime
from collections import defaultdict
from copy import deepcopy

# ============================================================
# 0. 真实围棋基因库 - 定式与战术
# ============================================================

class GoKnowledgeBase:
    """
    围棋知识库——存储真实的定式和战术基因
    
    基因类型：
    1. 定式基因（Opening）：开局定式
    2. 战术基因（Tactic）：打吃、长气、双叫吃等
    3. 战略基因（Strategy）：扩张、防守、进攻倾向
    """
    
    # 棋型表示：0=空, 1=黑, 2=白, -1=边界
    
    @staticmethod
    def get_opening_patterns():
        """
        获取开局定式基因
        
        星位定式：占据边角的策略
        小目定式：偏重实地的策略
        高目定式：偏重外势的策略
        """
        return [
            {
                'id': 'opening-star-01',
                'name': '星位',
                'type': 'opening',
                'pattern': [
                    0, 0, 0,
                    0, 0, 0,
                    0, 0, 1  # 黑方下在星位
                ],
                'best_move': (2, 2),
                'tactic_value': 0.9,  # 进攻性
                'strategic_value': 0.7  # 战略性
            },
            {
                'id': 'opening-komoku-01',
                'name': '小目',
                'type': 'opening',
                'pattern': [
                    0, 0, 0,
                    0, 0, 0,
                    0, 1, 0  # 黑方下在小目
                ],
                'best_move': (2, 1),
                'tactic_value': 0.8,
                'strategic_value': 0.6
            },
            {
                'id': 'opening-takemoku-01',
                'name': '高目',
                'type': 'opening',
                'pattern': [
                    0, 0, 0,
                    0, 1, 0,
                    0, 0, 0  # 黑方下在高目
                ],
                'best_move': (1, 1),
                'tactic_value': 0.85,
                'strategic_value': 0.65
            }
        ]
    
    @staticmethod
    def get_tactic_patterns():
        """
        获取战术基因
        
        打吃：威胁对手棋子的气
        长气：增加自己棋子的气
        双叫吃：同时威胁两个目标
        征子：追逐对手直到无处可逃
        """
        return [
            # 打吃战术：吃掉对手孤立的棋子
            {
                'id': 'tactic-atari-01',
                'name': '打吃',
                'type': 'tactic',
                'pattern': [
                    0, 2, 0,
                    2, 0, 0,  # 对手只有两气
                    0, 1, 0   # 我方即将打吃
                ],
                'best_move': (1, 1),  # 落子打吃
                'tactic': 'capture',
                'alpha1': 0.8,  # 个体性：直接吃子
                'alpha2': 0.3,  # 关系性：影响周边
                'alpha3': 0.1,  # 变化性
                'emergence_value': 2.0
            },
            # 长气战术：保存自己的棋子
            {
                'id': 'tactic-extend-01',
                'name': '长气',
                'type': 'tactic',
                'pattern': [
                    0, 0, 0,
                    0, 1, 0,  # 我方只有一气
                    0, 2, 0   # 对手威胁
                ],
                'best_move': (0, 1),  # 向上长气
                'tactic': 'extend',
                'alpha1': 0.6,
                'alpha2': 0.5,
                'alpha3': 0.1,
                'emergence_value': 1.5
            },
            # 双叫吃战术：同时威胁两个目标
            {
                'id': 'tactic-double-01',
                'name': '双叫吃',
                'type': 'tactic',
                'pattern': [
                    0, 2, 0,
                    2, 0, 2,  # 对手有两个威胁点
                    0, 1, 0   # 我方落子
                ],
                'best_move': (1, 1),
                'tactic': 'double_threat',
                'alpha1': 0.3,
                'alpha2': 0.9,
                'alpha3': 0.2,
                'emergence_value': 2.5
            },
            # 连接战术：连接自己的棋子
            {
                'id': 'tactic-connect-01',
                'name': '连接',
                'type': 'tactic',
                'pattern': [
                    1, 0, 1,  # 两个棋子被分开
                    0, 0, 0,
                    0, 0, 0
                ],
                'best_move': (0, 1),
                'tactic': 'connect',
                'alpha1': 0.2,
                'alpha2': 0.8,
                'alpha3': 0.3,
                'emergence_value': 1.8
            },
            # 断吃战术：切断对手的连接
            {
                'id': 'tactic-cut-01',
                'name': '断',
                'type': 'tactic',
                'pattern': [
                    2, 0, 2,  # 对手看似连接
                    0, 1, 0,  # 我方准备切断
                    0, 0, 0
                ],
                'best_move': (0, 1),
                'tactic': 'cut',
                'alpha1': 0.7,
                'alpha2': 0.4,
                'alpha3': 0.2,
                'emergence_value': 1.9
            }
        ]
    
    @staticmethod
    def get_strategy_patterns():
        """
        获取战略基因
        
        扩张：扩大自己的势力范围
        防守：保护重要的棋子
        进攻：主动攻击对手的薄弱处
        """
        return [
            # 扩张战略：向中心发展
            {
                'id': 'strategy-expand-01',
                'name': '扩张',
                'type': 'strategy',
                'pattern': [
                    0, 0, 0,
                    0, 1, 0,  # 我方棋子
                    0, 0, 0
                ],
                'best_move': (0, 1),  # 向中心扩张
                'strategy': 'expand',
                'alpha1': 0.1,
                'alpha2': 0.5,
                'alpha3': 0.7,
                'emergence_value': 1.2
            },
            # 防守战略：保护基地
            {
                'id': 'strategy-defend-01',
                'name': '防守',
                'type': 'strategy',
                'pattern': [
                    0, 1, 0,
                    0, 2, 0,  # 对手威胁
                    0, 0, 0
                ],
                'best_move': (2, 1),  # 向下防守
                'strategy': 'defend',
                'alpha1': 0.4,
                'alpha2': 0.6,
                'alpha3': 0.1,
                'emergence_value': 1.3
            },
            # 进攻战略：攻击薄弱处
            {
                'id': 'strategy-attack-01',
                'name': '进攻',
                'type': 'strategy',
                'pattern': [
                    0, 2, 0,  # 对手薄弱
                    0, 0, 0,
                    1, 0, 0   # 我方棋子
                ],
                'best_move': (0, 1),  # 发起进攻
                'strategy': 'attack',
                'alpha1': 0.5,
                'alpha2': 0.3,
                'alpha3': 0.6,
                'emergence_value': 1.6
            }
        ]


# ============================================================
# 1. 围棋基因库 V2 (GoGenePoolV2)
# ============================================================

class GoGenePoolV2:
    """
    围棋基因库V2——融合真实基因与随机基因
    
    核心改进：
    1. 加载真实定式和战术基因
    2. 基于战术意图进行DNA交叉，而非随机
    3. 计算真实的涌现值（基于历史胜率）
    """
    
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.genes = []
        self.tactic_genes = []
        self.strategy_genes = []
        self.opening_genes = []
        self.gene_map = {}
        
        # 初始化知识库
        self._load_knowledge_base()
        
    def _load_knowledge_base(self):
        """加载真实基因"""
        kb = GoKnowledgeBase()
        
        # 加载定式基因
        for gene in kb.get_opening_patterns():
            self.opening_genes.append(self._convert_to_dna(gene))
            
        # 加载战术基因
        for gene in kb.get_tactic_patterns():
            self.tactic_genes.append(self._convert_to_dna(gene))
            
        # 加载战略基因
        for gene in kb.get_strategy_patterns():
            self.strategy_genes.append(self._convert_to_dna(gene))
            
        # 合并所有基因
        self.genes = self.tactic_genes + self.strategy_genes + self.opening_genes
        
        # 补充随机基因（保持多样性）
        self._add_random_genes(100)
        
        # 构建索引
        self._build_gene_map()
        
        print(f"✅ 基因库初始化完成:")
        print(f"   - 战术基因: {len(self.tactic_genes)}")
        print(f"   - 战略基因: {len(self.strategy_genes)}")
        print(f"   - 定式基因: {len(self.opening_genes)}")
        print(f"   - 随机基因: {len(self.genes) - len(self.tactic_genes) - len(self.strategy_genes) - len(self.opening_genes)}")
        
    def _convert_to_dna(self, knowledge_gene):
        """将知识库基因转换为DNA格式"""
        return {
            'id': knowledge_gene['id'],
            'name': knowledge_gene['name'],
            'type': knowledge_gene['type'],
            'pattern': knowledge_gene['pattern'],
            'best_move': knowledge_gene['best_move'],
            'move_index': knowledge_gene['best_move'][0] * 3 + knowledge_gene['best_move'][1],
            'tactic': knowledge_gene.get('tactic', 'unknown'),
            'strategy': knowledge_gene.get('strategy', 'unknown'),
            'alpha1': knowledge_gene.get('alpha1', 0.3),
            'alpha2': knowledge_gene.get('alpha2', 0.3),
            'alpha3': knowledge_gene.get('alpha3', 0.4),
            'emergence_value': knowledge_gene.get('emergence_value', 1.0),
            'is_real': True,  # 标记为真实基因
        }
        
    def _add_random_genes(self, count):
        """添加随机基因以增加多样性"""
        for i in range(count):
            pattern = []
            for j in range(9):
                r = random.random()
                if r < 0.55:
                    pattern.append(0)
                elif r < 0.8:
                    pattern.append(1)
                else:
                    pattern.append(2)
                    
            empty_positions = [i for i, v in enumerate(pattern) if v == 0]
            if not empty_positions:
                empty_positions = [4]
                
            best_move = random.choice(empty_positions)
            x, y = best_move // 3, best_move % 3
            
            alpha1 = random.uniform(0.1, 0.5)
            alpha2 = random.uniform(0.2, 0.5)
            alpha3 = max(0.05, 1.0 - alpha1 - alpha2)
            
            emergence = alpha1 * 1.5 + alpha2 * 2.0 + alpha3 * 1.2
            
            self.genes.append({
                'id': f'random-{len(self.genes):04d}',
                'name': '随机基因',
                'type': 'random',
                'pattern': pattern,
                'best_move': (x, y),
                'move_index': best_move,
                'tactic': 'unknown',
                'alpha1': round(alpha1, 4),
                'alpha2': round(alpha2, 4),
                'alpha3': round(alpha3, 4),
                'emergence_value': round(emergence, 4),
                'is_real': False,
            })
            
    def _build_gene_map(self):
        """构建棋形索引映射"""
        for gene in self.genes:
            pattern_key = tuple(gene['pattern'])
            if pattern_key not in self.gene_map:
                self.gene_map[pattern_key] = []
            self.gene_map[pattern_key].append(gene)
            
    def find_tactic_genes(self, local_pattern):
        """
        查找当前局面的战术基因
        
        特殊处理：基于当前局面的特征识别战术意图
        """
        matches = []
        pattern_key = tuple(local_pattern)
        
        # 精确匹配
        if pattern_key in self.gene_map:
            matches.extend(self.gene_map[pattern_key])
            
        # 基于战术特征的匹配
        tactic_matches = self._identify_tactics(local_pattern)
        matches.extend(tactic_matches)
        
        return matches
        
    def _identify_tactics(self, local_pattern):
        """
        识别当前局面可能的战术
        
        基于棋型特征判断：
        - 是否有打吃机会（对手棋子气少）
        - 是否可以连接（己方棋子分散）
        - 是否可以切断（对手棋子即将连接）
        """
        tactics_found = []
        
        # 特征提取
        black_positions = [i for i, v in enumerate(local_pattern) if v == 1]
        white_positions = [i for i, v in enumerate(local_pattern) if v == 2]
        empty_positions = [i for i, v in enumerate(local_pattern) if v == 0]
        
        # 检查打吃机会
        for gene in self.tactic_genes:
            if gene['tactic'] == 'capture':
                # 如果对手棋子气少
                if len(white_positions) <= 2 and empty_positions:
                    gene_copy = gene.copy()
                    gene_copy['score_boost'] = 1.5  # 打吃加成
                    tactics_found.append(gene_copy)
                    
        # 检查长气机会
        for gene in self.tactic_genes:
            if gene['tactic'] == 'extend':
                if len(black_positions) <= 2 and empty_positions:
                    gene_copy = gene.copy()
                    gene_copy['score_boost'] = 1.3
                    tactics_found.append(gene_copy)
                    
        # 检查连接机会
        for gene in self.tactic_genes:
            if gene['tactic'] == 'connect':
                if len(black_positions) >= 2 and empty_positions:
                    # 检查棋子是否分散
                    groups = self._count_groups_from_pattern(local_pattern)
                    if groups >= 2:
                        gene_copy = gene.copy()
                        gene_copy['score_boost'] = 1.4
                        tactics_found.append(gene_copy)
                        
        # 检查切断机会
        for gene in self.tactic_genes:
            if gene['tactic'] == 'cut':
                if len(white_positions) >= 2 and empty_positions:
                    groups = self._count_groups_from_pattern(local_pattern)
                    if groups >= 2:
                        gene_copy = gene.copy()
                        gene_copy['score_boost'] = 1.6
                        tactics_found.append(gene_copy)
                        
        return tactics_found
        
    def _count_groups_from_pattern(self, pattern):
        """计算棋型中的连通块数量"""
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
                    
    def cross_over_genes(self, gene_a, gene_b, strategy='tactical'):
        """
        战术驱动的DNA交叉重组
        
        策略：
        - tactical: 战术交叉（保留棋型，交换战术意图）
        - structural: 结构交叉（交换棋型的一部分）
        - creative: 创造性交叉（混合多种策略）
        """
        if strategy == 'tactical':
            # 保留基因A的棋型，但注入基因B的战术意图
            new_pattern = gene_a['pattern'][:]
            new_tactic = gene_b['tactic']
            new_strategy = gene_b.get('strategy', 'unknown')
            
            # 计算新的落子点（基于新战术）
            new_move = self._calculate_tactical_move(new_pattern, new_tactic, gene_a['best_move'])
            
            # 计算新参数
            alpha1 = (gene_a['alpha1'] + gene_b['alpha1']) / 2
            alpha2 = (gene_a['alpha2'] + gene_b['alpha2']) / 2
            alpha3 = (gene_a['alpha3'] + gene_b['alpha3']) / 2
            
            total = alpha1 + alpha2 + alpha3
            alpha1 /= total
            alpha2 /= total
            alpha3 /= total
            
            # 涌现值：基础值 + 战术加成
            emergence = (alpha1 * 1.5 + alpha2 * 2.0 + alpha3 * 1.2)
            
            # 如果是战术基因，加成更高
            if gene_b['type'] == 'tactic':
                emergence *= 1.8
            elif gene_b['type'] == 'strategy':
                emergence *= 1.5
                
            emergence *= random.uniform(0.9, 1.2)  # 随机波动
            
        elif strategy == 'structural':
            # 交换棋型的一部分
            new_pattern = gene_a['pattern'][:]
            block_start = random.randint(0, 6)
            block_end = block_start + 3
            
            # 从基因B复制片段
            if block_end <= 9:
                new_pattern[block_start:block_end] = gene_b['pattern'][block_start:block_end]
                
            new_move = gene_b['best_move']
            new_tactic = gene_b['tactic']
            
            alpha1 = gene_a['alpha1'] * 0.5 + gene_b['alpha1'] * 0.5
            alpha2 = gene_a['alpha2'] * 0.5 + gene_b['alpha2'] * 0.5
            alpha3 = gene_a['alpha3'] * 0.5 + gene_b['alpha3'] * 0.5
            
            total = alpha1 + alpha2 + alpha3
            alpha1 /= total
            alpha2 /= total
            alpha3 /= total
            
            emergence = alpha1 * 1.5 + alpha2 * 2.0 + alpha3 * 1.2
            
        else:  # creative
            # 混合多种策略
            new_pattern = gene_a['pattern'][:]
            
            # 随机交换2-3个位置
            swap_count = random.randint(2, 3)
            positions = random.sample(range(9), swap_count)
            
            for pos in positions:
                new_pattern[pos] = gene_b['pattern'][pos]
                
            new_move = self._find_best_move_in_pattern(new_pattern)
            new_tactic = random.choice([gene_a['tactic'], gene_b['tactic']])
            
            alpha1 = (gene_a['alpha1'] ** 0.7 + gene_b['alpha1'] ** 0.7) ** (1/0.7)
            alpha2 = (gene_a['alpha2'] ** 0.7 + gene_b['alpha2'] ** 0.7) ** (1/0.7)
            alpha3 = (gene_a['alpha3'] ** 0.7 + gene_b['alpha3'] ** 0.7) ** (1/0.7)
            
            total = alpha1 + alpha2 + alpha3
            alpha1 /= total
            alpha2 /= total
            alpha3 /= total
            
            emergence = alpha1 * 1.5 + alpha2 * 2.0 + alpha3 * 1.2
            emergence *= 1.3  # 创造性加成
            
        return {
            'id': f'DREAM-{datetime.now().strftime("%H%M%S")}-{random.randint(100,999)}',
            'name': f'梦境基因({strategy})',
            'type': 'dream',
            'pattern': new_pattern,
            'best_move': new_move,
            'move_index': new_move[0] * 3 + new_move[1],
            'tactic': new_tactic,
            'strategy': new_strategy if strategy == 'tactical' else 'mixed',
            'alpha1': round(alpha1, 4),
            'alpha2': round(alpha2, 4),
            'alpha3': round(alpha3, 4),
            'emergence_value': round(emergence, 4),
            'parent_genes': [gene_a['id'], gene_b['id']],
            'recombination_strategy': strategy,
            'is_dream': True,
        }
        
    def _calculate_tactical_move(self, pattern, tactic, original_move):
        """基于战术意图计算新的落子点"""
        if tactic == 'capture':
            # 打吃：找到对手棋子旁的位置
            for i, v in enumerate(pattern):
                if v == 2:  # 对手棋子
                    x, y = i // 3, i % 3
                    neighbors = []
                    if x > 0: neighbors.append(i - 3)
                    if x < 2: neighbors.append(i + 3)
                    if y > 0: neighbors.append(i - 1)
                    if y < 2: neighbors.append(i + 1)
                    
                    for n in neighbors:
                        if pattern[n] == 0:
                            return (n // 3, n % 3)
                            
        elif tactic == 'extend':
            # 长气：在己方棋子旁延伸
            for i, v in enumerate(pattern):
                if v == 1:  # 己方棋子
                    x, y = i // 3, i % 3
                    neighbors = []
                    if x > 0: neighbors.append(i - 3)
                    if x < 2: neighbors.append(i + 3)
                    if y > 0: neighbors.append(i - 1)
                    if y < 2: neighbors.append(i + 1)
                    
                    for n in neighbors:
                        if pattern[n] == 0:
                            return (n // 3, n % 3)
                            
        elif tactic == 'connect':
            # 连接：找到连接己方棋子的位置
            black_positions = [i for i, v in enumerate(pattern) if v == 1]
            if len(black_positions) >= 2:
                # 找到中间的空位
                mid = sum(black_positions) // len(black_positions)
                if pattern[mid] == 0:
                    return (mid // 3, mid % 3)
                    
        # 默认返回原位置或中心
        if pattern[4] == 0:
            return (1, 1)
        return original_move
        
    def _find_best_move_in_pattern(self, pattern):
        """为棋型找到最佳落子点"""
        empty_positions = [(i // 3, i % 3) for i, v in enumerate(pattern) if v == 0]
        if not empty_positions:
            return (1, 1)
            
        best_pos = None
        best_score = -float('inf')
        
        for pos in empty_positions:
            x, y = pos
            score = 0.0
            
            # 连接性
            idx = x * 3 + y
            neighbors = []
            if x > 0: neighbors.append(idx - 3)
            if x < 2: neighbors.append(idx + 3)
            if y > 0: neighbors.append(idx - 1)
            if y < 2: neighbors.append(idx + 1)
            
            friendly = sum(1 for n in neighbors if pattern[n] == 1)
            enemy = sum(1 for n in neighbors if pattern[n] == 2)
            
            score += friendly * 0.5
            score += enemy * 0.4
            
            # 中心偏好
            center_dist = abs(x - 1) + abs(y - 1)
            score += max(0, 1.0 - center_dist * 0.3)
            
            if score > best_score:
                best_score = score
                best_pos = pos
                
        return best_pos
