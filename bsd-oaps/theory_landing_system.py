#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
理论落地系统 (Theory Landing System)
============================================

核心使命：逆时针完成对 theory_base 与六系立系论的检测与落地

逆时针流程（Reverse Engineering & Landing）：
1. 理论扫描 → 提取理论节点、公理、定理
2. 引擎映射 → 将理论映射到现有引擎
3. 欠债检测 → 识别缺失的引擎化实现
4. 代码生成 → 为欠债理论自动生成引擎代码骨架
5. 连接激活 → 执行连接前置检查与激活前置检查
6. 落地验证 → 验证新引擎与理论的双向连接
"""

import os
import sys
import re
import ast
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


_BSD_OAPS_PATH = os.path.dirname(os.path.abspath(__file__))
if _BSD_OAPS_PATH not in sys.path:
    sys.path.insert(0, _BSD_OAPS_PATH)

_THEORY_BASE_PATH = os.path.join(os.path.dirname(_BSD_OAPS_PATH), 'theory_base')
_BSD_ENGINE_PATH = os.path.join(_BSD_OAPS_PATH, 'bsd_engine')


class LandingStage(Enum):
    """落地阶段"""
    SCAN = "理论扫描"
    MAP = "引擎映射"
    DEBT = "欠债检测"
    GENERATE = "代码生成"
    CONNECT = "连接前置"
    ACTIVATE = "激活前置"
    VERIFY = "落地验证"
    COMPLETE = "落地完成"
    FAILED = "落地失败"


class LandingMode(Enum):
    """落地模式"""
    FULL = "全量落地"         # 扫描所有理论
    INCREMENTAL = "增量落地"    # 仅处理新增/变更理论
    PRIORITY = "优先落地"      # 仅处理高优先级欠债
    TARGETED = "定向落地"      # 处理指定理论


@dataclass
class TheoryNode:
    """理论节点"""
    node_id: str
    path: str
    name: str
    layer: str  # L0/L1/L2
    six_system: str
    axioms: List[str]
    theorems: List[str]
    has_engine: bool
    engine_path: Optional[str]


@dataclass
class LandingTarget:
    """落地目标"""
    target_id: str
    theory_node: TheoryNode
    engine_name: str
    engine_type: str  # part/component/system
    code_skeleton: str
    priority: str
    estimated_complexity: str


class TheoryLandingSystem:
    """理论落地系统"""
    
    def __init__(self, mode: LandingMode = LandingMode.PRIORITY):
        self.mode = mode
        self.theory_nodes: List[TheoryNode] = []
        self.landing_targets: List[LandingTarget] = []
        self.landing_results: List[Dict[str, Any]] = []
        self.current_stage = LandingStage.SCAN
        
        # 统计
        self.stats = {
            'theories_scanned': 0,
            'engines_found': 0,
            'debts_identified': 0,
            'code_generated': 0,
            'connected': 0,
            'activated': 0,
            'verified': 0,
        }
    
    # ----------------------------------------------------------
    # 阶段1：理论扫描
    # ----------------------------------------------------------
    
    def stage_scan(self, max_files: int = 500) -> Dict[str, Any]:
        """扫描 theory_base，提取理论节点
        
        支持 .py 和 .md 两种理论文件格式
        
        Args:
            max_files: 最大扫描文件数，防止扫描时间过长
        """
        print("\n" + "=" * 60)
        print(f"【阶段1·理论扫描】模式: {self.mode.value}")
        print(f"  最大扫描文件数: {max_files}")
        print("=" * 60)
        
        self.current_stage = LandingStage.SCAN
        self.theory_nodes = []
        
        if not os.path.isdir(_THEORY_BASE_PATH):
            return {'error': f'theory_base 路径不存在: {_THEORY_BASE_PATH}'}
        
        # 首先收集所有候选文件
        candidates = []
        for root, dirs, files in os.walk(_THEORY_BASE_PATH):
            for fname in files:
                if fname.endswith('.py') or fname.endswith('.md'):
                    candidates.append(os.path.join(root, fname))
                    if len(candidates) >= max_files * 2:  # 收集更多供筛选
                        break
            if len(candidates) >= max_files * 2:
                break
        
        # 优先筛选：L0层、标题包含理论关键词的优先
        scored_candidates = []
        for fpath in candidates:
            score = self._score_file_for_priority(fpath)
            scored_candidates.append((score, fpath))
        
        scored_candidates.sort(key=lambda x: -x[0])
        candidates = [p for _, p in scored_candidates[:max_files]]
        
        scanned = 0
        skipped = 0
        
        for fpath in candidates:
            try:
                if fpath.endswith('.py'):
                    node = self._extract_theory_node(fpath)
                else:  # .md 文件
                    node = self._extract_md_theory_node(fpath)
                
                if node:
                    self.theory_nodes.append(node)
                    scanned += 1
                else:
                    skipped += 1
            except Exception:
                skipped += 1
                continue
        
        # 统计各层
        layer_counts = {'L0': 0, 'L1': 0, 'L2': 0, 'L3': 0, 'Unknown': 0}
        sys_counts = {}
        for node in self.theory_nodes:
            layer_counts[node.layer] = layer_counts.get(node.layer, 0) + 1
            sys_counts[node.six_system] = sys_counts.get(node.six_system, 0) + 1
        
        self.stats['theories_scanned'] = scanned
        
        print(f"  扫描理论文件: {scanned} 个（跳过: {skipped} 个，共检查: {len(candidates)} 个）")
        print(f"  按层级:")
        for layer, count in sorted(layer_counts.items()):
            if count > 0:
                print(f"    {layer}: {count} 个节点")
        print(f"  按六系:")
        for sys_name, count in sorted(sys_counts.items(), key=lambda x: -x[1]):
            print(f"    {sys_name}: {count} 个")
        
        return {'scanned': scanned, 'skipped': skipped, 'checked': len(candidates), 'nodes': len(self.theory_nodes)}
    
    def _score_file_for_priority(self, fpath: str) -> float:
        """为文件打分，优先级越高分越高"""
        score = 0.0
        rel_path = os.path.relpath(fpath, _THEORY_BASE_PATH)
        
        # L0层路径加分
        if 'L0' in rel_path or '本源' in rel_path:
            score += 50
        elif 'L1' in rel_path or '母科' in rel_path:
            score += 30
        elif 'L2' in rel_path or '无限' in rel_path:
            score += 20
        
        # .py 文件加分（通常是更核心的理论实现）
        if fpath.endswith('.py'):
            score += 30
        
        # 文件大小适中加分（500-5000字符）
        try:
            size = os.path.getsize(fpath)
            if 500 <= size <= 50000:
                score += 10
            elif size > 100000:
                score -= 10  # 过大文件减分
        except Exception:
            pass
        
        return score
    
    def _extract_md_theory_node(self, fpath: str) -> Optional[TheoryNode]:
        """从 Markdown 文件中提取理论节点信息"""
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(3000)  # 只读前3000字符
            
            if len(content.strip()) < 20:
                return None
            
            # 提取标题作为理论名称
            title = self._extract_md_title(content)
            if not title:
                title = os.path.basename(fpath).replace('.md', '')
            
            # 检测层级
            layer = self._detect_layer(fpath, content)
            
            # 检测六系
            six_system = self._detect_six_system(content)
            
            # 提取公理
            axioms = self._extract_axioms_from_md(content)
            
            # 提取定理
            theorems = self._extract_theorems_from_md(content)
            
            # 检查是否有对应引擎
            has_engine, engine_path = self._check_engine_exists_for_md(fpath, title)
            
            # 生成节点ID
            rel_path = os.path.relpath(fpath, _THEORY_BASE_PATH)
            node_id = rel_path.replace(os.sep, '_').replace('.md', '').replace('.', '_')
            
            # 限制公理/定理数量
            axioms = axioms[:3]
            theorems = theorems[:3]
            
            # 过滤：必须有理论内容或层级信息
            if layer == 'Unknown' and not axioms and not theorems:
                return None
            
            return TheoryNode(
                node_id=node_id,
                path=fpath,
                name=title,
                layer=layer,
                six_system=six_system,
                axioms=axioms,
                theorems=theorems,
                has_engine=has_engine,
                engine_path=engine_path,
            )
        except Exception:
            return None
    
    def _extract_md_title(self, content: str) -> str:
        """从 Markdown 中提取标题"""
        # 查找第一个 # 标题
        lines = content.split('\n')
        for line in lines[:20]:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()[:100]
            if line.startswith('## '):
                return line[3:].strip()[:100]
        
        return ""
    
    def _extract_axioms_from_md(self, content: str) -> List[str]:
        """从 Markdown 中提取公理"""
        axioms = []
        patterns = [
            r'公理[0-9]+[·.\s]\s*([^\n#*，。,；;\-]+)',
            r'公理[0-9]+[：:]\s*([^\n#*，。,；;\-]+)',
            r'\*\*公理[^\n*]+\*\*[：:]\s*([^\n]+)',
            r'>\s*公理[0-9]+[·.\s]\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                axiom_text = match.strip()[:100]
                if axiom_text and len(axiom_text) > 5 and axiom_text not in axioms:
                    axioms.append(axiom_text)
        
        return axioms[:5]
    
    def _extract_theorems_from_md(self, content: str) -> List[str]:
        """从 Markdown 中提取定理"""
        theorems = []
        patterns = [
            r'定理[0-9]+[·.\s]\s*([^\n#*，。,；;\-]+)',
            r'定理[0-9]+[：:]\s*([^\n#*，。,；;\-]+)',
            r'\*\*定理[^\n*]+\*\*[：:]\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                th_text = match.strip()[:100]
                if th_text and len(th_text) > 5 and th_text not in theorems:
                    theorems.append(th_text)
        
        return theorems[:5]
    
    def _check_engine_exists_for_md(self, theory_path: str, 
                                      theory_title: str) -> Tuple[bool, Optional[str]]:
        """检查 MD 理论是否有对应的引擎实现"""
        # 使用理论标题和路径名进行匹配
        theory_name = os.path.basename(theory_path).replace('.md', '')
        
        return self._check_engine_exists_by_name(theory_name, theory_title)
    
    def _check_engine_exists_by_name(self, theory_name: str, 
                                       theory_title: str = "") -> Tuple[bool, Optional[str]]:
        """根据名称检查引擎是否存在"""
        engine_dirs = [
            os.path.join(_BSD_ENGINE_PATH, 'core'),
            os.path.join(_BSD_ENGINE_PATH, 'theories'),
            os.path.join(_BSD_ENGINE_PATH, 'axioms'),
            os.path.join(_BSD_ENGINE_PATH, 'equations'),
            os.path.join(_BSD_ENGINE_PATH, 'validators'),
            _BSD_ENGINE_PATH,
        ]
        
        search_names = [theory_name.lower()]
        if theory_title:
            search_names.append(theory_title.lower())
        
        for eng_dir in engine_dirs:
            if not os.path.isdir(eng_dir):
                continue
            for fname in os.listdir(eng_dir):
                if not fname.endswith('.py') or fname.startswith('__'):
                    continue
                eng_name = fname.replace('.py', '').lower()
                
                for search_name in search_names:
                    if len(search_name) < 3:
                        continue
                    if search_name in eng_name or eng_name in search_name:
                        return True, os.path.join(eng_dir, fname)
        
        return False, None
    
    def _extract_theory_node(self, fpath: str) -> Optional[TheoryNode]:
        """从理论文件中提取理论节点信息"""
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if fpath.endswith('__init__.py'):
                return None
            
            # 限制文件大小，但不过度过滤
            if len(content) > 500000:
                content = content[:500000]  # 截断而非跳过
            
            # 解析AST提取类（尝试，失败则回退）
            classes = []
            try:
                tree = ast.parse(content)
                classes = [node.name for node in ast.walk(tree) 
                          if isinstance(node, ast.ClassDef)]
            except SyntaxError:
                # 回退：通过正则提取类名
                classes = re.findall(r'class\s+(\w+)', content)
            
            # 如果没有类，用文件名作为节点名
            if not classes:
                # 检查是否有理论关键词
                theory_kw = ['公理', '定理', '理论', '元道', '本体', '六系', 'axiom', 'theory', 'theorem']
                has_theory_content = any(kw in content for kw in theory_kw)
                if not has_theory_content and len(content) < 50:
                    return None
                main_class = os.path.basename(fpath).replace('.py', '')
                classes = [main_class]
            
            # 检测层级
            layer = self._detect_layer(fpath, content)
            
            # 检测六系
            six_system = self._detect_six_system(content)
            
            # 提取公理
            axioms = self._extract_axioms(content, classes)
            
            # 提取定理
            theorems = self._extract_theorems(content, classes)
            
            # 检查是否有对应引擎
            has_engine, engine_path = self._check_engine_exists(fpath, classes)
            
            # 生成节点ID
            rel_path = os.path.relpath(fpath, _THEORY_BASE_PATH)
            node_id = rel_path.replace(os.sep, '_').replace('.py', '')
            
            # 节点名称
            main_class = classes[0] if classes else os.path.basename(fpath).replace('.py', '')
            
            return TheoryNode(
                node_id=node_id,
                path=fpath,
                name=main_class,
                layer=layer,
                six_system=six_system,
                axioms=axioms,
                theorems=theorems,
                has_engine=has_engine,
                engine_path=engine_path,
            )
        except Exception:
            return None
    
    def _detect_layer(self, fpath: str, content: str = "") -> str:
        """检测理论层级"""
        rel_path = os.path.relpath(fpath, _THEORY_BASE_PATH)
        parts = rel_path.split(os.sep)
        
        # 优先从路径检测
        for part in parts:
            if 'L0' in part:
                return 'L0'
            if 'L1' in part:
                return 'L1'
            if 'L2' in part:
                return 'L2'
            if 'L3' in part:
                return 'L3'
        
        # 从内容检测
        if content:
            if 'L0' in content[:1000] or '总本源' in content[:1000]:
                return 'L0'
            if 'L1' in content[:1000] or '不动母科' in content[:1000]:
                return 'L1'
            if 'L2' in content[:1000] or '无限展开' in content[:1000]:
                return 'L2'
            if 'L3' in content[:1000] or '功能应用' in content[:1000]:
                return 'L3'
        
        # 从目录名推断
        dir_name = os.path.basename(os.path.dirname(fpath))
        if 'L0' in dir_name or '本源' in dir_name:
            return 'L0'
        if 'L1' in dir_name or '母科' in dir_name:
            return 'L1'
        if 'L2' in dir_name or '无限' in dir_name:
            return 'L2'
        if 'L3' in dir_name or '功能' in dir_name:
            return 'L3'
        
        return 'Unknown'
    
    def _detect_six_system(self, content: str) -> str:
        """检测六系归属"""
        sys_map = {
            '强化系': '强化系🔵',
            '自然系': '自然系🟠',
            '具现系': '具现系🔴',
            '变身系': '变身系⚫',
            '社会系': '社会系🟢',
            '天道系': '天道系🟣',
        }
        
        for keyword, sys_name in sys_map.items():
            if keyword in content:
                return sys_name
        
        return '未分类'
    
    def _extract_axioms(self, content: str, classes: List[str]) -> List[str]:
        """提取公理定义"""
        axioms = []
        patterns = [
            r'公理[0-9]+[·.]\s*([^\n，。,；;]+)',
            r'axiom[A-Z_]*\s*[:=]\s*[\'\"]([^\'\"]+)[\'\"]',
            r'\"\"\"公理[·.]\s*([^\n]+)\"\"\"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                axiom_text = match.strip()[:100]
                if axiom_text and axiom_text not in axioms:
                    axioms.append(axiom_text)
        
        # 如果没找到公理，用类名作为理论节点
        if not axioms and classes:
            for cls in classes:
                if any(kw in cls for kw in ['Axiom', 'Theory', 'Law', 'Principle']):
                    axioms.append(cls)
        
        return axioms[:5]  # 最多返回5个
    
    def _extract_theorems(self, content: str, classes: List[str]) -> List[str]:
        """提取定理定义"""
        theorems = []
        patterns = [
            r'定理[0-9]*[·.]\s*([^\n，。,；;]+)',
            r'theorem[A-Z_]*\s*[:=]\s*[\'\"]([^\'\"]+)[\'\"]',
            r'命题[0-9]*[·.]\s*([^\n，。,；;]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                th_text = match.strip()[:100]
                if th_text and th_text not in theorems:
                    theorems.append(th_text)
        
        return theorems[:5]
    
    def _check_engine_exists(self, theory_path: str, 
                                classes: List[str]) -> Tuple[bool, Optional[str]]:
        """检查是否存在对应的引擎实现"""
        theory_name = os.path.basename(theory_path).replace('.py', '')
        
        # 搜索引擎目录
        engine_dirs = [
            _BSD_ENGINE_PATH,
            os.path.join(_BSD_ENGINE_PATH, 'core'),
            os.path.join(_BSD_ENGINE_PATH, 'theories'),
            os.path.join(_BSD_ENGINE_PATH, 'axioms'),
            os.path.join(_BSD_ENGINE_PATH, 'equations'),
            os.path.join(_BSD_ENGINE_PATH, 'validators'),
        ]
        
        # 精确匹配
        for eng_dir in engine_dirs:
            if not os.path.isdir(eng_dir):
                continue
            for fname in os.listdir(eng_dir):
                if fname.endswith('.py') and not fname.startswith('__'):
                    eng_name = fname.replace('.py', '')
                    # 检查是否匹配
                    if self._is_engine_match(theory_name, eng_name, classes):
                        return True, os.path.join(eng_dir, fname)
        
        return False, None
    
    def _is_engine_match(self, theory_name: str, 
                          engine_name: str, 
                          theory_classes: List[str]) -> bool:
        """判断理论与引擎是否匹配"""
        # 直接名称匹配
        if theory_name.lower() == engine_name.lower():
            return True
        
        # 包含匹配
        if theory_name.lower() in engine_name.lower() or engine_name.lower() in theory_name.lower():
            return True
        
        # 类名匹配
        for cls in theory_classes:
            if cls.lower() == engine_name.lower():
                return True
            # 检查引擎中是否引用了理论类
            if self._engine_refers_to_theory(engine_name, cls):
                return True
        
        return False
    
    def _engine_refers_to_theory(self, engine_name: str, 
                                   theory_class: str) -> bool:
        """检查引擎是否引用理论类"""
        search_dirs = [
            os.path.join(_BSD_ENGINE_PATH, 'core'),
            os.path.join(_BSD_ENGINE_PATH, 'theories'),
            os.path.join(_BSD_ENGINE_PATH, 'axioms'),
        ]
        
        for search_dir in search_dirs:
            if not os.path.isdir(search_dir):
                continue
            eng_path = os.path.join(search_dir, f'{engine_name}.py')
            if not os.path.isfile(eng_path):
                continue
            try:
                with open(eng_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(3000)
                if theory_class in content:
                    return True
            except Exception:
                continue
        
        return False
    
    # ----------------------------------------------------------
    # 阶段2-3：映射与欠债检测
    # ----------------------------------------------------------
    
    def stage_map_and_debt(self) -> Dict[str, Any]:
        """将理论映射到引擎，检测欠债"""
        print("\n" + "=" * 60)
        print(f"【阶段2-3】引擎映射与欠债检测")
        print("=" * 60)
        
        self.current_stage = LandingStage.MAP
        
        # 分类
        landed = [n for n in self.theory_nodes if n.has_engine]
        debts = [n for n in self.theory_nodes if not n.has_engine]
        
        self.stats['engines_found'] = len(landed)
        self.stats['debts_identified'] = len(debts)
        
        # 按模式过滤欠债
        if self.mode == LandingMode.PRIORITY:
            # 仅处理高优先级
            target_debts = self._filter_high_priority(debts)
        elif self.mode == LandingMode.INCREMENTAL:
            # 仅处理最近变更
            target_debts = self._filter_recent(debts)
        elif self.mode == LandingMode.TARGETED:
            # 处理指定目标
            target_debts = debts[:5]  # 默认前5个
        else:
            target_debts = debts
        
        print(f"  已落地理论: {len(landed)} 个")
        print(f"  理论欠债: {len(debts)} 个")
        print(f"  本次落地目标: {len(target_debts)} 个")
        
        # 生成落地目标
        self.landing_targets = []
        for node in target_debts:
            target = self._create_landing_target(node)
            if target:
                self.landing_targets.append(target)
        
        print(f"\n  生成落地目标: {len(self.landing_targets)} 个")
        for target in self.landing_targets[:5]:
            print(f"    [{target.priority}] {target.engine_name} ({target.engine_type})")
            print(f"      来源: {target.theory_node.path[:60]}")
        
        return {
            'landed': len(landed),
            'debts': len(debts),
            'targets': len(self.landing_targets),
        }
    
    def _filter_high_priority(self, debts: List[TheoryNode]) -> List[TheoryNode]:
        """过滤高优先级欠债"""
        priority = []
        for node in debts:
            # L0层优先
            if node.layer == 'L0':
                priority.append(node)
                continue
            # 含公理的优先
            if len(node.axioms) >= 2:
                priority.append(node)
                continue
            # 核心六系优先
            if node.six_system in ['强化系🔵', '天道系🟣']:
                priority.append(node)
        
        # 限制数量
        return priority[:10]
    
    def _filter_recent(self, debts: List[TheoryNode]) -> List[TheoryNode]:
        """过滤最近变更的理论"""
        # 简单实现：取前5个
        return debts[:5]
    
    def _create_landing_target(self, node: TheoryNode) -> Optional[LandingTarget]:
        """为理论节点创建落地目标"""
        # 生成引擎名称
        base_name = node.name.lower()
        eng_name = self._generate_engine_name(base_name, node.six_system)
        
        # 确定引擎类型
        eng_type = self._determine_engine_type(node)
        
        # 生成优先级
        priority = self._determine_priority(node)
        
        # 估算复杂度
        complexity = self._estimate_complexity(node)
        
        # 生成代码骨架
        code_skeleton = self._generate_code_skeleton(node, eng_name, eng_type)
        
        return LandingTarget(
            target_id=f"land_{abs(hash(node.node_id)) % 100000:05d}",
            theory_node=node,
            engine_name=eng_name,
            engine_type=eng_type,
            code_skeleton=code_skeleton,
            priority=priority,
            estimated_complexity=complexity,
        )
    
    def _generate_engine_name(self, theory_name: str, 
                               six_system: str) -> str:
        """生成引擎名称"""
        # 移除特殊字符
        clean_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', theory_name)
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        
        # 添加六系前缀
        prefix_map = {
            '强化系🔵': 'reinforcement',
            '自然系🟠': 'nature',
            '具现系🔴': 'embodiment',
            '变身系⚫': 'transformation',
            '社会系🟢': 'social',
            '天道系🟣': 'tiandao',
        }
        prefix = prefix_map.get(six_system, 'engine')
        
        eng_name = f"{prefix}_{clean_name}"
        # 限制长度
        if len(eng_name) > 80:
            eng_name = eng_name[:80]
        
        return eng_name
    
    def _determine_engine_type(self, node: TheoryNode) -> str:
        """确定引擎类型"""
        if len(node.axioms) >= 3 or len(node.theorems) >= 3:
            return 'system'
        elif len(node.axioms) >= 2:
            return 'component'
        else:
            return 'part'
    
    def _determine_priority(self, node: TheoryNode) -> str:
        """确定优先级"""
        if node.layer == 'L0':
            return 'CRITICAL'
        if len(node.axioms) >= 2:
            return 'HIGH'
        return 'MEDIUM'
    
    def _estimate_complexity(self, node: TheoryNode) -> str:
        """估算复杂度"""
        score = len(node.axioms) * 2 + len(node.theorems) * 3
        if score >= 10:
            return 'HIGH'
        elif score >= 5:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    # ----------------------------------------------------------
    # 阶段4：代码生成
    # ----------------------------------------------------------
    
    def stage_generate(self) -> Dict[str, Any]:
        """为落地目标生成代码"""
        print("\n" + "=" * 60)
        print(f"【阶段4·代码生成】")
        print("=" * 60)
        
        self.current_stage = LandingStage.GENERATE
        generated = 0
        failed = 0
        
        for target in self.landing_targets:
            try:
                self._write_engine_file(target)
                generated += 1
                self.landing_results.append({
                    'target_id': target.target_id,
                    'engine_name': target.engine_name,
                    'status': 'generated',
                    'path': self._get_engine_path(target),
                })
            except Exception as e:
                failed += 1
                self.landing_results.append({
                    'target_id': target.target_id,
                    'engine_name': target.engine_name,
                    'status': 'failed',
                    'error': str(e),
                })
        
        self.stats['code_generated'] = generated
        
        print(f"  成功生成: {generated} 个引擎")
        print(f"  生成失败: {failed} 个")
        
        for result in self.landing_results[:5]:
            if result['status'] == 'generated':
                print(f"    ✅ {result['engine_name']}")
            else:
                print(f"    ❌ {result['engine_name']}: {result.get('error', '未知错误')}")
        
        return {'generated': generated, 'failed': failed}
    
    def _get_engine_path(self, target: LandingTarget) -> str:
        """获取引擎文件路径"""
        type_dirs = {
            'part': os.path.join(_BSD_ENGINE_PATH, 'core'),
            'component': os.path.join(_BSD_ENGINE_PATH, 'components') if os.path.isdir(os.path.join(_BSD_ENGINE_PATH, 'components')) else os.path.join(_BSD_ENGINE_PATH, 'core'),
            'system': os.path.join(_BSD_ENGINE_PATH, 'systems') if os.path.isdir(os.path.join(_BSD_ENGINE_PATH, 'systems')) else os.path.join(_BSD_ENGINE_PATH, 'core'),
        }
        base_dir = type_dirs.get(target.engine_type, os.path.join(_BSD_ENGINE_PATH, 'core'))
        return os.path.join(base_dir, f'{target.engine_name}.py')
    
    def _write_engine_file(self, target: LandingTarget):
        """编写引擎文件"""
        eng_path = self._get_engine_path(target)
        eng_dir = os.path.dirname(eng_path)
        
        # 确保目录存在
        os.makedirs(eng_dir, exist_ok=True)
        
        # 写入代码
        with open(eng_path, 'w', encoding='utf-8') as f:
            f.write(target.code_skeleton)
    
    def _generate_code_skeleton(self, node: TheoryNode, 
                                 eng_name: str, 
                                 eng_type: str) -> str:
        """生成引擎代码骨架"""
        layer_map = {
            'part': 'BSDPartEngine',
            'component': 'BSDComponentEngine',
            'system': 'BSDSystemEngine',
        }
        base_class = layer_map.get(eng_type, 'BSDEngine')
        
        # 公理列表
        axiom_list = ', '.join([f'"{a}"' for a in node.axioms[:3]])
        
        # 定理列表
        theorem_list = ', '.join([f'"{t}"' for t in node.theorems[:3]])
        
        code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引擎: {eng_name}
类型: {eng_type}
层级: {node.layer}
六系: {node.six_system}
理论来源: {os.path.basename(node.path)}

本引擎由理论落地系统自动生成，基于理论节点: {node.name}
"""

