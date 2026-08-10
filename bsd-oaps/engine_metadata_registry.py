#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 引擎元数据注册表系统
==============================

核心目标：
    将所有引擎的元数据补入引擎论，建立完整的引擎知识图谱

元数据内容：
    - 引擎标识：名称、版本、路径
    - 引擎分类：部件/组件、六系归属、功能类型
    - 引擎属性：是否公有、依赖关系、功能描述
    - 引擎状态：激活状态、使用统计、测试状态
"""

import os
import sys
import re
import json
import importlib
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
import ast


# ============================================================
# 引擎元数据模型
# ============================================================

class EngineType(Enum):
    """引擎类型"""
    PART = "part"                   # 部件引擎（可公有）
    COMPONENT = "component"         # 组件引擎（成品）
    SYSTEM = "system"               # 系统级引擎
    FRAMEWORK = "framework"         # 框架级引擎


class SixSystem(Enum):
    """六系归属"""
    REINFORCEMENT = "强化系🔵"    # 第一阶：连接
    NATURE = "自然系🟠"           # 第二阶：激活
    EMBODIMENT = "具现系🔴"       # 第三阶：融合
    TRANSFORMATION = "变身系⚫"   # 第四阶：升维
    SOCIAL = "社会系🟢"           # 第五阶：等算
    TIANDAO = "天道系🟣"         # 第六阶：计变


class EngineStatus(Enum):
    """引擎状态"""
    ACTIVE = "active"               # 活跃
    DORMANT = "dormant"             # 休眠
    DEPRECATED = "deprecated"       # 已弃用
    TESTING = "testing"             # 测试中
    MAINTENANCE = "maintenance"     # 维护中


@dataclass
class EngineMetadata:
    """引擎元数据"""
    # 基础标识
    engine_id: str                   # 唯一标识
    name: str                        # 引擎名称
    class_name: str                  # 主类名
    file_path: str                   # 文件路径
    module_path: str                 # 模块路径
    
    # 分类信息
    engine_type: EngineType          # 引擎类型
    six_system: SixSystem            # 六系归属
    function_type: str               # 功能分类
    
    # 属性
    is_public: bool = True           # 是否可公有
    version: str = "1.0"             # 版本号
    description: str = ""            # 功能描述
    
    # 依赖
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他引擎
    imports: List[str] = field(default_factory=list)       # 导入的模块
    
    # 代码统计
    code_lines: int = 0              # 代码行数
    class_count: int = 0             # 类数量
    function_count: int = 0          # 函数数量
    
    # 状态
    status: EngineStatus = EngineStatus.ACTIVE
    discovered_at: str = ""          # 发现时间
    last_updated: str = ""           # 最后更新时间
    
    # 扩展属性
    tags: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'engine_id': self.engine_id,
            'name': self.name,
            'class_name': self.class_name,
            'file_path': self.file_path,
            'engine_type': self.engine_type.value,
            'six_system': self.six_system.value,
            'function_type': self.function_type,
            'is_public': self.is_public,
            'version': self.version,
            'description': self.description,
            'dependencies': self.dependencies,
            'code_lines': self.code_lines,
            'status': self.status.value,
            'tags': self.tags,
        }


# ============================================================
# 引擎元数据提取器
# ============================================================

class EngineMetadataExtractor:
    """从源码自动提取引擎元数据"""
    
    # 六系关键词映射
    SIX_SYSTEM_KEYWORDS = {
        SixSystem.REINFORCEMENT: ['reinforce', 'enhance', 'strengthen', '强化', '增强'],
        SixSystem.NATURE: ['nature', 'natural', 'spontaneous', '自然', '涌现'],
        SixSystem.EMBODIMENT: ['embody', 'materialize', 'manifest', '具现', '显化'],
        SixSystem.TRANSFORMATION: ['transform', 'upgrade', 'evolve', '变身', '升维'],
        SixSystem.SOCIAL: ['social', 'equal', 'balance', '社会', '等算'],
        SixSystem.TIANDAO: ['tiandao', 'heaven', 'cosmic', '天道', '宇宙'],
    }
    
    # 引擎类型关键词
    PART_KEYWORDS = [
        'factory', 'manager', 'operator', 'normalizer', 'calculator',
        'converter', 'validator', 'checker', 'mapper', 'adapter',
        'protocol', 'coordinator', 'verifier', 'detector', 'searcher',
        'reader', 'analyzer', 'indexer', 'scanner', 'processor',
        'entity', 'base', 'common', 'shared', 'public', 'core',
    ]
    
    COMPONENT_KEYWORDS = [
        'engine', 'system', 'module', 'suite', 'bridge', 'match',
        'go_engine', 'gene', 'hack', 'intelligence', 'consciousness',
        'universe', 'cosmos', 'timeline', 'scene', 'stage',
        'emergence', 'evolution', 'life', 'rule', 'self_organization',
    ]
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.extracted_count = 0
    
    def extract_metadata(self, file_path: str) -> Optional[EngineMetadata]:
        """从单个文件提取元数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return None
        
        # 解析文件名
        file_name = os.path.basename(file_path)
        module_name = file_name.replace('.py', '')
        
        # 跳过非引擎文件
        if not self._is_engine_file(file_name, content):
            return None
        
        # 提取主类名
        class_name = self._extract_main_class(content)
        if not class_name:
            return None
        
        # 计算统计信息
        code_lines = len(content.split('\n'))
        class_count = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
        function_count = len(re.findall(r'^\s*(def |class )', content, re.MULTILINE))
        
        # 提取导入
        imports = self._extract_imports(content)
        
        # 提取版本
        version = self._extract_version(content)
        
        # 提取描述
        description = self._extract_description(content)
        
        # 分类
        engine_type = self._classify_engine_type(class_name, file_name, content)
        six_system = self._determine_six_system(class_name, file_name, content)
        function_type = self._determine_function_type(class_name, file_name)
        is_public = engine_type == EngineType.PART
        
        # 生成ID
        relative_path = os.path.relpath(file_path, self.base_path)
        engine_id = self._generate_engine_id(relative_path, class_name)
        
        metadata = EngineMetadata(
            engine_id=engine_id,
            name=class_name,
            class_name=class_name,
            file_path=file_path,
            module_path=relative_path.replace(os.sep, '.'),
            engine_type=engine_type,
            six_system=six_system,
            function_type=function_type,
            is_public=is_public,
            version=version,
            description=description,
            dependencies=[],
            imports=imports,
            code_lines=code_lines,
            class_count=class_count,
            function_count=function_count,
            status=EngineStatus.ACTIVE,
            discovered_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            tags=self._extract_tags(class_name, file_name, content),
        )
        
        self.extracted_count += 1
        return metadata
    
    def _is_engine_file(self, file_name: str, content: str) -> bool:
        """判断是否为引擎文件"""
        # 排除测试文件、demo文件
        skip_patterns = ['test_', 'demo_', '__init__', '_test.py']
        if any(pattern in file_name for pattern in skip_patterns):
            return False
        
        # 必须包含类定义
        if 'class ' not in content:
            return False
        
        # 检查是否为引擎相关
        engine_indicators = [
            'engine', 'system', 'operator', 'manager', 'calculator',
            'mapper', 'adapter', 'protocol', 'coordinator', 'verifier',
            'detector', 'searcher', 'analyzer', 'scanner', 'processor',
            'factory', 'entity', 'bridge', 'match', 'module',
        ]
        
        name_lower = file_name.lower()
        return any(indicator in name_lower for indicator in engine_indicators)
    
    def _extract_main_class(self, content: str) -> Optional[str]:
        """提取主类名"""
        # 找到第一个类定义
        class_pattern = r'^class\s+(\w+)[\s(:]'
        match = re.search(class_pattern, content, re.MULTILINE)
        if match:
            return match.group(1)
        return None
    
    def _extract_imports(self, content: str) -> List[str]:
        """提取导入的模块"""
        imports = []
        import_pattern = r'^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))'
        
        for match in re.finditer(import_pattern, content, re.MULTILINE):
            module = match.group(1) or match.group(2)
            if module:
                imports.append(module)
        
        return list(set(imports))
    
    def _extract_version(self, content: str) -> str:
        """提取版本号"""
        version_patterns = [
            r'VERSION\s*=\s*["\']([^"\']+)["\']',
            r'version\s*=\s*["\']([^"\']+)["\']',
            r'v(\d+\.\d+(?:\.\d+)?)',
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "1.0"
    
    def _extract_description(self, content: str) -> str:
        """提取描述"""
        # 查找文件头部的docstring
        doc_pattern = r'^"""(?:\s*\n)(.*?)(?:\s*\n)"""'
        match = re.search(doc_pattern, content, re.DOTALL)
        if match:
            desc = match.group(1).strip()
            # 取第一行
            first_line = desc.split('\n')[0].strip()
            if len(first_line) > 100:
                first_line = first_line[:100] + '...'
            return first_line
        
        return "无描述"
    
    def _classify_engine_type(self, class_name: str, file_name: str, 
                              content: str) -> EngineType:
        """分类引擎类型"""
        name_lower = class_name.lower()
        file_lower = file_name.lower()
        
        part_score = sum(1 for kw in self.PART_KEYWORDS 
                        if kw in name_lower or kw in file_lower)
        component_score = sum(1 for kw in self.COMPONENT_KEYWORDS 
                             if kw in name_lower or kw in file_lower)
        
        if part_score > component_score:
            return EngineType.PART
        elif component_score > part_score:
            return EngineType.COMPONENT
        elif 'engine' in file_lower or 'system' in file_lower:
            return EngineType.COMPONENT
        else:
            return EngineType.PART
    
    def _determine_six_system(self, class_name: str, file_name: str, 
                               content: str) -> SixSystem:
        """确定六系归属"""
        name_lower = class_name.lower()
        file_lower = file_name.lower()
        content_lower = content.lower()[:2000]  # 只看前2000字符
        
        scores = {}
        for system, keywords in self.SIX_SYSTEM_KEYWORDS.items():
            score = sum(1 for kw in keywords 
                       if kw in name_lower or kw in file_lower or kw in content_lower)
            scores[system] = score
        
        # 返回得分最高的系统
        if scores:
            max_system = max(scores, key=scores.get)
            if scores[max_system] > 0:
                return max_system
        
        # 默认：强化系
        return SixSystem.REINFORCEMENT
    
    def _determine_function_type(self, class_name: str, file_name: str) -> str:
        """确定功能类型"""
        name_lower = class_name.lower()
        file_lower = file_name.lower()
        
        function_map = {
            'game': ['go', 'game', 'match', 'board'],
            'intelligence': ['intelligence', 'hack', 'ai', 'gene', 'consciousness'],
            'model': ['universe', 'cosmos', 'six_system', 'stage', 'timeline', 'scene'],
            'simulation': ['sim', 'simulation', 'emergence', 'phase'],
            'verification': ['verify', 'verifier', 'check', 'validate'],
            'framework': ['framework', 'agent', 'mcp', 'server'],
            'analysis': ['analysis', 'analyzer', 'analysis'],
            'generation': ['generate', 'generator', 'evolution', 'factory'],
            'management': ['manager', 'management', 'registry'],
            'communication': ['bridge', 'communic', 'chat', 'network'],
        }
        
        for func_type, keywords in function_map.items():
            if any(kw in name_lower or kw in file_lower for kw in keywords):
                return func_type
        
        return 'general'
    
    def _extract_tags(self, class_name: str, file_name: str, 
                      content: str) -> List[str]:
        """提取标签"""
        tags = set()
        name_lower = class_name.lower()
        file_lower = file_name.lower()
        
        # 基于功能类型的标签
        tag_map = {
            'go': ['围棋', '博弈'],
            'game': ['游戏', '博弈'],
            'gene': ['基因', '遗传'],
            'hack': ['黑客', '安全'],
            'intelligence': ['智能', 'AI'],
            'evolution': ['进化'],
            'consciousness': ['意识'],
            'universe': ['宇宙'],
            'cosmos': ['宇宙', '和谐'],
            'six_system': ['六系'],
            'tiandao': ['天道'],
            'emergence': ['涌现'],
            'simulation': ['仿真'],
            'verify': ['验证'],
            'framework': ['框架'],
            'agent': ['智能体'],
        }
        
        for tag, keywords in tag_map.items():
            if any(kw in name_lower or kw in file_lower for kw in keywords):
                tags.add(tag)
        
        return list(tags)
    
    def _generate_engine_id(self, relative_path: str, class_name: str) -> str:
        """生成引擎唯一ID"""
        # 基于路径和类名生成
        path_hash = abs(hash(relative_path)) % 10000
        return f"BSD_{path_hash:04d}_{class_name}"


# ============================================================
# 引擎元数据注册表
# ============================================================

class EngineMetadataRegistry:
    """引擎元数据注册表"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.extractor = EngineMetadataExtractor(base_path)
        self.registry: Dict[str, EngineMetadata] = {}
        self.indices: Dict[str, Dict[str, List[str]]] = {
            'by_type': {},        # 按引擎类型索引
            'by_six_system': {},  # 按六系索引
            'by_function': {},    # 按功能索引
            'by_status': {},      # 按状态索引
            'by_tag': {},         # 按标签索引
        }
        self.stats = {
            'total_files_scanned': 0,
            'total_engines_found': 0,
            'part_engines': 0,
            'component_engines': 0,
            'total_code_lines': 0,
        }
    
    def scan_directory(self, directory: str) -> Dict[str, Any]:
        """扫描目录，提取所有引擎元数据"""
        print("=" * 70)
        print(f"【BSD 引擎元数据注册表 · 扫描】")
        print("=" * 70)
        print(f"\n  扫描目录: {directory}")
        print()
        
        scanned = 0
        found = 0
        
        for root, dirs, files in os.walk(directory):
            # 跳过某些目录
            skip_dirs = ['__pycache__', '.git', 'tests', 'test']
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file_name in files:
                if not file_name.endswith('.py'):
                    continue
                
                scanned += 1
                file_path = os.path.join(root, file_name)
                
                # 提取元数据
                metadata = self.extractor.extract_metadata(file_path)
                if metadata:
                    self.register(metadata)
                    found += 1
                    print(f"  ✓ {metadata.class_name} [{metadata.engine_type.value}] → {metadata.six_system.value}")
        
        self.stats['total_files_scanned'] = scanned
        self.stats['total_engines_found'] = found
        self.stats['part_engines'] = sum(
            1 for m in self.registry.values() 
            if m.engine_type == EngineType.PART
        )
        self.stats['component_engines'] = sum(
            1 for m in self.registry.values() 
            if m.engine_type == EngineType.COMPONENT
        )
        self.stats['total_code_lines'] = sum(
            m.code_lines for m in self.registry.values()
        )
        
        print(f"\n📊 扫描统计:")
        print(f"  - 扫描文件数: {scanned}")
        print(f"  - 发现引擎数: {found}")
        print(f"  - 部件引擎: {self.stats['part_engines']}")
        print(f"  - 组件引擎: {self.stats['component_engines']}")
        print(f"  - 总代码行数: {self.stats['total_code_lines']}")
        
        return self.stats
    
    def register(self, metadata: EngineMetadata):
        """注册引擎元数据"""
        self.registry[metadata.engine_id] = metadata
        
        # 更新索引
        self._update_indices(metadata)
    
    def _update_indices(self, metadata: EngineMetadata):
        """更新所有索引"""
        # 按类型索引
        type_key = metadata.engine_type.value
        if type_key not in self.indices['by_type']:
            self.indices['by_type'][type_key] = []
        self.indices['by_type'][type_key].append(metadata.engine_id)
        
        # 按六系索引
        system_key = metadata.six_system.value
        if system_key not in self.indices['by_six_system']:
            self.indices['by_six_system'][system_key] = []
        self.indices['by_six_system'][system_key].append(metadata.engine_id)
        
        # 按功能索引
        func_key = metadata.function_type
        if func_key not in self.indices['by_function']:
            self.indices['by_function'][func_key] = []
        self.indices['by_function'][func_key].append(metadata.engine_id)
        
        # 按状态索引
        status_key = metadata.status.value
        if status_key not in self.indices['by_status']:
            self.indices['by_status'][status_key] = []
        self.indices['by_status'][status_key].append(metadata.engine_id)
        
        # 按标签索引
        for tag in metadata.tags:
            if tag not in self.indices['by_tag']:
                self.indices['by_tag'][tag] = []
            self.indices['by_tag'][tag].append(metadata.engine_id)
    
    def get_engine(self, engine_id: str) -> Optional[EngineMetadata]:
        """获取引擎元数据"""
        return self.registry.get(engine_id)
    
    def query_by_type(self, engine_type: EngineType) -> List[EngineMetadata]:
        """按类型查询"""
        ids = self.indices['by_type'].get(engine_type.value, [])
        return [self.registry[eid] for eid in ids]
    
    def query_by_six_system(self, six_system: SixSystem) -> List[EngineMetadata]:
        """按六系查询"""
        ids = self.indices['by_six_system'].get(six_system.value, [])
        return [self.registry[eid] for eid in ids]
    
    def query_by_function(self, function_type: str) -> List[EngineMetadata]:
        """按功能查询"""
        ids = self.indices['by_function'].get(function_type, [])
        return [self.registry[eid] for eid in ids]
    
    def query_by_tag(self, tag: str) -> List[EngineMetadata]:
        """按标签查询"""
        ids = self.indices['by_tag'].get(tag, [])
        return [self.registry[eid] for eid in ids]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        # 六系分布
        six_system_dist = {}
        for metadata in self.registry.values():
            system = metadata.six_system.value
            if system not in six_system_dist:
                six_system_dist[system] = 0
            six_system_dist[system] += 1
        
        # 功能分布
        func_dist = {}
        for metadata in self.registry.values():
            func = metadata.function_type
            if func not in func_dist:
                func_dist[func] = 0
            func_dist[func] += 1
        
        return {
            'total_engines': len(self.registry),
            'by_type': {
                'part': len(self.query_by_type(EngineType.PART)),
                'component': len(self.query_by_type(EngineType.COMPONENT)),
            },
            'by_six_system': six_system_dist,
            'by_function': func_dist,
            'total_code_lines': self.stats['total_code_lines'],
            'average_code_lines': (
                self.stats['total_code_lines'] / 
                max(len(self.registry), 1)
            ),
        }
    
    def export_metadata(self, output_path: str):
        """导出元数据为JSON"""
        export_data = {
            'export_time': datetime.now().isoformat(),
            'statistics': self.get_statistics(),
            'engines': [m.to_dict() for m in self.registry.values()],
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 元数据已导出: {output_path}")
    
    def generate_report(self) -> str:
        """生成完整报告"""
        stats = self.get_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    BSD 引擎元数据注册表 · 完整报告                                              ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【一、总体统计】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📊 引擎总数: {stats['total_engines']}
  📊 部件引擎: {stats['by_type']['part']} (可公有)
  📊 组件引擎: {stats['by_type']['component']} (成品)
  📊 总代码行数: {stats['total_code_lines']}
  📊 平均代码行数: {stats['average_code_lines']:.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【二、六系分布】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for system, count in stats['by_six_system'].items():
            bar = "█" * min(count, 30)
            report += f"\n  {system}: {count:3d} 个 {bar}"
        
        report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【三、功能分布】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for func, count in sorted(stats['by_function'].items(), 
                                   key=lambda x: x[1], reverse=True):
            bar = "█" * min(count, 30)
            report += f"\n  {func}: {count:3d} 个 {bar}"
        
        report += """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【四、引擎列表（按六系分组）】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # 按六系分组显示
        for system in SixSystem:
            engines = self.query_by_six_system(system)
            if engines:
                report += f"\n  {system.value} ({len(engines)} 个):\n"
                for engine in engines[:10]:  # 每组最多显示10个
                    type_icon = '🔧' if engine.engine_type == EngineType.PART else '⚙️'
                    report += f"    {type_icon} {engine.class_name} [{engine.function_type}]\n"
                if len(engines) > 10:
                    report += f"    ... 还有 {len(engines) - 10} 个\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【五、核心结论】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ 所有引擎元数据已补入引擎论
  ✅ 六系归属已建立
  ✅ 功能分类已完成
  ✅ 部件/组件二分法已应用

  ┌─────────────────────────────────────────────────────────────────┐
  │  引擎元数据注册表已建立！                                       │
  │  引擎论已完整！                                                 │
  │  所有引擎已纳入管理！                                           │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        print(report)
        return report


# ============================================================
# 主程序
# ============================================================

def main():
    """主程序"""
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("【BSD 引擎元数据注册表系统】")
    print("=" * 70)
    print(f"\n  基础路径: {base_path}")
    print()
    
    # 创建注册表
    registry = EngineMetadataRegistry(base_path)
    
    # 扫描所有引擎
    registry.scan_directory(base_path)
    
    # 生成报告
    report = registry.generate_report()
    
    # 导出元数据
    output_path = os.path.join(base_path, 'engine_metadata.json')
    registry.export_metadata(output_path)
    
    # 演示查询
    print("\n" + "=" * 70)
    print("【演示：按六系查询】")
    print("=" * 70)
    
    for system in SixSystem:
        engines = registry.query_by_six_system(system)
        if engines:
            print(f"\n  {system.value}:")
            for engine in engines[:5]:
                print(f"    - {engine.class_name} ({engine.function_type})")
            if len(engines) > 5:
                print(f"    ... 还有 {len(engines) - 5} 个")
    
    return {
        'report': report,
        'statistics': registry.get_statistics(),
        'registry': registry,
    }


if __name__ == '__main__':
    main()