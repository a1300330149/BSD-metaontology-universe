"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第2条（全域九维法理公理）、第4条（选题创化生成机制）、第5条（成果落地转化范式）、第6条（全局宿命边界统摄理论）、第7条（系统自进化迭代公理）
对应九维维度：天道原理/天道动力学/创化社会/因果社会/道心能级
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, κ=0.35, θ_mv=0.005, θ_evo=0.002

SO-ARCLS - 六阶自主科研闭环系统
Sixth-Order Autonomous Research Closed-Loop System

阶段定位：整套自动科研系统的「顶层闭环层」，实现"选题→规划→实验→成果→落地→复盘→进化"的完整自主闭环

理论映射：
- ScienceDomain枚举：对应三界维度秩序公理（公理三）
- ResearchTopicType枚举：对应选题创化生成机制（公理四）
- ProjectStatus枚举：对应自主科研闭环动力学公理（公理二）
- ValueDimension枚举：对应科研价值边际判定公理（公理三）
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple


# ============================================================================
# 全局核心数理参数（锁档固定，禁止修改）
# ============================================================================
# 理论依据：《V3.0元本体理论分册》第二章 九维法理基底
# 参数来源：四位一体驻波动力学框架锁档版本（SHA256: e62f918340dc2975108294736ac8927d90584136972485931027958740925713）

class CoreParameters:
    """
    功能：全局核心数理参数定义与校验
    理论映射：规则相位位（第二位）·全域道运流转规则
    约束来源：三重具现转化公理
    禁止修改：以下参数为锁档核心，修改会破坏理论闭环
    """
    
    # 三阶变身阈值（对应公理二：全域九维法理公理）
    E1 = 0.35  # 一阶变身阈值（肉身能级）
    E2 = 0.65  # 二阶变身阈值（精神能级）
    E3 = 0.90  # 三阶变身阈值（道心能级）
    
    # 时序衰减系数（对应公理二：全域九维法理公理）
    GAMMA = 0.92  # γ = 0.92，衰减系数
    
    # 耦合强度系数（对应公理二：全域九维法理公理）
    KAPPA = 0.35  # κ = 0.35，耦合强度
    
    # 稀疏补偿系数（对应公理二：全域九维法理公理）
    ALPHA = 0.18  # α = 0.18，稀疏补偿
    
    # 边际判定阈值（对应公理三：科研价值边际判定公理）
    THETA_MV = 0.005  # θ_mv = 0.005，边际判定阈值
    
    # 自进化增量（对应公理七：系统自进化迭代公理）
    THETA_EVO = 0.002  # θ_evo = 0.002，自进化增量
    
    # 负迁移阈值（对应公理六：全局宿命边界统摄理论）
    THETA_NEG = 0.02  # θ_neg = 0.02，负迁移阈值
    
    # 成果质量校验阈值
    QUALITY_THRESHOLD = 0.8
    
    # 最大迭代次数
    MAX_RETRY = 3
    
    @classmethod
    def validate_parameters(cls):
        """
        功能：校验核心参数是否被篡改
        理论映射：全局宿命边界统摄理论（公理六）
        约束来源：锁档核心参数完整性校验
        """
        expected_values = {
            'E1': 0.35,
            'E2': 0.65,
            'E3': 0.90,
            'GAMMA': 0.92,
            'KAPPA': 0.35,
            'ALPHA': 0.18,
            'THETA_MV': 0.005,
            'THETA_EVO': 0.002,
            'THETA_NEG': 0.02,
            'QUALITY_THRESHOLD': 0.8,
            'MAX_RETRY': 3,
        }
        
        violations = []
        for param_name, expected in expected_values.items():
            actual = getattr(cls, param_name)
            if actual != expected:
                violations.append(f"{param_name}: expected {expected}, got {actual}")
        
        if violations:
            raise RuntimeError(
                f"核心参数完整性校验失败！以下参数被篡改:\n"
                f"{chr(10).join(violations)}\n"
                f"请检查并恢复锁档参数值。"
            )
        
        return True
    
    @classmethod
    def get_parameter_summary(cls) -> Dict[str, float]:
        """获取核心参数汇总"""
        return {
            'E1': cls.E1,
            'E2': cls.E2,
            'E3': cls.E3,
            'γ': cls.GAMMA,
            'κ': cls.KAPPA,
            'α': cls.ALPHA,
            'θ_mv': cls.THETA_MV,
            'θ_evo': cls.THETA_EVO,
            'θ_neg': cls.THETA_NEG,
            'QUALITY_THRESHOLD': cls.QUALITY_THRESHOLD,
            'MAX_RETRY': cls.MAX_RETRY,
        }


