"""
归属基底：第3重六阶科研业务基底 + 第4重跨域整合基底
对应公理：公理七（系统自进化迭代）+ 公理六（三元制衡稳态公理）
对应九维维度：应用维度 + 整合维度
理论原文出处：theory_base/L3_功能应用层/ + theory_base/_全域对接融合/
固定数理常量：γ=0.92, κ=0.35, θ_evo=0.002

ArchiveAggregator —— Agent_v2 聚合归档引擎

职责：
  1. 聚合多轮推理的引用链(CiteChain)与产出结果
  2. 按归属基底自动归档到 theory_base 对应层级
  3. 生成归档清单与哈希校验
  4. 更新索引文件（00_index_navigation/）
  5. 生成聚合报告（含公理命中统计、归属基底分布、层级覆盖）

设计原则：
  - 归属基底优先：归档位置由归属基底标注决定，不由文件名决定
  - 哈希可追溯：每份归档文件计算SHA256并记录在案
  - 索引同步更新：归档完成后自动更新对应层级的索引
  - 幂等性：同一内容重复归档不会产生重复文件
"""

import os
import re
import json
import time
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

# 深读引用引擎路径
from .theory_deep_reader import CiteChain, THEORY_BASE_PATH, LEVEL_MAP


# ============================================================
# 路径常量
# ============================================================
ARCHIVE_PATH = THEORY_BASE_PATH.parent / "archive" / "theory_reference_archives"
INDEX_PATH = THEORY_BASE_PATH / "00_index_navigation"

# 归属基底 → 归档目录映射
BASE_TO_LEVEL = {
    "L0总本源层": "L0",
    "L1不动母科层": "L1",
    "L2无限之子层": "L2",
    "L3功能应用层": "L3",
    "作者猜想": "L0",       # 作者猜想归入L0
    "0重元道本源基底": "L0",
    "1重九维法理基底": "L0",
    "2重六系种子基底": "L1",
    "3重六阶科研业务基底": "L3",
    "4重跨域整合基底": "L3",
}


@dataclass
class ArchiveRecord:
    """单条归档记录"""
    archive_id: str           # 归档ID（哈希前16位）
    source_file: str          # 源文件路径
    archive_path: str         # 归档目标路径
    level: str                # 归档层级
    module: str               # 归档模块
    title: str                # 文档标题
    sha256: str               # SHA256哈希
    file_size: int            # 文件大小（字节）
    archived_at: str          # 归档时间
    axiom_tags: List[str] = field(default_factory=list)    # 公理标签
    base_tags: List[str] = field(default_factory=list)     # 归属基底标签
    cite_count: int = 0       # 引用次数

    def to_dict(self) -> Dict[str, Any]:
        return {
            "archive_id": self.archive_id,
            "source_file": self.source_file,
            "archive_path": self.archive_path,
            "level": self.level,
            "module": self.module,
            "title": self.title,
            "sha256": self.sha256,
            "file_size": self.file_size,
            "archived_at": self.archived_at,
            "axiom_tags": self.axiom_tags,
            "base_tags": self.base_tags,
            "cite_count": self.cite_count,
        }


