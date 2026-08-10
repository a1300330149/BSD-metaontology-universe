# -*- coding: utf-8 -*-
# ======================================================
# 归属: 4重·四层执行载体
# 对应公理: 熵减演化
# ======================================================
"""
归属基底：第相变演化位（第三位）·人道秩序配套拓展
对应三界秩序：人道秩序
对应公理：第4条（双边界守恒公理）、第5条（科研动力学公理）、第6条（相变临界公理）、第7条（递归自指公理）
对应九维维度：因果社会/创化社会/精神能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E1=0.35, E2=0.65, E3=0.90

拓展分支：消融自动化（仅外围增量，不改动1重核心流转逻辑）
归属：2重人道秩序基底配套拓展
"""

import numpy as np
from typing import Dict, List, Any, Tuple
import json

class AblationAutomationModule:
    """
    功能：消融实验自动化管理
    理论映射：2重人道秩序基底配套拓展·消融实验规则
    约束来源：科研动力学公理（公理五）、双边界守恒公理（公理四）

    实现消融实验自动化能力，支持系统组件的自动消融和影响评估。

    固定参数（锁档核心）：
    - E1 = 0.35：一阶变身阈值
    - E2 = 0.65：二阶变身阈值
    - E3 = 0.90：三阶变身阈值
    """

    def __init__(self):
        """
        初始化消融自动化模块 - 对应科研动力学公理（公理五）
        """
        self.component_registry = {}  # 组件注册表 - 对应递归自指公理（公理七）
        self.ablation_history = []  # 消融历史 - 对应递归自指公理（公理七）
        self.baseline_performance = {}  # 基线性能 - 对应双边界守恒公理（公理四）
        self.ablation_results = {}  # 消融结果 - 对应科研动力学公理（公理五）

    def register_component(self, component_name: str, component_type: str, importance: float = 1.0):
        """
        注册组件 - 对应递归自指公理（公理七）

        Args:
            component_name (str): 组件名称
            component_type (str): 组件类型
            importance (float): 重要性权重
        """
        # 组件注册 - 对应递归自指公理（公理七）
        self.component_registry[component_name] = {
            'type': component_type,
            'importance': importance,
            'enabled': True,
            'ablation_count': 0
        }

    def set_baseline_performance(self, metric_name: str, baseline_value: float):
        """
        设置基线性能 - 对应双边界守恒公理（公理四）

        Args:
            metric_name (str): 指标名称
            baseline_value (float): 基线值
        """
        # 基线性能设置 - 对应双边界守恒公理（公理四）
        self.baseline_performance[metric_name] = baseline_value

    def ablate_component(self, component_name: str) -> Dict[str, Any]:
        """
        消融组件 - 对应科研动力学公理（公理五）

        Args:
            component_name (str): 组件名称

        Returns:
            Dict[str, Any]: 消融结果
        """
        # 检查组件 - 对应递归自指公理（公理七）
        if component_name not in self.component_registry:
            return {'error': 'Component not found'}

        # 消融操作 - 对应科研动力学公理（公理五）
        component = self.component_registry[component_name]
        component['enabled'] = False
        component['ablation_count'] += 1

        # 记录消融历史 - 对应递归自指公理（公理七）
        ablation_record = {
            'component': component_name,
            'type': component['type'],
            'importance': component['importance'],
            'timestamp': len(self.ablation_history)
        }
        self.ablation_history.append(ablation_record)

        return ablation_record

    def restore_component(self, component_name: str) -> Dict[str, Any]:
        """
        恢复组件 - 对应科研动力学公理（公理五）

        Args:
            component_name (str): 组件名称

        Returns:
            Dict[str, Any]: 恢复结果
        """
        # 检查组件 - 对应递归自指公理（公理七）
        if component_name not in self.component_registry:
            return {'error': 'Component not found'}

        # 恢复操作 - 对应科研动力学公理（公理五）
        component = self.component_registry[component_name]
        component['enabled'] = True

        return {'component': component_name, 'restored': True}

    def evaluate_ablation_impact(self, metric_name: str, ablated_performance: float) -> Dict[str, Any]:
        """
        评估消融影响 - 对应科研动力学公理（公理五）

        Args:
            metric_name (str): 指标名称
            ablated_performance (float): 消融后性能

        Returns:
            Dict[str, Any]: 影响评估结果
        """
        # 获取基线 - 对应双边界守恒公理（公理四）
        baseline = self.baseline_performance.get(metric_name, 0.0)

        # 计算影响 - 对应科研动力学公理（公理五）
        # Impact = (Baseline - Ablated) / Baseline
        if baseline == 0:
            impact = 0.0
        else:
            impact = (baseline - ablated_performance) / baseline

        # 影响评估 - 对应科研动力学公理（公理五）
        impact_level = self._classify_impact(impact)

        result = {
            'metric': metric_name,
            'baseline': baseline,
            'ablated': ablated_performance,
            'impact': impact,
            'impact_level': impact_level
        }

        # 存储结果 - 对应递归自指公理（公理七）
        if metric_name not in self.ablation_results:
            self.ablation_results[metric_name] = []
        self.ablation_results[metric_name].append(result)

        return result

    def _classify_impact(self, impact: float) -> str:
        """
        分类影响等级 - 对应相变临界公理（公理六）

        Args:
            impact (float): 影响值

        Returns:
            str: 影响等级
        """
        # 影响等级分类 - 对应相变临界公理（公理六）
        if abs(impact) < 0.05:
            return 'negligible'  # 可忽略
        elif abs(impact) < 0.15:
            return 'minor'  # 轻微
        elif abs(impact) < 0.30:
            return 'moderate'  # 中等
        else:
            return 'significant'  # 显著

    def run_full_ablation_study(self, evaluation_function) -> Dict[str, Any]:
        """
        运行完整消融研究 - 对应科研动力学公理（公理五）

        Args:
            evaluation_function: 评估函数

        Returns:
            Dict[str, Any]: 完整消融研究结果
        """
        # 完整消融研究 - 对应科研动力学公理（公理五）
        results = {}

        # 遍历所有组件 - 对应递归自指公理（公理七）
        for component_name in self.component_registry:
            # 消融组件 - 对应科研动力学公理（公理五）
            self.ablate_component(component_name)

            # 评估性能 - 对应科研动力学公理（公理五）
            ablated_performance = evaluation_function()

            # 评估影响 - 对应科研动力学公理（公理五）
            for metric_name in self.baseline_performance:
                if metric_name in ablated_performance:
                    impact_result = self.evaluate_ablation_impact(
                        metric_name,
                        ablated_performance[metric_name]
                    )

                    if component_name not in results:
                        results[component_name] = {}
                    results[component_name][metric_name] = impact_result

            # 恢复组件 - 对应科研动力学公理（公理五）
            self.restore_component(component_name)

        return results

    def get_ablation_summary(self) -> Dict[str, Any]:
        """
        获取消融总结 - 对应递归自指公理（公理七）

        Returns:
            Dict[str, Any]: 消融总结
        """
        # 消融总结 - 对应递归自指公理（公理七）
        summary = {
            'total_components': len(self.component_registry),
            'total_ablations': len(self.ablation_history),
            'baseline_performance': self.baseline_performance,
            'component_status': {
                name: comp['enabled']
                for name, comp in self.component_registry.items()
            }
        }

        return summary

    def export_ablation_results(self, filepath: str):
        """
        导出消融结果 - 对应递归自指公理（公理七）

        Args:
            filepath (str): 文件路径
        """
        # 导出结果 - 对应递归自指公理（公理七）
        export_data = {
            'component_registry': self.component_registry,
            'ablation_history': self.ablation_history,
            'baseline_performance': self.baseline_performance,
            'ablation_results': self.ablation_results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)


