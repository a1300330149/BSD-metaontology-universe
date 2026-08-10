"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第2条（全域九维法理公理）、第4条（选题创化生成机制）、第5条（成果落地转化范式）、第6条（全局宿命边界统摄理论）、第7条（系统自进化迭代公理）
对应九维维度：天道原理/天道动力学/创化社会/因果社会/道心能级
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, κ=0.35, θ_mv=0.005, θ_evo=0.002, θ_neg=0.02

SO-ARCLS - 六阶自主科研闭环系统
Sixth-Order Autonomous Research Closed-Loop System

阶段定位：整套自动科研系统的「顶层闭环层」
实现"选题→规划→实验→成果→落地→复盘→进化"的完整自主闭环

理论映射：
- 六阶模块整体：对应自主科研闭环动力学公理（公理二）
- 选题引擎：对应选题创化生成机制（公理四）
- 规划引擎：对应自主科研闭环动力学公理（公理二）项目层调度
- 执行引擎：对应自主科研闭环动力学公理（公理二）执行层管控
- 落地模块：对应成果落地转化范式（公理五）
- 进化引擎：对应系统自进化迭代公理（公理七）
- 边界管控：对应全局宿命边界统摄理论（公理六）
"""

from .types import (
    ResearchTopicType,
    ProjectStatus,
    ValueDimension,
    AutoMode,
    ScienceDomain,
    TopicItem,
    ResearchPlan,
    Project,
    ExecutionRecord,
    EvaluationReport,
    LandingResult,
    EvolutionUpdate,
    Milestone,
    TaskNode,
    ProjectPlan,
    ProjectResult,
    LandingSolution,
)

from .topic_evaluation_engine import (
    TopicEvaluationEngine,
    get_topic_evaluation_engine,
)

from .project_planning_engine import (
    ProjectPlanningEngine,
    get_project_planning_engine,
)

from .execution_control_engine import (
    ExecutionControlEngine,
    get_execution_control_engine,
)

from .landing_transformation_module import (
    LandingTransformationModule,
    get_landing_transformation_module,
)

from .self_evolution_engine import (
    SelfEvolutionEngine,
    get_self_evolution_engine,
)

from .boundary_control_center import (
    GlobalBoundaryControlCenter,
    get_boundary_control_center,
)

from .scheduler import (
    GlobalScheduler,
    GlobalBoundaryControl,
    get_global_scheduler,
)

from .api import (
    FinalProjectPackage,
    generate_and_evaluate_topics,
    plan_research_project,
    run_project_full_pipeline,
    generate_landing_solution,
    project_retrospective_and_evolution,
    global_boundary_check,
    run_full_autonomous_research,
)

__version__ = "6.0.0"

__all__ = [
    # 版本
    "__version__",
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
    # 模块引擎（高级用户）
    "TopicEvaluationEngine",
    "ProjectPlanningEngine",
    "ExecutionControlEngine",
    "LandingTransformationModule",
    "SelfEvolutionEngine",
    "GlobalBoundaryControlCenter",
    "GlobalScheduler",
    "GlobalBoundaryControl",
    # 引擎获取函数
    "get_topic_evaluation_engine",
    "get_project_planning_engine",
    "get_execution_control_engine",
    "get_landing_transformation_module",
    "get_self_evolution_engine",
    "get_boundary_control_center",
    "get_global_scheduler",
    # API接口
    "FinalProjectPackage",
    "generate_and_evaluate_topics",
    "plan_research_project",
    "run_project_full_pipeline",
    "generate_landing_solution",
    "project_retrospective_and_evolution",
    "global_boundary_check",
    "run_full_autonomous_research",
]
