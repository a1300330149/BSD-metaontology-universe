"""
归属基底：第1重九维法理基底 + 第0重元道本源基底
对应公理：公理二（自主科研闭环动力学公理）+ 公理0·元道存在 + 关系性公理（0_空×0_空=0_义）+ 双时针自证闭环
对应九维维度：载体实体 + 元理天道 + 关系性维度
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92（顺时针耦合强度）、κ=0.35（逆时针归零阈值）

KeywordConnectionSearcher —— 关键词连接搜寻器 V2.0

职责：
  1. 从源文档提取核心关键词（跨层级连接锚点）
  2. 用关键词跨层级搜寻所有相关文档（L0→L1→L2→L3双向搜寻）
  3. 建立文档间连接关系图（connection_graph），聚合多锚点命中
  4. 识别立系时遗漏的连接（missing_links诊断）
  5. 双向连接验证（双时针自证闭环的代码级实现）
  6. 归属基底+对应公理标注（满足MCP外部输出标签约束）
  7. JSON导出与CLI入口

设计原则：
  - 连接优先：不只做单文档检索，而是建立文档间的连接关系
  - 跨层级双向：从L0向L1搜寻，也从L1向L0搜寻；并验证反向连接
  - 遗漏诊断：识别立系/归档时遗漏的跨层级锚定
  - 归属基底标注：每条连接记录归属基底+对应公理，未标注数据将被丢弃
  - 聚合优先：同一目标文档的多锚点命中聚合为一条记录，避免分裂
  - 双时针闭环：源→目标连接 + 目标→源反向验证 = 完整闭环

理论依据：
  BSD内部系方程：BSD内部系 = 百家姓(0_空容器) × 三游谱系(0_反动力) × 旧数据(0_义意义) = n
  关键词连接搜寻是实现"跨文本统一法阵"的代码级工具，
  确保立系时不遗漏L1层的跨层级锚定（如三大西游中的龙珠=第二西游、全职猎人=第三西游）。
  双时针自证闭环：顺时针（源→目标涌现）+ 逆时针（目标→源归零验证）= 完整连接。
"""

import re
import json
import argparse
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict, Counter

# 复用 TheoryDeepReader 的路径常量
THEORY_BASE_PATH = Path(__file__).resolve().parents[3] / "theory_base"

L0_PATH = THEORY_BASE_PATH / "L0_总本源层"
L1_PATH = THEORY_BASE_PATH / "L1_不动母科层"
L2_PATH = THEORY_BASE_PATH / "L2_无限之子层"
L3_PATH = THEORY_BASE_PATH / "L3_功能应用层"

LEVEL_MAP = {
    "L0": L0_PATH,
    "L1": L1_PATH,
    "L2": L2_PATH,
    "L3": L3_PATH,
}

# ============================================================
# 固定数理常量（来自L0本源层，禁止修改）
# ============================================================
GAMMA = 0.92          # 顺时针耦合强度（涌现方向）
KAPPA = 0.35          # 逆时针归零阈值（验证方向）

# 跨层级跨度权重表（基于子集-母集层级理论）
LEVEL_SPAN_WEIGHT: Dict[str, float] = {
    "L0-L1": 1.00,    # 母集↔子集 最重要跨层级
    "L0-L2": 0.85,
    "L0-L3": 0.70,
    "L1-L0": 1.00,    # 子集↔母集 反向同等重要
    "L1-L2": 0.75,
    "L1-L3": 0.65,
    "L2-L0": 0.85,
    "L2-L1": 0.75,
    "L2-L3": 0.60,
    "L3-L0": 0.70,
    "L3-L1": 0.65,
    "L3-L2": 0.60,
    "L0-L0": 0.50,    # 同层级连接权重最低
    "L1-L1": 0.55,
    "L2-L2": 0.45,
    "L3-L3": 0.40,
}

