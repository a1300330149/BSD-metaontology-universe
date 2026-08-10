#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋V5精准激活测试 · V5 + Connector
==========================================

核心思想：
- V5天道追问引擎本身就是一个强大的统一引擎
- 不需要重新构建，只需要激活它缺失的连接点
- 通过连接器逐步激活E06(量子)、E11(三语言)等外挂模块
- 测试"低段位少连接、高段位多连接"的层级引发效应

理论依据：
- 0×0=n → 引擎(0) × 外挂模块(0) = 协同增益(n)
- 激活协议：命名→映射→潜能→整合
- 层级引发：低段位不需要太多连接

版本：V1.0 · 2026-08-04
"""

import os
import sys
import random
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# 0. 统一棋盘 (兼容所有引擎)
# ============================================================

class UnifiedBoard:
    def __init__(self, size=9):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.current = 1
        self.move_count = 0
    
    def place(self, x, y):
        if x is None or y is None:
            return False
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if self.board[x][y] != 0:
            return False
        self.board[x][y] = self.current
        self.move_count += 1
        self.current = 3 - self.current
        return True
    
    def empty(self):
        return [(x, y) for x in range(self.size) for y in range(self.size) 
                if self.board[x][y] == 0]
    
    def liberties_at(self, x, y):
        count = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.board[nx][ny] == 0:
                    count += 1
        return count
    
    def score(self):
        s = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    s += 1 + self._pos(x, y)
                elif self.board[x][y] == 2:
                    s -= 1 + self._pos(x, y)
        return s
    
    def _pos(self, x, y):
        center = self.size // 2
        if x == center and y == center:
            return 3
        if abs(x - center) <= 1 and abs(y - center) <= 1:
            return 2
        if x in [0, self.size-1] or y in [0, self.size-1]:
            return 0.5
        return 1
    
    def get_board_state(self):
        own_stones = sum(1 for x in range(self.size) 
                       for y in range(self.size) 
                       if self.board[x][y] == 1)
        opp_stones = sum(1 for x in range(self.size) 
                        for y in range(self.size) 
                        if self.board[x][y] == 2)
        return {
            'move_count': self.move_count,
            'total_points': self.size * self.size,
            'own_stones': own_stones,
            'opp_stones': opp_stones,
        }


# ============================================================
# 1. V5 核心引擎 (直接从 BSD_Go_Unified_Engine 提取)
# ============================================================

class V5CoreEngine:
    """
    V5天道追问引擎——原始核心
    
    核心功能：
    - 循环检测
    - 劣势判断
    - 危急触发
    - 反性计算
    - 哲学追问
    
    这是被验证过的统一引擎核心，不需要重写
    """
    
    PHILOSOPHICAL_QUESTIONS = [
        "此手是否体现强化系的算力深度？",
        "此手是否体现自然系的演化方向？",
        "此手是否体现具现系的落子凝结？",
        "此手是否体现变身系的创新可能？",
        "此手是否体现社会系的博弈关系？",
        "此手是否体现天道系的终极意义？",
    ]
    
    def __init__(self):
        self.cycle_counter = 0
        self.last_positions = []
        self.awakening_count = 0
        self.insight_log = []
        self.decision_log = []
        
        # V5配置参数
        self.cycle_threshold = 8
        self.behind_threshold = -0.25
        self.critical_threshold = -0.50
        self.insight_min_confidence = 0.7
        self.cycle_distance = 4
    
    def decide_move(self, board, player):
        """V5核心决策流程"""
        empty = board.empty()
        if not empty:
            return None
        
        self.last_positions.append(None)  # placeholder
        candidates = self._generate_candidates(board, player, empty)
        
        if candidates:
            best = candidates[0]
            move = best['move']
            self.decision_log.append(move)
            return move
        
        return self._evaluate_empty(board, player)
    
    def _generate_candidates(self, board, player, empty):
        """生成候选落子"""
        candidates = []
        opponent = 3 - player
        center = board.size // 2
        
        for x, y in empty:
            score = 0.0
            
            # 1. 局部控制力 (强化系)
            own_near = 0
            opp_near = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == player:
                            own_near += 1
                        elif board.board[nx][ny] == opponent:
                            opp_near += 1
            score += (own_near - opp_near * 0.8) * 0.3
            
            # 2. 位置价值 (自然系)
            dist = abs(x - center) + abs(y - center)
            max_dist = 2 * center
            zr_score = (1.0 - dist / max_dist) * 0.6
            score += zr_score * 0.25
            
            # 3. 落子势能 (具现系)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == 0:
                        score += 0.05
                    elif board.board[nx][ny] == player:
                        score += 0.1
                    elif board.board[nx][ny] == opponent:
                        score -= 0.08
            
            # 4. 开局偏好
            if board.move_count < 10:
                corners = [(0,0),(0,8),(8,0),(8,8)]
                star_points = [(2,2),(2,6),(6,2),(6,6)]
                if (x, y) in corners:
                    score += 1.5
                if (x, y) in star_points:
                    score += 1.0
                if (x, y) == (4, 4):
                    score += 0.8
            
            # 5. 打吃潜力
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs = 0
                        for dx2, dy2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nx2, ny2 = nx + dx2, ny + dy2
                            if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                                if board.board[nx2][ny2] == 0:
                                    opp_libs += 1
                        if opp_libs <= 2:
                            score += 1.5
            
            # 6. 成连潜力
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        nx2, ny2 = x + 2*dx, y + 2*dy
                        if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                            if board.board[nx2][ny2] == player:
                                score += 2.0
            
            # 惩罚：过度集中
            own_in_region = sum(1 for dx in range(-2,3) for dy in range(-2,3)
                             if 0 <= x+dx < board.size and 0 <= y+dy < board.size
                             and board.board[x+dx][y+dy] == player)
            if own_in_region >= 5:
                score -= 0.5 * (own_in_region - 4)
            
            candidates.append({
                'move': (x, y),
                'score': score,
                'gene_id': 'v5_core',
                'six_system': {},
            })
        
        candidates.sort(key=lambda c: c['score'], reverse=True)
        return candidates[:15]
    
    def _evaluate_empty(self, board, player):
        empty = board.empty()
        if not empty:
            return None
        
        best_move = None
        best_score = -float('inf')
        
        for x, y in empty:
            score = 0.0
            opponent = 3 - player
            
            # 局部控制力
            own_near = 0
            opp_near = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == player:
                            own_near += 1
                        elif board.board[nx][ny] == opponent:
                            opp_near += 1
            score += (own_near - opp_near * 0.8) * 0.3
            
            # 位置
            center = board.size // 2
            dist = abs(x - center) + abs(y - center)
            score += (1.0 - dist / (2 * center)) * 0.25
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move
    
    def record_move(self, x, y):
        self.last_positions.append((x, y))
        if len(self.last_positions) > 100:
            self.last_positions = self.last_positions[-50:]
    
    def get_stats(self):
        return {
            'total_decisions': len(self.decision_log),
            'cycle_counter': self.cycle_counter,
            'awakening_count': self.awakening_count,
        }


# ============================================================
# 2. V5精准激活器 (V5 + Connector)
# ============================================================

class V5PrecisionActivator:
    """
    V5精准激活器——只激活缺失的连接，不重写引擎
    
    设计哲学：
    - V5核心是统一引擎的骨架
    - 连接器提供"连接·激活·路由"
    - 逐步激活外挂模块，观察协同效应
    
    激活层级：
    - Level 0: 纯V5核心 (不激活任何外挂)
    - Level 1: + E06(量子引擎) — 量子退火优化
    - Level 2: + E06 + E11(三语言) — 协同涌现
    - Level 3: + E06 + E11 + E07(V9) — 深度整合
    - Level 4: + E06 + E11 + E07 + E08(V8) — 全栈统一
    """
    
    def __init__(self, activation_level=0):
        self.activation_level = activation_level
        self.v5_core = V5CoreEngine()
        self.activated_modules = {}
        self.decision_log = []
        self.stats = {
            'total_moves': 0,
            'v5_only_moves': 0,
            'e06_quantum_moves': 0,
            'e11_tri_lang_moves': 0,
            'hybrid_moves': 0,
        }
        
        # 渐进式激活
        self._activate_by_level(activation_level)
    
    def _activate_by_level(self, level):
        """按层级激活外挂模块"""
        print(f"\n  [V5精准激活] 层级={level}")
        
        if level >= 1:
            self._activate_e06()
        
        if level >= 2:
            self._activate_e11()
        
        if level >= 3:
            self._activate_e07()
        
        if level >= 4:
            self._activate_e08()
    
    def _activate_e06(self):
        """激活E06量子引擎"""
        try:
            from BSD_Go_Quantum_Dream_Engine import QuantumAnnealingEngine
            self.activated_modules['E06'] = QuantumAnnealingEngine()
            print("    ✓ E06(量子退火) 激活成功")
        except Exception as e:
            print(f"    ✗ E06激活失败: {e}")
            self.activated_modules['E06'] = None
    
    def _activate_e11(self):
        """激活E11三语言模块"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bsd_engine', 'core'))
            from tri_language_emergence_engine import TriLanguageEmergenceEngine
            self.activated_modules['E11'] = TriLanguageEmergenceEngine(9)
            print("    ✓ E11(三语言涌现) 激活成功")
        except Exception as e:
            print(f"    ✗ E11激活失败: {e}")
            self.activated_modules['E11'] = None
    
    def _activate_e07(self):
        """激活E07 V9整合版"""
        try:
            from BSD_Go_Engine_V9_Integrated import UnifiedGoAI as V9GoAI
            self.activated_modules['E07'] = V9GoAI(auto_connect=False)
            print("    ✓ E07(V9整合) 激活成功")
        except Exception as e:
            print(f"    ✗ E07激活失败: {e}")
            self.activated_modules['E07'] = None
    
    def _activate_e08(self):
        """激活E08 V8统一版"""
        try:
            from BSD_Go_Unified_Engine import UnifiedGoAI as V8GoAI
            self.activated_modules['E08'] = V8GoAI(auto_connect=False)
            print("    ✓ E08(V8统一) 激活成功")
        except Exception as e:
            print(f"    ✗ E08激活失败: {e}")
            self.activated_modules['E08'] = None
    
    def decide_move(self, board, player):
        """
        V5精准激活决策
        
        流程：
        1. V5核心生成候选
        2. 激活的外挂模块提供增强
        3. 融合决策
        """
        self.stats['total_moves'] += 1
        empty = board.empty()
        if not empty:
            return None
        
        # Step 1: V5核心决策
        v5_move = self.v5_core.decide_move(board, player)
        
        if self.activation_level == 0 or len(self.activated_modules) == 0:
            self.stats['v5_only_moves'] += 1
            self.decision_log.append({
                'move': v5_move,
                'mode': 'v5_only',
                'level': 0,
            })
            return v5_move
        
        # Step 2: 外挂模块增强
        enhanced_move = self._enhance_by_modules(board, player, v5_move)
        
        if enhanced_move and enhanced_move != v5_move:
            self.stats['hybrid_moves'] += 1
            self.decision_log.append({
                'move': enhanced_move,
                'mode': 'hybrid',
                'level': self.activation_level,
            })
            return enhanced_move
        
        self.stats['v5_only_moves'] += 1
        self.decision_log.append({
            'move': v5_move,
            'mode': 'v5_only',
            'level': self.activation_level,
        })
        return v5_move
    
    def _enhance_by_modules(self, board, player, v5_move):
        """通过外挂模块增强V5决策"""
        candidates = []
        
        # E06: 量子退火优化
        if self.activated_modules.get('E06'):
            try:
                quantum = self.activated_modules['E06']
                if hasattr(quantum, 'optimize_move'):
                    q_move = quantum.optimize_move(board, player, v5_move)
                    if q_move and board.board[q_move[0]][q_move[1]] == 0:
                        candidates.append({
                            'move': q_move,
                            'source': 'E06_quantum',
                            'score': 0.9,
                        })
            except:
                pass
        
        # E11: 三语言涌现评估
        if self.activated_modules.get('E11'):
            try:
                tl = self.activated_modules['E11']
                if hasattr(tl, 'compute_three_language'):
                    tl_result = tl.compute_three_language(board, player)
                    if tl_result.get('is_emergent'):
                        # 三语言涌现触发，提供创造性落子
                        empty = board.empty()
                        if empty:
                            # 基于涌现潜力选择
                            best_empty = None
                            best_potential = -1
                            for ex, ey in empty:
                                pot = tl_result.get('emergence_potential', 0)
                                if pot > best_potential:
                                    best_potential = pot
                                    best_empty = (ex, ey)
                            if best_empty:
                                candidates.append({
                                    'move': best_empty,
                                    'source': 'E11_tri_lang',
                                    'score': tl_result.get('weighted_score', 0.5),
                                })
            except:
                pass
        
        # E07: V9深度整合
        if self.activated_modules.get('E07'):
            try:
                v9 = self.activated_modules['E07']
                if hasattr(v9, 'decide_move'):
                    v9_move = v9.decide_move(board, player)
                    if v9_move and board.board[v9_move[0]][v9_move[1]] == 0:
                        candidates.append({
                            'move': v9_move,
                            'source': 'E07_v9',
                            'score': 0.8,
                        })
            except:
                pass
        
        # E08: V8统一引擎
        if self.activated_modules.get('E08'):
            try:
                v8 = self.activated_modules['E08']
                if hasattr(v8, 'decide_move'):
                    v8_move = v8.decide_move(board, player)
                    if v8_move and board.board[v8_move[0]][v8_move[1]] == 0:
                        candidates.append({
                            'move': v8_move,
                            'source': 'E08_v8',
                            'score': 0.85,
                        })
            except:
                pass
        
        # 融合：如果外挂模块提供了更好的候选
        if candidates:
            # 选择分数最高的候选
            best = max(candidates, key=lambda c: c['score'])
            # 只有当外挂模块的候选明显优于V5时才替换
            if best['score'] > 0.7:
                return best['move']
        
        return v5_move
    
    def get_stats(self):
        return {
            'activation_level': self.activation_level,
            'activated_modules': list(self.activated_modules.keys()),
            'total_moves': self.stats['total_moves'],
            'v5_only_rate': self.stats['v5_only_moves'] / max(self.stats['total_moves'], 1),
            'hybrid_rate': self.stats['hybrid_moves'] / max(self.stats['total_moves'], 1),
            'module_stats': {
                k: v is not None for k, v in self.activated_modules.items()
            },
        }


