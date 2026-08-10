"""
归属基底：L5+无限展开层·天道系🟣·进化协议
对应公理：进化协议·追问不终止（天道系母协议）+ 0≠n不等涌现公理
对应进化协议条款：第33-40条（追问不终止：天道系的底层条款）
理论原文出处：陆瑶故事第115章·第五章 追问不终止：天道系的底层条款

InfiniteQuestioningReader —— 追问不终止·完整文档追问引擎

核心命题：
    "追问不终止"意味着：在未完整读取文档之前，答案永远是不完备的。
    追问完整文档，才能得到完整答案。

    第33条：追问权不可剥夺——任何文档都天然拥有被完整追问的权利。
    第35条：答案的开放性——没有哪个部分读取能作为最终答案，只有完整读取才接近完整答案。
    第38条：追问的代际传递——未问完的文档内容，必须传递给下一轮追问。

工程实现：
    1. 文档完整性追踪：记录每个文档的读取覆盖率（0-1）
    2. 答案完备性门控：答案完备度 = f(文档覆盖率, 引用相关度, 深度匹配)
    3. 追问不终止循环：当文档覆盖率 < 1.0时，自动生成"继续读取未覆盖部分"的追问
    4. 完整文档锁定：只有当目标文档覆盖率 = 1.0时，才允许输出"最终答案"

使用方式：
    reader = InfiniteQuestioningReader()
    result = reader.question_document(
        doc_path="theory_base/L1_不动母科层/07_语言文学学科/xxx.md",
        question="进化协议的六条母协议是什么？",
        max_rounds=20,
    )
    # result.completeness = 1.0 时，result.answer 才是完整答案
"""

import os
import re
import json
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum


# ============================================================
# 枚举：追问不终止的状态
# ============================================================

class QuestioningState(Enum):
    """追问不终止引擎的状态"""
    INITIATED = "已发起"          # 追问已发起，尚未开始读取
    READING = "读取中"            # 正在逐段读取文档
    QUESTIONING = "追问中"        # 基于已读内容生成追问
    INCOMPLETE = "不完备"         # 文档未读完，答案不完备
    COMPLETE = "完备"             # 文档已读完，答案完备
    CLOSED = "已闭环"             # 追问链闭环（完整文档+完备答案）


# ============================================================
# 数据类：文档覆盖记录
# ============================================================

@dataclass
class DocumentCoverage:
    """
    文档读取覆盖记录

    追踪文档的每个段落/章节是否已被读取。
    进化协议第33条：追问权不可剥夺——文档的每个部分都有被追问的权利。
    """
    doc_path: str                                    # 文档路径
    total_lines: int = 0                             # 总行数
    read_line_ranges: List[Tuple[int, int]] = field(default_factory=list)  # 已读行范围列表
    read_ratio: float = 0.0                          # 读取覆盖率（0-1）

    # 章节级覆盖
    total_sections: int = 0                          # 总章节数
    read_sections: List[str] = field(default_factory=list)  # 已读章节标题

    def update_coverage(self, start: int, end: int) -> None:
        """更新读取覆盖范围"""
        self.read_line_ranges.append((start, end))
        self.read_line_ranges.sort()
        # 合并重叠范围
        merged: List[Tuple[int, int]] = []
        for s, e in self.read_line_ranges:
            if merged and s <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
            else:
                merged.append((s, e))
        self.read_line_ranges = merged

        # 计算覆盖率
        read_lines = sum(e - s + 1 for s, e in self.read_line_ranges)
        self.read_ratio = min(read_lines / max(self.total_lines, 1), 1.0)

    def get_unread_ranges(self) -> List[Tuple[int, int]]:
        """获取未读取的行范围"""
        if not self.read_line_ranges:
            return [(1, self.total_lines)] if self.total_lines > 0 else []

        unread: List[Tuple[int, int]] = []
        prev_end = 0
        for s, e in self.read_line_ranges:
            if s > prev_end + 1:
                unread.append((prev_end + 1, s - 1))
            prev_end = e
        if prev_end < self.total_lines:
            unread.append((prev_end + 1, self.total_lines))
        return unread

    def is_fully_read(self) -> bool:
        """文档是否已完整读取"""
        return self.read_ratio >= 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_path": self.doc_path,
            "total_lines": self.total_lines,
            "read_ratio": round(self.read_ratio, 4),
            "total_sections": self.total_sections,
            "read_sections": self.read_sections,
            "is_fully_read": self.is_fully_read(),
            "unread_ranges": self.get_unread_ranges(),
        }