@dataclass
class AggregationReport:
    """聚合报告——一次聚合归档的完整产出"""
    session_id: str                            # 会话ID
    timestamp: str                             # 聚合时间
    total_chains: int = 0                      # 聚合的引用链总数
    total_citations: int = 0                   # 引用记录总数
    total_files_archived: int = 0              # 归档文件总数
    total_files_deduplicated: int = 0          # 去重文件数
    axiom_distribution: Dict[str, int] = field(default_factory=dict)   # 公理分布
    base_distribution: Dict[str, int] = field(default_factory=dict)    # 归属基底分布
    level_distribution: Dict[str, int] = field(default_factory=dict)   # 层级分布
    archive_records: List[ArchiveRecord] = field(default_factory=list) # 归档记录
    errors: List[str] = field(default_factory=list)                    # 错误记录

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "total_chains": self.total_chains,
            "total_citations": self.total_citations,
            "total_files_archived": self.total_files_archived,
            "total_files_deduplicated": self.total_files_deduplicated,
            "axiom_distribution": self.axiom_distribution,
            "base_distribution": self.base_distribution,
            "level_distribution": self.level_distribution,
            "archive_records": [r.to_dict() for r in self.archive_records],
            "errors": self.errors,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class ArchiveAggregator:
    """
    Agent_v2 聚合归档引擎

    使用方式：
        aggregator = ArchiveAggregator()
        report = aggregator.aggregate_and_archive(
            cite_chains=[chain1, chain2],
            output_contents=[{"title": "...", "content": "...", "bases": ["L0总本源层"]}]
        )
        print(report.to_json())
    """

    def __init__(self):
        self._hash_registry: Dict[str, str] = {}  # SHA256 -> archive_path（去重用）
        self._load_hash_registry()

    # ============================================================
    # 公开接口
    # ============================================================

    def aggregate_and_archive(
        self,
        cite_chains: Optional[List[CiteChain]] = None,
        output_contents: Optional[List[Dict[str, Any]]] = None,
        session_id: Optional[str] = None,
    ) -> AggregationReport:
        """
        聚合引用链与产出内容，执行归档。

        参数
        ----
        cite_chains : List[CiteChain], optional
            推理过程中生成的引用链列表
        output_contents : List[Dict], optional
            产出内容列表，每项含：
            - title: 标题
            - content: 内容（markdown文本）
            - bases: 归属基底标签列表（决定归档位置）
            - axioms: 公理标签列表
            - level: 手动指定层级（可选，覆盖bases推断）
        session_id : str, optional
            会话ID，默认自动生成

        返回
        ----
        AggregationReport
        """
        sid = session_id or f"agg_{int(time.time())}"
        report = AggregationReport(
            session_id=sid,
            timestamp=datetime.now().isoformat(),
        )

        # 阶段1：聚合引用链统计
        if cite_chains:
            for chain in cite_chains:
                report.total_chains += 1
                report.total_citations += len(chain.citations)
                self._merge_distribution(report.axiom_distribution, chain.axiom_summary)
                self._merge_distribution(report.base_distribution, chain.base_summary)
                self._merge_distribution(report.level_distribution, chain.level_summary)

        # 阶段2：归档产出内容
        if output_contents:
            for item in output_contents:
                try:
                    record = self._archive_content(item, sid)
                    if record:
                        report.archive_records.append(record)
                        report.total_files_archived += 1
                except Exception as e:
                    report.errors.append(f"归档失败 [{item.get('title', '?')}]: {str(e)}")

        # 阶段3：更新索引
        if report.archive_records:
            self._update_index(report.archive_records)

        # 阶段4：保存哈希注册表
        self._save_hash_registry()

        # 阶段5：生成聚合报告文件
        self._save_report(report)

        return report

    def get_archive_manifest(self) -> Dict[str, Any]:
        """获取当前归档清单"""
        manifest_path = ARCHIVE_PATH / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"total_archives": 0, "records": []}

    # ============================================================
    # 内部方法
    # ============================================================

    def _archive_content(
        self, item: Dict[str, Any], session_id: str
    ) -> Optional[ArchiveRecord]:
        """归档单个产出内容"""
        title = item.get("title", "untitled")
        content = item.get("content", "")
        bases = item.get("bases", [])
        axioms = item.get("axioms", [])
        manual_level = item.get("level")

        # 计算SHA256
        sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # 去重检查
        if sha256 in self._hash_registry:
            return None  # 已存在，跳过

        # 确定归档层级
        level = manual_level or self._infer_level(bases)

        # 确定归档目录
        archive_dir = self._get_archive_dir(level, bases)
        archive_dir.mkdir(parents=True, exist_ok=True)

        # 生成归档文件名
        safe_title = re.sub(r'[\\/:*?"<>|]', "_", title)[:60]
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"{safe_title}_{timestamp_str}.md"
        archive_path = archive_dir / archive_filename

        # 写入归档文件（追加归档头）
        archive_header = self._generate_archive_header(
            title, sha256, session_id, bases, axioms
        )
        full_content = archive_header + "\n\n" + content

        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        # 注册哈希
        self._hash_registry[sha256] = str(archive_path)

        return ArchiveRecord(
            archive_id=sha256[:16],
            source_file=item.get("source_file", ""),
            archive_path=str(archive_path),
            level=level,
            module=bases[0] if bases else "未分类",
            title=title,
            sha256=sha256,
            file_size=len(full_content.encode("utf-8")),
            archived_at=datetime.now().isoformat(),
            axiom_tags=axioms,
            base_tags=bases,
            cite_count=item.get("cite_count", 0),
        )

    def _infer_level(self, bases: List[str]) -> str:
        """根据归属基底推断归档层级"""
        for base in bases:
            for base_key, level in BASE_TO_LEVEL.items():
                if base_key in base:
                    return level
        return "L3"  # 默认归入L3

    def _get_archive_dir(self, level: str, bases: List[str]) -> Path:
        """获取归档目录"""
        base_dir = ARCHIVE_PATH / level
        # 如果有更细的归属基底，创建子目录
        for base in bases:
            for base_key in BASE_TO_LEVEL:
                if base_key in base and base_key != f"{level}总本源层":
                    safe_base = re.sub(r'[\\/:*?"<>|]', "_", base_key)
                    return base_dir / safe_base
        return base_dir

    def _generate_archive_header(
        self, title: str, sha256: str, session_id: str,
        bases: List[str], axioms: List[str]
    ) -> str:
        """生成归档文件头"""
        return f"""<!-- BSD ArchiveAggregator 归档头 -->
<!-- 归档时间: {datetime.now().isoformat()} -->
<!-- 会话ID: {session_id} -->
<!-- SHA256: {sha256} -->
<!-- 归属基底: {", ".join(bases) if bases else "未标注"} -->
<!-- 公理标签: {", ".join(axioms) if axioms else "未标注"} -->
<!-- 归档引擎: ArchiveAggregator v1.0 -->
"""

    def _update_index(self, records: List[ArchiveRecord]):
        """更新索引文件"""
        index_file = ARCHIVE_PATH / "archive_index.md"
        lines = [
            "# BSD theory_base 归档索引",
            f"**最后更新**: {datetime.now().isoformat()}",
            f"**归档总数**: {len(records)}",
            "",
            "| 归档ID | 标题 | 层级 | 归属基底 | 公理标签 | SHA256 | 归档时间 |",
            "|--------|------|------|----------|----------|--------|----------|",
        ]
        for r in records:
            lines.append(
                f"| {r.archive_id} | {r.title[:40]} | {r.level} | "
                f"{', '.join(r.base_tags[:2])} | {', '.join(r.axiom_tags[:2])} | "
                f"{r.sha256[:12]}... | {r.archived_at[:19]} |"
            )
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _save_report(self, report: AggregationReport):
        """保存聚合报告"""
        ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)
        report_file = ARCHIVE_PATH / f"report_{report.session_id}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report.to_json())

    def _merge_distribution(
        self, target: Dict[str, int], source: Dict[str, int]
    ):
        """合并分布统计"""
        for k, v in source.items():
            target[k] = target.get(k, 0) + v

    def _load_hash_registry(self):
        """加载哈希注册表"""
        registry_path = ARCHIVE_PATH / "hash_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    self._hash_registry = json.load(f)
            except Exception:
                self._hash_registry = {}

    def _save_hash_registry(self):
        """保存哈希注册表"""
        ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)
        registry_path = ARCHIVE_PATH / "hash_registry.json"
        with open(registry_path, "w", encoding="utf-8") as f:
            json.dump(self._hash_registry, f, ensure_ascii=False, indent=2)