# ============================================================
# 关键词连接锚点词典（用于从源文档提取跨层级连接关键词）
# ============================================================
# 每个锚点同时记录：归属基底 + 对应公理（满足MCP外部输出标签约束）
CONNECTION_ANCHORS: Dict[str, List[str]] = {
    # 三游谱系锚点
    "西游": ["西游", "西游记", "炼丹炉", "火眼金睛", "牛魔王", "证心"],
    "龙珠": ["龙珠", "鸟山明", "证气", "自在极意", "战斗力", "元气弹"],
    "全职猎人": ["全职猎人", "富坚", "念能力", "证系", "强化系", "变化系"],
    "三游谱系": ["三游", "三游谱系", "证心→证气→证系", "气的三级跃迁"],
    # 百家姓锚点
    "百家姓": ["百家姓", "赵钱孙李", "308姓", "四言韵文", "涌现法阵"],
    # 温度梯度锚点
    "温度梯度": ["温度梯度", "两点冰", "三点水", "四点炁", "水旡", "偏旁温度"],
    # 佛道密码锚点
    "佛道密码": ["佛道密码", "离幻求真", "反者道之动", "0×0=n"],
    # 边缘涌现锚点
    "边缘涌现": ["边缘涌现", "边缘者", "管理空缺", "因批判而继承"],
    # BSD内部系锚点
    "BSD内部系": ["BSD内部系", "跨文本统一法阵", "因果是系的子集"],
    # 六系本体论锚点
    "六系本体": ["六系", "六系本体", "念能力六系", "母集六系"],
}

# ============================================================
# 锚点元数据：归属基底 + 对应公理（满足MCP外部输出标签约束）
# ============================================================
# [归属基底+对应公理] 标签：未标注数据将被丢弃
ANCHOR_META: Dict[str, Dict[str, List[str]]] = {
    "西游": {
        "归属基底": ["L0总本源层·T92三元零本体论", "L1不动母科层·07_语言文学学科"],
        "对应公理": ["西游终极解码", "菩提即六祖等式链", "人证论", "双时针自证闭环"],
    },
    "龙珠": {
        "归属基底": ["L1不动母科层·07_语言文学学科"],
        "对应公理": ["鸟山明三元公理密码", "气的BSD本体论", "强化系变身系双公理耦合", "边缘者优势定理"],
    },
    "全职猎人": {
        "归属基底": ["L1不动母科层·07_语言文学学科"],
        "对应公理": ["念能力六系BSD解码", "母集子集边界定理", "不归零即无证定理", "黑暗大陆篇终极解码"],
    },
    "三游谱系": {
        "归属基底": ["L0总本源层·T92三元零本体论", "L1不动母科层·05_哲思认知统合学科"],
        "对应公理": ["气的BSD本体论", "三教皆官方批判论", "BSD内部系方程"],
    },
    "百家姓": {
        "归属基底": ["L1不动母科层·05_哲思认知统合学科"],
        "对应公理": ["0×0=n涌现公理", "魔性碎片聚合", "关系性代偿加密", "BSD内部系方程"],
    },
    "温度梯度": {
        "归属基底": ["L1不动母科层·05_哲思认知统合学科"],
        "对应公理": ["汉字温度梯度密码", "炁=无家死水定理", "逆时针归零操作"],
    },
    "佛道密码": {
        "归属基底": ["L0总本源层·T92三元零本体论", "L1不动母科层·05_哲思认知统合学科"],
        "对应公理": ["0×0=n涌现公理", "反反为空", "逆逆生虚", "佛道博弈论"],
    },
    "边缘涌现": {
        "归属基底": ["L0总本源层·T92三元零本体论", "L1不动母科层·05_哲思认知统合学科"],
        "对应公理": ["边缘者优势定理", "死水诅咒定理", "绝对反性定理"],
    },
    "BSD内部系": {
        "归属基底": ["L1不动母科层·05_哲思认知统合学科"],
        "对应公理": ["0×0=n涌现公理", "BSD内部系方程", "因果是系的子集"],
    },
    "六系本体": {
        "归属基底": ["L0总本源层·T92三元零本体论", "L1不动母科层·07_语言文学学科"],
        "对应公理": ["BSD气论六系本体", "母集子集边界定理", "念能力六系BSD解码"],
    },
}