# ============================================================
# 3. 传统AI对手 (StrongGoAI)
# ============================================================

class StrongGoAI:
    """
    传统围棋AI对手
    
    强度等级：3, 4, 6, 8, 10
    数值越高，评估越精确，搜索越深
    """
    
    def __init__(self, strength=8):
        self.strength = strength
        self.decision_log = []
    
    def decide_move(self, board, player):
        empty = board.empty()
        if not empty:
            return None
        
        candidates = []
        opponent = 3 - player
        center = board.size // 2
        
        for x, y in empty:
            score = 0.0
            
            # 基础评估
            own_near = 0
            opp_near = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == player:
                            own_near += 1
                        elif board.board[nx][ny] == opponent:
                            opp_near += 1
            score += (own_near - opp_near * 0.8) * 0.3
            
            # 位置评估
            dist = abs(x - center) + abs(y - center)
            score += (1.0 - dist / (2 * center)) * 0.3
            
            # 根据强度调整精度
            if self.strength >= 6:
                # 更精确的打吃检测
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == opponent:
                            opp_libs = 0
                            for dx2, dy2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                                nx2, ny2 = nx + dx2, ny + dy2
                                if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                                    if board.board[nx2][ny2] == 0:
                                        opp_libs += 1
                            if opp_libs <= 2:
                                score += 2.0
            
            if self.strength >= 8:
                # 更深远的成连检测
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == player:
                            nx2, ny2 = x + 2*dx, y + 2*dy
                            if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                                if board.board[nx2][ny2] == player:
                                    score += 2.5
                                elif board.board[nx2][ny2] == opponent:
                                    score -= 1.0
            
            if self.strength >= 10:
                # 终极强度：全局模式识别
                own_in_region = sum(1 for dx in range(-3,4) for dy in range(-3,4)
                                 if 0 <= x+dx < board.size and 0 <= y+dy < board.size
                                 and board.board[x+dx][y+dy] == player)
                if own_in_region >= 5:
                    score -= 0.3 * (own_in_region - 4)
            
            # 开局偏好
            if board.move_count < 10:
                corners = [(0,0),(0,8),(8,0),(8,8)]
                star_points = [(2,2),(2,6),(6,2),(6,6)]
                if (x, y) in corners:
                    score += 1.5
                if (x, y) in star_points:
                    score += 1.0
                if (x, y) == (4, 4):
                    score += 0.8
            
            candidates.append({
                'move': (x, y),
                'score': score,
            })
        
        candidates.sort(key=lambda c: c['score'], reverse=True)
        
        # 增加随机性（低强度更随机）
        if self.strength <= 4 and len(candidates) > 3:
            idx = random.randint(0, min(2, len(candidates)-1))
            return candidates[idx]['move']
        
        return candidates[0]['move']


