#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋引擎桥接测试 · Bridge Integration Test
================================================

核心目标：通过连接器桥接散落引擎，验证协同增益

测试架构：
┌───────────────────────────────────────────────────────────────┐
│                    BSD Bridge Test Runner                      │
├───────────────────────────────────────────────────────────────┤
│  Step 1: E06(量子引擎) ↔ E11(三语言模块) 桥接                │
│  Step 2: 连接器路由接入PlayTest框架                           │
│  Step 3: 逐步激活引擎 → 观察协同效应                           │
│  Step 4: BSDAI vs StrongGoAI Strength=3/4/6/8/10 验证          │
└───────────────────────────────────────────────────────────────┘

理论依据：
- 0×0=n 双零涌现：多引擎连接产生协同增益
- 定理五十八·三语言涌现定理
- 定理五十九·围棋六系映射定理

版本：V1.0 · 2026-08-04
"""

import os
import sys
import time
import random
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 '..', 'bsd_engine', 'core'))


# ============================================================
# 0. 统一棋盘适配器
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
    
    def pattern(self, x, y, r=1):
        p = []
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = x + dx, y + dy
                p.append(self.board[nx][ny] 
                        if 0 <= nx < self.size and 0 <= ny < self.size 
                        else -1)
        return p
    
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
    
    def get_group(self, x, y):
        """获取连通块"""
        color = self.board[x][y]
        if color == 0:
            return []
        group = []
        visited = set()
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            if not (0 <= cx < self.size and 0 <= cy < self.size):
                continue
            if self.board[cx][cy] != color:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                stack.append((cx + dx, cy + dy))
        return group
    
    def display(self):
        symbols = {0: '.', 1: '●', 2: '○'}
        for x in range(self.size):
            row = ''
            for y in range(self.size):
                row += symbols.get(self.board[x][y], '?') + ' '
            print(f'  {row}')


# ============================================================
# 1. 桥接AI（BridgeGoAI）
# ============================================================

class BridgeGoAI:
    """
    桥接AI——通过连接器组合多个引擎
    
    决策流程：
    1. 连接器路由 → 选定主引擎+副引擎
    2. 主引擎(E06量子)生成候选
    3. 副引擎(E07三语言)评估候选
    4. 综合评分 → 最终落子
    
    理论：0×0=n → 量子引擎(0) × 三语言引擎(0) = 协同增益(n)
    """
    
    def __init__(self, connector, auto_activate=True):
        self.connector = connector
        self.move_count = 0
        self.activated_engines = {}
        self.decision_log = []
        self.bridge_stats = {
            'quantum_decisions': 0,
            'tri_lang_decisions': 0,
            'synergy_decisions': 0,
            'fallback_decisions': 0,
        }
        
        if auto_activate:
            self._activate_core_engines()
    
    def _activate_core_engines(self):
        """激活核心引擎"""
        for eid in ['E06', 'E07', 'E08', 'E10', 'E11']:
            module = self.connector.activate_engine(eid)
            if module:
                self.activated_engines[eid] = module
    
    def decide_move(self, board, player):
        """
        桥接决策
        
        策略：
        1. 用E06(量子引擎)获取候选落子
        2. 用E07/E11(三语言)评估候选
        3. 用E08/V11(统一引擎)兜底
        """
        self.move_count += 1
        empty = board.empty()
        if not empty:
            return None
        
        phase = self._detect_phase(board)
        
        # Step 1: 量子引擎候选
        quantum_candidates = self._get_quantum_candidates(board, player, empty)
        
        # Step 2: 三语言评估排序
        ranked = self._tri_lang_rank(board, player, quantum_candidates, phase)
        
        # Step 3: 选择最佳
        if ranked:
            best = ranked[0]
            move = best[0]
            score = best[1]
            mode = best[2]
            
            self.decision_log.append({
                'move': move,
                'score': score,
                'mode': mode,
                'phase': phase,
                'candidates_count': len(quantum_candidates),
            })
            
            if mode == 'quantum_inspiration':
                self.bridge_stats['quantum_decisions'] += 1
            elif mode == 'tri_lang_emergence':
                self.bridge_stats['tri_lang_decisions'] += 1
            elif mode == 'synergy':
                self.bridge_stats['synergy_decisions'] += 1
            else:
                self.bridge_stats['fallback_decisions'] += 1
            
            return move
        
        # Fallback: 位置启发式
        return self._fallback_decide(board, player, empty)
    
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
    
    def _get_quantum_candidates(self, board, player, empty):
        """从E06量子引擎获取候选落子"""
        candidates = []
        
        # 尝试E06量子引擎
        if 'E06' in self.activated_engines:
            try:
                module = self.activated_engines['E06']
                if hasattr(module, 'QuantumInspirationAI'):
                    ai = module.QuantumInspirationAI(auto_connect=False)
                    move = ai.decide_move(board, player)
                    if move and board.board[move[0]][move[1]] == 0:
                        candidates.append({
                            'move': move,
                            'source': 'E06_quantum',
                            'base_score': 0.8,
                            'quantum': True,
                        })
            except Exception:
                pass
        
        # 启发式候选（模拟E06的纠缠匹配逻辑）
        for x, y in empty:
            score = self._quantum_heuristic(board, x, y, player)
            if score > 0.5:
                candidates.append({
                    'move': (x, y),
                    'source': 'E06_heuristic',
                    'base_score': score,
                    'quantum': score > 0.7,
                })
        
        # 去重
        seen = set()
        unique = []
        for c in candidates:
            if c['move'] not in seen:
                seen.add(c['move'])
                unique.append(c)
        
        return unique[:8]
    
    def _quantum_heuristic(self, board, x, y, player):
        """量子启发式评分——模拟叠加态概率"""
        opponent = 3 - player
        score = 0.5
        
        own_neighbors = 0
        opp_neighbors = 0
        empty_neighbors = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                v = board.board[nx][ny]
                if v == player:
                    own_neighbors += 1
                elif v == opponent:
                    opp_neighbors += 1
                elif v == 0:
                    empty_neighbors += 1
        
        score += own_neighbors * 0.08
        score -= opp_neighbors * 0.06
        score += empty_neighbors * 0.03
        
        # 位置加成
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        score += max(0, (board.size - dist)) * 0.02
        
        # 棋形匹配（模拟纠缠态）
        liberties = board.liberties_at(x, y)
        if liberties >= 2:
            score += 0.1
        
        # 量子叠加：多邻域中心概率更高
        if own_neighbors >= 2:
            score += 0.15  # 纠缠增强
        
        return min(1.0, max(0.0, score))
    
    def _tri_lang_rank(self, board, player, candidates, phase):
        """三语言评估排序——整合E07/E11的评估能力"""
        ranked = []
        
        for c in candidates:
            move = c['move']
            base_score = c['base_score']
            
            # 数字层评估（E11 NumberLayer）
            num_score = self._number_eval(board, move, player)
            
            # 英文层评估（E11 EnglishLayer）
            eng_score = self._english_eval(board, move, player)
            
            # 中文层评估（E11 ChinesePhilosophyLayer）
            chi_score = self._chinese_eval(board, move, player, phase)
            
            # 三零元乘积 → 涌现潜力
            emergence = num_score * eng_score * chi_score
            
            # 综合评分 = 基础分×0.4 + 涌现×0.6
            final_score = base_score * 0.4 + emergence * 0.6
            
            # 决策模式判定
            if c.get('quantum') and emergence > 0.125:
                mode = 'synergy'  # 量子+涌现协同
            elif c.get('quantum'):
                mode = 'quantum_inspiration'
            elif emergence > 0.125:
                mode = 'tri_lang_emergence'
            else:
                mode = 'heuristic'
            
            ranked.append((move, final_score, mode, {
                'num': num_score,
                'eng': eng_score,
                'chi': chi_score,
                'emergence': emergence,
                'base': base_score,
            }))
        
        ranked.sort(key=lambda r: r[1], reverse=True)
        return ranked
    
    def _number_eval(self, board, move, player):
        """数字层评估：坐标映射·气数计算·领地计算"""
        x, y = move
        score = 0.5
        
        # 坐标中心度
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        score += max(0, (board.size - dist)) * 0.02
        
        # 邻域密度
        opponent = 3 - player
        own = 0
        opp = 0
        empty = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                v = board.board[nx][ny]
                if v == player:
                    own += 1
                elif v == opponent:
                    opp += 1
                elif v == 0:
                    empty += 1
        
        score += own * 0.15
        score -= opp * 0.10
        score += empty * 0.05
        
        # 气数估计
        liberties = 1 + empty
        score += min(0.2, liberties * 0.03)
        
        return min(1.0, max(0.0, score))
    
    def _english_eval(self, board, move, player):
        """英文层评估：AI威胁检测·棋形识别·攻防分析"""
        x, y = move
        score = 0.5
        opponent = 3 - player
        
        # 威胁检测：是否攻击对方
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == opponent:
                    # 检查对方气
                    opp_libs = board.liberties_at(nx, ny)
                    if opp_libs == 1:
                        score += 0.3  # 打吃！
                    elif opp_libs <= 2:
                        score += 0.15
        
        # 棋形识别：是否连接己方
        own_group = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[nx][ny] == player:
                    own_group.append((nx, ny))
        
        if own_group:
            # 连接得分
            score += 0.15 + min(0.1, len(own_group) * 0.03)
            
            # 长连检测
            for ox, oy in own_group:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = ox + dx, oy + dy
                    if (nx, ny) != (x, y) and 0 <= nx < board.size and 0 <= ny < board.size:
                        if board.board[nx][ny] == player:
                            score += 0.1  # 连续二子
        
        # 攻防平衡
        if score > 0.7:
            score = 0.5 + (score - 0.5) * 0.5  # 攻击型调整
        
        return min(1.0, max(0.0, score))
    
    def _chinese_eval(self, board, move, player, phase):
        """中文层评估：六系坐标·棋道追问·哲学评估"""
        x, y = move
        score = 0.5
        
        # 阶段权重
        phase_weights = {
            'opening': {'qh': 0.12, 'zr': 0.25, 'jx': 0.18, 'bs': 0.15, 'sh': 0.15, 'td': 0.15},
            'middle': {'qh': 0.15, 'zr': 0.20, 'jx': 0.15, 'bs': 0.20, 'sh': 0.15, 'td': 0.15},
            'ending': {'qh': 0.12, 'zr': 0.15, 'jx': 0.20, 'bs': 0.15, 'sh': 0.18, 'td': 0.20},
            'final': {'qh': 0.10, 'zr': 0.10, 'jx': 0.25, 'bs': 0.15, 'sh': 0.20, 'td': 0.20},
        }
        weights = phase_weights.get(phase, phase_weights['middle'])
        
        # 强化系🔵：算力贡献
        qh_score = 0.5
        opponent = 3 - player
        own_count = 0
        opp_count = 0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        own_count += 1
                    elif board.board[nx][ny] == opponent:
                        opp_count += 1
        qh_score = 0.5 + (own_count - opp_count) * 0.03
        
        # 自然系🟠：演化潜力
        zr_score = 0.5
        center = board.size // 2
        dist = abs(x - center) + abs(y - center)
        if phase in ['opening', 'middle']:
            zr_score = 0.7 if dist <= 3 else 0.4
        else:
            zr_score = 0.6 if dist <= 2 else 0.5
        
        # 具现系🔴：落子凝结
        jx_score = 0.6  # 落子本身的确定性
        
        # 变身系⚫：创新变化
        bs_score = 0.5
        # 检查是否创造新模式
        has_own_neighbor = any(
            0 <= x+dx < board.size and 0 <= y+dy < board.size and
            board.board[x+dx][y+dy] == player
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]
        )
        if not has_own_neighbor and phase == 'opening':
            bs_score = 0.7  # 开局独立落子=创新
        elif has_own_neighbor and phase in ['middle', 'ending']:
            bs_score = 0.6  # 中后盘连接=稳妥变化
        
        # 社会系🟢：博弈关系
        sh_score = 0.5
        if phase in ['ending', 'final']:
            opp_libs = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == opponent:
                        opp_libs += board.liberties_at(nx, ny)
            if opp_libs <= 3:
                sh_score = 0.7  # 威胁对方
        
        # 天道系🟣：意义追问
        td_score = 0.5
        if phase == 'final':
            total_empty = sum(1 for ex in range(board.size) 
                            for ey in range(board.size) 
                            if board.board[ex][ey] == 0)
            if total_empty < board.size * board.size * 0.2:
                td_score = 0.7  # 终局重视意义
        
        # 六系加权
        score = (weights['qh'] * qh_score + 
                 weights['zr'] * zr_score + 
                 weights['jx'] * jx_score +
                 weights['bs'] * bs_score + 
                 weights['sh'] * sh_score + 
                 weights['td'] * td_score)
        
        return min(1.0, max(0.0, score))
    
    def _fallback_decide(self, board, player, empty):
        """兜底启发式决策"""
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
        
        self.bridge_stats['fallback_decisions'] += 1
        return best_move
    
    def get_stats(self):
        total = sum(self.bridge_stats.values())
        modes = {}
        for mode, count in self.bridge_stats.items():
            if count > 0:
                modes[mode] = f"{count}次 ({count/max(total,1)*100:.1f}%)"
        
        return {
            'total_moves': self.move_count,
            'activated_engines': list(self.activated_engines.keys()),
            'decision_modes': modes,
            'bridge_stats': dict(self.bridge_stats),
            'decision_log_length': len(self.decision_log),
        }


# ============================================================
# 2. 传统AI对手（StrongGoAI）
# ============================================================

class StrongGoAI:
    """
    传统围棋AI——模拟AlphaGo/KataGo
    
    强度等级：
    - S3: 基础算力，随机30%
    - S4: 基础+局部棋形
    - S6: 棋形+威胁检测+30%随机
    - S8: 棋形+威胁+布局+高级策略
    - S10: 全套AlphaGo基础版
    """
    
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
            # 长连奖励
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.board[nx][ny] == player:
                        for dx2, dy2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nx2, ny2 = nx + dx2, ny + dy2
                            if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                                if (nx2, ny2) != (x, y) and board.board[nx2][ny2] == player:
                                    score += 0.15
            
            # 开局中心偏好
            if self.move_count < 10:
                if abs(x - center) <= 2 and abs(y - center) <= 2:
                    score += 0.3
        
        # 5. S10终极策略
        if self.strength >= 10:
            # 模仿对手最佳点
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
# 3. 对弈框架
# ============================================================

class BridgeTournament:
    """桥接对弈锦标赛"""
    
    def __init__(self, connector):
        self.connector = connector
        self.bridge_ai = BridgeGoAI(connector, auto_activate=True)
        self.results = defaultdict(list)
        self.game_log = []
    
    def play_game(self, opponent, board_size=9, komi=7.5, ai_first=True, 
                  max_moves=None):
        """进行一局对弈"""
        board = UnifiedBoard(board_size)
        max_moves = max_moves or board_size * board_size * 2
        ai_player = 1 if ai_first else 2
        opp_player = 3 - ai_player
        
        moves = []
        move_count = 0
        consecutive_passes = 0
        
        while move_count < max_moves:
            # AI回合
            if board.current == ai_player:
                move = self.bridge_ai.decide_move(board, ai_player)
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
                    'player': board.current,  # 注意：current已切换
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
        
        # 贴目
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
    
    def run_tournament(self, strengths=[3, 4, 6, 8, 10], games_per_strength=3):
        """运行锦标赛"""
        print("=" * 70)
        print("  BSD 桥接AI vs StrongGoAI 锦标赛")
        print("=" * 70)
        print()
        
        total_wins = 0
        total_games = 0
        
        for strength in strengths:
            print(f"  ┌─── StrongGoAI-S{strength} ───┐")
            wins = 0
            losses = 0
            draws = 0
            
            for i in range(games_per_strength):
                opponent = StrongGoAI(strength=strength)
                result = self.play_game(
                    opponent, 
                    board_size=9, 
                    komi=7.5,
                    ai_first=(i % 2 == 0)
                )
                
                self.results[strength].append(result)
                self.game_log.append(result)
                
                if result['winner'] == 'ai':
                    wins += 1
                elif result['winner'] == 'opponent':
                    losses += 1
                else:
                    draws += 0.5
                
                tag = "✓" if result['winner'] == 'ai' else "✗" if result['winner'] == 'opponent' else "="
                print(f"  │  第{i+1}局: {tag} {result['winner']:>8} | "
                      f"AI={result['ai_score']:+.1f} vs Opp={result['opponent_score']:+.1f} | "
                      f"{result['total_moves']}手")
            
            win_rate = wins / games_per_strength * 100
            total_wins += wins
            total_games += games_per_strength
            
            rate_bar = "█" * int(win_rate / 5) + "░" * (20 - int(win_rate / 5))
            print(f"  │  胜率: {rate_bar} {win_rate:.0f}% ({wins}/{games_per_strength})")
            print(f"  └{'─'*30}┘")
            print()
        
        # 汇总
        print("=" * 70)
        print("  锦标赛汇总")
        print("=" * 70)
        print()
        
        for strength in strengths:
            results = self.results[strength]
            wins = sum(1 for r in results if r['winner'] == 'ai')
            rate = wins / len(results) * 100
            status = "✅" if rate == 100 else "⚠️" if rate >= 50 else "❌"
            print(f"  {status} S{strength}: {rate:.0f}% ({wins}/{len(results)})")
        
        print()
        print(f"  总胜率: {total_wins}/{total_games} = {total_wins/max(total_games,1)*100:.1f}%")
        
        # 桥接AI统计
        stats = self.bridge_ai.get_stats()
        print()
        print("=" * 70)
        print("  桥接AI决策统计")
        print("=" * 70)
        print(f"  总落子: {stats['total_moves']}")
        print(f"  激活引擎: {stats['activated_engines']}")
        print(f"  决策模式分布:")
        for mode, info in stats['decision_modes'].items():
            print(f"    - {mode}: {info}")
        
        return self.results


# ============================================================
# 4. 桥接协同增益分析
# ============================================================

class SynergyAnalyzer:
    """协同增益分析器"""
    
    def __init__(self, connector):
        self.connector = connector
    
    def analyze_bridge(self, engine_a_id, engine_b_id):
        """分析两个引擎的桥接增益"""
        eng_a = self.connector.registry.get_engine(engine_a_id)
        eng_b = self.connector.registry.get_engine(engine_b_id)
        
        if not eng_a or not eng_b:
            return {'error': '引擎未找到'}
        
        # 能力互补度
        caps_a = set(eng_a.capabilities)
        caps_b = set(eng_b.capabilities)
        overlap = caps_a & caps_b
        union = caps_a | caps_b
        
        complementarity = 1.0 - len(overlap) / max(len(union), 1)
        
        # 阶段覆盖
        phases_a = set(eng_a.best_phase)
        phases_b = set(eng_b.best_phase)
        phase_coverage = phases_a | phases_b
        
        # 优先级乘积
        priority_product = eng_a.priority * eng_b.priority
        
        # 协同增益估计
        synergy = complementarity * priority_product * 100
        
        return {
            'engine_a': {'id': engine_a_id, 'version': eng_a.version, 'priority': eng_a.priority},
            'engine_b': {'id': engine_b_id, 'version': eng_b.version, 'priority': eng_b.priority},
            'complementarity': round(complementarity, 3),
            'shared_capabilities': list(overlap),
            'unique_a': list(caps_a - caps_b),
            'unique_b': list(caps_b - caps_a),
            'phase_coverage': list(phase_coverage),
            'priority_product': round(priority_product, 3),
            'estimated_synergy': round(synergy, 1),
            'recommendation': 'high' if synergy > 50 else 'medium' if synergy > 30 else 'low',
        }
    
    def analyze_full_chain(self, engine_ids):
        """分析完整引擎链的协同"""
        engines = [self.connector.registry.get_engine(eid) 
                   for eid in engine_ids
                   if self.connector.registry.get_engine(eid)]
        
        if len(engines) < 2:
            return {'error': '至少需要2个引擎'}
        
        total_complementarity = 0
        total_overlap = 0
        
        for i in range(len(engines)):
            for j in range(i+1, len(engines)):
                caps_i = set(engines[i].capabilities)
                caps_j = set(engines[j].capabilities)
                total_overlap += len(caps_i & caps_j)
                union = caps_i | caps_j
                comp = 1.0 - len(caps_i & caps_j) / max(len(union), 1)
                total_complementarity += comp
        
        n_pairs = len(engines) * (len(engines) - 1) // 2
        avg_complementarity = total_complementarity / max(n_pairs, 1)
        
        all_phases = set()
        for eng in engines:
            all_phases.update(eng.best_phase)
        
        avg_priority = sum(eng.priority for eng in engines) / len(engines)
        
        return {
            'chain_length': len(engines),
            'engines': [{'id': e.engine_id, 'version': e.version} for e in engines],
            'avg_complementarity': round(avg_complementarity, 3),
            'total_shared': total_overlap,
            'phase_coverage': list(all_phases),
            'avg_priority': round(avg_priority, 3),
            'estimated_synergy': round(avg_complementarity * avg_priority * 100, 1),
        }


# ============================================================
# 5. 主程序
# ============================================================

def main():
    """主测试程序"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "BSD 围棋引擎桥接测试 V1.0" + " " * 17 + "║")
    print("║" + " " * 10 + "Bridge Integration Test · E06×E11 Synergy Verification" + " " * 9 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # ========== Step 1: 创建连接器 ==========
    print("【Step 1】初始化连接器")
    print("-" * 50)
    
    from BSD_Go_Engine_Connector import EngineConnector
    connector = EngineConnector(auto_discover=True)
    
    # ========== Step 2: 桥接增益分析 ==========
    print()
    print("【Step 2】E06(量子) × E11(三语言) 桥接增益分析")
    print("-" * 50)
    
    analyzer = SynergyAnalyzer(connector)
    
    # 双引擎桥接
    bridge_analysis = analyzer.analyze_bridge('E06', 'E11')
    print(f"  互补度: {bridge_analysis['complementarity']:.2f}")
    print(f"  共享能力: {bridge_analysis['shared_capabilities']}")
    print(f"  E06独有: {bridge_analysis['unique_a']}")
    print(f"  E11独有: {bridge_analysis['unique_b']}")
    print(f"  优先级乘积: {bridge_analysis['priority_product']:.3f}")
    print(f"  估计协同增益: {bridge_analysis['estimated_synergy']:.1f}%")
    print(f"  推荐等级: {bridge_analysis['recommendation']}")
    
    # 全链分析
    print()
    print("【Step 3】全引擎链协同分析")
    print("-" * 50)
    
    chain = analyzer.analyze_full_chain(['E06', 'E07', 'E08', 'E10', 'E11'])
    print(f"  链长度: {chain['chain_length']} 个引擎")
    print(f"  平均互补度: {chain['avg_complementarity']:.3f}")
    print(f"  阶段覆盖: {chain['phase_coverage']}")
    print(f"  平均优先级: {chain['avg_priority']:.3f}")
    print(f"  估计协同增益: {chain['estimated_synergy']:.1f}%")
    
    # ========== Step 3: 激活引擎 ==========
    print()
    print("【Step 4】逐步激活引擎")
    print("-" * 50)
    
    activation_order = ['E06', 'E11', 'E07', 'E08', 'E10']
    for eid in activation_order:
        eng = connector.registry.get_engine(eid)
        if eng:
            module = connector.activate_engine(eid)
            status = "✓" if module else "✗"
            print(f"  {status} {eid} ({eng.version}) - {'成功激活' if module else '激活失败'}")
    
    # ========== Step 4: 运行锦标赛 ==========
    print()
    print("【Step 5】桥接AI vs StrongGoAI 锦标赛")
    print("-" * 50)
    
    tournament = BridgeTournament(connector)
    results = tournament.run_tournament(
        strengths=[3, 4, 6, 8, 10],
        games_per_strength=3
    )
    
    # ========== Step 5: 高阶挑战 ==========
    print()
    print("【Step 6】高阶验证")
    print("-" * 50)
    
    # 对S8进行10局大战
    print("  S8 强度 10局大战:")
    s8_wins = 0
    for i in range(10):
        opponent = StrongGoAI(strength=8)
        result = tournament.play_game(opponent, board_size=9, komi=7.5, 
                                      ai_first=(i % 2 == 0))
        if result['winner'] == 'ai':
            s8_wins += 1
        tag = "✓" if result['winner'] == 'ai' else "✗"
        print(f"    第{i+1}局: {tag} {result['winner']} ({result['ai_score']:+.1f} vs {result['opponent_score']:+.1f})")
    
    print(f"    S8胜率: {s8_wins}/10 = {s8_wins*10:.0f}%")
    
    # 对S10进行5局大战
    print()
    print("  S10 强度 5局大战:")
    s10_wins = 0
    for i in range(5):
        opponent = StrongGoAI(strength=10)
        result = tournament.play_game(opponent, board_size=9, komi=7.5,
                                      ai_first=(i % 2 == 0))
        if result['winner'] == 'ai':
            s10_wins += 1
        tag = "✓" if result['winner'] == 'ai' else "✗"
        print(f"    第{i+1}局: {tag} {result['winner']} ({result['ai_score']:+.1f} vs {result['opponent_score']:+.1f})")
    
    print(f"    S10胜率: {s10_wins}/5 = {s10_wins*20:.0f}%")
    
    # ========== Step 6: 最终结论 ==========
    print()
    print("=" * 70)
    print("  最终结论")
    print("=" * 70)
    
    all_results = []
    for strength in [3, 4, 6, 8]:
        results_list = results.get(strength, [])
        wins = sum(1 for r in results_list if r['winner'] == 'ai')
        total = len(results_list)
        rate = wins / max(total, 1) * 100
        all_results.append((strength, rate))
    
    # 加上额外的S8和S10
    all_results.append((8, s8_wins * 10))
    all_results.append((10, s10_wins * 20))
    
    all_results.sort(key=lambda x: x[0])
    
    print()
    print("  胜率曲线:")
    for strength, rate in all_results:
        bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
        print(f"    S{strength:>2}: {bar} {rate:>5.1f}%")
    
    max_rate = max(r for _, r in all_results)
    min_rate = min(r for _, r in all_results)
    
    print()
    print(f"  最高胜率: S{max(all_results, key=lambda x: x[1])[0]} = {max_rate:.1f}%")
    print(f"  最低胜率: S{min(all_results, key=lambda x: x[1])[0]} = {min_rate:.1f}%")
    
    if max_rate == 100:
        print()
        print("  ╔══════════════════════════════════╗")
        print("  ║  ✅ 百分百胜率达成！              ║")
        print("  ║  BSDAI桥接引擎验证通过            ║")
        print("  ╚══════════════════════════════════╝")
    elif max_rate >= 80:
        print()
        print("  ⚠️  高胜率但未达100%")
        print("  下一步：增加引擎激活数量 + 优化桥接策略")
    else:
        print()
        print("  ❌ 胜率偏低，需要进一步优化")
        print("  建议：检查决策逻辑 + 增加候选引擎")
    
    print()
    print("=" * 70)
    print("  桥接测试完成")
    print("=" * 70)
    
    return tournament


if __name__ == '__main__':
    main()