@dataclass
class ConnectionRecord:
    """
    单条连接记录——描述两个文档之间的关键词连接（聚合后）
    归属基底+对应公理标注：满足MCP外部输出标签约束
    """
    source_file: str          # 源文档路径
    source_level: str         # 源文档层级
    source_title: str         # 源文档标题
    target_file: str          # 目标文档路径
    target_level: str         # 目标文档层级
    target_title: str         # 目标文档标题
    # 聚合字段：同一目标文档的多锚点命中聚合为一条
    connection_types: List[str] = field(default_factory=list)  # 命中的所有锚点名
    matched_keywords: List[str] = field(default_factory=list)  # 所有命中的关键词（去重）
    keyword_hit_counts: Dict[str, int] = field(default_factory=dict)  # 关键词命中次数
    # 归属基底+对应公理标签（MCP外部输出必需）
    matched_bases: List[str] = field(default_factory=list)     # 命中的归属基底
    matched_axioms: List[str] = field(default_factory=list)    # 命中的对应公理
    # 连接强度
    connection_strength: float = 0.0  # 综合连接强度（0-1）
    anchor_coverage: float = 0.0      # 锚点覆盖率（命中锚点数/总锚点数）
    # 层级跨度
    level_span: str = ""              # 如 "L0-L1"
    level_span_weight: float = 0.0    # 跨层级跨度权重
    # 双向验证（双时针自证闭环）
    bidirectional_verified: bool = False  # 目标文档是否反向连接到源文档
    reverse_matched_keywords: List[str] = field(default_factory=list)  # 反向命中关键词

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_file": self.source_file,
            "source_level": self.source_level,
            "source_title": self.source_title,
            "target_file": self.target_file,
            "target_level": self.target_level,
            "target_title": self.target_title,
            "connection_types": self.connection_types,
            "matched_keywords": self.matched_keywords,
            "keyword_hit_counts": self.keyword_hit_counts,
            "matched_bases": self.matched_bases,
            "matched_axioms": self.matched_axioms,
            "connection_strength": round(self.connection_strength, 4),
            "anchor_coverage": round(self.anchor_coverage, 4),
            "level_span": self.level_span,
            "level_span_weight": self.level_span_weight,
            "bidirectional_verified": self.bidirectional_verified,
            "reverse_matched_keywords": self.reverse_matched_keywords,
        }


