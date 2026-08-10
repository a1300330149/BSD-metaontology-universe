"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第2条（全域九维法理公理）、第6条（全局宿命边界统摄理论）
对应九维维度：天道原理/天道动力学/创化社会
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：γ=0.92（衰减系数）, κ=0.35（耦合强度）

SO-ARCLS - 全局调度器
统一调度下层所有能力，实现"选题→规划→实验→成果→落地→复盘→进化"的完整自主闭环

核心职责：
1. 全局边界与风险管控
2. 各模块协同调度
3. 全链路可追溯、可审计、可复现
4. 系统稳态保障

理论映射：
- GlobalScheduler：对应自主科研闭环动力学公理（公理二）全局调度
- GlobalBoundaryControl：对应全局宿命边界统摄理论（公理六）边界管控
- run_autonomous_research：对应自主科研闭环动力学公理（公理二）全流程串联
- MAX_PROJECTS=10：对应资源边界约束
- MAX_BUDGET=1000：对应预算边界约束
- MAX_CYCLE=36：对应周期边界约束
"""

import time
from typing import Dict, List, Optional, Any

from .types import (
    Project, ProjectStatus, AutoMode, ScienceDomain,
    ResearchTopicType, TopicItem, ProjectPlan, ProjectResult,
)
from .topic_evaluation_engine import get_topic_evaluation_engine
from .project_planning_engine import get_project_planning_engine
from .execution_control_engine import get_execution_control_engine
from .landing_transformation_module import get_landing_transformation_module
from .self_evolution_engine import get_self_evolution_engine


class GlobalBoundaryControl:
    """
    功能：全局边界与风险管控中心
    理论映射：对应全局宿命边界统摄理论（公理六）
    """
    
    MAX_PROJECTS = 10
    MAX_BUDGET = 1000
    MAX_CYCLE = 36
    
    def __init__(self):
        self.active_projects = 0
        self.total_budget_used = 0
        self.risk_threshold = 0.7
    
    def check_boundary(self, topic_item: TopicItem, constraints: Dict) -> Dict:
        """
        检查选题是否在全局边界内
        
        Args:
            topic_item: 选题项
            constraints: 约束条件
            
        Returns:
            Dict: 边界检查结果
        """
        checks = []
        warnings = []
        
        # 项目数量检查
        if self.active_projects >= self.MAX_PROJECTS:
            checks.append({"check": "project_limit", "passed": False, "reason": f"已达最大项目数 {self.MAX_PROJECTS}"})
            warnings.append("项目数量已达上限")
        else:
            checks.append({"check": "project_limit", "passed": True})
        
        # 预算检查
        if topic_item.expected_budget + self.total_budget_used > self.MAX_BUDGET:
            checks.append({"check": "budget_limit", "passed": False, "reason": f"预算超支: {topic_item.expected_budget} + {self.total_budget_used} > {self.MAX_BUDGET}"})
            warnings.append("预算超支风险")
        else:
            checks.append({"check": "budget_limit", "passed": True})
        
        # 周期检查
        if topic_item.expected_cycle > self.MAX_CYCLE:
            checks.append({"check": "cycle_limit", "passed": False, "reason": f"周期超限: {topic_item.expected_cycle} > {self.MAX_CYCLE}个月"})
            warnings.append("周期超限风险")
        else:
            checks.append({"check": "cycle_limit", "passed": True})
        
        # 重复风险检查
        if topic_item.duplicate_risk > self.risk_threshold:
            checks.append({"check": "duplicate_risk", "passed": False, "reason": f"重复风险过高: {topic_item.duplicate_risk}"})
            warnings.append("选题重复风险较高")
        else:
            checks.append({"check": "duplicate_risk", "passed": True})
        
        # 可行性检查
        feasibility = topic_item.value_scores.get('feasibility', 0)
        if feasibility < 0.3:
            checks.append({"check": "feasibility", "passed": False, "reason": f"可行性过低: {feasibility}"})
            warnings.append("选题可行性较低")
        else:
            checks.append({"check": "feasibility", "passed": True})
        
        all_passed = all(c["passed"] for c in checks)
        
        return {
            "all_passed": all_passed,
            "checks": checks,
            "warnings": warnings,
            "risk_level": "low" if all_passed else "high" if len(warnings) >= 2 else "medium",
        }
    
    def allocate_resources(self, topic_item: TopicItem) -> bool:
        """分配资源"""
        if self.active_projects < self.MAX_PROJECTS and \
           self.total_budget_used + topic_item.expected_budget <= self.MAX_BUDGET:
            self.active_projects += 1
            self.total_budget_used += topic_item.expected_budget
            return True
        return False
    
    def release_resources(self, topic_item: TopicItem):
        """释放资源"""
        self.active_projects = max(0, self.active_projects - 1)
        self.total_budget_used = max(0, self.total_budget_used - topic_item.expected_budget)
    
    def get_resource_status(self) -> Dict:
        """获取资源状态"""
        return {
            "active_projects": self.active_projects,
            "max_projects": self.MAX_PROJECTS,
            "budget_used": self.total_budget_used,
            "max_budget": self.MAX_BUDGET,
            "project_utilization": self.active_projects / self.MAX_PROJECTS * 100,
            "budget_utilization": self.total_budget_used / self.MAX_BUDGET * 100,
        }


class GlobalScheduler:
    """
    功能：全局调度器
    理论映射：对应自主科研闭环动力学公理（公理二）全局调度
    """
    
    def __init__(self):
        self.topic_engine = get_topic_evaluation_engine()
        self.planning_engine = get_project_planning_engine()
        self.execution_engine = get_execution_control_engine()
        self.landing_module = get_landing_transformation_module()
        self.evolution_engine = get_self_evolution_engine()
        self.boundary_control = GlobalBoundaryControl()
        
        self.projects = {}
    
    def run_autonomous_research(
        self,
        domain: ScienceDomain,
        topic_type: ResearchTopicType = ResearchTopicType.APPLIED,
        auto_mode: AutoMode = AutoMode.FULL_AUTO,
        constraints: Optional[Dict] = None,
        num_topics: int = 5,
        landing_type: str = "academic_publication",
        target_scenario: str = None,
    ) -> Dict[str, Any]:
        """
        运行完整的自主科研闭环（增强版）
        
        流程：选题→规划→实验→成果→落地→复盘→进化
        
        Args:
            domain: 研究领域
            topic_type: 选题类型
            auto_mode: 自主运行模式
            constraints: 约束条件
            num_topics: 候选选题数量
            landing_type: 落地类型
            target_scenario: 目标落地场景
            
        Returns:
            Dict: 完整的科研闭环结果
        """
        print("\n" + "=" * 80)
        print("SO-ARCLS 六阶自主科研闭环系统")
        print("=" * 80)
        print(f"领域: {domain.value}")
        print(f"选题类型: {topic_type.value}")
        print(f"自主模式: {auto_mode.value}")
        print(f"落地场景: {target_scenario or '默认'}")
        print("=" * 80)
        
        if constraints is None:
            constraints = {}
        
        # ========== 阶段1: 自主选题 ==========
        print("\n[阶段1] 自主选题与价值评估")
        print("-" * 60)
        
        topics = self.topic_engine.generate_and_evaluate_topics(
            domain=domain,
            topic_type=topic_type,
            constraints=constraints,
            num_topics=num_topics,
        )
        
        if not topics:
            print("❌ 未生成符合条件的选题")
            return {"status": "failed", "reason": "无合格选题"}
        
        # 选择最优选题
        selected_topic = topics[0]
        print(f"\n✅ 选中最优选题:")
        print(f"   内容: {selected_topic.content}")
        print(f"   综合得分: {selected_topic.total_score:.4f}")
        print(f"   学术价值: {selected_topic.value_scores.get('academic_value', 0):.4f}")
        print(f"   创新价值: {selected_topic.value_scores.get('innovation_value', 0):.4f}")
        print(f"   产业价值: {selected_topic.value_scores.get('industry_value', 0):.4f}")
        print(f"   可行性: {selected_topic.value_scores.get('feasibility', 0):.4f}")
        print(f"   预计预算: {selected_topic.expected_budget}万元")
        print(f"   预计周期: {selected_topic.expected_cycle}个月")
        
        # 边界检查
        boundary_check = self.boundary_control.check_boundary(selected_topic, constraints)
        print(f"\n边界检查结果: {boundary_check['risk_level']}")
        if boundary_check["warnings"]:
            for warning in boundary_check["warnings"]:
                print(f"   ⚠️ {warning}")
        
        if not boundary_check["all_passed"]:
            print("\n❌ 边界检查未通过，终止项目")
            return {"status": "failed", "reason": "边界检查未通过"}
        
        # ========== 阶段2: 项目规划（增强版）==========
        print("\n[阶段2] 项目自主规划与调度（增强版）")
        print("-" * 60)
        
        project_plan = self.planning_engine.plan_research_project(
            topic=selected_topic,
            total_budget=selected_topic.expected_budget,
            mode=auto_mode,
        )
        
        print(f"\n✅ 项目计划生成完成: {project_plan.project_id}")
        print(f"   里程碑数: {len(project_plan.milestones)}")
        print(f"   任务节点数: {len(project_plan.task_graph)}")
        print(f"   总预算: {project_plan.total_budget}万元")
        print(f"   风险预案数: {len(project_plan.risk_plan)}")
        
        if project_plan.human_checkpoints:
            print(f"   人工干预节点: {', '.join(project_plan.human_checkpoints)}")
        
        # 分配资源
        if not self.boundary_control.allocate_resources(selected_topic):
            print("\n❌ 资源分配失败")
            return {"status": "failed", "reason": "资源不足"}
        
        # ========== 阶段3: 执行管控（增强版）==========
        print("\n[阶段3] 全链路闭环执行管控（增强版）")
        print("-" * 60)
        
        project_result = self.execution_engine.run_project_full_pipeline(project_plan)
        
        print(f"\n项目执行状态: {project_result.status.value}")
        
        if project_result.error_message:
            print(f"   错误信息: {project_result.error_message}")
        
        # ========== 阶段4: 成果落地（增强版）==========
        print("\n[阶段4] 成果落地与转化适配（增强版）")
        print("-" * 60)
        
        landing_result = None
        landing_solution = None
        
        if target_scenario:
            landing_solution = self.landing_module.generate_landing_solution(
                research_result=project_result,
                target_scenario=target_scenario,
                constraints=constraints,
            )
            print(f"\n✅ 产业落地方案生成完成: {landing_solution.solution_id}")
            print(f"   目标场景: {landing_solution.target_scenario}")
            print(f"   预计收益: {landing_solution.benefit_estimate['total_benefit']}万元")
            print(f"   风险等级: {landing_solution.risk_assessment['risk_level']}")
            print(f"   落地周期: {sum(p['duration_months'] for p in landing_solution.roadmap)}个月")
        else:
            project = Project(
                project_id=project_plan.project_id,
                topic_item=selected_topic,
                plan=project_plan,
                status=project_result.status,
                auto_mode=auto_mode,
                artifacts=project_result.artifacts,
            )
            landing_result = self.landing_module.transform_to_landing(project, landing_type)
            print(f"\n✅ 成果转化完成")
            print(f"   转化类型: {landing_result.landing_type}")
            print(f"   商业价值: {landing_result.commercial_value}万元")
            print(f"   影响力评分: {landing_result.impact_score}")
        
        # ========== 阶段5: 复盘评估 ==========
        print("\n[阶段5] 系统自进化迭代")
        print("-" * 60)
        
        project_for_eval = Project(
            project_id=project_plan.project_id,
            topic_item=selected_topic,
            plan=project_plan,
            status=project_result.status,
            auto_mode=auto_mode,
            artifacts=project_result.artifacts,
        )
        evaluation_report = self.evolution_engine.evaluate_project(project_for_eval)
        
        print(f"\n评估报告:")
        print(f"   成功率: {evaluation_report.success_rate:.1f}%")
        print(f"   关键结论: {evaluation_report.conclusions[0]}")
        print(f"   建议数: {len(evaluation_report.recommendations)}")
        
        # ========== 阶段6: 自进化 ==========
        evolution_updates = self.evolution_engine.evolve_from_evaluation(evaluation_report)
        
        # 释放资源
        self.boundary_control.release_resources(selected_topic)
        
        # 保存项目
        self.projects[project_plan.project_id] = project_for_eval
        
        # ========== 返回结果 ==========
        print("\n" + "=" * 80)
        print("自主科研闭环完成!")
        print("=" * 80)
        
        result = {
            "status": "completed",
            "project_id": project_plan.project_id,
            "topic": selected_topic.content,
            "domain": domain.value,
            "auto_mode": auto_mode.value,
            "project_status": project_result.status.value,
            "project_plan": {
                "milestone_count": len(project_plan.milestones),
                "task_count": len(project_plan.task_graph),
                "total_budget": project_plan.total_budget,
                "human_checkpoints": project_plan.human_checkpoints,
            },
            "project_result": {
                "phase_results": len(project_result.phase_results),
                "artifacts": len(project_result.artifacts),
                "error_message": project_result.error_message,
            },
            "evaluation_report": {
                "success_rate": evaluation_report.success_rate,
                "conclusions": evaluation_report.conclusions,
                "recommendations": evaluation_report.recommendations,
                "lessons_learned": evaluation_report.lessons_learned,
            },
            "evolution_updates": len(evolution_updates),
            "resource_status": self.boundary_control.get_resource_status(),
        }
        
        if landing_solution:
            result["landing_solution"] = {
                "solution_id": landing_solution.solution_id,
                "target_scenario": landing_solution.target_scenario,
                "total_benefit": landing_solution.benefit_estimate["total_benefit"],
                "risk_level": landing_solution.risk_assessment["risk_level"],
                "roadmap_phases": len(landing_solution.roadmap),
            }
        elif landing_result:
            result["landing_result"] = {
                "type": landing_result.landing_type,
                "commercial_value": landing_result.commercial_value,
                "impact_score": landing_result.impact_score,
            }
        
        return result
    
    def run_research_from_plan(
        self,
        project_plan: ProjectPlan,
        target_scenario: str = None,
    ) -> Dict[str, Any]:
        """
        从已有项目计划执行科研闭环
        
        Args:
            project_plan: 项目计划
            target_scenario: 目标落地场景
            
        Returns:
            Dict: 科研闭环结果
        """
        print("\n" + "=" * 80)
        print("SO-ARCLS - 从计划执行科研闭环")
        print("=" * 80)
        print(f"项目ID: {project_plan.project_id}")
        print(f"选题: {project_plan.topic.content}")
        print("=" * 80)
        
        # 执行管控
        print("\n[阶段1] 全链路闭环执行管控")
        print("-" * 60)
        
        project_result = self.execution_engine.run_project_full_pipeline(project_plan)
        
        print(f"\n项目执行状态: {project_result.status.value}")
        
        # 成果落地
        print("\n[阶段2] 成果落地与转化适配")
        print("-" * 60)
        
        landing_solution = None
        
        if target_scenario:
            landing_solution = self.landing_module.generate_landing_solution(
                research_result=project_result,
                target_scenario=target_scenario,
                constraints={},
            )
            print(f"\n✅ 产业落地方案生成完成: {landing_solution.solution_id}")
            print(f"   目标场景: {landing_solution.target_scenario}")
            print(f"   预计收益: {landing_solution.benefit_estimate['total_benefit']}万元")
        else:
            project = Project(
                project_id=project_plan.project_id,
                topic_item=project_plan.topic,
                plan=project_plan,
                status=project_result.status,
                auto_mode=project_plan.mode,
                artifacts=project_result.artifacts,
            )
            landing_result = self.landing_module.transform_to_landing(project, "academic_publication")
            print(f"\n✅ 成果转化完成")
        
        # 复盘评估
        print("\n[阶段3] 系统自进化迭代")
        print("-" * 60)
        
        project_for_eval = Project(
            project_id=project_plan.project_id,
            topic_item=project_plan.topic,
            plan=project_plan,
            status=project_result.status,
            auto_mode=project_plan.mode,
            artifacts=project_result.artifacts,
        )
        evaluation_report = self.evolution_engine.evaluate_project(project_for_eval)
        
        print(f"\n评估报告:")
        print(f"   成功率: {evaluation_report.success_rate:.1f}%")
        
        # 自进化
        evolution_updates = self.evolution_engine.evolve_from_evaluation(evaluation_report)
        
        # 保存项目
        self.projects[project_plan.project_id] = project_for_eval
        
        result = {
            "status": "completed",
            "project_id": project_plan.project_id,
            "project_status": project_result.status.value,
            "evaluation_report": {
                "success_rate": evaluation_report.success_rate,
                "conclusions": evaluation_report.conclusions,
            },
            "evolution_updates": len(evolution_updates),
        }
        
        if landing_solution:
            result["landing_solution"] = {
                "solution_id": landing_solution.solution_id,
                "target_scenario": landing_solution.target_scenario,
                "total_benefit": landing_solution.benefit_estimate["total_benefit"],
            }
        
        return result
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """获取项目"""
        return self.projects.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """获取所有项目"""
        return list(self.projects.values())
    
    def get_resource_status(self) -> Dict:
        """获取资源状态"""
        return self.boundary_control.get_resource_status()


# 全局实例
_global_scheduler = None

def get_global_scheduler() -> GlobalScheduler:
    """获取全局调度器实例"""
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = GlobalScheduler()
    return _global_scheduler


__all__ = [
    "GlobalScheduler",
    "GlobalBoundaryControl",
    "get_global_scheduler",
]
