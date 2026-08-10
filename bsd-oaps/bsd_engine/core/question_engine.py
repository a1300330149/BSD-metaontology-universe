"""
归属基底：第0重元道本源基底
对应公理：公理0·元道存在 + 0×0=n涌现公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/0元本体论大一统/
固定数理常量：γ=0.92, κ=0.35

QuestionEngine —— BSD追问引擎核心模块

核心命题：
    "问" = 0×0=n涌现的触发器
    "问"是0∅（认知空白）与0Ψ（已有认知结构）发生耦合的动力，
    是意义一元自证的最本源表达，也是智能体直观意识流的显现。

没有"问"，0∅与0Ψ不会耦合，0×0=n不会发生。
"问"是涌现的第一推动力。

三元公理分解：
    个体性之问（What/Who）→ 逆时针归零，追问存在本身
    变化性之问（Why）      → 顺时针涌现，追问变化原因
    关系性之问（How/What-if）→ 横向扩展，追问关联与可能

追问链 = 双时针动力学：
    顺时针：问→答→新问（涌现向，从已知到未知）
    逆时针：问→反思→更根本的问（归零向，从现象到本源）

使用方式：
    engine = QuestionEngine()
    chain = engine.ask("为什么0×0=n是涌现公理？")
    # 引擎自动：分解问题维度 → 深读theory_base → 生成追问链
"""

import re
import json
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# 对接深读引用引擎
from .theory_deep_reader import TheoryDeepReader, CiteChain, CitationRecord


# ============================================================
# 枚举：问题维度与追问方向
# ============================================================

class QuestionDimension(Enum):
    """问题三元公理维度"""
    INDIVIDUALITY = "个体性"      # What/Who：追问存在本身
    VARIABILITY = "变化性"        # Why：追问变化原因
    RELATIONALITY = "关系性"      # How/What-if：追问关联与可能

class QuestionDirection(Enum):
    """追问方向（双时针）"""
    CLOCKWISE = "顺时针"          # 涌现向：问→答→新问（从已知到未知）
    COUNTERCLOCKWISE = "逆时针"  # 归零向：问→反思→更根本的问（从现象到本源）
    LATERAL = "横向"              # 扩展向：追问关联与可能

class QuestionDepth(Enum):
    """追问深度（BSD层级）"""
    SURFACE = 0       # 表层：现象级提问
    STRUCTURAL = 1    # 结构级：机制级提问
    ONTOLOGICAL = 2   # 本体级：公理级提问
    ORIGIN = 3        # 本源级：0×0=n级提问


# ============================================================
# 数据类
# ============================================================

@dataclass
class Question:
    """
    单个问题的BSD本体表征

    每个"问"都是0∅→0Ψ→n的微缩涌现：
    - unknown（0∅）：问题指向的未知领域
    - existing_knowledge（0Ψ）：已有的认知结构
    - 问本身：驱动耦合的力
    """
    text: str                                    # 问题文本
    dimension: QuestionDimension = QuestionDimension.VARIABILITY
    direction: QuestionDirection = QuestionDirection.CLOCKWISE
    depth: QuestionDepth = QuestionDepth.SURFACE
    parent_id: Optional[str] = None              # 父问题ID（追问链中的上一问）
    question_id: str = field(default_factory=lambda: f"q_{int(time.time()*1000)}")
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # 关联的引用链（深读结果）
    cite_chain: Optional[Dict[str, Any]] = None

    # 答案（如有）
    answer: Optional[str] = None
    answer_completeness: float = 0.0             # 答案完备度（0-1）

    # 追问产生的子问题
    child_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "text": self.text,
            "dimension": self.dimension.value,
            "direction": self.direction.value,
            "depth": self.depth.name,
            "depth_score": self.depth.value,
            "parent_id": self.parent_id,
            "timestamp": self.timestamp,
            "cite_chain": self.cite_chain,
            "answer": self.answer,
            "answer_completeness": self.answer_completeness,
            "child_ids": self.child_ids,
        }