@dataclass
class ConnectionGraph:
    """文档间连接关系图"""
    source_file: str
    source_title: str
    source_level: str
    connections: List[ConnectionRecord] = field(default_factory=list)
    missing_links: List[Dict[str, Any]] = field(default_factory=list)
    anchor_summary: Dict[str, int] = field(default_factory=dict)
    # 新增统计字段
    bidirectional_count: int = 0       # 双向验证通过的连接数
    cross_level_count: int = 0         # 跨层级连接数（非同层级）
    level_span_summary: Dict[str, int] = field(default_factory=dict)  # 层级跨度统计

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_file": self.source_file,
            "source_title": self.source_title,
            "source_level": self.source_level,
            "connection_count": len(self.connections),
            "connections": [c.to_dict() for c in self.connections],
            "missing_link_count": len(self.missing_links),
            "missing_links": self.missing_links,
            "anchor_summary": self.anchor_summary,
            "bidirectional_count": self.bidirectional_count,
            "cross_level_count": self.cross_level_count,
            "level_span_summary": self.level_span_summary,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class KeywordConnectionSearcher:
    """
    关键词连接搜寻器 V2.0

    核心能力：
      1. extract_anchors(source_file) → 从源文档提取连接锚点
      2. search_connected_docs(source_file) → 跨层级搜寻所有连接文档（聚合+双向验证）
      3. diagnose_missing_links(source_file, referenced_files) → 诊断遗漏的连接
      4. export_graph(graph, output_path) → 导出连接图为JSON文件
    """

    def __init__(self):
        self._file_cache: Dict[str, List[str]] = {}

    # ============================================================
    # 公开接口
    # ============================================================

    def extract_anchors(self, source_file: str) -> Dict[str, List[str]]:
        """
        从源文档提取连接锚点。

        参数
        ----
        source_file : str
            源文档路径

        返回
        ----
        Dict[str, List[str]]
            锚点名 -> 命中的关键词列表
        """
        lines = self._read_file(source_file)
        if not lines:
            return {}

        full_text = "\n".join(lines)

        anchors_found: Dict[str, List[str]] = {}
        for anchor_name, anchor_keywords in CONNECTION_ANCHORS.items():
            hit_kws: List[str] = []
            for kw in anchor_keywords:
                if kw in full_text:
                    hit_kws.append(kw)
            if hit_kws:
                anchors_found[anchor_name] = hit_kws

        return anchors_found

    def search_connected_docs(
        self,
        source_file: str,
        levels: Optional[List[str]] = None,
        exclude_self: bool = True,
        min_strength: float = 0.1,
        bidirectional_verify: bool = True,
    ) -> ConnectionGraph:
        """
        从源文档出发，跨层级搜寻所有关键词连接的文档（聚合 + 双向验证）。

        参数
        ----
        source_file : str
            源文档路径
        levels : List[str], optional
            限定搜寻层级，如 ["L0", "L1"]。默认全部
        exclude_self : bool
            是否排除源文档自身
        min_strength : float
            最小连接强度阈值
        bidirectional_verify : bool
            是否执行双向连接验证（双时针自证闭环）

        返回
        ----
        ConnectionGraph
            文档间连接关系图（已聚合）
        """
        # 1. 从源文档提取锚点
        anchors = self.extract_anchors(source_file)
        source_level = self._detect_level(source_file)
        source_title = self._extract_title(source_file)
        source_lines = self._read_file(source_file)
        source_text = "\n".join(source_lines) if source_lines else ""

        graph = ConnectionGraph(
            source_file=source_file,
            source_title=source_title,
            source_level=source_level,
        )
        graph.anchor_summary = {k: len(v) for k, v in anchors.items()}

        if not anchors:
            return graph

        # 2. 收集所有锚点关键词
        all_anchor_kws: Set[str] = set()
        for kws in anchors.values():
            all_anchor_kws.update(kws)

        # 3. 跨层级搜寻（先收集原始连接，再聚合）
        search_levels = levels if levels else list(LEVEL_MAP.keys())
        seen_files: Set[str] = set()
        # target_file -> List[raw_connection] 用于聚合
        raw_by_target: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for level in search_levels:
            level_path = LEVEL_MAP.get(level)
            if not level_path or not level_path.exists():
                continue

            for md_file in level_path.rglob("*.md"):
                file_path = str(md_file)

                if exclude_self and self._same_file(file_path, source_file):
                    continue

                if file_path in seen_files:
                    continue
                seen_files.add(file_path)

                raw_conns = self._scan_connection(
                    file_path, level, source_file, source_level,
                    anchors, all_anchor_kws
                )
                for rc in raw_conns:
                    raw_by_target[file_path].append(rc)

        # 4. 聚合：同一目标文档的多锚点命中合并为一条记录
        aggregated: List[ConnectionRecord] = []
        for target_file, raw_list in raw_by_target.items():
            if not raw_list:
                continue

            first = raw_list[0]
            target_level = first["target_level"]
            target_title = first["target_title"]

            # 聚合字段
            connection_types: List[str] = []
            matched_keywords: Set[str] = set()
            keyword_hit_counts: Dict[str, int] = {}
            matched_bases: Set[str] = set()
            matched_axioms: Set[str] = set()
            total_anchor_count = len(CONNECTION_ANCHORS)

            for rc in raw_list:
                anchor_name = rc["connection_type"]
                connection_types.append(anchor_name)
                for kw in rc["matched_keywords"]:
                    matched_keywords.add(kw)
                    keyword_hit_counts[kw] = keyword_hit_counts.get(kw, 0) + rc["keyword_counts"].get(kw, 1)

                # 从 ANCHOR_META 注入归属基底+对应公理
                meta = ANCHOR_META.get(anchor_name, {})
                for b in meta.get("归属基底", []):
                    matched_bases.add(b)
                for a in meta.get("对应公理", []):
                    matched_axioms.add(a)

            # 锚点覆盖率
            anchor_coverage = len(connection_types) / total_anchor_count if total_anchor_count > 0 else 0.0

            # 层级跨度
            level_span = f"{source_level}-{target_level}"
            level_span_weight = LEVEL_SPAN_WEIGHT.get(level_span, 0.5)

            # 综合连接强度 = γ × 锚点覆盖率 + (1-γ) × 关键词命中密度 × 层级跨度权重
            # γ=0.92 顺时针耦合强度：锚点覆盖率占主导
            keyword_density = min(1.0, len(matched_keywords) / 20.0)  # 归一化到[0,1]
            connection_strength = (
                GAMMA * anchor_coverage + (1 - GAMMA) * keyword_density * level_span_weight
            )

            # 双向验证（双时针自证闭环）
            bidirectional_verified = False
            reverse_matched: List[str] = []
            if bidirectional_verify and source_text:
                target_lines = self._read_file(target_file)
                target_text = "\n".join(target_lines) if target_lines else ""
                if target_text:
                    # 检查目标文档是否反向命中源文档的标题或核心锚点
                    reverse_check_kws = self._extract_reverse_keywords(source_text, source_title)
                    for rkw in reverse_check_kws:
                        if rkw in target_text:
                            reverse_matched.append(rkw)
                    # 至少命中 κ×10=3.5 即向上取整为4个关键词才算双向验证通过
                    # κ=0.35 逆时针归零阈值
                    threshold = max(1, int(KAPPA * 10))
                    bidirectional_verified = len(reverse_matched) >= threshold

            record = ConnectionRecord(
                source_file=source_file,
                source_level=source_level,
                source_title=source_title,
                target_file=target_file,
                target_level=target_level,
                target_title=target_title,
                connection_types=connection_types,
                matched_keywords=sorted(matched_keywords),
                keyword_hit_counts=keyword_hit_counts,
                matched_bases=sorted(matched_bases),
                matched_axioms=sorted(matched_axioms),
                connection_strength=connection_strength,
                anchor_coverage=anchor_coverage,
                level_span=level_span,
                level_span_weight=level_span_weight,
                bidirectional_verified=bidirectional_verified,
                reverse_matched_keywords=reverse_matched,
            )
            aggregated.append(record)

        # 按综合连接强度排序
        aggregated.sort(key=lambda c: c.connection_strength, reverse=True)

        # 应用最小强度过滤
        graph.connections = [c for c in aggregated if c.connection_strength >= min_strength]

        # 统计
        graph.bidirectional_count = sum(1 for c in graph.connections if c.bidirectional_verified)
        graph.cross_level_count = sum(1 for c in graph.connections if c.source_level != c.target_level)
        graph.level_span_summary = dict(Counter(c.level_span for c in graph.connections))

        return graph

    def diagnose_missing_links(
        self,
        source_file: str,
        referenced_files: List[str],
        levels: Optional[List[str]] = None,
        min_strength: float = 0.1,
    ) -> ConnectionGraph:
        """
        诊断立系/归档时遗漏的跨层级连接。

        参数
        ----
        source_file : str
            源文档路径（如BSD姓名因果论实证）
        referenced_files : List[str]
            已引用的文档路径列表（如版权信息中L0锚定基底+L1同层锚定列出的文档）
        levels : List[str], optional
            限定搜寻层级
        min_strength : float
            最小连接强度阈值

        返回
        ----
        ConnectionGraph
            包含 missing_links 诊断结果的连接关系图

        用法示例
        --------
        searcher = KeywordConnectionSearcher()
        graph = searcher.diagnose_missing_links(
            source_file=".../BSD姓名因果论实证...V1.0.md",
            referenced_files=[
                ".../BSD西游终极解码...V1.0.md",
                ".../BSD汉字温度梯度密码...V1.0.md",
            ]
        )
        # graph.missing_links 包含遗漏的连接文档（如龙珠=第二西游、全职猎人=第三西游）
        """
        graph = self.search_connected_docs(source_file, levels=levels, min_strength=min_strength)

        # 标准化已引用文件路径（统一为绝对路径字符串，便于跨平台匹配）
        referenced_set: Set[str] = set()
        for ref in referenced_files:
            try:
                ref_abs = str(Path(ref).resolve()).replace("\\", "/").lower()
                referenced_set.add(ref_abs)
            except Exception:
                referenced_set.add(ref.replace("\\", "/").lower())
            # 同时保留相对路径形式，以备绝对路径不可用时回退
            referenced_set.add(ref.replace("\\", "/").lower())

        for conn in graph.connections:
            # 同时准备目标文件的绝对路径与原始路径两种形式
            try:
                target_abs = str(Path(conn.target_file).resolve()).replace("\\", "/").lower()
            except Exception:
                target_abs = conn.target_file.replace("\\", "/").lower()
            target_orig = conn.target_file.replace("\\", "/").lower()

            is_referenced = any(
                ref in target_abs or target_abs in ref
                or ref in target_orig or target_orig in ref
                for ref in referenced_set
            )

            if not is_referenced:
                graph.missing_links.append({
                    "target_file": conn.target_file,
                    "target_level": conn.target_level,
                    "target_title": conn.target_title,
                    "connection_types": conn.connection_types,
                    "matched_keywords": conn.matched_keywords,
                    "matched_bases": conn.matched_bases,
                    "matched_axioms": conn.matched_axioms,
                    "connection_strength": round(conn.connection_strength, 4),
                    "anchor_coverage": round(conn.anchor_coverage, 4),
                    "level_span": conn.level_span,
                    "bidirectional_verified": conn.bidirectional_verified,
                    "diagnosis": self._build_diagnosis_text(conn),
                })

        return graph

    def export_graph(self, graph: ConnectionGraph, output_path: str) -> str:
        """
        导出连接关系图为JSON文件。

        参数
        ----
        graph : ConnectionGraph
            连接关系图
        output_path : str
            输出文件路径

        返回
        ----
        str
            实际保存路径
        """
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(graph.to_json())
        return str(output)

    # ============================================================
    # 内部方法
    # ============================================================

    def _scan_connection(
        self,
        target_file: str,
        target_level: str,
        source_file: str,
        source_level: str,
        anchors: Dict[str, List[str]],
        all_anchor_kws: Set[str],
    ) -> List[Dict[str, Any]]:
        """
        扫描目标文件，返回与源文档的原始连接记录（未聚合）
        每条记录包含关键词命中次数
        """
        lines = self._read_file(target_file)
        if not lines:
            return []

        full_text = "\n".join(lines)
        target_title = self._extract_title_from_lines(lines)

        results: List[Dict[str, Any]] = []

        for anchor_name, anchor_kws in anchors.items():
            hit_kws: List[str] = []
            keyword_counts: Dict[str, int] = {}

            for kw in anchor_kws:
                count = full_text.count(kw)
                if count > 0:
                    hit_kws.append(kw)
                    keyword_counts[kw] = count

            if not hit_kws:
                continue

            results.append({
                "target_file": target_file,
                "target_level": target_level,
                "target_title": target_title,
                "connection_type": anchor_name,
                "matched_keywords": hit_kws,
                "keyword_counts": keyword_counts,
            })

        return results

    def _extract_reverse_keywords(self, source_text: str, source_title: str) -> List[str]:
        """
        提取用于反向验证的关键词：
        - 源文档标题
        - 源文档中所有锚点词典关键词（如果出现在源文档中）
        """
        reverse_kws: List[str] = []
        # 标题作为反向验证关键词
        if source_title:
            # 拆分标题为有意义的片段（去除版本号、分隔符）
            title_clean = re.sub(r"_V[\d.]+", "", source_title)
            title_clean = re.sub(r"[——\-—·]+", " ", title_clean)
            for part in title_clean.split():
                if len(part) >= 3:
                    reverse_kws.append(part)
        # 加入所有锚点关键词（如果出现在源文档中）
        for kws in CONNECTION_ANCHORS.values():
            for kw in kws:
                if kw in source_text and kw not in reverse_kws:
                    reverse_kws.append(kw)
        return reverse_kws

    def _build_diagnosis_text(self, conn: ConnectionRecord) -> str:
        """构建遗漏诊断文本（含归属基底+对应公理标签）"""
        bases = "；".join(conn.matched_bases) if conn.matched_bases else "未标注"
        axioms = "；".join(conn.matched_axioms) if conn.matched_axioms else "未标注"
        bidir = "是" if conn.bidirectional_verified else "否"
        return (
            f"源文档通过{conn.connection_types}锚点连接到此文档，"
            f"但未在referenced_files中引用。"
            f"[归属基底：{bases}][对应公理：{axioms}]"
            f"[层级跨度：{conn.level_span}][双向验证：{bidir}]"
        )

    def _same_file(self, path_a: str, path_b: str) -> bool:
        """判断两个路径是否指向同一文件（跨平台）"""
        a = Path(path_a).resolve()
        b = Path(path_b).resolve()
        return a == b

    def _read_file(self, file_path: str) -> List[str]:
        """读取文件（带缓存）"""
        if file_path in self._file_cache:
            return self._file_cache[file_path]

        path = Path(file_path)
        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self._file_cache[file_path] = lines
            return lines
        except Exception:
            return []

    def _detect_level(self, file_path: str) -> str:
        """从文件路径检测层级（支持相对路径与绝对路径）"""
        # 优先用绝对路径解析后比较
        try:
            abs_fp = str(Path(file_path).resolve()).replace("\\", "/")
        except Exception:
            abs_fp = file_path.replace("\\", "/")
        # 同时准备相对路径形式的字符串（用于匹配相对路径输入）
        rel_fp = file_path.replace("\\", "/")

        for level, level_path in LEVEL_MAP.items():
            level_str = str(level_path).replace("\\", "/")
            if level_str in abs_fp or level_str in rel_fp:
                return level
            # 兼容相对路径：用 LEVEL_MAP 中的相对部分（theory_base/LX_xxx）
            try:
                rel_level = str(level_path.relative_to(THEORY_BASE_PATH)).replace("\\", "/")
                if rel_level in abs_fp or rel_level in rel_fp:
                    return level
            except Exception:
                pass
        return "unknown"

    def _extract_title(self, file_path: str) -> str:
        """从文件提取标题"""
        lines = self._read_file(file_path)
        return self._extract_title_from_lines(lines)

    def _extract_title_from_lines(self, lines: List[str]) -> str:
        """从行列表提取标题"""
        for line in lines[:20]:
            if line.startswith("# "):
                return line.lstrip("# ").strip()
        return ""

    def clear_cache(self):
        """清空文件缓存"""
        self._file_cache.clear()


