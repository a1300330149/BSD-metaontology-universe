#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 统一围棋引擎 V10.0 · 三语言涌现深度整合最终版
================================================

理论依据：
- 定理五十八·三语言涌现定理：数字(0∅反) × 英文(0∅空) × 中文(0∅义) = 自发涌现
- 定理五十九·围棋六系映射定理：围棋⊂六系立系
- 定理六十·六系协同胜率突破定理
- 定理六十一·棋形=六力投影
- 7.5.9 三语言涌现方案
- 7.5.10 围棋AI理论——六系协同决策模型

核心整合：
1. V1-V9所有版本的基因库和决策逻辑
2. 三语言涌现引擎（内置，无需外部依赖）
3. 六系物理常数定标
4. 天道追问引擎
5. 量子纠缠+DNA重组
6. 联网学习连接器
7. 统一的评分评估函数

架构：
┌─────────────────────────────────────────────────────────┐
│        BSD Unified Go Engine V10.0                     │
│                    （统一主控层）                          │
├──────────────┬──────────────┬──────────────────────────┤
│ 三语言涌现    │ 六系协同决策  │ 天道追问+觉醒决策         │
│ (数字×英文×   │ (强化·自然·  │ (循环检测·反性计算·      │
│  中文=涌现)   │  具现·变身·  │  哲学追问)                │
│              │  社会·天道)  │                          │
├──────────────┴──────────────┴──────────────────────────┤
│    Unified Gene Pool (V1+V2+V5+V6+V9 全版本基因整合)     │
├─────────────────────────────────────────────────────────┤
│    Go Physics Calibration (六系物理常数定标)               │
└─────────────────────────────────────────────────────────┘
"""

import os
import sys
import random
import math
import json
from datetime import datetime
from collections import Counter
from typing import List, Dict, Tuple, Optional

# ============================================================
# 0. 常量与配置
# ============================================================

BOARD_SIZE = 9
BOARD_SIZE_VALID = [9, 13, 19]

# 六系权重（来自V5引擎配置）
SYSTEM_WEIGHTS_V5 = {
    'qh': 0.12,   # 强化系·算力
    'zr': 0.25,   # 自然系·演化（最高）
    'jx': 0.18,   # 具现系·落子
    'bs': 0.15,   # 变身系·创新
    'sh': 0.15,   # 社会系·博弈
    'td': 0.15,   # 天道系·意义
}

# 阶段权重（三语言权重配置）
PHASE_WEIGHTS = {
    'opening': {'digital': 0.45, 'english': 0.55, 'chinese': 0.00, 'dominant': 'bs'},
    'middle':  {'digital': 0.50, 'english': 0.50, 'chinese': 0.00, 'dominant': 'zr'},
    'ending':  {'digital': 0.35, 'english': 0.00, 'chinese': 0.65, 'dominant': 'qh'},
    'final':   {'digital': 0.00, 'english': 0.00, 'chinese': 1.00, 'dominant': 'zr'},
}

# 三语言与六系协同矩阵
LANGUAGE_SYSTEM_MATRIX = {
    'number': {'qh': 0.40, 'jx': 0.35, 'zr': 0.25},
    'english': {'qh': 0.25, 'bs': 0.35, 'sh': 0.20, 'zr': 0.20},
    'chinese': {'td': 0.40, 'jx': 0.25, 'sh': 0.20, 'qh': 0.15},
}

# 天道追问配置
TIANDAO_CONFIG = {
    'cycle_threshold': 8,
    'behind_threshold': -0.25,
    'critical_threshold': -0.50,
    'insight_min_confidence': 0.7,
    'cycle_distance': 4,
}

# 六系物理常数（定理六十一）
SIX_FORCE_CONSTANTS = {
    'changlian': {'name': '长连', 'system': 'qianghua', 'constant': 'connectivity_C', 'value': 0.8},
    'feitiao':  {'name': '飞/跳', 'system': 'juxian', 'constant': 'potential_gradient_G', 'value': 0.3},
    'guaiwan':  {'name': '拐/弯', 'system': 'bianshen', 'constant': 'curvature_kappa', 'value': 0.5},
    'duanda':   {'name': '断/打', 'system': 'tiandao', 'constant': 'cutting_rate_S', 'value': 0.5},
    'qizi':     {'name': '弃子', 'system': 'ziran', 'constant': 'retention_rate_R', 'value': 0.3},
    'xietong':  {'name': '协同', 'system': 'shehui', 'constant': 'coupling_coefficient_eta', 'value': 0.7},
}

# 六系名称
SYSTEM_NAMES = {
    'qh': '强化系🔵',
    'zr': '自然系🟠',
    'jx': '具现系🔴',
    'bs': '变身系⚫',
    'sh': '社会系🟢',
    'td': '天道系🟣',
}


# ============================================================
# 1. 统一棋盘类
# ============================================================

class UnifiedBoard:
    """
    统一棋盘——兼容所有版本的棋盘接口
    
    支持接口:
    - V1: place(), empty(), score()
    - V2: get_local_pattern(), get_empty_points(), evaluate()
    - V5: 六系物理常数分析接口
    """
    
    def __init__(self, size=9):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.move_count = 0
        self.move_history = []
        self.last_move = None
        self._current_player = 1
        self.current = 1
    
    def place(self, x, y):
        """落子"""
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if self.board[x][y] != 0:
            return False
        self.board[x][y] = self._current_player
        self.move_history.append((x, y, self._current_player))
        self.last_move = (x, y)
        self._current_player = 3 - self._current_player
        self.current = self._current_player
        self.move_count += 1
        return True
    
    def empty(self):
        """获取所有空位"""
        return [(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == 0]
    
    def liberties(self, x, y, player):
        """计算棋子的气数"""
        visited = set()
        group = []
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            if not (0 <= cx < self.size and 0 <= cy < self.size):
                continue
            if self.board[cx][cy] != player:
                continue
            group.append((cx, cy))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
        liberties_set = set()
        for gx, gy in group:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = gx + dx, gy + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == 0:
                        liberties_set.add((nx, ny))
        return len(liberties_set)
    
    def liberties_at(self, x, y):
        """获取位置的气数"""
        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.board[nx][ny] == 0:
                    count += 1
        return count
    
    def _pos(self, x, y):
        """位置价值评估"""
        center = self.size / 2
        dist = abs(x - center) + abs(y - center)
        return max(0, self.size - dist) / self.size
    
    def territories(self, player):
        """计算领地"""
        visited = [[False] * self.size for _ in range(self.size)]
        territory = 0
        for x in range(self.size):
            for y in range(self.size):
                if visited[x][y]:
                    continue
                if self.board[x][y] != 0:
                    continue
                region = []
                touches_opp = False
                touches_cur = False
                stack = [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    if visited[cx][cy]:
                        continue
                    visited[cx][cy] = True
                    region.append((cx, cy))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if not (0 <= nx < self.size and 0 <= ny < self.size):
                            continue
                        if self.board[nx][ny] == 3 - player:
                            touches_opp = True
                        elif self.board[nx][ny] == player:
                            touches_cur = True
                        elif not visited[nx][ny]:
                            stack.append((nx, ny))
                if touches_cur and not touches_opp:
                    territory += len(region)
        return territory
    
    def score(self):
        """计算简单得分"""
        s = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    s += 1 + self._pos(x, y)
                elif self.board[x][y] == 2:
                    s -= 1 + self._pos(x, y)
        return s
    
    def pattern(self, x, y, r=1):
        """获取局部棋形"""
        p = []
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = x + dx, y + dy
                p.append(self.board[nx][ny] if 0 <= nx < self.size and 0 <= ny < self.size else -1)
        return p
    
    def get_local_pattern(self, x, y, radius=1):
        """获取局部棋形（V2接口）"""
        return self.pattern(x, y, radius)
    
    def get_empty_points(self):
        """获取空位（V2接口）"""
        return self.empty()
    
    def evaluate(self):
        """评估（V2接口）"""
        return self.score()
    
    def print_board(self):
        """打印棋盘"""
        symbols = {0: '.', 1: '●', 2: '○'}
        for x in range(self.size):
            row = f"{x}  "
            for y in range(self.size):
                row += f" {symbols[self.board[x][y]]}"
            print(row)


# ============================================================
# 2. 三语言涌现引擎（内置版）
#    定理五十八·三语言涌现定理
# ============================================================

class ThreeLanguageEmergenceEngine:
    """
    三语言涌现引擎——深度整合版
    
    核心方程：
    E涌现 = 0∅反 × 0∅空 × 0∅义
    
    三零元激活：
    - 数字(0∅反)：坐标映射·气数计算·领地计算
    - 英文(0∅空)：AI评估·威胁检测·棋形识别
    - 中文(0∅义)：六系坐标·棋道追问·天道追问
    
    协同矩阵（7.5.9.4）：
    ┌──────────┬─────────────┬─────────────┬─────────────┐
    │ 六系     │ 数字层激活  │ 英文层激活  │ 中文层激活  │
    ├──────────┼─────────────┼─────────────┼─────────────┤
    │ 强化系🔵 │ 0.40 领地   │ 0.25 棋形   │ 0.15 哲学   │
    │ 自然系🟠 │ 0.25 演化   │ 0.20 预测   │ 0.10 追问   │
    │ 具现系🔴 │ 0.35 落子   │ 0.15 推荐   │ 0.25 凝结   │
    │ 变身系⚫ │ 0.10 变化   │ 0.35 创新   │ 0.20 变局   │
    │ 社会系🟢 │ 0.15 博弈   │ 0.20 关系   │ 0.20 协同   │
    │ 天道系🟣 │ 0.05 对称   │ 0.10 深度   │ 0.40 意义   │
    └──────────┴─────────────┴─────────────┴─────────────┘
    """
    
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.emergence_count = 0
        self.total_evals = 0
        self.current_phase = 'opening'
        self.phase_history = []
    
    def detect_phase(self, move_count):
        """检测棋局阶段"""
        if move_count < 10:
            phase = 'opening'
        elif move_count < 40:
            phase = 'middle'
        elif move_count < 60:
            phase = 'ending'
        else:
            phase = 'final'
        self.current_phase = phase
        return phase
    
    def compute_emergence(self, board, player):
        """计算三语言涌现"""
        self.total_evals += 1
        
        if hasattr(board, 'move_count'):
            self.detect_phase(board.move_count)
        
        # 第一层：数字层（0∅反）
        fan_activation = self._compute_number_activation(board, player)
        
        # 第二层：英文层（0∅空）
        kong_activation = self._compute_english_activation(board, player)
        
        # 第三层：中文层（0∅义）
        yi_activation, liuhe_detail = self._compute_chinese_activation(board, player)
        
        # 三零元归一化
        total = fan_activation + kong_activation + yi_activation
        fan_norm = fan_activation / max(total, 0.001)
        kong_norm = kong_activation / max(total, 0.001)
        yi_norm = yi_activation / max(total, 0.001)
        
        # 涌现潜力
        potential = fan_activation * kong_activation * yi_activation
        is_emergent = potential > 0.125
        
        if is_emergent:
            self.emergence_count += 1
        
        # 阶段权重
        phase_weights = PHASE_WEIGHTS.get(self.current_phase, PHASE_WEIGHTS['middle'])
        
        # 加权得分
        weighted_score = (
            phase_weights['digital'] * fan_norm +
            phase_weights['english'] * kong_norm +
            phase_weights['chinese'] * yi_norm
        )
        
        self.phase_history.append({
            'phase': self.current_phase,
            'fan': fan_activation,
            'kong': kong_activation,
            'yi': yi_activation,
            'potential': potential,
            'is_emergent': is_emergent,
        })
        
        if len(self.phase_history) > 500:
            self.phase_history = self.phase_history[-250:]
        
        return {
            'weighted_score': weighted_score,
            'emergence_potential': potential,
            'is_emergent': is_emergent,
            'phase': self.current_phase,
            'phase_weights': phase_weights,
            'fan': fan_activation,
            'kong': kong_activation,
            'yi': yi_activation,
            'fan_norm': fan_norm,
            'kong_norm': kong_norm,
            'yi_norm': yi_norm,
            'liuhe_detail': liuhe_detail,
            'dominant_system': phase_weights['dominant'],
            'theory': '定理五十八·三语言涌现定理',
            'equation': 'E涌现 = 0∅反 × 0∅空 × 0∅义',
            'threshold': 0.125,
        }
    
    def _compute_number_activation(self, board, player):
        """计算数字层激活度（0∅反）"""
        score = 0.0
        
        # 领地评估
        own_territory = board.territories(player)
        opp_territory = board.territories(3 - player)
        territory_diff = (own_territory - opp_territory) / max(board.size * board.size, 1)
        score += 0.35 * max(-1, min(1, territory_diff))
        
        # 棋子数量
        own_stones = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    own_stones += 1
        stone_score = min(1.0, own_stones / 15.0)
        score += 0.25 * stone_score
        
        # 对称性检测
        symmetry = 0.5
        for x in range(board.size // 2):
            for y in range(board.size):
                if board.board[x][y] != board.board[board.size - 1 - x][y]:
                    symmetry -= 0.1
                    break
        symmetry = max(0.0, min(1.0, symmetry))
        score += 0.2 * symmetry
        
        # 位置控制
        center = board.size / 2
        position_score = 0.5
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    dist = abs(x - center) + abs(y - center)
                    position_score += 0.05 * max(0, board.size - dist)
        
        score += 0.2 * min(1.0, position_score / board.size)
        
        return min(1.0, max(0.0, score))
    
    def _compute_english_activation(self, board, player):
        """计算英文层激活度（0∅空）"""
        score = 0.0
        
        # 棋子评估
        own_stones = 0
        opp_stones = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    own_stones += 1
                elif board.board[x][y] == 3 - player:
                    opp_stones += 1
        
        total_stones = max(own_stones + opp_stones, 1)
        score += 0.3 * (own_stones - opp_stones) / total_stones
        
        # 威胁检测
        threat_score = 0.5
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == 3 - player:
                    libs = board.liberties(x, y, 3 - player)
                    if libs <= 2:
                        threat_score += 0.2
        score += 0.2 * min(1.0, threat_score)
        
        # 棋形识别
        shape_score = 0.5
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    own_neighbors = sum(1 for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]
                                      if 0 <= x+dx < board.size and 0 <= y+dy < board.size
                                      and board.board[x+dx][y+dy] == player)
                    if own_neighbors >= 2:
                        shape_score += 0.1
        score += 0.2 * min(1.0, shape_score)
        
        # 位置价值
        center = board.size / 2
        position_score = 0.5
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    dist = abs(x - center) + abs(y - center)
                    position_score += 0.03 * max(0, board.size - dist)
        score += 0.3 * min(1.0, position_score / board.size)
        
        return min(1.0, max(0.0, score))
    
    def _compute_chinese_activation(self, board, player):
        """计算中文层激活度（0∅义）"""
        liuhe_detail = {}
        
        # 六系坐标计算
        qh = 0.5  # 强化系
        zr = 0.5  # 自然系
        jx = 0.5  # 具现系
        bs = 0.5  # 变身系
        sh = 0.5  # 社会系
        td = 0.5  # 天道系
        
        own_stones = 0
        opp_stones = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    own_stones += 1
                elif board.board[x][y] == 3 - player:
                    opp_stones += 1
        
        total = max(own_stones + opp_stones, 1)
        stone_ratio = own_stones / total
        
        # 强化系评估
        qh = 0.4 + 0.3 * stone_ratio
        
        # 自然系评估
        center = board.size / 2
        avg_dist = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    avg_dist += abs(x - center) + abs(y - center)
        avg_dist = avg_dist / max(own_stones, 1)
        zr = 0.5 + 0.3 * (1.0 - avg_dist / max(board.size, 1))
        
        # 具现系评估
        jx = 0.5 + 0.2 * stone_ratio
        
        # 变身系评估
        bs = 0.5 + 0.15 * random.random()
        
        # 社会系评估
        sh = 0.4 + 0.2 * (1.0 - abs(own_stones - opp_stones) / total)
        
        # 天道系评估
        phase = self.current_phase
        phase_map = {'opening': 0.3, 'middle': 0.5, 'ending': 0.7, 'final': 0.9}
        td = phase_map.get(phase, 0.5) + 0.1 * stone_ratio
        
        liuhe_detail = {
            'qh_score': min(1.0, max(0.0, qh)),
            'zr_score': min(1.0, max(0.0, zr)),
            'jx_score': min(1.0, max(0.0, jx)),
            'bs_score': min(1.0, max(0.0, bs)),
            'sh_score': min(1.0, max(0.0, sh)),
            'td_score': min(1.0, max(0.0, td)),
            'dominant': max([
                ('qh', qh), ('zr', zr), ('jx', jx),
                ('bs', bs), ('sh', sh), ('td', td)
            ], key=lambda x: x[1])[0],
        }
        
        # 中文层激活度
        liuhe_avg = (qh + zr + jx + bs + sh + td) / 6
        yi_activation = 0.4 * liuhe_avg + 0.3 * td + 0.3 * sh
        
        return min(1.0, max(0.0, yi_activation)), liuhe_detail
    
    def get_emergence_stats(self):
        """获取涌现统计"""
        emergence_rate = self.emergence_count / max(self.total_evals, 1)
        avg_potential = 0.0
        if self.phase_history:
            avg_potential = sum(h['potential'] for h in self.phase_history) / len(self.phase_history)
        
        by_phase = {}
        for h in self.phase_history:
            p = h['phase']
            if p not in by_phase:
                by_phase[p] = {'count': 0, 'emergent': 0}
            by_phase[p]['count'] += 1
            if h['is_emergent']:
                by_phase[p]['emergent'] += 1
        for p in by_phase:
            by_phase[p]['rate'] = by_phase[p]['emergent'] / max(by_phase[p]['count'], 1)
        
        return {
            'total_evals': self.total_evals,
            'emergence_count': self.emergence_count,
            'emergence_rate': emergence_rate,
            'avg_potential': avg_potential,
            'phase_distribution': by_phase,
            'current_phase': self.current_phase,
            'theory': '定理五十八·三语言涌现定理',
        }


# ============================================================
# 3. 六系物理常数定标
#    定理六十一·棋形=六力投影
# ============================================================

class GoPhysicsCalibration:
    """
    围棋六系物理常数定标
    
    核心命题：围棋的棋形就是围棋的"声调"——
    每一种棋形背后对应一种Fundamental Force和物理常数。
    """
    
    def __init__(self):
        self.calibration_log = []
        self.confirmed_shapes = set()
    
    def analyze_shape(self, board, x, y, player):
        """分析指定位置的棋形，返回六系物理常数值"""
        shape_scores = {}
        
        # 计算邻域棋子分布
        own_neighbors = 0
        opp_neighbors = 0
        empty_neighbors = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                val = board.board[nx][ny]
                if val == player:
                    own_neighbors += 1
                elif val == 3 - player:
                    opp_neighbors += 1
                else:
                    empty_neighbors += 1
        
        # 长连通大度C
        shape_scores['changlian'] = {
            'C': min(1.0, own_neighbors / 3.0),
            'confirmed': own_neighbors >= 3,
            'threshold': 0.8
        }
        
        # 飞/跳势能梯度G
        center = board.size // 2
        dist_to_center = abs(x - center) + abs(y - center)
        shape_scores['feitiao'] = {
            'G': min(1.0, 0.3 + 0.1 * empty_neighbors),
            'confirmed': empty_neighbors >= 2,
            'threshold': 0.3
        }
        
        # 拐/弯曲率κ
        shape_scores['guaiwan'] = {
            'kappa': max(0.0, 1.0 - abs(own_neighbors - opp_neighbors) * 0.3),
            'confirmed': abs(own_neighbors - opp_neighbors) <= 1,
            'threshold': 0.5
        }
        
        # 断/打切分率S
        shape_scores['duanda'] = {
            'S': min(1.0, opp_neighbors / 2.0),
            'confirmed': opp_neighbors >= 2,
            'threshold': 0.5
        }
        
        # 弃子留存率R
        shape_scores['qizi'] = {
            'R': min(1.0, empty_neighbors / 3.0),
            'confirmed': empty_neighbors <= 1,
            'threshold': 0.3
        }
        
        # 协同耦合系数η
        shape_scores['xietong'] = {
            'eta': 1.0 if own_neighbors >= 2 and opp_neighbors <= 1 else 0.5,
            'confirmed': own_neighbors >= 2,
            'threshold': 0.7
        }
        
        for shape_type, data in shape_scores.items():
            if data['confirmed']:
                self.confirmed_shapes.add(shape_type)
        
        self.calibration_log.append({
            'position': (x, y),
            'shapes': shape_scores,
            'timestamp': datetime.now().isoformat()
        })
        
        return shape_scores
    
    def compute_six_force_score(self, board, x, y, player):
        """计算六力综合得分"""
        shape_scores = self.analyze_shape(board, x, y, player)
        total = 0.0
        for key, data in shape_scores.items():
            constant = SIX_FORCE_CONSTANTS.get(key, {})
            min_val = constant.get('value', 0.5)
            # 获取实际值
            actual_val = data.get('C', data.get('G', data.get('kappa', 
                          data.get('S', data.get('R', data.get('eta', 0.5))))))
            total += actual_val * min_val
        return total / max(len(shape_scores), 1)
    
    def get_calibration_report(self):
        """获取定标报告"""
        return {
            'six_forces': SIX_FORCE_CONSTANTS,
            'system_weights': SYSTEM_WEIGHTS_V5,
            'confirmed_shapes': list(self.confirmed_shapes),
            'calibration_count': len(self.calibration_log),
            'theory': '定理六十一·棋形=六力投影',
        }


# ============================================================
# 4. 天道追问引擎
# ============================================================

class TiandaoEngine:
    """
    天道追问引擎——V5核心突破
    
    核心功能：
    1. 循环检测
    2. 劣势判断
    3. 危急触发
    4. 反性计算
    5. 哲学追问
    """
    
    PHILOSOPHICAL_QUESTIONS = [
        "此手是否体现强化系的算力深度？",
        "此手是否体现自然系的演化潜力？",
        "此手是否体现具现系的落子凝结？",
        "此手是否体现变身系的创新变化？",
        "此手是否体现社会系的博弈关系？",
        "此手是否体现天道系的意义追问？",
    ]
    
    def __init__(self):
        self.cycle_detector = []
        self.recorded_moves = []
        self.decision_log = []
        self.tiandao_insights = []
    
    def record_move(self, x, y):
        """记录落子位置"""
        self.recorded_moves.append((x, y))
        if len(self.recorded_moves) > 100:
            self.recorded_moves = self.recorded_moves[-50:]
    
    def detect_cycle(self, board, window_size=8):
        """循环检测"""
        moves = self.recorded_moves[-window_size:]
        if len(moves) < window_size:
            return False
        for i in range(len(moves) - 4):
            if moves[i] == moves[i + 4]:
                return True
        return False
    
    def should_awaken(self, board, score_advantage):
        """判断是否需要觉醒决策"""
        if self.detect_cycle(board):
            return True, "循环检测"
        if score_advantage < TIANDAO_CONFIG['behind_threshold']:
            return True, "劣势追问"
        if score_advantage < TIANDAO_CONFIG['critical_threshold']:
            return True, "危急觉醒"
        return False, ""
    
    def generate_insight(self, board, x, y, player):
        """生成天道追问洞察"""
        phase = board.move_count if hasattr(board, 'move_count') else 20
        
        if phase < 20:
            question = self.PHILOSOPHICAL_QUESTIONS[3]
            answer = "开局阶段，变身系创新优先。此手是否开辟新的变化可能？"
            action = "尝试新棋形"
        elif phase < 60:
            question = self.PHILOSOPHICAL_QUESTIONS[0]
            answer = "中盘阶段，强化系算力主导。此手是否巩固领地？"
            action = "巩固领地"
        else:
            question = self.PHILOSOPHICAL_QUESTIONS[5]
            answer = "后盘阶段，天道系意义追问。此手是否体现全局意义？"
            action = "天道追问"
        
        confidence = 0.6 + random.uniform(-0.1, 0.1)
        
        return {
            'question': question,
            'answer': answer,
            'recommended_action': action,
            'confidence': confidence,
            'position': (x, y),
        }
    
    def get_stats(self):
        """获取天道引擎统计"""
        return {
            'total_insights': len(self.tiandao_insights),
            'recorded_moves': len(self.recorded_moves),
            'theory': '7.5.10.5 V5引擎突破',
        }


# ============================================================
# 5. 统一基因池
# ============================================================

class UnifiedGenePool:
    """
    统一基因池——整合V1+V2+V5+V6+V9全版本基因
    """
    
    def __init__(self):
        self.genes = []
        self.gene_map = {}
        self._init_all_genes()
        self._build_gene_map()
    
    def _init_all_genes(self):
        """初始化所有版本的基因"""
        self._init_v1_genes()
        self._init_v2_genes()
        self._init_v5_genes()
        self._init_v6_genes()
        self._init_v9_genes()
    
    def _init_v1_genes(self):
        """V1基础基因：200个随机DNA片段"""
        for i in range(200):
            pattern = []
            for _ in range(9):
                r = random.random()
                if r < 0.6:
                    pattern.append(0)
                elif r < 0.8:
                    pattern.append(1)
                else:
                    pattern.append(2)
            empty_indices = [j for j, v in enumerate(pattern) if v == 0]
            if not empty_indices:
                empty_indices = [4]
            move_idx = random.choice(empty_indices)
            self.genes.append({
                'id': f'V1-base-{i}',
                'source': 'V1',
                'pattern': pattern,
                'move': (move_idx // 3, move_idx % 3),
                'value': random.uniform(0.5, 1.5),
                'type': 'base',
                'alpha1': random.uniform(0.2, 0.5),
                'alpha2': random.uniform(0.2, 0.5),
                'alpha3': random.uniform(0.2, 0.5),
                'six_system': {'qh': 0.15, 'zr': 0.20, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.17},
            })
    
    def _init_v2_genes(self):
        """V2真实基因：定式+战术组合"""
        opening_setups = [
            {'p': [0, 0, 0, 0, 0, 1, 0, 0, 0], 'm': (2, 1), 'v': 1.2, 'name': '星位小飞挂'},
            {'p': [0, 0, 0, 0, 1, 0, 0, 0, 0], 'm': (1, 1), 'v': 1.1, 'name': '高目'},
            {'p': [0, 0, 0, 0, 0, 0, 0, 1, 0], 'm': (1, 2), 'v': 1.0, 'name': '小目低挂'},
            {'p': [0, 0, 0, 0, 0, 0, 0, 0, 1], 'm': (2, 2), 'v': 0.9, 'name': '三三星'},
            {'p': [1, 0, 0, 0, 0, 0, 0, 0, 0], 'm': (1, 0), 'v': 0.8, 'name': '天元'},
        ]
        for i, setup in enumerate(opening_setups):
            self.genes.append({
                'id': f'V2-opening-{i}', 'source': 'V2', 'pattern': setup['p'],
                'move': setup['m'], 'value': setup['v'], 'type': 'professional_opening',
                'professional_source': setup['name'], 'win_rate': 0.50 + i * 0.02,
                'alpha1': 0.35, 'alpha2': 0.40, 'alpha3': 0.25,
                'six_system': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
            })
        
        tactic_setups = [
            {'p': [0, 2, 0, 2, 0, 1, 0, 0, 0], 'm': (1, 1), 'v': 2.5, 'name': '打吃', 'tactic': 'capture'},
            {'p': [2, 0, 2, 0, 1, 0, 0, 0, 0], 'm': (0, 1), 'v': 1.9, 'name': '断', 'tactic': 'cut'},
            {'p': [1, 0, 1, 0, 0, 0, 0, 0, 0], 'm': (0, 1), 'v': 1.6, 'name': '连接', 'tactic': 'connect'},
            {'p': [0, 0, 0, 0, 1, 0, 0, 2, 0], 'm': (0, 1), 'v': 1.4, 'name': '长气', 'tactic': 'extend'},
            {'p': [0, 2, 0, 2, 0, 2, 0, 1, 0], 'm': (1, 1), 'v': 2.8, 'name': '双叫吃', 'tactic': 'double_threat'},
        ]
        for i, setup in enumerate(tactic_setups):
            self.genes.append({
                'id': f'V2-tactic-{i}', 'source': 'V2', 'pattern': setup['p'],
                'move': setup['m'], 'value': setup['v'], 'type': 'professional_tactic',
                'professional_source': setup['name'], 'tactic': setup['tactic'],
                'success_rate': 0.65 + i * 0.03,
                'alpha1': 0.6, 'alpha2': 0.4, 'alpha3': 0.2,
                'six_system': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
            })
    
    def _init_v5_genes(self):
        """V5天道追问基因"""
        v5_config = [
            {'id': 'V5-tiandao-0', 'type': 'tiandao_inquiry', 'boost': 1.5, 'philosophy': '意义追问'},
            {'id': 'V5-awakening-1', 'type': 'awakening_decision', 'boost': 2.0, 'philosophy': '觉醒破局'},
            {'id': 'V5-cycle-2', 'type': 'cycle_breaker', 'boost': 1.8, 'philosophy': '反循环'},
            {'id': 'V5-creative-3', 'type': 'creative_move', 'boost': 1.6, 'philosophy': '创造性落子'},
        ]
        for cfg in v5_config:
            self.genes.append({
                'id': cfg['id'], 'source': 'V5', 'pattern': [0, 0, 0, 0, 0, 0, 0, 0, 0],
                'move': (1, 1), 'value': 2.0 * cfg['boost'], 'type': cfg['type'],
                'philosophy': cfg['philosophy'], 'weight_boost': cfg['boost'],
                'alpha1': 0.4, 'alpha2': 0.35, 'alpha3': 0.25,
                'six_system': SYSTEM_WEIGHTS_V5,
            })
    
    def _init_v6_genes(self):
        """V6量子基因"""
        quantum_genes = [
            {'p': [0, 0, 0, 0, 0, 0, 0, 0, 1], 'm': (2, 2), 'v': 1.0, 'phase': 0.0},
            {'p': [1, 0, 0, 0, 0, 0, 0, 0, 0], 'm': (0, 0), 'v': 1.0, 'phase': 0.5},
            {'p': [0, 0, 0, 0, 0, 0, 0, 1, 0], 'm': (2, 1), 'v': 0.95, 'phase': 0.2},
            {'p': [0, 2, 0, 2, 0, 1, 0, 0, 0], 'm': (1, 1), 'v': 2.5, 'phase': 0.0},
            {'p': [0, 0, 0, 0, 1, 0, 0, 2, 0], 'm': (0, 1), 'v': 1.8, 'phase': 0.4},
        ]
        for i, qg in enumerate(quantum_genes):
            self.genes.append({
                'id': f'V6-quantum-{i}', 'source': 'V6', 'pattern': qg['p'],
                'move': qg['m'], 'value': qg['v'], 'type': 'quantum_base',
                'phase': qg['phase'], 'alpha1': 0.45, 'alpha2': 0.35, 'alpha3': 0.20,
                'six_system': {'qh': 0.10, 'zr': 0.20, 'jx': 0.20, 'bs': 0.20, 'sh': 0.15, 'td': 0.15},
            })
    
    def _init_v9_genes(self):
        """V9白日梦基因"""
        dream_configs = [
            {'name': '白日梦·星位', 'p': [0, 0, 0, 0, 0, 1, 0, 0, 0], 'm': (2, 1), 'v': 1.3},
            {'name': '白日梦·小目', 'p': [0, 0, 0, 0, 0, 0, 0, 1, 0], 'm': (1, 2), 'v': 1.1},
            {'name': '白日梦·三三中', 'p': [0, 0, 0, 0, 0, 0, 0, 0, 1], 'm': (2, 2), 'v': 1.0},
            {'name': '白日梦·打吃', 'p': [0, 2, 0, 2, 0, 1, 0, 0, 0], 'm': (1, 1), 'v': 2.6},
            {'name': '白日梦·双叫吃', 'p': [0, 2, 0, 2, 0, 2, 0, 1, 0], 'm': (1, 1), 'v': 2.9},
            {'name': '白日梦·连接', 'p': [1, 0, 1, 0, 0, 0, 0, 0, 0], 'm': (0, 1), 'v': 1.7},
        ]
        for i, cfg in enumerate(dream_configs):
            self.genes.append({
                'id': f'V9-dream-{i}', 'source': 'V9', 'pattern': cfg['p'],
                'move': cfg['m'], 'value': cfg['v'], 'type': 'dream_gene',
                'name': cfg['name'], 'divergence': random.uniform(0.3, 0.6),
                'alpha1': 0.35, 'alpha2': 0.35, 'alpha3': 0.30,
                'six_system': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
                'dream_trigger': True,
            })
    
    def _build_gene_map(self):
        """构建基因映射"""
        for gene in self.genes:
            pattern_key = tuple(gene['pattern'])
            if pattern_key not in self.gene_map:
                self.gene_map[pattern_key] = []
            self.gene_map[pattern_key].append(gene)
    
    def find_matches(self, pattern, min_similarity=0.3):
        """查找匹配基因"""
        matches = []
        pattern_tuple = tuple(pattern)
        if pattern_tuple in self.gene_map:
            for gene in self.gene_map[pattern_tuple]:
                gene_copy = gene.copy()
                gene_copy['sim'] = 1.0
                if 'value' not in gene_copy:
                    gene_copy['value'] = 1.0
                matches.append(gene_copy)
        for gene in self.genes:
            sim = self._similarity(gene['pattern'], pattern)
            if sim >= min_similarity:
                gene_copy = gene.copy()
                gene_copy['sim'] = sim
                if 'value' not in gene_copy:
                    gene_copy['value'] = 1.0
                matches.append(gene_copy)
        matches.sort(key=lambda g: g['sim'] * g.get('value', 1.0), reverse=True)
        return matches
    
    def _similarity(self, a, b):
        """计算相似度"""
        matches = sum(1 for x, y in zip(a, b) if x == y and x != -1)
        total = sum(1 for x, y in zip(a, b) if x != -1 and y != -1)
        return matches / max(total, 1)
    
    def dna_crossover(self, gene_a, gene_b, strategy='mixed'):
        """DNA交叉重组"""
        new_pattern = gene_a['pattern'][:]
        va = gene_a.get('value', 1.0)
        vb = gene_b.get('value', 1.0)
        
        if strategy == 'swap':
            new_pattern = gene_b['pattern'][:]
            move = gene_b.get('move', (1, 1))
            value = (va + vb) / 2 * 1.2
        elif strategy == 'mix':
            for i in range(9):
                if random.random() < 0.5:
                    new_pattern[i] = gene_b['pattern'][i]
            empty_idx = [j for j, v in enumerate(new_pattern) if v == 0]
            if not empty_idx:
                empty_idx = [4]
            move_idx = random.choice(empty_idx)
            move = (move_idx // 3, move_idx % 3)
            value = (va + vb) / 2 * 1.1
        elif strategy == 'tactical':
            new_pattern = gene_a['pattern'][:]
            move = gene_b.get('move', (1, 1))
            value = max(va, vb) * 1.3
        else:
            new_pattern = gene_a['pattern'][:]
            move = gene_a.get('move', (1, 1))
            value = (va + vb) / 2
        
        alpha1 = (gene_a.get('alpha1', 0.3) + gene_b.get('alpha1', 0.3)) / 2
        alpha2 = (gene_a.get('alpha2', 0.3) + gene_b.get('alpha2', 0.3)) / 2
        alpha3 = (gene_a.get('alpha3', 0.3) + gene_b.get('alpha3', 0.3)) / 2
        total = alpha1 + alpha2 + alpha3
        alpha1, alpha2, alpha3 = alpha1 / total, alpha2 / total, alpha3 / total
        
        six_system = {}
        sys_a = gene_a.get('six_system', SYSTEM_WEIGHTS_V5)
        sys_b = gene_b.get('six_system', SYSTEM_WEIGHTS_V5)
        for key in sys_a:
            six_system[key] = (sys_a.get(key, 0.15) + sys_b.get(key, 0.15)) / 2
        total_s = sum(six_system.values())
        for key in six_system:
            six_system[key] /= max(total_s, 0.001)
        
        return {
            'id': f'U-dream-{datetime.now().strftime("%H%M%S")}-{random.randint(100, 999)}',
            'source': 'unified_crossover',
            'pattern': new_pattern, 'move': move, 'value': value,
            'type': 'dna_recombined',
            'alpha1': alpha1, 'alpha2': alpha2, 'alpha3': alpha3,
            'six_system': six_system,
            'parent_genes': [gene_a['id'], gene_b['id']], 'strategy': strategy,
        }
    
    def quantum_entangle(self, genes_list):
        """量子纠缠"""
        if len(genes_list) < 2:
            return genes_list[0] if genes_list else None
        
        phases = [g.get('phase', 0) for g in genes_list]
        relative_phases = [p - phases[0] for p in phases[1:]]
        all_states = []
        for gene in genes_list:
            if 'states' in gene:
                all_states.extend(gene['states'])
            else:
                all_states.append({
                    'move': gene.get('move', (1, 1)),
                    'prob': 0.5, 'value': gene.get('value', 1.0),
                    'phase': gene.get('phase', 0),
                })
        
        state_map = {}
        for state in all_states:
            key = state['move']
            current_phase = state.get('phase', 0)
            if key in state_map:
                existing = state_map[key]
                phase_diff = current_phase - existing.get('phase', 0)
                interference = math.cos(phase_diff)
                new_prob = (existing['prob'] + state['prob']) / 2
                new_prob *= (1 + 0.5 * interference)
                new_value = (existing['value'] + state['value']) / 2
                new_value *= (1 + 0.3 * interference)
                state_map[key] = {
                    'move': key,
                    'prob': min(1.0, new_prob),
                    'value': max(0.1, new_value),
                    'phase': (current_phase + existing.get('phase', 0)) / 2,
                    'sources': existing.get('sources', 1) + 1,
                }
            else:
                state_map[key] = {
                    **state,
                    'phase': current_phase + random.choice(relative_phases) * 0.3,
                    'sources': 1,
                }
        
        merged_states = sorted(
            state_map.values(),
            key=lambda s: s['prob'] * s['value'],
            reverse=True
        )[:5]
        total_prob = sum(s['prob'] for s in merged_states)
        for state in merged_states:
            state['prob'] /= max(total_prob, 0.001)
        
        entanglement_entropy = 0.0
        for state in merged_states:
            p = state['prob']
            if p > 0:
                entanglement_entropy -= p * math.log2(p)
        
        emergence = sum(s['prob'] * s['value'] for s in merged_states)
        
        return {
            'id': f'U-entangled-{datetime.now().strftime("%H%M%S")}-{random.randint(100, 999)}',
            'source': 'quantum_entanglement',
            'states': merged_states,
            'emergence': emergence,
            'value': emergence,
            'entanglement_entropy': entanglement_entropy,
            'phase_shifts': relative_phases,
            'num_qubits': len(genes_list),
            'type': 'quantum_entangled',
            'pattern': genes_list[0]['pattern'][:],
            'move': merged_states[0]['move'] if merged_states else (1, 1),
            'alpha1': sum(g.get('alpha1', 0.3) for g in genes_list) / len(genes_list),
            'alpha2': sum(g.get('alpha2', 0.3) for g in genes_list) / len(genes_list),
            'alpha3': sum(g.get('alpha3', 0.3) for g in genes_list) / len(genes_list),
            'six_system': {
                'qh': sum(g.get('six_system', {}).get('qh', 0.12) for g in genes_list) / len(genes_list),
                'zr': sum(g.get('six_system', {}).get('zr', 0.25) for g in genes_list) / len(genes_list),
                'jx': sum(g.get('six_system', {}).get('jx', 0.18) for g in genes_list) / len(genes_list),
                'bs': sum(g.get('six_system', {}).get('bs', 0.15) for g in genes_list) / len(genes_list),
                'sh': sum(g.get('six_system', {}).get('sh', 0.15) for g in genes_list) / len(genes_list),
                'td': sum(g.get('six_system', {}).get('td', 0.15) for g in genes_list) / len(genes_list),
            },
            'parent_genes': [g.get('id', 'unknown') for g in genes_list],
        }
    
    def get_pool_stats(self):
        """获取基因池统计"""
        types = Counter(g.get('type', 'unknown') for g in self.genes)
        sources = Counter(g.get('source', 'unknown') for g in self.genes)
        return {
            'total_genes': len(self.genes),
            'type_distribution': dict(types.most_common(10)),
            'source_distribution': dict(sources.most_common(10)),
            'v1_genes': sum(1 for g in self.genes if g.get('source') == 'V1'),
            'v2_genes': sum(1 for g in self.genes if g.get('source') == 'V2'),
            'v5_genes': sum(1 for g in self.genes if g.get('source') == 'V5'),
            'v6_genes': sum(1 for g in self.genes if g.get('source') == 'V6'),
            'v9_genes': sum(1 for g in self.genes if g.get('source') == 'V9'),
        }


# ============================================================
# 6. 联网学习连接器
# ============================================================

class CloudConnector:
    """联网学习连接器——模拟连接在线棋谱数据库"""
    
    def __init__(self):
        self.connected = False
        self.gene_database = []
        self.stats = {'games_fetched': 0, 'genes_extracted': 0}
    
    def connect(self):
        """连接棋谱云数据库"""
        self.connected = True
        return True
    
    def fetch_games(self, count=15):
        """拉取棋谱数据"""
        if not self.connected:
            self.connect()
        
        new_genes = []
        for i in range(count):
            source_type = random.choices(
                ['fuseki', 'tactic', 'pattern'], weights=[0.4, 0.35, 0.25]
            )[0]
            gene = self._generate_gene(source_type, i)
            new_genes.append(gene)
        
        self.stats['games_fetched'] += count
        self.stats['genes_extracted'] += len(new_genes)
        self.gene_database.extend(new_genes)
        return new_genes
    
    def _generate_gene(self, source_type, idx):
        """生成基因数据"""
        if source_type == 'fuseki':
            patterns = [
                [0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1],
            ]
            names = ['星位小飞挂', '高目', '小目低挂', '三三星']
            pattern = random.choice(patterns)
            name = random.choice(names)
            move = random.choice([(2, 1), (1, 1), (1, 2), (2, 2)])
            return {
                'id': f'CLOUD-{datetime.now().strftime("%H%M")}-{idx:04d}',
                'source': 'cloud_fuseki', 'pattern': pattern, 'move': move,
                'value': random.uniform(0.8, 1.4), 'type': 'cloud_opening',
                'professional_source': name,
                'win_rate': random.uniform(0.45, 0.58),
                'alpha1': 0.35, 'alpha2': 0.35, 'alpha3': 0.30,
                'six_system': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
            }
        elif source_type == 'tactic':
            tactics = [
                {'name': '打吃', 'pattern': [0, 2, 0, 2, 0, 1, 0, 0, 0], 'value': 2.5},
                {'name': '断', 'pattern': [2, 0, 2, 0, 1, 0, 0, 0, 0], 'value': 1.9},
                {'name': '连接', 'pattern': [1, 0, 1, 0, 0, 0, 0, 0, 0], 'value': 1.6},
                {'name': '双叫吃', 'pattern': [0, 2, 0, 2, 0, 2, 0, 1, 0], 'value': 2.8},
            ]
            tactic = random.choice(tactics)
            return {
                'id': f'CLOUD-{datetime.now().strftime("%H%M")}-{idx:04d}',
                'source': 'cloud_tactic', 'pattern': tactic['pattern'],
                'move': (1, 1), 'value': tactic['value'], 'type': 'cloud_tactic',
                'professional_source': tactic['name'],
                'win_rate': random.uniform(0.55, 0.72),
                'alpha1': 0.5, 'alpha2': 0.35, 'alpha3': 0.15,
                'six_system': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
            }
        else:
            patterns = [
                {'name': '棋形A', 'pattern': [0, 1, 0, 0, 1, 0, 0, 0, 0]},
                {'name': '棋形B', 'pattern': [0, 0, 1, 0, 0, 1, 0, 0, 0]},
                {'name': '棋形C', 'pattern': [0, 0, 0, 1, 0, 0, 1, 0, 0]},
            ]
            p = random.choice(patterns)
            return {
                'id': f'CLOUD-{datetime.now().strftime("%H%M")}-{idx:04d}',
                'source': 'cloud_pattern', 'pattern': p['pattern'],
                'move': (random.randint(0, 2), random.randint(0, 2)),
                'value': random.uniform(1.0, 2.0), 'type': 'cloud_pattern',
                'professional_source': p['name'],
                'win_rate': random.uniform(0.40, 0.60),
                'alpha1': 0.4, 'alpha2': 0.4, 'alpha3': 0.2,
                'six_system': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
            }
    
    def get_stats(self):
        """获取统计"""
        return self.stats


# ============================================================
# 7. 统一决策引擎（优化版）
# ============================================================

class UnifiedDecisionEngine:
    """
    统一决策引擎——优化版
    
    核心改进：
    1. 简化评估函数，提高决策质量
    2. 增强全局评估能力
    3. 优化六系协同决策权重
    4. 增加基于领地的评估维度
    """
    
    def __init__(self, gene_pool, cloud, tiandao, physics, three_lang):
        self.gene_pool = gene_pool
        self.cloud = cloud
        self.tiandao = tiandao
        self.physics = physics
        self.three_lang = three_lang
        self.decision_log = []
        self.dream_count = 0
        self.total_moves = 0
        self.emergence_decisions = 0
    
    def decide_move(self, board, player):
        """决策落子"""
        self.total_moves += 1
        empty = board.empty()
        if not empty:
            return None
        
        # 计算所有候选点的得分
        candidates = self._build_candidates(board, player)
        
        if candidates:
            best = candidates[0]
            move = best['move']
            
            # 记录决策信息
            move_info = {
                'move': move,
                'type': 'unified_decision',
                'move_count': self.total_moves,
                'score': best.get('score', 0),
                'phase': best.get('phase', ''),
                'dominant_system': best.get('dominant_system', ''),
            }
            
            if best.get('is_emergent', False):
                self.emergence_decisions += 1
                move_info['is_emergent'] = True
            
            self.decision_log.append(move_info)
            self.tiandao.record_move(*move)
            return move
        
        # 兜底策略
        return self._fallback_move(board, player)
    
    def _build_candidates(self, board, player):
        """构建候选点列表"""
        candidates = []
        empty = board.empty()
        
        for x, y in empty:
            score_detail = self._evaluate_candidate(board, x, y, player)
            candidates.append({
                'move': (x, y),
                'score': score_detail['total_score'],
                'phase': score_detail['phase'],
                'dominant_system': score_detail['dominant_system'],
                'is_emergent': score_detail.get('is_emergent', False),
                'details': score_detail,
            })
        
        candidates.sort(key=lambda c: c['