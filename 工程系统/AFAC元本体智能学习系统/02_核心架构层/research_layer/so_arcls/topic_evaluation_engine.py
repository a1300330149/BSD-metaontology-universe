"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第3条（科研价值边际判定公理）、第4条（选题创化生成机制）
对应九维维度：天道原理/天道动力学/创化社会/因果社会
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：θ_mv=0.005（边际判定阈值）, γ=0.92

SO-ARCLS - 自主选题与价值评估引擎
对应：科研价值边际判定公理 + 选题创化生成机制

核心职责：
1. 候选选题自动生成
2. 多维度价值量化评估
3. 选题差异化校验
4. 选题分级排序
5. 选题可行性预判

理论映射：
- TopicEvaluationEngine：对应选题创化生成机制（公理四）
- DEFAULT_VALUE_WEIGHTS：对应科研价值边际判定公理（公理三）
- _calc_*_value方法：对应科研价值边际判定公理（公理三）
- _check_topic_duplication：对应全局宿命边界统摄理论（公理六）
"""

import time
import random
from typing import Dict, List, Optional, Any

from .types import (
    TopicItem, ResearchTopicType, ValueDimension, ScienceDomain,
)


class TopicEvaluationEngine:
    """
    功能：自主选题与价值评估引擎
    理论映射：对应选题创化生成机制（公理四）、科研价值边际判定公理（公理三）
    """
    
    DEFAULT_VALUE_WEIGHTS = {
        ValueDimension.ACADEMIC.value: 0.3,
        ValueDimension.INNOVATION.value: 0.3,
        ValueDimension.INDUSTRY.value: 0.2,
        ValueDimension.FEASIBILITY.value: 0.2,
    }
    
    KNOWLEDGE_GAPS_TEMPLATES = {
        ScienceDomain.COMPUTER_VISION: [
            "基于{method}的{task}在{scenario}场景下的{problem}问题研究",
            "{method1}与{method2}融合的{task}方法改进",
            "{scenario}场景下{task}的{metric}指标提升研究",
            "{new_paradigm}范式在{task}中的创新性应用",
        ],
        ScienceDomain.NATURAL_LANGUAGE_PROCESSING: [
            "{task}任务中{specific_problem}问题的{method}解决方案",
            "{domain}领域{task}的{method}方法优化",
            "{method1}与{method2}结合的{task}创新方法",
            "{scenario}场景下{task}的{metric}提升研究",
        ],
        ScienceDomain.RECOMMENDATION_SYSTEM: [
            "{scenario}场景下{task}的{method}方法研究",
            "{problem}问题的{method}解决方案",
            "{method1}与{method2}融合的推荐算法优化",
            "{metric}指标提升的{task}方法创新",
        ],
        ScienceDomain.BIOINFORMATICS: [
            "{task}任务中{method}方法的{scenario}应用",
            "{problem}问题的{method}解决方案",
            "{method}在{domain}数据分析中的创新性应用",
            "{metric}指标提升的{task}方法研究",
        ],
        ScienceDomain.MATERIALS_SCIENCE: [
            "{material}材料{property}性能的{method}预测方法",
            "{method}在{material}材料设计中的应用",
            "{property}性能优化的{method}方法研究",
            "{scenario}场景下{material}材料的{method}设计",
        ],
        ScienceDomain.MACHINE_LEARNING: [
            "{task}任务中{method}的{problem}问题解决",
            "{method1}与{method2}结合的{task}创新",
            "{scenario}场景下{task}的{metric}提升",
            "{new_paradigm}在{task}中的应用研究",
        ],
    }
    
    METHODS = [
        "图神经网络", "深度学习", "强化学习", "迁移学习", "元学习",
        "注意力机制", "Transformer", "生成模型", "对比学习", "自监督学习",
        "联邦学习", "隐私保护机器学习", "知识图谱", "因果推断", "多模态学习",
    ]
    
    TASKS = {
        ScienceDomain.COMPUTER_VISION: ["图像分类", "目标检测", "图像分割", "图像生成", "图像检索"],
        ScienceDomain.NATURAL_LANGUAGE_PROCESSING: ["文本分类", "情感分析", "命名实体识别", "机器翻译", "文本生成"],
        ScienceDomain.RECOMMENDATION_SYSTEM: ["协同过滤", "序列推荐", "社交推荐", "跨域推荐", "可解释推荐"],
        ScienceDomain.BIOINFORMATICS: ["蛋白质结构预测", "基因表达分析", "药物发现", "疾病诊断", "序列分析"],
        ScienceDomain.MATERIALS_SCIENCE: ["材料性能预测", "材料设计", "相图预测", "缺陷检测", "结构优化"],
        ScienceDomain.MACHINE_LEARNING: ["分类", "回归", "聚类", "异常检测", "生成建模"],
    }
    
    SCENARIOS = ["真实世界", "工业", "医疗", "金融", "教育", "交通", "能源", "环境"]
    
    PROBLEMS = ["鲁棒性", "泛化能力", "可解释性", "效率", "数据稀缺", "隐私保护", "长尾分布"]
    
    METRICS = ["准确率", "F1值", "AUC", "MAE", "RMSE", "召回率", "NDCG", "MAP"]
    
    NEW_PARADIGMS = ["大模型", "多模态", "自主智能体", "神经符号AI", "具身智能"]
    
    def __init__(self):
        self.topic_counter = 0
    
    def generate_and_evaluate_topics(
        self,
        domain: ScienceDomain,
        topic_type: ResearchTopicType = ResearchTopicType.APPLIED,
        constraints: Optional[Dict] = None,
        num_topics: int = 10,
    ) -> List[TopicItem]:
        """
        生成并评估候选科研选题
        
        流程：知识缺口挖掘 → 候选选题生成 → 多维度价值评估 → 查重校验 → 排序输出
        
        Args:
            domain: 研究领域
            topic_type: 选题类型
            constraints: 约束条件（预算、周期等）
            num_topics: 生成选题数量
            
        Returns:
            List[TopicItem]: 评估后的选题列表（按综合得分降序）
        """
        print(f"\n[选题引擎] 开始生成{domain.value}领域的{topic_type.value}选题...")
        
        if constraints is None:
            constraints = {}
        
        # 挖掘目标领域的知识缺口与未解决问题
        knowledge_gaps = self._analyze_knowledge_gaps(domain, topic_type)
        print(f"[选题引擎] 挖掘到 {len(knowledge_gaps)} 个知识缺口")
        
        # 基于缺口生成候选选题池
        candidate_topics = self._generate_topics_from_gaps(knowledge_gaps, topic_type, num_topics)
        print(f"[选题引擎] 生成了 {len(candidate_topics)} 个候选选题")
        
        # 批量多维度价值评估
        evaluated_topics = []
        for topic in candidate_topics:
            # 四维价值打分
            scores = {
                ValueDimension.ACADEMIC.value: self._calc_academic_value(topic, domain),
                ValueDimension.INDUSTRY.value: self._calc_industry_value(topic, domain),
                ValueDimension.INNOVATION.value: self._calc_innovation_value(topic, domain),
                ValueDimension.FEASIBILITY.value: self._calc_feasibility(topic, domain, constraints),
            }
            
            # 查重校验
            duplicate_risk = self._check_topic_duplication(topic, domain)
            
            # 综合加权得分
            total_score = self._weighted_sum(scores, self.DEFAULT_VALUE_WEIGHTS)
            
            evaluated_topics.append(TopicItem(
                topic_id=self._generate_topic_id(),
                content=topic,
                domain=domain,
                topic_type=topic_type,
                value_scores=scores,
                total_score=total_score,
                duplicate_risk=duplicate_risk,
                expected_budget=self._estimate_budget(topic),
                expected_cycle=self._estimate_cycle(topic),
            ))
        
        # 按综合得分降序排序，过滤高重复风险选题
        evaluated_topics = [t for t in evaluated_topics if t.duplicate_risk < 0.3]
        evaluated_topics.sort(key=lambda x: x.total_score, reverse=True)
        
        print(f"[选题引擎] 筛选后剩余 {len(evaluated_topics)} 个选题")
        
        return evaluated_topics
    
    def _analyze_knowledge_gaps(self, domain: ScienceDomain, topic_type: ResearchTopicType) -> List[Dict]:
        """分析知识缺口"""
        gaps = []
        
        tasks = self.TASKS.get(domain, [])
        methods = self.METHODS
        scenarios = self.SCENARIOS
        problems = self.PROBLEMS
        
        for _ in range(8):
            gap = {
                "task": random.choice(tasks),
                "method": random.choice(methods),
                "scenario": random.choice(scenarios),
                "problem": random.choice(problems),
                "metric": random.choice(self.METRICS),
                "topic_type": topic_type.value,
            }
            gaps.append(gap)
        
        return gaps
    
    def _generate_topics_from_gaps(self, gaps: List[Dict], topic_type: ResearchTopicType,
                                   num_topics: int) -> List[str]:
        """基于知识缺口生成候选选题"""
        topics = []
        templates = self.KNOWLEDGE_GAPS_TEMPLATES.get(ScienceDomain.MACHINE_LEARNING,
                                                       self.KNOWLEDGE_GAPS_TEMPLATES[ScienceDomain.COMPUTER_VISION])
        
        for i in range(num_topics):
            gap = gaps[i % len(gaps)]
            template = random.choice(templates)
            
            method = gap["method"]
            method1 = random.choice(self.METHODS)
            method2 = random.choice([m for m in self.METHODS if m != method1])
            task = gap["task"]
            scenario = gap["scenario"]
            problem = gap["problem"]
            metric = gap["metric"]
            new_paradigm = random.choice(self.NEW_PARADIGMS)
            domain = gap["task"].split(" ")[0] if " " in gap["task"] else gap["task"]
            
            topic = template.format(
                method=method,
                method1=method1,
                method2=method2,
                task=task,
                scenario=scenario,
                problem=problem,
                metric=metric,
                new_paradigm=new_paradigm,
                domain=domain,
            )
            
            topics.append(topic)
        
        return topics
    
    def _calc_academic_value(self, topic: str, domain: ScienceDomain) -> float:
        """计算学术价值"""
        score = 0.5
        
        if any(keyword in topic for keyword in ["创新", "新方法", "新范式", "突破性"]):
            score += 0.2
        if any(method in topic for method in ["图神经网络", "Transformer", "大模型"]):
            score += 0.15
        if any(task in topic for task in ["预测", "分析", "检测"]):
            score += 0.1
        
        return min(1.0, score)
    
    def _calc_industry_value(self, topic: str, domain: ScienceDomain) -> float:
        """计算产业价值"""
        score = 0.4
        
        if any(scenario in topic for scenario in ["工业", "医疗", "金融", "交通"]):
            score += 0.3
        if any(keyword in topic for keyword in ["落地", "应用", "优化", "效率"]):
            score += 0.2
        
        return min(1.0, score)
    
    def _calc_innovation_value(self, topic: str, domain: ScienceDomain) -> float:
        """计算创新价值"""
        score = 0.4
        
        if "融合" in topic or "结合" in topic:
            score += 0.25
        if any(paradigm in topic for paradigm in self.NEW_PARADIGMS):
            score += 0.2
        if any(problem in topic for problem in ["鲁棒性", "泛化能力", "可解释性"]):
            score += 0.15
        
        return min(1.0, score)
    
    def _calc_feasibility(self, topic: str, domain: ScienceDomain, constraints: Dict) -> float:
        """计算可行性"""
        score = 0.6
        
        if any(keyword in topic for keyword in ["改进", "优化", "提升"]):
            score += 0.25
        if "深度学习" in topic or "图神经网络" in topic:
            score += 0.1
        
        budget_limit = constraints.get("max_budget", float('inf'))
        cycle_limit = constraints.get("max_cycle", float('inf'))
        
        estimated_budget = self._estimate_budget(topic)
        estimated_cycle = self._estimate_cycle(topic)
        
        if estimated_budget > budget_limit:
            score -= 0.2
        if estimated_cycle > cycle_limit:
            score -= 0.15
        
        return max(0.0, min(1.0, score))
    
    def _check_topic_duplication(self, topic: str, domain: ScienceDomain) -> float:
        """检查选题重复风险"""
        common_topics = [
            "深度学习", "神经网络", "机器学习", "分类", "回归",
            "预测", "分析", "检测", "识别",
        ]
        
        common_count = sum(1 for word in common_topics if word in topic)
        
        if common_count >= 3:
            return random.uniform(0.3, 0.5)
        elif common_count >= 2:
            return random.uniform(0.15, 0.3)
        else:
            return random.uniform(0.0, 0.15)
    
    def _weighted_sum(self, scores: Dict[ValueDimension, float],
                      weights: Dict[ValueDimension, float]) -> float:
        """加权求和"""
        total = 0.0
        for dimension, score in scores.items():
            total += score * weights.get(dimension, 0.25)
        return round(total, 4)
    
    def _generate_topic_id(self) -> str:
        """生成选题ID"""
        self.topic_counter += 1
        return f"topic_{int(time.time())}_{self.topic_counter:04d}"
    
    def _estimate_budget(self, topic: str) -> float:
        """估算预算（万元）"""
        base_budget = 5.0
        
        if "大模型" in topic or "多模态" in topic:
            base_budget += 10.0
        if "工业" in topic or "医疗" in topic:
            base_budget += 5.0
        if "优化" in topic or "改进" in topic:
            base_budget -= 2.0
        
        return round(base_budget, 1)
    
    def _estimate_cycle(self, topic: str) -> int:
        """估算周期（月）"""
        base_cycle = 6
        
        if "大模型" in topic or "多模态" in topic:
            base_cycle += 3
        if "创新" in topic:
            base_cycle += 2
        if "优化" in topic or "改进" in topic:
            base_cycle -= 2
        
        return max(3, base_cycle)


# 全局实例
_topic_engine = None

def get_topic_evaluation_engine() -> TopicEvaluationEngine:
    """获取选题评估引擎实例"""
    global _topic_engine
    if _topic_engine is None:
        _topic_engine = TopicEvaluationEngine()
    return _topic_engine


__all__ = [
    "TopicEvaluationEngine",
    "get_topic_evaluation_engine",
]
