"""
归属基底：第3重六阶科研业务基底
对应公理：公理七（系统自进化迭代）
对应九维维度：应用维度
理论原文出处：theory_base/L3_功能应用层/
固定数理常量：γ=0.92, κ=0.35, θ_evo=0.002

BSD Agent 结果聚合模块
—— 聚合多Agent协作执行结果，生成统一汇总报告
"""
import time
import uuid
from typing import Any, Dict, List, Optional


class ResultAggregator:
    """
    结果聚合器

    职责：
    - collect：收集单个Agent执行结果
    - aggregate：聚合指定任务的所有结果
    - get_summary：获取汇总报告
    - merge_results：合并多个结果
    - check_completeness：检查所有Agent是否已完成
    """

    def __init__(self):
        # task_id -> {agent_name -> result_record}
        self._results: Dict[str, Dict[str, Any]] = {}
        # task_id -> expected_agents (list)
        self._expected: Dict[str, List[str]] = {}
        # task_id -> created_at
        self._created_at: Dict[str, float] = {}

    def collect(self, task_id: str, agent_name: str, result: Any) -> Dict[str, Any]:
        """
        收集结果。

        参数
        ----
        task_id : str
            任务ID
        agent_name : str
            来源Agent名
        result : Any
            执行结果

        返回
        ----
        dict
            收集记录
        """
        if not task_id:
            return {"task_id": task_id, "agent_name": agent_name, "collected": False,
                    "error": "task_id 为空"}
        if task_id not in self._results:
            self._results[task_id] = {}
            self._created_at[task_id] = time.time()
        self._results[task_id][agent_name] = {
            "result": result,
            "collected_at": time.time(),
        }
        return {
            "task_id": task_id,
            "agent_name": agent_name,
            "collected": True,
            "total_agents_reported": len(self._results[task_id]),
        }

    def aggregate(self, task_id: str) -> Dict[str, Any]:
        """
        聚合指定任务的所有结果。

        参数
        ----
        task_id : str
            任务ID

        返回
        ----
        dict
            {task_id, agent_count, agents, results, created_at}
        """
        agents_results = self._results.get(task_id, {})
        return {
            "task_id": task_id,
            "agent_count": len(agents_results),
            "agents": list(agents_results.keys()),
            "results": {
                agent: rec["result"]
                for agent, rec in agents_results.items()
            },
            "created_at": self._created_at.get(task_id),
        }

    def get_summary(self, task_id: str) -> Dict[str, Any]:
        """
        获取汇总报告。

        参数
        ----
        task_id : str
            任务ID

        返回
        ----
        dict
            {task_id, agent_count, expected_count, missing_agents,
             complete, agents, results, summary_id}
        """
        agg = self.aggregate(task_id)
        expected = self._expected.get(task_id, [])
        reported = list(self._results.get(task_id, {}).keys())
        missing = [a for a in expected if a not in reported]
        return {
            "task_id": task_id,
            "agent_count": agg["agent_count"],
            "expected_count": len(expected),
            "missing_agents": missing,
            "complete": (len(missing) == 0) if expected else True,
            "agents": agg["agents"],
            "results": agg["results"],
            "summary_id": str(uuid.uuid4()),
        }

    def merge_results(self, results: List[Any]) -> Dict[str, Any]:
        """
        合并多个结果。

        参数
        ----
        results : list
            待合并的结果列表

        返回
        ----
        dict
            {merged, errors, total_inputs, successful_merges}
        """
        merged: Dict[str, Any] = {}
        errors: List[Any] = []
        for idx, r in enumerate(results):
            if isinstance(r, dict):
                if r.get("error"):
                    errors.append(r)
                    continue
                for k, v in r.items():
                    if k in merged:
                        # 冲突键加索引前缀避免覆盖
                        merged[f"{k}__{idx}"] = v
                    else:
                        merged[k] = v
            elif isinstance(r, Exception):
                errors.append({"error": str(r), "index": idx})
            else:
                merged[f"result_{idx}"] = r
        return {
            "merged": merged,
            "errors": errors,
            "total_inputs": len(results),
            "successful_merges": len(merged),
        }

    def check_completeness(self, task_id: str) -> Dict[str, Any]:
        """
        检查所有Agent是否已完成。

        参数
        ----
        task_id : str
            任务ID

        返回
        ----
        dict
            {task_id, expected_agents, reported_agents, missing_agents,
             expected_count, reported_count, missing_count, complete}
        """
        expected = self._expected.get(task_id, [])
        reported = list(self._results.get(task_id, {}).keys())
        missing = [a for a in expected if a not in reported]
        return {
            "task_id": task_id,
            "expected_agents": expected,
            "reported_agents": reported,
            "missing_agents": missing,
            "expected_count": len(expected),
            "reported_count": len(reported),
            "missing_count": len(missing),
            "complete": (len(missing) == 0) if expected else True,
        }

    def set_expected_agents(self, task_id: str, agent_names: List[str]) -> None:
        """
        设置任务的期望Agent列表。

        参数
        ----
        task_id : str
            任务ID
        agent_names : list of str
            期望Agent名列表
        """
        self._expected[task_id] = list(agent_names)
