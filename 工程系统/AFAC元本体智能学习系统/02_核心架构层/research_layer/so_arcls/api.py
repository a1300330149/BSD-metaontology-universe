"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第2条（全域九维法理公理）、第4条（选题创化生成机制）、第5条（成果落地转化范式）、第6条（全局宿命边界统摄理论）、第7条（系统自进化迭代公理）
对应九维维度：天道原理/天道动力学/创化社会/因果社会/道心能级
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, κ=0.35, θ_mv=0.005, θ_evo=0.002

SO-ARCLS - 对外统一API

提供一键式科研成果全链路生成接口及各模块独立调用接口，
实现"选题→规划→实验→成果→落地→复盘→进化"的完整自主闭环。

核心接口：
1. run_full_autonomous_research - 全自主科研总入口
2. generate_and_evaluate_topics - 选题生成与评估
3. plan_research_project - 项目规划
4. run_project_full_pipeline - 全流程执行
5. generate_landing_solution - 成果落地
6. project_retrospective_and_evolution - 复盘进化
7. global_boundary_check - 全局边界校验

理论映射：
- run_full_autonomous_research：对应自主科研闭环动力学公理（公理二）全流程执行
- generate_and_evaluate_topics：对应选题创化生成机制（公理四）
- generate_landing_solution：对应成果落地转化范式（公理五）
- project_retrospective_and_evolution：对应系统自进化迭代公理（公理七）
- global_boundary_check：对应全局宿命边界统摄理论（公理六）
"""

from typing import Dict, List, Optional, Any

from .types import (
    ScienceDomain, ResearchTopicType, ProjectStatus, AutoMode,
    TopicItem, ProjectPlan, ProjectResult, LandingSolution,
)
from .topic_evaluation_engine import get_topic_evaluation_engine
from .project_planning_engine import get_project_planning_engine
from .execution_control_engine import get_execution_control_engine
from .landing_transformation_module import get_landing_transformation_module
from .self_evolution_engine import get_self_evolution_engine
from .boundary_control_center import get_boundary_control_center


class FinalProjectPackage:
    """
    功能：最终项目包数据结构
    理论映射：对应自主科研闭环动力学公理（公理二）
    """
    def __init__(self, project_id: str, topic: TopicItem,
                 project_plan: ProjectPlan, research_result: ProjectResult,
                 landing_solution: LandingSolution = None,
                 evolution_report: Dict = None):
        self.project_id = project_id
        self.topic = topic
        self.project_plan = project_plan
        self.research_result = research_result
        self.landing_solution = landing_solution
        self.evolution_report = evolution_report


def generate_and_evaluate_topics(domain: ScienceDomain,
                                  topic_type: ResearchTopicType,
                                  count: int = 3) -> List[TopicItem]:
    """
    生成并评估科研选题
    
    Args:
        domain: 科学领域
        topic_type: 选题类型
        count: 生成数量
        
    Returns:
        List[TopicItem]: 选题列表（已排序）
    """
    engine = get_topic_evaluation_engine()
    topics = engine.generate_and_evaluate_topics(domain, topic_type, num_topics=count)
    return topics


def plan_research_project(topic: TopicItem,
                          total_budget: int,
                          mode: AutoMode = AutoMode.FULL_AUTO) -> ProjectPlan:
    """
    为选定选题生成完整项目执行规划
    
    Args:
        topic: 选题项
        total_budget: 总预算
        mode: 自主模式
        
    Returns:
        ProjectPlan: 项目计划
    """
    engine = get_project_planning_engine()
    project_plan = engine.plan_research_project(topic, total_budget, mode)
    return project_plan


def run_project_full_pipeline(project_plan: ProjectPlan) -> ProjectResult:
    """
    按项目规划执行全流程自主科研闭环
    
    Args:
        project_plan: 项目计划
        
    Returns:
        ProjectResult: 项目执行结果
    """
    engine = get_execution_control_engine()
    project_result = engine.run_project_full_pipeline(project_plan)
    return project_result


def generate_landing_solution(research_result: ProjectResult,
                               target_scenario: str,
                               constraints: Dict = None) -> LandingSolution:
    """
    基于科研成果生成产业落地方案
    
    Args:
        research_result: 科研成果
        target_scenario: 目标场景
        constraints: 约束条件
        
    Returns:
        LandingSolution: 落地方案
    """
    module = get_landing_transformation_module()
    landing_solution = module.generate_landing_solution(
        research_result=research_result,
        target_scenario=target_scenario,
        constraints=constraints or {},
    )
    return landing_solution


def project_retrospective_and_evolution(project_result: ProjectResult) -> Dict:
    """
    项目复盘并触发系统自进化
    
    Args:
        project_result: 项目执行结果
        
    Returns:
        Dict: 进化报告
    """
    engine = get_self_evolution_engine()
    evolution_report = engine.project_retrospective_and_evolution(project_result)
    return evolution_report


def global_boundary_check(content: Any,
                          domain: ScienceDomain = None,
                          level: str = "normal") -> Dict:
    """
    全局边界统一校验入口
    
    Args:
        content: 待校验内容
        domain: 科学领域
        level: 校验级别
        
    Returns:
        Dict: 校验结果
    """
    center = get_boundary_control_center()
    passed, message = center.global_boundary_check(content, domain, level)
    return {"passed": passed, "message": message}


def run_full_autonomous_research(domain: ScienceDomain,
                                  topic_type: ResearchTopicType,
                                  total_budget: int,
                                  mode: AutoMode = AutoMode.FULL_AUTO,
                                  target_scenario: str = None,
                                  constraints: Dict = None) -> FinalProjectPackage:
    """
    全自主科研总入口：输入领域与预算，自动完成从选题到落地的完整科研闭环
    
    流程：选题生成与评估 → 项目规划 → 全局边界校验 → 全流程执行 → 成果产出 → 落地适配 → 复盘进化
    
    Args:
        domain: 科学领域
        topic_type: 选题类型
        total_budget: 总预算（万元）
        mode: 自主运行模式
        target_scenario: 目标落地场景
        constraints: 约束条件
        
    Returns:
        FinalProjectPackage: 最终项目包，包含所有阶段结果
    """
    constraints = constraints or {}
    
    print("=" * 80)
    print("SO-ARCLS 全自主科研总入口")
    print("=" * 80)
    print(f"领域: {domain.value}")
    print(f"选题类型: {topic_type.value}")
    print(f"总预算: {total_budget}万元")
    print(f"自主模式: {mode.value}")
    if target_scenario:
        print(f"目标场景: {target_scenario}")
    print("=" * 80)
    
    # ========== 阶段1: 选题生成与评估 ==========
    print("\n[阶段1] 选题生成与评估")
    print("-" * 60)
    
    topics = generate_and_evaluate_topics(domain, topic_type, count=3)
    
    if not topics:
        raise RuntimeError("未生成有效的选题")
    
    best_topic = topics[0]
    print(f"\n✅ 选中最优选题: {best_topic.content}")
    print(f"   综合得分: {best_topic.total_score:.4f}")
    print(f"   预计预算: {best_topic.expected_budget}万元")
    print(f"   预计周期: {best_topic.expected_cycle}个月")
    
    # 更新选题预算为用户指定的预算
    best_topic.expected_budget = total_budget
    
    # ========== 阶段2: 全局边界校验 ==========
    print("\n[阶段2] 全局边界校验")
    print("-" * 60)
    
    boundary_result = global_boundary_check(best_topic, domain)
    print(f"边界校验结果: {'✅ 通过' if boundary_result['passed'] else '❌ 未通过'}")
    
    if not boundary_result["passed"]:
        raise RuntimeError(f"边界校验未通过: {boundary_result['message']}")
    
    # ========== 阶段3: 项目规划 ==========
    print("\n[阶段3] 项目规划")
    print("-" * 60)
    
    project_plan = plan_research_project(best_topic, total_budget, mode)
    
    print(f"\n✅ 项目计划生成完成: {project_plan.project_id}")
    print(f"   里程碑数: {len(project_plan.milestones)}")
    print(f"   任务节点数: {len(project_plan.task_graph)}")
    
    # 项目规划后再次边界校验（关联项目ID）
    plan_boundary_result = global_boundary_check(project_plan, domain)
    if not plan_boundary_result["passed"]:
        raise RuntimeError(f"项目计划边界校验未通过: {plan_boundary_result['message']}")
    
    # ========== 阶段4: 全流程执行 ==========
    print("\n[阶段4] 全流程自主执行")
    print("-" * 60)
    
    project_result = run_project_full_pipeline(project_plan)
    
    print(f"\n项目执行状态: {project_result.status.value}")
    
    if project_result.error_message:
        print(f"   错误信息: {project_result.error_message}")
    
    # ========== 阶段5: 成果落地（可选） ==========
    landing_solution = None
    
    if target_scenario:
        print("\n[阶段5] 成果落地适配")
        print("-" * 60)
        
        landing_solution = generate_landing_solution(project_result, target_scenario, constraints)
        
        print(f"\n✅ 产业落地方案生成完成: {landing_solution.solution_id}")
        print(f"   目标场景: {landing_solution.target_scenario}")
        print(f"   预计收益: {landing_solution.benefit_estimate['total_benefit']}万元")
        print(f"   风险等级: {landing_solution.risk_assessment['risk_level']}")
    
    # ========== 阶段6: 复盘进化 ==========
    print("\n[阶段6] 项目复盘与系统进化")
    print("-" * 60)
    
    evolution_report = project_retrospective_and_evolution(project_result)
    
    print(f"\n✅ 进化报告生成完成: {evolution_report['report_id']}")
    print(f"   新增知识: {evolution_report['knowledge_added']} 条")
    print(f"   优化模块: {len(evolution_report['optimized_modules'])} 个")
    print(f"   预期收益: {evolution_report['expected_gain']:.1f}%")
    
    # ========== 汇总结果 ==========
    final_package = FinalProjectPackage(
        project_id=project_plan.project_id,
        topic=best_topic,
        project_plan=project_plan,
        research_result=project_result,
        landing_solution=landing_solution,
        evolution_report=evolution_report,
    )
    
    print("\n" + "=" * 80)
    print("全自主科研闭环完成!")
    print("=" * 80)
    
    return final_package


__all__ = [
    # 核心类型
    "FinalProjectPackage",
    # 独立模块接口
    "generate_and_evaluate_topics",
    "plan_research_project",
    "run_project_full_pipeline",
    "generate_landing_solution",
    "project_retrospective_and_evolution",
    "global_boundary_check",
    # 全流程入口
    "run_full_autonomous_research",
]