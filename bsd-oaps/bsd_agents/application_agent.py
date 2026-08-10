"""
归属基底：第3重六阶科研业务基底 + 第0重元道本源基底（跨层T90 V1.8适配）
对应公理：个体与群体同构嵌套公理 + 公理十一/十二/十三（T90 V1.8 §11.8.11-§11.8.12）
对应九维维度：应用维度 + 元理天道（双时针闭环时序）
理论原文出处：theory_base/L3_功能应用层/ + T90 BSD AI幻觉本体论 V1.8 §11.8.10-§11.8.12
固定数理常量：γ=0.92, κ=0.35, α=0.18, k₊=0.9, k₋=0.1, S₀=0.81, λ=0.62, λ⁻=1.38, π=3.1415926535, Π₂=2.8274333882
理论版本状态码：ACTIVE-V1.8

应用落地 Agent（L3 功能）—— T90 V1.8 同步升级版
—— 将 BSD 理论落地到具体应用场景（医学、物理、文明、经济）
   调用 bsd_sim.life_steady_sim / bsd_sim.civilization_sim / bsd_sim.cosmology_sim 既有仿真器
   集成 C1 双向迭代算子（𝒯₊/𝒯₋/𝒟）双时针动力学
   集成 C2 六层多元进制 / C3 三0.9同构 / C5 粒子家族矩阵

确权信息：
    作者：杨腾飞
    证件：433127199812193215
    哈希：e62f918340dc2975108294736ac8927d90584136972485931027958740925713
    锁档日期：2026-06-20
    三维确权：杨腾飞60%｜墨心25%｜豆包15%
"""
from typing import Any, Dict, List, Optional

from bsd_agents.base import BSDAgentBase, AgentMessage
from bsd_sim.life_steady_sim import LifeSteadySimulator
from bsd_sim.civilization_sim import CivilizationSimulator
from bsd_sim.cosmology_sim import CosmologySimulator
from bsd_engine.registry.constants import (
    GAMMA, KAPPA, ALPHA,
    # T90 V1.8 新增固定参数（2026-07-24锁档）
    K_PLUS, K_MINUS, S_ZERO, LAMBDA, LAMBDA_INV, PI_LOCKED, PI_2,
    AUTHOR, AUTHOR_ID, HASH_SHA256, LOCK_DATE, EQUITY_SPLIT,
    verify_params,
)
from bsd_engine.core.bidirectional_iteration_operator import BidirectionalIterationOperator
from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix


# 仿真器类型注册表
_SIM_TYPES = {"medicine", "physics", "civilization", "life_steady"}


