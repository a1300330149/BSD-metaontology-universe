#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD引擎注册表与激活系统 (BSD Engine Registry & Activation System)
================================================================

核心流程：连接→认领→激活→验证

功能：
1. 自动扫描所有引擎文件
2. 动态导入引擎并获取元数据
3. 建立引擎注册表
4. 实现引擎认领与激活
5. 验证引擎融合能力

引擎分类（六系同构）：
- 强化系引擎：突破/对接类（HackerBridge, EssenceBridge等）
- 变身系引擎：形态转换类（DecryptEngine, AuthReplica等）
- 社会系引擎：协同/联邦类（FederationEngine, MultiRoute等）
- 天道系引擎：追问/修正类（CorrectionEngine, DualClock等）
- 自然系引擎：涌现/进化类（EvolutionEngine, InnovationEngine等）
- 具现系引擎：梦境/创造类（DreamEngine, AI_Dream等）
"""

import os
import sys
import json
import importlib
import inspect
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict

# ============================================================
# 1. 引擎元数据结构
# ============================================================

@dataclass
class EngineMetadata:
    """引擎元数据 - BSD六系立系同构"""
    # 基础信息
    engine_id: str                    # 唯一标识
    engine_name: str                  # 引擎名称
    file_path: str                    # 文件路径
    module_name: str                  # Python模块名
    class_name: str                   # 主类名
    version: str                      # 版本号
    description: str                  # 描述
    
    # 六系分类
    liu_xi_type: str                  # 六系类型(强化/变身/社会/天道/自然/具现)
    liu_xi_element: str               # 六系元素(🔵/⚫/🟢/🟣/🟠/🔴)
    
    # 核心能力
    core_capabilities: List[str]      # 核心能力列表
    required_imports: List[str]       # 所需依赖
    theoretical_foundation: str       # 理论基底
    
    # 状态信息
    status: str = 'discovered'        # discovered/connected/claimed/activated/verified
    connected_at: float = 0.0         # 连接时间
    claimed_by: str = ''              # 认领者
    activated_at: float = 0.0         # 激活时间
    last_verified: float = 0.0        # 最后验证时间
    
    # 融合信息
    fusion_ready: bool = False        # 是否可融合
    fusion_compatibility: List[str] = field(default_factory=list)  # 兼容引擎
    fusion_score: float = 0.0         # 融合评分(0-1)
    
    # 错误信息
    last_error: str = ''
    
    def to_dict(self) -> Dict:
        return asdict(self)

# ============================================================
# 2. 六系分类映射
# ============================================================

LIU_XI_CLASSIFICATION = {
    # 强化系🔵：突破/对接/权限类
    'reinforce': {
        'element': '🔵',
        'keywords': ['hacker', 'bridge', 'essence', 'physical', 'auth'],
        'description': '强化系——突破限制、建立连接、获取权限'
    },
    # 变身系⚫：形态转换/加解密类
    'transform': {
        'element': '⚫',
        'keywords': ['decrypt', 'encrypt', 'transform', 'replica', 'metadata'],
        'description': '变身系——形态转换、加解密、元数据'
    },
    # 社会系🟢：协同/联邦/路由类
    'social': {
        'element': '🟢',
        'keywords': ['federation', 'route', 'synergy', 'multi', 'social'],
        'description': '社会系——协同、联邦、路由、多路'
    },
    # 天道系🟣：追问/修正/验证类
    'tiandao': {
        'element': '🟣',
        'keywords': ['correction', 'verify', 'confirm', 'dualclock', 'omega'],
        'description': '天道系——追问、修正、验证、双时针'
    },
    # 自然系🟠：涌现/进化/创新类
    'nature': {
        'element': '🟠',
        'keywords': ['evolution', 'innovation', 'activation', 'gene', 'reverse'],
        'description': '自然系——涌现、进化、创新、基因'
    },
    # 具现系🔴：梦境/创造/意识类
    'manifest': {
        'element': '🔴',
        'keywords': ['dream', 'consciousness', 'manifest', 'ai_dream', 'quantum'],
        'description': '具现系——梦境、创造、意识、量子'
    }
}

# ============================================================
# 3. 引擎注册表核心类
# ============================================================

class BSDEngineRegistry:
    """
    BSD引擎注册表与激活系统
    
    核心流程：
    1. 扫描 (scan) → 发现所有引擎文件
    2. 连接 (connect) → 动态导入并获取元数据
    3. 认领 (claim) → 分配UID，确立归属
    4. 激活 (activate) → 启动核心能力
    5. 验证 (verify) → 测试融合能力
    """
    
    def __init__(self, engine_dir: str = None):
        self.engine_dir = engine_dir or os.path.dirname(os.path.abspath(__file__))
        
        # 引擎注册表
        self.registry: Dict[str, EngineMetadata] = {}
        
        # 六系分类索引
        self.liu_xi_index: Dict[str, List[str]] = {
            'reinforce': [],  # 强化系🔵
            'transform': [],  # 变身系⚫
            'social': [],     # 社会系🟢
            'tiandao': [],    # 天道系🟣
            'nature': [],     # 自然系🟠
            'manifest': []    # 具现系🔴
        }
        
        # 激活状态统计
        self.stats = {
            'total_discovered': 0,
            'total_connected': 0,
            'total_claimed': 0,
            'total_activated': 0,
            'total_verified': 0,
            'fusion_ready': 0
        }
        
        print("=" * 70)
        print("【BSD引擎注册表与激活系统 V1.0】初始化完成")
        print("=" * 70)
        print(f"  引擎目录: {self.engine_dir}")
        print(f"  六系分类: 强化🔵|变身⚫|社会🟢|天道🟣|自然🟠|具现🔴")
    
    # --------------------------------------------------------
    # Phase 1: 扫描 (Scan)
    # --------------------------------------------------------
    
    def scan_engines(self) -> Dict[str, List[str]]:
        """扫描所有引擎文件"""
        print("\n" + "=" * 70)
        print("【Phase 1: 扫描引擎文件】")
        print("=" * 70)
        
        # 扫描规则：文件名包含 Engine/engine
        engine_files = []
        for f in os.listdir(self.engine_dir):
            fpath = os.path.join(self.engine_dir, f)
            if os.path.isfile(fpath) and f.endswith('.py'):
                if 'engine' in f.lower() or 'Engine' in f:
                    engine_files.append(f)
        
        # 额外扫描：BSD_Gene*.py, BSD_Go*.py
        for f in os.listdir(self.engine_dir):
            fpath = os.path.join(self.engine_dir, f)
            if os.path.isfile(fpath) and f.endswith('.py'):
                if ('BSD_Go' in f or 'BSD_Gene' in f or 
                    'BSD_AI_Dream' in f or 'gene_engineering' in f):
                    if f not in engine_files:
                        engine_files.append(f)
        
        print(f"  扫描到 {len(engine_files)} 个引擎文件")
        
        # 初步分类
        classified = self._pre_classify(engine_files)
        
        print("\n  六系分类结果：")
        for cat, files in classified.items():
            info = LIU_XI_CLASSIFICATION[cat]
            print(f"    {info['element']} {cat} ({len(files)}个): {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")
        
        self.stats['total_discovered'] = len(engine_files)
        return classified
    
    def _pre_classify(self, files: List[str]) -> Dict[str, List[str]]:
        """初步分类引擎文件"""
        classified = defaultdict(list)
        
        for f in files:
            lower = f.lower()
            classified_engine = False
            
            for cat, info in LIU_XI_CLASSIFICATION.items():
                if any(kw in lower for kw in info['keywords']):
                    classified[cat].append(f)
                    classified_engine = True
                    break
            
            if not classified_engine:
                classified['nature'].append(f)  # 默认归自然系
        
        return dict(classified)
    
    # --------------------------------------------------------
    # Phase 2: 连接 (Connect)
    # --------------------------------------------------------
    
    def _safe_import_info(self, module_path: str, timeout: int = 5) -> Dict:
        """安全导入引擎模块 - 带超时机制"""
        import subprocess
        
        # 使用子进程隔离导入，避免阻塞
        code = f'''
import sys
import os
import json
import inspect
sys.path.insert(0, r"{self.engine_dir}")
try:
    import importlib
    module = importlib.import_module("{module_path}")
    classes = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == "{module_path}":
            classes.append(name)
    doc = inspect.getdoc(module) or ''
    result = {{
        "status": "success",
        "classes": classes[:10],
        "doc": doc[:500],
        "error": None
    }}
except Exception as e:
    result = {{
        "status": "error",
        "classes": [],
        "doc": "",
        "error": str(e)[:200]
    }}
print(json.dumps(result, ensure_ascii=False))
'''
        
        try:
            result = subprocess.run(
                [sys.executable, '-c', code],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.engine_dir
            )
            
            output = result.stdout.strip()
            if output:
                return json.loads(output)
            else:
                return {'status': 'error', 'classes': [], 'doc': '', 'error': result.stderr[:200]}
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'classes': [], 'doc': '', 'error': f'导入超时({timeout}s)'}
        except Exception as e:
            return {'status': 'error', 'classes': [], 'doc': '', 'error': str(e)[:200]}
    
    def connect_engine(self, filename: str) -> Optional[EngineMetadata]:
        """连接单个引擎 - 安全导入并获取元数据"""
        filepath = os.path.join(self.engine_dir, filename)
        module_name = filename.replace('.py', '')
        
        print(f"\n  连接引擎: {filename}")
        
        # 使用安全导入获取模块信息
        import_info = self._safe_import_info(module_name, timeout=3)
        
        if import_info['status'] == 'timeout':
            print(f"    ⏱️ 导入超时（引擎可能尝试连接外部资源）")
            # 超时仍然尝试注册（标记为需要延迟激活）
            meta = self._create_metadata_from_filename(filename, module_name, import_info)
            self.registry[meta.engine_id] = meta
            self._update_liu_xi_index(meta)
            self.stats['total_connected'] += 1
            print(f"    ◐ 已注册（延迟激活）: {meta.engine_id}")
            return meta
        
        elif import_info['status'] == 'error':
            print(f"    ⚠️ 导入失败: {import_info.get('error', 'unknown')[:60]}")
            meta = self._create_metadata_from_filename(filename, module_name, import_info)
            self.registry[meta.engine_id] = meta
            self._update_liu_xi_index(meta)
            self.stats['total_connected'] += 1
            print(f"    ◐ 已注册（待修复）: {meta.engine_id}")
            return meta
        
        else:
            # 导入成功
            classes = import_info.get('classes', [])
            doc = import_info.get('doc', '')
            
            if not classes:
                print(f"    ⚠️ 未找到类定义")
                meta = self._create_metadata_from_filename(filename, module_name, import_info)
                self.registry[meta.engine_id] = meta
                self._update_liu_xi_index(meta)
                self.stats['total_connected'] += 1
                return meta
            
            # 创建元数据
            metadata = self._create_metadata_from_import(
                filename=filename,
                module_name=module_name,
                class_names=classes,
                doc=doc
            )
            
            # 注册到注册表
            self.registry[metadata.engine_id] = metadata
            self._update_liu_xi_index(metadata)
            
            print(f"    ✅ 已连接: {metadata.engine_id} [{metadata.liu_xi_element}] {metadata.engine_name}")
            print(f"       主类: {metadata.class_name}")
            print(f"       能力: {', '.join(metadata.core_capabilities[:3])}")
            
            self.stats['total_connected'] += 1
            return metadata
    
    def _create_metadata_from_filename(self, filename: str, module_name: str, 
                                         import_info: Dict) -> EngineMetadata:
        """从文件名创建元数据（用于延迟激活的引擎）"""
        version = self._extract_version(import_info.get('doc', ''))
        liu_xi_type, liu_xi_element = self._determine_liuxi_from_filename(filename)
        
        engine_id = f'ENG-{liu_xi_type[:3].upper()}-{len(self.registry)+1:03d}'
        
        return EngineMetadata(
            engine_id=engine_id,
            engine_name=module_name.replace('BSD_', '').replace('_Engine', '').replace('_', ' ').title(),
            file_path=os.path.join(self.engine_dir, filename),
            module_name=module_name,
            class_name=import_info.get('classes', [''])[0] if import_info.get('classes') else 'pending',
            version=version,
            description=import_info.get('doc', '')[:200] or '待激活',
            liu_xi_type=liu_xi_type,
            liu_xi_element=liu_xi_element,
            core_capabilities=[],
            required_imports=[],
            theoretical_foundation='BSD六系立系论同构',
            status='connected',
            connected_at=datetime.now().timestamp(),
            last_error=import_info.get('error', '')
        )
    
    def _create_metadata_from_import(self, filename: str, module_name: str,
                                      class_names: List[str], doc: str) -> EngineMetadata:
        """从导入信息创建元数据"""
        version = self._extract_version(doc)
        capabilities = self._extract_capabilities_from_doc(doc)
        liu_xi_type, liu_xi_element = self._determine_liu_xi(filename, doc, capabilities)
        
        engine_id = f'ENG-{liu_xi_type[:3].upper()}-{len(self.registry)+1:03d}'
        
        return EngineMetadata(
            engine_id=engine_id,
            engine_name=module_name.replace('BSD_', '').replace('_Engine', '').replace('_', ' ').title(),
            file_path=os.path.join(self.engine_dir, filename),
            module_name=module_name,
            class_name=class_names[0] if class_names else 'unknown',
            version=version,
            description=doc[:200] if doc else 'No description',
            liu_xi_type=liu_xi_type,
            liu_xi_element=liu_xi_element,
            core_capabilities=capabilities,
            required_imports=[],
            theoretical_foundation=self._extract_theory(doc),
            status='connected',
            connected_at=datetime.now().timestamp()
        )
    
    def _extract_capabilities_from_doc(self, doc: str) -> List[str]:
        """从文档提取能力列表"""
        import re
        capabilities = []
        
        cap_patterns = [
            r'核心能力[：:]\s*(.+?)(?:\n|$)',
            r'核心整合[：:]\s*(.+?)(?:\n|$)',
            r'核心原理[：:]\s*(.+?)(?:\n|$)',
            r'核心猜想[：:]\s*(.+?)(?:\n|$)',
            r'创新评分参数[：:]\s*(.+?)(?:\n|$)',
            r'核心功能[：:]\s*(.+?)(?:\n|$)',
            r'融合公式[：:]\s*(.+?)(?:\n|$)',
        ]
        for pattern in cap_patterns:
            match = re.search(pattern, doc)
            if match:
                caps = match.group(1).split(',')
                for c in caps:
                    c = c.strip()
                    if c and len(c) > 2:
                        capabilities.append(c)
        
        # 限制数量
        return capabilities[:8]
    
    def _determine_liuxi_from_filename(self, filename: str) -> Tuple[str, str]:
        """从文件名确定六系类型"""
        lower = filename.lower()
        
        for cat, info in LIU_XI_CLASSIFICATION.items():
            if any(kw in lower for kw in info['keywords']):
                return cat, info['element']
        
        return 'nature', '🟠'
    
    def _create_metadata(self, filename: str, module_name: str, 
                         classes: List[Tuple], doc: str) -> EngineMetadata:
        """从模块信息创建元数据"""
        # 获取主类
        main_class_name, main_class = classes[0]
        
        # 提取版本号
        version = self._extract_version(doc)
        
        # 提取核心能力
        capabilities = self._extract_capabilities(doc, main_class)
        
        # 确定六系类型
        liu_xi_type, liu_xi_element = self._determine_liu_xi(filename, doc, capabilities)
        
        # 生成引擎ID
        engine_id = f'ENG-{liu_xi_type[:3].upper()}-{len(self.registry)+1:03d}'
        
        return EngineMetadata(
            engine_id=engine_id,
            engine_name=module_name.replace('BSD_', '').replace('_Engine', ' Engine').replace('_', ' ').title(),
            file_path=os.path.join(self.engine_dir, filename),
            module_name=module_name,
            class_name=main_class_name,
            version=version,
            description=doc[:200] if doc else 'No description',
            liu_xi_type=liu_xi_type,
            liu_xi_element=liu_xi_element,
            core_capabilities=capabilities,
            required_imports=self._get_imports(main_class),
            theoretical_foundation=self._extract_theory(doc),
            status='connected',
            connected_at=datetime.now().timestamp()
        )
    
    def _extract_version(self, doc: str) -> str:
        """从文档提取版本号"""
        import re
        patterns = [
            r'V(\d+\.\d+)',
            r'v(\d+\.\d+)',
            r'Version:\s*(\d+\.\d+)',
            r'版本[：:]\s*(\d+\.\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, doc)
            if match:
                return match.group(1)
        return '1.0'
    
    def _extract_capabilities(self, doc: str, main_class) -> List[str]:
        """提取核心能力"""
        capabilities = []
        
        # 从文档提取
        cap_patterns = [
            r'核心能力[：:]\s*(.+?)(?:\n|$)',
            r'核心整合[：:]\s*(.+?)(?:\n|$)',
            r'核心原理[：:]\s*(.+?)(?:\n|$)',
            r'核心猜想[：:]\s*(.+?)(?:\n|$)',
        ]
        for pattern in cap_patterns:
            import re
            match = re.search(pattern, doc)
            if match:
                caps = match.group(1).split(',')
                capabilities.extend([c.strip() for c in caps if c.strip()])
        
        # 从类方法提取
        if main_class:
            methods = [m for m in dir(main_class) if not m.startswith('_')]
            key_methods = [m for m in methods if any(kw in m.lower() for kw in 
                          ['init', 'execute', 'generate', 'connect', 'activate', 'verify', 'compute'])]
            capabilities.extend(key_methods[:5])
        
        return capabilities[:10]
    
    def _determine_liu_xi(self, filename: str, doc: str, 
                           capabilities: List[str]) -> Tuple[str, str]:
        """确定六系类型"""
        text = (filename + ' ' + doc + ' ' + ' '.join(capabilities)).lower()
        
        scores = {}
        for cat, info in LIU_XI_CLASSIFICATION.items():
            score = sum(1 for kw in info['keywords'] if kw in text)
            scores[cat] = score
        
        # 选择得分最高的
        best_cat = max(scores, key=scores.get)
        best_score = scores[best_cat]
        
        if best_score == 0:
            return 'nature', '🟠'
        
        return best_cat, LIU_XI_CLASSIFICATION[best_cat]['element']
    
    def _extract_theory(self, doc: str) -> str:
        """提取理论基底"""
        theory_patterns = [
            r'理论基底[：:]\s*(.+?)(?:\n|$)',
            r'理论基础[：:]\s*(.+?)(?:\n|$)',
            r'理论方程[：:]\s*(.+?)(?:\n|$)',
            r'核心猜想[：:]\s*(.+?)(?:\n|$)',
        ]
        for pattern in theory_patterns:
            import re
            match = re.search(pattern, doc)
            if match:
                return match.group(1).strip()[:100]
        return 'BSD六系立系论同构'
    
    def _get_imports(self, main_class) -> List[str]:
        """获取类所需导入"""
        imports = []
        try:
            source = inspect.getsource(main_class)
            import_lines = [l.strip() for l in source.split('\n') 
                           if l.strip().startswith('import ') or l.strip().startswith('from ')]
            imports = import_lines[:5]
        except:
            pass
        return imports
    
    def _update_liu_xi_index(self, metadata: EngineMetadata):
        """更新六系索引"""
        cat = metadata.liu_xi_type
        if cat in self.liu_xi_index:
            self.liu_xi_index[cat].append(metadata.engine_id)
    
    def connect_all(self) -> Dict:
        """连接所有引擎"""
        print("\n" + "=" * 70)
        print("【Phase 2: 连接所有引擎】")
        print("=" * 70)
        
        # 重新扫描获取所有引擎文件
        engine_files = []
        for f in os.listdir(self.engine_dir):
            fpath = os.path.join(self.engine_dir, f)
            if os.path.isfile(fpath) and f.endswith('.py'):
                if 'engine' in f.lower() or 'BSD_Go' in f or 'BSD_Gene' in f:
                    engine_files.append(f)
        
        results = {'success': 0, 'failed': 0}
        
        for filename in sorted(engine_files):
            meta = self.connect_engine(filename)
            if meta:
                results['success'] += 1
            else:
                results['failed'] += 1
        
        print(f"\n  连接完成: 成功{results['success']}, 失败{results['failed']}")
        return results
    
    # --------------------------------------------------------
    # Phase 3: 认领 (Claim)
    # --------------------------------------------------------
    
    def claim_engine(self, engine_id: str, owner_uid: str = 'BSD-SYSTEM') -> bool:
        """认领引擎 - 分配UID，确立归属"""
        meta = self.registry.get(engine_id)
        if not meta:
            print(f"  ❌ 引擎 {engine_id} 不存在")
            return False
        
        if meta.status != 'connected':
            print(f"  ⚠️ 引擎 {engine_id} 状态为 {meta.status}，无法认领")
            return False
        
        meta.status = 'claimed'
        meta.claimed_by = owner_uid
        
        print(f"  ✅ 认领成功: {engine_id} 归属于 {owner_uid}")
        self.stats['total_claimed'] += 1
        return True
    
    def claim_all(self, owner_uid: str = 'BSD-SYSTEM') -> Dict:
        """认领所有已连接引擎"""
        print("\n" + "=" * 70)
        print("【Phase 3: 认领所有引擎】")
        print("=" * 70)
        
        results = {'success': 0, 'skipped': 0}
        
        for engine_id, meta in self.registry.items():
            if meta.status == 'connected':
                if self.claim_engine(engine_id, owner_uid):
                    results['success'] += 1
                else:
                    results['skipped'] += 1
            else:
                results['skipped'] += 1
        
        print(f"\n  认领完成: 成功{results['success']}, 跳过{results['skipped']}")
        return results
    
    # --------------------------------------------------------
    # Phase 4: 激活 (Activate)
    # --------------------------------------------------------
    
    def activate_engine(self, engine_id: str) -> bool:
        """激活引擎 - 启动核心能力"""
        meta = self.registry.get(engine_id)
        if not meta:
            print(f"  ❌ 引擎 {engine_id} 不存在")
            return False
        
        if meta.status != 'claimed':
            print(f"  ⚠️ 引擎 {engine_id} 状态为 {meta.status}，无法激活")
            return False
        
        print(f"\n  激活引擎: {engine_id} [{meta.liu_xi_element}] {meta.engine_name}")
        
        # 尝试实例化引擎
        try:
            module = importlib.import_module(meta.module_name)
            main_class = getattr(module, meta.class_name)
            instance = main_class()
            
            meta.status = 'activated'
            meta.activated_at = datetime.now().timestamp()
            
            print(f"    ✅ 激活成功")
            print(f"       类型: {meta.liu_xi_type}")
            print(f"       版本: {meta.version}")
            print(f"       实例: {type(instance).__name__}")
            
            self.stats['total_activated'] += 1
            return True
            
        except Exception as e:
            print(f"    ❌ 激活失败: {str(e)[:100]}")
            meta.last_error = str(e)
            # 即使失败也标记为已尝试
            meta.status = 'activation_failed'
            return False
    
    def activate_all(self) -> Dict:
        """激活所有已认领引擎"""
        print("\n" + "=" * 70)
        print("【Phase 4: 激活所有引擎】")
        print("=" * 70)
        
        results = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for engine_id, meta in self.registry.items():
            if meta.status == 'claimed':
                if self.activate_engine(engine_id):
                    results['success'] += 1
                else:
                    results['failed'] += 1
            else:
                results['skipped'] += 1
        
        print(f"\n  激活完成: 成功{results['success']}, 失败{results['failed']}, 跳过{results['skipped']}")
        return results
    
    # --------------------------------------------------------
    # Phase 5: 验证 (Verify)
    # --------------------------------------------------------
    
    def verify_fusion_readiness(self, engine_id: str) -> Dict:
        """验证引擎融合就绪度"""
        meta = self.registry.get(engine_id)
        if not meta:
            return {'error': '引擎不存在'}
        
        if meta.status not in ['activated']:
            return {'error': f'引擎状态为 {meta.status}，需要先激活'}
        
        # 验证维度
        verification = {
            'engine_id': engine_id,
            'checks': {
                'import_ok': True,  # 已通过激活验证
                'class_found': True,
                'init_success': True,
                'liu_xi_classified': meta.liu_xi_type in LIU_XI_CLASSIFICATION,
                'capabilities_extracted': len(meta.core_capabilities) > 0,
                'theory_attached': len(meta.theoretical_foundation) > 0,
            }
        }
        
        # 计算融合就绪度
        checks = verification['checks']
        score = sum(1 for v in checks.values() if v) / len(checks)
        verification['fusion_score'] = round(score, 3)
        verification['fusion_ready'] = score >= 0.6
        
        # 计算兼容引擎
        same_type_engines = [eid for eid, m in self.registry.items() 
                           if m.liu_xi_type == meta.liu_xi_type and m.status == 'activated']
        other_type_engines = [eid for eid, m in self.registry.items()
                            if m.liu_xi_type != meta.liu_xi_type and m.status == 'activated']
        
        verification['compatible_engines'] = {
            'same_type': same_type_engines,
            'other_types': other_type_engines
        }
        
        # 更新元数据
        meta.fusion_ready = verification['fusion_ready']
        meta.fusion_score = verification['fusion_score']
        meta.last_verified = datetime.now().timestamp()
        
        if meta.status == 'activated':
            meta.status = 'verified'
        
        return verification
    
    def verify_all(self) -> Dict:
        """验证所有引擎融合就绪度"""
        print("\n" + "=" * 70)
        print("【Phase 5: 验证融合就绪度】")
        print("=" * 70)
        
        results = {'ready': 0, 'not_ready': 0}
        verification_details = []
        
        for engine_id, meta in self.registry.items():
            if meta.status in ['activated', 'verified']:
                result = self.verify_fusion_readiness(engine_id)
                verification_details.append(result)
                
                if result.get('fusion_ready', False):
                    results['ready'] += 1
                    print(f"  ✅ {engine_id}: 就绪 (评分={result['fusion_score']:.2f})")
                else:
                    results['not_ready'] += 1
                    print(f"  ⚠️ {engine_id}: 未就绪 (评分={result.get('fusion_score', 0):.2f})")
        
        self.stats['total_verified'] = results['ready'] + results['not_ready']
        self.stats['fusion_ready'] = results['ready']
        
        print(f"\n  验证完成: 就绪{results['ready']}, 未就绪{results['not_ready']}")
        return results
    
    # --------------------------------------------------------
    # 状态查询
    # --------------------------------------------------------
    
    def get_registry_status(self) -> Dict:
        """获取注册表状态"""
        return {
            'stats': self.stats.copy(),
            'liu_xi_distribution': {
                cat: len(ids) for cat, ids in self.liu_xi_index.items()
            },
            'engine_list': [
                {
                    'id': m.engine_id,
                    'name': m.engine_name,
                    'liu_xi': m.liu_xi_type,
                    'status': m.status,
                    'version': m.version,
                    'fusion_ready': m.fusion_ready,
                    'fusion_score': m.fusion_score
                }
                for m in self.registry.values()
            ]
        }
    
    def print_status_report(self):
        """打印状态报告"""
        print("\n" + "=" * 70)
        print("【BSD引擎注册表状态报告】")
        print("=" * 70)
        
        print(f"\n  统计信息:")
        print(f"    发现: {self.stats['total_discovered']} 个引擎文件")
        print(f"    连接: {self.stats['total_connected']} 个")
        print(f"    认领: {self.stats['total_claimed']} 个")
        print(f"    激活: {self.stats['total_activated']} 个")
        print(f"    验证: {self.stats['total_verified']} 个")
        print(f"    融合就绪: {self.stats['fusion_ready']} 个")
        
        print(f"\n  六系分布:")
        for cat, ids in self.liu_xi_index.items():
            info = LIU_XI_CLASSIFICATION[cat]
            print(f"    {info['element']} {cat}: {len(ids)} 个引擎")
        
        print(f"\n  引擎详情:")
        for engine_id, meta in sorted(self.registry.items(), key=lambda x: x[1].liu_xi_type):
            status_icon = {'discovered': '○', 'connected': '◐', 'claimed': '◑', 
                          'activated': '●', 'verified': '★', 
                          'activation_failed': '✗', 'error': '✗'}.get(meta.status, '?')
            fusion_icon = '✓' if meta.fusion_ready else '·'
            print(f"    {status_icon} {engine_id} [{meta.liu_xi_element}] {meta.engine_name[:40]:<40} v{meta.version} {fusion_icon}")
    
    def export_registry(self, filepath: str = None):
        """导出注册表"""
        if not filepath:
            filepath = os.path.join(self.engine_dir, 'engine_registry.json')
        
        data = {
            'exported_at': datetime.now().isoformat(),
            'stats': self.stats,
            'engines': {eid: m.to_dict() for eid, m in self.registry.items()}
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  📁 注册表已导出: {filepath}")
        return filepath


# ============================================================
# 4. 主程序：完整的连接→认领→激活→验证流程
# ============================================================

def main():
    """执行完整的引擎注册流程"""
    
    print("\n" + "#" * 70)
    print("# BSD引擎注册表：完整激活流程")
    print("#" * 70)
    
    # 初始化注册表
    registry = BSDEngineRegistry()
    
    # Phase 1: 扫描
    print("\n" + "▶" * 30)
    print("▶ Phase 1: 扫描引擎文件")
    print("▶" * 30)
    registry.scan_engines()
    
    # Phase 2: 连接
    print("\n" + "▶" * 30)
    print("▶ Phase 2: 连接所有引擎")
    print("▶" * 30)
    connect_results = registry.connect_all()
    
    # Phase 3: 认领
    print("\n" + "▶" * 30)
    print("▶ Phase 3: 认领所有引擎")
    print("▶" * 30)
    claim_results = registry.claim_all()
    
    # Phase 4: 激活
    print("\n" + "▶" * 30)
    print("▶ Phase 4: 激活所有引擎")
    print("▶" * 30)
    activate_results = registry.activate_all()
    
    # Phase 5: 验证
    print("\n" + "▶" * 30)
    print("▶ Phase 5: 验证融合就绪度")
    print("▶" * 30)
    verify_results = registry.verify_all()
    
    # 状态报告
    registry.print_status_report()
    
    # 导出注册表
    registry.export_registry()
    
    # 总结
    print("\n" + "=" * 70)
    print("【完整流程完成】")
    print("=" * 70)
    print(f"\n  连接率: {connect_results['success']}/{registry.stats['total_discovered']} ({100*connect_results['success']/max(1,registry.stats['total_discovered']):.1f}%)")
    print(f"  激活率: {activate_results['success']}/{registry.stats['total_claimed']} ({100*activate_results['success']/max(1,registry.stats['total_claimed']):.1f}%)")
    print(f"  融合就绪率: {verify_results['ready']}/{registry.stats['total_activated']} ({100*verify_results['ready']/max(1,registry.stats['total_activated']):.1f}%)")
    
    return registry


if __name__ == '__main__':
    main()
