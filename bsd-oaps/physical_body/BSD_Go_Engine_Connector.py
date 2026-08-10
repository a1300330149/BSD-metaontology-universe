#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋引擎连接器 (Go Engine Connector)
==========================================

核心定位：连接与激活散落的引擎，而非合并成单一文件。
理论依据：0×0=n 双零涌现——多引擎连接产生协同增益。

设计哲学：
- 散落的引擎各有独特能力，不应被合并消解
- 连接器只做"连接·路由·激活"，不重新实现引擎逻辑
- 每个引擎保持独立，通过连接器实现协同

已发现的散落引擎清单：
┌────────────────────────────────────────────────────────────────┐
│ ID  │ 文件                              │ 核心能力                  │
├─────┼────────────────────────────────────┼─────────────────────────┤
│ E01 │ BSD_Go_QuickTest.py               │ 简易棋盘+简化基因库       │
│ E02 │ BSD_Go_Dream_Engine.py            │ V1白日梦·DNA重组         │
│ E03 │ BSD_Go_Dream_Engine_V2.py         │ V2真实定式+战术基因      │
│ E04 │ BSD_Go_Dream_Engine_V3.py         │ V3差异化对比              │
│ E05 │ BSD_Go_GenePool_V2.py             │ V2独立基因库              │
│ E06 │ BSD_Go_Quantum_Dream_Engine.py    │ V6量子退火+多比特纠缠    │
│ E07 │ BSD_Go_Engine_V9_Integrated.py    │ V9三语言涌现深度整合      │
│ E08 │ BSD_Go_Unified_Engine.py          │ V8统一主控+物理定标       │
│ E09 │ BSD_Go_Engine_V10_Unified.py      │ V10三语言深度整合         │
│ E10 │ BSD_Go_Engine_V11_Final.py        │ V11最终版                 │
│ E11 │ tri_language_emergence_engine.py  │ 三语言涌现引擎(外部模块)  │
└─────┴────────────────────────────────────┴─────────────────────────┘

连接架构：
                    ┌─────────────────┐
                    │  EngineConnector │
                    │  (连接·路由·激活) │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │ EngineRouter │   │ EngineBridge │   │  Capability  │
    │ 动态选引擎   │   │ 跨引擎协同   │   │    Mapper    │
    └─────────────┘   └─────────────┘   └─────────────┘
           │                 │                 │
    ┌──────┴─────────────────┴─────────────────┴──────┐
    ▼         ▼         ▼         ▼         ▼         ▼
  E01(简易)  E02(V1)  E03(V2)  E06(量子)  E07(V9)  E08(V8) ...

