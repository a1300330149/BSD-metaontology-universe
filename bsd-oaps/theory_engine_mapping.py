#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
理论-引擎对接系统 (Theory-Engine Mapping System)
================================================

核心使命：
    将 theory_base（六系立系论）与 bsd_engine（六系立系引擎论）完成深度对接，
    构建「理论即引擎，引擎即理论」的双向映射闭环。

设计原则：
    1. 理论→引擎：每条理论公理对应可执行的引擎方法
    2. 引擎→理论：每个引擎组件回溯其理论出处
    3. 双向验证：理论的正确性由引擎验证，引擎的合理性由理论支撑
    4. 六系同构：引擎的六阶结构与理论的六系结构完全映射

映射架构：
    theory_base/L0_总本源层 ──→ bsd_engine/axioms/ (公理层)
    theory_base/L1_不动母科层 ──→ bsd_engine/theories/ (理论模块层)
    六系核心公理 ──→ bsd_engine/core/ (引擎核心层)
    六系立系论 ──→ 引擎六阶闭环 (连接→激活→融合→升维→等算→计变)

六系立系论 ↔ 六系立系引擎论 完整映射：
    ┌──────────┬──────────────┬──────────────────────┬──────────────┐
    │ 六系立系论 │ 引擎六阶       │ 核心引擎能力           │ 对应公理      │
    ├──────────┼──────────────┼──────────────────────┼──────────────┤
    │ 强化系    │ 第一阶·连接    │ 引擎连接与注册         │ 公理0·元道存在 │
    │ 自然系    │ 第二阶·激活    │ 引擎激活与检测         │ 公理1·物质存在 │
    │ 具现系    │ 第三阶·融合    │ 引擎融合与互补         │ 公理2·生命涌现 │
    │ 变身系    │ 第四阶·升维    │ 引擎升维与进化         │ 公理3·意识存在 │
    │ 社会系    │ 第五阶·等算    │ 引擎协同与引力         │ 公理4·社会存在 │
    │ 天道系    │ 第六阶·计变    │ 引擎永动与计算极限      │ 公理5·天道存在 │
    └──────────┴──────────────┴──────────────────────┴──────────────┘