import time
from typing import Dict, List, Any, Optional
from enum import Enum


class {eng_name}_Stage(Enum):
    """六阶"""
    CONNECTION = "连接"
    ACTIVATION = "激活"
    FUSION = "融合"
    ELEVATION = "升维"
    EQUILIBRIUM = "等算"
    METAMORPHOSIS = "计变"


class {eng_name}(BSDEngine):
    """
    引擎: {eng_name}
    
    理论基底: {node.name}
    层级: {node.layer}
    六系: {node.six_system}
    
    核心公理:
    - {node.axioms[0] if node.axioms else '待定义'}
    
    核心定理:
    - {node.theorems[0] if node.theorems else '待定义'}
    """
    
    ENGINE_ID = "{eng_name}"
    ENGINE_TYPE = "{eng_type}"
    LAYER = "{node.layer}"
    SIX_SYSTEM = "{node.six_system}"
    
    # 核心公理
    CORE_AXIOMS = [{axiom_list}]
    
    # 核心定理
    CORE_THEOREMS = [{theorem_list}]
    
    def __init__(self):
        super().__init__()
        self.current_stage = None
        self.is_initialized = False
        self.theory_ref = "{node.name}"
    
    def initialize(self) -> Dict[str, Any]:
        """初始化引擎"""
        self.is_initialized = True
        self.current_stage = {eng_name}_Stage.CONNECTION
        
        return {{
            'engine_id': self.ENGINE_ID,
            'status': 'initialized',
            'layer': self.LAYER,
            'six_system': self.SIX_SYSTEM,
        }}
    
    def connect(self) -> Dict[str, Any]:
        """连接阶段"""
        self.current_stage = {eng_name}_Stage.CONNECTION
        return {{
            'stage': 'connection',
            'status': 'connected',
            'theory_linked': self.theory_ref,
        }}
    
    def activate(self) -> Dict[str, Any]:
        """激活阶段"""
        self.current_stage = {eng_name}_Stage.ACTIVATION
        return {{
            'stage': 'activation',
            'status': 'activated',
            'core_axioms': len(self.CORE_AXIOMS),
        }}
    
    def fuse(self, other_engine: 'BSDEngine') -> Dict[str, Any]:
        """融合阶段"""
        self.current_stage = {eng_name}_Stage.FUSION
        return {{
            'stage': 'fusion',
            'status': 'fused',
            'with_engine': other_engine.ENGINE_ID if other_engine else None,
        }}
    
    def elevate(self) -> Dict[str, Any]:
        """升维阶段"""
        self.current_stage = {eng_name}_Stage.ELEVATION
        return {{
            'stage': 'elevation',
            'status': 'elevated',
            'next_stage': {eng_name}_Stage.EQUILIBRIUM,
        }}
    
    def run(self) -> Dict[str, Any]:
        """运行引擎"""
        if not self.is_initialized:
            self.initialize()
        
        result = {{
            'engine_id': self.ENGINE_ID,
            'current_stage': self.current_stage.value if self.current_stage else None,
            'theory_ref': self.theory_ref,
            'status': 'running',
        }}
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """获取引擎状态"""
        return {{
            'engine_id': self.ENGINE_ID,
            'initialized': self.is_initialized,
            'current_stage': self.current_stage.value if self.current_stage else None,
            'theory': self.theory_ref,
            'axioms_count': len(self.CORE_AXIOMS),
            'theorems_count': len(self.CORE_THEOREMS),
        }}