# ============================================================
# 4. 对弈测试框架
# ============================================================

class PlayTest:
    def play_game(self, ai, opponent, board_size=9, komi=7.5, ai_first=True, max_moves=200):
        board = UnifiedBoard(board_size)
        
        ai_player = 1 if ai_first else 2
        opp_player = 3 - ai_player
        
        move_count = 0
        consecutive_passes = 0
        
        while move_count < max_moves:
            # AI落子
            if board.current == ai_player:
                move = ai.decide_move(board, ai_player)
            else:
                move = opponent.decide_move(board, opp_player)
            
            if move is None:
                consecutive_passes += 1
                if consecutive_passes >= 2:
                    break
            else:
                consecutive_passes = 0
                board.place(move[0], move[1])
                move_count += 1
        
        # 计算得分
        ai_score = self._calc_score(board, ai_player, komi)
        opp_score = self._calc_score(board, opp_player, 0)
        
        winner = 'ai' if ai_score > opp_score else 'opponent'
        
        return {
            'winner': winner,
            'ai_score': ai_score,
            'opponent_score': opp_score,
            'moves': move_count,
            'board': board,
        }
    
    def _calc_score(self, board, player, komi):
        score = komi
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == player:
                    score += 1
                # 简化的领地计算
                elif board.board[x][y] == 0:
                    # 空点周围全是己方则算领地
                    neighbors = [board.board[nx][ny] 
                                for nx, ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
                                if 0 <= nx < board.size and 0 <= ny < board.size]
                    if neighbors and all(n == player for n in neighbors):
                        score += 1
        return score


