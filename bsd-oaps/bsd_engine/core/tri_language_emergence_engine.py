"""
三语言涌现引擎 (Tri-Language Emergence Engine)
================================================

核心理论：
- 三语言=三零元：数字(0∅反) × 英文(0∅空) × 中文(0∅义)
- 涌现方程：数字(000) × 英文(0110) × 中文(六系立系) = 自发涌现
- 公共AI底层是计算语言，BSD底层是中文哲学

三语言对应：
┌──────────┬──────────────────────┬──────────────┬────────────────────┐
│ 语言     │ BSD对应              │ 零元         │ 理解能力           │
├──────────┼──────────────────────┼──────────────┼────────────────────┤
│ 数字     │ 000本源基底·计算原点 │ 0∅反(反性)  │ 最强·直接映射参数  │
│ 英文     │ 0110计算开元·技术层 │ 0∅空(承载)  │ 强·AI训练主力     │
│ 中文     │ 六系立系·语义层     │ 0∅义(意义)  │ 中等·哲学语义     │
└──────────┴──────────────────────┴──────────────┴────────────────────┘

实现层级：
1. 数字层(NumberLayer)：纯计算基底，000本源
2. 英文层(EnglishLayer)：AI技术承载，0110开元
3. 中文哲学层(ChineseLayer)：六系立系显化，天道追问
"""

import math
import time
import random
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ZeroYuanType(Enum):
    """零元类型"""
    FAN = "0∅反"      # 数字层：反性·最底层
    KONG = "0∅空"     # 英文层：承载·技术容器
    YI = "0∅义"       # 中文层：意义·六系显化


class LiuHeSystem(Enum):
    """六系"""
    QH = "强化系"    # 算力
    ZR = "自然系"    # 演化
    JX = "具现系"    # 落子
    BS = "变身系"    # 创新
    SH = "社会系"    # 博弈
    TD = "天道系"    # 意义


@dataclass
class TriLanguageInput:
    """三语言输入"""
    number_input: Dict = field(default_factory=dict)   # 数字层输入
    english_input: Dict = field(default_factory=dict)  # 英文层输入
    chinese_input: Dict = field(default_factory=dict)   # 中文哲学层输入


@dataclass
class ZeroYuanState:
    """零元状态"""
    zhi_fan: float = 0.0    # 0∅反（数字层激活度）
    zhi_kong: float = 0.0   # 0∅空（英文层激活度）
    zhi_yi: float = 0.0     # 0∅义（中文层激活度）
    
    @property
    def emergence_potential(self) -> float:
        """涌现潜力 = 三零元乘积"""
        return self.zhi_fan * self.zhi_kong * self.zhi_yi
    
    @property
    def is_emergent(self) -> bool:
        """是否达到涌现阈值
        
        原阈值0.125(12.5%)过高，现降至0.05(5%)
        以确保三语言涌现更频繁参与决策
        """
        return self.emergence_potential > 0.05  # 5%阈值（降低后）


