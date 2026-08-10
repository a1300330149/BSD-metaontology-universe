#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引擎识别检测系统 (Engine Detection System)
============================================

核心使命：
    在制造新引擎之前，先检测现有引擎库中是否已存在相同或可复用的引擎，
    彻底避免重复搭建（防止造轮子），贯彻虚拟宇宙「公有部件」理念。

设计原则：
    1. 先检测后制造：任何新引擎制造前必须先通过检测
    2. 部件优先复用：优先使用已有的公有部件
    3. 组合优先重建：优先组合现有引擎而非从零构建
    4. 理论验证：检测结果需通过理论-引擎映射验证

检测维度：
    - 功能相似度：是否已有引擎实现了相同功能
    - 六系归属：是否在同一六系中有成熟引擎
    - 依赖兼容性：现有引擎的依赖是否可复用
    - 公有部件匹配：是否有可直接复用的公有部件

检测决策树：
    需求 → 检测现有引擎 → 找到完全匹配？→ 是 → 直接复用
                              ↓否
                         找到相似引擎？→ 是 → 扩展/组合现有引擎
                              ↓否
                         找到公有部件？→ 是 → 基于部件组装
                              ↓否
                         从零构建新引擎
"""

import os
import sys
import re
import json
import ast
import importlib
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

_BSD_ENGINE_PATH = os.path.join(_BSD_OAPS_PATH, 'bsd_engine')
_BSD_CORE_PATH = os.path.join(_BSD_ENGINE_PATH, 'core')
_PUBLIC_PARTS_PATH = os.path.join(_BSD_CORE_PATH, 'public_parts')


# ============================================================
# 1. 检测结果分类
# ============================================================

class DetectionVerdict(Enum):
    """检测裁决"""
    REUSE = "直接复用"           # 已有完全匹配的引擎
    EXTEND = "扩展现有"         # 有相似引擎，可扩展
    COMPOSE = "组合构建"         # 可通过组合现有部件实现
    BUILD_NEW = "从零构建"       # 无匹配，需全新构建
    INVALID = "需求无效"         # 需求描述不清或违反公理


class MatchLevel(Enum):
    """匹配等级"""
    EXACT = 1.0       # 精确匹配（功能完全一致）
    HIGH = 0.8        # 高匹配（核心功能一致）
    MEDIUM = 0.6      # 中等匹配（部分功能重叠）
    LOW = 0.3         # 低匹配（仅相关）
    NONE = 0.0        # 无匹配


# ============================================================
# 2. 引擎特征提取
# ============================================================

@dataclass
class EngineSignature:
    """引擎签名——用于相似度比对的特征向量"""
    signature_id: str
    name: str
    file_path: str
    functions: List[str]              # 公开方法/函数
    classes: List[str]                # 类名
    imports: List[str]                # 导入的模块
    six_system: str = "未分类"         # 六系归属
    engine_type: str = "unknown"      # part/component/system
    keywords: List[str] = field(default_factory=list)
    code_lines: int = 0
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'signature_id': self.signature_id,
            'name': self.name,
            'file_path': self.file_path,
            'functions': self.functions,
            'classes': self.classes,
            'imports': self.imports,
            'six_system': self.six_system,
            'engine_type': self.engine_type,
            'keywords': self.keywords,
            'code_lines': self.code_lines,
            'dependencies': self.dependencies,
        }


@dataclass
class DetectionResult:
    """检测结果"""
    query_id: str
    query_description: str
    verdict: DetectionVerdict
    confidence: float
    matches: List[Tuple[EngineSignature, float]]  # (签名, 相似度)
    recommendation: str
    action_plan: List[str]
    theory_validation: Optional[Dict[str, Any]] = None
    timestamp: str = ""


# ============================================================
# 3. 引擎库扫描器
# ============================================================

class EngineLibraryScanner:
    """
    引擎库扫描器
    
    扫描所有现有引擎文件，提取签名特征，构建引擎签名库
    """
    
    def __init__(self, scan_paths: List[str] = None):
        self.scan_paths = scan_paths or [
            _BSD_CORE_PATH,
            os.path.join(_BSD_ENGINE_PATH, 'theories'),
            os.path.join(_BSD_ENGINE_PATH, 'axioms'),
            os.path.join(_BSD_ENGINE_PATH, 'equations'),
            os.path.join(_BSD_ENGINE_PATH, 'validators'),
            os.path.join(_BSD_OAPS_PATH, 'physical_body'),
        ]
        self.signatures: Dict[str, EngineSignature] = {}
        self._scan_complete = False
    
    def scan(self) -> Dict[str, EngineSignature]:
        """扫描所有引擎文件，提取签名"""
        print("\n" + "=" * 60)
        print("【引擎检测】扫描引擎库...")
        print("=" * 60)
        
        total_files = 0
        for scan_path in self.scan_paths:
            if not os.path.isdir(scan_path):
                continue
            
            for root, dirs, files in os.walk(scan_path):
                for fname in files:
                    if fname.endswith('.py') and not fname.startswith('__'):
                        total_files += 1
                        fpath = os.path.join(root, fname)
                        try:
                            sig = self._extract_signature(fpath)
                            if sig:
                                self.signatures[sig.signature_id] = sig
                        except Exception as e:
                            pass
        
        self._scan_complete = True
        print(f"  扫描文件: {total_files} 个")
        print(f"  提取签名: {len(self.signatures)} 个")
        
        # 按类型统计
        type_stats: Dict[str, int] = {}
        for sig in self.signatures.values():
            t = sig.engine_type
            type_stats[t] = type_stats.get(t, 0) + 1
        
        for t, count in sorted(type_stats.items()):
            print(f"    {t}: {count} 个")
        
        # 按六系统计
        sys_stats: Dict[str, int] = {}
        for sig in self.signatures.values():
            s = sig.six_system
            sys_stats[s] = sys_stats.get(s, 0) + 1
        
        for s, count in sorted(sys_stats.items()):
            print(f"    {s}: {count} 个")
        
        return self.signatures
    
    def _extract_signature(self, fpath: str) -> Optional[EngineSignature]:
        """从Python文件提取引擎签名"""
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 跳过测试文件和非引擎文件
            if content.strip().startswith('#') and 'test' in fpath.lower():
                return None
            
            tree = ast.parse(content)
            
            # 提取类名
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            
            # 提取顶层函数
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            
            # 提取导入
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # 计算代码行数
            code_lines = len(content.split('\n'))
            
            # 检测引擎类型
            eng_type = self._detect_type(fpath, content, classes)
            
            # 检测六系归属
            six_sys = self._detect_six_system(content)
            
            # 提取关键词
            keywords = self._extract_keywords(content, classes, functions)
            
            # 检测依赖
            dependencies = self._detect_dependencies(imports)
            
            sig_id = f"sig_{abs(hash(os.path.basename(fpath))) % 100000:05d}"
            
            return EngineSignature(
                signature_id=sig_id,
                name=os.path.basename(fpath).replace('.py', ''),
                file_path=fpath,
                functions=functions,
                classes=classes,
                imports=imports,
                six_system=six_sys,
                engine_type=eng_type,
                keywords=keywords,
                code_lines=code_lines,
                dependencies=dependencies,
            )
        except Exception:
            return None
    
    def _detect_type(self, fpath: str, content: str, classes: List[str]) -> str:
        """检测引擎类型"""
        name = os.path.basename(fpath).lower()
        
        if 'public' in name or 'part_' in name or 'common' in name:
            return 'part'
        elif 'system' in name or 'registry' in name or 'hub' in name:
            return 'system'
        elif 'match' in name or 'game' in name or 'manager' in name:
            return 'component'
        elif 'engine' in name:
            return 'component'
        elif 'core' in fpath.lower():
            return 'system'
        return 'part'
    
    def _detect_six_system(self, content: str) -> str:
        """检测六系归属"""
        system_keywords = {
            '强化系🔵': ['强化系', 'connection', 'connect', 'register'],
            '自然系🟠': ['自然系', 'activation', 'activate', 'detect'],
            '具现系🔴': ['具现系', 'fusion', 'fuse', 'emerge'],
            '变身系⚫': ['变身系', 'elevation', 'elevate', 'transform'],
            '社会系🟢': ['社会系', 'equilibrium', 'balance', 'social'],
            '天道系🟣': ['天道系', 'metamorphosis', 'cosmolog', 'infinite'],
        }
        
        content_lower = content.lower()
        scores: Dict[str, int] = {}
        for sys_name, keywords in system_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in content_lower)
            if score > 0:
                scores[sys_name] = score
        
        if scores:
            return max(scores, key=scores.get)
        return '未分类'
    
    def _extract_keywords(self, content: str, classes: List[str], functions: List[str]) -> List[str]:
        """提取特征关键词"""
        keywords = set()
        
        # 从类名提取
        for cls in classes:
            # 分词：大写字母分割
            parts = re.findall(r'[A-Z][a-z]+', cls)
            keywords.update([p.lower() for p in parts if len(p) > 2])
        
        # 从函数名提取关键部分
        for func in functions:
            parts = func.split('_')
            keywords.update([p for p in parts if len(p) > 2])
        
        # 从内容提取中文关键词
        chinese = re.findall(r'[\u4e00-\u9fff]{2,4}', content[:1000])
        keywords.update(chinese)
        
        return list(keywords)[:50]
    
    def _detect_dependencies(self, imports: List[str]) -> List[str]:
        """检测引擎依赖"""
        internal_deps = [imp for imp in imports if 'bsd' in imp.lower() or 'engine' in imp.lower()]
        return internal_deps
    
    def get_signatures_by_type(self, eng_type: str) -> List[EngineSignature]:
        """按类型获取签名"""
        return [s for s in self.signatures.values() if s.engine_type == eng_type]
    
    def get_signatures_by_system(self, six_system: str) -> List[EngineSignature]:
        """按六系获取签名"""
        return [s for s in self.signatures.values() if s.six_system == six_system]


# ============================================================
# 4. 引擎检测器（核心检测逻辑）
# ============================================================

class EngineDetector:
    """
    引擎识别检测器
    
    核心流程：
    1. 接收引擎制造需求（功能描述、六系归属、类型）
    2. 扫描现有引擎库
    3. 计算需求与现有引擎的相似度
    4. 给出检测裁决与行动建议
    """
    
    # 功能关键词库——需求描述→关键词映射
    FUNCTION_KEYWORD_MAP: Dict[str, List[str]] = {
        '连接注册': ['connect', 'register', '连接', '注册', '注册中心', 'hub'],
        '激活检测': ['activate', 'detect', '激活', '检测', 'scan', 'discover'],
        '融合组装': ['fuse', 'compose', '融合', '组装', 'assemble', 'combine'],
        '升维进化': ['elevate', 'evolve', '升维', '进化', 'transform', 'upgrade'],
        '协同计算': ['equilibrium', 'collaborate', '协同', '计算', 'balance', 'gravity'],
        '永动计算': ['metamorphosis', 'cosmological', '永动', '宇宙', 'infinite', 'limit'],
        '围棋博弈': ['go', 'weiqi', '围棋', 'board', 'stone', 'gomoku'],
        '基因分析': ['gene', 'genetic', '基因', 'dna', 'protein', 'evolution'],
        '黑客突破': ['hack', 'bridge', '突破', '对接', 'inject', 'bypass'],
        '记忆系统': ['memory', 'anchor', '记忆', '锚点', 'compress', 'recall'],
        '元数据': ['metadata', 'registry', '元数据', '注册表', 'catalog'],
        '部件管理': ['part', 'component', '部件', '组件', 'public', 'reusable'],
        '理论驱动': ['theory', 'axiom', '理论', '公理', 'theorem', 'proof'],
        '方程计算': ['equation', 'formula', '方程', '公式', 'compute', 'calculate'],
        '验证测试': ['verify', 'validate', '验证', '测试', 'check', 'compliance'],
        '仿真模拟': ['simulate', 'simulation', '仿真', '模拟', 'model', 'run'],
    }
    
    def __init__(self):
        self.scanner = EngineLibraryScanner()
        self._signatures_loaded = False
        self._detection_history: List[DetectionResult] = []
    
    def detect(self, 
               function_description: str,
               six_system: str = None,
               engine_type: str = None,
               min_confidence: float = 0.3) -> DetectionResult:
        """
        执行引擎检测
        
        Args:
            function_description: 功能描述（自然语言）
            six_system: 六系归属（可选，缩小搜索范围）
            engine_type: 引擎类型（可选，part/component/system）
            min_confidence: 最低匹配阈值
        
        Returns:
            DetectionResult 检测结果
        """
        # 1. 确保签名库已加载
        if not self._signatures_loaded:
            self.scanner.scan()
            self._signatures_loaded = True
        
        # 2. 从需求描述提取功能关键词
        query_keywords = self._extract_query_keywords(function_description)
        
        # 3. 计算与每个引擎签名的相似度
        matches = []
        for sig in self.scanner.signatures.values():
            # 可选过滤
            if six_system and sig.six_system != six_system:
                continue
            if engine_type and sig.engine_type != engine_type:
                continue
            
            similarity = self._compute_similarity(query_keywords, sig, function_description)
            if similarity >= min_confidence:
                matches.append((sig, similarity))
        
        # 按相似度排序
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # 4. 做出检测裁决
        verdict, confidence = self._make_verdict(matches, function_description)
        
        # 5. 生成行动建议
        recommendation = self._generate_recommendation(verdict, matches, function_description)
        action_plan = self._generate_action_plan(verdict, matches, function_description)
        
        result = DetectionResult(
            query_id=f"det_{abs(hash(function_description + datetime.now().isoformat())) % 100000:05d}",
            query_description=function_description,
            verdict=verdict,
            confidence=confidence,
            matches=matches[:10],  # 最多返回10个匹配
            recommendation=recommendation,
            action_plan=action_plan,
            timestamp=datetime.now().isoformat(),
        )
        
        self._detection_history.append(result)
        return result
    
    def _extract_query_keywords(self, description: str) -> Dict[str, float]:
        """从需求描述提取功能关键词及权重"""
        keywords = {}
        desc_lower = description.lower()
        
        # 匹配功能关键词库
        for func_name, kw_list in self.FUNCTION_KEYWORD_MAP.items():
            score = 0
            for kw in kw_list:
                if kw.lower() in desc_lower:
                    score += 1.0
                    # 记录匹配的原始关键词
                    keywords[kw.lower()] = max(keywords.get(kw.lower(), 0), 0.5)
            if score > 0:
                keywords[f'__func_{func_name}'] = score
        
        # 额外提取中文关键词
        chinese = re.findall(r'[\u4e00-\u9fff]{2,4}', description)
        for c in chinese:
            keywords[c] = max(keywords.get(c, 0), 0.3)
        
        # 额外提取英文关键词
        english = re.findall(r'[a-zA-Z]{3,}', description)
        for e in english:
            keywords[e.lower()] = max(keywords.get(e.lower(), 0), 0.2)
        
        return keywords
    
    def _compute_similarity(self, 
                            query_keywords: Dict[str, float], 
                            sig: EngineSignature,
                            description: str) -> float:
        """计算需求与引擎签名的相似度"""
        if not query_keywords:
            return 0.0
        
        score = 0.0
        total_weight = 0.0
        
        # 关键词匹配
        sig_keywords_lower = set(k.lower() for k in sig.keywords)
        sig_functions_lower = set(f.lower() for f in sig.functions)
        sig_classes_lower = set(c.lower() for c in sig.classes)
        sig_name_lower = sig.name.lower()
        
        for kw, weight in query_keywords.items():
            total_weight += weight
            
            kw_lower = kw.lower()
            # 精确匹配
            if kw_lower in sig_keywords_lower:
                score += weight * 1.0
            # 函数名匹配
            elif kw_lower in sig_functions_lower:
                score += weight * 0.9
            # 类名匹配
            elif kw_lower in sig_classes_lower:
                score += weight * 0.8
            # 名称匹配
            elif kw_lower in sig_name_lower:
                score += weight * 0.7
            # 子串匹配
            elif kw_lower in sig_name_lower or kw_lower in sig_name_lower:
                score += weight * 0.4
        
        # 六系加成
        desc_sys = self._detect_query_six_system(description)
        if desc_sys and desc_sys == sig.six_system:
            score += 0.15
        
        # 类型加成
        if 'part' in description.lower() and sig.engine_type == 'part':
            score += 0.1
        
        return min(score / max(total_weight, 1.0), 1.0)
    
    def _detect_query_six_system(self, description: str) -> Optional[str]:
        """检测需求的六系归属"""
        sys_patterns = {
            '强化系🔵': ['强化', '连接', '注册'],
            '自然系🟠': ['自然', '激活', '检测'],
            '具现系🔴': ['具现', '融合', '组装'],
            '变身系⚫': ['变身', '升维', '进化'],
            '社会系🟢': ['社会', '协同', '计算'],
            '天道系🟣': ['天道', '永动', '宇宙'],
        }
        for sys_name, patterns in sys_patterns.items():
            for p in patterns:
                if p in description:
                    return sys_name
        return None
    
    def _make_verdict(self, 
                      matches: List[Tuple[EngineSignature, float]],
                      description: str) -> Tuple[DetectionVerdict, float]:
        """根据匹配结果做出裁决"""
        if not matches:
            return DetectionVerdict.BUILD_NEW, 0.0
        
        best_match, best_score = matches[0]
        
        if best_score >= 0.85:
            # 精确匹配
            return DetectionVerdict.REUSE, best_score
        elif best_score >= 0.65:
            # 高匹配
            return DetectionVerdict.EXTEND, best_score
        elif best_score >= 0.45:
            # 中等匹配——看是否有多个可组合
            if len(matches) >= 2:
                combined_score = matches[0][1] + matches[1][1] * 0.5
                if combined_score >= 0.8:
                    return DetectionVerdict.COMPOSE, combined_score
            return DetectionVerdict.COMPOSE, best_score
        elif best_score >= 0.25:
            # 低匹配
            return DetectionVerdict.COMPOSE, best_score
        else:
            return DetectionVerdict.BUILD_NEW, best_score
    
    def _generate_recommendation(self, 
                                  verdict: DetectionVerdict,
                                  matches: List[Tuple[EngineSignature, float]],
                                  description: str) -> str:
        """生成推荐建议"""
        if verdict == DetectionVerdict.REUSE:
            sig = matches[0][0]
            return f"✅ 检测到完全匹配的引擎【{sig.name}】，建议直接复用，无需重新制造。"
        elif verdict == DetectionVerdict.EXTEND:
            sig = matches[0][0]
            return f"🔧 检测到高度相似的引擎【{sig.name}】，建议基于现有引擎扩展功能。"
        elif verdict == DetectionVerdict.COMPOSE:
            names = [m[0].name for m in matches[:3]]
            return f"🧩 检测到可组合的引擎部件【{', '.join(names)}】，建议通过组合构建。"
        elif verdict == DetectionVerdict.BUILD_NEW:
            return "🆕 未检测到匹配引擎，建议从零构建新引擎。"
        else:
            return "⚠️ 需求描述无效或不明确，请重新描述需求。"
    
    def _generate_action_plan(self,
                               verdict: DetectionVerdict,
                               matches: List[Tuple[EngineSignature, float]],
                               description: str) -> List[str]:
        """生成行动计划"""
        plan = []
        
        if verdict == DetectionVerdict.REUSE:
            sig = matches[0][0]
            plan.append(f"1. 导入现有引擎: import {sig.name}")
            plan.append(f"2. 实例化引擎: engine = {sig.name}()")
            plan.append(f"3. 直接使用: engine.run()")
            plan.append(f"4. 如需定制，可通过参数配置而非修改源码")
        elif verdict == DetectionVerdict.EXTEND:
            sig = matches[0][0]
            plan.append(f"1. 继承现有引擎: class NewEngine({sig.name}):")
            plan.append(f"2. 扩展需要的方法")
            plan.append(f"3. 保持向后兼容")
            plan.append(f"4. 注册到引擎注册表")
        elif verdict == DetectionVerdict.COMPOSE:
            plan.append(f"1. 分析所需功能部件")
            plan.append(f"2. 从公有部件库提取可复用部件")
            plan.append(f"3. 通过组合模式组装新引擎")
            plan.append(f"4. 验证组合后的功能完备性")
        elif verdict == DetectionVerdict.BUILD_NEW:
            plan.append(f"1. 确认需求的理论依据（映射到六系公理）")
            plan.append(f"2. 设计引擎的六阶结构")
            plan.append(f"3. 从公有部件库提取基础部件")
            plan.append(f"4. 实现特有功能")
            plan.append(f"5. 注册到引擎注册表")
            plan.append(f"6. 验证与现有引擎的兼容性")
        
        return plan
    
    def get_detection_history(self) -> List[DetectionResult]:
        """获取检测历史"""
        return self._detection_history
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取检测统计"""
        if not self._detection_history:
            return {'total': 0}
        
        verdict_counts = {}
        for result in self._detection_history:
            v = result.verdict.value
            verdict_counts[v] = verdict_counts.get(v, 0) + 1
        
        return {
            'total_detections': len(self._detection_history),
            'verdict_distribution': verdict_counts,
            'avg_confidence': sum(r.confidence for r in self._detection_history) / len(self._detection_history),
        }