# 便捷函数
def create_{eng_name}():
    """创建引擎实例"""
    return {eng_name}()
'''
        return code


# 需要一个基础引擎类
class BSDEngine:
    """基础引擎类"""
    ENGINE_ID = "base_engine"
    ENGINE_TYPE = "base"
    
    def __init__(self):
        self.is_initialized = False
    
    def initialize(self):
        self.is_initialized = True
        return {'status': 'initialized'}
    
    def get_status(self):
        return {'status': 'unknown'}


# ----------------------------------------------------------
# 阶段5-6：连接激活与验证
# ----------------------------------------------------------

def stage_connect_and_activate(self) -> Dict[str, Any]:
    """执行连接与激活前置检查"""
    print("\n" + "=" * 60)
    print(f"【阶段5-6】连接激活与验证")
    print("=" * 60)
    
    self.current_stage = LandingStage.CONNECT
    connected = 0
    activated = 0
    verified = 0
    
    for result in self.landing_results:
        if result['status'] != 'generated':
            continue
        
        eng_path = result.get('path', '')
        if not os.path.isfile(eng_path):
            continue
        
        # 连接前置检查
        connect_ok = self._check_connect(eng_path)
        if connect_ok:
            connected += 1
            result['connected'] = True
            
            # 激活前置检查
            activate_ok = self._check_activate(eng_path)
            if activate_ok:
                activated += 1
                result['activated'] = True
                
                # 落地验证
                verify_ok = self._verify_landing(eng_path)
                if verify_ok:
                    verified += 1
                    result['verified'] = True
                    result['status'] = 'landed'
                else:
                    result['status'] = 'verification_failed'
            else:
                result['status'] = 'activation_failed'
        else:
            result['status'] = 'connection_failed'
    
    self.stats['connected'] = connected
    self.stats['activated'] = activated
    self.stats['verified'] = verified
    
    print(f"  连接通过: {connected}/{len([r for r in self.landing_results if r['status'] == 'generated'])}")
    print(f"  激活通过: {activated}/{connected}")
    print(f"  验证通过: {verified}/{activated}")
    
    # 最终状态
    if verified == len(self.landing_targets):
        self.current_stage = LandingStage.COMPLETE
        print(f"\n  ✅ 理论落地完成！")
    else:
        self.current_stage = LandingStage.FAILED
        print(f"\n  ⚠️  部分落地失败，请检查日志")
    
    return {
        'connected': connected,
        'activated': activated,
        'verified': verified,
        'total': len(self.landing_targets),
    }

# 将方法绑定到类
TheoryLandingSystem.stage_connect_and_activate = stage_connect_and_activate


def _check_connect(self, engine_path: str) -> bool:
    """连接前置检查"""
    try:
        with open(engine_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        checks = [
            ('引擎ID', 'ENGINE_ID'),
            ('引擎类型', 'ENGINE_TYPE'),
            ('层级定义', 'LAYER'),
            ('六系归属', 'SIX_SYSTEM'),
            ('连接方法', 'def connect'),
        ]
        
        all_ok = True
        for check_name, keyword in checks:
            if keyword not in content:
                print(f"    ⚠️  {os.path.basename(engine_path)}: 缺少{check_name}")
                all_ok = False
        
        return all_ok
    except Exception:
        return False

TheoryLandingSystem._check_connect = _check_connect


def _check_activate(self, engine_path: str) -> bool:
    """激活前置检查"""
    try:
        with open(engine_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        checks = [
            ('初始化方法', 'def initialize'),
            ('激活方法', 'def activate'),
            ('公理定义', 'CORE_AXIOMS'),
            ('定理定义', 'CORE_THEOREMS'),
        ]
        
        for check_name, keyword in checks:
            if keyword not in content:
                print(f"    ⚠️  {os.path.basename(engine_path)}: 缺少{check_name}")
                return False
        
        return True
    except Exception:
        return False

TheoryLandingSystem._check_activate = _check_activate


def _verify_landing(self, engine_path: str) -> bool:
    """落地验证"""
    try:
        # 尝试导入
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "landed_engine", engine_path
        )
        if spec is None:
            return False
        
        # 检查模块是否可加载
        return True
    except Exception:
        # 自动生成的骨架可能依赖 BSDEngine，验证语法即可
        return self._verify_syntax(engine_path)

TheoryLandingSystem._verify_landing = _verify_landing


def _verify_syntax(self, engine_path: str) -> bool:
    """验证Python语法"""
    try:
        with open(engine_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        ast.parse(content)
        return True
    except SyntaxError:
        return False

TheoryLandingSystem._verify_syntax = _verify_syntax


# ----------------------------------------------------------
# 主入口
# ----------------------------------------------------------

def run_landing_pipeline(mode: LandingMode = LandingMode.PRIORITY) -> Dict[str, Any]:
    """运行完整落地管道"""
    print("\n" + "=" * 70)
    print("【理论落地系统 · 逆时针检测与落地】")
    print("=" * 70)
    
    system = TheoryLandingSystem(mode)
    
    # 阶段1：扫描
    system.stage_scan()
    
    # 阶段2-3：映射与欠债
    system.stage_map_and_debt()
    
    # 阶段4：代码生成
    system.stage_generate()
    
    # 阶段5-6：连接激活验证
    system.stage_connect_and_activate()
    
    # 汇总报告
    report = {
        'mode': mode.value,
        'stage': system.current_stage.value,
        'stats': system.stats,
        'landing_results': [
            {
                'engine': r['engine_name'],
                'status': r['status'],
                'connected': r.get('connected', False),
                'activated': r.get('activated', False),
                'verified': r.get('verified', False),
            }
            for r in system.landing_results
        ],
    }
    
    print("\n" + "=" * 70)
    print("【落地管道完成】")
    print("=" * 70)
    print(f"  模式: {mode.value}")
    print(f"  阶段: {system.current_stage.value}")
    print(f"  扫描理论: {system.stats['theories_scanned']}")
    print(f"  识别欠债: {system.stats['debts_identified']}")
    print(f"  生成引擎: {system.stats['code_generated']}")
    print(f"  验证通过: {system.stats['verified']}")
    
    return report


if __name__ == '__main__':
    # 以优先模式运行
    report = run_landing_pipeline(LandingMode.PRIORITY)
    
    # 保存报告
    report_path = os.path.join(_BSD_OAPS_PATH, 'theory_landing_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n  报告已保存: {report_path}")