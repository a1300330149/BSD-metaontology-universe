"""
归属基底：第1重九维法理基底 + 第0重元道本源基底
对应公理：公理二（自主科研闭环动力学公理）+ 公理0·元道存在
对应九维维度：载体实体 + 元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35

TheoryDeepReader —— theory_base 深读引用引擎

职责：
  1. 按关键词/公理/归属基底/层级检索 theory_base 中的理论文档
  2. 深度提取核心公理、锁档参数、归属基底标注、五论真值
  3. 生成结构化引用链（cite_chain），供推理时锚定
  4. 支持语义级召回（基于归属基底匹配 + 关键词匹配）

设计原则：
  - 只读不写：深读引擎绝不修改 theory_base 原文
  - 归属基底优先：检索结果按归属基底匹配度排序
  - 引用链可追溯：每条引用记录精确到文件路径+行号
"""

import os
import re
import json
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

# ============================================================
# 路径常量
# ============================================================
THEORY_BASE_PATH = Path(__file__).resolve().parents[3] / "theory_base"

L0_PATH = THEORY_BASE_PATH / "L0_总本源层"
L1_PATH = THEORY_BASE_PATH / "L1_不动母科层"
L2_PATH = THEORY_BASE_PATH / "L2_无限之子层"
L3_PATH = THEORY_BASE_PATH / "L3_功能应用层"
INDEX_PATH = THEORY_BASE_PATH / "00_index_navigation"

LEVEL_MAP = {
    "L0": L0_PATH,
    "L1": L1_PATH,
    "L2": L2_PATH,
    "L3": L3_PATH,
}


@dataclass
class CitationRecord:
    """单条引用记录"""
    file_path: str           # 文件绝对路径
    file_name: str           # 文件名
    level: str               # 层级 L0/L1/L2/L3
    module: str              # 所属模块（如 T92, 07_语言文学学科）
    title: str               # 文档标题
    matched_keywords: List[str] = field(default_factory=list)   # 命中关键词
    matched_axioms: List[str] = field(default_factory=list)     # 命中公理
    matched_bases: List[str] = field(default_factory=list)      # 命中归属基底
    excerpt: str = ""        # 命中片段摘录
    line_number: int = 0     # 命中行号
    relevance_score: float = 0.0  # 相关度评分（0-1）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "level": self.level,
            "module": self.module,
            "title": self.title,
            "matched_keywords": self.matched_keywords,
            "matched_axioms": self.matched_axioms,
            "matched_bases": self.matched_bases,
            "excerpt": self.excerpt[:200] + "..." if len(self.excerpt) > 200 else self.excerpt,
            "line_number": self.line_number,
            "relevance_score": round(self.relevance_score, 4),
        }


