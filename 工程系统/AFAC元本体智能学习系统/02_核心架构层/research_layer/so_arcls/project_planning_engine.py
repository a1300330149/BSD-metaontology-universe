"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：天道秩序
对应公理：第2条（全域九维法理公理）、第4条（选题创化生成机制）、第6条（全局宿命边界统摄理论）
对应九维维度：天道原理/天道动力学/创化社会/因果社会
理论原文出处：theory_base/六阶自主科研闭环系统（SO-ARCLS）工程化完整设计文档.md
核心数理参数：γ=0.92（衰减系数）, κ=0.35（耦合强度）

SO-ARCLS - 项目自主规划与调度引擎

理论溯源：自主科研闭环动力学的项目层调度规则

核心职责：
1. 项目里程碑拆解：将立项选题自动拆解为实验设计、数据准备、迭代优化、成果产出、落地验证等阶段里程碑
2. 全局资源规划：自动分配算力预算、时间节点、调度优先级，匹配最优资源配置
3. 任务依赖编排：梳理各任务的前后置依赖关系，生成无冲突的最优执行链路
4. 动态进度管控：实时跟踪项目进度，自动识别延期风险、卡点问题并调整执行计划
5. 多项目并行调度：支持多个科研项目并行管理，按优先级全局统筹资源分配