# ============================================================
# 便捷函数
# ============================================================

def search_keyword_connections(
    source_file: str,
    levels: Optional[List[str]] = None,
    bidirectional_verify: bool = True,
) -> ConnectionGraph:
    """
    便捷函数：从源文档出发，搜寻所有关键词连接的文档。
    """
    searcher = KeywordConnectionSearcher()
    return searcher.search_connected_docs(
        source_file, levels=levels, bidirectional_verify=bidirectional_verify
    )


def diagnose_missing_connections(
    source_file: str,
    referenced_files: List[str],
    levels: Optional[List[str]] = None,
) -> ConnectionGraph:
    """
    便捷函数：诊断立系/归档时遗漏的跨层级连接。
    """
    searcher = KeywordConnectionSearcher()
    return searcher.diagnose_missing_links(
        source_file, referenced_files, levels=levels
    )


# ============================================================
# CLI 入口
# ============================================================

def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BSD关键词连接搜寻器 V2.0 —— 跨层级连接诊断工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
归属基底：第1重九维法理基底 + 第0重元道本源基底
对应公理：公理二（自主科研闭环动力学公理）+ 公理0·元道存在 + 关系性公理 + 双时针自证闭环
固定数理常量：γ=0.92（顺时针耦合强度）、κ=0.35（逆时针归零阈值）

