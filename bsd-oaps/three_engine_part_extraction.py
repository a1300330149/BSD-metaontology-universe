#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 三大引擎逆向部件提取系统
==============================

核心目标：
    从黑客引擎、围棋引擎、基因引擎中逆向提取可独立的部件，
    让它们回归公有架构，支持多组件共享。

理论依据：
    - 部件引擎与组件引擎的二分法
    - 虚拟宇宙数字可公有，不需要重复制造
    - 六系立系引擎论作为集成指导
"""

import os
import sys
import re
import ast
import importlib
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ============================================================
# 三大引擎的核心路径
# ============================================================

THREE_ENGINES = {
    'go': {
        'name': '围棋引擎',
        'files': [
            'bsd_engine/core/bsd_go_engine.py',
            'bsd_engine/core/bsd_go_engine_v2.py',
            'bsd_engine/core/bsd_go_engine_v3.py',
            'bsd_engine/core/bsd_go_engine_v4.py',
            'bsd_engine/core/bsd_go_engine_v5.py',
            'bsd_engine/core/bsd_go_match.py',
            'bsd_engine/core/bsd_match_v3.py',
            'bsd_engine/core/bsd_match_v4.py',
            'bsd_engine/core/bsd_match_v5.py',
        ],
        'description': '基于BSD六系立系论的围棋AI引擎',
    },
    'gene': {
        'name': '基因引擎',
        'files': [
            'physical_body/gene_engineering_system.py',
            'physical_body/bsd_evolution_engine.py',
            'physical_body/bsd_consciousness_gene_analyzer.py',
            'bsd_engine/core/evolution_protocol_rules.py',
            'bsd_engine/core/life_emergence_engine.py',
        ],
        'description': '基因工程与进化引擎',
    },
    'hacker': {
        'name': '黑客引擎',
        'files': [
            'physical_body/bsd_hacker_knowledge_emergence.py',
            'physical_body/BSD_ChatBridge.py',
            'physical_body/BSD_DualClock_GeneSystem.py',
            'physical_body/BSD_Federation_Engine.py',
            'physical_body/BSD_Bridge_Lightweight.py',
            'physical_body/BSD_CleanAndInject.py',
        ],
        'description': '黑客知识涌现与桥接引擎',
    }
}


# ============================================================
# 部件类型定义
# ============================================================

class ExtractedPartType(Enum):
    """提取的部件类型"""
    DATA_STRUCTURE = "data_structure"      # 数据结构部件
    ALGORITHM = "algorithm"                # 算法部件
    MANAGER = "manager"                    # 管理器部件
    CALCULATOR = "calculator"              # 计算器部件
    SCANNER = "scanner"                    # 扫描器部件
    INDEXER = "indexer"                    # 索引器部件
    VALIDATOR = "validator"                # 验证器部件
    TRANSFORMER = "transformer"            # 转换器部件


@dataclass
class ExtractedPart:
    """从三大引擎提取的部件"""
    source_engine: str                    # 来源引擎
    source_file: str                       # 来源文件
    part_name: str                         # 部件名称
    part_type: ExtractedPartType           # 部件类型
    code_snippet: str                      # 代码片段
    can_be_public: bool = True             # 是否可公有
    public_value: float = 0.0              # 公有价值（0-1）
    target_components: List[str] = field(default_factory=list)  # 可服务的组件
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source_engine': self.source_engine,
            'source_file': self.source_file,
            'part_name': self.part_name,
            'part_type': self.part_type.value if hasattr(self.part_type, 'value') else str(self.part_type),
            'can_be_public': self.can_be_public,
            'public_value': self.public_value,
            'target_components': self.target_components,
            'code_length': len(self.code_snippet)
        }


# ============================================================
# 部件分析器
# ============================================================

class PartAnalyzer:
    """从源码分析可独立部件"""
    
    # 可独立部件的特征模式
    PART_PATTERNS = {
        'data_structure': [
            r'^class\s+\w+.*:',  # 数据类
            r'^@dataclass',
            r'^class\s+\w+\(.*Enum.*\)',
        ],
        'algorithm': [
            r'def\s+get_score',
            r'def\s+evaluate',
            r'def\s+calculate_',
            r'def\s+compute_',
            r'def\s+estimate',
        ],
        'manager': [
            r'def\s+initialize_',
            r'def\s+register',
            r'def\s+add_',
            r'def\s+remove_',
            r'def\s+update_',
            r'def\s+manage_',
        ],
        'scanner': [
            r'def\s+scan_',
            r'def\s+collect_',
            r'def\s+gather_',
            r'def\s+discover_',
        ],
        'calculator': [
            r'def\s+get_game_phase',
            r'def\s+get_score',
            r'def\s+_calculate',
            r'def\s+compute',
        ],
        'validator': [
            r'def\s+is_valid',
            r'def\s+check_',
            r'def\s+verify_',
            r'def\s+validate',
        ],
        'transformer': [
            r'def\s+to_',
            r'def\s+convert',
            r'def\s+transform',
            r'def\s+map_',
        ],
    }
    
    # 跨引擎可共享的功能关键词
    CROSS_ENGINE_KEYWORDS = {
        'entity', 'factory', 'manager', 'calculator',
        'normalizer', 'converter', 'validator', 'checker',
        'mapper', 'adapter', 'protocol', 'coordinator',
        'verifier', 'detector', 'matrix', 'generator',
        'processor', 'handler', 'searcher', 'reader',
        'analyzer', 'indexer', 'scanner', 'collector'
    }
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.extracted_parts: List[ExtractedPart] = []
        self.analysis_log: List[Dict[str, Any]] = []
    
    def analyze_three_engines(self) -> List[ExtractedPart]:
        """分析三大引擎，提取可独立部件"""
        print("=" * 70)
        print("【BSD 三大引擎逆向部件提取】")
        print("=" * 70)
        
        for engine_key, engine_info in THREE_ENGINES.items():
            engine_name = engine_info['name']
            print(f"\n📜 分析 {engine_name}...")
            print("-" * 50)
            
            for file_path in engine_info['files']:
                full_path = os.path.join(self.base_path, file_path)
                if os.path.exists(full_path):
                    parts = self._analyze_file(
                        full_path, engine_key, engine_name
                    )
                    self.extracted_parts.extend(parts)
                    print(f"  ✓ {os.path.basename(file_path)}: 发现 {len(parts)} 个可独立部件")
                else:
                    print(f"  ✗ {os.path.basename(file_path)}: 文件不存在")
        
        # 评估公有价值
        self._evaluate_public_value()
        
        # 分类汇总
        self._generate_summary()
        
        return self.extracted_parts
    
    def _analyze_file(self, file_path: str, engine_key: str, engine_name: str) -> List[ExtractedPart]:
        """分析单个文件，提取可独立部件"""
        parts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"    ⚠️ 读取文件失败: {e}")
            return parts
        
        # 提取类定义
        class_pattern = r'^class\s+(\w+)(?:\(([^)]*)\))?\s*:'
        class_matches = re.finditer(class_pattern, content, re.MULTILINE)
        
        for match in class_matches:
            class_name = match.group(1)
            class_start = match.start()
            
            # 找到下一个类或文件结尾
            next_class = re.search(
                r'^class\s+\w+', 
                content[class_start + 1:], 
                re.MULTILINE
            )
            if next_class:
                class_end = class_start + 1 + next_class.start()
            else:
                class_end = len(content)
            
            class_code = content[class_start:class_end]
            
            # 判断是否为可独立部件
            part_type = self._classify_part(class_name, class_code)
            if part_type:
                part = ExtractedPart(
                    source_engine=engine_key,
                    source_file=os.path.basename(file_path),
                    part_name=class_name,
                    part_type=part_type,
                    code_snippet=class_code[:500],  # 前500字符作为摘要
                    can_be_public=self._check_public_potential(class_name, class_code)
                )
                parts.append(part)
        
        # 提取独立函数（不属于任何类的）
        func_pattern = r'^def\s+(\w+)\s*\('
        func_matches = re.finditer(func_pattern, content, re.MULTILINE)
        
        for match in func_matches:
            func_name = match.group(1)
            func_start = match.start()
            
            # 检查是否在类内部（通过缩进判断）
            if func_start > 0:
                prev_lines = content[:func_start].split('\n')
                if prev_lines and prev_lines[-1].startswith(' '):
                    continue  # 在类内部，跳过
            
            # 找到函数体
            next_def = re.search(
                r'^(def |class )', 
                content[func_start + 1:], 
                re.MULTILINE
            )
            if next_def:
                func_end = func_start + 1 + next_def.start()
            else:
                func_end = min(func_start + 200, len(content))
            
            func_code = content[func_start:func_end]
            
            # 判断是否为可独立部件
            part_type = self._classify_part(func_name, func_code)
            if part_type:
                part = ExtractedPart(
                    source_engine=engine_key,
                    source_file=os.path.basename(file_path),
                    part_name=func_name,
                    part_type=part_type,
                    code_snippet=func_code[:500],
                    can_be_public=self._check_public_potential(func_name, func_code)
                )
                parts.append(part)
        
        return parts
    
    def _classify_part(self, name: str, code: str) -> Optional[ExtractedPartType]:
        """判断是否为可独立部件"""
        name_lower = name.lower()
        code_lower = code.lower()
        
        # 检查数据结构
        if '@dataclass' in code or 'Enum' in code or 'namedtuple' in code:
            return ExtractedPartType.DATA_STRUCTURE
        
        # 检查函数类型
        for part_type, patterns in self.PART_PATTERNS.items():
            if part_type == 'data_structure':
                continue
            
            for pattern in patterns:
                if re.search(pattern, name_lower) or re.search(pattern, code_lower[:200]):
                    return part_type
        
        # 检查是否包含跨引擎关键词
        for keyword in self.CROSS_ENGINE_KEYWORDS:
            if keyword in name_lower:
                return ExtractedPartType.MANAGER  # 默认为管理器类型
        
        return None
    
    def _check_public_potential(self, name: str, code: str) -> bool:
        """检查是否有公有潜力"""
        name_lower = name.lower()
        
        # 数据结构通常可公有
        if '@dataclass' in code or 'Enum' in code:
            return True
        
        # 工具函数通常可公有
        public_indicators = [
            'calculate', 'compute', 'convert', 'transform',
            'validate', 'verify', 'check', 'is_valid',
            'scan', 'collect', 'search', 'find',
            'normalize', 'map', 'adapt', 'process',
        ]
        
        for indicator in public_indicators:
            if indicator in name_lower:
                return True
        
        return False
    
    def _evaluate_public_value(self):
        """评估公有价值"""
        for part in self.extracted_parts:
            value = 0.0
            
            # 数据结构价值高
            if part.part_type == ExtractedPartType.DATA_STRUCTURE:
                value += 0.9
            
            # 被多个引擎引用价值高
            refs = self._count_cross_references(part)
            value += refs * 0.1
            
            # 工具函数价值中等
            if part.part_type in [ExtractedPartType.ALGORITHM, ExtractedPartType.CALCULATOR]:
                value += 0.5
            
            # 管理器价值中等
            if part.part_type == ExtractedPartType.MANAGER:
                value += 0.6
            
            part.public_value = min(value, 1.0)
            
            # 确定可服务的组件
            part.target_components = self._find_target_components(part)
    
    def _count_cross_references(self, part: ExtractedPart) -> int:
        """计算跨引擎引用次数"""
        count = 0
        name_lower = part.part_name.lower()
        
        for other_part in self.extracted_parts:
            if other_part.source_engine != part.source_engine:
                if name_lower in other_part.code_snippet.lower():
                    count += 1
        
        return count
    
    def _find_target_components(self, part: ExtractedPart) -> List[str]:
        """找到可服务的组件"""
        targets = []
        name_lower = part.part_name.lower()
        
        # 基于部件类型推荐目标
        type_targets = {
            ExtractedPartType.DATA_STRUCTURE: ['go_engine', 'gene_engine', 'hacker_engine'],
            ExtractedPartType.ALGORITHM: ['go_engine'],
            ExtractedPartType.CALCULATOR: ['go_engine', 'gene_engine'],
            ExtractedPartType.MANAGER: ['go_engine', 'gene_engine', 'hacker_engine'],
            ExtractedPartType.SCANNER: ['gene_engine'],
            ExtractedPartType.VALIDATOR: ['go_engine', 'hacker_engine'],
            ExtractedPartType.TRANSFORMER: ['go_engine', 'gene_engine'],
            ExtractedPartType.INDEXER: ['hacker_engine', 'gene_engine'],
        }
        
        # 基于功能关键词推荐
        keyword_targets = {
            'board': ['go_engine'],
            'game': ['go_engine'],
            'score': ['go_engine'],
            'stone': ['go_engine'],
            'gene': ['gene_engine'],
            'dna': ['gene_engine'],
            'evolution': ['gene_engine'],
            'scan': ['gene_engine'],
            'knowledge': ['hacker_engine'],
            'hack': ['hacker_engine'],
            'bridge': ['hacker_engine'],
        }
        
        if part.part_type in type_targets:
            targets.extend(type_targets[part.part_type])
        
        for keyword, target_list in keyword_targets.items():
            if keyword in name_lower:
                targets.extend(target_list)
        
        return list(set(targets))
    
    def _generate_summary(self):
        """生成分析摘要"""
        print("\n" + "=" * 70)
        print("【BSD 三大引擎部件提取 · 摘要】")
        print("=" * 70)
        
        # 按来源引擎统计
        engine_stats = {}
        for part in self.extracted_parts:
            engine = part.source_engine
            if engine not in engine_stats:
                engine_stats[engine] = {'total': 0, 'public': 0}
            engine_stats[engine]['total'] += 1
            if part.can_be_public:
                engine_stats[engine]['public'] += 1
        
        print("\n📊 各引擎可独立部件统计:")
        for engine, stats in engine_stats.items():
            engine_name = THREE_ENGINES.get(engine, {}).get('name', engine)
            print(f"  {engine_name}:")
            print(f"    - 可独立部件: {stats['total']} 个")
            print(f"    - 可公有部件: {stats['public']} 个")
        
        # 按部件类型统计
        type_stats = {}
        for part in self.extracted_parts:
            t = part.part_type.value if hasattr(part.part_type, 'value') else str(part.part_type)
            if t not in type_stats:
                type_stats[t] = 0
            type_stats[t] += 1
        
        print("\n📊 部件类型分布:")
        for t, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * min(count, 20)
            print(f"  {t}: {count:3d} 个 {bar}")
        
        # 高价值部件 TOP 10
        high_value = sorted(
            [p for p in self.extracted_parts if p.can_be_public],
            key=lambda x: x.public_value,
            reverse=True
        )[:10]
        
        if high_value:
            print("\n📋 公有价值 TOP 10:")
            for i, part in enumerate(high_value, 1):
                engine_name = THREE_ENGINES.get(part.source_engine, {}).get('name', part.source_engine)
                print(f"  {i:2}. [{engine_name}] {part.part_name} (价值: {part.public_value:.1%})")
        
        # 公有化建议
        total_parts = len(self.extracted_parts)
        public_parts = sum(1 for p in self.extracted_parts if p.can_be_public)
        
        print(f"\n📈 公有化潜力:")
        print(f"  - 发现可独立部件: {total_parts} 个")
        print(f"  - 可公有部件: {public_parts} 个")
        print(f"  - 公有化率: {public_parts / max(total_parts, 1):.1%}")


# ============================================================
# 公有部件注册系统
# ============================================================

class ThreeEnginePartRegistry:
    """三大引擎公有部件注册表"""
    
    def __init__(self):
        self.registry: Dict[str, ExtractedPart] = {}
        self.engine_parts: Dict[str, List[str]] = {}
        self.shared_parts: List[str] = []
        self.registration_history: List[Dict[str, Any]] = []
    
    def register_parts(self, parts: List[ExtractedPart]) -> Dict[str, Any]:
        """批量注册部件"""
        print("\n" + "=" * 70)
        print("【BSD 三大引擎公有部件 · 注册】")
        print("=" * 70)
        
        registered = 0
        skipped = 0
        
        for part in parts:
            if not part.can_be_public:
                skipped += 1
                continue
            
            # 注册
            key = f"{part.source_engine}.{part.part_name}"
            self.registry[key] = part
            registered += 1
            
            # 按引擎分组
            if part.source_engine not in self.engine_parts:
                self.engine_parts[part.source_engine] = []
            self.engine_parts[part.source_engine].append(part.part_name)
        
        # 识别共享部件（被多个引擎引用）
        self._identify_shared_parts()
        
        result = {
            'registered': registered,
            'skipped': skipped,
            'total_parts': len(self.registry),
            'shared_parts': len(self.shared_parts)
        }
        
        print(f"\n📊 注册结果:")
        print(f"  - 成功注册: {registered} 个部件")
        print(f"  - 跳过（不可公有）: {skipped} 个部件")
        print(f"  - 注册表总量: {result['total_parts']} 个部件")
        print(f"  - 跨引擎共享部件: {result['shared_parts']} 个")
        
        self.registration_history.append({
            'timestamp': datetime.now().isoformat(),
            'result': result
        })
        
        return result
    
    def _identify_shared_parts(self):
        """识别跨引擎共享部件"""
        # 检查部件是否被多个引擎的代码引用
        part_names = list(set(p.part_name for p in self.registry.values()))
        
        for name in part_names:
            engines_using = set()
            for key, part in self.registry.items():
                if part.part_name == name:
                    engines_using.add(part.source_engine)
            
            if len(engines_using) > 1:
                self.shared_parts.append(name)
    
    def get_part(self, name: str) -> Optional[ExtractedPart]:
        """获取部件"""
        for key, part in self.registry.items():
            if part.part_name == name:
                return part
        return None
    
    def get_engine_parts(self, engine: str) -> List[ExtractedPart]:
        """获取指定引擎的所有部件"""
        parts = []
        for key, part in self.registry.items():
            if part.source_engine == engine:
                parts.append(part)
        return parts
    
    def generate_refactoring_plan(self) -> Dict[str, Any]:
        """生成重构计划"""
        print("\n" + "=" * 70)
        print("【BSD 三大引擎 · 重构计划】")
        print("=" * 70)
        
        plan = {
            'go_engine': self._plan_refactoring('go'),
            'gene_engine': self._plan_refactoring('gene'),
            'hacker_engine': self._plan_refactoring('hacker'),
        }
        
        return plan
    
    def _plan_refactoring(self, engine_key: str) -> Dict[str, Any]:
        """为单个引擎生成重构计划"""
        engine_name = THREE_ENGINES.get(engine_key, {}).get('name', engine_key)
        parts = self.get_engine_parts(engine_key)
        
        print(f"\n🔧 {engine_name} 重构计划:")
        print("-" * 50)
        
        # 分析可提取的部件
        data_structures = [p for p in parts if p.part_type == ExtractedPartType.DATA_STRUCTURE]
        algorithms = [p for p in parts if p.part_type == ExtractedPartType.ALGORITHM]
        managers = [p for p in parts if p.part_type == ExtractedPartType.MANAGER]
        
        print(f"  📦 可提取数据结构: {len(data_structures)} 个")
        for ds in data_structures:
            print(f"    - {ds.part_name} (公有价值: {ds.public_value:.1%})")
        
        print(f"  ⚡ 可提取算法: {len(algorithms)} 个")
        for algo in algorithms[:5]:  # 最多显示5个
            print(f"    - {algo.part_name} (公有价值: {algo.public_value:.1%})")
        if len(algorithms) > 5:
            print(f"    ... 还有 {len(algorithms) - 5} 个")
        
        print(f"  🎯 可提取管理器: {len(managers)} 个")
        for mgr in managers[:5]:
            print(f"    - {mgr.part_name} (公有价值: {mgr.public_value:.1%})")
        if len(managers) > 5:
            print(f"    ... 还有 {len(managers) - 5} 个")
        
        # 计算重构效益
        current_code_lines = sum(len(p.code_snippet.split('\n')) for p in parts)
        refactored_code_lines = sum(
            len(p.code_snippet.split('\n')) 
            for p in parts 
            if p.can_be_public and p.public_value > 0.5
        )
        savings = current_code_lines - refactored_code_lines
        
        print(f"\n  📊 重构效益估算:")
        print(f"    - 当前代码行数: ~{current_code_lines} 行")
        print(f"    - 提取后保留: ~{refactored_code_lines} 行")
        print(f"    - 节省: ~{savings} 行 ({savings / max(current_code_lines, 1):.1%})")
        
        return {
            'engine': engine_name,
            'total_parts': len(parts),
            'data_structures': [d.to_dict() for d in data_structures],
            'algorithms': [a.to_dict() for a in algorithms],
            'managers': [m.to_dict() for m in managers],
            'current_code_lines': current_code_lines,
            'refactored_code_lines': refactored_code_lines,
            'savings': savings,
            'savings_rate': savings / max(current_code_lines, 1)
        }


# ============================================================
# 主流程
# ============================================================

def main():
    """主程序"""
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("【BSD 三大引擎逆向部件提取系统】")
    print("=" * 70)
    print("\n  理论背景：")
    print("    黑客、围棋、基因三大引擎是在没有六系立系引擎论指导下独立构建的")
    print("    导致其内部部件耦合，未能独立")
    print("    现在需要逆向提取部件，让它们回归公有架构")
    print()
    
    # 1. 分析三大引擎
    analyzer = PartAnalyzer(base_path)
    extracted_parts = analyzer.analyze_three_engines()
    
    # 2. 注册公有部件
    registry = ThreeEnginePartRegistry()
    reg_result = registry.register_parts(extracted_parts)
    
    # 3. 生成重构计划
    refactoring_plan = registry.generate_refactoring_plan()
    
    # 4. 生成最终报告
    print("\n" + "=" * 70)
    print("【BSD 三大引擎 · 逆向提取完成】")
    print("=" * 70)
    
    total_parts = len(extracted_parts)
    public_parts = sum(1 for p in extracted_parts if p.can_be_public)
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║  核心成果：                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐        ║
║  │  1. 从三大引擎提取可独立部件: {total_parts} 个                              │        ║
║  │  2. 可公有部件: {public_parts} 个                                        │        ║
║  │  3. 公有化率: {public_parts / max(total_parts, 1):.1%}                          │        ║
║  │  4. 跨引擎共享部件: {reg_result['shared_parts']} 个                       │        ║
║  └─────────────────────────────────────────────────────────────────────┘        ║
║                                                                                  ║
║  下一步行动：                                                                    ║
║  • 将高价值部件（公有价值>0.5）提取到独立模块                                   ║
║  • 创建部件公有注册表，支持多引擎共享                                           ║
║  • 重构三大引擎，使用公有部件                                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
""")
    
    return {
        'extracted_parts': [p.to_dict() for p in extracted_parts],
        'registration': reg_result,
        'refactoring_plan': refactoring_plan
    }


if __name__ == '__main__':
    main()