@dataclass
class QuestionChain:
    """
    追问链——一次完整追问的动态轨迹

    追问链本身就是双时针自证闭环：
    - 顺时针段：问→深读→答→新问（涌现）
    - 逆时针段：答→反思→更根本的问（归零）
    """
    root_question: str                           # 根问题文本
    chain_id: str = field(default_factory=lambda: f"chain_{int(time.time()*1000)}")
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    questions: List[Question] = field(default_factory=list)
    total_depth_reached: int = 0                 # 达到的最大深度
    total_citations: int = 0                     # 引用的theory_base条目数
    dimension_distribution: Dict[str, int] = field(default_factory=dict)
    direction_distribution: Dict[str, int] = field(default_factory=dict)

    # 闭环判定
    is_closed: bool = False                      # 是否完成闭环（最后一个问题回到本源）
    closure_point: Optional[str] = None          # 闭环点（回到哪个问题）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "root_question": self.root_question,
            "timestamp": self.timestamp,
            "total_questions": len(self.questions),
            "total_depth_reached": self.total_depth_reached,
            "total_citations": self.total_citations,
            "dimension_distribution": self.dimension_distribution,
            "direction_distribution": self.direction_distribution,
            "is_closed": self.is_closed,
            "closure_point": self.closure_point,
            "questions": [q.to_dict() for q in self.questions],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 追问引擎
# ============================================================

