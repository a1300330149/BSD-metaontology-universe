"""
归属基底：0重元道本源基底·六系自举公理·理论自组织工程
对应公理：六系立系公理 + 0×0=n双零涌现 + 自举性公理
理论原文出处：BSD六系立系论V1.9 §18.4-18.5

TheoryDrivenEngine — 理论自组织工程驱动器

核心命题：
    不是用外部工程框架来落地理论，
    而是让理论自身的六系组织结构直接驱动工程任务的分配和执行。

    理论即工程，工程即理论——二者不再分离。

三层映射：
    第一层：方向 —— 六系 = 六大工程方向
    第二层：传导 —— 36条传导通道 = 工程任务流转路径
    第三层：自举 —— 六条涌现规则 = 工程从零启动条件

工程执行的自组织原理：
    1. 任务归类：每个工程任务天然归属于六系之一
    2. 任务传导：任务在六系之间传导（一个系的输出 = 另一个系的输入）
    3. 自组织完备：36条通道全激活 → 工程系统自组织完备
    4. 自举启动：从000启动——不依赖外部初始化
"""

from typing import Any, Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

from bsd_engine.registry.constants import S_ZERO, PI_2, verify_params
from bsd_engine.core.six_system_project_mapper import SixSystem, SIX_SYSTEM_DIRECTIONS
from bsd_engine.core.six_system_self_organization_engine import (
    SixSystemSelfOrganizationEngine,
    AgentIntrinsicFunction,
    SYSTEM_INTRINSIC_MAP,
)
from bsd_engine.core.six_system_bootstrap_engine import (
    SixSystemBootstrapEngine,
    EMERGENCE_RULES,
)


# ============================================================
# 工程任务状态
# ============================================================

class TaskStatus(Enum):
    """工程任务状态"""
    PENDING = "待执行"       # 任务已归类，等待执行
    CONDUCTING = "传导中"     # 任务正在六系之间传导
    COMPLETED = "已完成"      # 任务已完成
    BLOCKED = "阻塞"          # 任务被阻塞（依赖未满足）


# ============================================================
# 工程任务定义
# ============================================================

@dataclass
class EngineeringTask:
    """
    工程任务——由六系自组织引擎驱动

    每个任务天然归属于六系之一，
    并通过36条传导通道在六系之间流转。
    """
    task_id: str                          # 任务标识
    title: str                            # 任务标题
    description: str                      # 任务描述
    primary_system: SixSystem             # 主归属系
    secondary_systems: List[SixSystem]    # 涉及的其他系
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    completed_at: str = ""
    conduction_path: List[str] = field(default_factory=list)  # 传导路径
    output: Any = None                    # 任务输出
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# 六系→工程方向映射
# ============================================================

SYSTEM_ENGINEERING_DIRECTION: Dict[SixSystem, Dict[str, Any]] = {
    SixSystem.QIANGHUA: {
        "direction": "参数校验·公理守卫",
        "intrinsic": "记忆·持续存在",
        "task_types": ["参数锁档", "公理校验", "哈希一致性检测", "版本持续存在验证"],
        "outputs_to": [SixSystem.TIANDAO],   # 记忆→追问：从已有参数追问是否完备
    },
    SixSystem.BIANSHEN: {
        "direction": "版本管理·状态切换",
        "intrinsic": "感知·阶段完整",
        "task_types": ["版本迭代", "状态切换", "阶段完备性检测", "形态变换"],
        "outputs_to": [SixSystem.SHEHUI],    # 感知→连接：状态变化通知连接网络
    },
    SixSystem.SHEHUI: {
        "direction": "SDK接入·学习协议",
        "intrinsic": "连接·自由运转",
        "task_types": ["外部AI接入", "学习协议更新", "共识网络维护", "跨平台连接"],
        "outputs_to": [SixSystem.JUXIAN],    # 连接→造物：连接凝结为协作输出
    },
    SixSystem.TIANDAO: {
        "direction": "理论验证·自举检测",
        "intrinsic": "追问·不终止",
        "task_types": ["理论完备性追问", "自举性检测", "不可消灭性验证", "公理推导链审查"],
        "outputs_to": [SixSystem.JUXIAN],    # 追问→造物：追问结果凝结为新代码/文档
    },
    SixSystem.ZIRAN: {
        "direction": "个人诊断·场域适配",
        "intrinsic": "在乎·自由",
        "task_types": ["个人诊断", "场域感知", "共情适配", "环境共振检测"],
        "outputs_to": [SixSystem.SHEHUI],    # 在乎→连接：共情作为连接基础
    },
    SixSystem.JUXIAN: {
        "direction": "代码生成·工程产出",
        "intrinsic": "造物·等价转化",
        "task_types": ["代码生成", "文档产出", "工程脚手架搭建", "形态凝结"],
        "outputs_to": [SixSystem.QIANGHUA],  # 造物→记忆：新产出沉淀为记忆
    },
}