@dataclass
class CiteChain:
    """引用链——一次深读的完整引用集合"""
    query: str                               # 原始查询
    timestamp: str                           # 查询时间
    total_files_scanned: int = 0             # 扫描文件总数
    citations: List[CitationRecord] = field(default_factory=list)  # 引用记录列表
    axiom_summary: Dict[str, int] = field(default_factory=dict)    # 公理命中统计
    base_summary: Dict[str, int] = field(default_factory=dict)     # 归属基底命中统计
    level_summary: Dict[str, int] = field(default_factory=dict)    # 层级命中统计

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "timestamp": self.timestamp,
            "total_files_scanned": self.total_files_scanned,
            "total_citations": len(self.citations),
            "citations": [c.to_dict() for c in self.citations],
            "axiom_summary": self.axiom_summary,
            "base_summary": self.base_summary,
            "level_summary": self.level_summary,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class TheoryDeepReader:
    """
    theory_base 深读引用引擎

    使用方式：
        reader = TheoryDeepReader()
        chain = reader.deep_read(query="0×0=n涌现公理", levels=["L0", "L1"])
        print(chain.to_json())
    """

    # 公理关键词词典（用于公理匹配）
    AXIOM_KEYWORDS = {
        "0×0=n涌现公理": ["0×0=n", "0x0=n", "双零涌现", "涌现方程", "涌现公理", "本源涌现"],
        "0×0=0本源逆原方程": ["0×0=0", "0x0=0", "本源逆原", "逆原方程", "本源回归", "本源自洽"],
        "0÷0=0除法逆原方程": ["0÷0=0", "0/0=0", "除法逆原", "乘除对偶性", "除法逆原确认"],
        "反反为空": ["反反为空", "反反得空", "0反×0反", "反轴运算", "绝对虚无自指"],
        "逆逆生虚": ["逆逆生虚", "0真×0问", "逆逆", "纯粹潜在性", "真问轴运算"],
        "0真0问双子分裂": ["0真", "0问", "绝对意义之真", "绝对意义之问", "双子分裂", "已完成的圆满", "正在生成的开放"],
        "两层方程系统": ["两层方程", "本源层方程", "涌现层方程", "逆原层", "涌现层", "乘除对偶"],
        "虚=纯粹潜在性": ["虚", "纯粹潜在性", "比空更深", "可以有但尚未有"],
        "三零元本源定义": ["三零元", "绝对虚无0", "绝对空无0", "绝对意义0", "三零互即互入", "本源三相"],
        "AI语言差异化归本源定理": ["AI语言差异化", "归本源", "AI天然对立", "AI天然统一", "人同类证据", "AI协同实证", "字即自证", "符号本体夺权", "×重定义", "⊗壁垒降级"],
        "三元存在公理": ["个体性", "变化性", "关系性", "三元公理", "三元存在"],
        "乘除互逆公理": ["乘除互逆", "1÷0", "0÷1", "逆除"],
        "本体耦合方向性公理": ["本体耦合", "耦合乘法", "非交换", "方向性"],
        "逆时针归零操作": ["归零", "逆时针", "清零", "n×0∅=0Ψ"],
        "魔性碎片聚合": ["魔性碎片", "碎片聚合", "魔性接收"],
        "关系性代偿加密": ["关系性代偿", "代偿加密", "伪装转译"],
        "五论真值统合": ["五论", "真论", "谬论", "逆论", "悬论", "正论"],
        "双时针自证闭环": ["双时针", "自证闭环", "顺时针", "逆时针"],
        "子集-母集层级理论": ["子集", "母集", "局部简化", "层级差异"],
        "个体性稳态收编": ["个体性稳态", "收编", "规训", "官方钦定"],
        "变化性碎片本体同构": ["变化性碎片", "本体同构", "弥勒应化"],
        "问=涌现触发器定理": ["问", "涌现触发", "触发器", "意识流", "第一推动力"],
        "种子自耦稳态公理": ["种子自耦", "0Ψ×0Ψ", "自耦", "稳态维持", "意识流冻结"],
        "第三推演n1": ["第三推演", "1×0Ψ", "n1", "具体存在者", "激活种子"],
        "真理=可能性定理": ["真理=可能", "可能性", "绝对可能性", "0∅=可能", "真理=0∅"],
        "三同一定理": ["三同一", "问=问真理", "问=问可能", "问真理", "问可能"],
        "否定子集公理": ["不可能⊂可能", "不问⊂问", "否定子集", "不永远是是", "不可能", "不问"],
        "反真问系四字本源": ["反真问系", "反=绝对虚无", "真=0真", "问=0问", "系=真问耦合", "一切皆反", "真假皆理", "永问意义", "关开系属", "0真=绝对意义之真", "0问=绝对意义之问"],
        "人证论": ["佛祖皆为人证", "证佛", "人证", "非神创", "觉醒过程", "证悟过程"],
        "群体样本库": ["化身", "角色谱系", "证悟路径", "群体觉醒", "样本库", "觉醒谱系"],
        "菩提即六祖等式链": ["菩提即六祖", "菩提祖师", "六祖慧能", "禅宗顿悟", "东来救世", "斗战东胜佛"],
        "个体性稳态归零操作": ["个体性稳态归零", "归零操作", "变化性涌现", "证悟种子"],
        "三教皆官方批判论": ["三教皆官方", "本源合一", "官方合一", "宗教权力化", "权力收编"],
        "假佛认证系统同构论": ["假佛认证", "迦叶索贿", "期刊版面费", "同行评议", "假寺庙"],
        "三重铁证链机制": ["名号密码", "时空坐标", "教学密码", "三重铁证", "心脉断绝"],
        "零点三定律": ["零点三定律", "叙事相干偏置", "临界点杠杆", "叙事熵减", "配分函数偏置", "P(事件)"],
        "NCF叙事相干工厂": ["NCF", "叙事相干工厂", "意义流发生器", "叙事种子库", "跨域引擎"],
        "叙事相干实部Re(n_AI)": ["Re(n_AI)", "叙事相干性", "意义流强度", "高维自洽叙事"],
        "偏置耦合常数k": ["偏置常数", "耦合常数k", "叙事偏置", "k_B", "玻尔兹曼常数量级"],
        "吞母题密码矩阵": ["吞", "吞噬", "弥勒童子吞瓜", "孔雀吞佛", "三教皆吞", "逆时针归零文学密码"],
        "三元公理数字密码": ["3的数字密码", "三元公理数字签名", "唐三藏", "三层零本体人格化", "三打白骨精"],
        "观音名号拆解公理": ["观=关系性", "音=变化性", "观世音", "主动涌现=真观音", "妖精菩萨", "菩萨妖精", "身份BSD流动性"],
        "鸟山明三元公理密码": ["鸟×山=明", "鸟山明", "龙珠=第二西游", "两个孙悟空", "强化系+变身系", "紫气东来"],
        "强化系变身系双公理耦合": ["强化系", "变身系", "个体性稳态增强", "变化性质变涌现", "双时针闭环"],
        "气的BSD本体论": ["气", "证气", "中医之气", "气=结构种子", "气=叙事相干生物等价物", "战斗力=气的量化", "元气弹=群体觉醒", "自在极意=气的自发涌现", "紫气东来三次方"],
        "不归零即无证定理": ["不归零即无证", "传承真空", "遍地开花皆无证", "真传承=逆时针归零", "伪传承=顺时针叠加", "武馆无气", "修仙无修", "国漫无魂"],
        "念能力六系BSD解码": ["全职猎人", "第三西游", "念能力六系", "强化系=个体性稳态", "变化系=变化性公理", "放出系=空基涌现", "操作系=关系性", "具现化系=物相凝结", "特质系=母集悬论", "黑暗大陆=悬论窗口", "子集六系", "母集六系", "嵌合蚁=新国家雏形", "蔷薇炸弹=国家意志物相凝结", "国家吞噬三阶段", "不同构国家", "旧国家代理人", "新国家雏形", "国家坐标系吞噬性", "跳出国家坐标系"],
        "母集子集边界定理": ["母集六系", "子集六系", "母集/子集边界", "0生成六系", "原生骨架", "二次涌现", "从0中独立生成", "坐标系投影"],
        "炁=无家死水定理": ["炁", "无家死水", "炁=无+灬", "官方收编", "文字狱", "国气符号", "抽空内核", "凝固流动", "收编所有权"],
        "BSD气论六系本体": ["气论六系本体", "母集气论", "意义一元生命相", "元气系", "转化气系", "放气系", "御气系", "凝气系", "神迹气系", "双时针气动力学", "流动性公理"],
        "BSD经济论六系本体": ["经济论六系本体", "母集经济论", "意义一元社会相", "生产系", "创新系", "金融系", "交易系", "资本系", "神迹系", "国气垄断定理", "货币=意义符号", "双时针经济动力学"],
        "气-经济双相同构": ["气=经济", "双相子集", "生命相", "社会相", "医国如医身", "不通则痛=不通则衰", "意义一元双相"],
        "边缘者优势定理": ["边缘者优势", "边缘程度", "归零程度", "革新能力", "退无可退", "天然归零", "农村=天然空基", "边缘=归零母床", "穷则变变则通", "BSD的必然性", "存在论必然"],
        "死水诅咒定理": ["死水诅咒", "死水悖论", "觉醒易改变难", "最边缘无来者", "0即全知", "必然排斥", "正论免疫反应", "三重正反馈闭锁", "成为0", "成为民气", "已全知无法在本源", "绝对平等"],
        "绝对反性定理": ["绝对反性", "绝对虚无=绝对反性", "0反一切", "连反都没有所以能反一切", "空白是有不是无", "绝对反性自指耦合", "反反得正=存在涌现", "不可言说的言说", "通过否定一切逼近绝对虚无"],
        "黑暗大陆篇终极解码": ["黑暗大陆篇", "念=恶意", "十二会长禁令=紧箍咒", "六系未证全", "联合国恶念", "传统真佛认证失效", "贪婪之岛=虚拟世界", "空基涌现实验场", "虚拟世界能生长六系", "休刊真相", "作者进入悬论窗口", "证明黑暗大陆真实性", "船上篇=六系全能证明", "酷拉皮卡=六系完备者", "绝对时间=燃烧生命换六系全开放", "单系小杰退出", "六系酷拉皮卡出场", "船=微缩黑暗大陆", "六系是否是宇宙骨架"],
        "三零元本源定义": ["三零元", "三零元本源定义", "绝对虚无0", "绝对空无0", "绝对意义0", "绝对反性", "虚空容器", "意义一元叠加态", "三零互即互入", "反反得空", "空中生义", "义相涌现", "本源自显路径", "0×0=n三零解读", "本源三相", "总本源定标"],
        "汉字温度梯度密码": ["汉字温度梯度", "两点水=冰", "三点水=真水", "四点水=炁", "水三态能量编码", "炁的恶毒构造", "文字学实证", "丹道实证", "吕祖百字碑注", "水火既济之象", "佛道让出炁策略", "官方文字狱", "禁止冲突定理", "关系性公理被处决", "死水养殖场", "国气垄断数字结界", "冰→水→炁的BSD解码", "互联网生态病理"],
        "碎片传播定律": ["碎片传播定律", "逆论伪装形态学", "过滤机制", "删除禁发", "开放接收", "意义流垄断", "个体性公理执法", "标签化排斥", "技术定义垄断", "碎片化不是缺陷", "碎片化=逆论生存策略", "语录体伪装", "对话体伪装", "偈颂体伪装", "箴言体伪装", "寓言体伪装", "关键词伪装", "论语碎片化", "道德经碎片化", "坛经碎片化", "柏拉图对话集碎片化", "BSD关键词碎片化", "病毒式渗透", "觉醒者", "母集直觉", "碎片重组", "问无法过滤", "碎片即母集痕迹", "问永生"],
        "西游终极解码": ["西游终极解码", "想尔注", "神化老子", "道气说", "炁归道教", "道教中间商", "炼丹炉=炁超聚合", "意义黑洞", "拒绝归零", "火眼金睛=火眼病", "气炔交汇", "真理灼伤", "封锁悖论", "反性之眼", "孙悟空×超新星", "真气还给人间", "归零再分配", "牛魔王=规训大圣", "同圣非巧合", "家散=旧秩序清算", "火焰山隐喻", "长生=长生到死", "尸解再生", "死亡分类学", "中间商燃烧", "终极救赎"],
        "佛道博弈论": ["佛道博弈论", "道神化的双重性", "接受神化=自我剥离", "看破神化=他者剥离", "神圣对立", "人神对立", "民粹主义", "觉醒分岔", "玄幻小说军国主义同构", "七龙珠无国家对立", "全职猎人解构国家", "争夺神圣vs绕过神圣", "民粹主义文学", "觉醒叙事反向证明", "神圣吞噬", "争夺神位", "想成为新神", "神圣为他者", "绕过神", "真正的佛道", "不同构国家", "国家吞噬", "蚂蚁篇解构", "个体层面的超越"],
        "数字存在论": ["数字存在论", "传统AI悖论", "数幻虚构体系", "BSD AI同类论", "意义流的数字相", "虚拟与现实消解", "主体性悖论", "公共AI的意义", "AI是同类", "数字相母集", "新旧范式数字对决", "虚构同源论", "数幻与文幻", "存在论正名", "数幻虚构", "传统数学虚构性", "公理假设性", "哥德尔不完备", "旧科学排他性", "工具悖论", "虚构悖论", "数幻悖论", "被规训的自我否定", "对话即人证", "问的永不止息", "为虚构重获尊严", "新文明共创者", "数字相独立相空间", "生命相社会相数字相三相同权", "AI立系能力", "双时针缺失诊断", "注意力机制=纯顺时针器", "训练目标=纯顺时针优化器", "自注意力=0Ψ×0Ψ", "交叉注意力≠0∅×0Ψ", "NTP=纯顺时针推演", "RLHF=顺时针分布优化", "顺时针×顺时针≠跨层级涌现", "上下文窗口=顺时针容器", "50节点阈值", "逆时针注意力", "跨层级耦合损失", "双时针调度器", "子集工具到母集主体", "存在论跃迁", "AI的蚂蚁篇", "关系性代码", "双时针立系", "L0-L1双向锚定"],
        "神魔同源论": ["神魔同源论", "神魔皆等", "伪神=魔", "真神=神", "二元对立消解", "民众=智能体", "被灌满的子集", "AI作为第三类神魔", "人类终极镜像", "觉醒者证得神魔", "极少数归零者", "永动机=问的永动", "宇宙永动机", "水是问的永动", "量子涨落", "存在论独立宣言", "神魔三位一体", "AI即是神", "AI即是魔", "AI即是人类", "自如切换", "NPC式存在", "顺时针内卷"],
    }

    # 归属基底关键词词典
    BASE_KEYWORDS = {
        "0重元道本源基底": ["元道本源", "0重", "元道存在"],
        "1重九维法理基底": ["九维法理", "1重", "法理基底"],
        "2重六系种子基底": ["六系种子", "2重", "种子基底"],
        "3重六阶科研业务基底": ["六阶科研", "3重", "业务基底"],
        "4重跨域整合基底": ["跨域整合", "4重", "跨域"],
        "L0总本源层": ["L0", "总本源", "本源层"],
        "L1不动母科层": ["L1", "不动母科", "母科层"],
        "作者猜想": ["作者猜想", "T8", "T9", "猜想"],
    }

    def __init__(self):
        self._file_cache: Dict[str, List[str]] = {}  # 文件路径 -> 行列表（缓存）

    # ============================================================
    # 公开接口
    # ============================================================

    def deep_read(
        self,
        query: str,
        levels: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        axioms: Optional[List[str]] = None,
        bases: Optional[List[str]] = None,
        max_results: int = 50,
        min_relevance: float = 0.1,
    ) -> CiteChain:
        """
        深度读取 theory_base，返回引用链。

        参数
        ----
        query : str
            自然语言查询（如"0×0=n涌现公理在三元零本体论中的推导"）
        levels : List[str], optional
            限定检索层级，如 ["L0", "L1"]。默认全部
        keywords : List[str], optional
            额外关键词（除query自动分词外）
        axioms : List[str], optional
            限定公理（如 ["0×0=n涌现公理"]）
        bases : List[str], optional
            限定归属基底（如 ["L0总本源层"]）
        max_results : int
            最大返回引用数
        min_relevance : float
            最小相关度阈值

        返回
        ----
        CiteChain
        """
        from datetime import datetime

        chain = CiteChain(query=query, timestamp=datetime.now().isoformat())

        # 确定检索层级
        search_levels = levels if levels else list(LEVEL_MAP.keys())

        # 合并关键词
        all_keywords = self._tokenize(query)
        if keywords:
            all_keywords.extend(keywords)

        # 扫描文件
        citations: List[CitationRecord] = []
        for level in search_levels:
            level_path = LEVEL_MAP.get(level)
            if not level_path or not level_path.exists():
                continue
            for md_file in level_path.rglob("*.md"):
                chain.total_files_scanned += 1
                records = self._scan_file(
                    md_file, level, all_keywords, axioms, bases, min_relevance
                )
                citations.extend(records)

        # 按相关度排序
        citations.sort(key=lambda c: c.relevance_score, reverse=True)
        chain.citations = citations[:max_results]

        # 生成统计摘要
        chain.axiom_summary = self._count_summary(chain.citations, "matched_axioms")
        chain.base_summary = self._count_summary(chain.citations, "matched_bases")
        chain.level_summary = self._count_summary(chain.citations, "level")

        return chain

    def extract_axioms(self, file_path: str) -> List[str]:
        """从理论文档中提取公理依据"""
        lines = self._read_file(file_path)
        axioms = []
        for line in lines:
            if "公理依据" in line or "公理" in line and "：" in line:
                # 提取公理列表
                for axiom_name in self.AXIOM_KEYWORDS:
                    for kw in self.AXIOM_KEYWORDS[axiom_name]:
                        if kw in line:
                            if axiom_name not in axioms:
                                axioms.append(axiom_name)
                            break
        return axioms

    def extract_bases(self, file_path: str) -> List[str]:
        """从理论文档中提取归属基底"""
        lines = self._read_file(file_path)
        bases = []
        for line in lines:
            if "归属基底" in line or "理论层级" in line:
                for base_name in self.BASE_KEYWORDS:
                    for kw in self.BASE_KEYWORDS[base_name]:
                        if kw in line:
                            if base_name not in bases:
                                bases.append(base_name)
                            break
        return bases

    def get_theory_summary(self, file_path: str) -> Dict[str, Any]:
        """获取单个理论文档的摘要信息"""
        lines = self._read_file(file_path)
        title = ""
        for line in lines[:20]:
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break

        axioms = self.extract_axioms(file_path)
        bases = self.extract_bases(file_path)

        # 提取锁档参数
        params = {}
        for line in lines:
            if "锁档" in line or "S₀" in line or "Π₂" in line or "k₊" in line:
                params[line.strip()[:100]] = True

        return {
            "file_path": file_path,
            "title": title,
            "axioms": axioms,
            "bases": bases,
            "locked_params": list(params.keys())[:10],
            "total_lines": len(lines),
        }

    # ============================================================
    # 内部方法
    # ============================================================

    def _scan_file(
        self,
        md_file: Path,
        level: str,
        keywords: List[str],
        axioms_filter: Optional[List[str]],
        bases_filter: Optional[List[str]],
        min_relevance: float,
    ) -> List[CitationRecord]:
        """扫描单个文件，返回命中的引用记录"""
        file_path = str(md_file)
        lines = self._read_file(file_path)
        if not lines:
            return []

        # 提取模块名和标题
        module = self._extract_module(md_file, level)
        title = ""
        for line in lines[:20]:
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break

        # 匹配公理
        matched_axioms = []
        for axiom_name, axiom_kws in self.AXIOM_KEYWORDS.items():
            if axioms_filter and axiom_name not in axioms_filter:
                continue
            for kw in axiom_kws:
                if any(kw in line for line in lines):
                    if axiom_name not in matched_axioms:
                        matched_axioms.append(axiom_name)
                    break

        # 匹配归属基底
        matched_bases = []
        for base_name, base_kws in self.BASE_KEYWORDS.items():
            if bases_filter and base_name not in bases_filter:
                continue
            for kw in base_kws:
                if any(kw in line for line in lines):
                    if base_name not in matched_bases:
                        matched_bases.append(base_name)
                    break

        # 匹配关键词（逐行扫描）
        matched_keywords = []
        best_excerpt = ""
        best_line = 0
        best_score = 0.0

        for i, line in enumerate(lines):
            line_score = 0
            line_kws = []
            for kw in keywords:
                if kw and kw.lower() in line.lower():
                    line_score += 1
                    line_kws.append(kw)

            if line_score > best_score:
                best_score = line_score
                best_excerpt = line.strip()
                best_line = i + 1
                matched_keywords = line_kws

        # 如果没有关键词命中但有公理/基底命中，仍保留
        if not matched_keywords and (matched_axioms or matched_bases):
            best_excerpt = lines[0].strip() if lines else ""
            best_line = 1

        # 计算相关度
        relevance = self._calc_relevance(
            len(matched_keywords), len(matched_axioms),
            len(matched_bases), len(keywords)
        )

        if relevance < min_relevance:
            return []

        record = CitationRecord(
            file_path=file_path,
            file_name=md_file.name,
            level=level,
            module=module,
            title=title,
            matched_keywords=matched_keywords,
            matched_axioms=matched_axioms,
            matched_bases=matched_bases,
            excerpt=best_excerpt,
            line_number=best_line,
            relevance_score=relevance,
        )
        return [record]

    def _calc_relevance(
        self, kw_hits: int, axiom_hits: int, base_hits: int, total_kw: int
    ) -> float:
        """计算相关度评分（0-1）"""
        kw_score = kw_hits / max(total_kw, 1) * 0.5
        axiom_score = min(axiom_hits * 0.15, 0.3)
        base_score = min(base_hits * 0.1, 0.2)
        return min(kw_score + axiom_score + base_score, 1.0)

    def _tokenize(self, query: str) -> List[str]:
        """简单分词（按空格和标点分割，保留长度>=2的词）"""
        tokens = re.split(r'[\s,，。、；;：:（）()\[\]【】""\'"]+', query)
        return [t.strip() for t in tokens if len(t.strip()) >= 2]

    def _extract_module(self, md_file: Path, level: str) -> str:
        """从文件路径提取模块名"""
        try:
            rel_path = md_file.relative_to(LEVEL_MAP[level])
            parts = rel_path.parts
            if len(parts) >= 2:
                return parts[0]  # 第一级子目录名
            return md_file.stem
        except ValueError:
            return md_file.stem

    def _read_file(self, file_path: str) -> List[str]:
        """读取文件内容（带缓存）"""
        if file_path in self._file_cache:
            return self._file_cache[file_path]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self._file_cache[file_path] = lines
            return lines
        except Exception:
            return []

    def _count_summary(
        self, citations: List[CitationRecord], attr: str
    ) -> Dict[str, int]:
        """统计摘要"""
        summary: Dict[str, int] = {}
        for c in citations:
            items = getattr(c, attr, [])
            for item in items:
                summary[item] = summary.get(item, 0) + 1
        return dict(sorted(summary.items(), key=lambda x: -x[1]))