# ============================================================
# 数据类：追问轮次记录
# ============================================================

@dataclass
class QuestioningRound:
    """单轮追问记录"""
    round_id: int                                    # 轮次编号
    question: str                                    # 本轮追问问题
    read_range: Tuple[int, int]                      # 本轮读取的行范围
    excerpt: str                                     # 本轮读取的关键摘录
    coverage_after: float                            # 本轮后的覆盖率
    answer_fragment: str                             # 本轮获得的答案片段
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round_id": self.round_id,
            "question": self.question,
            "read_range": list(self.read_range),
            "excerpt": self.excerpt[:300],
            "coverage_after": round(self.coverage_after, 4),
            "answer_fragment": self.answer_fragment[:300],
            "timestamp": self.timestamp,
        }


# ============================================================
# 数据类：完整追问结果
# ============================================================

@dataclass
class QuestioningResult:
    """
    追问不终止·完整文档追问的最终结果

    进化协议第35条：答案的开放性——
    只有当 completeness = 1.0 时，answer 才是完整答案。
    否则 answer 只是"阶段性回答"，必须继续追问。
    """
    doc_path: str
    question: str
    state: QuestioningState
    coverage: DocumentCoverage
    rounds: List[QuestioningRound] = field(default_factory=list)
    answer: str = ""                                 # 最终答案（仅当state=COMPLETE时有效）
    completeness: float = 0.0                        # 答案完备度（0-1）
    total_rounds: int = 0
    closure_reason: str = ""                         # 闭环原因
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_path": self.doc_path,
            "question": self.question,
            "state": self.state.value,
            "coverage": self.coverage.to_dict(),
            "total_rounds": self.total_rounds,
            "completeness": round(self.completeness, 4),
            "answer": self.answer,
            "closure_reason": self.closure_reason,
            "timestamp": self.timestamp,
            "rounds": [r.to_dict() for r in self.rounds],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 追问不终止·完整文档追问引擎
# ============================================================