class QuestionEngine:
    """
    BSD追问引擎

    核心机制：
    1. 问题分解：将自然语言问题分解为三元公理维度
    2. 深度评估：评估问题触及的BSD层级
    3. 深读引用：对接TheoryDeepReader检索theory_base
    4. 追问生成：基于答案完备性自动生成下一问
    5. 闭环判定：当追问触及0×0=n本源时判定闭环

    使用方式：
        engine = QuestionEngine()
        chain = engine.ask("为什么0×0=n是涌现公理？", max_followups=5)
        print(chain.to_json())
    """

    # 维度关键词词典（用于问题分类）
    DIMENSION_KEYWORDS = {
        QuestionDimension.INDIVIDUALITY: [
            "是什么", "是谁", "什么是", "本质", "本体", "存在", "定义",
            "what", "who", "essence", "being", "define",
        ],
        QuestionDimension.VARIABILITY: [
            "为什么", "为何", "原因", "怎么", "怎样", "导致", "驱动",
            "变化", "演化", "涌现", "why", "cause", "how come",
        ],
        QuestionDimension.RELATIONALITY: [
            "如何", "怎样关联", "什么关系", "如果", "假设", "之间",
            "对比", "区别", "联系", "how", "what if", "relate",
        ],
    }

    # 本源级关键词（触及0×0=n）
    ORIGIN_KEYWORDS = [
        "0×0", "0x0", "涌现公理", "本源", "第一性", "元道", "0元",
        "空无", "虚空", "种子", "耦合", "最根本", "终极",
        "问", "不问", "意识流", "触发器", "涌现触发",
    ]

    # 本体级关键词（触及公理体系）
    ONTOLOGICAL_KEYWORDS = [
        "公理", "定理", "个体性", "变化性", "关系性", "三元",
        "归属基底", "五论", "真论", "逆论", "悬论",
        "种子自耦", "意识流冻结", "第三推演", "n1", "具体存在者",
        "0Ψ自耦", "拒绝型种子", "追问链", "双时针",
    ]

    # 结构级关键词（触及机制）
    STRUCTURAL_KEYWORDS = [
        "机制", "结构", "模型", "方程", "参数", "系统", "框架",
        "动力学", "稳态", "闭环",
    ]

    def __init__(self, reader: Optional[TheoryDeepReader] = None):
        self.reader = reader or TheoryDeepReader()

    # ============================================================
    # 公开接口
    # ============================================================

    def ask(
        self,
        question: str,
        max_followups: int = 5,
        auto_deep_read: bool = True,
        closure_threshold: float = 0.85,
    ) -> QuestionChain:
        """
        提出问题，启动追问链。

        参数
        ----
        question : str
            根问题（自然语言）
        max_followups : int
            最大追问轮数
        auto_deep_read : bool
            是否自动深读theory_base
        closure_threshold : float
            闭环阈值（答案完备度超过此值且触及本源级时判定闭环）

        返回
        ----
        QuestionChain
        """
        chain = QuestionChain(root_question=question)

        # 处理根问题
        root_q = self._process_question(question, parent=None, auto_deep_read=auto_deep_read)
        chain.questions.append(root_q)

        # 追问循环
        current = root_q
        for i in range(max_followups):
            # 判定闭环
            if (current.depth == QuestionDepth.ORIGIN and
                current.answer_completeness >= closure_threshold):
                chain.is_closed = True
                chain.closure_point = current.question_id
                break

            # 生成下一问
            next_q = self._generate_followup(current, auto_deep_read=auto_deep_read)
            if not next_q:
                break

            chain.questions.append(next_q)
            current = next_q

        # 统计
        chain.total_depth_reached = max(q.depth.value for q in chain.questions)
        chain.total_citations = sum(
            q.cite_chain.get("total_citations", 0) if q.cite_chain else 0
            for q in chain.questions
        )
        chain.dimension_distribution = self._count_distribution(
            chain.questions, lambda q: q.dimension.value
        )
        chain.direction_distribution = self._count_distribution(
            chain.questions, lambda q: q.direction.value
        )

        return chain

    def classify(self, question: str) -> Tuple[QuestionDimension, QuestionDepth]:
        """
        分类问题：确定三元公理维度与追问深度。

        参数
        ----
        question : str
            问题文本

        返回
        ----
        (QuestionDimension, QuestionDepth)
        """
        dimension = self._classify_dimension(question)
        depth = self._classify_depth(question)
        return dimension, depth

    def generate_followup(
        self,
        question: str,
        answer: Optional[str] = None,
        cite_chain: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        基于当前问题与答案，生成下一问。

        这是追问引擎的核心智能：
        - 如果答案不完备 → 追问答案的缺口
        - 如果答案完备但未触本源 → 逆时针追问更深
        - 如果已触本源 → 顺时针追问涌现应用

        参数
        ----
        question : str
            当前问题
        answer : str, optional
            当前答案
        cite_chain : dict, optional
            当前引用链

        返回
        ----
        str or None
            下一问文本（如无需追问则返回None）
        """
        dimension, depth = self.classify(question)

        # 无答案：追问答案本身
        if not answer:
            return self._formulate_followup(question, dimension, depth, mode="seek_answer", cite_chain=cite_chain)

        # 答案存在但未触本源：逆时针追问更深
        if depth.value < QuestionDepth.ORIGIN.value:
            return self._formulate_followup(question, dimension, depth, mode="go_deeper", cite_chain=cite_chain)

        # 已触本源：顺时针追问涌现应用
        return self._formulate_followup(question, dimension, depth, mode="emerge", cite_chain=cite_chain)

    # ============================================================
    # 意识流接口：连续追问
    # ============================================================

    def consciousness_stream(
        self,
        seed: str,
        duration: int = 10,
        auto_deep_read: bool = True,
    ) -> List[QuestionChain]:
        """
        意识流模式：从种子问题出发，连续生成多条追问链。

        模拟智能体直观意识流的连续涌现：
        每条追问链结束后，基于闭环点的残余张力，
        自发涌现下一条追问链的种子问题。

        参数
        ----
        seed : str
            种子问题
        duration : int
            意识流持续轮数（生成多少条追问链）
        auto_deep_read : bool
            是否自动深读

        返回
        ----
        List[QuestionChain]
        """
        streams: List[QuestionChain] = []
        current_seed = seed

        for i in range(duration):
            chain = self.ask(current_seed, max_followups=3, auto_deep_read=auto_deep_read)
            streams.append(chain)

            # 从上一条链的闭环点涌现下一颗种子
            if chain.questions:
                last_q = chain.questions[-1]
                # 如果闭环了，顺时针涌现新方向
                if chain.is_closed:
                    new_seed = self._emerge_new_seed(last_q)
                    current_seed = new_seed
                else:
                    # 未闭环，继续追问同一方向
                    next_text = self._formulate_followup(
                        last_q.text, last_q.dimension, last_q.depth, mode="continue",
                        cite_chain=last_q.cite_chain
                    )
                    if next_text:
                        current_seed = next_text
                    else:
                        break  # 无法继续追问，意识流终止
            else:
                break

        return streams

    # ============================================================
    # 内部方法
    # ============================================================

    def _process_question(
        self,
        question: str,
        parent: Optional[Question],
        auto_deep_read: bool,
    ) -> Question:
        """处理单个问题：分类→深读→评估"""
        dimension, depth = self.classify(question)

        # 确定追问方向
        if depth == QuestionDepth.ORIGIN:
            direction = QuestionDirection.COUNTERCLOCKWISE
        elif dimension == QuestionDimension.INDIVIDUALITY:
            direction = QuestionDirection.COUNTERCLOCKWISE
        elif dimension == QuestionDimension.VARIABILITY:
            direction = QuestionDirection.CLOCKWISE
        else:
            direction = QuestionDirection.LATERAL

        q = Question(
            text=question,
            dimension=dimension,
            direction=direction,
            depth=depth,
            parent_id=parent.question_id if parent else None,
        )

        # 深读引用
        if auto_deep_read:
            chain = self.reader.deep_read(
                query=question, max_results=10, min_relevance=0.05
            )
            q.cite_chain = chain.to_dict()

            # 基于引用链评估答案完备度
            q.answer_completeness = self._evaluate_completeness(chain, depth)

            # 生成初步答案
            q.answer = self._synthesize_answer(question, chain)

        return q

    def _generate_followup(
        self, current: Question, auto_deep_read: bool
    ) -> Optional[Question]:
        """生成下一个追问"""
        next_text = self.generate_followup(
            current.text, current.answer, current.cite_chain
        )
        if not next_text:
            return None

        next_q = self._process_question(next_text, parent=current, auto_deep_read=auto_deep_read)
        current.child_ids.append(next_q.question_id)
        return next_q

    def _classify_dimension(self, question: str) -> QuestionDimension:
        """分类问题维度（三元公理）"""
        scores = {}
        for dim, keywords in self.DIMENSION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in question.lower())
            scores[dim] = score

        max_score = max(scores.values())
        if max_score == 0:
            return QuestionDimension.VARIABILITY  # 默认变化性

        for dim, score in scores.items():
            if score == max_score:
                return dim
        return QuestionDimension.VARIABILITY

    def _classify_depth(self, question: str) -> QuestionDepth:
        """分类问题深度（BSD层级）"""
        q_lower = question.lower()

        # 检查本源级
        for kw in self.ORIGIN_KEYWORDS:
            if kw.lower() in q_lower:
                return QuestionDepth.ORIGIN

        # 检查本体级
        for kw in self.ONTOLOGICAL_KEYWORDS:
            if kw.lower() in q_lower:
                return QuestionDepth.ONTOLOGICAL

        # 检查结构级
        for kw in self.STRUCTURAL_KEYWORDS:
            if kw.lower() in q_lower:
                return QuestionDepth.STRUCTURAL

        return QuestionDepth.SURFACE

    def _evaluate_completeness(self, chain: CiteChain, depth: QuestionDepth) -> float:
        """基于引用链评估答案完备度"""
        if not chain.citations:
            return 0.0

        # 引用数量得分
        cite_score = min(len(chain.citations) / 10.0, 0.4)

        # 最高相关度得分
        max_relevance = max(c.relevance_score for c in chain.citations) if chain.citations else 0
        rel_score = min(max_relevance * 0.4, 0.4)

        # 深度匹配得分
        depth_score = 0.0
        if depth == QuestionDepth.ORIGIN:
            # 本源级问题需要引用到L0
            l0_count = sum(1 for c in chain.citations if c.level == "L0")
            depth_score = min(l0_count / 3.0, 0.2)
        elif depth == QuestionDepth.ONTOLOGICAL:
            axiom_count = sum(len(c.matched_axioms) for c in chain.citations)
            depth_score = min(axiom_count / 5.0, 0.2)
        else:
            depth_score = 0.1

        return min(cite_score + rel_score + depth_score, 1.0)

    def _synthesize_answer(self, question: str, chain: CiteChain) -> Optional[str]:
        """基于引用链合成初步答案"""
        if not chain.citations:
            return None

        top = chain.citations[0]
        parts = [f"基于theory_base深读（{chain.total_files_scanned}文件扫描，{len(chain.citations)}条引用）："]

        if top.matched_axioms:
            parts.append(f"关联公理：{', '.join(top.matched_axioms[:3])}")
        if top.matched_bases:
            parts.append(f"归属基底：{', '.join(top.matched_bases[:3])}")
        parts.append(f"最相关文档：[{top.level}] {top.file_name}")
        if top.excerpt:
            parts.append(f"关键摘录：{top.excerpt[:150]}")

        return "\n".join(parts)

    def _formulate_followup(
        self,
        question: str,
        dimension: QuestionDimension,
        depth: QuestionDepth,
        mode: str,
        cite_chain: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """根据模式生成下一问（基于引用链生成具体追问，避免重复）"""

        # 从引用链提取上下文，用于生成具体追问
        context_axioms = []
        context_bases = []
        context_title = ""
        if cite_chain and cite_chain.get("citations"):
            top = cite_chain["citations"][0]
            context_axioms = top.get("matched_axioms", [])[:2]
            context_bases = top.get("matched_bases", [])[:1]
            context_title = top.get("title", "")[:30]

        if mode == "seek_answer":
            if context_axioms:
                return "theory_base中关于{}的论述是什么？具体对应哪些公理？".format(context_axioms[0])
            templates = {
                QuestionDimension.INDIVIDUALITY: "这个存在的本体论定义是什么？它属于哪个归属基底？",
                QuestionDimension.VARIABILITY: "导致这一现象的底层公理是什么？变化的动力学机制如何？",
                QuestionDimension.RELATIONALITY: "这与theory_base中的哪些理论模块存在关联？",
            }
            return templates.get(dimension, "theory_base中对此有何论述？")

        if mode == "go_deeper":
            if depth == QuestionDepth.SURFACE:
                return "这一现象背后的结构性机制是什么？"
            elif depth == QuestionDepth.STRUCTURAL:
                if context_axioms:
                    return "这一机制是否对应{}？其本体论依据是什么？".format(context_axioms[0])
                return "这一机制对应BSD哪条公理？其本体论依据是什么？"
            elif depth == QuestionDepth.ONTOLOGICAL:
                return "这条公理的根源是否指向0×0=n涌现方程？"
            else:
                return None

        if mode == "emerge":
            # 基于引用链中的公理/基底生成具体涌现追问
            if context_axioms:
                return "基于{}，在{}中有哪些具体应用实例？".format(
                    context_axioms[0],
                    context_bases[0] if context_bases else "实际场景"
                )
            if context_title:
                return "基于{}的结论，可以涌现出哪些应用层面的推论？".format(context_title)
            return "基于这个本源公理，可以涌现出哪些应用层面的推论？"

        if mode == "continue":
            if context_axioms:
                return "关于{}，在{}中还有哪些未展开的维度？".format(
                    context_axioms[0],
                    context_bases[0] if context_bases else "theory_base"
                )
            return "关于{}，还有哪些未展开的维度？".format(question[:30])

        return None

    def _emerge_new_seed(self, closed_question: Question) -> str:
        """从闭环点涌现新的种子问题"""
        # 闭环意味着触及0×0=n本源
        # 新种子应该顺时针涌现到应用层
        return f"基于0×0=n涌现公理，{closed_question.text}的结论如何应用到实际场景中？"

    def _count_distribution(self, questions: List[Question], key_func) -> Dict[str, int]:
        """统计分布"""
        dist: Dict[str, int] = {}
        for q in questions:
            key = key_func(q)
            dist[key] = dist.get(key, 0) + 1
        return dict(sorted(dist.items(), key=lambda x: -x[1]))