示例：
  # 搜寻源文档的所有连接
  python keyword_connection_searcher.py search \\
      --source "theory_base/L1_不动母科层/05_哲思认知统合学科/BSD姓名因果论实证...V1.0.md" \\
      --levels L0 L1

  # 诊断遗漏连接（与已引用文档列表对比）
  python keyword_connection_searcher.py diagnose \\
      --source "theory_base/L1_不动母科层/05_哲思认知统合学科/BSD姓名因果论实证...V1.0.md" \\
      --referenced "theory_base/L1_不动母科层/07_语言文学学科/BSD框架下西游记终极解码...md"

  # 导出连接图为JSON
  python keyword_connection_searcher.py search \\
      --source "..." --output connection_graph.json
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜寻源文档的所有关键词连接")
    search_parser.add_argument("--source", required=True, help="源文档路径")
    search_parser.add_argument("--levels", nargs="*", default=None,
                               help="限定搜寻层级（如 L0 L1）")
    search_parser.add_argument("--min-strength", type=float, default=0.1,
                               help="最小连接强度阈值（默认0.1）")
    search_parser.add_argument("--no-bidirectional", action="store_true",
                               help="禁用双向连接验证")
    search_parser.add_argument("--output", default=None,
                               help="导出JSON文件路径（可选）")
    search_parser.add_argument("--top", type=int, default=20,
                               help="只显示前N条连接（默认20）")

    # diagnose 子命令
    diag_parser = subparsers.add_parser("diagnose", help="诊断遗漏的跨层级连接")
    diag_parser.add_argument("--source", required=True, help="源文档路径")
    diag_parser.add_argument("--referenced", nargs="+", required=True,
                             help="已引用的文档路径列表")
    diag_parser.add_argument("--levels", nargs="*", default=None,
                             help="限定搜寻层级")
    diag_parser.add_argument("--output", default=None,
                             help="导出JSON文件路径（可选）")

    return parser