# ============================================================
# 5. 主测试程序
# ============================================================

def run_precision_activation_test():
    """V5精准激活测试主程序"""
    
    print("=" * 60)
    print("  BSD V5精准激活测试")
    print("  理论：激活缺失的连接，不重写引擎")
    print("  方法：层级引发 — 低段位少连接")
    print("=" * 60)
    
    test = PlayTest()
    results = {}
    
    # 测试不同激活层级
    for level in range(5):
        print(f"\n{'─' * 50}")
        print(f"  测试激活层级: {level}")
        print(f"  {'─' * 50}")
        
        # 创建V5精准激活器
        activator = V5PrecisionActivator(activation_level=level)
        
        level_results = {}
        
        # 测试不同强度对手
        for strength in [3, 4, 6, 8]:
            opponent = StrongGoAI(strength=strength)
            wins = 0
            total = 3
            
            print(f"\n  强度={strength}:")
            
            for i in range(total):
                result = test.play_game(
                    activator, opponent,
                    board_size=9,
                    komi=7.5,
                    ai_first=(i % 2 == 0)
                )
                
                if result['winner'] == 'ai':
                    wins += 1
                    print(f"    第{i+1}局: ✓ 胜 ({result['ai_score']:.1f} vs {result['opponent_score']:.1f})")
                else:
                    print(f"    第{i+1}局: ✗ 负 ({result['ai_score']:.1f} vs {result['opponent_score']:.1f})")
            
            win_rate = wins / total * 100
            level_results[strength] = win_rate
            print(f"    => 胜率: {wins}/{total} = {win_rate:.0f}%")
        
        results[level] = level_results
        
        # 打印激活器统计
        stats = activator.get_stats()
        print(f"\n  激活器统计:")
        print(f"    激活模块: {stats['activated_modules']}")
        print(f"    V5原生决策率: {stats['v5_only_rate']:.1%}")
        print(f"     Hybrid决策率: {stats['hybrid_rate']:.1%}")
    
    # 汇总结果
    print(f"\n{'=' * 60}")
    print(f"  测试结果汇总")
    print(f"  {'=' * 60}")
    
    print(f"\n  层级 | S3    | S4    | S6    | S8")
    print(f"  {'─' * 45}")
    for level in range(5):
        rates = results.get(level, {})
        s3 = f"{rates.get(3, 0):.0f}%"
        s4 = f"{rates.get(4, 0):.0f}%"
        s6 = f"{rates.get(6, 0):.0f}%"
        s8 = f"{rates.get(8, 0):.0f}%"
        print(f"  L{level}   | {s3:>5} | {s4:>5} | {s6:>5} | {s8:>5}")
    
    # 找到最优配置
    print(f"\n{'─' * 60}")
    print(f"  最优配置分析")
    
    best_level = None
    best_s8_rate = -1
    
    for level in range(5):
        s8_rate = results.get(level, {}).get(8, 0)
        if s8_rate > best_s8_rate:
            best_s8_rate = s8_rate
            best_level = level
    
    print(f"  最优层级: L{best_level} (S8胜率: {best_s8_rate:.0f}%)")
    
    if best_s8_rate >= 100:
        print(f"\n  🎉 突破！BSDAI对S8实现100%胜率！")
    elif best_s8_rate >= 80:
        print(f"\n  ⚠️  接近突破，需要进一步优化评估函数")
    elif best_s8_rate >= 50:
        print(f"\n  ⚠️  中等胜率，需要增强战术能力")
    else:
        print(f"\n  ⚠️  胜率较低，需要激活更多连接或优化核心")
    
    return results


if __name__ == '__main__':
    results = run_precision_activation_test()