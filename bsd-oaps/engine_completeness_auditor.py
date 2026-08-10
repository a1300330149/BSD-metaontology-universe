#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引擎完备性审计系统 (Engine Completeness Auditor)
==================================================

核心洞察：
    引擎的本质 = 定理的纯系开发 + 复合
    
    「纯系开发」：将单一理论公理转化为独立引擎模块
    「复合」：将多个纯系引擎组合成更复杂的系统
    
    历史问题：引擎从六系立系论中途开始开发 → 
    1. 很多理论并未完成引擎化（有理论无引擎）
    2. 引擎间缺乏理论层面的系统组合（有引擎无理论复合）
    3. 缺乏从理论到引擎的完整追溯链
    
审计目标：
    1. 理论欠债审计：找出哪些理论没有对应的引擎实现
    2. 引擎完备性评估：每个引擎是否完整实现了对应理论
    3. 复合机会识别：哪些现有引擎可以理论层面复合
    4. 纯系开发建议：基于理论欠债，给出纯系开发清单
"""

import os
import sys
import re
import json
import ast
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ============================================================
# 0. 路径常量
# ============================================================
_BSD_OAPS_PATH = os.path.dirname(os.path.abspath(__file__))
if _BSD_OAPS_PATH not in sys.path:
    sys.path.insert(0, _BSD_OAPS_PATH)

_THEORY_BASE_PATH = os.path.join(os.path.dirname(_BSD_OAPS_PATH), 'theory_base')
_BSD_ENGINE_PATH = os.path.join(_BSD_OAPS_PATH, 'bsd_engine')
_BSD_CORE_PATH = os.path.join(_BSD_ENGINE_PATH, 'core')


# ============================================================
# 1. 审计维度定义
# ============================================================

class AuditDimension(Enum):
    """审计维度"""
    THEORY_COVERAGE = "理论覆盖度"         # 理论→引擎的覆盖
    ENGINE_COMPLETENESS = "引擎完备性"     # 引擎→理论的实现
    COMPOSITION_READINESS = "复合就绪度"   # 引擎间可组合性
    PURE_SYSTEM_READINESS = "纯系就绪度"   # 纯系开发就绪度


class DebtLevel(Enum):
    """欠债等级"""
    CRITICAL = "严重欠债"     # 核心公理无引擎实现
    HIGH = "高优先欠债"       # 重要理论无引擎
    MEDIUM = "中等欠债"       # 一般理论无引擎
    LOW = "低优先欠债"       # 边缘理论无引擎
    NONE = "无欠债"          # 已完全引擎化


class EngineLevel(Enum):
    """引擎完备性等级"""
    COMPLETE = "完备"        # 理论完全实现
    MOSTLY_COMPLETE = "基本完备"  # 核心功能已实现
    PARTIAL = "部分完备"     # 部分功能实现
    MINIMAL = "最小实现"    # 仅有框架
    MISSING = "缺失"        # 无引擎实现


# ============================================================
# 2. 理论-引擎欠债矩阵
# ============================================================

# 核心公理清单（从theory_base提取）
CORE_AXIOM_LIST: List[Dict[str, Any]] = [
    {
        'axiom_id': 'A0',
        'name': '公理0·元道存在',
        'six_system': '强化系🔵',
        'theory_layer': 'L0_总本源层',
        'core_content': '元道是一切存在的起点，0元本体论大一统',
        'expected_engines': ['theory_hub', 'six_system_bootstrap_engine', 'origin_triple_zero'],
        'priority': 'CRITICAL',
    },
    {
        'axiom_id': 'A1',
        'name': '公理1·物质存在',
        'six_system': '自然系🟠',
        'theory_layer': 'L0_总本源层',
        'core_content': '物质世界的客观存在与规律',
        'expected_engines': ['theory_driven_engine', 'six_system_project_mapper', 'free_connection_protocol'],
        'priority': 'CRITICAL',
    },
    {
        'axiom_id': 'A2',
        'name': '公理2·生命涌现',
        'six_system': '具现系🔴',
        'theory_layer': 'L0_总本源层',
        'core_content': '生命从非生命涌现的自组织过程',
        'expected_engines': ['life_emergence_engine', 'cross_origin_weight_mapper', 'phase_transition'],
        'priority': 'CRITICAL',
    },
    {
        'axiom_id': 'A3',
        'name': '公理3·意识存在',
        'six_system': '变身系⚫',
        'theory_layer': 'L0_总本源层',
        'core_content': '意识的本质及其与物质的关系',
        'expected_engines': ['dual_polarity_spawner', 'theory_deep_reader', 'tri_source_engineering'],
        'priority': 'HIGH',
    },
    {
        'axiom_id': 'A4',
        'name': '公理4·社会存在',
        'six_system': '社会系🟢',
        'theory_layer': 'L1_不动母科层',
        'core_content': '社会秩序的形成与维持',
        'expected_engines': ['institutional_economics', 'six_system_completion_suite', 'global_entropy_conservation_judge'],
        'priority': 'HIGH',
    },
    {
        'axiom_id': 'A5',
        'name': '公理5·天道存在',
        'six_system': '天道系🟣',
        'theory_layer': 'L0_总本源层',
        'core_content': '宇宙的终极规律与计算极限',
        'expected_engines': ['cosmological_constant', 'standing_wave', 'void_potential_accumulator'],
        'priority': 'CRITICAL',
    },
    {
        'axiom_id': 'A6',
        'name': '公理6·六系自组织',
        'six_system': '全局',
        'theory_layer': 'L0_总本源层',
        'core_content': '六系之间的自组织与传导',
        'expected_engines': ['six_system_self_organization_engine', 'six_system_conduction_engine', 'six_system_nested_coupling'],
        'priority': 'CRITICAL',
    },
    {
        'axiom_id': 'A7',
        'name': '公理7·反真问系',
        'six_system': '全局',
        'theory_layer': 'L0_总本源层',
        'core_content': '从子集回到本源的逆原路径',
        'expected_engines': ['reverse_three_stage_transformer', 'reverse_entropy_calculator', 'zero_one_to_liuhe_engine'],
        'priority': 'HIGH',
    },
    {
        'axiom_id': 'A8',
        'name': '公理8·光气算思同构',
        'six_system': '全局',
        'theory_layer': 'L0_总本源层',
        'core_content': '光、气、算、思的同构关系',
        'expected_engines': ['particle_family_engine', 'sphere_coordinate_engine', 'void_potential_accumulator'],
        'priority': 'MEDIUM',
    },
    {
        'axiom_id': 'A9',
        'name': '公理9·计算即引力',
        'six_system': '社会系🟢',
        'theory_layer': 'L2_无限展开层',
        'core_content': '系统通过计算形成的等式维持连接与秩序',
        'expected_engines': ['standing_wave', 'entropy_flow', 'structural_entropy'],
        'priority': 'MEDIUM',
    },
    {
        'axiom_id': 'A10',
        'name': '公理10·计变即暗物质',
        'six_system': '天道系🟣',
        'theory_layer': 'L2_无限展开层',
        'core_content': '计算变化构成系统的暗物质',
        'expected_engines': ['cosmological_constant', 'global_coherence', 'steady_state_potential'],
        'priority': 'MEDIUM',
    },
]


# ============================================================
# 3. 审计数据模型
# ============================================================

@dataclass
class TheoryDebtItem:
    """理论欠债项"""
    axiom_id: str
    axiom_name: str
    six_system: str
    theory_layer: str
    debt_level: DebtLevel
    missing_engines: List[str]
    existing_engines: List[str]
    completion_rate: float  # 0-1
    pure_dev_plan: List[str]
    notes: str = ""


@dataclass
class EngineCompletenessItem:
    """引擎完备性项"""
    engine_name: str
    engine_path: str
    six_system: str
    implemented_axioms: List[str]
    missing_axioms: List[str]
    completeness_level: EngineLevel
    code_lines: int
    has_tests: bool
    has_doc: bool


@dataclass
class CompositionOpportunity:
    """复合机会项"""
    composition_id: str
    engines_to_compose: List[str]
    composite_goal: str
    shared_theory: List[str]
    composition_difficulty: str  # low/medium/high
    expected_benefit: str


@dataclass
class AuditReport:
    """审计报告"""
    report_id: str
    generated_at: str
    theory_debts: List[TheoryDebtItem]
    engine_completeness: List[EngineCompletenessItem]
    composition_opportunities: List[CompositionOpportunity]
    summary: Dict[str, Any]


# ============================================================
# 4. 引擎完备性审计器（核心类）
# ============================================================

class EngineCompletenessAuditor:
    """
    引擎完备性审计器
    
    审计逻辑：
    1. 理论欠债审计：CORE_AXIOM_LIST中的每条公理 → 检查预期引擎是否存在
    2. 引擎完备性评估：扫描所有引擎 → 评估其实现的公理数量
    3. 复合机会识别：分析引擎组合可能性 → 提出复合方案
    4. 纯系开发建议：基于审计结果 → 生成纯系开发清单
    """
    
    def __init__(self):
        self.engines: Dict[str, Dict[str, Any]] = {}
        self.theory_debts: List[TheoryDebtItem] = []
        self.completeness_items: List[EngineCompletenessItem] = []
        self.composition_opportunities: List[CompositionOpportunity] = []
    
    # ----------------------------------------------------------
    # 4.1 扫描引擎库
    # ----------------------------------------------------------
    
    def scan_engine_library(self) -> Dict[str, Any]:
        """扫描所有引擎文件"""
        print("\n" + "=" * 60)
        print("【引擎审计】扫描引擎库...")
        print("=" * 60)
        
        scanned = 0
        engine_dirs = [
            _BSD_CORE_PATH,
            os.path.join(_BSD_ENGINE_PATH, 'theories'),
            os.path.join(_BSD_ENGINE_PATH, 'axioms'),
            os.path.join(_BSD_ENGINE_PATH, 'equations'),
            os.path.join(_BSD_ENGINE_PATH, 'validators'),
        ]
        
        for eng_path in engine_dirs:
            if not os.path.isdir(eng_path):
                continue
            for fname in os.listdir(eng_path):
                if fname.endswith('.py') and not fname.startswith('__'):
                    fpath = os.path.join(eng_path, fname)
                    info = self._extract_engine_info(fpath)
                    if info:
                        self.engines[info['name']] = info
                        scanned += 1
        
        print(f"  扫描引擎: {scanned} 个")
        return {'scanned': scanned, 'engines': list(self.engines.keys())}
    
    def _extract_engine_info(self, fpath: str) -> Optional[Dict[str, Any]]:
        """提取引擎信息"""
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # 提取类
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            
            # 计算代码行数
            code_lines = len(content.split('\n'))
            
            # 检测六系
            six_sys = self._detect_six_system(content)
            
            # 检测理论关联
            theory_refs = self._detect_theory_references(content)
            
            # 检测测试文件
            eng_name = os.path.basename(fpath).replace('.py', '')
            has_tests = self._check_test_exists(eng_name)
            
            # 检测文档
            has_doc = self._check_doc_exists(eng_name)
            
            return {
                'name': eng_name,
                'path': fpath,
                'classes': classes,
                'code_lines': code_lines,
                'six_system': six_sys,
                'theory_refs': theory_refs,
                'has_tests': has_tests,
                'has_doc': has_doc,
            }
        except Exception:
            return None
    
    def _detect_six_system(self, content: str) -> str:
        """检测六系归属"""
        sys_patterns = {
            '强化系🔵': ['强化系', 'reinforcement', 'connection'],
            '自然系🟠': ['自然系', 'nature', 'activation'],
            '具现系🔴': ['具现系', 'embodiment', 'fusion'],
            '变身系⚫': ['变身系', 'transformation', 'elevation'],
            '社会系🟢': ['社会系', 'social', 'equilibrium'],
            '天道系🟣': ['天道系', 'tiandao', 'metamorphosis'],
        }
        for sys_name, patterns in sys_patterns.items():
            for pat in patterns:
                if pat.lower() in content.lower():
                    return sys_name
        return '未分类'
    
    def _detect_theory_references(self, content: str) -> List[str]:
        """检测理论引用"""
        refs = set()
        theory_keywords = [
            '公理', '定理', 'theory', 'axiom', 'theorem',
            '六系', '本源', '本体论', '大一统',
        ]
        for kw in theory_keywords:
            if kw.lower() in content.lower():
                refs.add(kw)
        return list(refs)
    
    def _check_test_exists(self, engine_name: str) -> bool:
        """检查是否有测试文件"""
        search_paths = [
            os.path.join(_BSD_ENGINE_PATH, '..', 'tests'),
            _BSD_CORE_PATH,
        ]
        for sp in search_paths:
            if os.path.isdir(sp):
                for fname in os.listdir(sp):
                    if engine_name in fname.lower() and 'test' in fname.lower():
                        return True
        return False
    
    def _check_doc_exists(self, engine_name: str) -> bool:
        """检查是否有文档"""
        doc_paths = [
            os.path.join(os.path.dirname(_BSD_OAPS_PATH), 'docs'),
            _BSD_OAPS_PATH,
        ]
        for dp in doc_paths:
            if os.path.isdir(dp):
                for fname in os.listdir(dp):
                    if engine_name.replace('_', ' ') in fname.lower().replace('_', ' '):
                        return True
        return False
    
    # ----------------------------------------------------------
    # 4.2 理论欠债审计
    # ----------------------------------------------------------
    
    def audit_theory_debts(self) -> List[TheoryDebtItem]:
        """审计理论欠债——找出哪些公理没有对应的引擎实现"""
        print("\n" + "=" * 60)
        print("【引擎审计】理论欠债审计...")
        print("=" * 60)
        
        self.theory_debts = []
        
        for axiom in CORE_AXIOM_LIST:
            missing = []
            existing = []
            
            for expected_eng in axiom['expected_engines']:
                if expected_eng in self.engines:
                    existing.append(expected_eng)
                else:
                    missing.append(expected_eng)
            
            completion_rate = len(existing) / max(len(axiom['expected_engines']), 1)
            
            # 判定欠债等级
            if completion_rate == 0:
                debt_level = DebtLevel.CRITICAL
            elif completion_rate < 0.3:
                debt_level = DebtLevel.HIGH
            elif completion_rate < 0.6:
                debt_level = DebtLevel.MEDIUM
            elif completion_rate < 1.0:
                debt_level = DebtLevel.LOW
            else:
                debt_level = DebtLevel.NONE
            
            # 生成纯系开发计划
            pure_dev_plan = self._generate_pure_dev_plan(axiom, missing)
            
            item = TheoryDebtItem(
                axiom_id=axiom['axiom_id'],
                axiom_name=axiom['name'],
                six_system=axiom['six_system'],
                theory_layer=axiom['theory_layer'],
                debt_level=debt_level,
                missing_engines=missing,
                existing_engines=existing,
                completion_rate=completion_rate,
                pure_dev_plan=pure_dev_plan,
            )
            self.theory_debts.append(item)
        
        # 打印统计
        for level in DebtLevel:
            count = sum(1 for d in self.theory_debts if d.debt_level == level)
            if count > 0:
                print(f"  {level.value}: {count} 条公理")
        
        for item in self.theory_debts:
            if item.debt_level in [DebtLevel.CRITICAL, DebtLevel.HIGH]:
                print(f"\n  ⚠️ {item.axiom_name} ({item.debt_level.value})")
                print(f"    完成度: {item.completion_rate:.0%}")
                if item.missing_engines:
                    print(f"    缺失引擎: {', '.join(item.missing_engines[:3])}")
        
        return self.theory_debts
    
    def _generate_pure_dev_plan(self, 
                                 axiom: Dict[str, Any], 
                                 missing_engines: List[str]) -> List[str]:
        """为欠债公理生成纯系开发计划"""
        plan = []
        
        if not missing_engines:
            return plan
        
        plan.append(f"【{axiom['name']}】纯系开发计划：")
        plan.append(f"  1. 理论溯源：从 {axiom['theory_layer']} 提取核心内容")
        plan.append(f"     核心: {axiom['core_content'][:50]}")
        
        for i, eng_name in enumerate(missing_engines, 1):
            plan.append(f"  {i+1}. 开发引擎: {eng_name}")
            plan.append(f"     - 确定引擎类型（part/component/system）")
            plan.append(f"     - 设计六阶结构")
            plan.append(f"     - 实现核心方法")
            plan.append(f"     - 注册到引擎注册表")
        
        plan.append(f"  {len(missing_engines)+1}. 验证：通过六阶闭环验证")
        plan.append(f"  {len(missing_engines)+2}. 文档：生成引擎文档与测试")
        
        return plan
    
    # ----------------------------------------------------------
    # 4.3 引擎完备性评估
    # ----------------------------------------------------------
    
    def assess_engine_completeness(self) -> List[EngineCompletenessItem]:
        """评估每个引擎的完备性"""
        print("\n" + "=" * 60)
        print("【引擎审计】引擎完备性评估...")
        print("=" * 60)
        
        self.completeness_items = []
        
        for eng_name, eng_info in self.engines.items():
            # 查找引擎实现的公理
            implemented_axioms = []
            missing_axioms = []
            
            for axiom in CORE_AXIOM_LIST:
                if eng_name in axiom['expected_engines']:
                    implemented_axioms.append(axiom['axiom_id'])
                elif axiom['six_system'] == eng_info['six_system']:
                    # 同六系但未在预期列表中→可能需要扩展
                    if len(implemented_axioms) < 2:
                        missing_axioms.append(axiom['axiom_id'])
            
            # 判定完备性
            total_expected = len([a for a in CORE_AXIOM_LIST 
                                  if eng_name in a['expected_engines']])
            if total_expected == 0:
                level = EngineLevel.MINIMAL
            elif len(implemented_axioms) >= total_expected:
                level = EngineLevel.COMPLETE
            elif len(implemented_axioms) >= total_expected * 0.7:
                level = EngineLevel.MOSTLY_COMPLETE
            elif len(implemented_axioms) >= total_expected * 0.3:
                level = EngineLevel.PARTIAL
            else:
                level = EngineLevel.MINIMAL
            
            item = EngineCompletenessItem(
                engine_name=eng_name,
                engine_path=eng_info['path'],
                six_system=eng_info['six_system'],
                implemented_axioms=implemented_axioms,
                missing_axioms=missing_axioms,
                completeness_level=level,
                code_lines=eng_info['code_lines'],
                has_tests=eng_info['has_tests'],
                has_doc=eng_info['has_doc'],
            )
            self.completeness_items.append(item)
        
        # 统计
        for level in EngineLevel:
            count = sum(1 for c in self.completeness_items if c.completeness_level == level)
            if count > 0:
                print(f"  {level.value}: {count} 个引擎")
        
        # 高亮不完备的引擎
        incomplete = [c for c in self.completeness_items 
                     if c.completeness_level in [EngineLevel.MINIMAL, EngineLevel.PARTIAL]]
        if incomplete:
            print(f"\n  ⚠️ 不完备引擎 ({len(incomplete)} 个):")
            for item in incomplete[:10]:
                print(f"    - {item.engine_name} [{item.completeness_level.value}] ({item.code_lines}行)")
        
        return self.completeness_items
    
    # ----------------------------------------------------------
    # 4.4 复合机会识别
    # ----------------------------------------------------------
    
    def identify_composition_opportunities(self) -> List[CompositionOpportunity]:
        """识别引擎复合机会"""
        print("\n" + "=" * 60)
        print("【引擎审计】复合机会识别...")
        print("=" * 60)
        
        self.composition_opportunities = []
        opp_id = 0
        
        # 策略1：同六系引擎可复合
        systems = {}
        for eng_name, eng_info in self.engines.items():
            ss = eng_info['six_system']
            if ss not in systems:
                systems[ss] = []
            systems[ss].append(eng_name)
        
        for ss, engs in systems.items():
            if len(engs) >= 3:
                opp_id += 1
                opp = CompositionOpportunity(
                    composition_id=f"comp_{opp_id:03d}",
                    engines_to_compose=engs[:5],
                    composite_goal=f"{ss}引擎复合系统",
                    shared_theory=self._get_shared_theory(ss),
                    composition_difficulty="medium",
                    expected_benefit=f"将{len(engs)}个{ss}引擎复合为完整子系统",
                )
                self.composition_opportunities.append(opp)
        
        # 策略2：跨六系互补引擎
        cross_system_pairs = [
            ('强化系🔵', '自然系🟠', '连接-激活复合引擎'),
            ('具现系🔴', '变身系⚫', '融合-升维复合引擎'),
            ('社会系🟢', '天道系🟣', '等算-计变复合引擎'),
            ('强化系🔵', '天道系🟣', '本源-极限复合引擎'),
        ]
        
        for sys1, sys2, goal in cross_system_pairs:
            engs1 = [name for name, info in self.engines.items() if info['six_system'] == sys1]
            engs2 = [name for name, info in self.engines.items() if info['six_system'] == sys2]
            
            if engs1 and engs2:
                opp_id += 1
                opp = CompositionOpportunity(
                    composition_id=f"comp_{opp_id:03d}",
                    engines_to_compose=engs1[:2] + engs2[:2],
                    composite_goal=goal,
                    shared_theory=[sys1, sys2],
                    composition_difficulty="high",
                    expected_benefit=f"跨越{sys1}与{sys2}的六阶闭环系统",
                )
                self.composition_opportunities.append(opp)
        
        print(f"  识别复合机会: {len(self.composition_opportunities)} 项")
        for opp in self.composition_opportunities[:5]:
            print(f"    [{opp.composition_id}] {opp.composite_goal}")
            print(f"      引擎: {', '.join(opp.engines_to_compose[:4])}")
            print(f"      难度: {opp.composition_difficulty}")
        
        return self.composition_opportunities
    
    def _get_shared_theory(self, six_system: str) -> List[str]:
        """获取六系共享理论"""
        shared = []
        for axiom in CORE_AXIOM_LIST:
            if axiom['six_system'] == six_system or axiom['six_system'] == '全局':
                shared.append(axiom['axiom_id'])
        return shared
    
    # ----------------------------------------------------------
    # 4.5 生成完整报告
    # ----------------------------------------------------------
    
    def generate_report(self) -> AuditReport:
        """生成完整审计报告"""
        # 汇总
        total_axioms = len(CORE_AXIOM_LIST)
        critical_debts = sum(1 for d in self.theory_debts if d.debt_level == DebtLevel.CRITICAL)
        high_debts = sum(1 for d in self.theory_debts if d.debt_level == DebtLevel.HIGH)
        
        complete_engines = sum(1 for c in self.completeness_items 
                              if c.completeness_level == EngineLevel.COMPLETE)
        total_engines = len(self.completeness_items)
        
        avg_completion = 0.0
        if self.theory_debts:
            avg_completion = sum(d.completion_rate for d in self.theory_debts) / len(self.theory_debts)
        
        summary = {
            'total_axioms': total_axioms,
            'critical_debts': critical_debts,
            'high_debts': high_debts,
            'total_engines': total_engines,
            'complete_engines': complete_engines,
            'avg_theory_completion': avg_completion,
            'composition_opportunities': len(self.composition_opportunities),
            'audit_timestamp': datetime.now().isoformat(),
        }
        
        report = AuditReport(
            report_id=f"audit_{abs(hash(datetime.now().isoformat())) % 100000:05d}",
            generated_at=datetime.now().isoformat(),
            theory_debts=self.theory_debts,
            engine_completeness=self.completeness_items,
            composition_opportunities=self.composition_opportunities,
            summary=summary,
        )
        
        # 打印汇总
        print("\n" + "=" * 60)
        print("【引擎完备性审计报告】")
        print("=" * 60)
        print(f"  审计公理: {total_axioms} 条")
        print(f"  严重欠债: {critical_debts} 条")
        print(f"  高优先欠债: {high_debts} 条")
        print(f"  审计引擎: {total_engines} 个")
        print(f"  完备引擎: {complete_engines} 个")
        print(f"  理论平均完成度: {avg_completion:.0%}")
        print(f"  复合机会: {len(self.composition_opportunities)} 项")
        
        return report


# ============================================================
# 5. 便捷函数
# ============================================================

def quick_audit() -> AuditReport:
    """快速执行完整审计"""
    auditor = EngineCompletenessAuditor()
    auditor.scan_engine_library()
    auditor.audit_theory_debts()
    auditor.assess_engine_completeness()
    auditor.identify_composition_opportunities()
    return auditor.generate_report()


if __name__ == '__main__':
    report = quick_audit()
    
    # 保存报告
    report_path = os.path.join(_BSD_OAPS_PATH, 'engine_completeness_audit_report.json')
    
    # 转换为可序列化格式
    report_dict = {
        'report_id': report.report_id,
        'generated_at': report.generated_at,
        'summary': report.summary,
        'theory_debts': [
            {
                'axiom_id': d.axiom_id,
                'axiom_name': d.axiom_name,
                'six_system': d.six_system,
                'debt_level': d.debt_level.value,
                'completion_rate': d.completion_rate,
                'missing_engines': d.missing_engines,
            }
            for d in report.theory_debts
        ],
        'composition_opportunities': [
            {
                'id': c.composition_id,
                'goal': c.composite_goal,
                'engines': c.engines_to_compose,
                'difficulty': c.composition_difficulty,
            }
            for c in report.composition_opportunities
        ],
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)
    
    print(f"\n  报告已保存: {report_path}")