版本：V1.0 · 2026-08-04
"""

import os
import sys
import importlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field


# ============================================================
# 0. 引擎注册表（Capability Registry）
# ============================================================

@dataclass
class EngineCapability:
    """引擎能力描述符"""
    engine_id: str
    file_path: str
    module_name: str
    version: str
    capabilities: List[str]
    strengths: List[str]
    best_phase: List[str]
    priority: float = 1.0
    status: str = "discovered"  # discovered | imported | active | failed
    
    def to_dict(self) -> Dict:
        return {
            'engine_id': self.engine_id,
            'file_path': self.file_path,
            'version': self.version,
            'capabilities': self.capabilities,
            'strengths': self.strengths,
            'best_phase': self.best_phase,
            'priority': self.priority,
            'status': self.status,
        }


class EngineRegistry:
    """
    引擎注册表——管理所有散落引擎的能力清单
    
    核心功能：
    1. 记录每个引擎的文件路径、版本、核心能力
    2. 支持按能力、阶段、版本检索
    3. 追踪引擎的激活状态
    """
    
    def __init__(self):
        self._registry: Dict[str, EngineCapability] = {}
        self._init_registry()
    
    def _init_registry(self):
        """初始化——登记所有已发现的散落引擎"""
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 统一能力标签集（用于互补度计算）
        # 标签: board, genepool, dream, DNA_crossover, opening, tactic,
        #       quantum, entanglement, trigger, tri_lang, emergence,
        #       six_system, tiandao, physics, calibration, networking,
        #       unified, evolution, physics_calibration
        engines = [
            EngineCapability(
                engine_id="E01",
                file_path=os.path.join(base_dir, "BSD_Go_QuickTest.py"),
                module_name="BSD_Go_QuickTest",
                version="QuickTest",
                capabilities=["board", "genepool", "dream", "DNA_crossover"],
                strengths=["快速验证", "零依赖"],
                best_phase=["opening", "middle"],
                priority=0.3,
            ),
            EngineCapability(
                engine_id="E02",
                file_path=os.path.join(base_dir, "BSD_Go_Dream_Engine.py"),
                module_name="BSD_Go_Dream_Engine",
                version="V1",
                capabilities=["genepool", "dream", "DNA_crossover"],
                strengths=["首创白日梦机制", "200基因"],
                best_phase=["middle", "ending"],
                priority=0.5,
            ),
            EngineCapability(
                engine_id="E03",
                file_path=os.path.join(base_dir, "BSD_Go_Dream_Engine_V2.py"),
                module_name="BSD_Go_Dream_Engine_V2",
                version="V2",
                capabilities=["genepool", "opening", "tactic", "knowledge_base"],
                strengths=["真实棋谱", "定式+战术"],
                best_phase=["opening", "middle"],
                priority=0.6,
            ),
            EngineCapability(
                engine_id="E04",
                file_path=os.path.join(base_dir, "BSD_Go_Dream_Engine_V3.py"),
                module_name="BSD_Go_Dream_Engine_V3",
                version="V3",
                capabilities=["genepool", "dream", "DNA_crossover", "baseline_compare"],
                strengths=["A/B测试", "基线对比"],
                best_phase=["middle"],
                priority=0.4,
            ),
            EngineCapability(
                engine_id="E05",
                file_path=os.path.join(base_dir, "BSD_Go_GenePool_V2.py"),
                module_name="BSD_Go_GenePool_V2",
                version="GenePool-V2",
                capabilities=["genepool", "opening", "tactic"],
                strengths=["纯基因库", "无引擎依赖"],
                best_phase=["opening", "middle"],
                priority=0.5,
            ),
            EngineCapability(
                engine_id="E06",
                file_path=os.path.join(base_dir, "BSD_Go_Quantum_Dream_Engine.py"),
                module_name="BSD_Go_Quantum_Dream_Engine",
                version="V6",
                capabilities=["quantum", "entanglement", "trigger", 
                           "genepool", "networking", "DNA_crossover"],
                strengths=["量子计算", "4+基因纠缠", "自适应触发"],
                best_phase=["middle", "ending"],
                priority=0.9,
            ),
            EngineCapability(
                engine_id="E07",
                file_path=os.path.join(base_dir, "BSD_Go_Engine_V9_Integrated.py"),
                module_name="BSD_Go_Engine_V9_Integrated",
                version="V9",
                capabilities=["tri_lang", "emergence", "six_system", 
                           "tiandao", "physics_calibration", "DNA_crossover"],
                strengths=["三语言深度整合", "涌现方程实现"],
                best_phase=["opening", "middle", "ending", "final"],
                priority=0.85,
            ),
            EngineCapability(
                engine_id="E08",
                file_path=os.path.join(base_dir, "BSD_Go_Unified_Engine.py"),
                module_name="BSD_Go_Unified_Engine",
                version="V8",
                capabilities=["unified", "physics_calibration", "tiandao", 
                           "tri_lang", "networking", "emergence"],
                strengths=["已导入tri_language", "物理定标完备"],
                best_phase=["opening", "middle", "ending"],
                priority=0.9,
            ),
            EngineCapability(
                engine_id="E09",
                file_path=os.path.join(base_dir, "BSD_Go_Engine_V10_Unified.py"),
                module_name="BSD_Go_Engine_V10_Unified",
                version="V10",
                capabilities=["tri_lang", "emergence", "six_system", 
                           "tiandao", "quantum", "DNA_crossover", "networking"],
                strengths=["V9+V10整合", "统一评估函数"],
                best_phase=["opening", "middle", "ending", "final"],
                priority=0.88,
            ),
            EngineCapability(
                engine_id="E10",
                file_path=os.path.join(base_dir, "BSD_Go_Engine_V11_Final.py"),
                module_name="BSD_Go_Engine_V11_Final",
                version="V11",
                capabilities=["unified", "tri_lang", "emergence", 
                           "physics_calibration", "tiandao", "quantum", 
                           "genepool", "DNA_crossover"],
                strengths=["最终版集成", "全版本基因池"],
                best_phase=["opening", "middle", "ending", "final"],
                priority=0.92,
            ),
            EngineCapability(
                engine_id="E11",
                file_path=os.path.join(base_dir, "..", "bsd_engine", "core", 
                                       "tri_language_emergence_engine.py"),
                module_name="tri_language_emergence_engine",
                version="TriLang",
                capabilities=["tri_lang", "emergence", "six_system", 
                           "coordinate_mapping", "NumberLayer", "ChinesePhilosophyLayer"],
                strengths=["外部模块", "三语言独立实现"],
                best_phase=["opening", "middle", "ending", "final"],
                priority=0.85,
            ),
        ]
        
        for eng in engines:
            self._registry[eng.engine_id] = eng
    
    def get_engine(self, engine_id: str) -> Optional[EngineCapability]:
        return self._registry.get(engine_id)
    
    def get_all_engines(self) -> List[EngineCapability]:
        return list(self._registry.values())
    
    def find_by_capability(self, capability: str) -> List[EngineCapability]:
        """按能力检索引擎"""
        results = []
        for eng in self._registry.values():
            if capability in eng.capabilities:
                results.append(eng)
        return sorted(results, key=lambda e: e.priority, reverse=True)
    
    def find_by_phase(self, phase: str) -> List[EngineCapability]:
        """按棋局阶段检索引擎"""
        results = []
        for eng in self._registry.values():
            if phase in eng.best_phase:
                results.append(eng)
        return sorted(results, key=lambda e: e.priority, reverse=True)
    
    def get_top_engines(self, n: int = 3) -> List[EngineCapability]:
        """获取优先级最高的N个引擎"""
        return sorted(self._registry.values(), 
                      key=lambda e: e.priority, reverse=True)[:n]
    
    def update_status(self, engine_id: str, status: str):
        if engine_id in self._registry:
            self._registry[engine_id].status = status
    
    def get_status_report(self) -> Dict:
        """获取注册表状态报告"""
        by_status = {}
        for eng in self._registry.values():
            s = eng.status
            if s not in by_status:
                by_status[s] = []
            by_status[s].append(eng.engine_id)
        
        return {
            'total_engines': len(self._registry),
            'by_status': by_status,
            'engines': {k: v.to_dict() for k, v in self._registry.items()},
        }


# ============================================================
# 1. 引擎路由器（EngineRouter）
# ============================================================

@dataclass
class RouteDecision:
    """路由决策结果"""
    primary_engine: str
    secondary_engines: List[str]
    routing_reason: str
    confidence: float
    phase: str


class EngineRouter:
    """
    引擎路由器——根据棋局状态动态选择引擎
    
    路由策略：
    1. 开局(opening)：优先三语言涌现引擎(E07/E11) + 真实定式(E03/E05)
    2. 中盘(middle)：优先量子引擎(E06) + 白日梦(E02/E04)
    3. 后盘(ending)：优先物理定标(E08) + 天道追问(E07/E10)
    4. 终局(final)：优先天道追问(E07/E10) + 统一引擎(E10/E11)
    """
    
    # 阶段路由规则
    PHASE_ROUTING = {
        'opening': {
            'primary': ['E07', 'E11'],
            'secondary': ['E03', 'E05', 'E08'],
            'reason': '开局侧重三语言涌现+真实定式',
        },
        'middle': {
            'primary': ['E06', 'E07'],
            'secondary': ['E02', 'E04', 'E08'],
            'reason': '中盘侧重量子退火+白日梦DNA重组',
        },
        'ending': {
            'primary': ['E08', 'E10'],
            'secondary': ['E07', 'E06', 'E11'],
            'reason': '后盘侧重物理定标+天道追问',
        },
        'final': {
            'primary': ['E10', 'E11'],
            'secondary': ['E07', 'E08'],
            'reason': '终局侧重天道追问+全版本整合',
        },
    }
    
    def __init__(self, registry: EngineRegistry):
        self.registry = registry
        self.route_history = []
    
    def route(self, board_state: Dict, phase: str = None, 
              context: Dict = None) -> RouteDecision:
        """
        路由决策——基于阶段规则+引擎优先级联合决定
        
        Args:
            board_state: 棋盘状态信息
            phase: 棋局阶段 (opening/middle/ending/final)
            context: 上下文信息（如评估分数、候选点数等）
        """
        if phase is None:
            phase = self._detect_phase(board_state)
        
        rules = self.PHASE_ROUTING.get(phase, self.PHASE_ROUTING['middle'])
        
        # 从候选引擎中按优先级选择
        all_candidates = rules['primary'] + rules['secondary']
        valid_engines = []
        for eid in all_candidates:
            eng = self.registry.get_engine(eid)
            if eng:
                valid_engines.append(eng)
        
        valid_engines.sort(key=lambda e: e.priority, reverse=True)
        
        primary = valid_engines[0].engine_id if valid_engines else 'E01'
        secondary = [e.engine_id for e in valid_engines[1:4]]
        
        decision = RouteDecision(
            primary_engine=primary,
            secondary_engines=secondary,
            routing_reason=rules['reason'],
            confidence=self._calc_confidence(valid_engines, context),
            phase=phase,
        )
        
        self.route_history.append({
            'phase': phase,
            'decision': decision,
            'timestamp': datetime.now().isoformat(),
        })
        
        return decision
    
    def _detect_phase(self, board_state: Dict) -> str:
        """检测棋局阶段"""
        move_count = board_state.get('move_count', 0)
        total_points = board_state.get('total_points', 81)
        own_stones = board_state.get('own_stones', 0)
        opp_stones = board_state.get('opp_stones', 0)
        
        total_moves = own_stones + opp_stones
        
        if total_moves < 10:
            return 'opening'
        elif total_moves < 30:
            return 'middle'
        elif total_moves < total_points * 0.7:
            return 'ending'
        else:
            return 'final'
    
    def _calc_confidence(self, primary_engines: List[str], 
                         context: Dict) -> float:
        """计算路由置信度"""
        if not primary_engines:
            return 0.1
        
        base = 0.8
        
        if context:
            score_available = context.get('score_available', False)
            candidates_available = context.get('candidates_available', False)
            
            if score_available:
                base += 0.05
            if candidates_available:
                base += 0.05
        
        return min(1.0, base)
    
    def get_route_summary(self) -> Dict:
        """获取路由历史摘要"""
        if not self.route_history:
            return {'status': 'no_routes'}
        
        phases = {}
        for r in self.route_history:
            p = r['phase']
            if p not in phases:
                phases[p] = 0
            phases[p] += 1
        
        return {
            'total_routes': len(self.route_history),
            'phase_distribution': phases,
            'last_decision': self.route_history[-1] if self.route_history else None,
        }


# ============================================================
# 2. 引擎桥接（EngineBridge）
# ============================================================

class EngineBridge:
    """
    引擎桥接——让不同引擎协同工作
    
    桥接模式：
    1. 主引擎+副引擎并行：主引擎决策，副引擎提供候选
    2. 阶段切换：开局用引擎A，中盘切换到引擎B
    3. 能力互补：量子引擎(决策) + 基因库(知识) + 物理定标(验证)
    """
    
    def __init__(self, registry: EngineRegistry):
        self.registry = registry
        self.bridge_log = []
    
    def bridge_parallel(self, primary_id: str, secondary_ids: List[str],
                        board_state: Dict) -> Dict:
        """
        并行桥接：主引擎决策，副引擎提供候选/验证
        
        理论：0×0=n——两个引擎的连接产生协同增益
        """
        primary = self.registry.get_engine(primary_id)
        secondary = [self.registry.get_engine(sid) for sid in secondary_ids 
                     if self.registry.get_engine(sid)]
        
        result = {
            'mode': 'parallel',
            'primary_engine': primary_id,
            'secondary_engines': secondary_ids,
            'synergy_score': self._calc_synergy(primary, secondary),
            'status': 'bridged',
        }
        
        self.bridge_log.append({
            'type': 'parallel',
            'engines': [primary_id] + secondary_ids,
            'synergy': result['synergy_score'],
            'timestamp': datetime.now().isoformat(),
        })
        
        return result
    
    def bridge_chain(self, engine_chain: List[str], 
                     trigger_points: List[Dict]) -> Dict:
        """
        链式桥接：按序使用不同引擎
        
        例如：开局→E07 → 中盘→E06 → 后盘→E08 → 终局→E10
        """
        engines = [self.registry.get_engine(eid) for eid in engine_chain
                   if self.registry.get_engine(eid)]
        
        result = {
            'mode': 'chain',
            'engine_chain': engine_chain,
            'trigger_points': trigger_points,
            'chain_length': len(engines),
            'total_synergy': sum(e.priority for e in engines) / max(len(engines), 1),
            'status': 'chained',
        }
        
        self.bridge_log.append({
            'type': 'chain',
            'engine_chain': engine_chain,
            'total_synergy': result['total_synergy'],
            'timestamp': datetime.now().isoformat(),
        })
        
        return result
    
    def _calc_synergy(self, primary: EngineCapability, 
                      secondary: List[EngineCapability]) -> float:
        """计算协同增益"""
        if not secondary:
            return primary.priority
        
        cap_overlap = 0
        for sec in secondary:
            overlap = set(primary.capabilities) & set(sec.capabilities)
            cap_overlap += len(overlap) / max(len(primary.capabilities), 1)
        
        avg_overlap = cap_overlap / len(secondary)
        synergy = (primary.priority + sum(s.priority for s in secondary) / len(secondary))
        synergy *= (1.0 - 0.3 * avg_overlap)  # 能力互补提升协同
        
        return min(1.0, synergy)
    
    def get_bridge_summary(self) -> Dict:
        return {
            'total_bridges': len(self.bridge_log),
            'bridges': self.bridge_log,
        }


# ============================================================
# 3. 连接器主控（EngineConnector）
# ============================================================

class EngineConnector:
    """
    围棋引擎连接器——统一入口
    
    使用方式：
    >>> connector = EngineConnector()
    >>> 
    >>> # 获取连接关系图
    >>> graph = connector.get_connection_graph()
    >>> 
    >>> # 路由决策
    >>> decision = connector.route(board_state, phase='middle')
    >>> 
    >>> # 激活引擎（动态import）
    >>> module = connector.activate_engine('E06')
    >>> 
    >>> # 获取最佳引擎组合
    >>> best = connector.get_best_combo(phase='ending')
    """
    
    def __init__(self, auto_discover: bool = True):
        self.registry = EngineRegistry()
        self.router = EngineRouter(self.registry)
        self.bridge = EngineBridge(self.registry)
        self._active_modules: Dict[str, object] = {}
        
        if auto_discover:
            self._discover_engines()
    
    def _discover_engines(self):
        """发现并登记所有散落引擎"""
        report = self.registry.get_status_report()
        total = report['total_engines']
        print(f"[Connector] 发现 {total} 个散落引擎：")
        for eng in self.registry.get_all_engines():
            print(f"  {eng.engine_id} | {eng.version:>12} | "
                  f"priority={eng.priority:.2f} | "
                  f"capabilities={len(eng.capabilities)}项")
    
    def activate_engine(self, engine_id: str) -> Optional[object]:
        """
        激活引擎——动态import对应模块
        
        不修改引擎代码，仅通过import连接
        """
        eng = self.registry.get_engine(engine_id)
        if not eng:
            print(f"[Connector] 引擎 {engine_id} 未找到")
            return None
        
        if engine_id in self._active_modules:
            return self._active_modules[engine_id]
        
        try:
            module_dir = os.path.dirname(eng.file_path)
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            
            if eng.engine_id == 'E11':
                # 三语言引擎在外部路径
                ext_dir = os.path.join(os.path.dirname(eng.file_path), 
                                       '..', 'bsd_engine', 'core')
                if ext_dir not in sys.path:
                    sys.path.insert(0, ext_dir)
            
            module = importlib.import_module(eng.module_name)
            self._active_modules[engine_id] = module
            self.registry.update_status(engine_id, "active")
            print(f"[Connector] 激活 {engine_id} ({eng.version}) ✓")
            return module
            
        except ImportError as e:
            self.registry.update_status(engine_id, "failed")
            print(f"[Connector] 激活 {engine_id} 失败: {e}")
            return None
    
    def activate_top_n(self, n: int = 3) -> Dict[str, bool]:
        """激活优先级最高的N个引擎"""
        top = self.registry.get_top_engines(n)
        results = {}
        for eng in top:
            module = self.activate_engine(eng.engine_id)
            results[eng.engine_id] = module is not None
        return results
    
    def route(self, board_state: Dict, phase: str = None,
              context: Dict = None) -> RouteDecision:
        """路由决策"""
        return self.router.route(board_state, phase, context)
    
    def get_best_combo(self, phase: str = 'middle', 
                       strategy: str = 'parallel') -> Dict:
        """
        获取最佳引擎组合
        
        Args:
            phase: 棋局阶段
            strategy: 'parallel'(并行) | 'chain'(链式)
        """
        decision = self.router.route({}, phase=phase)
        
        if strategy == 'parallel':
            bridge_result = self.bridge.bridge_parallel(
                decision.primary_engine,
                decision.secondary_engines,
                {}
            )
        else:
            chain = [decision.primary_engine] + decision.secondary_engines
            bridge_result = self.bridge.bridge_chain(chain, [])
        
        return {
            'decision': decision,
            'bridge': bridge_result,
            'engines_involved': [decision.primary_engine] + decision.secondary_engines,
        }
    
    def get_connection_graph(self) -> Dict:
        """
        获取连接关系图
        
        返回所有引擎的能力矩阵和连接建议
        """
        engines = self.registry.get_all_engines()
        
        # 能力矩阵
        cap_matrix = {}
        for eng in engines:
            cap_matrix[eng.engine_id] = {
                'version': eng.version,
                'priority': eng.priority,
                'capabilities': eng.capabilities,
                'strengths': eng.strengths,
                'best_phase': eng.best_phase,
                'status': eng.status,
            }
        
        # 连接建议（基于能力互补）
        connections = self._suggest_connections(engines)
        
        # 阶段推荐
        phase_recs = {}
        for phase in ['opening', 'middle', 'ending', 'final']:
            engines_for_phase = self.registry.find_by_phase(phase)
            phase_recs[phase] = [
                {'id': e.engine_id, 'version': e.version, 'priority': e.priority}
                for e in engines_for_phase[:3]
            ]
        
        return {
            'total_engines': len(engines),
            'capability_matrix': cap_matrix,
            'suggested_connections': connections,
            'phase_recommendations': phase_recs,
            'top_engines': [
                {'id': e.engine_id, 'version': e.version, 'priority': e.priority}
                for e in self.registry.get_top_engines(5)
            ],
        }
    
    def _suggest_connections(self, engines: List[EngineCapability]) -> List[Dict]:
        """
        建议连接关系
        
        基于能力互补性：两个引擎能力重叠度低 → 互补性强
        """
        suggestions = []
        
        for i, eng_a in enumerate(engines):
            for eng_b in engines[i+1:]:
                caps_a = set(eng_a.capabilities)
                caps_b = set(eng_b.capabilities)
                
                overlap = caps_a & caps_b
                union = caps_a | caps_b
                
                if len(union) == 0:
                    continue
                
                complementarity = 1.0 - len(overlap) / len(union)
                
                if complementarity > 0.5:  # 互补性阈值
                    suggestions.append({
                        'engine_a': eng_a.engine_id,
                        'engine_b': eng_b.engine_id,
                        'complementarity': round(complementarity, 3),
                        'shared_capabilities': list(overlap),
                        'unique_to_a': list(caps_a - caps_b),
                        'unique_to_b': list(caps_b - caps_a),
                        'recommendation': 'strong' if complementarity > 0.7 else 'moderate',
                    })
        
        suggestions.sort(key=lambda s: s['complementarity'], reverse=True)
        return suggestions[:10]
    
    def get_stats(self) -> Dict:
        """连接器统计"""
        status = self.registry.get_status_report()
        router_summary = self.router.get_route_summary()
        bridge_summary = self.bridge.get_bridge_summary()
        
        return {
            'connector_version': 'V1.0',
            'discovered_engines': status['total_engines'],
            'active_engines': len(self._active_modules),
            'by_status': status['by_status'],
            'routes': router_summary,
            'bridges': bridge_summary,
        }


# ============================================================
# 4. 演示与验证
# ============================================================

def main():
    """连接器演示"""
    print("=" * 70)
    print("BSD 围棋引擎连接器 V1.0")
    print("=" * 70)
    
    # 1. 创建连接器（自动发现所有散落引擎）
    connector = EngineConnector(auto_discover=True)
    
    print("\n" + "=" * 70)
    print("【连接关系图】")
    print("=" * 70)
    
    graph = connector.get_connection_graph()
    
    print(f"\n引擎总数: {graph['total_engines']}")
    
    print("\n【优先级Top 5】")
    for i, eng in enumerate(graph['top_engines']):
        print(f"  #{i+1} {eng['id']} ({eng['version']}) priority={eng['priority']:.2f}")
    
    print("\n【阶段推荐】")
    for phase, engines in graph['phase_recommendations'].items():
        print(f"\n  {phase}:")
        for eng in engines:
            print(f"    → {eng['id']} ({eng['version']}) p={eng['priority']:.2f}")
    
    print("\n【能力互补连接建议】")
    for conn in graph['suggested_connections'][:5]:
        print(f"  {conn['engine_a']} ↔ {conn['engine_b']} | "
              f"互补性={conn['complementarity']:.2f} | "
              f"推荐={conn['recommendation']}")
    
    print("\n" + "=" * 70)
    print("【激活引擎】")
    print("=" * 70)
    
    # 激活优先级最高的3个引擎
    activation_results = connector.activate_top_n(3)
    for eid, success in activation_results.items():
        status = "✓ 已激活" if success else "✗ 失败"
        print(f"  {eid}: {status}")
    
    print("\n" + "=" * 70)
    print("【路由决策演示】")
    print("=" * 70)
    
    # 模拟棋局状态
    for phase in ['opening', 'middle', 'ending', 'final']:
        board_state = {
            'move_count': 15 if phase == 'opening' else 
                         25 if phase == 'middle' else 
                         45 if phase == 'ending' else 70,
            'total_points': 81,
            'own_stones': 8 if phase == 'opening' else 
                         15 if phase == 'middle' else 
                         25 if phase == 'ending' else 35,
            'opp_stones': 7 if phase == 'opening' else 
                         14 if phase == 'middle' else 
                         24 if phase == 'ending' else 34,
        }
        
        decision = connector.route(board_state, phase=phase)
        print(f"\n  {phase}:")
        print(f"    主引擎: {decision.primary_engine}")
        print(f"    副引擎: {decision.secondary_engines}")
        print(f"    理由: {decision.routing_reason}")
        print(f"    置信度: {decision.confidence:.2f}")
    
    print("\n" + "=" * 70)
    print("【引擎组合推荐】")
    print("=" * 70)
    
    for phase in ['opening', 'middle', 'ending', 'final']:
        combo = connector.get_best_combo(phase=phase, strategy='parallel')
        engines = combo['engines_involved']
        synergy = combo['bridge']['synergy_score']
        print(f"\n  {phase}: {engines} → 协同分={synergy:.3f}")
    
    print("\n" + "=" * 70)
    print("【连接器统计】")
    print("=" * 70)
    
    stats = connector.get_stats()
    print(f"  已发现引擎: {stats['discovered_engines']}")
    print(f"  已激活引擎: {stats['active_engines']}")
    print(f"  路由次数: {stats['routes']['total_routes']}")
    print(f"  桥接次数: {stats['bridges']['total_bridges']}")
    
    print("\n" + "=" * 70)
    print("连接器就绪——散落引擎已连接")
    print("=" * 70)
    
    return connector


if __name__ == '__main__':
    main()