# ============================================================
# 5. 便捷函数
# ============================================================

def quick_detect(function_desc: str, six_system: str = None) -> DetectionResult:
    """快速执行引擎检测"""
    detector = EngineDetector()
    return detector.detect(function_desc, six_system)


if __name__ == '__main__':
    print("=" * 60)
    print("【引擎识别检测系统演示】")
    print("=" * 60)
    
    detector = EngineDetector()
    
    test_queries = [
        "我需要一个围棋引擎，能够进行落子决策和局面评估",
        "需要一个记忆压缩系统，支持脉络蒸馏和关键词锚定",
        "构建一个全新的情感分析引擎，目前没有任何类似实现",
        "需要一个元数据注册表来管理所有引擎的信息",
        "实现一个引擎激活系统，自动发现并激活所有子引擎",
    ]
    
    for query in test_queries:
        print(f"\n🔍 需求: {query}")
        result = detector.detect(query)
        print(f"  裁决: {result.verdict.value} (置信度: {result.confidence:.2f})")
        print(f"  推荐: {result.recommendation}")
        if result.matches:
            print(f"  Top3匹配:")
            for sig, score in result.matches[:3]:
                print(f"    - {sig.name} ({score:.2f}) [{sig.engine_type}] [{sig.six_system}]")
        print(f"  行动计划:")
        for step in result.action_plan:
            print(f"    {step}")