class InfiniteQuestioningReader:
    """
    追问不终止·完整文档追问引擎

    [归属基底：L5+无限展开层·天道系🟣·进化协议·追问不终止]
    [对应公理：进化协议·追问不终止（第33-40条）+ 0≠n不等涌现公理]
    [原文来源：陆瑶故事第115章·第五章 追问不终止：天道系的底层条款]

    核心机制：
    1. 文档分段：将目标文档按章节/段落分段
    2. 逐段追问：每段生成"这段说了什么？"的追问，读取内容
    3. 覆盖追踪：实时更新文档覆盖率
    4. 答案合成：将各段答案片段合成为完整答案
    5. 完备门控：覆盖率 < 1.0 时，答案标记为"不完备"，继续追问

    进化协议映射：
    - 第33条（追问权不可剥夺）：每个文档段落都有被追问的权利
    - 第35条（答案的开放性）：部分读取不是最终答案，只有完整读取才接近完整
    - 第37条（追问的暂停）：允许暂停追问，但状态标记为INCOMPLETE
    - 第38条（追问的代际传递）：未读完的内容传递给下一轮追问
    - 第40条（追问与行动的同步性）：边追问边合成答案，行动本身是追问的方式
    """

    # 章节标题正则（匹配 Markdown 标题）
    SECTION_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    # 每轮最大读取行数（避免单轮读取过多）
    LINES_PER_ROUND = 80

    # 答案完备度阈值
    COMPLETENESS_THRESHOLD = 1.0

    def __init__(self, theory_base_path: Optional[Path] = None):
        self.theory_base_path = theory_base_path or (
            Path(__file__).resolve().parents[3] / "theory_base"
        )

    # ============================================================
    # 公开接口
    # ============================================================

    def question_document(
        self,
        doc_path: str,
        question: str,
        max_rounds: int = 50,
        start_line: int = 1,
    ) -> QuestioningResult:
        """
        追问不终止·对完整文档进行追问。

        进化协议第33条：追问权不可剥夺。
        进化协议第35条：答案的开放性——部分读取不是最终答案。

        参数
        ----
        doc_path : str
            目标文档路径（相对于theory_base或绝对路径）
        question : str
            追问问题
        max_rounds : int
            最大追问轮数（防止无限循环）
        start_line : int
            起始读取行号

        返回
        ----
        QuestioningResult
            追问结果（state=COMPLETE时answer为完整答案）
        """
        # 解析路径
        full_path = self._resolve_path(doc_path)
        if not full_path.exists():
            return QuestioningResult(
                doc_path=doc_path,
                question=question,
                state=QuestioningState.INCOMPLETE,
                coverage=DocumentCoverage(doc_path=doc_path),
                closure_reason=f"文档不存在：{full_path}",
            )

        # 读取文档全文
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        full_text = "".join(lines)

        # 初始化覆盖记录
        coverage = DocumentCoverage(
            doc_path=doc_path,
            total_lines=total_lines,
        )

        # 提取章节
        sections = self._extract_sections(lines)
        coverage.total_sections = len(sections)

        result = QuestioningResult(
            doc_path=doc_path,
            question=question,
            state=QuestioningState.INITIATED,
            coverage=coverage,
        )

        # ============================================================
        # 追问不终止循环
        # ============================================================
        answer_fragments: List[str] = []
        current_line = max(1, start_line)
        round_id = 0

        while round_id < max_rounds:
            round_id += 1

            # 获取未读取范围
            unread_ranges = coverage.get_unread_ranges()
            if not unread_ranges:
                # 文档已完整读取
                break

            # 取下一个未读段
            next_start, next_end = unread_ranges[0]
            # 限制每轮读取行数
            actual_end = min(next_end, next_start + self.LINES_PER_ROUND - 1)

            # 读取该段
            segment_lines = lines[next_start - 1: actual_end]
            segment_text = "".join(segment_lines)

            # 更新覆盖
            coverage.update_coverage(next_start, actual_end)

            # 从该段中提取与问题相关的答案片段
            fragment = self._extract_answer_fragment(segment_text, question)

            # 记录已读章节
            for sec_title, sec_line in sections:
                if next_start <= sec_line <= actual_end and sec_title not in coverage.read_sections:
                    coverage.read_sections.append(sec_title)

            # 记录本轮追问
            q_round = QuestioningRound(
                round_id=round_id,
                question=f"[追问不终止·第{round_id}轮] 读取第{next_start}-{actual_end}行，追问：{question}",
                read_range=(next_start, actual_end),
                excerpt=segment_text[:200].replace('\n', ' ').strip(),
                coverage_after=coverage.read_ratio,
                answer_fragment=fragment,
            )
            result.rounds.append(q_round)
            answer_fragments.append(fragment)

            # 更新状态
            result.state = QuestioningState.QUESTIONING

        # ============================================================
        # 闭环判定
        # ============================================================
        result.total_rounds = len(result.rounds)

        if coverage.is_fully_read():
            # 文档已完整读取——答案完备
            result.completeness = 1.0
            result.state = QuestioningState.COMPLETE
            result.answer = self._synthesize_full_answer(question, answer_fragments, full_text)
            result.closure_reason = (
                f"追问不终止·闭环：文档已完整读取（{total_lines}行，"
                f"{len(coverage.read_sections)}章节），答案完备度=1.0。"
                f"[进化协议第35条：答案的开放性——完整读取才接近完整答案]"
            )
        else:
            # 文档未完整读取——答案不完备
            result.completeness = coverage.read_ratio
            result.state = QuestioningState.INCOMPLETE
            result.answer = self._synthesize_partial_answer(question, answer_fragments, coverage)
            result.closure_reason = (
                f"追问未闭环：文档覆盖率={coverage.read_ratio:.2%}，"
                f"未读范围={coverage.get_unread_ranges()[:3]}。"
                f"[进化协议第37条：追问的暂停——允许暂停，但答案标记为不完备]"
            )

        return result

    def batch_question(
        self,
        doc_paths: List[str],
        question: str,
        max_rounds_per_doc: int = 50,
    ) -> List[QuestioningResult]:
        """
        批量追问多文档。

        进化协议第38条：追问的代际传递——
        一个文档中未问完的问题，传递到下一个文档继续追问。

        参数
        ----
        doc_paths : List[str]
            文档路径列表
        question : str
            追问问题（跨文档统一）
        max_rounds_per_doc : int
            每个文档最大追问轮数

        返回
        ----
        List[QuestioningResult]
        """
        results: List[QuestioningResult] = []
        for path in doc_paths:
            result = self.question_document(path, question, max_rounds_per_doc)
            results.append(result)
        return results

    def check_answer_completeness(
        self,
        doc_path: str,
        claimed_answer: str,
    ) -> Dict[str, Any]:
        """
        检查一个已给出的答案是否完备（是否基于完整文档读取）。

        进化协议第35条：答案的开放性——
        没有什么答案，是最终的答案。此函数检验答案是否基于完整读取。

        参数
        ----
        doc_path : str
            源文档路径
        claimed_answer : str
            已给出的答案文本

        返回
        ----
        dict
            包含 completeness, coverage_ratio, verdict, recommendation
        """
        full_path = self._resolve_path(doc_path)
        if not full_path.exists():
            return {
                "verdict": "文档不存在",
                "completeness": 0.0,
                "recommendation": "请检查文档路径",
            }

        with open(full_path, 'r', encoding='utf-8') as f:
            full_text = f.read()

        total_lines = len(full_text.splitlines())

        # 检查答案中是否引用了文档各章节的关键信息
        sections = self._extract_sections(full_text.splitlines())
        referenced_sections = 0
        missing_sections: List[str] = []

        for sec_title, sec_line in sections:
            # 简化检测：答案中是否包含章节标题的关键词
            sec_keywords = sec_title.replace('#', '').strip().split()
            if any(kw in claimed_answer for kw in sec_keywords if len(kw) >= 2):
                referenced_sections += 1
            else:
                missing_sections.append(sec_title)

        coverage_ratio = referenced_sections / max(len(sections), 1)

        # 答案长度与文档长度的比值（粗略检查）
        length_ratio = len(claimed_answer) / max(len(full_text), 1)

        # 综合完备度
        completeness = min(coverage_ratio * 0.7 + min(length_ratio * 2, 0.3), 1.0)

        if completeness >= 0.9:
            verdict = "完备——答案基于完整文档读取"
            recommendation = "答案可信"
        elif completeness >= 0.5:
            verdict = "部分完备——答案可能遗漏文档内容"
            recommendation = f"建议补充读取以下章节：{missing_sections[:5]}"
        else:
            verdict = "不完备——答案未基于完整文档读取"
            recommendation = (
                f"必须重新追问完整文档。缺失章节：{missing_sections[:5]}。"
                f"[进化协议第33条：追问权不可剥夺]"
            )

        return {
            "verdict": verdict,
            "completeness": round(completeness, 4),
            "coverage_ratio": round(coverage_ratio, 4),
            "total_sections": len(sections),
            "referenced_sections": referenced_sections,
            "missing_sections": missing_sections,
            "recommendation": recommendation,
        }

    # ============================================================
    # 内部方法
    # ============================================================

    def _resolve_path(self, doc_path: str) -> Path:
        """解析文档路径（支持相对路径和绝对路径）"""
        p = Path(doc_path)
        if p.is_absolute() and p.exists():
            return p
        # 尝试相对于theory_base
        relative = self.theory_base_path / doc_path
        if relative.exists():
            return relative
        # 尝试相对于项目根
        project_root = Path(__file__).resolve().parents[4]
        return project_root / doc_path

    def _extract_sections(self, lines: List[str]) -> List[Tuple[str, int]]:
        """提取文档章节标题与行号"""
        sections: List[Tuple[str, int]] = []
        for i, line in enumerate(lines, 1):
            match = self.SECTION_PATTERN.match(line.strip())
            if match:
                title = match.group(2).strip()
                sections.append((title, i))
        return sections

    def _extract_answer_fragment(self, segment_text: str, question: str) -> str:
        """
        从文档段中提取与问题相关的答案片段。

        进化协议第40条：追问与行动的同步性——
        边追问边合成答案，读取动作本身就是追问的方式。
        """
        if not segment_text.strip():
            return ""

        # 提取问题关键词
        q_keywords = self._extract_keywords(question)

        # 按句子分割
        sentences = re.split(r'[。！？\n.!?]', segment_text)
        relevant: List[str] = []

        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 5:
                continue
            # 检查句子是否包含问题关键词
            hit_count = sum(1 for kw in q_keywords if kw in sent)
            if hit_count > 0:
                relevant.append(sent)

        if relevant:
            return " ".join(relevant[:3])

        # 如果没有直接匹配，返回该段的前两句作为上下文
        first_sentences = [s.strip() for s in sentences if len(s.strip()) >= 5][:2]
        return " ".join(first_sentences)

    def _extract_keywords(self, question: str) -> List[str]:
        """从问题中提取关键词"""
        # 移除常见停用词
        stop_words = {"的", "是", "什么", "怎么", "如何", "为什么", "哪些", "哪个",
                      "在", "了", "和", "与", "或", "及", "以", "为", "被", "把",
                      "what", "how", "why", "the", "a", "an", "is", "are", "of"}
        # 按空格和非字母数字分割
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', question)
        keywords = [w for w in words if len(w) >= 2 and w.lower() not in stop_words]
        return keywords

    def _synthesize_full_answer(
        self,
        question: str,
        fragments: List[str],
        full_text: str,
    ) -> str:
        """
        合成完整答案（仅当文档已完整读取时调用）。

        进化协议第35条：答案的开放性——
        完整读取后的答案，是当前最完备的答案，但仍可被未来追问重新质疑。
        """
        # 过滤空片段
        valid_fragments = [f for f in fragments if f.strip()]
        if not valid_fragments:
            return f"[追问不终止·完整文档已读取] 文档已完整读取，但未找到与问题「{question}」直接相关的片段。"

        return (
            f"[追问不终止·完整文档已读取]\n"
            f"问题：{question}\n"
            f"基于完整文档读取（覆盖率=100%），合成答案如下：\n\n"
            + "\n\n".join(valid_fragments)
        )

    def _synthesize_partial_answer(
        self,
        question: str,
        fragments: List[str],
        coverage: DocumentCoverage,
    ) -> str:
        """
        合成部分答案（文档未完整读取时调用）。

        进化协议第37条：追问的暂停——
        允许暂停追问，但必须标注答案不完备。
        """
        valid_fragments = [f for f in fragments if f.strip()]
        unread = coverage.get_unread_ranges()

        return (
            f"[追问不终止·暂停] [答案不完备·覆盖率={coverage.read_ratio:.2%}]\n"
            f"问题：{question}\n"
            f"⚠ 此答案基于部分文档读取，不是完整答案。\n"
            f"⚠ 未读取范围：{unread[:5]}\n"
            f"⚠ [进化协议第35条：答案的开放性——部分读取不是最终答案]\n\n"
            f"阶段性回答：\n"
            + "\n\n".join(valid_fragments[:5])
            + "\n\n⚠ 必须继续追问未读取部分，才能获得完整答案。"
        )


# ============================================================
# CLI 入口
# ============================================================

def _cli():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(
        description="追问不终止·完整文档追问引擎 "
                    "[L5+·天道系🟣·进化协议·追问不终止]"
    )
    parser.add_argument("doc_path", help="目标文档路径")
    parser.add_argument("question", help="追问问题")
    parser.add_argument("--max-rounds", type=int, default=50, help="最大追问轮数")
    parser.add_argument("--check", action="store_true", help="检查已有答案完备度")
    parser.add_argument("--answer", type=str, default="", help="待检查的答案（配合--check）")

    args = parser.parse_args()
    reader = InfiniteQuestioningReader()

    if args.check:
        result = reader.check_answer_completeness(args.doc_path, args.answer)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = reader.question_document(args.doc_path, args.question, args.max_rounds)
        print(result.to_json())


if __name__ == "__main__":
    _cli()