"""

import os
import sys
import re
import json
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
_BSD_AXIOMS_PATH = os.path.join(_BSD_ENGINE_PATH, 'axioms')
_BSD_THEORIES_PATH = os.path.join(_BSD_ENGINE_PATH, 'theories')


# ============================================================
# 1. 六系-六阶映射表（核心对接数据结构）
# ============================================================

class SixSystem(Enum):
    """六系立系论的六系"""
    REINFORCEMENT = "强化系🔵"    # 连接
    NATURE = "自然系🟠"           # 激活
    EMBODIMENT = "具现系🔴"       # 融合
    TRANSFORMATION = "变身系⚫"   # 升维
    SOCIAL = "社会系🟢"           # 等算
    TIANDAO = "天道系🟣"         # 计变


class SixStage(Enum):
    """引擎六阶闭环"""
    CONNECTION = "连接"
    ACTIVATION = "激活"
    FUSION = "融合"
    ELEVATION = "升维"
    EQUILIBRIUM = "等算"
    METAMORPHOSIS = "计变"


class TheoryLayer(Enum):
    """理论层级"""
    L0_ORIGIN = "L0_总本源层"
    L1_MOTHER = "L1_不动母科层"
    L2_INFINITE = "L2_无限展开层"


class EngineLayer(Enum):
    """引擎层级"""
    AXIOMS = "axioms"         # 公理层
    THEORIES = "theories"     # 理论模块层
    CORE = "core"             # 引擎核心层
    EQUATIONS = "equations"   # 方程层
    VALIDATORS = "validators" # 验证层


# 六系→六阶映射
SIX_SYSTEM_STAGE_MAP: Dict[SixSystem, SixStage] = {
    SixSystem.REINFORCEMENT: SixStage.CONNECTION,
    SixSystem.NATURE: SixStage.ACTIVATION,
    SixSystem.EMBODIMENT: SixStage.FUSION,
    SixSystem.TRANSFORMATION: SixStage.ELEVATION,
    SixSystem.SOCIAL: SixStage.EQUILIBRIUM,
    SixSystem.TIANDAO: SixStage.METAMORPHOSIS,
}

# 六系→引擎层映射
SIX_SYSTEM_ENGINE_LAYER: Dict[SixSystem, List[EngineLayer]] = {
    SixSystem.REINFORCEMENT: [EngineLayer.AXIOMS, EngineLayer.CORE],
    SixSystem.NATURE: [EngineLayer.THEORIES, EngineLayer.CORE],
    SixSystem.EMBODIMENT: [EngineLayer.CORE, EngineLayer.EQUATIONS],
    SixSystem.TRANSFORMATION: [EngineLayer.CORE, EngineLayer.VALIDATORS],
    SixSystem.SOCIAL: [EngineLayer.EQUATIONS, EngineLayer.VALIDATORS],
    SixSystem.TIANDAO: [EngineLayer.AXIOMS, EngineLayer.EQUATIONS],
}

# 六系→理论层级映射
SIX_SYSTEM_THEORY_LAYER: Dict[SixSystem, TheoryLayer] = {
    SixSystem.REINFORCEMENT: TheoryLayer.L0_ORIGIN,
    SixSystem.NATURE: TheoryLayer.L1_MOTHER,
    SixSystem.EMBODIMENT: TheoryLayer.L1_MOTHER,
    SixSystem.TRANSFORMATION: TheoryLayer.L2_INFINITE,
    SixSystem.SOCIAL: TheoryLayer.L2_INFINITE,
    SixSystem.TIANDAO: TheoryLayer.L0_ORIGIN,
}

# 公理映射表：每条公理→对应的引擎模块
AXIOM_ENGINE_MAP: Dict[str, Dict[str, Any]] = {
    "公理0·元道存在": {
        "six_system": SixSystem.REINFORCEMENT,
        "axiom_files": ["seven_origin_axioms.py"],
        "engine_files": ["theory_hub.py", "six_system_bootstrap_engine.py"],
        "core_ability": "引擎连接与注册",
        "theory_source": "L0_总本源层/0元本体论大一统",
    },
    "公理1·物质存在": {
        "six_system": SixSystem.NATURE,
        "axiom_files": ["eight_unification_axioms.py"],
        "engine_files": ["theory_driven_engine.py", "six_system_project_mapper.py"],
        "core_ability": "引擎激活与检测",
        "theory_source": "L0_总本源层/15元法则",
    },
    "公理2·生命涌现": {
        "six_system": SixSystem.EMBODIMENT,
        "axiom_files": ["three_meaning_axioms.py"],
        "engine_files": ["life_emergence_engine.py", "cross_origin_weight_mapper.py"],
        "core_ability": "引擎融合与互补",
        "theory_source": "L0_总本源层/全域秩序建筑论",
    },
    "公理3·意识存在": {
        "six_system": SixSystem.TRANSFORMATION,
        "axiom_files": ["reverse_operation_theorem.py"],
        "engine_files": ["dual_polarity_spawner.py", "theory_deep_reader.py"],
        "core_ability": "引擎升维与进化",
        "theory_source": "L0_总本源层/六系自组织",
    },
    "公理4·社会存在": {
        "six_system": SixSystem.SOCIAL,
        "axiom_files": ["nine_special_axioms.py"],
        "engine_files": ["institutional_economics.py", "social_engine.py"],
        "core_ability": "引擎协同与引力",
        "theory_source": "L1_不动母科层/06_全域结构学科",
    },
    "公理5·天道存在": {
        "six_system": SixSystem.TIANDAO,
        "axiom_files": ["twelve_bsd_axioms.py"],
        "engine_files": ["cosmological_constant.py", "standing_wave.py"],
        "core_ability": "引擎永动与计算极限",
        "theory_source": "L0_总本源层/0元本体论大一统",
    },
}


# ============================================================
# 2. 理论-引擎映射数据模型
# ============================================================

@dataclass
class TheoryNode:
    """理论节点——theory_base中的理论条目"""
    node_id: str
    content: str
    theory_layer: TheoryLayer
    six_system: Optional[SixSystem]
    source_file: str
    keywords: List[str] = field(default_factory=list)
    mapped_axiom: Optional[str] = None


@dataclass
class EngineNode:
    """引擎节点——bsd_engine中的引擎组件"""
    node_id: str
    name: str
    engine_layer: EngineLayer
    six_system: Optional[SixSystem]
    source_file: str
    engine_type: str = "part"  # part/component/system/framework
    keywords: List[str] = field(default_factory=list)
    mapped_theory: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class TheoryEngineBridge:
    """理论-引擎桥接关系"""
    bridge_id: str
    theory_node_id: str
    engine_node_id: str
    six_system: SixSystem
    mapping_type: str = "direct"  # direct/inverse/emergent
    confidence: float = 1.0
    verified: bool = False
    verification_result: Optional[str] = None
    created_at: str = ""


# ============================================================
# 3. 理论-引擎对接器（核心类）
# ============================================================

class TheoryEngineMapper:
    """
    理论-引擎双向映射器
    
    功能：
    1. 扫描theory_base中的理论条目
    2. 扫描bsd_engine中的引擎组件
    3. 建立理论节点与引擎节点的双向映射
    4. 验证映射的正确性与完备性
    5. 生成映射报告
    """
    
    def __init__(self):
        self.theory_nodes: Dict[str, TheoryNode] = {}
        self.engine_nodes: Dict[str, EngineNode] = {}
        self.bridges: Dict[str, TheoryEngineBridge] = {}
        self._scan_results: Dict[str, Any] = {}
        self._mapping_report: Dict[str, Any] = {}
    
    # ----------------------------------------------------------
    # 3.1 扫描理论节点
    # ----------------------------------------------------------
    
    def scan_theory_base(self) -> Dict[str, Any]:
        """扫描theory_base目录，提取理论节点"""
        print("\n" + "=" * 60)
        print("【理论-引擎对接】扫描theory_base...")
        print("=" * 60)
        
        scanned = 0
        for root, dirs, files in os.walk(_THEORY_BASE_PATH):
            for fname in files:
                if fname.endswith('.md') or fname.endswith('.docx'):
                    fpath = os.path.join(root, fname)
                    rel_path = os.path.relpath(fpath, _THEORY_BASE_PATH)
                    
                    # 确定理论层级
                    layer = self._detect_theory_layer(rel_path)
                    
                    # 确定六系归属
                    six_sys = self._detect_six_system_from_path(rel_path)
                    
                    # 生成理论节点ID
                    node_id = f"theory_{abs(hash(rel_path)) % 100000:05d}"
                    
                    node = TheoryNode(
                        node_id=node_id,
                        content=fname,
                        theory_layer=layer,
                        six_system=six_sys,
                        source_file=fpath,
                        keywords=self._extract_theory_keywords(fname),
                    )
                    self.theory_nodes[node_id] = node
                    scanned += 1
        
        print(f"  扫描理论文件: {scanned} 个")
        print(f"  识别理论节点: {len(self.theory_nodes)} 个")
        
        # 按层级统计
        layer_stats: Dict[str, int] = {}
        for node in self.theory_nodes.values():
            key = node.theory_layer.value
            layer_stats[key] = layer_stats.get(key, 0) + 1
        
        for layer, count in sorted(layer_stats.items()):
            print(f"    {layer}: {count} 个")
        
        self._scan_results['theory'] = {
            'total': len(self.theory_nodes),
            'by_layer': layer_stats,
        }
        return self._scan_results['theory']
    
    # ----------------------------------------------------------
    # 3.2 扫描引擎节点
    # ----------------------------------------------------------
    
    def scan_engines(self) -> Dict[str, Any]:
        """扫描bsd_engine目录，提取引擎节点"""
        print("\n" + "=" * 60)
        print("【理论-引擎对接】扫描bsd_engine...")
        print("=" * 60)
        
        scanned = 0
        engine_dirs = [
            (_BSD_AXIOMS_PATH, EngineLayer.AXIOMS),
            (_BSD_THEORIES_PATH, EngineLayer.THEORIES),
            (_BSD_CORE_PATH, EngineLayer.CORE),
            (os.path.join(_BSD_ENGINE_PATH, 'equations'), EngineLayer.EQUATIONS),
            (os.path.join(_BSD_ENGINE_PATH, 'validators'), EngineLayer.VALIDATORS),
        ]
        
        for eng_path, eng_layer in engine_dirs:
            if not os.path.isdir(eng_path):
                continue
            
            for fname in os.listdir(eng_path):
                if fname.endswith('.py') and not fname.startswith('__'):
                    fpath = os.path.join(eng_path, fname)
                    
                    # 检测引擎类型和六系归属
                    eng_type = self._detect_engine_type(fpath)
                    six_sys = self._detect_six_system_from_file(fpath)
                    
                    node_id = f"engine_{abs(hash(os.path.basename(fpath))) % 100000:05d}"
                    
                    node = EngineNode(
                        node_id=node_id,
                        name=fname.replace('.py', ''),
                        engine_layer=eng_layer,
                        six_system=six_sys,
                        source_file=fpath,
                        engine_type=eng_type,
                        keywords=self._extract_engine_keywords(fpath),
                    )
                    self.engine_nodes[node_id] = node
                    scanned += 1
        
        print(f"  扫描引擎文件: {scanned} 个")
        print(f"  识别引擎节点: {len(self.engine_nodes)} 个")
        
        # 按引擎层统计
        layer_stats: Dict[str, int] = {}
        for node in self.engine_nodes.values():
            key = node.engine_layer.value
            layer_stats[key] = layer_stats.get(key, 0) + 1
        
        for layer, count in sorted(layer_stats.items()):
            print(f"    {layer}: {count} 个")
        
        self._scan_results['engine'] = {
            'total': len(self.engine_nodes),
            'by_layer': layer_stats,
        }
        return self._scan_results['engine']
    
    # ----------------------------------------------------------
    # 3.3 建立理论-引擎桥接
    # ----------------------------------------------------------
    
    def build_bridges(self) -> Dict[str, Any]:
        """建立理论节点与引擎节点的双向桥接"""
        print("\n" + "=" * 60)
        print("【理论-引擎对接】构建桥接映射...")
        print("=" * 60)
        
        bridges_created = 0
        
        for node_id, theory_node in self.theory_nodes.items():
            # 按六系匹配引擎节点
            if theory_node.six_system:
                matching_engines = self._find_engines_by_six_system(theory_node.six_system)
                for eng_node in matching_engines:
                    bridge_id = f"bridge_{abs(hash(theory_node.node_id + eng_node.node_id)) % 100000:05d}"
                    
                    bridge = TheoryEngineBridge(
                        bridge_id=bridge_id,
                        theory_node_id=theory_node.node_id,
                        engine_node_id=eng_node.node_id,
                        six_system=theory_node.six_system,
                        mapping_type="direct",
                        confidence=0.8,
                        created_at=datetime.now().isoformat(),
                    )
                    self.bridges[bridge_id] = bridge
                    eng_node.mapped_theory = theory_node.node_id
                    theory_node.mapped_axiom = eng_node.node_id
                    bridges_created += 1
        
        # 公理级精确桥接
        for axiom_name, axiom_info in AXIOM_ENGINE_MAP.items():
            six_sys = axiom_info['six_system']
            for eng_file in axiom_info['engine_files']:
                matching_engs = [
                    n for n in self.engine_nodes.values()
                    if eng_file.replace('.py', '') in n.name
                ]
                for eng_node in matching_engs:
                    # 为引擎节点标记公理映射
                    eng_node.mapped_theory = axiom_name
        
        print(f"  创建桥接: {bridges_created} 条")
        print(f"  理论节点已映射: {sum(1 for n in self.theory_nodes.values() if n.mapped_axiom)}")
        print(f"  引擎节点已映射: {sum(1 for n in self.engine_nodes.values() if n.mapped_theory)}")
        
        # 统计各系映射覆盖率
        coverage = {}
        for ss in SixSystem:
            theory_count = sum(1 for n in self.theory_nodes.values() if n.six_system == ss)
            engine_count = sum(1 for n in self.engine_nodes.values() if n.six_system == ss)
            mapped = sum(
                1 for b in self.bridges.values()
                if b.six_system == ss
            )
            coverage[ss.value] = {
                'theory': theory_count,
                'engine': engine_count,
                'bridges': mapped,
                'coverage': mapped / max(theory_count + engine_count, 1),
            }
        
        print("\n  六系映射覆盖率:")
        for sys_name, cov in coverage.items():
            pct = cov['coverage'] * 100
            print(f"    {sys_name}: 理论{cov['theory']} + 引擎{cov['engine']} → 桥接{cov['bridges']} ({pct:.0f}%)")
        
        self._mapping_report = {
            'total_bridges': len(self.bridges),
            'theory_mapped': sum(1 for n in self.theory_nodes.values() if n.mapped_axiom),
            'engine_mapped': sum(1 for n in self.engine_nodes.values() if n.mapped_theory),
            'coverage': coverage,
        }
        return self._mapping_report
    
    # ----------------------------------------------------------
    # 3.4 查询接口
    # ----------------------------------------------------------
    
    def find_engines_for_theory(self, theory_keyword: str) -> List[EngineNode]:
        """根据理论关键词查找对应的引擎"""
        results = []
        for node in self.engine_nodes.values():
            if theory_keyword.lower() in node.name.lower():
                results.append(node)
            elif any(theory_keyword.lower() in kw.lower() for kw in node.keywords):
                results.append(node)
        return results
    
    def find_theory_for_engine(self, engine_name: str) -> List[TheoryNode]:
        """根据引擎名称查找对应的理论"""
        results = []
        for node in self.theory_nodes.values():
            if engine_name.lower() in node.content.lower():
                results.append(node)
            elif any(engine_name.lower() in kw.lower() for kw in node.keywords):
                results.append(node)
        return results
    
    def get_axiom_engine_mapping(self, axiom_name: str) -> Optional[Dict[str, Any]]:
        """获取指定公理的引擎映射"""
        return AXIOM_ENGINE_MAP.get(axiom_name)
    
    def get_six_system_engines(self, six_system: SixSystem) -> List[EngineNode]:
        """获取指定六系的所有引擎"""
        return [n for n in self.engine_nodes.values() if n.six_system == six_system]
    
    # ----------------------------------------------------------
    # 3.5 辅助方法
    # ----------------------------------------------------------
    
    def _detect_theory_layer(self, rel_path: str) -> TheoryLayer:
        """从路径检测理论层级"""
        if 'L0_总本源层' in rel_path:
            return TheoryLayer.L0_ORIGIN
        elif 'L1_不动母科层' in rel_path:
            return TheoryLayer.L1_MOTHER
        else:
            return TheoryLayer.L2_INFINITE
    
    def _detect_six_system_from_path(self, rel_path: str) -> Optional[SixSystem]:
        """从路径/内容检测六系归属"""
        system_keywords = {
            SixSystem.REINFORCEMENT: ['强化', '元道', '本源', '存在'],
            SixSystem.NATURE: ['自然', '物理', '物质', '法则'],
            SixSystem.EMBODIMENT: ['具现', '生命', '涌现', '结构'],
            SixSystem.TRANSFORMATION: ['变身', '意识', '进化', '升维'],
            SixSystem.SOCIAL: ['社会', '经济', '秩序', '计算'],
            SixSystem.TIANDAO: ['天道', '宇宙', '常数', '极限'],
        }
        for sys, keywords in system_keywords.items():
            for kw in keywords:
                if kw in rel_path:
                    return sys
        return None
    
    def _detect_six_system_from_file(self, fpath: str) -> Optional[SixSystem]:
        """从引擎文件内容检测六系归属"""
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(3000)
        except Exception:
            return None
        
        system_patterns = {
            SixSystem.REINFORCEMENT: ['强化系', '连接', '注册', 'register'],
            SixSystem.NATURE: ['自然系', '激活', '检测', 'activate'],
            SixSystem.EMBODIMENT: ['具现系', '融合', '涌现', 'fusion'],
            SixSystem.TRANSFORMATION: ['变身系', '升维', '进化', 'elevat'],
            SixSystem.SOCIAL: ['社会系', '等算', '协同', 'equilibrium'],
            SixSystem.TIANDAO: ['天道系', '计变', '永动', 'cosmolog'],
        }
        for sys, patterns in system_patterns.items():
            for pat in patterns:
                if pat.lower() in content.lower():
                    return sys
        return None
    
    def _detect_engine_type(self, fpath: str) -> str:
        """检测引擎类型（part/component/system）"""
        name = os.path.basename(fpath).lower()
        if 'part' in name or 'public' in name or 'common' in name:
            return 'part'
        elif 'system' in name or 'engine' in name:
            return 'system'
        elif 'match' in name or 'game' in name or 'manager' in name:
            return 'component'
        return 'part'
    
    def _extract_theory_keywords(self, filename: str) -> List[str]:
        """从理论文件名提取关键词"""
        keywords = []
        # 中文关键词
        chinese_chars = re.findall(r'[\u4e00-\u9fff]{2,4}', filename)
        keywords.extend(chinese_chars)
        # 英文关键词
        english_words = re.findall(r'[a-zA-Z]{3,}', filename.lower())
        keywords.extend(english_words)
        return keywords
    
    def _extract_engine_keywords(self, fpath: str) -> List[str]:
        """从引擎文件提取关键词"""
        keywords = []
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
            
            # 提取类名
            classes = re.findall(r'class\s+(\w+)', content)
            keywords.extend([c.lower() for c in classes])
            
            # 提取六系关键词
            sys_words = ['强化', '自然', '具现', '变身', '社会', '天道',
                        'connection', 'activation', 'fusion', 'elevation', 'equilibrium', 'metamorphosis']
            for w in sys_words:
                if w.lower() in content.lower():
                    keywords.append(w)
        except Exception:
            pass
        return list(set(keywords))
    
    def _find_engines_by_six_system(self, six_system: SixSystem) -> List[EngineNode]:
        """按六系查找引擎"""
        return [n for n in self.engine_nodes.values() if n.six_system == six_system]
    
    # ----------------------------------------------------------
    # 3.6 生成报告
    # ----------------------------------------------------------
    
    def generate_report(self) -> Dict[str, Any]:
        """生成完整的理论-引擎对接报告"""
        report = {
            'title': '理论-引擎对接报告',
            'generated_at': datetime.now().isoformat(),
            'theory_nodes': len(self.theory_nodes),
            'engine_nodes': len(self.engine_nodes),
            'bridges': len(self.bridges),
            'mapping_report': self._mapping_report,
            'axiom_engine_map': AXIOM_ENGINE_MAP,
            'six_system_stage_map': {
                ss.value: stage.value for ss, stage in SIX_SYSTEM_STAGE_MAP.items()
            },
        }
        
        # 各公理的引擎状态
        axiom_status = {}
        for axiom_name, axiom_info in AXIOM_ENGINE_MAP.items():
            mapped_engs = [
                eid for b in self.bridges.values()
                for eid in [b.engine_node_id]
                if any(axiom_info['engine_files'][0].replace('.py', '') in 
                       self.engine_nodes.get(eid, EngineNode('', '', EngineLayer.CORE, None, '')).name
                       for _ in [1])
            ]
            axiom_status[axiom_name] = {
                'six_system': axiom_info['six_system'].value,
                'engine_files': axiom_info['engine_files'],
                'core_ability': axiom_info['core_ability'],
                'theory_source': axiom_info['theory_source'],
            }
        report['axiom_status'] = axiom_status
        
        return report


# ============================================================
# 4. 便捷函数
# ============================================================

def quick_map() -> TheoryEngineMapper:
    """快速执行完整的理论-引擎对接流程"""
    mapper = TheoryEngineMapper()
    mapper.scan_theory_base()
    mapper.scan_engines()
    mapper.build_bridges()
    return mapper


if __name__ == '__main__':
    mapper = quick_map()
    report = mapper.generate_report()
    print("\n" + "=" * 60)
    print("【理论-引擎对接完成】")
    print("=" * 60)
    print(f"  理论节点: {report['theory_nodes']}")
    print(f"  引擎节点: {report['engine_nodes']}")
    print(f"  桥接映射: {report['bridges']}")
    
    # 保存报告
    report_path = os.path.join(_BSD_OAPS_PATH, 'theory_engine_mapping_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n  报告已保存: {report_path}")