"""
归属基底：第相变演化位（第三位）
对应三界秩序：天道/自然/人道（分域秩序层面）
对应公理：第3条（三界维度秩序公理）、第6条（全局宿命边界统摄理论）
对应九维维度：天道原理/天道动力学（天道）、自然相变/自然实体（自然）、社会创造/社会因果（人道）
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：三界秩序配置参数

本模块实现三界维度秩序基底，九维法理向下分化，划分宇宙三大秩序场域。

理论映射：
- 三界划分：对应三界维度秩序公理（公理三）
- 秩序约束：对应全局宿命边界统摄理论（公理六）
"""

from src.foundation.base_1_nine_dim_legal import NineDimensionLegalFoundation

class ThreeRealmsOrderFoundation:
    """
    功能：三界维度秩序基底管理
    理论映射：相变演化位（第三位）·宇宙分域规则
    约束来源：三界维度秩序公理（公理三）

    第2重基底：三界维度秩序基底
    九维法理向下分化，划分宇宙三大秩序场域
    介于纯数理与科研业务之间的宇宙分域规则基底
    """
    FOUNDATION_ID = "THREE_REALMS_ORDER"
    FOUNDATION_LEVEL = 2
    FOUNDATION_NAME = "三界维度秩序基底"

    REALMS = {
        "TAO": {
            "name": "天道秩序基底",
            "scope": "全域宏观",
            "responsibilities": ["时空管控", "维度升降", "全局因果回流", "全局边界管控"],
            "corresponding_agents": ["顶层主控智能体", "分布式集群负载均衡"]
        },
        "NATURE": {
            "name": "自然秩序基底",
            "scope": "物质实体层",
            "responsibilities": ["粒子管控", "图谱管控", "数据管控", "模型管控", "物质相变"],
            "corresponding_agents": ["底层实体智能体", "图模型", "数据预处理", "轻量化分支"]
        },
        "HUMAN": {
            "name": "人道秩序基底",
            "scope": "智慧意识层",
            "responsibilities": ["决策管控", "探索管控", "奖励管控", "进化管控", "意识能级"],
            "corresponding_agents": ["中层决策智能体", "贝叶斯寻优", "因果奖励", "文娱创世分支"]
        }
    }

    COMPETITION_ORDER = {
        "TAO": {
            "budget_limit": False,
            "distributed_parallel": True,
            "budget_interception_simplified": True,
            "priority_by_eself": True,
            "knowledge_sharing": True,
            "preload_prior": True
        },
        "NATURE": {
            "auto_phase_upgrade": True,
            "sparse_debias_always_on": True,
            "enable_lightweight": False,
            "max_hidden_dim": 256,
            "skip_mlp_cold_start": True,
            "phase_threshold_reduction": 0.10,
            "feature_enhancement": True,
            "missing_value_fill": True
        },
        "HUMAN": {
            "bayes_explore_rate": 0.40,
            "reward_weight": 1.25,
            "evolution_cycle": 5,
            "negative_transfer_strict": False,
            "causal_reward_weight": 1.3,
            "adaptive_exploration": True
        }
    }

    RESEARCH_ORDER = {
        "TAO": {
            "budget_limit": True,
            "distributed_parallel": False,
            "budget_interception_simplified": False,
            "priority_by_eself": False,
            "knowledge_sharing": False,
            "preload_prior": False
        },
        "NATURE": {
            "auto_phase_upgrade": False,
            "sparse_debias_always_on": False,
            "enable_lightweight": True,
            "max_hidden_dim": 128,
            "skip_mlp_cold_start": False,
            "phase_threshold_reduction": 0.0,
            "feature_enhancement": False,
            "missing_value_fill": False
        },
        "HUMAN": {
            "bayes_explore_rate": 0.20,
            "reward_weight": 1.0,
            "evolution_cycle": 10,
            "negative_transfer_strict": True,
            "causal_reward_weight": 1.0,
            "adaptive_exploration": False
        }
    }

    DOMAIN_ALLOWANCE = {
        "TAO": {"distributed_parallel": True, "load_balancing": True, "global_boundary": True},
        "NATURE": {"graph_models": True, "data_preprocessing": True, "lightweight": True, "multi_modal": True},
        "HUMAN": {"bayesian_opt": True, "cause_reward": True, "self_evolution": True, "creation_mode": True}
    }

    def __init__(self, nine_dim: NineDimensionLegalFoundation = None, task_mode: str = "research"):
        self.nine_dim = nine_dim or NineDimensionLegalFoundation(task_mode=task_mode)
        self.task_mode = task_mode.lower()
        self.current_order = self.COMPETITION_ORDER if self.task_mode == "competition" else self.RESEARCH_ORDER
        self.current_realm = "NATURE"
        self.creation_mode_enabled = False

    def switch_task_mode(self, mode: str):
        self.task_mode = mode.lower()
        self.current_order = self.COMPETITION_ORDER if self.task_mode == "competition" else self.RESEARCH_ORDER
        if self.nine_dim:
            self.nine_dim.switch_task_mode(mode)

    def get_realm_config(self, realm: str):
        if realm in self.current_order:
            return self.current_order[realm]
        return None

    def validate_operation(self, op_name: str, realm: str = None) -> bool:
        target_realm = realm or self.current_realm
        if target_realm not in self.DOMAIN_ALLOWANCE:
            return False
        return op_name in self.DOMAIN_ALLOWANCE[target_realm]

    def set_realm(self, realm: str):
        if realm in self.REALMS:
            self.current_realm = realm
            return True
        return False

    def enable_creation_mode(self):
        self.creation_mode_enabled = True

    def disable_creation_mode(self):
        self.creation_mode_enabled = False

    def is_operation_allowed(self, op_name: str, realm: str = None) -> tuple:
        allowed = self.validate_operation(op_name, realm)
        if not allowed and self.creation_mode_enabled and op_name == "creation_mode":
            return True, "创世模式临时放开人道秩序约束"
        if allowed:
            return True, f"{op_name} 在{self.REALMS[realm or self.current_realm]['name']}中被允许"
        return False, f"{op_name} 在{self.REALMS[realm or self.current_realm]['name']}中不被允许"

    def get_agent_boundaries(self):
        boundaries = {
            "顶层全局主控智能体": {"realm": "TAO", "powers": ["全局调度", "边界管控", "变身判定"]},
            "中层决策寻优智能体": {"realm": "HUMAN", "powers": ["贝叶斯寻优", "因果奖励", "负迁移校验"]},
            "底层实体执行智能体": {"realm": "NATURE", "powers": ["模型训练", "相变执行", "数据处理"]},
            "辅助支撑配套智能体": {"realm": "ALL", "powers": ["成果归档", "知识管理", "合规审计"]}
        }
        for agent, info in boundaries.items():
            realm_cfg = self.get_realm_config(info["realm"])
            if realm_cfg:
                info["config"] = realm_cfg
        return boundaries

    def get_foundation_constraints(self):
        return {
            "realm_boundary_enforced": True,
            "cross_realm_operation_prohibited": True,
            "creation_mode_restricted": True,
            "multimodal_follows_nature_order": True,
            "ablation_follows_scientific_order": True,
            "task_mode": self.task_mode,
            "current_order": self.current_order
        }

    def feedback_to_legal_foundation(self, sparse_ratio: float = 0.0, delta_illu: float = 0.0, progress: float = 0.0):
        if self.nine_dim:
            self.nine_dim.update_alpha_sparse(sparse_ratio)
            self.nine_dim.update_kappa_by_illusion(delta_illu)
            self.nine_dim.update_flow_matrix_strength(progress)

    def get_effective_phase_threshold(self, base_threshold: float):
        nature_config = self.get_realm_config("NATURE")
        reduction = nature_config.get("phase_threshold_reduction", 0.0) if nature_config else 0.0
        return max(base_threshold - reduction, 0.0)

    def __str__(self):
        return f"{self.FOUNDATION_NAME} (第{self.FOUNDATION_LEVEL}重, 模式:{self.task_mode})"