# 参数校验（模块加载时自动执行）
CoreParameters.validate_parameters()


# ============================================================================
# 全局枚举定义
# ============================================================================

class ResearchTopicType(Enum):
    """
    功能：科研选题类型枚举
    理论映射：对应选题创化生成机制（公理四）
    """
    BASIC = "basic_research"
    APPLIED = "applied_research"
    ENGINEERING = "engineering_opt"
    CROSS = "cross_innovation"


class ProjectStatus(Enum):
    """
    功能：项目全生命周期状态枚举
    理论映射：对应自主科研闭环动力学公理（公理二）
    """
    TOPIC_EVAL = "topic_evaluation"
    PLANNING = "planning"
    EXECUTING = "executing"
    OUTPUT = "result_output"
    LANDING = "landing_transform"
    REVIEW = "retrospective"
    FINISHED = "finished"
    FAILED = "failed"


class ValueDimension(Enum):
    """
    功能：选题价值评估维度枚举
    理论映射：对应科研价值边际判定公理（公理三）
    """
    ACADEMIC = "academic_value"
    INDUSTRY = "industry_value"
    INNOVATION = "innovation_value"
    FEASIBILITY = "feasibility"


class AutoMode(Enum):
    """
    功能：自主运行模式枚举
    理论映射：对应全局宿命边界统摄理论（公理六）
    """
    FULL_AUTO = "full_autonomous"
    SEMI_AUTO = "semi_autonomous"
    HUMAN_LOOP = "human_in_loop"


class ScienceDomain(Enum):
    """
    功能：科学领域枚举
    理论映射：对应三界维度秩序公理（公理三）
    """
    COMPUTER_VISION = "computer_vision"
    NATURAL_LANGUAGE_PROCESSING = "natural_language_processing"
    RECOMMENDATION_SYSTEM = "recommendation_system"
    BIOINFORMATICS = "bioinformatics"
    MATERIALS_SCIENCE = "materials_science"
    MACHINE_LEARNING = "machine_learning"
    DATA_MINING = "data_mining"
    ROBOTICS = "robotics"
    CYBER_SECURITY = "cyber_security"


# ============================================================================
# 核心数据类型
# ============================================================================

class TopicItem:
    """
    功能：选题项数据结构
    理论映射：对应选题创化生成机制（公理四）
    """
    def __init__(self, topic_id: str, content: str, domain: ScienceDomain,
                 topic_type: ResearchTopicType, value_scores: Dict[ValueDimension, float],
                 total_score: float, duplicate_risk: float,
                 expected_budget: float = 0.0, expected_cycle: int = 0):
        self.topic_id = topic_id
        self.content = content
        self.domain = domain
        self.topic_type = topic_type
        self.value_scores = value_scores
        self.total_score = total_score
        self.duplicate_risk = duplicate_risk
        self.expected_budget = expected_budget
        self.expected_cycle = expected_cycle


class ResearchPlan:
    """
    功能：科研计划数据结构
    理论映射：对应科研动力学公理（公理五）
    """
    def __init__(self, plan_id: str, topic_item: TopicItem, phases: List[Dict],
                 resource_allocation: Dict, milestones: List[Dict], risks: List[Dict]):
        self.plan_id = plan_id
        self.topic_item = topic_item
        self.phases = phases
        self.resource_allocation = resource_allocation
        self.milestones = milestones
        self.risks = risks


class Project:
    """
    功能：科研项目数据结构
    理论映射：对应自主科研闭环动力学公理（公理二）
    """
    def __init__(self, project_id: str, topic_item: TopicItem, plan: ResearchPlan,
                 status: ProjectStatus, auto_mode: AutoMode,
                 execution_history: List[Dict] = None, artifacts: Dict = None):
        self.project_id = project_id
        self.topic_item = topic_item
        self.plan = plan
        self.status = status
        self.auto_mode = auto_mode
        self.execution_history = execution_history or []
        self.artifacts = artifacts or {}


class ExecutionRecord:
    """
    功能：执行记录数据结构
    理论映射：对应科研动力学公理（公理五）
    """
    def __init__(self, step_id: str, phase: str, action: str,
                 timestamp: float, status: str, result: Any = None,
                 error: str = None):
        self.step_id = step_id
        self.phase = phase
        self.action = action
        self.timestamp = timestamp
        self.status = status
        self.result = result
        self.error = error


class EvaluationReport:
    """
    功能：评估报告数据结构
    理论映射：对应成果落地转化范式（公理五）
    """
    def __init__(self, project_id: str, metrics: Dict[str, float],
                 conclusions: List[str], recommendations: List[str],
                 success_rate: float, lessons_learned: List[str]):
        self.project_id = project_id
        self.metrics = metrics
        self.conclusions = conclusions
        self.recommendations = recommendations
        self.success_rate = success_rate
        self.lessons_learned = lessons_learned


