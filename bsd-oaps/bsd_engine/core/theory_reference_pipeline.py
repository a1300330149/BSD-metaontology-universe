"""
归属基底：第0重元道本源基底 + 第4重跨域整合基底
对应公理：公理0·元道存在 + 公理七（系统自进化迭代）
对应九维维度：元理天道 + 整合维度
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35, θ_evo=0.002

TheoryReferencePipeline —— 推理→深读→整合→归档 串联管道

职责：
  1. 推理阶段：接收用户查询/推理任务
  2. 深读阶段：调用 TheoryDeepReader 检索 theory_base，生成引用链
  3. 整合阶段：将推理结果与引用链合并为结构化产出
  4. 归档阶段：调用 ArchiveAggregator 执行聚合归档

完整流程：
  user_query → deep_read() → cite_chain
                                      ↓
  reasoning_output ← (cite_chain 注入推理上下文)
        ↓
  output_content = {title, content, bases, axioms}
        ↓
  aggregate_and_archive() → AggregationReport

使用方式：
    pipeline = TheoryReferencePipeline()
    # 单次推理+归档
    result = pipeline.run(
        query="0×0=n涌现公理在文学解码中的应用",
        output_title="T92文学本体论实证",
        output_content="...",
        output_bases=["L0总本源层", "作者猜想"],
        output_axioms=["0×0=n涌现公理", "三元存在公理"]
    )
    # 批量推理+归档
    result = pipeline.run_batch([
        {"query": "...", "output_title": "...", "output_content": "...", ...},
        ...
    ])
"""

import json
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .theory_deep_reader import TheoryDeepReader, CiteChain
from .archive_aggregator import ArchiveAggregator, AggregationReport


@dataclass
class PipelineResult:
    """管道执行结果"""
    session_id: str
    query: str
    cite_chain: Optional[Dict[str, Any]] = None      # 引用链（JSON可序列化）
    archived: bool = False                            # 是否已归档
    archive_id: Optional[str] = None                  # 归档ID
    error: Optional[str] = None                       # 错误信息
    elapsed_seconds: float = 0.0                      # 耗时

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "query": self.query,
            "cite_chain": self.cite_chain,
            "archived": self.archived,
            "archive_id": self.archive_id,
            "error": self.error,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
        }