class ApplicationAgent(BSDAgentBase):
    """
    应用落地 Agent（L3 功能）—— T90 V1.8 同步升级版

    职责：
    - apply_to_medicine：调用生命五维稳态仿真器，落地医学诊断
    - apply_to_physics：调用宇宙学仿真器，落地物理系统分析
    - apply_to_civilization：调用文明六系仿真器，落地文明演化预测
    - run_simulation：统一仿真调度入口
    - run_dual_clockwise_iteration：执行 C1 双时针 𝒯₊/𝒯₋ 迭代动力学（T90 V1.8 新增）
    - get_t90_v18_status：获取 T90 V1.8 合规状态（T90 V1.8 新增）

    T90 V1.8 适配内容：
    - 引用 7 个 T90 V1.8 锁档参数（k₊/k₋/S₀/λ/λ⁻/π/Π₂）
    - 集成 C1-C5 四大算子模块
    - 实现双时针 𝒯₊/𝒯₋ 动力学闭环
    - 标注 ACTIVE-V1.8 状态码
    - 包含版权确权信息
    """

    # T90 V1.8 理论版本状态码
    THEORY_VERSION = "ACTIVE-V1.8"

    # 版权确权信息
    COPYRIGHT = {
        "author": AUTHOR,
        "author_id": AUTHOR_ID,
        "hash_sha256": HASH_SHA256,
        "lock_date": LOCK_DATE,
        "equity_split": EQUITY_SPLIT,
    }

    # T90 V1.8 锁档参数快照（供结果注入）
    T90_V18_PARAMS = {
        "K_PLUS": K_PLUS,
        "K_MINUS": K_MINUS,
        "S_ZERO": S_ZERO,
        "LAMBDA": LAMBDA,
        "LAMBDA_INV": LAMBDA_INV,
        "PI_LOCKED": PI_LOCKED,
        "PI_2": PI_2,
    }

    def __init__(self):
        super().__init__(
            name="ApplicationAgent",
            description="应用落地Agent（L3功能）T90 V1.8：医学/物理/文明场景仿真落地 + 双时针动力学",
        )
        # 初始化 T90 V1.8 四大算子模块
        self._init_t90_v18_operators()

    def _init_t90_v18_operators(self):
        """初始化 T90 V1.8 四大核心算子模块"""
        # C1 BSD双向迭代算子（𝒯₊/𝒯₋/𝒟）
        self.bidirectional_operator = BidirectionalIterationOperator()
        # C2 六层多元进制（B₁-B₆）
        self.six_level_emergence = SixLevelBaseEmergence()
        # C3 三个0.9同构定理（0.9̇≅0.9π≅E₃=0.90）
        self.three_nine_isomorphism = ThreeNineIsomorphism()
        # C5 3×3粒子家族矩阵（生点证圆·双时针阴阳对偶）
        self.particle_family_matrix = ParticleFamilyMatrix()

    # ------------------------------------------------------------------
    # T90 V1.8 双时针动力学
    # ------------------------------------------------------------------
    def run_dual_clockwise_iteration(self) -> Dict[str, Any]:
        """
        执行 C1 双时针迭代动力学（T90 V1.8 §11.8.11）

        完整 BSD 迭代：𝒟 = 𝒯₋ ∘ 𝒯₊
        - 顺时针展开 𝒯₊：0∅ → 1 → 3 → 6 → 9 → 12 → N（涌现方向）
        - 逆时针逆反 𝒯₋：N → 12 → 9 → 6 → 3 → 1 → 0_迹 → 1'（湮灭方向）
        - 升维 𝒟：Info(1') > Info(1)，维度增长（定理11.19/11.20）

        返回
        ----
        dict
            含迭代结果、对偶性校验、信息痕迹守恒律校验、T90 V1.8 参数快照
        """
        # 执行完整 BSD 迭代
        iteration_result = self.bidirectional_operator.execute_full_iteration()

        return {
            "scene": "dual_clockwise_iteration",
            "theory_version": self.THEORY_VERSION,
            "operator": "C1 BidirectionalIterationOperator (𝒯₊/𝒯₋/𝒟)",
            "iteration_result": iteration_result,
            "t90_v18_params": self.T90_V18_PARAMS,
            "copyright": self.COPYRIGHT,
        }

    def get_t90_v18_status(self) -> Dict[str, Any]:
        """
        获取 T90 V1.8 合规状态

        返回
        ----
        dict
            含理论版本状态码、锁档参数校验、四大算子自检、版权确权信息
        """
        # 锁档参数校验
        try:
            params_verified = verify_params()
            params_error = None
        except ValueError as exc:
            params_verified = False
            params_error = str(exc)

        # 四大算子自检
        c1_ok, c1_errors = self.bidirectional_operator.validate()
        c2_ok, c2_errors = self.six_level_emergence.validate()
        c3_ok, c3_errors = self.three_nine_isomorphism.validate()
        c5_ok, c5_errors = self.particle_family_matrix.validate()

        return {
            "theory_version": self.THEORY_VERSION,
            "params_verified": params_verified,
            "params_error": params_error,
            "t90_v18_params": self.T90_V18_PARAMS,
            "operators": {
                "C1_bidirectional_iteration": {
                    "module_id": self.bidirectional_operator.module_id,
                    "validated": c1_ok,
                    "errors": c1_errors,
                },
                "C2_six_level_emergence": {
                    "module_id": self.six_level_emergence.module_id,
                    "validated": c2_ok,
                    "errors": c2_errors,
                },
                "C3_three_nine_isomorphism": {
                    "module_id": self.three_nine_isomorphism.module_id,
                    "validated": c3_ok,
                    "errors": c3_errors,
                },
                "C5_particle_family_matrix": {
                    "module_id": self.particle_family_matrix.module_id,
                    "validated": c5_ok,
                    "errors": c5_errors,
                },
            },
            "all_operators_valid": c1_ok and c2_ok and c3_ok and c5_ok,
            "copyright": self.COPYRIGHT,
        }

    # ------------------------------------------------------------------
    # 医学诊断
    # ------------------------------------------------------------------
    def apply_to_medicine(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用到医学诊断：基于生命五维稳态仿真器。

        参数
        ----
        patient_data : dict
            必含五维初始值：qi / blood / body / mind / dao（取值 [0,1]）
            可选：time_steps、dt、perturb={"dimension":..., "magnitude":...}

        返回
        ----
        dict
            含仿真状态、全局相干度、健康等级与扰动韧性信息、T90 V1.8 参数快照
        """
        try:
            qi = float(patient_data.get("qi", 0.7))
            blood = float(patient_data.get("blood", 0.7))
            body = float(patient_data.get("body", 0.7))
            mind = float(patient_data.get("mind", 0.7))
            dao = float(patient_data.get("dao", 0.7))
        except (TypeError, ValueError) as exc:
            return {"error": f"五维参数解析失败: {exc}"}

        time_steps = int(patient_data.get("time_steps", 500))
        dt = float(patient_data.get("dt", 0.01))

        sim = LifeSteadySimulator(time_steps=time_steps, dt=dt)
        sim.setup_subject(qi=qi, blood=blood, body=body, mind=mind, dao=dao)

        # 可选扰动韧性测试
        perturb_cfg = patient_data.get("perturb")
        if isinstance(perturb_cfg, dict) and perturb_cfg:
            try:
                sim.perturb(
                    dimension=perturb_cfg.get("dimension", "qi"),
                    magnitude=float(perturb_cfg.get("magnitude", 0.0)),
                )
            except Exception as exc:  # noqa: BLE001 - 扰动失败不阻断主流程
                return {"error": f"扰动测试失败: {exc}", "stage": "perturb"}

        try:
            sim.run()
            results = sim.get_results()
        except Exception as exc:  # noqa: BLE001 - 容错保护
            return {"error": f"仿真运行失败: {exc}", "stage": "run"}

        return {
            "scene": "medicine",
            "theory_version": self.THEORY_VERSION,
            "patient_initial": {
                "qi": qi, "blood": blood, "body": body, "mind": mind, "dao": dao,
            },
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
            "t90_v18_params": self.T90_V18_PARAMS,
            "health_level": results.get("health_level") if isinstance(results, dict) else None,
            "global_coherence": results.get("gc_final") if isinstance(results, dict) else None,
            "qi_purity": results.get("qi_purity_final") if isinstance(results, dict) else None,
            # S₀ 稳态纯净度阈值评估（T90 V1.8 §11.8.12）
            "s_zero_threshold": S_ZERO,
            "s_zero_assessment": self._assess_s_zero(
                results.get("qi_purity_final") if isinstance(results, dict) else None
            ),
            "raw_results": results,
        }

    def _assess_s_zero(self, qi_purity: Optional[float]) -> Optional[str]:
        """基于 S₀=0.81 稳态纯净度阈值评估（T90 V1.8）"""
        if qi_purity is None:
            return None
        if qi_purity >= S_ZERO:
            return "稳态达标（qi_purity >= S₀=0.81）"
        return "稳态未达标（qi_purity < S₀=0.81）"

    # ------------------------------------------------------------------
    # 物理系统分析
    # ------------------------------------------------------------------
    def apply_to_physics(self, system_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用到物理系统分析：基于宇宙学仿真器。

        参数
        ----
        system_params : dict
            必含：Lambda（宇宙学常数）、Omega_m（物质密度）、Omega_r（辐射密度）
            可选：time_steps

        返回
        ----
        dict
            含尺度因子演化、哈勃参数、Λ 验证结果、T90 V1.8 参数快照
        """
        try:
            Lambda = float(system_params.get("Lambda", 1.1e-52))
            Omega_m = float(system_params.get("Omega_m", 0.3111))
            Omega_r = float(system_params.get("Omega_r", 9.0e-5))
        except (TypeError, ValueError) as exc:
            return {"error": f"宇宙学参数解析失败: {exc}"}

        time_steps = int(system_params.get("time_steps", 200))
        sim = CosmologySimulator(time_steps=time_steps)
        sim.setup_universe(Lambda=Lambda, Omega_m=Omega_m, Omega_r=Omega_r)

        try:
            sim.run()
            results = sim.get_results()
        except Exception as exc:  # noqa: BLE001 - 容错保护
            return {"error": f"物理仿真运行失败: {exc}", "stage": "run"}

        # Λ 守恒验证（若可用）
        lambda_verify: Optional[Dict[str, Any]] = None
        if hasattr(sim, "verify_lambda"):
            try:
                lambda_verify = sim.verify_lambda()
            except Exception as exc:  # noqa: BLE001
                lambda_verify = {"error": str(exc)}

        return {
            "scene": "physics",
            "theory_version": self.THEORY_VERSION,
            "cosmology_params": {
                "Lambda": Lambda, "Omega_m": Omega_m, "Omega_r": Omega_r,
            },
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
            "t90_v18_params": self.T90_V18_PARAMS,
            # Π₂ 拓扑稳态常数对照（T90 V1.8 定理11.23：Π₂=π×k₊/(k₊+k₋)）
            "pi2_topological_constant": PI_2,
            "lambda_verification": lambda_verify,
            "raw_results": results,
        }

    # ------------------------------------------------------------------
    # 文明演化预测
    # ------------------------------------------------------------------
    def apply_to_civilization(self, civ_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用到文明演化预测：基于文明六系仿真器。

        参数
        ----
        civ_params : dict
            必含：six_systems_params（六系初始值，array 或 dict）
            可选：time_steps、dt

        返回
        ----
        dict
            含六系轨迹、熵流曲线、灾变检测结果、T90 V1.8 参数快照
        """
        six_systems_params = civ_params.get("six_systems_params")
        if six_systems_params is None:
            return {"error": "缺少 six_systems_params 参数"}

        time_steps = int(civ_params.get("time_steps", 1000))
        dt = float(civ_params.get("dt", 0.1))

        sim = CivilizationSimulator(time_steps=time_steps, dt=dt)
        try:
            sim.setup_civilization(six_systems_params)
            sim.run()
            results = sim.get_results()
        except Exception as exc:  # noqa: BLE001 - 容错保护
            return {"error": f"文明仿真运行失败: {exc}", "stage": "run"}

        # 灾变检测（若可用）
        catastrophe: Optional[Any] = None
        if hasattr(sim, "check_catastrophe"):
            try:
                catastrophe = sim.check_catastrophe()
            except Exception as exc:  # noqa: BLE001
                catastrophe = {"error": str(exc)}

        # C2 六层多元进制文明跃迁映射（T90 V1.8 推论11.12）
        civ_mapping = self.six_level_emergence.verify_civilization_mapping()

        return {
            "scene": "civilization",
            "theory_version": self.THEORY_VERSION,
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA, "ALPHA": ALPHA},
            "t90_v18_params": self.T90_V18_PARAMS,
            # C2 文明跃迁映射（T90 V1.8 推论11.12：工业文明→信息文明→本体文明）
            "civilization_mapping": civ_mapping,
            "catastrophe": catastrophe,
            "raw_results": results,
        }

    # ------------------------------------------------------------------
    # 统一仿真调度
    # ------------------------------------------------------------------
    def run_simulation(self, sim_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用仿真引擎（统一入口）。

        参数
        ----
        sim_type : str
            仿真类型："medicine" / "physics" / "civilization" / "life_steady"
            （"life_steady" 为 "medicine" 的兼容别名）
        params : dict
            对应场景的参数字典

        返回
        ----
        dict
            对应仿真器的运行结果
        """
        # 兼容别名：life_steady → medicine
        if sim_type == "life_steady":
            sim_type = "medicine"

        if sim_type not in _SIM_TYPES:
            return {
                "error": f"未知仿真类型: {sim_type}",
                "valid_types": sorted(_SIM_TYPES),
            }
        if not isinstance(params, dict):
            return {"error": "params 必须为字典"}

        if sim_type == "medicine":
            return self.apply_to_medicine(params)
        if sim_type == "physics":
            return self.apply_to_physics(params)
        return self.apply_to_civilization(params)

    # ------------------------------------------------------------------
    # 消息处理
    # ------------------------------------------------------------------
    def process(self) -> List[Dict[str, Any]]:
        """
        处理消息队列中的应用请求。

        支持的 content.action：
        - "apply_to_medicine"     content.patient_data
        - "apply_to_physics"      content.system_params
        - "apply_to_civilization" content.civ_params
        - "run_simulation"        content.sim_type / content.params
        - "run_dual_clockwise_iteration"  （T90 V1.8 新增，无参数）
        - "get_t90_v18_status"           （T90 V1.8 新增，无参数）
        """
        results: List[Dict[str, Any]] = []
        while self.message_queue:
            msg: AgentMessage = self.message_queue.pop(0)
            content = msg.content if isinstance(msg.content, dict) else {}
            action = content.get("action", "")
            try:
                if action == "apply_to_medicine":
                    res = self.apply_to_medicine(content.get("patient_data", {}) or {})
                elif action == "apply_to_physics":
                    res = self.apply_to_physics(content.get("system_params", {}) or {})
                elif action == "apply_to_civilization":
                    res = self.apply_to_civilization(content.get("civ_params", {}) or {})
                elif action == "run_simulation":
                    res = self.run_simulation(
                        content.get("sim_type", ""),
                        content.get("params", {}) or {},
                    )
                elif action == "run_dual_clockwise_iteration":
                    res = self.run_dual_clockwise_iteration()
                elif action == "get_t90_v18_status":
                    res = self.get_t90_v18_status()
                else:
                    res = {"error": f"未知 action: {action}"}
            except Exception as exc:  # noqa: BLE001 - 容错保护
                res = {"error": str(exc), "action": action}
            results.append({
                "message_id": msg.message_id,
                "action": action,
                "result": res,
            })
        return results