class LandingResult:
    """
    功能：落地成果数据结构
    理论映射：对应成果落地转化范式（公理五）
    """
    def __init__(self, project_id: str, landing_type: str,
                 artifacts: List[str], transformation_report: str,
                 commercial_value: float, impact_score: float):
        self.project_id = project_id
        self.landing_type = landing_type
        self.artifacts = artifacts
        self.transformation_report = transformation_report
        self.commercial_value = commercial_value
        self.impact_score = impact_score


class Milestone:
    """
    功能：里程碑数据结构
    理论映射：对应科研动力学公理（公理五）
    """
    def __init__(self, milestone_id: str, name: str, milestone_type: str,
                 deadline_month: int, status: str, associated_phase: str,
                 dependencies: List[str] = None, quality_threshold: float = 0.8):
        self.milestone_id = milestone_id
        self.name = name
        self.milestone_type = milestone_type
        self.deadline_month = deadline_month
        self.status = status
        self.associated_phase = associated_phase
        self.dependencies = dependencies or []
        self.quality_threshold = quality_threshold


class TaskNode:
    """
    功能：任务节点数据结构
    理论映射：对应科研动力学公理（公理五）
    """
    def __init__(self, task_id: str, name: str, phase: str,
                 dependencies: List[str], resources: List[str],
                 duration: int, priority: int = 1):
        self.task_id = task_id
        self.name = name
        self.phase = phase
        self.dependencies = dependencies
        self.resources = resources
        self.duration = duration
        self.priority = priority


class ProjectPlan:
    """
    功能：项目计划数据结构（增强版）
    理论映射：对应科研动力学公理（公理五）
    """
    def __init__(self, project_id: str, topic: TopicItem, milestones: List[Milestone],
                 budget_plan: Dict, timeline: Dict, task_graph: List[TaskNode],
                 human_checkpoints: List[str], risk_plan: List[Dict],
                 mode: AutoMode, total_budget: int):
        self.project_id = project_id
        self.topic = topic
        self.milestones = milestones
        self.budget_plan = budget_plan
        self.timeline = timeline
        self.task_graph = task_graph
        self.human_checkpoints = human_checkpoints
        self.risk_plan = risk_plan
        self.mode = mode
        self.total_budget = total_budget


class ProjectResult:
    """
    功能：项目执行结果数据结构
    理论映射：对应科研动力学公理（公理五）
    """
    def __init__(self, project_id: str, status: ProjectStatus,
                 phase_results: Dict, artifacts: Dict,
                 final_output: Any, error_message: str = None):
        self.project_id = project_id
        self.status = status
        self.phase_results = phase_results
        self.artifacts = artifacts
        self.final_output = final_output
        self.error_message = error_message


class LandingSolution:
    """
    功能：落地方案数据结构
    理论映射：对应成果落地转化范式（公理五）
    """
    def __init__(self, solution_id: str, target_scenario: str,
                 core_technology: Dict, engineering_plan: Dict,
                 benefit_estimate: Dict, risk_assessment: Dict,
                 roadmap: List[Dict], trace_project_id: str):
        self.solution_id = solution_id
        self.target_scenario = target_scenario
        self.core_technology = core_technology
        self.engineering_plan = engineering_plan
        self.benefit_estimate = benefit_estimate
        self.risk_assessment = risk_assessment
        self.roadmap = roadmap
        self.trace_project_id = trace_project_id


class EvolutionUpdate:
    """
    功能：进化更新数据结构
    理论映射：对应系统自进化迭代公理（公理七）
    """
    def __init__(self, update_id: str, update_type: str,
                 target: str, content: Any,
                 rationale: str, validation_status: str):
        self.update_id = update_id
        self.update_type = update_type
        self.target = target
        self.content = content
        self.rationale = rationale
        self.validation_status = validation_status


__all__ = [
    # 核心参数（锁档固定）
    "CoreParameters",
    # 枚举类型
    "ResearchTopicType",
    "ProjectStatus",
    "ValueDimension",
    "AutoMode",
    "ScienceDomain",
    # 数据类型
    "TopicItem",
    "ResearchPlan",
    "Project",
    "ExecutionRecord",
    "EvaluationReport",
    "LandingResult",
    "EvolutionUpdate",
    # 增强数据类型
    "Milestone",
    "TaskNode",
    "ProjectPlan",
    "ProjectResult",
    "LandingSolution",
]