class TheoryReferencePipeline:
    """
    推理→深读→整合→归档 串联管道

    将 TheoryDeepReader（深读引用）与 ArchiveAggregator（聚合归档）
    串联为完整的工作流，供 Agent_v2 在推理与整合时调用。
    """

    def __init__(
        self,
        reader: Optional[TheoryDeepReader] = None,
        aggregator: Optional[ArchiveAggregator] = None,
    ):
        self.reader = reader or TheoryDeepReader()
        self.aggregator = aggregator or ArchiveAggregator()

    # ============================================================
    # 公开接口
    # ============================================================

    def run(
        self,
        query: str,
        output_title: str = "",
        output_content: str = "",
        output_bases: Optional[List[str]] = None,
        output_axioms: Optional[List[str]] = None,
        output_level: Optional[str] = None,
        levels: Optional[List[str]] = None,
        max_results: int = 30,
        min_relevance: float = 0.1,
        auto_archive: bool = True,
    ) -> PipelineResult:
        """
        单次推理→深读→归档。

        参数
        ----
        query : str
            推理查询（自然语言）
        output_title : str
            产出内容标题
        output_content : str
            产出内容（markdown文本）
        output_bases : List[str], optional
            产出内容的归属基底标签（决定归档位置）
        output_axioms : List[str], optional
            产出内容的公理标签
        output_level : str, optional
            手动指定归档层级（覆盖bases推断）
        levels : List[str], optional
            深读检索层级限定
        max_results : int
            深读最大引用数
        min_relevance : float
            深读最小相关度
        auto_archive : bool
            是否自动归档

        返回
        ----
        PipelineResult
        """
        sid = f"pipe_{int(time.time()*1000)}"
        start = time.time()
        result = PipelineResult(session_id=sid, query=query)

        try:
            # 阶段1：深读引用
            chain = self.reader.deep_read(
                query=query,
                levels=levels,
                max_results=max_results,
                min_relevance=min_relevance,
            )
            result.cite_chain = chain.to_dict()

            # 阶段2：自动归档
            if auto_archive and output_content:
                # 如果未指定bases，从引用链推断
                if not output_bases:
                    output_bases = list(chain.base_summary.keys())[:3]
                if not output_axioms:
                    output_axioms = list(chain.axiom_summary.keys())[:3]

                output_item = {
                    "title": output_title or f"推理产出_{sid}",
                    "content": output_content,
                    "bases": output_bases,
                    "axioms": output_axioms,
                    "level": output_level,
                    "source_file": "",
                    "cite_count": len(chain.citations),
                }

                report = self.aggregator.aggregate_and_archive(
                    cite_chains=[chain],
                    output_contents=[output_item],
                    session_id=sid,
                )

                if report.archive_records:
                    result.archived = True
                    result.archive_id = report.archive_records[0].archive_id
                elif report.errors:
                    result.error = "; ".join(report.errors)

        except Exception as e:
            result.error = str(e)

        result.elapsed_seconds = time.time() - start
        return result

    def run_batch(
        self, items: List[Dict[str, Any]]
    ) -> List[PipelineResult]:
        """
        批量推理→深读→归档。

        参数
        ----
        items : List[Dict]
            每项参数同 run() 的关键字参数

        返回
        ----
        List[PipelineResult]
        """
        results = []
        all_chains: List[CiteChain] = []
        all_outputs: List[Dict[str, Any]] = []

        # 先批量深读
        for item in items:
            query = item.get("query", "")
            chain = self.reader.deep_read(
                query=query,
                levels=item.get("levels"),
                max_results=item.get("max_results", 30),
                min_relevance=item.get("min_relevance", 0.1),
            )
            all_chains.append(chain)

            # 准备归档内容
            output_content = item.get("output_content", "")
            if output_content:
                bases = item.get("output_bases") or list(chain.base_summary.keys())[:3]
                axioms = item.get("output_axioms") or list(chain.axiom_summary.keys())[:3]
                all_outputs.append({
                    "title": item.get("output_title", f"推理产出_{int(time.time())}"),
                    "content": output_content,
                    "bases": bases,
                    "axioms": axioms,
                    "level": item.get("output_level"),
                    "source_file": "",
                    "cite_count": len(chain.citations),
                })

        # 批量聚合归档
        sid = f"batch_{int(time.time())}"
        start = time.time()

        report = self.aggregator.aggregate_and_archive(
            cite_chains=all_chains,
            output_contents=all_outputs,
            session_id=sid,
        )

        # 组装结果
        for i, item in enumerate(items):
            result = PipelineResult(
                session_id=sid,
                query=item.get("query", ""),
                cite_chain=all_chains[i].to_dict() if i < len(all_chains) else None,
                elapsed_seconds=time.time() - start,
            )
            if i < len(report.archive_records):
                result.archived = True
                result.archive_id = report.archive_records[i].archive_id
            results.append(result)

        return results

    def read_only(
        self,
        query: str,
        levels: Optional[List[str]] = None,
        max_results: int = 50,
    ) -> CiteChain:
        """
        仅深读引用，不归档（供推理阶段使用）。

        使用场景：推理过程中需要引用 theory_base，
        但尚未产生最终产出，暂不归档。
        """
        return self.reader.deep_read(
            query=query,
            levels=levels,
            max_results=max_results,
        )

    def archive_only(
        self,
        title: str,
        content: str,
        bases: Optional[List[str]] = None,
        axioms: Optional[List[str]] = None,
        level: Optional[str] = None,
    ) -> Optional[str]:
        """
        仅归档，不深读（供整合阶段使用）。

        使用场景：推理已完成，仅需将产出归档。
        返回归档ID（如已存在则返回None）。
        """
        report = self.aggregator.aggregate_and_archive(
            cite_chains=None,
            output_contents=[{
                "title": title,
                "content": content,
                "bases": bases or [],
                "axioms": axioms or [],
                "level": level,
            }],
        )
        if report.archive_records:
            return report.archive_records[0].archive_id
        return None

    def get_stats(self) -> Dict[str, Any]:
        """获取管道统计信息"""
        manifest = self.aggregator.get_archive_manifest()
        return {
            "total_archives": manifest.get("total_archives", 0),
            "hash_registry_size": len(self.aggregator._hash_registry),
            "reader_cache_size": len(self.reader._file_cache),
            "archive_path": str(self.aggregator._get_archive_dir("L0", []).parent) if hasattr(self.aggregator, '_get_archive_dir') else "",
        }