class AutomatedExperimentRunner:
    """
    功能：自动化实验运行管理
    理论映射：2重人道秩序基底配套拓展·实验运行规则
    约束来源：科研动力学公理（公理五）、递归自指公理（公理七）

    实现自动化实验运行和结果收集。

    固定参数（锁档核心）：
    - E1 = 0.35：一阶变身阈值
    - E2 = 0.65：二阶变身阈值
    - E3 = 0.90：三阶变身阈值
    """

    def __init__(self):
        """
        初始化自动化实验运行器 - 对应科研动力学公理（公理五）
        """
        self.experiment_queue = []  # 实验队列 - 对应科研动力学公理（公理五）
        self.completed_experiments = []  # 完成实验 - 对应递归自指公理（公理七）
        self.current_experiment = None  # 当前实验 - 对应科研动力学公理（公理五）

    def add_experiment(self, experiment_config: Dict[str, Any]):
        """
        添加实验 - 对应科研动力学公理（公理五）

        Args:
            experiment_config (Dict[str, Any]): 实验配置
        """
        # 添加实验 - 对应科研动力学公理（公理五）
        self.experiment_queue.append({
            'config': experiment_config,
            'status': 'pending',
            'timestamp': len(self.experiment_queue)
        })

    def run_next_experiment(self, execution_function) -> Dict[str, Any]:
        """
        运行下一个实验 - 对应科研动力学公理（公理五）

        Args:
            execution_function: 执行函数

        Returns:
            Dict[str, Any]: 实验结果
        """
        # 检查队列 - 对应科研动力学公理（公理五）
        if not self.experiment_queue:
            return {'error': 'No experiments in queue'}

        # 获取下一个实验 - 对应科研动力学公理（公理五）
        self.current_experiment = self.experiment_queue.pop(0)
        self.current_experiment['status'] = 'running'

        # 执行实验 - 对应科研动力学公理（公理五）
        try:
            result = execution_function(self.current_experiment['config'])
            self.current_experiment['result'] = result
            self.current_experiment['status'] = 'completed'
        except Exception as e:
            self.current_experiment['error'] = str(e)
            self.current_experiment['status'] = 'failed'

        # 存储完成实验 - 对应递归自指公理（公理七）
        self.completed_experiments.append(self.current_experiment)

        return self.current_experiment

    def run_all_experiments(self, execution_function) -> List[Dict[str, Any]]:
        """
        运行所有实验 - 对应科研动力学公理（公理五）

        Args:
            execution_function: 执行函数

        Returns:
            List[Dict[str, Any]]: 所有实验结果
        """
        # 运行所有实验 - 对应科研动力学公理（公理五）
        results = []

        while self.experiment_queue:
            result = self.run_next_experiment(execution_function)
            results.append(result)

        return results

    def get_experiment_statistics(self) -> Dict[str, Any]:
        """
        获取实验统计 - 对应递归自指公理（公理七）

        Returns:
            Dict[str, Any]: 实验统计
        """
        # 实验统计 - 对应递归自指公理（公理七）
        total = len(self.completed_experiments)
        completed = sum(1 for exp in self.completed_experiments if exp['status'] == 'completed')
        failed = sum(1 for exp in self.completed_experiments if exp['status'] == 'failed')

        statistics = {
            'total_experiments': total,
            'completed': completed,
            'failed': failed,
            'success_rate': completed / total if total > 0 else 0.0
        }

        return statistics