理论映射：
- ProjectPlanningEngine：对应自主科研闭环动力学公理（公理二）
- _decompose_project_milestones：对应选题创化生成机制（公理四）
- _allocate_phase_budget：对应科研价值边际判定公理（公理三）
- _generate_project_risk_plan：对应全局宿命边界统摄理论（公理六）
"""

import time
import random
from typing import Dict, List, Optional, Any

from .types import (
    TopicItem, ResearchPlan, Project, ProjectStatus, AutoMode,
    ExecutionRecord, Milestone, TaskNode, ProjectPlan,
)


class ProjectPlanningEngine:
    """
    功能：项目自主规划与调度引擎
    理论映射：对应自主科研闭环动力学公理（公理二）、选题创化生成机制（公理四）
    """
    
    PHASES_TEMPLATE = {
        "basic_research": [
            {"phase": "文献调研", "duration": 4, "resources": ["算力", "文献库"], "output": "文献综述", "type": "preparation"},
            {"phase": "理论建模", "duration": 6, "resources": ["算力", "专家咨询"], "output": "理论框架", "type": "design"},
            {"phase": "仿真验证", "duration": 4, "resources": ["算力"], "output": "仿真结果", "type": "experiment"},
            {"phase": "理论分析", "duration": 3, "resources": ["专家咨询"], "output": "理论结论", "type": "analysis"},
            {"phase": "论文撰写", "duration": 4, "resources": ["写作工具"], "output": "学术论文", "type": "output"},
        ],
        "applied_research": [
            {"phase": "问题分析", "duration": 2, "resources": ["领域专家"], "output": "问题定义", "type": "preparation"},
            {"phase": "方法设计", "duration": 4, "resources": ["算力", "专家"], "output": "方法方案", "type": "design"},
            {"phase": "实验验证", "duration": 6, "resources": ["算力", "数据集"], "output": "实验结果", "type": "experiment"},
            {"phase": "结果分析", "duration": 3, "resources": ["专家"], "output": "分析报告", "type": "analysis"},
            {"phase": "论文撰写", "duration": 4, "resources": ["写作工具"], "output": "学术论文", "type": "output"},
        ],
        "engineering_opt": [
            {"phase": "需求分析", "duration": 2, "resources": ["用户反馈"], "output": "需求文档", "type": "preparation"},
            {"phase": "方案设计", "duration": 3, "resources": ["工程师"], "output": "技术方案", "type": "design"},
            {"phase": "开发实现", "duration": 6, "resources": ["算力", "工程师"], "output": "原型系统", "type": "experiment"},
            {"phase": "测试优化", "duration": 4, "resources": ["测试资源"], "output": "优化版本", "type": "analysis"},
            {"phase": "部署落地", "duration": 3, "resources": ["运维资源"], "output": "部署文档", "type": "landing"},
        ],
        "cross_innovation": [
            {"phase": "跨域调研", "duration": 4, "resources": ["多领域专家"], "output": "跨域综述", "type": "preparation"},
            {"phase": "融合设计", "duration": 5, "resources": ["多领域专家", "算力"], "output": "融合方案", "type": "design"},
            {"phase": "实验验证", "duration": 6, "resources": ["算力", "多领域数据"], "output": "实验结果", "type": "experiment"},
            {"phase": "创新评估", "duration": 3, "resources": ["专家评审"], "output": "创新报告", "type": "analysis"},
            {"phase": "成果输出", "duration": 4, "resources": ["写作工具"], "output": "论文/专利", "type": "output"},
        ],
    }
    
    RISK_TYPES = [
        {"type": "技术风险", "description": "核心技术无法突破", "impact": 0.8, "probability": 0.3},
        {"type": "数据风险", "description": "数据质量不足或获取困难", "impact": 0.6, "probability": 0.4},
        {"type": "时间风险", "description": "进度滞后", "impact": 0.5, "probability": 0.5},
        {"type": "资源风险", "description": "算力/人力不足", "impact": 0.7, "probability": 0.2},
        {"type": "竞争风险", "description": "同类研究抢先发表", "impact": 0.9, "probability": 0.2},
    ]
    
    def __init__(self):
        self.plan_counter = 0
        self.project_counter = 0
    
    def plan_research_project(self, topic: TopicItem,
                              total_budget: int,
                              mode: AutoMode = AutoMode.FULL_AUTO) -> ProjectPlan:
        """
        为选定选题生成完整项目执行规划（核心函数）
        
        Args:
            topic: 选题项
            total_budget: 总预算（万元）
            mode: 自主运行模式
            
        Returns:
            ProjectPlan: 项目计划
        """
        print(f"\n[规划引擎] 为选题 '{topic.content[:30]}...' 生成完整项目执行规划")
        print(f"[规划引擎] 总预算: {total_budget}万元, 模式: {mode.value}")
        
        # 拆解项目阶段与里程碑
        milestones = self._decompose_project_milestones(topic)
        
        # 各阶段预算与时间分配
        budget_allocation = self._allocate_phase_budget(milestones, total_budget)
        timeline_allocation = self._allocate_phase_timeline(milestones, topic.expected_cycle)
        
        # 编排任务依赖关系，生成执行链路
        task_graph = self._build_task_dependency_graph(milestones)
        
        # 设置人工干预节点（半自主模式下）
        checkpoints = []
        if mode != AutoMode.FULL_AUTO:
            checkpoints = self._generate_human_checkpoints(milestones, mode)
        
        # 生成风险预案
        risk_plan = self._generate_project_risk_plan(topic, milestones)
        
        project_plan = ProjectPlan(
            project_id=self._generate_project_id(),
            topic=topic,
            milestones=milestones,
            budget_plan=budget_allocation,
            timeline=timeline_allocation,
            task_graph=task_graph,
            human_checkpoints=checkpoints,
            risk_plan=risk_plan,
            mode=mode,
            total_budget=total_budget,
        )
        
        print(f"[规划引擎] 项目规划完成: {project_plan.project_id}")
        print(f"[规划引擎] 里程碑数: {len(milestones)}, 任务数: {len(task_graph)}")
        
        return project_plan
    
    def create_project_plan(self, topic_item: TopicItem,
                            constraints: Optional[Dict] = None) -> ResearchPlan:
        """
        基于选题生成详细科研计划（兼容旧接口）
        
        Args:
            topic_item: 选题项
            constraints: 约束条件
            
        Returns:
            ResearchPlan: 科研计划
        """
        print(f"\n[规划引擎] 为选题 '{topic_item.content[:30]}...' 创建计划")
        
        if constraints is None:
            constraints = {}
        
        phases_template = self.PHASES_TEMPLATE.get(
            topic_item.topic_type.value,
            self.PHASES_TEMPLATE["applied_research"]
        )
        
        phases = []
        current_month = 0
        for template in phases_template:
            phase = {
                "phase_name": template["phase"],
                "start_month": current_month,
                "duration": template["duration"],
                "end_month": current_month + template["duration"],
                "resources": template["resources"],
                "expected_output": template["output"],
                "status": "pending",
                "type": template["type"],
            }
            phases.append(phase)
            current_month += template["duration"]
        
        resource_allocation = self._allocate_resources(topic_item, phases)
        milestones = self._set_milestones(phases)
        risks = self._identify_risks(topic_item, phases)
        
        plan = ResearchPlan(
            plan_id=self._generate_plan_id(),
            topic_item=topic_item,
            phases=phases,
            resource_allocation=resource_allocation,
            milestones=milestones,
            risks=risks,
        )
        
        print(f"[规划引擎] 计划创建完成，共 {len(phases)} 个阶段，预计 {current_month} 个月")
        return plan
    
    def create_project(self, topic_item: TopicItem, auto_mode: AutoMode,
                       constraints: Optional[Dict] = None) -> Project:
        """
        创建科研项目
        
        Args:
            topic_item: 选题项
            auto_mode: 自主运行模式
            constraints: 约束条件
            
        Returns:
            Project: 科研项目
        """
        plan = self.create_project_plan(topic_item, constraints)
        
        project = Project(
            project_id=self._generate_project_id(),
            topic_item=topic_item,
            plan=plan,
            status=ProjectStatus.PLANNING,
            auto_mode=auto_mode,
            execution_history=[],
            artifacts={},
        )
        
        print(f"[规划引擎] 项目创建完成: {project.project_id}")
        return project
    
    def _decompose_project_milestones(self, topic: TopicItem) -> List[Milestone]:
        """
        拆解项目阶段与里程碑
        
        Args:
            topic: 选题项
            
        Returns:
            List[Milestone]: 里程碑列表
        """
        phases_template = self.PHASES_TEMPLATE.get(
            topic.topic_type.value,
            self.PHASES_TEMPLATE["applied_research"]
        )
        
        milestones = []
        dependencies = []
        current_month = 0
        
        for i, template in enumerate(phases_template):
            milestone_id = f"ms_{i+1}"
            
            milestone = Milestone(
                milestone_id=milestone_id,
                name=f"{template['phase']}完成",
                milestone_type=template["type"],
                deadline_month=current_month + template["duration"],
                status="pending",
                associated_phase=template["phase"],
                dependencies=dependencies.copy(),
                quality_threshold=0.8,
            )
            
            milestones.append(milestone)
            dependencies.append(milestone_id)
            current_month += template["duration"]
        
        return milestones
    
    def _allocate_phase_budget(self, milestones: List[Milestone],
                               total_budget: int) -> Dict:
        """
        各阶段预算分配
        
        Args:
            milestones: 里程碑列表
            total_budget: 总预算
            
        Returns:
            Dict: 预算分配方案
        """
        budget_plan = {
            "total": total_budget,
            "phase_budgets": {},
            "resource_budgets": {
                "算力": 0,
                "人力": 0,
                "数据": 0,
                "其他": 0,
            },
        }
        
        weights = {
            "preparation": 0.15,
            "design": 0.20,
            "experiment": 0.35,
            "analysis": 0.15,
            "output": 0.10,
            "landing": 0.15,
        }
        
        for milestone in milestones:
            weight = weights.get(milestone.milestone_type, 0.2)
            budget_plan["phase_budgets"][milestone.name] = round(total_budget * weight, 1)
            
            if milestone.milestone_type == "experiment":
                budget_plan["resource_budgets"]["算力"] += total_budget * weight * 0.6
                budget_plan["resource_budgets"]["数据"] += total_budget * weight * 0.2
            elif milestone.milestone_type == "design":
                budget_plan["resource_budgets"]["人力"] += total_budget * weight * 0.7
            elif milestone.milestone_type == "preparation":
                budget_plan["resource_budgets"]["人力"] += total_budget * weight * 0.5
        
        for key in budget_plan["resource_budgets"]:
            budget_plan["resource_budgets"][key] = round(budget_plan["resource_budgets"][key], 1)
        
        return budget_plan
    
    def _allocate_phase_timeline(self, milestones: List[Milestone],
                                 expected_cycle: int) -> Dict:
        """
        各阶段时间分配
        
        Args:
            milestones: 里程碑列表
            expected_cycle: 预期周期（月）
            
        Returns:
            Dict: 时间线分配方案
        """
        timeline = {
            "total_months": expected_cycle,
            "milestone_deadlines": {},
            "gantt_chart": [],
        }
        
        total_duration = sum(m.deadline_month for m in milestones) / len(milestones) * len(milestones)
        scaling_factor = expected_cycle / total_duration if total_duration > 0 else 1
        
        current_month = 0
        for milestone in milestones:
            duration = round(milestone.deadline_month / len(milestones) * scaling_factor, 1)
            end_month = current_month + duration
            
            timeline["milestone_deadlines"][milestone.name] = {
                "start_month": round(current_month, 1),
                "duration": duration,
                "end_month": round(end_month, 1),
            }
            
            timeline["gantt_chart"].append({
                "milestone_id": milestone.milestone_id,
                "name": milestone.name,
                "start": round(current_month, 1),
                "end": round(end_month, 1),
            })
            
            current_month = end_month
        
        return timeline
    
    def _build_task_dependency_graph(self, milestones: List[Milestone]) -> List[TaskNode]:
        """
        编排任务依赖关系，生成执行链路
        
        Args:
            milestones: 里程碑列表
            
        Returns:
            List[TaskNode]: 任务节点列表（含依赖关系）
        """
        task_graph = []
        task_counter = 0
        
        for milestone in milestones:
            for task_name in self._get_tasks_for_milestone(milestone):
                task_counter += 1
                
                task = TaskNode(
                    task_id=f"task_{task_counter:04d}",
                    name=task_name,
                    phase=milestone.associated_phase,
                    dependencies=milestone.dependencies.copy(),
                    resources=self._get_resources_for_task(task_name, milestone),
                    duration=round(milestone.deadline_month / 3),
                    priority=len(milestone.dependencies) + 1,
                )
                
                task_graph.append(task)
        
        return task_graph
    
    def _get_tasks_for_milestone(self, milestone: Milestone) -> List[str]:
        """获取里程碑对应的子任务"""
        task_map = {
            "preparation": ["文献收集", "领域调研", "问题定义", "数据初步分析"],
            "design": ["方案设计", "算法选型", "架构设计", "实验规划"],
            "experiment": ["数据准备", "模型训练", "结果验证", "对比实验"],
            "analysis": ["结果分析", "可视化", "结论提炼", "创新点总结"],
            "output": ["论文撰写", "图表制作", "格式排版", "投稿准备"],
            "landing": ["工程化改造", "性能优化", "部署方案", "验收测试"],
        }
        
        return task_map.get(milestone.milestone_type, ["核心任务"])
    
    def _get_resources_for_task(self, task_name: str, milestone: Milestone) -> List[str]:
        """获取任务所需资源"""
        resource_map = {
            "文献收集": ["文献库", "网络资源"],
            "领域调研": ["专家", "文献库"],
            "问题定义": ["专家", "数据"],
            "数据初步分析": ["算力", "数据"],
            "方案设计": ["专家", "算力"],
            "算法选型": ["专家", "文献"],
            "架构设计": ["工程师", "专家"],
            "实验规划": ["专家", "数据"],
            "数据准备": ["数据", "算力"],
            "模型训练": ["算力", "数据"],
            "结果验证": ["算力", "专家"],
            "对比实验": ["算力", "数据"],
            "结果分析": ["专家", "可视化工具"],
            "可视化": ["可视化工具", "算力"],
            "结论提炼": ["专家"],
            "创新点总结": ["专家"],
            "论文撰写": ["写作工具", "专家"],
            "图表制作": ["可视化工具"],
            "格式排版": ["写作工具"],
            "投稿准备": ["投稿系统", "专家"],
            "工程化改造": ["工程师", "算力"],
            "性能优化": ["工程师", "算力"],
            "部署方案": ["工程师", "运维"],
            "验收测试": ["测试资源", "专家"],
        }
        
        return resource_map.get(task_name, ["通用资源"])
    
    def _generate_human_checkpoints(self, milestones: List[Milestone],
                                    mode: AutoMode) -> List[str]:
        """
        生成人工干预节点
        
        Args:
            milestones: 里程碑列表
            mode: 自主运行模式
            
        Returns:
            List[str]: 人工检查点ID列表
        """
        checkpoints = []
        
        if mode == AutoMode.SEMI_AUTO:
            checkpoints = [m.milestone_id for m in milestones if m.milestone_type in ["design", "experiment", "output"]]
        elif mode == AutoMode.HUMAN_LOOP:
            checkpoints = [m.milestone_id for m in milestones]
        
        print(f"[规划引擎] 生成 {len(checkpoints)} 个人工检查点")
        return checkpoints
    
    def _generate_project_risk_plan(self, topic: TopicItem,
                                    milestones: List[Milestone]) -> List[Dict]:
        """
        生成风险预案
        
        Args:
            topic: 选题项
            milestones: 里程碑列表
            
        Returns:
            List[Dict]: 风险预案列表
        """
        risk_plan = []
        
        for risk_template in self.RISK_TYPES:
            if random.random() < risk_template["probability"]:
                risk = {
                    "risk_id": f"risk_{int(time.time())}_{len(risk_plan)}",
                    "type": risk_template["type"],
                    "description": risk_template["description"],
                    "impact": risk_template["impact"],
                    "probability": risk_template["probability"],
                    "affected_milestones": [m.milestone_id for m in milestones],
                    "mitigation": self._generate_mitigation(risk_template["type"]),
                    "trigger_condition": self._generate_trigger_condition(risk_template["type"], milestones),
                    "contingency_plan": self._generate_contingency_plan(risk_template["type"]),
                    "status": "identified",
                }
                risk_plan.append(risk)
        
        print(f"[规划引擎] 识别到 {len(risk_plan)} 项风险")
        return risk_plan
    
    def _generate_trigger_condition(self, risk_type: str, milestones: List[Milestone]) -> str:
        """生成风险触发条件"""
        conditions = {
            "技术风险": f"{milestones[1].name}进度滞后超过20%",
            "数据风险": f"{milestones[2].name}数据质量检查不通过",
            "时间风险": "任意里程碑延期超过1个月",
            "资源风险": "算力利用率持续低于30%或高于90%",
            "竞争风险": "监测到同类研究发表",
        }
        return conditions.get(risk_type, "项目进度异常")
    
    def _generate_contingency_plan(self, risk_type: str) -> str:
        """生成应急预案"""
        plans = {
            "技术风险": "启动B方案，调整研究方向，增加专家咨询频次",
            "数据风险": "切换备用数据源，实施数据增强策略，调整实验方案",
            "时间风险": "压缩非核心任务时间，并行执行可并行任务，申请资源追加",
            "资源风险": "弹性资源调度，优化算法效率，申请额外资源",
            "竞争风险": "加快成果整理，提前预印本发布，强化创新点突出",
        }
        return plans.get(risk_type, "启动应急响应流程")
    
    def _allocate_resources(self, topic_item: TopicItem, phases: List[Dict]) -> Dict:
        """资源分配（兼容旧接口）"""
        base_resources = {
            "算力": {"gpu_hours": 1000, "cpu_hours": 5000},
            "人力": {"researchers": 2, "engineers": 1},
            "预算": {"total": topic_item.expected_budget, "phases": {}},
        }
        
        phase_budget = topic_item.expected_budget / len(phases)
        for i, phase in enumerate(phases):
            base_resources["预算"]["phases"][phase["phase_name"]] = round(phase_budget, 1)
        
        if "大模型" in topic_item.content or "多模态" in topic_item.content:
            base_resources["算力"]["gpu_hours"] *= 3
            base_resources["预算"]["total"] *= 1.5
        
        return base_resources
    
    def _set_milestones(self, phases: List[Dict]) -> List[Dict]:
        """设定里程碑（兼容旧接口）"""
        milestones = []
        
        for i, phase in enumerate(phases):
            milestone = {
                "milestone_id": f"ms_{i+1}",
                "name": f"{phase['phase_name']}完成",
                "deadline_month": phase["end_month"],
                "status": "pending",
                "associated_phase": phase["phase_name"],
                "type": phase.get("type", "general"),
            }
            milestones.append(milestone)
        
        return milestones
    
    def _identify_risks(self, topic_item: TopicItem, phases: List[Dict]) -> List[Dict]:
        """识别风险（兼容旧接口）"""
        risks = []
        
        for risk_template in self.RISK_TYPES:
            if random.random() < risk_template["probability"]:
                risk = {
                    "risk_id": f"risk_{int(time.time())}_{len(risks)}",
                    "type": risk_template["type"],
                    "description": risk_template["description"],
                    "impact": risk_template["impact"],
                    "probability": risk_template["probability"],
                    "mitigation": self._generate_mitigation(risk_template["type"]),
                    "status": "identified",
                }
                risks.append(risk)
        
        return risks
    
    def _generate_mitigation(self, risk_type: str) -> str:
        """生成风险应对策略"""
        mitigations = {
            "技术风险": "预留20%缓冲时间，准备替代方案，定期技术评审",
            "数据风险": "提前数据质量评估，准备多数据源，数据增强策略",
            "时间风险": "细化任务分解，设置周进度检查点，并行任务安排",
            "资源风险": "提前资源预约，弹性资源调度，优化算法效率",
            "竞争风险": "加快实验进度，及时整理阶段性成果，预印本发布",
        }
        return mitigations.get(risk_type, "加强监控，及时调整计划")
    
    def _generate_plan_id(self) -> str:
        """生成计划ID"""
        self.plan_counter += 1
        return f"plan_{int(time.time())}_{self.plan_counter:04d}"
    
    def _generate_project_id(self) -> str:
        """生成项目ID"""
        self.project_counter += 1
        return f"proj_{int(time.time())}_{self.project_counter:04d}"


# 全局实例
_planning_engine = None

def get_project_planning_engine() -> ProjectPlanningEngine:
    """获取项目规划引擎实例"""
    global _planning_engine
    if _planning_engine is None:
        _planning_engine = ProjectPlanningEngine()
    return _planning_engine


__all__ = [
    "ProjectPlanningEngine",
    "get_project_planning_engine",
]
