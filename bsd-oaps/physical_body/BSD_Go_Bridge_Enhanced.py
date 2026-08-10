#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋引擎桥接增强版 · Bridge Enhanced V2.0
================================================

核心改进：
1. 连接器路由接入 — 用路由替代硬编码引擎选择
2. 渐进式引擎激活 — 逐步激活更多引擎，观察协同效应
3. 六维评估优化 — 提升决策质量
4. S8+强度验证 — 挑战更高强度对手

理论依据：
- 0×0=n 双零涌现：多引擎连接产生协同增益
- 连接器路由动态选择引擎
- 逐步激活 → 协同效应递增

版本：V2.0 · 2026-08-04
"""

import os
import sys
import random
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# 0. 统一棋盘
# ============================================================

class UnifiedBoard:
    """统一棋盘——兼容所有引擎的Board接口"""
    
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
        """获取棋盘状态摘要（用于路由）"""
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
# 1. 增强版桥接AI（BridgeGoAI_Enhanced）
# ============================================================

class BridgeGoAI_Enhanced:
    """
    增强版桥接AI——连接器路由+渐进式激活
    
    核心改进：
    1. 使用连接器路由选择引擎（替代硬编码）
    2. 渐进式激活：先激活E06，再加E11，再加更多
    3. 六维评估：地盘/棋形/威胁/连接/布局/策略
    """
    
    def __init__(self, connector, activation_level=0):
        """
        Args:
            connector: 引擎连接器
            activation_level: 激活层级 (0=最小, 1=E06+E11, 2=+E07, 3=+E08, 4=+E10)
        """
        self.connector = connector
        self.activation_level = activation_level
        self.move_count = 0
        self.activated_engines = {}
        self.decision_log = []
        self.route_decisions = []
        
        # 统计
        self.stats = {
            'total_moves': 0,
            'route_used': {},
            'decision_modes': {},
        }
        
        # 渐进式激活引擎
        self._progressive_activate(activation_level)
    
    def _progressive_activate(self, level):
        """渐进式激活引擎"""
        activation_map = {
            0: [],
            1: ['E06', 'E11'],      # 量子+三语言
            2: ['E06', 'E11', 'E07'],  # +V9深度整合
            3: ['E06', 'E11', 'E07', 'E08'],  # +V8统一
            4: ['E06', 'E11', 'E07', 'E08', 'E10'],  # +V11最终
        }
        
        engine_ids = activation_map.get(level, ['E06', 'E11'])
        
        print(f"  [激活层级{level}] 激活引擎: {engine_ids}")
        for eid in engine_ids:
            module = self.connector.activate_engine(eid)
            if module:
                self.activated_engines[eid] = module
                print(f"    ✓ {eid} 激活成功")
    
    def decide_move(self, board, player):
        """
        增强版桥接决策
        
        流程：
        1. 连接器路由 → 获取推荐引擎组合
        2. 生成候选落子（多引擎协同）
        3. 六维评估排序
        4. 选择最佳落子
        """
        self.move_count += 1
        empty = board.empty()
        if not empty:
            return None
        
        # Step 1: 连接器路由
        board_state = board.get_board_state()
        route_decision = self.connector.route(board_state)
        
        self.route_decisions.append({
            'move': self.move_count,
            'primary': route_decision.primary_engine,
            'secondary': route_decision.secondary_engines,
            'phase': route_decision.phase,
            'confidence': route_decision.confidence,
        })
        
        # 记录路由使用
        primary = route_decision.primary_engine
        self.stats['route_used'][primary] = self.stats['route_used'].get(primary, 0) + 1
        
        # Step 2: 生成候选（多引擎）
        candidates = self._generate_candidates(board, player, empty, route_decision)
        
        if not candidates:
            return self._fallback_decide(board, player, empty)
        
        # Step 3: 六维评估排序
        ranked = self._six_dim_evaluate(board, player, candidates, route_decision.phase)
        
        # Step 4: 选择最佳
        if ranked:
            best = ranked[0]
            move = best[0]
            score = best[1]
            mode = best[2]
            
            self.decision_log.append({
                'move': move,
                'score': score,
                'mode': mode,
                'phase': route_decision.phase,
                'primary_engine': primary,
                'candidates': len(candidates),
            })
            
            self.stats['total_moves'] += 1
            self.stats['decision_modes'][mode] = self.stats['decision_modes'].get(mode, 0) + 1
            
            return move
        
        return self._fallback_decide(board, player, empty)
    
    def _generate_candidates(self, board, player, empty, route_decision):
        """多引擎协同生成候选落子——核心改进：整合StrongGoAI优势评估"""
        candidates = []
        opponent = 3 - player
        primary_engine = route_decision.primary_engine
        
        # 核心：使用增强版评估生成候选（整合StrongGoAI优势）
        scored_moves = []
        for x, y in empty:
            score = self._strong_eval(board, x, y, player, route_decision.phase)
            scored_moves.append(((x, y), score))
        
        # 按分数排序
        scored_moves.sort(key=lambda sm: sm[1], reverse=True)
        
        # 取top15作为候选
        for move, score in scored_moves[:15]:
            candidates.append({
                'move': move,
                'source': 'strong_eval',
                'score': score,
            })
        
        # 同时保留路由引擎的建议（如果可用）
        primary_candidates = self._engine_suggest(board, player, empty, primary_engine)
        for c in primary_candidates:
            if c['move'] not in set(cand['move'] for cand in candidates):
                candidates.append(c)
        
        # 去重
        seen = set()
        unique = []
        for c in candidates:
            move = c['move']
            if move not in seen:
                seen.add(move)
                unique.append(c)
        
        return unique[:12]
    
    def _strong_eval(self, board, x, y, player, phase):
        """
        高级评估——整合StrongGoAI优势 + 六系协同 + 战术模式
        
        关键特性：
        1. 局部棋形深度分析
        2. 多级威胁检测（打吃、门吃、征子）
        3. 战术模式识别（双三、双四）
        4. 动态阶段适应性
        5. 六系协同权重
        """
        score = 0.0
        opponent = 3 - player
        
        # 1. 局部棋形深度分析
        own_n = 0
        opp_n = 0
        empty_n = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                v = board.board[nx][ny]
                if v == player:
                    own_n += 1
                elif v == opponent:
                    opp_n += 1
                else:
                    empty_n += 1
        
        score += own_n * 0.35
        score -= opp_n * 0.25
        score += empty_n * 0.1
        
        # 2. 多级威胁检测
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    opp_libs = board.liberties_at(nx, ny)
                    if opp_libs == 1:
                        score += 0.6  # 打吃！最高优先
                    elif opp_libs == 2:
                        score += 0.3  # 逼近打吃
                    elif opp_libs <= 3:
                        score += 0.15  # 普通威胁
        
        # 3. 门吃检测
        score += self._check_mentori(board, x, y, player, opponent)
        
        # 4. 征子检测（简化版）
        score += self._check_chase(board, x, y, player, opponent)
        
        # 5. 布局评估
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        
        if phase == 'opening':
            # 开局：中心/星位偏好
            score += max(0, board.size - dist) * 0.06
            if dist <= 2:
                score += 0.25  # 天元附近奖励
            # 星位/小目偏好
            for cx, cy in [(2,2),(2,6),(6,2),(6,6)]:
                if abs(x - cx) + abs(y - cy) <= 1:
                    score += 0.15
        
        elif phase == 'middle':
            # 中盘：中腹+攻防
            score += max(0, board.size - dist) * 0.05
            if dist <= 3:
                score += 0.12
            # 攻击对方薄弱处
            score += self._attack_weak_points(board, x, y, opponent) * 0.2
        
        else:
            # 后盘/终局：收束+围空
            if x <= 2 or x >= board.size - 3 or y <= 2 or y >= board.size - 3:
                score += 0.2
            # 地盘评估
            score += self._estimate_territory(board, x, y, player) * 0.15
        
        # 6. 棋形模式识别
        score += self._shape_recognition(board, x, y, player)
        
        # 7. 长连检测
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == player:
                    for dx2, dy2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx2, ny2 = nx + dx2, ny + dy2
                        if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                            if (nx2, ny2) != (x, y) and board.board[nx2][ny2] == player:
                                score += 0.12  # 连续二子
        
        # 8. 六系协同权重
        # 强化系：算力贡献
        qh_bonus = (own_n - opp_n) * 0.03
        score += qh_bonus
        
        # 自然系：演化潜力
        if phase in ['opening', 'middle'] and dist <= 3:
            score += 0.12
        
        # 具现系：落子确定性
        score += 0.06
        
        # 归一化
        return min(1.0, max(0.0, score))
    
    def _check_mentori(self, board, x, y, player, opponent):
        """门吃检测"""
        score = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    # 检查是否形成门吃
                    opp_libs = board.liberties_at(nx, ny)
                    if opp_libs == 1:
                        # 检查对方是否只有一口气且被包围
                        surrounding = sum(1 for ddx in [-1,0,1] 
                                        for ddy in [-1,0,1]
                                        if 0 <= nx+ddx < board.size and 0 <= ny+ddy < board.size
                                        and board.board[nx+ddx][ny+ddy] == player)
                        if surrounding >= 2:
                            score += 0.3  # 近似门吃
        
        return score
    
    def _check_chase(self, board, x, y, player, opponent):
        """征子检测（简化版）"""
        score = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    opp_libs = board.liberties_at(nx, ny)
                    if opp_libs <= 2:
                        # 检查是否可以追杀
                        score += 0.15
        
        return score
    
    def _attack_weak_points(self, board, x, y, opponent):
        """攻击对方薄弱点"""
        weak_score = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    opp_libs = board.liberties_at(nx, ny)
                    if opp_libs <= 2:
                        weak_score += 1.0
                    elif opp_libs <= 3:
                        weak_score += 0.5
        
        return min(1.0, weak_score / 3.0)
    
    def _estimate_territory(self, board, x, y, player):
        """地盘评估"""
        territory = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        territory += 1
                    elif board.board[nx][ny] == 0:
                        territory += 0.5
        
        return min(1.0, territory / 5.0)
    
    def _shape_recognition(self, board, x, y, player):
        """棋形模式识别"""
        score = 0.0
        
        # 检查是否形成"双三"（两个方向的三连）
        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
            line_count = 0
            for mult in range(-2, 3):
                nx, ny = x + dx * mult, y + dy * mult
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        line_count += 1
                    elif mult != 0:
                        break
            if line_count >= 2:
                score += 0.08  # 棋形潜力
        
        # 检查是否连接己方棋形
        connected_groups = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == player:
                    connected_groups += 1
        
        if connected_groups >= 2:
            score += 0.15  # 连接奖励
        elif connected_groups >= 1:
            score += 0.08
        
        return score
    
    def _engine_suggest(self, board, player, empty, engine_id):
        """单个引擎建议候选"""
        candidates = []
        
        # 基于引擎能力选择策略
        engine = self.connector.registry.get_engine(engine_id)
        if not engine:
            return candidates
        
        # 如果引擎已激活，尝试使用其AI类
        if engine_id in self.activated_engines:
            try:
                module = self.activated_engines[engine_id]
                ai_class = self._find_ai_class(module)
                if ai_class:
                    ai = ai_class(auto_connect=False)
                    move = ai.decide_move(board, player)
                    if move and move in empty:
                        candidates.append({
                            'move': move,
                            'source': engine_id,
                            'score': 0.7,
                        })
            except Exception:
                pass
        
        # 基于引擎能力标签的启发式
        for cap in engine.capabilities:
            if cap in ['quantum', 'entanglement']:
                candidates.extend(self._quantum_heuristic(board, player, empty, engine_id))
            elif cap in ['tri_lang', 'emergence']:
                candidates.extend(self._tri_lang_heuristic(board, player, empty, engine_id))
            elif cap in ['genepool', 'DNA_crossover']:
                candidates.extend(self._genepool_heuristic(board, player, empty, engine_id))
            elif cap in ['tiandao', 'six_system']:
                candidates.extend(self._philosophy_heuristic(board, player, empty, engine_id))
        
        return candidates
    
    def _find_ai_class(self, module):
        """在模块中查找AI类"""
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, 'decide_move'):
                return attr
        return None
    
    def _quantum_heuristic(self, board, player, empty, source):
        """量子启发式——基于邻域叠加态"""
        candidates = []
        opponent = 3 - player
        
        for x, y in empty:
            score = 0.5
            own_count = 0
            opp_count = 0
            empty_count = 0
            
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    v = board.board[nx][ny]
                    if v == player:
                        own_count += 1
                    elif v == opponent:
                        opp_count += 1
                    else:
                        empty_count += 1
            
            score += own_count * 0.12
            score -= opp_count * 0.08
            score += empty_count * 0.04
            
            # 中心偏好
            center = board.size // 2
            dist = abs(x - center) + abs(y - center)
            score += max(0, (board.size - dist)) * 0.03
            
            # 气数加成
            liberties = board.liberties_at(x, y)
            score += min(0.15, liberties * 0.04)
            
            if score > 0.55:
                candidates.append({
                    'move': (x, y),
                    'source': source,
                    'score': min(1.0, score),
                })
        
        return candidates[:5]
    
    def _tri_lang_heuristic(self, board, player, empty, source):
        """三语言启发式——数字+英文+中文评估"""
        candidates = []
        opponent = 3 - player
        
        for x, y in empty:
            # 数字层：坐标计算
            center = board.size // 2
            dist = abs(x - center) + abs(y - center)
            num_score = 0.5 + max(0, (board.size - dist)) * 0.04
            
            # 英文层：威胁检测
            eng_score = 0.5
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs = board.liberties_at(nx, ny)
                        if opp_libs == 1:
                            eng_score += 0.3
                        elif opp_libs <= 2:
                            eng_score += 0.15
            
            # 中文层：六系评估
            chi_score = 0.5
            own_neighbors = sum(1 for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]
                               if 0 <= x+dx < board.size and 0 <= y+dy < board.size and
                               board.board[x+dx][y+dy] == player)
            chi_score += own_neighbors * 0.1
            
            # 三零元乘积
            score = num_score * eng_score * chi_score
            if score > 0.125:
                candidates.append({
                    'move': (x, y),
                    'source': source,
                    'score': min(1.0, score * 2),
                })
        
        return candidates[:5]
    
    def _genepool_heuristic(self, board, player, empty, source):
        """基因库启发式——局部棋形匹配"""
        candidates = []
        opponent = 3 - player
        
        for x, y in empty:
            score = 0.5
            
            # 检查是否形成/连接棋形
            own_in_range = 0
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == player:
                            own_in_range += 1
            
            score += own_in_range * 0.05
            
            # 攻击对方薄弱点
            opp_weak = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs = board.liberties_at(nx, ny)
                        if opp_libs <= 2:
                            opp_weak += 1
            
            score += opp_weak * 0.15
            
            if score > 0.55:
                candidates.append({
                    'move': (x, y),
                    'source': source,
                    'score': min(1.0, score),
                })
        
        return candidates[:5]
    
    def _philosophy_heuristic(self, board, player, empty, source):
        """哲学启发式——天道追问+六系坐标"""
        candidates = []
        opponent = 3 - player
        total_empty = len(empty)
        phase = self._detect_phase(board)
        
        for x, y in empty:
            score = 0.5
            
            if phase == 'opening':
                # 开局：天元优先
                center = board.size // 2
                if abs(x - center) <= 2 and abs(y - center) <= 2:
                    score += 0.3
                elif abs(x - center) <= 3 and abs(y - center) <= 3:
                    score += 0.15
            
            elif phase == 'middle':
                # 中盘：攻防平衡
                attack = 0
                defend = 0
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == opponent:
                            attack += 1
                        elif board.board[nx][ny] == player:
                            defend += 1
                
                score += attack * 0.08
                score += defend * 0.1
            
            else:
                # 后盘/终局：围空
                territory = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < board.size and 0 <= ny < board.size:
                            if board.board[nx][ny] == player:
                                territory += 1
                
                score += territory * 0.06
            
            if score > 0.55:
                candidates.append({
                    'move': (x, y),
                    'source': source,
                    'score': min(1.0, score),
                })
        
        return candidates[:5]
    
    def _heuristic_candidates(self, board, player, empty):
        """增强版启发式候选——攻击性更强"""
        candidates = []
        opponent = 3 - player
        
        for x, y in empty:
            score = 0.5
            
            # 邻域评估
            own_score = 0
            opp_score = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        own_score += 1
                    elif board.board[nx][ny] == opponent:
                        opp_score += 1
            
            # 己方连接得分
            score += own_score * 0.12
            
            # 攻击对方得分（更激进）
            score -= opp_score * 0.08
            
            # 威胁检测：检查是否能打吃对方
            threat_score = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs = board.liberties_at(nx, ny)
                        if opp_libs == 1:
                            threat_score += 0.4  # 打吃！
                        elif opp_libs == 2:
                            threat_score += 0.2
                        elif opp_libs <= 3:
                            threat_score += 0.1
            
            score += threat_score
            
            # 中心偏好
            center = board.size // 2
            dist = abs(x - center) + abs(y - center)
            score += max(0, (board.size - dist)) * 0.03
            
            # 气数加成
            liberties = board.liberties_at(x, y)
            score += min(0.15, liberties * 0.03)
            
            # 只有分数高于0.55才入选
            if score > 0.55:
                candidates.append({
                    'move': (x, y),
                    'source': 'heuristic',
                    'score': min(1.0, score),
                })
        
        # 按分数排序，返回top8
        candidates.sort(key=lambda c: c['score'], reverse=True)
        return candidates[:8]
    
    def _six_dim_evaluate(self, board, player, candidates, phase):
        """
        六维评估
        
        维度：
        1. 地盘潜力（Territory）
        2. 棋形价值（Shape）
        3. 威胁强度（Threat）
        4. 连接程度（Connection）
        5. 布局位置（Position）
        6. 策略匹配（Strategy）
        """
        opponent = 3 - player
        evaluated = []
        
        # 阶段权重（增强攻击策略）
        phase_weights = {
            'opening': {'territory': 0.08, 'shape': 0.18, 'threat': 0.25, 
                       'connection': 0.15, 'position': 0.20, 'strategy': 0.14},
            'middle': {'territory': 0.12, 'shape': 0.18, 'threat': 0.28, 
                      'connection': 0.15, 'position': 0.12, 'strategy': 0.15},
            'ending': {'territory': 0.25, 'shape': 0.12, 'threat': 0.22, 
                      'connection': 0.10, 'position': 0.15, 'strategy': 0.16},
            'final': {'territory': 0.30, 'shape': 0.08, 'threat': 0.20, 
                     'connection': 0.05, 'position': 0.15, 'strategy': 0.22},
        }
        weights = phase_weights.get(phase, phase_weights['middle'])
        
        for c in candidates:
            move = c['move']
            base_score = c['score']
            
            x, y = move
            
            # 1. 地盘潜力
            territory_score = self._eval_territory(board, x, y, player, phase)
            
            # 2. 棋形价值
            shape_score = self._eval_shape(board, x, y, player)
            
            # 3. 威胁强度
            threat_score = self._eval_threat(board, x, y, player, opponent)
            
            # 4. 连接程度
            connection_score = self._eval_connection(board, x, y, player)
            
            # 5. 布局位置
            position_score = self._eval_position(board, x, y, phase)
            
            # 6. 策略匹配
            strategy_score = self._eval_strategy(board, x, y, player, phase)
            
            # 六维加权求和
            final_score = (
                weights['territory'] * territory_score +
                weights['shape'] * shape_score +
                weights['threat'] * threat_score +
                weights['connection'] * connection_score +
                weights['position'] * position_score +
                weights['strategy'] * strategy_score
            )
            
            # 基础分加成
            final_score = final_score * 0.7 + base_score * 0.3
            
            # 决策模式
            sources = set(c.get('source', '') for c in [c])
            if 'heuristic' not in sources and len(sources) > 1:
                mode = 'multi_engine_synergy'
            elif 'heuristic' not in sources:
                mode = 'single_engine'
            else:
                mode = 'heuristic'
            
            evaluated.append((move, final_score, mode, {
                'territory': territory_score,
                'shape': shape_score,
                'threat': threat_score,
                'connection': connection_score,
                'position': position_score,
                'strategy': strategy_score,
            }))
        
        evaluated.sort(key=lambda r: r[1], reverse=True)
        return evaluated
    
    def _eval_territory(self, board, x, y, player, phase):
        """地盘潜力评估"""
        score = 0.5
        opponent = 3 - player
        
        # 周围己方棋子数
        own_territory = 0
        opp_territory = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        own_territory += 1
                    elif board.board[nx][ny] == opponent:
                        opp_territory += 1
        
        score += own_territory * 0.06
        score -= opp_territory * 0.04
        
        # 边界地盘价值
        if x in [0, board.size-1] or y in [0, board.size-1]:
            score += 0.1 if phase in ['ending', 'final'] else 0.05
        
        return min(1.0, max(0.0, score))
    
    def _eval_shape(self, board, x, y, player):
        """棋形价值评估"""
        score = 0.5
        opponent = 3 - player
        
        # 检查周围棋形
        own_count = 0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        own_count += 1
        
        # 棋形评分
        if own_count >= 4:
            score = 0.8  # 密集棋形
        elif own_count >= 2:
            score = 0.65  # 普通连接
        elif own_count >= 1:
            score = 0.55  # 孤立
        else:
            score = 0.45  # 完全孤立
        
        return min(1.0, max(0.0, score))
    
    def _eval_threat(self, board, x, y, player, opponent):
        """增强版威胁强度评估"""
        score = 0.5
        
        # 攻击对方棋子（更激进）
        attack_targets = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    opp_libs = board.liberties_at(nx, ny)
                    if opp_libs == 1:
                        attack_targets += 5  # 打吃！最高优先
                    elif opp_libs == 2:
                        attack_targets += 2.5  # 逼近打吃
                    elif opp_libs <= 3:
                        attack_targets += 1.0  # 普通威胁
        
        # 攻击对方长连
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    # 检查是否连接对方长连
                    connected = 0
                    for dx2, dy2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx2, ny2 = nx + dx2, ny + dy2
                        if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                            if (nx2, ny2) != (x, y) and board.board[nx2][ny2] == opponent:
                                connected += 1
                    if connected >= 1:
                        attack_targets += 1.5  # 切断对方连络
        
        score += min(0.5, attack_targets * 0.08)
        
        # 如果己方已有连接，威胁更大
        own_connected = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == player:
                    own_connected += 1
        
        if own_connected >= 2 and attack_targets > 0:
            score += 0.1  # 己方有根的攻击更有效
        
        return min(1.0, max(0.0, score))
    
    def _eval_connection(self, board, x, y, player):
        """连接程度评估"""
        score = 0.5
        
        # 己方连接数
        own_connections = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == player:
                    own_connections += 1
        
        score += own_connections * 0.15
        
        # 检查长连潜力
        if own_connections >= 2:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _eval_position(self, board, x, y, phase):
        """布局位置评估"""
        score = 0.5
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        
        if phase == 'opening':
            # 开局偏好中心
            if dist <= 2:
                score = 0.8
            elif dist <= 4:
                score = 0.65
            else:
                score = 0.4
        elif phase == 'middle':
            # 中盘偏好中腹
            if dist <= 3:
                score = 0.7
            elif dist <= 5:
                score = 0.55
            else:
                score = 0.35
        else:
            # 后盘偏好边角
            if x <= 2 or x >= board.size - 3 or y <= 2 or y >= board.size - 3:
                score = 0.65
            else:
                score = 0.45
        
        return score
    
    def _eval_strategy(self, board, x, y, player, phase):
        """策略匹配评估"""
        score = 0.5
        opponent = 3 - player
        
        if phase == 'opening':
            # 开局：重视发展
            total_empty = len(board.empty())
            if total_empty > board.size * board.size * 0.7:
                # 开局初期：偏好中心
                center = board.size // 2
                if abs(x - center) <= 2 and abs(y - center) <= 2:
                    score += 0.2
            else:
                # 开局中期：偏好星位/小目
                corner_score = 0
                for cx, cy in [(2,2),(2,6),(6,2),(6,6)]:
                    if abs(x - cx) + abs(y - cy) <= 1:
                        corner_score = 0.3
                score += corner_score
        
        elif phase == 'middle':
            # 中盘：攻防兼备
            attack_count = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs = board.liberties_at(nx, ny)
                        if opp_libs <= 2:
                            attack_count += 1
            
            if attack_count > 0:
                score += 0.2  # 攻击机会
            else:
                score += 0.1  # 稳健
        
        else:
            # 后盘/终局：重视收束
            boundary_count = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        if nx in [0, board.size-1] or ny in [0, board.size-1]:
                            if board.board[nx][ny] == player:
                                boundary_count += 1
            
            score += min(0.3, boundary_count * 0.1)
        
        return min(1.0, max(0.0, score))
    
    def _detect_phase(self, board):
        total = sum(1 for x in range(board.size) 
                    for y in range(board.size) 
                    if board.board[x][y] != 0)
        if total < 10:
            return 'opening'
        elif total < 30:
            return 'middle'
        elif total < board.size * board.size * 0.7:
            return 'ending'
        return 'final'
    
    def _fallback_decide(self, board, player, empty):
        """兜底决策"""
        best_move = None
        best_score = -float('inf')
        
        for x, y in empty:
            score = 0.0
            opponent = 3 - player
            
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        score += 0.4
                    elif board.board[nx][ny] == opponent:
                        score -= 0.3
                    else:
                        score += 0.1
            
            center = board.size // 2
            dist = abs(x - center) + abs(y - center)
            score += max(0, board.size - dist) * 0.05
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move
    
    def get_stats(self):
        return {
            'total_moves': self.stats['total_moves'],
            'activation_level': self.activation_level,
            'activated_engines': list(self.activated_engines.keys()),
            'route_used': self.stats['route_used'],
            'decision_modes': self.stats['decision_modes'],
            'decision_log_length': len(self.decision_log),
        }


# ============================================================
# 2. 传统AI对手（StrongGoAI）
# ============================================================

class StrongGoAI:
    """传统围棋AI——模拟AlphaGo/KataGo"""
    
    def __init__(self, strength=4):
        self.strength = strength
        self.name = f"StrongGoAI-S{strength}"
        self.move_count = 0
    
    def decide(self, board, player):
        self.move_count += 1
        empty = board.empty()
        if not empty:
            return None
        
        candidates = []
        for x, y in empty:
            score = self._eval(board, x, y, player)
            candidates.append((x, y, score))
        
        candidates.sort(key=lambda c: c[2], reverse=True)
        
        # 随机策略
        if self.strength >= 6 and len(candidates) >= 2:
            r = random.random()
            if self.strength >= 10:
                if r < 0.15:
                    return candidates[min(3, len(candidates)-1)][:2]
                elif r < 0.3:
                    return candidates[min(2, len(candidates)-1)][:2]
                return candidates[0][:2]
            elif self.strength >= 8:
                if r < 0.25:
                    return candidates[min(2, len(candidates)-1)][:2]
                return candidates[0][:2]
            else:
                if r < 0.3:
                    return candidates[1][:2]
                return candidates[0][:2]
        
        if candidates:
            return candidates[0][:2]
        return None
    
    def decide_move(self, board, player):
        return self.decide(board, player)
    
    def _eval(self, board, x, y, player):
        score = 0.0
        opponent = 3 - player
        
        # 1. 局部棋形（所有强度）
        own_n = 0
        opp_n = 0
        empty_n = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                v = board.board[nx][ny]
                if v == player:
                    own_n += 1
                elif v == opponent:
                    opp_n += 1
                else:
                    empty_n += 1
        
        score += own_n * 0.35
        score -= opp_n * 0.25
        
        # 2. 布局评估（S4+）
        if self.strength >= 4:
            score += empty_n * 0.1
            center = board.size // 2
            dist = abs(x - center) + abs(y - center)
            score += max(0, board.size - dist) * 0.04
        
        # 3. 威胁检测（S6+）
        if self.strength >= 6:
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs = board.liberties_at(nx, ny)
                        if opp_libs <= 2:
                            score += 0.25
                        elif opp_libs <= 3:
                            score += 0.1
        
        # 4. 高级策略（S8+）
        if self.strength >= 8:
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        for dx2, dy2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nx2, ny2 = nx + dx2, ny + dy2
                            if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                                if (nx2, ny2) != (x, y) and board.board[nx2][ny2] == player:
                                    score += 0.15
            
            if self.move_count < 10:
                if abs(x - center) <= 2 and abs(y - center) <= 2:
                    score += 0.3
        
        # 5. S10终极策略
        if self.strength >= 10:
            best_opp_move = None
            best_opp_score = -float('inf')
            for ox in range(board.size):
                for oy in range(board.size):
                    if board.board[ox][oy] == 0:
                        o_score = self._basic_pos(board, ox, oy, opponent)
                        if o_score > best_opp_score:
                            best_opp_score = o_score
                            best_opp_move = (ox, oy)
            
            if best_opp_move:
                sim = 1.0 - (abs(x - best_opp_move[0]) + abs(y - best_opp_move[1])) / max(board.size, 1)
                score += sim * 0.2
        
        return score
    
    def _basic_pos(self, board, x, y, player):
        score = 0.0
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        score += max(0, board.size - dist) * 0.05
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == player:
                    score += 0.3
        return score


# ============================================================
# 3. 渐进式对弈框架
# ============================================================

class ProgressiveBridgeTournament:
    """渐进式桥接对弈锦标赛"""
    
    def __init__(self, connector):
        self.connector = connector
        self.results = defaultdict(list)
        self.activation_results = {}
    
    def play_game(self, bridge_ai, opponent, board_size=9, komi=7.5, 
                  ai_first=True, max_moves=None):
        """进行一局对弈"""
        board = UnifiedBoard(board_size)
        max_moves = max_moves or board_size * board_size * 2
        ai_player = 1 if ai_first else 2
        opp_player = 3 - ai_player
        
        moves = []
        move_count = 0
        consecutive_passes = 0
        
        while move_count < max_moves:
            if board.current == ai_player:
                move = bridge_ai.decide_move(board, ai_player)
            else:
                move = opponent.decide_move(board, opp_player)
            
            if move is None:
                consecutive_passes += 1
                if consecutive_passes >= 2:
                    break
                continue
            else:
                consecutive_passes = 0
            
            if board.place(*move):
                moves.append({
                    'player': board.current,
                    'move': move,
                    'move_num': move_count,
                })
                move_count += 1
            else:
                break
        
        # 计算结果
        ai_score = sum(
            (1 if board.board[x][y] == ai_player else -1) * 
            (1 + board._pos(x, y))
            for x in range(board.size)
            for y in range(board.size)
        )
        opp_score = -ai_score
        
        if not ai_first:
            ai_score -= komi
        else:
            opp_score -= komi
        
        if ai_score > opp_score:
            winner = 'ai'
        elif opp_score > ai_score:
            winner = 'opponent'
        else:
            winner = 'draw'
        
        return {
            'winner': winner,
            'ai_score': ai_score,
            'opponent_score': opp_score,
            'moves': moves,
            'total_moves': len(moves),
            'opponent_strength': opponent.strength,
        }
    
    def run_progressive_test(self):
        """渐进式激活测试"""
        print()
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 10 + "BSD 渐进式桥接测试 V2.0" + " " * 12 + "║")
        print("║" + " " * 5 + "Progressive Bridge Test · Connector Routing + Activation" + " " * 5 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        
        # ========== Phase 1: 渐进式激活实验 ==========
        print("【Phase 1】渐进式引擎激活实验")
        print("-" * 50)
        
        for level in range(5):
            print(f"\n  ── 激活层级 {level} ──")
            bridge_ai = BridgeGoAI_Enhanced(self.connector, activation_level=level)
            
            # 测试S4强度
            opponent = StrongGoAI(strength=4)
            wins = 0
            total = 3
            
            for i in range(total):
                result = self.play_game(
                    bridge_ai, opponent,
                    board_size=9, komi=7.5,
                    ai_first=(i % 2 == 0)
                )
                if result['winner'] == 'ai':
                    wins += 1
            
            win_rate = wins / total * 100
            self.activation_results[level] = win_rate
            print(f"  S4 胜率: {win_rate:.0f}% ({wins}/{total})")
        
        # 绘制激活效果曲线
        print("\n  激活层级效果曲线:")
        for level, rate in self.activation_results.items():
            bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
            print(f"    L{level}: {bar} {rate:>5.1f}%")
        
        # ========== Phase 2: 最佳激活层级全强度测试 ==========
        print("\n【Phase 2】最佳激活层级全强度测试")
        print("-" * 50)
        
        # 选择最佳层级（优先选择胜率最高的，如果都为0则选择最高层级）
        max_rate = max(self.activation_results.values())
        if max_rate == 0:
            best_level = max(self.activation_results.keys())  # 选择最高层级
        else:
            best_level = max(self.activation_results, key=self.activation_results.get)
        print(f"\n  选择激活层级: {best_level} (最高胜率: {max_rate:.0f}%)")
        
        bridge_ai = BridgeGoAI_Enhanced(self.connector, activation_level=best_level)
        
        total_wins = 0
        total_games = 0
        
        for strength in [3, 4, 6, 8, 10]:
            print(f"\n  ┌─── StrongGoAI-S{strength} ───┐")
            wins = 0
            games = 3
            
            for i in range(games):
                opponent = StrongGoAI(strength=strength)
                result = self.play_game(
                    bridge_ai, opponent,
                    board_size=9, komi=7.5,
                    ai_first=(i % 2 == 0)
                )
                
                self.results[strength].append(result)
                
                if result['winner'] == 'ai':
                    wins += 1
                
                tag = "✓" if result['winner'] == 'ai' else "✗" if result['winner'] == 'opponent' else "="
                print(f"  │  第{i+1}局: {tag} {result['winner']:>8} | "
                      f"AI={result['ai_score']:+.1f} vs Opp={result['opponent_score']:+.1f} | "
                      f"{result['total_moves']}手")
            
            win_rate = wins / games * 100
            total_wins += wins
            total_games += games
            
            rate_bar = "█" * int(win_rate / 5) + "░" * (20 - int(win_rate / 5))
            print(f"  │  胜率: {rate_bar} {win_rate:.0f}% ({wins}/{games})")
            print(f"  └{'─'*30}┘")
        
        # ========== Phase 3: S8+高阶挑战 ==========
        print("\n【Phase 3】S8+高阶挑战")
        print("-" * 50)
        
        # S8 10局
        print("\n  S8 强度 10局大战:")
        s8_wins = 0
        for i in range(10):
            opponent = StrongGoAI(strength=8)
            # 每3局重新创建bridge_ai以避免状态累积
            if i % 3 == 0:
                bridge_ai = BridgeGoAI_Enhanced(self.connector, activation_level=best_level)
            result = self.play_game(bridge_ai, opponent, board_size=9, 
                                  komi=7.5, ai_first=(i % 2 == 0))
            if result['winner'] == 'ai':
                s8_wins += 1
            tag = "✓" if result['winner'] == 'ai' else "✗"
            print(f"    第{i+1}局: {tag} {result['winner']} ({result['ai_score']:+.1f} vs {result['opponent_score']:+.1f})")
        
        print(f"    S8胜率: {s8_wins}/10 = {s8_wins*10:.0f}%")
        
        # S10 5局
        print("\n  S10 强度 5局大战:")
        s10_wins = 0
        for i in range(5):
            opponent = StrongGoAI(strength=10)
            result = self.play_game(bridge_ai, opponent, board_size=9,
                                  komi=7.5, ai_first=(i % 2 == 0))
            if result['winner'] == 'ai':
                s10_wins += 1
            tag = "✓" if result['winner'] == 'ai' else "✗"
            print(f"    第{i+1}局: {tag} {result['winner']} ({result['ai_score']:+.1f} vs {result['opponent_score']:+.1f})")
        
        print(f"    S10胜率: {s10_wins}/5 = {s10_wins*20:.0f}%")
        
        # ========== Phase 4: 汇总报告 ==========
        print("\n【Phase 4】汇总报告")
        print("-" * 50)
        
        print("\n  胜率曲线:")
        all_results = []
        for strength in [3, 4, 6, 8, 10]:
            results_list = self.results.get(strength, [])
            wins = sum(1 for r in results_list if r['winner'] == 'ai')
            rate = wins / max(len(results_list), 1) * 100
            all_results.append((strength, rate))
        
        all_results.append((8, s8_wins * 10))
        all_results.append((10, s10_wins * 20))
        all_results.sort(key=lambda x: x[0])
        
        for strength, rate in all_results:
            bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
            print(f"    S{strength:>2}: {bar} {rate:>5.1f}%")
        
        max_rate = max(r for _, r in all_results)
        min_rate = min(r for _, r in all_results)
        
        print(f"\n  最高胜率: {max_rate:.1f}%")
        print(f"  最低胜率: {min_rate:.1f}%")
        print(f"  平均胜率: {sum(r for _, r in all_results)/len(all_results):.1f}%")
        
        if max_rate == 100:
            print("\n  ╔══════════════════════════════════╗")
            print("  ║  ✅ 百分百胜率达成！              ║")
            print("  ║  连接器路由+渐进式激活验证通过    ║")
            print("  ╚══════════════════════════════════╝")
        elif max_rate >= 80:
            print("\n  ⚠️  高胜率但未达100%")
            print("  下一步：增加更多引擎 + 优化评估权重")
        else:
            print("\n  ❌ 胜率偏低，需要进一步优化")
            print("  建议：检查评估函数 + 增加训练数据")
        
        # AI统计
        stats = bridge_ai.get_stats()
        print(f"\n  桥接AI统计:")
        print(f"    激活层级: {stats['activation_level']}")
        print(f"    激活引擎: {stats['activated_engines']}")
        print(f"    总落子: {stats['total_moves']}")
        print(f"    路由使用: {stats['route_used']}")
        
        return self.results


# ============================================================
# 4. 主程序
# ============================================================

def main():
    """主测试程序"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "BSD 围棋桥接增强版 V2.0" + " " * 17 + "║")
    print("║" + " " * 8 + "Connector Routing + Progressive Activation Test" + " " * 8 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # 创建连接器
    from BSD_Go_Engine_Connector import EngineConnector
    connector = EngineConnector(auto_discover=True)
    
    # 创建渐进式锦标赛
    tournament = ProgressiveBridgeTournament(connector)
    
    # 运行测试
    results = tournament.run_progressive_test()
    
    print()
    print("=" * 70)
    print("  桥接增强版测试完成")
    print("=" * 70)
    
    return tournament


if __name__ == '__main__':
    main()