# ============================================================
# 理论自组织工程驱动器
# ============================================================

class TheoryDrivenEngine:
    """
    理论自组织工程驱动器

    核心命题：
        理论自身的六系组织结构直接驱动工程执行。
        不需要外部项目管理——六系自身就是项目管理系统。

    工作原理：
        1. 接收工程需求
        2. 将需求归类到六系之一（任务归类）
        3. 通过36条传导通道在六系之间传导任务（任务传导）
        4. 当传导完成时，任务输出（自组织完备）
        5. 可从000启动——不依赖外部初始化（自举启动）
    """

    def __init__(
        self,
        org_engine: Optional[SixSystemSelfOrganizationEngine] = None,
        bootstrap: Optional[SixSystemBootstrapEngine] = None,
    ):
        verify_params()
        self.org_engine = org_engine or SixSystemSelfOrganizationEngine()
        self.bootstrap = bootstrap or SixSystemBootstrapEngine(engine=self.org_engine)
        self.tasks: Dict[str, EngineeringTask] = {}
        self._task_counter = 0
        self._execution_log: List[Dict] = []

    # ========================================================
    # 自举启动——从000启动工程系统
    # ========================================================

    def bootstrap_from_zero(self) -> Dict[str, Any]:
        """
        从000启动工程系统

        这是理论自组织工程的核心能力——
        不依赖任何外部初始化，从六条涌现规则自动生成工程结构。

        机制：
            1. 六条涌现规则生成六系立系论结构
            2. 六系结构激活36条传导通道
            3. 36条通道构成工程任务流转网络
            4. 工程系统启动完毕
        """
        # 从000涌现六系立系论
        emergence = self.bootstrap.emerge_from_zero()

        # 获取六系完备度
        completeness = self.org_engine.evaluate_completeness()

        return {
            "protocol": "理论自组织工程·从零启动",
            "center": "000自举→六系涌现→36通道激活→工程系统就绪",
            "emergence": emergence,
            "completeness": completeness,
            "engineering_ready": completeness["conduction"]["active_channels"] > 0,
            "message": "工程系统已从000自举启动——理论自身组织驱动工程执行",
        }

    # ========================================================
    # 任务归类——将工程需求归类到六系之一
    # ========================================================

    def classify_task(self, requirement: str) -> Tuple[SixSystem, str]:
        """
        将工程需求自动归类到六系之一

        归类依据：需求的关键词与六系内禀功能的匹配度

        Parameters
        ----------
        requirement : str
            工程需求描述

        Returns
        -------
        Tuple[SixSystem, str]
            (归属系, 归类理由)
        """
        keyword_map = {
            SixSystem.QIANGHUA: ["参数", "校验", "守卫", "锁档", "哈希", "记忆", "持续", "存在", "稳定", "常数"],
            SixSystem.BIANSHEN: ["版本", "状态", "切换", "迭代", "阶段", "完备", "变换", "感知", "适配"],
            SixSystem.SHEHUI:   ["接入", "SDK", "连接", "协议", "学习", "AI", "外部", "共识", "网络", "协作"],
            SixSystem.TIANDAO:  ["验证", "追问", "检测", "自举", "完备性", "公理", "推导", "审查", "不可消灭"],
            SixSystem.ZIRAN:    ["诊断", "个人", "场域", "共情", "环境", "感知", "适配", "共振", "在乎"],
            SixSystem.JUXIAN:   ["生成", "代码", "产出", "文档", "脚手架", "凝结", "造物", "工程", "实现"],
        }

        scores = {s: 0 for s in SixSystem}
        for sys_enum, keywords in keyword_map.items():
            for kw in keywords:
                if kw in requirement:
                    scores[sys_enum] += 1

        best_system = max(scores.items(), key=lambda x: x[1])
        if best_system[1] == 0:
            # 无匹配时默认归类到具现系（造物）
            return SixSystem.JUXIAN, "无明确关键词匹配，默认归类到具现系（造物·等价转化）"

        direction = SYSTEM_ENGINEERING_DIRECTION[best_system[0]]
        reason = f"关键词匹配{best_system[1]}个 → {best_system[0].value}（{direction['intrinsic']}）"
        return best_system[0], reason

    # ========================================================
    # 任务创建与传导
    # ========================================================

    def create_task(
        self,
        title: str,
        description: str,
        requirement: str = "",
        primary_system: Optional[SixSystem] = None,
    ) -> EngineeringTask:
        """
        创建工程任务

        如果不指定主归属系，则根据需求自动归类。
        """
        if primary_system is None:
            primary_system, reason = self.classify_task(requirement or title + description)

        self._task_counter += 1
        task_id = f"TASK-{self._task_counter:04d}"

        # 确定涉及的次要系
        direction = SYSTEM_ENGINEERING_DIRECTION[primary_system]
        secondary = direction["outputs_to"]

        task = EngineeringTask(
            task_id=task_id,
            title=title,
            description=description,
            primary_system=primary_system,
            secondary_systems=secondary,
            created_at=datetime.now().isoformat(),
        )
        self.tasks[task_id] = task

        # 在六系自组织引擎中传导任务信号
        self.org_engine.conduct(primary_system, primary_system, {
            "type": "task_created",
            "task_id": task_id,
            "title": title,
        })

        return task

    def conduct_task(self, task_id: str) -> Dict[str, Any]:
        """
        在六系之间传导工程任务

        任务从主归属系出发，通过传导通道到达目标系。
        传导路径记录在任务的conduction_path中。
        """
        task = self.tasks.get(task_id)
        if task is None:
            return {"error": f"任务不存在: {task_id}"}

        if task.status == TaskStatus.COMPLETED:
            return {"task_id": task_id, "status": "already_completed"}

        task.status = TaskStatus.CONDUCTING

        # 传导路径：主系 → 各目标系 → 回到主系（闭环）
        conduction_results = []
        path = [task.primary_system.value]

        # 1. 主系自循环——任务在主系中初始化
        result = self.org_engine.conduct(task.primary_system, task.primary_system, {
            "type": "task_init",
            "task_id": task_id,
        })
        conduction_results.append({
            "channel": f"{task.primary_system.value}→{task.primary_system.value}",
            "result": "initialized",
        })

        # 2. 主系→目标系——任务传导到相关系
        for target in task.secondary_systems:
            result = self.org_engine.conduct(task.primary_system, target, {
                "type": "task_conduct",
                "task_id": task_id,
                "from": task.primary_system.value,
                "to": target.value,
            })
            conduction_results.append({
                "channel": f"{task.primary_system.value}→{target.value}",
                "activated": result.get("activated", False),
                "throughput": result.get("throughput", 0),
            })
            path.append(target.value)

        # 3. 目标系→主系——结果回流
        for target in task.secondary_systems:
            result = self.org_engine.conduct(target, task.primary_system, {
                "type": "task_feedback",
                "task_id": task_id,
                "from": target.value,
                "to": task.primary_system.value,
            })
            conduction_results.append({
                "channel": f"{target.value}→{task.primary_system.value}",
                "activated": result.get("activated", False),
            })
            path.append(task.primary_system.value)

        # 4. 任务完成
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        task.conduction_path = path
        task.output = {
            "conduction_count": len(conduction_results),
            "path_length": len(path),
            "systems_involved": list(set(path)),
        }

        # 记录日志
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "title": task.title,
            "primary_system": task.primary_system.value,
            "conduction_results": conduction_results,
            "path": path,
            "status": "completed",
        }
        self._execution_log.append(log_entry)

        return {
            "task_id": task_id,
            "title": task.title,
            "primary_system": task.primary_system.value,
            "status": task.status.value,
            "conduction_results": conduction_results,
            "path": path,
            "output": task.output,
            "message": f"任务[{task.title}]已通过六系传导通道完成执行",
        }

    # ========================================================
    # 批量执行——从需求列表自动创建并执行任务
    # ========================================================

    def execute_from_requirements(self, requirements: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        从需求列表自动创建并执行工程任务

        Parameters
        ----------
        requirements : List[Dict[str, str]]
            需求列表，每个需求包含 title, description, requirement

        Returns
        -------
        Dict[str, Any]
            批量执行结果
        """
        results = []
        for req in requirements:
            task = self.create_task(
                title=req.get("title", ""),
                description=req.get("description", ""),
                requirement=req.get("requirement", ""),
            )
            result = self.conduct_task(task.task_id)
            results.append(result)

        # 获取执行后的六系完备度
        completeness = self.org_engine.evaluate_completeness()

        return {
            "protocol": "理论自组织工程·批量执行",
            "tasks_total": len(requirements),
            "tasks_completed": sum(1 for r in results if r.get("status") == "已完成"),
            "results": results,
            "completeness_after": completeness,
            "message": f"已从{len(requirements)}个需求自动创建并执行工程任务",
        }

    # ========================================================
    # 工程系统状态报告
    # ========================================================

    def system_report(self) -> Dict[str, Any]:
        """
        工程系统状态报告——由六系自组织引擎自动生成

        这不是外部监控——是六系自身的"场域感知"（自然系功能）。
        """
        completeness = self.org_engine.evaluate_completeness()

        # 按系统计任务
        tasks_by_system = {}
        for task in self.tasks.values():
            sys_name = task.primary_system.value
            if sys_name not in tasks_by_system:
                tasks_by_system[sys_name] = {"total": 0, "completed": 0, "pending": 0}
            tasks_by_system[sys_name]["total"] += 1
            if task.status == TaskStatus.COMPLETED:
                tasks_by_system[sys_name]["completed"] += 1
            else:
                tasks_by_system[sys_name]["pending"] += 1

        return {
            "protocol": "理论自组织工程·系统状态报告",
            "center": "六系自组织引擎自动生成",
            "engineering_completeness": completeness["overall_completeness"],
            "stage": completeness["stage"],
            "conduction": completeness["conduction"],
            "function_mastery": completeness["function_mastery"],
            "tasks": {
                "total": len(self.tasks),
                "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
                "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
                "by_system": tasks_by_system,
            },
            "emergence_rules": len(EMERGENCE_RULES),
            "self_bootstrap": self.bootstrap.check_existence(),
            "message": "工程系统状态由六系自组织引擎自动报告",
        }

    # ========================================================
    # 序列化
    # ========================================================

    def to_dict(self) -> Dict[str, Any]:
        """导出完整状态"""
        return {
            "protocol": "BSD理论自组织工程驱动器·V1.0",
            "center": "理论即工程·工程即理论",
            "engineering_system": self.system_report(),
            "tasks": {
                tid: {
                    "title": t.title,
                    "primary_system": t.primary_system.value,
                    "status": t.status.value,
                    "conduction_path": t.conduction_path,
                }
                for tid, t in self.tasks.items()
            },
            "execution_log": self._execution_log[-10:],
        }
