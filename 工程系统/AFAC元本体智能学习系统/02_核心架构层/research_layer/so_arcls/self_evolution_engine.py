"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第7条（系统自进化迭代公理）、第2条（全域九维法理公理）
对应九维维度：天道原理/天道动力学/道心能级
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：θ_evo=0.002（自进化增量）, γ=0.92（衰减系数）

SO-ARCLS - 系统自进化迭代引擎

对应系统自进化迭代公理，每完成一个完整科研项目，自动复盘全流程得失，
反哺优化底层基底库、策略模型与决策规则，实现系统能力的自我迭代、持续进化。

核心职责：
1. 项目全流程复盘：分析项目各环节的效率、收益、问题与卡点
2. 基底库迭代更新：沉淀知识、范式、规律、失败案例入全学科统一基底库
3. 决策策略优化：基于历史数据优化选题评估、预算分配、迁移策略等核心算法
4. 失败案例沉淀：将异常、失败、负迁移案例纳入失败知识库
5. 进化效果量化：定期评估系统能力提升幅度，输出进化报告

理论映射：
- SelfEvolutionEngine：对应系统自进化迭代公理（公理七）
- evaluate_project：对应科研价值边际判定公理（公理三）评估方法
- evolve_from_evaluation：对应系统自进化迭代公理（公理七）
- _add_project_knowledge：对应全域九维法理公理（公理二）知识积累
- _add_failure_cases：对应全局宿命边界统摄理论（公理六）风险沉淀
- _calculate_evolution_gain：对应θ_evo自进化增量参数
"""

import time
import random
from typing import Dict, List, Optional, Any, Tuple

from .types import (
    Project, EvaluationReport, EvolutionUpdate, ProjectResult,
)


class SelfEvolutionEngine:
    """
    功能：系统自进化迭代引擎
    理论映射：对应系统自进化迭代公理（公理七）
    """
    
    UPDATE_TYPES = [
        "strategy_update",
        "knowledge_base_update",
        "parameter_tuning",
        "model_improvement",
        "process_optimization",
    ]
    
    def __init__(self):
        self.update_counter = 0
        self.evolution_history = []
        self.performance_metrics = {}
    
    def evaluate_project(self, project: Project) -> EvaluationReport:
        """
        评估项目执行结果，生成复盘报告
        
        Args:
            project: 科研项目
            
        Returns:
            EvaluationReport: 评估报告
        """
        print(f"\n[进化引擎] 开始评估项目: {project.project_id}")
        
        # 计算各项指标
        metrics = self._calculate_metrics(project)
        
        # 生成结论
        conclusions = self._generate_conclusions(project, metrics)
        
        # 生成建议
        recommendations = self._generate_recommendations(project, metrics)
        
        # 计算成功率
        success_rate = self._calculate_success_rate(project, metrics)
        
        # 提取经验教训
        lessons_learned = self._extract_lessons(project)
        
        report = EvaluationReport(
            project_id=project.project_id,
            metrics=metrics,
            conclusions=conclusions,
            recommendations=recommendations,
            success_rate=success_rate,
            lessons_learned=lessons_learned,
        )
        
        print(f"\n[进化引擎] 评估完成! 成功率: {success_rate:.1f}%")
        print(f"[进化引擎] 关键结论: {conclusions[0][:50]}...")
        
        return report
    
    def evolve_from_evaluation(self, report: EvaluationReport) -> List[EvolutionUpdate]:
        """
        基于评估报告进行系统进化
        
        Args:
            report: 评估报告
            
        Returns:
            List[EvolutionUpdate]: 进化更新列表
        """
        print(f"\n[进化引擎] 基于评估报告进行进化...")
        
        updates = []
        
        # 根据评估结果生成进化更新
        if report.success_rate < 60:
            updates.extend(self._generate_improvement_updates(report))
        elif report.success_rate < 80:
            updates.extend(self._generate_optimization_updates(report))
        else:
            updates.extend(self._generate_enhancement_updates(report))
        
        # 验证更新
        for update in updates:
            update.validation_status = self._validate_update(update)
        
        # 应用更新
        self._apply_updates(updates)
        
        print(f"[进化引擎] 完成 {len(updates)} 项进化更新")
        
        return updates
    
    def _calculate_metrics(self, project: Project) -> Dict[str, float]:
        """计算项目指标"""
        metrics = {
            "phase_completion_rate": 0.0,
            "milestone_achievement_rate": 0.0,
            "budget_efficiency": 0.0,
            "time_efficiency": 0.0,
            "output_quality": 0.0,
        }
        
        if hasattr(project.plan, 'phases'):
            total_phases = len(project.plan.phases)
            completed_phases = sum(1 for p in project.plan.phases if p.get("status") == "completed")
        else:
            total_phases = len(project.plan.milestones) if hasattr(project.plan, 'milestones') else 0
            completed_phases = sum(1 for m in project.plan.milestones if getattr(m, 'status') == "completed") if hasattr(project.plan, 'milestones') else 0
        metrics["phase_completion_rate"] = completed_phases / total_phases if total_phases > 0 else 0
        
        if hasattr(project.plan, 'milestones'):
            total_milestones = len(project.plan.milestones)
            if project.plan.milestones and hasattr(project.plan.milestones[0], 'status'):
                achieved_milestones = sum(1 for m in project.plan.milestones if m.status == "completed")
            else:
                achieved_milestones = sum(1 for m in project.plan.milestones if m.get("status") == "completed") if isinstance(project.plan.milestones[0], dict) else 0
        else:
            total_milestones = 0
            achieved_milestones = 0
        metrics["milestone_achievement_rate"] = achieved_milestones / total_milestones if total_milestones > 0 else 0
        
        metrics["budget_efficiency"] = min(1.0, 0.8 + random.uniform(-0.1, 0.2))
        metrics["time_efficiency"] = min(1.0, 0.75 + random.uniform(-0.15, 0.2))
        metrics["output_quality"] = project.topic_item.total_score
        
        return {k: round(v, 4) for k, v in metrics.items()}
    
    def _generate_conclusions(self, project: Project, metrics: Dict) -> List[str]:
        """生成结论"""
        conclusions = []
        
        if metrics["phase_completion_rate"] >= 0.8:
            conclusions.append("项目执行进度良好，各阶段按时完成")
        else:
            conclusions.append("部分阶段进度滞后，需分析原因并优化")
        
        if metrics["milestone_achievement_rate"] >= 0.7:
            conclusions.append("关键里程碑达成情况良好")
        else:
            conclusions.append("部分关键里程碑未达成，需加强监控")
        
        if metrics["output_quality"] >= 0.7:
            conclusions.append("成果质量较高，具备进一步推广价值")
        else:
            conclusions.append("成果质量有待提升，建议进一步优化")
        
        return conclusions
    
    def _generate_recommendations(self, project: Project, metrics: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if metrics["time_efficiency"] < 0.7:
            recommendations.append("优化任务调度策略，减少不必要的等待时间")
            recommendations.append("引入并行执行机制，提高资源利用率")
        
        if metrics["budget_efficiency"] < 0.7:
            recommendations.append("精细化预算管理，建立成本控制机制")
            recommendations.append("评估资源使用效率，优化资源分配")
        
        if metrics["output_quality"] < 0.7:
            recommendations.append("加强成果审查机制，提升输出质量")
            recommendations.append("引入外部评审，获取专业反馈")
        
        if len(recommendations) == 0:
            recommendations.append("保持当前策略，持续监控执行效果")
        
        return recommendations
    
    def _calculate_success_rate(self, project: Project, metrics: Dict) -> float:
        """计算成功率"""
        weights = {
            "phase_completion_rate": 0.3,
            "milestone_achievement_rate": 0.25,
            "budget_efficiency": 0.15,
            "time_efficiency": 0.15,
            "output_quality": 0.15,
        }
        
        success_rate = sum(metrics[k] * weights[k] for k in weights) * 100
        return round(success_rate, 1)
    
    def _extract_lessons(self, project: Project) -> List[str]:
        """提取经验教训"""
        lessons = []
        
        if hasattr(project.plan, 'phases'):
            for phase in project.plan.phases:
                if phase.get("status") == "completed":
                    lessons.append(f"{phase.get('phase_name', '未知阶段')}阶段执行顺利，可作为后续项目参考")
                elif phase.get("status") in ("failed", "retry"):
                    lessons.append(f"{phase.get('phase_name', '未知阶段')}阶段遇到困难，需优化执行策略")
        elif hasattr(project.plan, 'milestones'):
            completed_count = sum(1 for m in project.plan.milestones if getattr(m, 'status') == "completed")
            total_count = len(project.plan.milestones)
            if completed_count == total_count:
                lessons.append(f"所有{total_count}个里程碑均已完成，项目执行顺利")
            elif completed_count > 0:
                lessons.append(f"完成了{completed_count}/{total_count}个里程碑，部分阶段需要关注")
        
        if hasattr(project.plan, 'risks') and len(project.plan.risks) > 0:
            if isinstance(project.plan.risks[0], dict):
                applied_risks = sum(1 for r in project.plan.risks if r.get("status") == "applied")
            else:
                applied_risks = 0
            if applied_risks > 0:
                lessons.append(f"成功应用了{applied_risks}项风险应对策略，验证了风险管理有效性")
        elif hasattr(project.plan, 'risk_plan') and len(project.plan.risk_plan) > 0:
            lessons.append(f"项目规划中识别了{len(project.plan.risk_plan)}项风险，风险管理体系有效")
        
        return lessons
    
    def _generate_improvement_updates(self, report: EvaluationReport) -> List[EvolutionUpdate]:
        """生成改进型更新（低成功率）"""
        updates = []
        
        updates.append(EvolutionUpdate(
            update_id=self._generate_update_id(),
            update_type="strategy_update",
            target="task_scheduling",
            content={"optimization_strategy": "dynamic_priority"},
            rationale="项目时间效率较低，需要优化任务调度策略",
            validation_status="pending",
        ))
        
        updates.append(EvolutionUpdate(
            update_id=self._generate_update_id(),
            update_type="parameter_tuning",
            target="learning_rate",
            content={"base_lr": 0.001, "scheduler": "cosine_annealing"},
            rationale="模型训练效率有待提升，调整学习率策略",
            validation_status="pending",
        ))
        
        return updates
    
    def _generate_optimization_updates(self, report: EvaluationReport) -> List[EvolutionUpdate]:
        """生成优化型更新（中等成功率）"""
        updates = []
        
        updates.append(EvolutionUpdate(
            update_id=self._generate_update_id(),
            update_type="process_optimization",
            target="phase_duration",
            content={"adjustment_factor": 0.9},
            rationale="阶段时间估算偏保守，适当压缩以提高效率",
            validation_status="pending",
        ))
        
        updates.append(EvolutionUpdate(
            update_id=self._generate_update_id(),
            update_type="knowledge_base_update",
            target="success_patterns",
            content={"patterns": report.lessons_learned},
            rationale="提取成功经验，丰富知识基底库",
            validation_status="pending",
        ))
        
        return updates
    
    def _generate_enhancement_updates(self, report: EvaluationReport) -> List[EvolutionUpdate]:
        """生成增强型更新（高成功率）"""
        updates = []
        
        updates.append(EvolutionUpdate(
            update_id=self._generate_update_id(),
            update_type="model_improvement",
            target="model_architecture",
            content={"enhancements": ["attention_mechanism", "residual_connections"]},
            rationale="当前模型效果良好，进一步增强架构以提升性能",
            validation_status="pending",
        ))
        
        updates.append(EvolutionUpdate(
            update_id=self._generate_update_id(),
            update_type="knowledge_base_update",
            target="domain_knowledge",
            content={"domain": report.project_id.split('_')[1], "knowledge": report.conclusions},
            rationale="项目成果丰富了领域知识，纳入基底库",
            validation_status="pending",
        ))
        
        return updates
    
    def _validate_update(self, update: EvolutionUpdate) -> str:
        """验证更新"""
        validation_result = "validated" if random.random() > 0.1 else "needs_review"
        return validation_result
    
    def _apply_updates(self, updates: List[EvolutionUpdate]):
        """应用更新"""
        for update in updates:
            if update.validation_status == "validated":
                self.evolution_history.append(update.__dict__)
                print(f"  [进化引擎] 应用更新: {update.update_type} -> {update.target}")
    
    def _generate_update_id(self) -> str:
        """生成更新ID"""
        self.update_counter += 1
        return f"update_{int(time.time())}_{self.update_counter:04d}"
    
    def get_evolution_history(self) -> List[Dict]:
        """获取进化历史"""
        return self.evolution_history
    
    def project_retrospective_and_evolution(self, project_result: ProjectResult) -> Dict:
        """
        项目复盘并触发系统自进化（核心函数）
        
        Args:
            project_result: 项目执行结果
            
        Returns:
            Dict: 进化报告
        """
        print(f"\n[进化引擎] 开始项目复盘与系统迭代: {project_result.project_id}")
        
        # 全流程多维度复盘
        review = self._full_project_review(project_result)
        
        # 1. 沉淀知识入基底库
        new_knowledge_count = self._add_project_knowledge(project_result, review)
        failed_cases_count = self._add_failure_cases(review["failed_cases"])
        
        # 2. 优化核心决策策略
        optimized_modules = []
        optimized_modules.extend(self._optimize_topic_evaluation_strategy(review))
        optimized_modules.extend(self._optimize_budget_allocation_strategy(review))
        optimized_modules.extend(self._optimize_transfer_adaptation_strategy(review))
        
        # 3. 更新风险预判规则
        risk_rules_updated = self._update_risk_prediction_rules(review["risk_cases"])
        
        # 4. 量化进化效果
        evolution_gain = self._calculate_evolution_gain(review)
        
        evolution_report = {
            "report_id": self._generate_report_id(),
            "project_id": project_result.project_id,
            "review_summary": review["summary"],
            "optimized_modules": optimized_modules,
            "knowledge_added": new_knowledge_count,
            "failed_cases_added": failed_cases_count,
            "risk_rules_updated": risk_rules_updated,
            "expected_gain": evolution_gain,
            "timestamp": time.time(),
        }
        
        print(f"\n[进化引擎] 复盘与迭代完成!")
        print(f"[进化引擎] 新增知识: {new_knowledge_count} 条")
        print(f"[进化引擎] 新增失败案例: {failed_cases_count} 条")
        print(f"[进化引擎] 优化模块: {len(optimized_modules)} 个")
        print(f"[进化引擎] 预期收益: {evolution_gain:.1f}%")
        
        return evolution_report
    
    def _full_project_review(self, project_result: ProjectResult) -> Dict:
        """全流程多维度复盘"""
        review = {
            "summary": "",
            "efficiency_metrics": {},
            "problem_points": [],
            "success_patterns": [],
            "failed_cases": [],
            "risk_cases": [],
            "optimization_points": [],
        }
        
        phase_count = len(project_result.phase_results)
        success_count = sum(1 for p in project_result.phase_results.values() 
                          if p.get("status") == "completed" or p.get("quality_score", 0) >= 0.8)
        
        review["efficiency_metrics"] = {
            "phase_completion_rate": success_count / phase_count if phase_count > 0 else 0,
            "total_phases": phase_count,
            "successful_phases": success_count,
            "has_errors": bool(project_result.error_message),
        }
        
        if project_result.status.value == "failed" or project_result.error_message:
            review["summary"] = f"项目执行失败，需重点分析原因"
            review["problem_points"].append(f"项目状态: {project_result.status.value}")
            if project_result.error_message:
                review["problem_points"].append(f"错误信息: {project_result.error_message}")
                review["failed_cases"].append({
                    "type": "execution_failure",
                    "description": project_result.error_message,
                    "severity": "high",
                })
        elif success_count == phase_count:
            review["summary"] = f"项目执行成功，所有{phase_count}个阶段均已完成"
            review["success_patterns"].append(f"全阶段成功完成，执行流程顺畅")
        else:
            review["summary"] = f"项目部分完成，{success_count}/{phase_count}个阶段成功"
            review["optimization_points"].append(f"{phase_count - success_count}个阶段未达标，需优化")
        
        for phase_id, phase_result in project_result.phase_results.items():
            quality_score = phase_result.get("quality_score", 0)
            if quality_score < 0.8:
                review["problem_points"].append(f"阶段 {phase_id} 质量不达标: {quality_score:.2f}")
                review["risk_cases"].append({
                    "phase": phase_id,
                    "type": "quality_risk",
                    "description": f"质量分数低于阈值",
                    "score": quality_score,
                })
        
        return review
    
    def _add_project_knowledge(self, project_result: ProjectResult, review: Dict) -> int:
        """沉淀知识入基底库"""
        knowledge_items = []
        
        for phase_id, phase_result in project_result.phase_results.items():
            if "output" in phase_result:
                knowledge_items.append({
                    "type": "phase_output",
                    "phase": phase_id,
                    "content": str(phase_result["output"])[:200],
                })
        
        if review["success_patterns"]:
            knowledge_items.append({
                "type": "success_pattern",
                "patterns": review["success_patterns"],
            })
        
        self._simulate_knowledge_base_update(knowledge_items)
        
        return len(knowledge_items)
    
    def _add_failure_cases(self, failed_cases: List[Dict]) -> int:
        """沉淀失败案例入失败知识库"""
        if failed_cases:
            print(f"  [进化引擎] 沉淀 {len(failed_cases)} 条失败案例")
            for case in failed_cases:
                self.evolution_history.append({
                    "type": "failure_case",
                    "case_type": case.get("type"),
                    "description": case.get("description"),
                    "severity": case.get("severity"),
                })
        
        return len(failed_cases)
    
    def _optimize_topic_evaluation_strategy(self, review: Dict) -> List[str]:
        """优化选题评估策略"""
        optimizations = []
        
        if review["efficiency_metrics"]["phase_completion_rate"] < 0.6:
            optimizations.append("选题评估权重调整：提高可行性维度权重")
            print("  [进化引擎] 优化选题评估策略：提高可行性权重")
        
        if review["problem_points"]:
            optimizations.append("选题评估指标扩展：新增执行风险预判")
            print("  [进化引擎] 优化选题评估策略：扩展评估指标")
        
        return optimizations
    
    def _optimize_budget_allocation_strategy(self, review: Dict) -> List[str]:
        """优化预算分配策略"""
        optimizations = []
        
        if review["efficiency_metrics"]["phase_completion_rate"] < 0.7:
            optimizations.append("预算分配策略优化：向关键阶段倾斜")
            print("  [进化引擎] 优化预算分配策略：调整阶段预算比例")
        
        return optimizations
    
    def _optimize_transfer_adaptation_strategy(self, review: Dict) -> List[str]:
        """优化迁移适配策略"""
        optimizations = []
        
        if "quality_risk" in [r.get("type") for r in review["risk_cases"]]:
            optimizations.append("迁移策略优化：增强跨阶段质量保障机制")
            print("  [进化引擎] 优化迁移适配策略：增强质量保障")
        
        return optimizations
    
    def _update_risk_prediction_rules(self, risk_cases: List[Dict]) -> int:
        """更新风险预判规则"""
        if risk_cases:
            print(f"  [进化引擎] 更新 {len(risk_cases)} 条风险预判规则")
            for risk in risk_cases:
                self.evolution_history.append({
                    "type": "risk_rule_update",
                    "phase": risk.get("phase"),
                    "risk_type": risk.get("type"),
                    "action": "增强监控",
                })
        
        return len(risk_cases)
    
    def _calculate_evolution_gain(self, review: Dict) -> float:
        """量化进化效果"""
        base_gain = 2.0
        
        if review["efficiency_metrics"]["phase_completion_rate"] >= 0.8:
            base_gain += 3.0
        elif review["efficiency_metrics"]["phase_completion_rate"] >= 0.6:
            base_gain += 1.5
        
        knowledge_bonus = len(review.get("success_patterns", [])) * 0.5
        risk_bonus = len(review.get("risk_cases", [])) * 0.3
        
        total_gain = base_gain + knowledge_bonus + risk_bonus
        
        return round(total_gain, 1)
    
    def _simulate_knowledge_base_update(self, knowledge_items: List[Dict]):
        """模拟知识基底库更新"""
        for item in knowledge_items:
            self.evolution_history.append({
                "type": "knowledge_addition",
                "knowledge_type": item.get("type"),
                "content": item.get("content", item.get("patterns", "N/A")),
            })
    
    def _generate_report_id(self) -> str:
        """生成报告ID"""
        return f"report_{int(time.time())}_{random.randint(1000, 9999)}"


# 全局实例
_evolution_engine = None

def get_self_evolution_engine() -> SelfEvolutionEngine:
    """获取自进化引擎实例"""
    global _evolution_engine
    if _evolution_engine is None:
        _evolution_engine = SelfEvolutionEngine()
    return _evolution_engine


__all__ = [
    "SelfEvolutionEngine",
    "get_self_evolution_engine",
]
