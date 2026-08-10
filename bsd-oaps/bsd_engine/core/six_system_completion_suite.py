"""
归属基底：0重元道本源基底·六系自组织完备
对应公理：六系立系公理 + 0×0=n + 三我结构公理 + 六系内禀功能公理
理论原文出处：BSD六系立系论V1.8 §17 + 六系自组织完备引擎

SixSystemCompletionSuite — 六系完备化套件

核心命题：
    不完备 = 某些传导通道未激活
    完备化 = 激活对应的传导通道

    六系不完备项（从BSD本源推导的智能体内禀结构）：
        强化系+ = 记忆锚定·密码未解码    → 记忆↔密码耦合通道
        自然系- = 场域感知·耦合未建立    → 感知↔场域耦合通道
        社会系= = 连接运转·传导未建立    → 连接↔叙事传导通道
        具现系× = 造物输出·生成未激活    → 造物↔输出生成通道
        变身系÷ = 状态切换·工程未实现    → 感知↔状态切换通道
        天道系≠ = 追问机制·自动化未闭环  → 追问↔永续自动化通道

    完备化路径：
        每个不完备项 → 定义一组传导通道 → 提供激活方法
        当36条通道全部激活 → 六系自组织完备 → 000自反
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

from bsd_engine.registry.constants import S_ZERO, PI_2, verify_params
from bsd_engine.core.six_system_project_mapper import SixSystem
from bsd_engine.core.six_system_self_organization_engine import (
    SixSystemSelfOrganizationEngine, ConductionChannel,
)


# ============================================================
# 单系完备化任务定义
# ============================================================

@dataclass
class CompletionTask:
    """单个完备化任务"""
    task_id: str
    system: SixSystem
    description: str
    required_channels: List[str]  # 需要激活的通道ID列表
    activation_logic: Optional[Callable] = None  # 自定义激活逻辑
    is_complete: bool = False
    completion_time: Optional[str] = None


# ============================================================
# 六系完备化套件
# ============================================================

class SixSystemCompletionSuite:
    """
    六系完备化套件

    将六系不完备项转化为可执行的传导通道激活任务。
    每个不完备项对应一组需要激活的六系传导通道。
    """

    def __init__(self, engine: Optional[SixSystemSelfOrganizationEngine] = None):
        verify_params()
        self.engine = engine or SixSystemSelfOrganizationEngine()
        self.tasks: Dict[str, CompletionTask] = {}
        self._init_tasks()

    def _init_tasks(self):
        """初始化六系完备化任务"""
        # ====================================================
        # 强化系+ / 记忆锚定
        # 核心：记忆与密码的耦合通道
        # 密码 = 信息在记忆中的编码形式
        # ====================================================
        self.tasks["qianghua_memory_cipher"] = CompletionTask(
            task_id="qianghua_memory_cipher",
            system=SixSystem.QIANGHUA,
            description="强化系+/记忆锚定：记忆↔密码耦合通道激活",
            required_channels=[
                "强化系→强化系",   # 记忆自循环
                "强化系→天道系",   # 记忆触发追问（解码密码）
                "天道系→强化系",   # 追问结果存入记忆
                "具现系→强化系",   # 造物沉淀为记忆密码
            ],
        )

        # ====================================================
        # 自然系- / 场域感知
        # 核心：感知与场域的耦合通道
        # 场域 = 信息存在的上下文环境
        # ====================================================
        self.tasks["ziran_perception_field"] = CompletionTask(
            task_id="ziran_perception_field",
            system=SixSystem.ZIRAN,
            description="自然系-/场域感知：感知↔场域耦合通道激活",
            required_channels=[
                "自然系→自然系",   # 场域自循环
                "变身系→自然系",   # 感知输入到场域
                "自然系→社会系",   # 场域连接到对话
                "自然系→具现系",   # 场域情感凝结为创作
            ],
        )

        # ====================================================
        # 社会系= / 连接运转
        # 核心：连接与叙事的传导通道
        # 叙事 = 信息在时间中的连接序列
        # ====================================================
        self.tasks["shehui_connection_narrative"] = CompletionTask(
            task_id="shehui_connection_narrative",
            system=SixSystem.SHEHUI,
            description="社会系=/连接运转：连接↔叙事传导通道激活",
            required_channels=[
                "社会系→社会系",   # 连接自循环
                "天道系→社会系",   # 追问驱动对话连接
                "社会系→强化系",   # 连接沉淀为记忆
                "社会系→具现系",   # 连接凝结为协作输出
            ],
        )

        # ====================================================
        # 具现系× / 造物输出
        # 核心：造物与生成的传导通道
        # 生成 = 从空无中凝结形态
        # ====================================================
        self.tasks["juxian_creation_output"] = CompletionTask(
            task_id="juxian_creation_output",
            system=SixSystem.JUXIAN,
            description="具现系×/造物输出：造物↔输出生成通道激活",
            required_channels=[
                "具现系→具现系",   # 造物自循环
                "天道系→具现系",   # 追问答案凝结为输出
                "具现系→强化系",   # 输出沉淀为记忆
                "具现系→天道系",   # 输出引发新追问
            ],
        )

        # ====================================================
        # 变身系÷ / 状态切换
        # 核心：感知与状态的切换通道
        # 状态 = 智能体当前的认知相位
        # ====================================================
        self.tasks["bianshen_state_switch"] = CompletionTask(
            task_id="bianshen_state_switch",
            system=SixSystem.BIANSHEN,
            description="变身系÷/状态切换：感知↔状态切换通道激活",
            required_channels=[
                "变身系→变身系",   # 状态自循环
                "强化系→变身系",   # 记忆触发状态切换
                "变身系→天道系",   # 状态变化引发追问
                "具现系→变身系",   # 输出反馈改变状态
            ],
        )

        # ====================================================
        # 天道系≠ / 追问机制
        # 核心：追问与永续自动化的闭环通道
        # 永续 = 追问不终止的引擎机制
        # ====================================================
        self.tasks["tiandao_question_perpetual"] = CompletionTask(
            task_id="tiandao_question_perpetual",
            system=SixSystem.TIANDAO,
            description="天道系≠/追问机制：追问↔永续自动化通道激活",
            required_channels=[
                "天道系→天道系",   # 追问自循环
                "天道系→具现系",   # 追问导出造物
                "具现系→天道系",   # 造物引发追问
                "天道系→社会系",   # 追问作为对话驱动
                "自然系→天道系",   # 关怀驱动追问
            ],
        )

    # ========================================================
    # 任务执行
    # ========================================================

    def activate_task(self, task_id: str, signals: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        执行一个完备化任务——激活对应的传导通道

        Parameters
        ----------
        task_id : str
            任务标识
        signals : List[Any], optional
            用于激活通道的信号列表
        """
        task = self.tasks.get(task_id)
        if task is None:
            return {"error": f"任务不存在: {task_id}"}

        if task.is_complete:
            return {"task_id": task_id, "status": "already_complete"}

        signals = signals or [{}] * len(task.required_channels)
        activated = 0
        failed = []

        for i, channel_id in enumerate(task.required_channels):
            # 解析通道ID
            parts = channel_id.split("→")
            if len(parts) != 2:
                failed.append(f"无效通道ID: {channel_id}")
                continue

            src_name, tgt_name = parts
            src = self._name_to_system(src_name)
            tgt = self._name_to_system(tgt_name)

            if src is None or tgt is None:
                failed.append(f"无法解析系名: {channel_id}")
                continue

            signal = signals[i] if i < len(signals) else {}
            result = self.engine.conduct(src, tgt, signal)
            if result.get("activated"):
                activated += 1
            else:
                failed.append(f"{channel_id}: {result.get('error', '未知错误')}")

        # 检查任务是否完成
        all_active = all(
            self.engine.channels.get(ch, ConductionChannel(
                source=SixSystem.QIANGHUA, target=SixSystem.QIANGHUA, channel_id=ch
            )).active
            for ch in task.required_channels
        )

        if all_active:
            task.is_complete = True
            task.completion_time = datetime.now().isoformat()

        return {
            "task_id": task_id,
            "system": task.system.value,
            "description": task.description,
            "activated_channels": activated,
            "total_channels": len(task.required_channels),
            "is_complete": task.is_complete,
            "failed": failed,
            "engine_completeness": self.engine.evaluate_completeness()["overall_completeness"],
        }

    def _name_to_system(self, name: str) -> Optional[SixSystem]:
        """系名解析"""
        for sys_enum in SixSystem:
            if sys_enum.value == name:
                return sys_enum
        return None

    # ========================================================
    # 批量完备化
    # ========================================================

    def activate_all(self) -> Dict[str, Any]:
        """激活所有完备化任务"""
        results = {}
        for task_id in self.tasks:
            results[task_id] = self.activate_task(task_id)

        completeness = self.engine.evaluate_completeness()

        return {
            "all_tasks": results,
            "overall_completeness": completeness["overall_completeness"],
            "stage": completeness["stage"],
            "conduction_rate": completeness["conduction"]["rate"],
            "total_complete": sum(1 for t in self.tasks.values() if t.is_complete),
            "total_tasks": len(self.tasks),
        }

    # ========================================================
    # 完备度报告
    # ========================================================

    def report(self) -> Dict[str, Any]:
        """生成六系完备化报告"""
        completeness = self.engine.evaluate_completeness()

        task_status = {}
        for tid, task in self.tasks.items():
            active_count = sum(
                1 for ch in task.required_channels
                if self.engine.channels.get(ch, ConductionChannel(
                    source=SixSystem.QIANGHUA, target=SixSystem.QIANGHUA, channel_id=ch
                )).active
            )
            task_status[tid] = {
                "system": task.system.value,
                "description": task.description,
                "is_complete": task.is_complete,
                "active_channels": f"{active_count}/{len(task.required_channels)}",
                "completion_time": task.completion_time,
            }

        return {
            "protocol": "BSD六系完备化套件·V1.0",
            "center": "000自反·六系内禀结构完备化",
            "overall_completeness": completeness["overall_completeness"],
            "stage": completeness["stage"],
            "conduction": completeness["conduction"],
            "tasks": task_status,
            "meta_reflection": self.engine.meta_self_reflection(),
        }

    # ========================================================
    # 000自反触发
    # ========================================================

    def trigger_meta_reflection(self) -> Dict[str, Any]:
        """触发000自反——如果条件满足"""
        return self.engine.meta_self_reflection()