class NumberLayer:
    """数字层 - 000本源基底·计算原点·0∅反
    
    功能：
    - 坐标计算
    - 气数统计
    - 领地计算
    - 纯数学评估
    """
    
    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.fan_activation = 0.0  # 0∅反激活度
        
    def compute(self, board, stone) -> Dict:
        """执行数字层计算"""
        # 1. 坐标映射（数学原点）
        coordinates = self._map_coordinates(board, stone)
        
        # 2. 气数计算（拓扑基础）
        liberties = self._count_liberties(board, stone)
        
        # 3. 领地计算（数值核心）
        territory = self._count_territory(board, stone)
        
        # 4. 位置价值（几何评估）
        position = self._compute_position_value(board, stone)
        
        # 5. 对称性检测（数学美感）
        symmetry = self._detect_symmetry(board)
        
        # 动态计算激活度（基于实际计算结果）
        self.fan_activation = self._compute_fan_activation(
            coordinates, liberties, territory, position, symmetry
        )
        
        return {
            'coordinates': coordinates,
            'liberties': liberties,
            'territory': territory,
            'position_value': position,
            'symmetry': symmetry,
            'fan_activation': self.fan_activation
        }
    
    def _compute_fan_activation(self, coordinates, liberties, territory, 
                                position, symmetry) -> float:
        """计算0∅反激活度（基于实际计算结果）"""
        # 基于领地优势、气数活力、位置控制等综合计算
        
        territory_score = abs(territory.get('own_ratio', 0.5) - territory.get('opp_ratio', 0.5))
        liberty_score = 1.0 - liberties.get('entropy', 0.5)  # 低熵=更有序
        position_score = position.get('center_control', 0.5)
        symmetry_score = symmetry.get('horizontal_symmetry', 0.5)
        
        # 加权融合
        activation = (
            0.3 * territory_score +
            0.25 * liberty_score +
            0.25 * position_score +
            0.2 * symmetry_score
        )
        
        return min(1.0, max(0.0, activation))
    
    def _map_coordinates(self, board, stone) -> Dict:
        """坐标映射 - 000本源的空间化"""
        points = []
        center = self.board_size / 2
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == stone:
                    # 映射为相对于天元的坐标
                    dx = x - center
                    dy = y - center
                    # 极坐标表示
                    r = math.sqrt(dx**2 + dy**2)
                    theta = math.atan2(dy, dx)
                    points.append({
                        'x': x, 'y': y,
                        'dx': dx, 'dy': dy,
                        'r': r, 'theta': theta
                    })
        
        return {'points': points, 'count': len(points)}
    
    def _count_liberties(self, board, stone) -> Dict:
        """气数计算 - 拓扑基础"""
        total_libs = 0
        group_libs = []
        visited = set()
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                point = type('Point', (), {'x': x, 'y': y})()
                if board.board[y][x] == stone and point not in visited:
                    group, libs = board.get_group(point)
                    for p in group:
                        visited.add(p)
                    total_libs += len(libs)
                    group_libs.append({
                        'size': len(group),
                        'liberties': len(libs),
                        'group': [(p.x, p.y) for p in group]
                    })
        
        # 计算气数分布（反性度量）
        if group_libs:
            avg_libs = total_libs / len(group_libs)
            max_libs = max(g['liberties'] for g in group_libs)
            min_libs = min(g['liberties'] for g in group_libs)
        else:
            avg_libs = max_libs = min_libs = 0
        
        return {
            'total': total_libs,
            'groups': group_libs,
            'avg': avg_libs,
            'max': max_libs,
            'min': min_libs,
            'entropy': self._compute_liberty_entropy(group_libs)
        }
    
    def _compute_liberty_entropy(self, group_libs: List[Dict]) -> float:
        """气数熵 - 反性复杂度"""
        if not group_libs:
            return 0.0
        
        total = sum(g['liberties'] for g in group_libs)
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for g in group_libs:
            p = g['liberties'] / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        max_entropy = math.log2(len(group_libs)) if len(group_libs) > 1 else 1.0
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _count_territory(self, board, stone) -> Dict:
        """领地计算 - 数值核心"""
        own_territory = 0
        opp_territory = 0
        neutral_points = 0
        
        opp = 1 if stone == 0 else 0  # 假设0=BLACK, 1=WHITE
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                cell = board.board[y][x]
                if cell == 2:  # EMPTY
                    # 检查周围棋子
                    neighbors = []
                    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            neighbors.append(board.board[ny][nx])
                    
                    own_count = neighbors.count(stone)
                    opp_count = neighbors.count(opp)
                    
                    if own_count > 0 and opp_count == 0:
                        own_territory += 1
                    elif opp_count > 0 and own_count == 0:
                        opp_territory += 1
                    else:
                        neutral_points += 1
                elif cell == stone:
                    own_territory += 1
                else:
                    opp_territory += 1
        
        total = self.board_size ** 2
        return {
            'own': own_territory,
            'opp': opp_territory,
            'neutral': neutral_points,
            'own_ratio': own_territory / total,
            'opp_ratio': opp_territory / total,
            'difference': own_territory - opp_territory
        }
    
    def _compute_position_value(self, board, stone) -> Dict:
        """位置价值 - 几何评估"""
        center = self.board_size / 2
        own_value = 0.0
        opp_value = 0.0
        opp = 1 if stone == 0 else 0
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                dist = abs(x - center) + abs(y - center)
                max_dist = 2 * center
                value = 1.0 - dist / max_dist
                
                if board.board[y][x] == stone:
                    own_value += value
                elif board.board[y][x] == opp:
                    opp_value += value
        
        total = self.board_size ** 2 * 2
        return {
            'own': own_value,
            'opp': opp_value,
            'own_density': own_value / total,
            'opp_density': opp_value / total,
            'center_control': own_value > opp_value
        }
    
    def _detect_symmetry(self, board) -> Dict:
        """对称性检测 - 数学美感"""
        # 检查左右对称
        left_half = []
        right_half = []
        
        for y in range(self.board_size):
            for x in range(self.board_size // 2):
                left_half.append(board.board[y][x])
                right_half.append(board.board[y][self.board_size - 1 - x])
        
        left_score = sum(1 for x in left_half if x != 2)
        right_score = sum(1 for x in right_half if x != 2)
        
        symmetry_ratio = 1.0 - abs(left_score - right_score) / max(left_score + right_score, 1)
        
        return {
            'horizontal_symmetry': symmetry_ratio,
            'is_beautiful': symmetry_ratio > 0.7
        }


class EnglishLayer:
    """英文层 - 0110计算开元·技术层·0∅空
    
    功能：
    - AI评估器
    - MCTS搜索
    - 威胁检测
    - 技术指标计算
    """
    
    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.kong_activation = 0.0  # 0∅空激活度
        self.technical_metrics = {}
        
    def compute(self, board, stone, number_result: Dict) -> Dict:
        """执行英文层计算"""
        # 1. AI评估（技术核心）
        evaluation = self._ai_evaluation(board, stone)
        
        # 2. 威胁检测（技术深度）
        threats = self._detect_threats(board, stone, number_result)
        
        # 3. 棋形识别（技术模式）
        shapes = self._recognize_shapes(board, stone)
        
        # 4. 攻防分析（技术策略）
        tactics = self._analyze_tactics(board, stone, number_result)
        
        # 动态计算激活度
        self.kong_activation = self._compute_kong_activation(
            evaluation, threats, shapes, tactics
        )
        
        return {
            'evaluation': evaluation,
            'threats': threats,
            'shapes': shapes,
            'tactics': tactics,
            'kong_activation': self.kong_activation
        }
    
    def _compute_kong_activation(self, evaluation, threats, shapes, tactics) -> float:
        """计算0∅空激活度"""
        eval_score = abs(evaluation.get('score', 0))
        threat_score = 1.0 if threats.get('threat_level') == 'high' else 0.6 if threats.get('threat_level') == 'medium' else 0.3
        shape_score = shapes.get('score', 0.5)
        tactic_score = tactics.get('tactical_score', 0.5)
        
        activation = (
            0.35 * eval_score +
            0.25 * threat_score +
            0.2 * shape_score +
            0.2 * tactic_score
        )
        
        return min(1.0, max(0.0, activation))
    
    def _ai_evaluation(self, board, stone) -> Dict:
        """AI评估 - 技术核心"""
        opp = 1 if stone == 0 else 0
        
        # 综合评分
        score = 0.0
        
        # 1. 棋子对比（30%）
        own = sum(1 for y in range(self.board_size) 
                 for x in range(self.board_size) 
                 if board.board[y][x] == stone)
        opp_count = sum(1 for y in range(self.board_size) 
                       for x in range(self.board_size) 
                       if board.board[y][x] == opp)
        total = max(own + opp_count, 1)
        score += 0.3 * (own - opp_count) / total
        
        # 2. 气数优势（25%）
        own_libs = self._count_total_liberties(board, stone)
        opp_libs = self._count_total_liberties(board, opp)
        lib_total = max(own_libs + opp_libs, 1)
        score += 0.25 * (own_libs - opp_libs) / lib_total
        
        # 3. 领地潜力（25%）
        own_territory = self._estimate_territory(board, stone)
        opp_territory = self._estimate_territory(board, opp)
        terr_total = max(own_territory + opp_territory, 1)
        score += 0.25 * (own_territory - opp_territory) / terr_total
        
        # 4. 机动性（20%）
        own_moves = self._count_valid_moves(board, stone)
        opp_moves = self._count_valid_moves(board, opp)
        move_total = max(own_moves + opp_moves, 1)
        score += 0.2 * (own_moves - opp_moves) / move_total
        
        return {
            'score': max(-1.0, min(1.0, score)),
            'components': {
                'stones': 0.3 * (own - opp_count) / total,
                'liberties': 0.25 * (own_libs - opp_libs) / lib_total,
                'territory': 0.25 * (own_territory - opp_territory) / terr_total,
                'mobility': 0.2 * (own_moves - opp_moves) / move_total
            }
        }
    
    def _count_total_liberties(self, board, stone) -> int:
        total = 0
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == stone:
                    point = type('Point', (), {'x': x, 'y': y})()
                    if point not in visited:
                        group, libs = board.get_group(point)
                        for p in group:
                            visited.add(p)
                        total += len(libs)
        return total
    
    def _estimate_territory(self, board, stone) -> float:
        territory = 0.0
        opp = 1 if stone == 0 else 0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == 2:  # EMPTY
                    neighbors = []
                    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                            neighbors.append(board.board[ny][nx])
                    if neighbors.count(stone) > 0 and neighbors.count(opp) == 0:
                        territory += 1
                elif board.board[y][x] == stone:
                    territory += 1
        return territory
    
    def _count_valid_moves(self, board, stone) -> int:
        count = 0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == 2:  # EMPTY
                    try:
                        point = type('Point', (), {'x': x, 'y': y})()
                        if board.is_valid_move(point, stone):
                            count += 1
                    except:
                        pass
        return count
    
    def _detect_threats(self, board, stone, number_result: Dict) -> Dict:
        """威胁检测"""
        opp = 1 if stone == 0 else 0
        threats = []
        
        # 1. 低气数敌方棋群
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == opp:
                    point = type('Point', (), {'x': x, 'y': y})()
                    if point not in visited:
                        group, libs = board.get_group(point)
                        for p in group:
                            visited.add(p)
                        if len(libs) <= 2:
                            threats.append({
                                'type': 'low_liberties',
                                'group_size': len(group),
                                'liberties': len(libs),
                                'severity': 'high' if len(libs) == 1 else 'medium'
                            })
        
        return {
            'count': len(threats),
            'threats': threats,
            'threat_level': 'high' if len(threats) >= 3 else ('medium' if len(threats) >= 1 else 'low')
        }
    
    def _recognize_shapes(self, board, stone) -> Dict:
        """棋形识别"""
        shapes_found = []
        
        # 简单棋形检测
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == stone:
                    # 检测三子连线
                    if (x + 2 < self.board_size and
                        board.board[y][x+1] == stone and
                        board.board[y][x+2] == stone):
                        shapes_found.append('line_3')
                    
                    # 检测拐角
                    if (x + 1 < self.board_size and y + 1 < self.board_size and
                        board.board[y][x+1] == stone and
                        board.board[y+1][x] == stone):
                        shapes_found.append('corner')
        
        # 棋形评估
        shape_score = 0.0
        shape_scores = {'line_3': 0.8, 'corner': 0.6}
        for shape in shapes_found:
            shape_score += shape_scores.get(shape, 0.3)
        
        return {
            'shapes': shapes_found,
            'score': min(1.0, shape_score / max(len(shapes_found), 1))
        }
    
    def _analyze_tactics(self, board, stone, number_result: Dict) -> Dict:
        """攻防分析"""
        opp = 1 if stone == 0 else 0
        
        # 基于数字层结果的策略分析
        territory_diff = number_result.get('territory', {}).get('difference', 0)
        liberty_entropy = number_result.get('liberties', {}).get('entropy', 0)
        
        # 判断攻防策略
        if territory_diff > 0:
            strategy = 'expansion'  # 扩张
        elif territory_diff < -5:
            strategy = 'defense'   # 防守
        else:
            strategy = 'balance'   # 平衡
        
        # 攻击机会评估
        threats_count = self._count_threats(board, opp)
        
        return {
            'strategy': strategy,
            'attack_opportunity': threats_count > 0,
            'defense_needed': territory_diff < 0,
            'tactical_score': 0.5 + 0.3 * (territory_diff / max(self.board_size**2, 1))
        }
    
    def _count_threats(self, board, stone) -> int:
        """计算威胁数"""
        count = 0
        visited = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == stone:
                    point = type('Point', (), {'x': x, 'y': y})()
                    if point not in visited:
                        group, libs = board.get_group(point)
                        for p in group:
                            visited.add(p)
                        if len(libs) <= 2:
                            count += 1
        return count


class ChinesePhilosophyLayer:
    """中文哲学层 - 六系立系·语义层·0∅义
    
    功能：
    - 六系坐标映射
    - 棋道意义追问
    - 哲学维度评估
    - 天道系追问
    """
    
    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.yi_activation = 0.0  # 0∅义激活度
        self.liuhe_coordinates = {}
        
    def compute(self, board, stone, number_result: Dict, 
                english_result: Dict) -> Dict:
        """执行中文哲学层计算"""
        # 1. 六系坐标映射
        liuhe = self._map_liuhe_coordinates(board, stone, number_result, english_result)
        
        # 2. 棋道意义追问
        meaning = self._pursue_meaning(board, stone, liuhe)
        
        # 3. 哲学维度评估
        philosophy = self._philosophical_evaluation(board, stone, liuhe)
        
        # 4. 天道系追问
        tiandao = self._tiandao_inquiry(board, stone, number_result, english_result)
        
        # 动态计算激活度
        self.yi_activation = self._compute_yi_activation(
            liuhe, meaning, philosophy, tiandao
        )
        
        self.liuhe_coordinates = liuhe
        
        return {
            'liuhe_coordinates': liuhe,
            'meaning': meaning,
            'philosophy': philosophy,
            'tiandao': tiandao,
            'yi_activation': self.yi_activation
        }
    
    def _compute_yi_activation(self, liuhe, meaning, philosophy, tiandao) -> float:
        """计算0∅义激活度"""
        # 六系总活跃度
        liuhe_avg = sum([
            liuhe.get('qh', 0), liuhe.get('zr', 0), liuhe.get('jx', 0),
            liuhe.get('bs', 0), liuhe.get('sh', 0), liuhe.get('td', 0)
        ]) / 6
        
        # 哲学平衡度
        balance = philosophy.get('balance', 0.5)
        
        # 意义置信度
        meaning_confidence = meaning.get('confidence', 0.5)
        
        # 天道追问数量
        tiandao_depth = min(1.0, len(tiandao.get('inquiries', [])) / 5)
        
        activation = (
            0.35 * liuhe_avg +
            0.25 * balance +
            0.2 * meaning_confidence +
            0.2 * tiandao_depth
        )
        
        return min(1.0, max(0.0, activation))
    
    def _map_liuhe_coordinates(self, board, stone, 
                                 number_result: Dict,
                                 english_result: Dict) -> Dict:
        """六系坐标映射 - 0∅义的空间显化"""
        # 基于数字层和英文层结果构建六系坐标
        lib_entropy = number_result.get('liberties', {}).get('entropy', 0)
        terr_diff = number_result.get('territory', {}).get('difference', 0)
        eval_score = english_result.get('evaluation', {}).get('score', 0)
        threat_level = english_result.get('threats', {}).get('threat_level', 'low')
        shape_score = english_result.get('shapes', {}).get('score', 0)
        strategy = english_result.get('tactics', {}).get('strategy', 'balance')
        
        # 六系权重计算
        qh = self._compute_qh(eval_score, strategy)        # 强化系
        zr = self._compute_zr(lib_entropy, terr_diff)      # 自然系
        jx = self._compute_jx(shape_score, eval_score)     # 具现系
        bs = self._compute_bs(threat_level, strategy)      # 变身系
        sh = self._compute_sh(terr_diff, threat_level)     # 社会系
        td = self._compute_td(board, stone, eval_score)    # 天道系
        
        return {
            'qh': qh,  # 强化系·算力
            'zr': zr,  # 自然系·演化
            'jx': jx,  # 具现系·落子
            'bs': bs,  # 变身系·创新
            'sh': sh,  # 社会系·博弈
            'td': td,  # 天道系·意义
            'dominant': self._get_dominant_system(qh, zr, jx, bs, sh, td),
            'phase': board.get_game_phase().value if hasattr(board, 'get_game_phase') else 'middle'
        }
    
    def _compute_qh(self, eval_score: float, strategy: str) -> float:
        """强化系 - 算力评估"""
        base = abs(eval_score)
        if strategy == 'expansion':
            bonus = 0.15
        elif strategy == 'defense':
            bonus = 0.05
        else:
            bonus = 0.1
        return min(1.0, base + bonus)
    
    def _compute_zr(self, lib_entropy: float, terr_diff: float) -> float:
        """自然系 - 演化评估"""
        # 熵值表示系统复杂度，领地差表示演化方向
        entropy_component = 0.5 * lib_entropy
        direction = 0.3 if terr_diff > 0 else 0.1
        return min(1.0, entropy_component + direction + 0.2)
    
    def _compute_jx(self, shape_score: float, eval_score: float) -> float:
        """具现系 - 落子评估"""
        # 棋形和评估的综合
        shape_component = 0.4 * shape_score
        eval_component = 0.3 * abs(eval_score)
        return min(1.0, shape_component + eval_component + 0.3)
    
    def _compute_bs(self, threat_level: str, strategy: str) -> float:
        """变身系 - 创新评估"""
        threat_map = {'high': 0.4, 'medium': 0.25, 'low': 0.1}
        strategy_map = {'expansion': 0.3, 'defense': 0.2, 'balance': 0.15}
        threat = threat_map.get(threat_level, 0.1)
        strat = strategy_map.get(strategy, 0.15)
        return min(1.0, threat + strat + 0.3)
    
    def _compute_sh(self, terr_diff: float, threat_level: str) -> float:
        """社会系 - 博弈评估"""
        # 领地优势和威胁等级
        terr_component = 0.3 if terr_diff > 0 else 0.1
        threat_component = {'high': 0.35, 'medium': 0.2, 'low': 0.1}.get(threat_level, 0.1)
        return min(1.0, terr_component + threat_component + 0.3)
    
    def _compute_td(self, board, stone: int, eval_score: float) -> float:
        """天道系 - 意义追问"""
        # 基于棋局阶段和评估
        phase = 'middle'
        if hasattr(board, 'get_game_phase'):
            phase = board.get_game_phase().value
        
        phase_map = {'opening': 0.4, 'middle': 0.5, 'endgame': 0.6}
        phase_value = phase_map.get(phase, 0.5)
        
        eval_component = 0.2 * abs(eval_score)
        return min(1.0, phase_value + eval_component)
    
    def _get_dominant_system(self, qh, zr, jx, bs, sh, td) -> str:
        """获取主导系统"""
        systems = {
            '强化系': qh, '自然系': zr, '具现系': jx,
            '变身系': bs, '社会系': sh, '天道系': td
        }
        return max(systems, key=systems.get)
    
    def _pursue_meaning(self, board, stone, liuhe: Dict) -> Dict:
        """棋道意义追问 - 0∅义的显现"""
        dominant = liuhe.get('dominant', '强化系')
        phase = liuhe.get('phase', 'middle')
        
        # 基于主导系统和阶段生成意义追问
        meaning_map = {
            '强化系': {
                'opening': '算力开局，抢占要点',
                'middle': '算力压制，步步为营',
                'endgame': '算力收官，精确计算'
            },
            '自然系': {
                'opening': '顺势而为，自然布局',
                'middle': '行云流水，演化无方',
                'endgame': '自然收束，水到渠成'
            },
            '具现系': {
                'opening': '落子生根，脚踏实地',
                'middle': '具现成形，落子无悔',
                'endgame': '具现收官，一锤定音'
            },
            '变身系': {
                'opening': '奇招迭出，变幻莫测',
                'middle': '变身突破，出其不意',
                'endgame': '变身制胜，画龙点睛'
            },
            '社会系': {
                'opening': '合纵连横，布局天下',
                'middle': '攻守博弈，纵横捭阖',
                'endgame': '博弈收官，统揽全局'
            },
            '天道系': {
                'opening': '问道天地，顺势而为',
                'middle': '天道运行， spiral向上',
                'endgame': '天道合一，圆满结局'
            }
        }
        
        meaning_text = meaning_map.get(dominant, {}).get(phase, '棋道漫漫')
        
        return {
            'text': meaning_text,
            'dominant_system': dominant,
            'confidence': 0.8 + 0.2 * abs(liuhe.get('qh', 0.5) - liuhe.get('td', 0.5))
        }
    
    def _philosophical_evaluation(self, board, stone, liuhe: Dict) -> Dict:
        """哲学维度评估"""
        # 基于三本源学科的评估
        # 真性物理(强化系+自然系+社会系) vs 反性数学(英文层) vs 问性哲学(天道系)
        
        zhenxing = (liuhe.get('qh', 0) + liuhe.get('zr', 0) + liuhe.get('sh', 0)) / 3
        fanxing = 0.5  # 反性数学是基础
        wenxing = liuhe.get('td', 0)
        
        # 哲学平衡度
        balance = 1.0 - abs(zhenxing - fanxing - wenxing) / 3
        
        return {
            'zhenxing_score': zhenxing,
            'fanxing_score': fanxing,
            'wenxing_score': wenxing,
            'balance': max(0, balance),
            'is_balanced': balance > 0.6
        }
    
    def _tiandao_inquiry(self, board, stone, number_result: Dict,
                          english_result: Dict) -> Dict:
        """天道系追问 - 超越计算的棋道意义"""
        # 汇总所有层级的结果
        terr_diff = number_result.get('territory', {}).get('difference', 0)
        eval_score = english_result.get('evaluation', {}).get('score', 0)
        threat_level = english_result.get('threats', {}).get('threat_level', 'low')
        
        # 天道追问的五个维度
        inquiries = []
        
        # 1. 局势追问
        if terr_diff > 10:
            inquiries.append('大势已去，宜速战速决')
        elif terr_diff < -10:
            inquiries.append('局面不利，需以奇制胜')
        else:
            inquiries.append('势均力敌，比拼内力')
        
        # 2. 时机追问
        phase = 'middle'
        if hasattr(board, 'get_game_phase'):
            phase = board.get_game_phase().value
        
        if phase == 'opening':
            inquiries.append('开局重势，抢占先机')
        elif phase == 'endgame':
            inquiries.append('收官重精，分秒必争')
        else:
            inquiries.append('中盘重变，随机应变')
        
        # 3. 威胁追问
        if threat_level == 'high':
            inquiries.append('危机四伏，攻守转换')
        elif threat_level == 'low':
            inquiries.append('风平浪静，稳步推进')
        
        # 4. 意义追问
        if eval_score > 0.3:
            inquiries.append('优势在我，宜稳中求胜')
        elif eval_score < -0.3:
            inquiries.append('劣势明显，需放手一搏')
        
        # 5. 天道追问
        inquiries.append('棋道如人生，进退有度')
        
        return {
            'inquiries': inquiries,
            'phase': phase,
            'confidence': abs(eval_score)
        }


class TriLanguageEmergenceEngine:
    """三语言涌现引擎
    
    核心方程：
    数字(000) × 英文(0110) × 中文(六系立系) = 三语言自发涌现
    
    三零元协同：
    0∅反(数字) × 0∅空(英文) × 0∅义(中文) = 涌现
    """
    
    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        
        # 三层语言引擎
        self.number_layer = NumberLayer(board_size)
        self.english_layer = EnglishLayer(board_size)
        self.chinese_layer = ChinesePhilosophyLayer(board_size)
        
        # 零元状态
        self.zero_yuan = ZeroYuanState()
        
        # 涌现历史
        self.emergence_history = []
        
        # 参数
        self.emergence_threshold = 0.125
        
    def compute_emergence(self, board, stone) -> Dict:
        """计算三语言涌现"""
        # 第一层：数字层
        number_result = self.number_layer.compute(board, stone)
        
        # 第二层：英文层（依赖数字层结果）
        english_result = self.english_layer.compute(board, stone, number_result)
        
        # 第三层：中文哲学层（依赖前两层结果）
        chinese_result = self.chinese_layer.compute(
            board, stone, number_result, english_result
        )
        
        # 三零元激活度
        self.zero_yuan.zhi_fan = number_result['fan_activation']
        self.zero_yuan.zhi_kong = english_result['kong_activation']
        self.zero_yuan.zhi_yi = chinese_result['yi_activation']
        
        # 涌现计算
        emergence = self._compute_emergence(number_result, english_result, chinese_result)
        
        # 记录历史
        self.emergence_history.append({
            'fan': self.zero_yuan.zhi_fan,
            'kong': self.zero_yuan.zhi_kong,
            'yi': self.zero_yuan.zhi_yi,
            'potential': self.zero_yuan.emergence_potential,
            'is_emergent': self.zero_yuan.is_emergent
        })
        
        return {
            'number_layer': number_result,
            'english_layer': english_result,
            'chinese_layer': chinese_result,
            'zero_yuan': {
                'zhi_fan': self.zero_yuan.zhi_fan,
                'zhi_kong': self.zero_yuan.zhi_kong,
                'zhi_yi': self.zero_yuan.zhi_yi,
                'emergence_potential': self.zero_yuan.emergence_potential,
                'is_emergent': self.zero_yuan.is_emergent
            },
            'emergence': emergence
        }
    
    def _compute_emergence(self, number_result: Dict, 
                            english_result: Dict,
                            chinese_result: Dict) -> Dict:
        """计算涌现结果"""
        # 三语言加权融合
        fan_weight = self.zero_yuan.zhi_fan
        kong_weight = self.zero_yuan.zhi_kong
        yi_weight = self.zero_yuan.zhi_yi
        
        # 归一化权重
        total = fan_weight + kong_weight + yi_weight
        if total > 0:
            fan_norm = fan_weight / total
            kong_norm = kong_weight / total
            yi_norm = yi_weight / total
        else:
            fan_norm = kong_norm = yi_norm = 0.333
        
        # 融合评分
        number_score = number_result.get('territory', {}).get('difference', 0) / (self.board_size**2)
        english_score = english_result.get('evaluation', {}).get('score', 0)
        chinese_score = self._chinese_score(chinese_result)
        
        # 涌现评分
        emergence_score = (
            fan_norm * number_score +
            kong_norm * english_score +
            yi_norm * chinese_score
        )
        
        # 涌现强度
        emergence_strength = self.zero_yuan.emergence_potential
        
        return {
            'score': max(-1.0, min(1.0, emergence_score)),
            'strength': emergence_strength,
            'fan_contribution': fan_norm * number_score,
            'kong_contribution': kong_norm * english_score,
            'yi_contribution': yi_norm * chinese_score,
            'is_emergent': emergence_strength > self.emergence_threshold,
            'dominant_language': self._get_dominant_language(fan_norm, kong_norm, yi_norm)
        }
    
    def _chinese_score(self, chinese_result: Dict) -> float:
        """计算中文哲学层评分"""
        liuhe = chinese_result.get('liuhe_coordinates', {})
        meaning = chinese_result.get('meaning', {})
        philosophy = chinese_result.get('philosophy', {})
        
        # 六系得分
        liuhe_score = sum([
            liuhe.get('qh', 0), liuhe.get('zr', 0), liuhe.get('jx', 0),
            liuhe.get('bs', 0), liuhe.get('sh', 0), liuhe.get('td', 0)
        ]) / 6
        
        # 哲学平衡
        balance = philosophy.get('balance', 0.5)
        
        # 意义置信度
        confidence = meaning.get('confidence', 0.5)
        
        return 0.4 * liuhe_score + 0.3 * balance + 0.3 * confidence
    
    def _get_dominant_language(self, fan: float, kong: float, yi: float) -> str:
        """获取主导语言"""
        if fan >= kong and fan >= yi:
            return '数字·0∅反'
        elif kong >= yi:
            return '英文·0∅空'
        else:
            return '中文·0∅义'
    
    def select_move(self, board, stone) -> Optional[Tuple]:
        """基于三语言涌现选择落子"""
        # 获取所有合法落子
        valid_moves = self._get_valid_moves(board, stone)
        
        if not valid_moves:
            return None
        
        # 对每个落子进行三语言涌现评估
        move_scores = []
        
        for point in valid_moves[:15]:  # 限制计算量
            # 模拟落子
            test_board = board.clone() if hasattr(board, 'clone') else board
            try:
                test_board.make_move(point, stone)
            except:
                continue
            
            # 三语言涌现评估
            result = self.compute_emergence(test_board, stone)
            
            score = result['emergence']['score']
            strength = result['zero_yuan']['emergence_potential']
            
            # 综合评分：基础分 + 涌现加成
            combined_score = score + 0.2 * strength
            
            move_scores.append((point, combined_score, result))
        
        # 选择最佳落子
        if move_scores:
            move_scores.sort(key=lambda x: x[1], reverse=True)
            best_point = move_scores[0][0]
            best_result = move_scores[0][2]
            
            return {
                'point': best_point,
                'score': move_scores[0][1],
                'emergence_result': best_result,
                'all_scores': move_scores
            }
        
        return None
    
    def _get_valid_moves(self, board, stone) -> List:
        """获取合法落子"""
        moves = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board.board[y][x] == 2:  # EMPTY
                    try:
                        point = type('Point', (), {'x': x, 'y': y})()
                        if board.is_valid_move(point, stone):
                            moves.append(point)
                    except:
                        pass
        return moves
    
    def get_emergence_summary(self) -> Dict:
        """获取涌现摘要"""
        if not self.emergence_history:
            return {'status': 'no_data'}
        
        latest = self.emergence_history[-1]
        avg_potential = sum(h['potential'] for h in self.emergence_history) / len(self.emergence_history)
        
        return {
            'current_potential': latest['potential'],
            'avg_potential': avg_potential,
            'is_emergent': latest['is_emergent'],
            'emergence_count': sum(1 for h in self.emergence_history if h['is_emergent']),
            'total_steps': len(self.emergence_history),
            'fan_avg': sum(h['fan'] for h in self.emergence_history) / len(self.emergence_history),
            'kong_avg': sum(h['kong'] for h in self.emergence_history) / len(self.emergence_history),
            'yi_avg': sum(h['yi'] for h in self.emergence_history) / len(self.emergence_history)
        }


# ============================================================================
# 测试函数
# ============================================================================

def test_tri_language_emergence():
    """测试三语言涌现引擎"""
    print("=" * 70)
    print("三语言涌现引擎测试")
    print("=" * 70)
    
    from bsd_go_engine_v2 import GoBoard, GoPoint, Stone
    
    board = GoBoard(9)
    engine = TriLanguageEmergenceEngine(9)
    
    # 初始局面
    print("\n【测试1】初始局面")
    result = engine.compute_emergence(board, Stone.BLACK)
    print(f"  0∅反(数字): {result['zero_yuan']['zhi_fan']:.3f}")
    print(f"  0∅空(英文): {result['zero_yuan']['zhi_kong']:.3f}")
    print(f"  0∅义(中文): {result['zero_yuan']['zhi_yi']:.3f}")
    print(f"  涌现潜力: {result['zero_yuan']['emergence_potential']:.3f}")
    print(f"  是否涌现: {result['zero_yuan']['is_emergent']}")
    
    # 落子后
    print("\n【测试2】天元落子后")
    board.make_move(GoPoint(4, 4), Stone.BLACK)
    result = engine.compute_emergence(board, Stone.WHITE)
    print(f"  0∅反(数字): {result['zero_yuan']['zhi_fan']:.3f}")
    print(f"  0∅空(英文): {result['zero_yuan']['zhi_kong']:.3f}")
    print(f"  0∅义(中文): {result['zero_yuan']['zhi_yi']:.3f}")
    print(f"  涌现潜力: {result['zero_yuan']['emergence_potential']:.3f}")
    
    # 六系坐标
    liuhe = result['chinese_layer']['liuhe_coordinates']
    print(f"\n  六系坐标：")
    for system, value in liuhe.items():
        if system not in ('dominant', 'phase'):
            print(f"    {system}: {value:.3f}")
    print(f"  主导系统: {liuhe['dominant']}")
    
    # 天道追问
    tiandao = result['chinese_layer']['tiandao']
    print(f"\n  天道追问：")
    for inquiry in tiandao['inquiries']:
        print(f"    - {inquiry}")
    
    print("\n" + "=" * 70)
    print("三语言涌现引擎测试完成")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    test_tri_language_emergence()