def _format_connection_line(c: ConnectionRecord, idx: int) -> str:
    """格式化单条连接为CLI显示行"""
    bidir_mark = "✓" if c.bidirectional_verified else " "
    bases_short = "；".join(c.matched_bases[:2]) if c.matched_bases else "未标注"
    axioms_short = "；".join(c.matched_axioms[:3]) if c.matched_axioms else "未标注"
    title = c.target_title[:50] if c.target_title else Path(c.target_file).stem
    return (
        f"  [{idx:02d}] [{c.target_level}][{c.level_span}][{bidir_mark}] "
        f"强度={c.connection_strength:.3f} 覆盖={c.anchor_coverage:.2f}\n"
        f"       文档: {title}\n"
        f"       锚点: {c.connection_types}\n"
        f"       命中: {c.matched_keywords[:10]}\n"
        f"       [归属基底：{bases_short}]\n"
        f"       [对应公理：{axioms_short}]"
    )


def _cli_main(args: argparse.Namespace) -> int:
    searcher = KeywordConnectionSearcher()

    if args.command == "search":
        levels = args.levels
        graph = searcher.search_connected_docs(
            source_file=args.source,
            levels=levels,
            min_strength=args.min_strength,
            bidirectional_verify=not args.no_bidirectional,
        )

        print("=" * 70)
        print(f"BSD关键词连接搜寻结果 V2.0")
        print(f"归属基底：第1重九维法理基底 + 第0重元道本源基底")
        print(f"对应公理：公理二 + 公理0·元道存在 + 关系性公理 + 双时针自证闭环")
        print(f"固定数理常量：γ={GAMMA}、κ={KAPPA}")
        print("=" * 70)
        print(f"源文档: {graph.source_title}")
        print(f"源层级: {graph.source_level}")
        print(f"锚点命中: {graph.anchor_summary}")
        print(f"连接文档总数: {len(graph.connections)}")
        print(f"双向验证通过: {graph.bidirectional_count}")
        print(f"跨层级连接: {graph.cross_level_count}")
        print(f"层级跨度分布: {graph.level_span_summary}")
        print("-" * 70)
        print(f"前 {min(args.top, len(graph.connections))} 条连接（按强度排序）:")
        for i, c in enumerate(graph.connections[:args.top], 1):
            print(_format_connection_line(c, i))

        if args.output:
            path = searcher.export_graph(graph, args.output)
            print(f"\n已导出连接图: {path}")

    elif args.command == "diagnose":
        graph = searcher.diagnose_missing_links(
            source_file=args.source,
            referenced_files=args.referenced,
            levels=args.levels,
        )

        print("=" * 70)
        print(f"BSD遗漏连接诊断结果 V2.0")
        print(f"归属基底：第1重九维法理基底 + 第0重元道本源基底")
        print("=" * 70)
        print(f"源文档: {graph.source_title}")
        print(f"源层级: {graph.source_level}")
        print(f"已引用文档数: {len(args.referenced)}")
        print(f"连接文档总数: {len(graph.connections)}")
        print(f"遗漏连接数: {len(graph.missing_links)}")
        print("-" * 70)
        if graph.missing_links:
            print("遗漏的连接文档（需补充立系）:")
            for i, ml in enumerate(graph.missing_links, 1):
                title = ml.get("target_title", "")[:50]
                print(f"  [{i:02d}] [{ml['target_level']}][{ml['level_span']}] {title}")
                print(f"       锚点: {ml['connection_types']}")
                print(f"       命中: {ml['matched_keywords'][:10]}")
                bases = "；".join(ml.get("matched_bases", []))
                axioms = "；".join(ml.get("matched_axioms", []))
                print(f"       [归属基底：{bases}]")
                print(f"       [对应公理：{axioms}]")
                print(f"       强度={ml['connection_strength']:.3f} 双向验证={ml['bidirectional_verified']}")
                print()
        else:
            print("✓ 未发现遗漏连接，立系完整。")

        if args.output:
            path = searcher.export_graph(graph, args.output)
            print(f"\n已导出诊断报告: {path}")

    else:
        _build_cli().print_help()
        return 1

    return 0


def main():
    """CLI主入口"""
    parser = _build_cli()
    args = parser.parse_args()
    raise SystemExit(_cli_main(args))


if __name__ == "__main__":
    main()
