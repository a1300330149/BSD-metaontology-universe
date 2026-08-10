# API 参考 | API Reference

## 目录

1. [bsd_engine - 核心计算层](#bsd_engine)
2. [bsd_sim - 仿真引擎层](#bsd_sim)
3. [bsd_agents - 智能体协议层](#bsd_agents)
4. [bsd_verify - 千禧年验证层](#bsd_verify)
5. [bsd_mcp - MCP发布层](#bsd_mcp)

---

## bsd_engine

### bsd_engine.axioms

#### 七大本源公理

```python
from bsd_engine.axioms.seven_origin_axioms import (
    AXIOM_ONE, AXIOM_TWO, AXIOM_THREE, AXIOM_FOUR,
    AXIOM_FIVE, AXIOM_SIX, AXIOM_SEVEN,
)

# 公理对象属性
axiom.name           # str: 公理名称
axiom.description    # str: 公理描述
axiom.formula        # str: 公理公式
axiom.category       # str: 公理类别
```

#### 三大意义公理

```python
from bsd_engine.axioms.three_meaning_axioms import (
    MEANING_AXIOM_ONE, MEANING_AXIOM_TWO, MEANING_AXIOM_THREE,
)
```

#### 十二基础公理

```python
from bsd_engine.axioms.twelve_bsd_axioms import (
    BSD_AXIOM_01, BSD_AXIOM_02, ..., BSD_AXIOM_12,
)
```

#### 九大专项公理

```python
from bsd_engine.axioms.nine_special_axioms import (
    SPECIAL_AXIOM_01, ..., SPECIAL_AXIOM_09,
)
```

#### 八大统一公理

```python
from bsd_engine.axioms.eight_unification_axioms import (
    UNIFICATION_AXIOM_01, ..., UNIFICATION_AXIOM_08,
)
```

---

### bsd_engine.equations

#### 驻波方程

```python
from bsd_engine.equations.standing_wave import standing_wave_solver

result = standing_wave_solver(
    omega=1.0,      # float: 角频率
    kappa=0.35,     # float: 耦合系数
    t_max=10.0,     # float: 最大时间
    n_points=1000,  # int: 采样点数
)

# 返回值
result['amplitude']      # float: 振幅
result['coherence']      # float: 相干度
result['t']              # np.ndarray: 时间数组
result['psi']            # np.ndarray: 波函数
```

#### 相变方程

```python
from bsd_engine.equations.phase_transition import phase_transition_solver

result = phase_transition_solver(
    alpha=0.18,     # float: 相变参数
    kappa=0.35,     # float: 耦合系数
    t_max=10.0,     # float: 最大时间
)
```

#### 涌现方程

```python
from bsd_engine.equations.emergence import emergence_equation

result = emergence_equation(
    n_levels=5,     # int: 涌现层级数
    steps=1000,     # int: 演化步数
)
```

#### 四力统一方程

```python
from bsd_engine.equations.four_force_unification import (
    four_force_unification,
    coupling_constants,
    unification_energy,
)

result = four_force_unification()
```

#### 熵流方程

```python
from bsd_engine.equations.entropy_flow import entropy_flow_equation

result = entropy_flow_equation(
    steps=1000,     # int: 计算步数
    system_type="closed",  # str: 系统类型
)

# 返回值
result['total_entropy']    # float: 总熵增量
result['entropy_rate']     # float: 熵增率
result['time_series']      # np.ndarray: 时序数据
```

#### 宇宙学常数方程

```python
from bsd_engine.equations.cosmological_constant import (
    lambda_theoretical,   # 理论值
    lambda_observed,      # 观测值
    lambda_error,         # 误差
    lambda_from_bsd,      # BSD推导值
)

Lambda, rho_vac, units = lambda_theoretical()
```

#### 结构熵方程

```python
from bsd_engine.equations.structural_entropy import structural_entropy

result = structural_entropy(system_data)
```

#### 生命稳态方程

```python
from bsd_engine.equations.life_steady_state import life_steady_state

result = life_steady_state(steps=1000)
```

#### 全局相干方程

```python
from bsd_engine.equations.global_coherence import global_coherence

result = global_coherence(steps=1000)
```

#### 稳态势方程

```python
from bsd_engine.equations.steady_state_potential import steady_state_potential

result = steady_state_potential()
```

#### κ相位方程

```python
from bsd_engine.equations.kappa_phase import kappa_phase_equation

result = kappa_phase_equation()
```

---

### bsd_engine.registry

#### 常量注册表

```python
from bsd_engine.registry.constants import (
    KAPPA,      # float: 本源耦合常数 κ = 0.35
    GAMMA,      # float: 对偶对称系数 γ = 0.92
    ALPHA,      # float: 相变阈值参数 α = 0.18
    E1,         # float: 第一能量级 ε₁ = 0.35
    E2,         # float: 第二能量级 ε₂ = 0.65
    E3,         # float: 第三能量级 ε₃ = 0.90
    get_all_constants,  # 获取所有常量
    verify_constants,   # 验证常量哈希
)
```

---

### bsd_engine.validators

#### 哈希校验器

```python
from bsd_engine.validators.hash_checker import HashChecker

checker = HashChecker()
result = checker.check_all()          # 全量检查
result = checker.check_core_params()  # 核心参数检查
result = checker.check_theory_base()  # 理论库检查
```

#### 合规检查器

```python
from bsd_engine.validators.compliance_checker import ComplianceChecker

checker = ComplianceChecker()
result = checker.check_axioms()       # 公理合规检查
result = checker.check_equations()    # 方程合规检查
result = checker.check_all()          # 全量检查
```

#### 绑定检查器

```python
from bsd_engine.validators.binding_checker import BindingChecker

checker = BindingChecker()
result = checker.check_coverage()     # 绑定覆盖率检查
result = checker.check_annotations()  # 标注检查
result = checker.check_all()          # 全量检查
```

---

## bsd_sim

### 仿真器基类

```python
from bsd_sim.base import BaseSimulator

class MySimulator(BaseSimulator):
    def _initialize(self): ...       # 初始化状态
    def _step(self): ...             # 单步推进
    def _collect_data(self): ...     # 数据采集
    def get_results(self): ...       # 返回结果
```

### 8大仿真器

#### 驻波仿真器

```python
from bsd_sim.standing_wave_sim import StandingWaveSimulator

sim = StandingWaveSimulator()
sim.run(steps=1000)
results = sim.get_results()
snapshot = sim.get_snapshot(step=500)
```

#### 相变仿真器

```python
from bsd_sim.phase_transition_sim import PhaseTransitionSimulator

sim = PhaseTransitionSimulator()
sim.run(steps=1000)
results = sim.get_results()
```

#### 涌现仿真器

```python
from bsd_sim.emergence_sim import EmergenceSimulator

sim = EmergenceSimulator()
sim.run(steps=1000, n_levels=5)
results = sim.get_results()
```

#### 四力统一仿真器

```python
from bsd_sim.four_force_sim import FourForceSimulator

sim = FourForceSimulator()
sim.run(steps=1000)
results = sim.get_results()
```

#### 化学系统仿真器

```python
from bsd_sim.chemistry_sim import ChemistrySimulator

sim = ChemistrySimulator()
sim.run(steps=1000)
results = sim.get_results()
```

#### 生命稳态仿真器

```python
from bsd_sim.life_steady_sim import LifeSteadySimulator

sim = LifeSteadySimulator()
sim.run(steps=1000)
results = sim.get_results()
```

#### 文明演化仿真器

```python
from bsd_sim.civilization_sim import CivilizationSimulator

sim = CivilizationSimulator()
sim.run(steps=1000)
results = sim.get_results()
```

#### 宇宙学仿真器

```python
from bsd_sim.cosmology_sim import CosmologySimulator

sim = CosmologySimulator()
sim.run(steps=1000)
results = sim.get_results()
```

### 可视化模块

```python
from bsd_sim.visualization.wave_plots import plot_standing_wave
from bsd_sim.visualization.phase_emergence_plots import plot_phase_transition
from bsd_sim.visualization.entropy_civilization_plots import plot_entropy_flow
from bsd_sim.visualization.life_cosmology_plots import plot_lambda_verification

fig = plot_standing_wave(results)
fig.savefig("standing_wave.png")
```

---

## bsd_agents

### Agent基类

```python
from bsd_agents.base import BaseAgent, AgentConfig

class MyAgent(BaseAgent):
    def run_task(self, task: str, **kwargs) -> dict: ...
    def receive_message(self, message: AgentMessage) -> None: ...
    def send_message(self, to: str, content: dict) -> None: ...
```

### 7大Agent

#### 元本体Agent

```python
from bsd_agents.meta_ontology_agent import MetaOntologyAgent

agent = MetaOntologyAgent()
result = agent.run_task("查询第1条公理")
result = agent.run_task("列出所有本源公理")
```

#### 理论演化Agent

```python
from bsd_agents.theory_evolution_agent import TheoryEvolutionAgent

agent = TheoryEvolutionAgent()
result = agent.run_task("演化T01理论")
```

#### 应用Agent

```python
from bsd_agents.application_agent import ApplicationAgent

agent = ApplicationAgent()
result = agent.run_task("求解驻波方程", params={...})
```

#### 交叉验证Agent

```python
from bsd_agents.cross_validation_agent import CrossValidationAgent

agent = CrossValidationAgent()
result = agent.validate_theory("t01_meta_origin_foundation")
result = agent.cross_check("p_vs_np", "navier_stokes")
```

#### 千禧年验证Agent

```python
from bsd_agents.millennium_agent import MillenniumVerificationAgent

agent = MillenniumVerificationAgent()
result = agent.verify("p_vs_np")       # 验证单个
results = agent.verify_all()           # 验证全部
summary = agent.get_summary()          # 获取汇总
```

#### 化学验证Agent

```python
from bsd_agents.chemistry_agent import ChemistryVerificationAgent

agent = ChemistryVerificationAgent()
result = agent.verify_all()            # 验证全部14个化学难题
result = agent.verify_category("basic")    # 验证7个基础理论难题
result = agent.verify_category("engineering")  # 验证7个工程悬赏难题
result = agent.verify_single("quantum_many_body")  # 验证单个
summary = agent.get_summary()          # 获取汇总
```

#### 制度经济学Agent

```python
from bsd_agents.institutional_economics_agent import InstitutionalEconomicsAgent

agent = InstitutionalEconomicsAgent()
result = agent.verify_all()            # 验证全部5个制度经济学项目
result = agent.verify_paradigm()       # 验证三元制度范式
result = agent.analyze_wave()          # 制度驻波动力学分析
summary = agent.get_summary()          # 获取汇总
```

### 通信协议

#### 消息格式

```python
from bsd_agents.protocols.agent_message import AgentMessage

msg = AgentMessage(
    from_id="agent_a",
    to_id="agent_b",
    msg_type="task",
    content={"task": "verify", "params": {...}},
    timestamp=time.time(),
)
```

#### 任务调度

```python
from bsd_agents.protocols.task_dispatch import TaskDispatcher

dispatcher = TaskDispatcher(agents=[...])
result = dispatcher.dispatch("task_name", params={...})
```

#### 结果聚合

```python
from bsd_agents.protocols.result_aggregation import ResultAggregator

aggregator = ResultAggregator()
final = aggregator.aggregate([result1, result2, result3])
```

---

## bsd_verify

### 验证器基类

```python
from bsd_verify.base import MillenniumVerifierBase, VerificationResult

class MyVerifier(MillenniumVerifierBase):
    problem_name = "My Problem"
    bsd_derivation_path = "L0_总本源层/..."

    def _do_verify(self, **kwargs) -> VerificationResult:
        self._add_proof_step(1, "标题", "描述", "公式", evidence={...})
        ...
        return VerificationResult(
            problem_name=self.problem_name,
            verdict="verified",
            confidence=0.95,
            proof_chain=self._proof_chain,
            key_equation="方程",
            numerical_evidence={...},
        )
```

### 8大验证器

```python
from bsd_verify.millennium.verifier_p_vs_np import PvsNPVerifier
from bsd_verify.millennium.verifier_navier_stokes import NavierStokesVerifier
from bsd_verify.millennium.verifier_riemann import RiemannVerifier
from bsd_verify.millennium.verifier_yang_mills import YangMillsVerifier
from bsd_verify.millennium.verifier_hodge import HodgeVerifier
from bsd_verify.millennium.verifier_bsd_conjecture import BSDConjectureVerifier
from bsd_verify.millennium.verifier_poincare import PoincareVerifier
from bsd_verify.millennium.verifier_beal import BealVerifier

# 使用方式
verifier = PvsNPVerifier()
result = verifier.verify()
print(result.verdict)
print(result.confidence)
```

### VerificationResult

```python
result.problem_name           # str: 难题名称
result.verdict                # str: 结论 (verified/refuted/inconclusive/error)
result.confidence             # float: 置信度 (0~1)
result.proof_chain            # list: 证明链
result.key_equation           # str: 关键方程
result.numerical_evidence     # dict: 数值证据
result.verification_time      # float: 耗时(秒)
result.error_message          # str: 错误信息

# 方法
result.to_dict()              # 转为字典
```

---

## bsd_mcp

### 工具注册中心

```python
from bsd_mcp.tool_registry import (
    ToolRegistry,
    get_global_registry,
    register_tool,
)

# 获取全局注册中心
reg = get_global_registry()

# 列出工具
tools = reg.list_tools()

# 获取工具
tool = reg.get_tool("bsd_query_axiom")

# 调用工具
result = reg.call_tool("bsd_verify_millennium", {"problem": "all"})
```

### MCP Server

```python
# 命令行: standalone模式
# python -m bsd_mcp.server list
# python -m bsd_mcp.server call <tool_name> <json_args>

# 或编程方式
from bsd_mcp.server import run_cli
run_cli(["list"])
run_cli(["call", "bsd_query_axiom", '{"axiom_id": 1}'])
```

### 28个MCP工具

#### 公理类（5个）

| 工具名 | 参数 | 返回 |
|--------|------|------|
| `bsd_query_axiom` | `axiom_id: int` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_list_all_axioms` | - | `{"success": bool, "data": [...], "error": str}` |
| `bsd_get_constants` | - | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_verify_params` | - | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_search_axiom` | `keyword: str` | `{"success": bool, "data": [...], "error": str}` |

#### 方程类（5个）

| 工具名 | 参数 | 返回 |
|--------|------|------|
| `bsd_solve_equation` | `equation_name: str, params: dict` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_list_equations` | - | `{"success": bool, "data": [...], "error": str}` |
| `bsd_compute_entropy` | `steps: int` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_compute_lambda` | - | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_compute_coherence` | `steps: int` | `{"success": bool, "data": {...}, "error": str}` |

#### 仿真类（5个）

| 工具名 | 参数 | 返回 |
|--------|------|------|
| `bsd_run_simulation` | `sim_type: str, steps: int, params: dict` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_list_simulations` | - | `{"success": bool, "data": [...], "error": str}` |
| `bsd_sim_results` | `sim_type: str` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_sim_snapshot` | `sim_type: str, step: int` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_sim_visualize` | `sim_type: str, save_path: str` | `{"success": bool, "data": {...}, "error": str}` |

#### 验证类（7个）

| 工具名 | 参数 | 返回 |
|--------|------|------|
| `bsd_verify_millennium` | `problem: str, detail_level: str` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_verify_hash` | `target: str` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_verify_compliance` | `target: str` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_verify_binding` | `target: str` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_full_validation` | `quick_mode: bool` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_verify_chemistry` | `category: str, problem: str` | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_verify_institutional` | `item: str` | `{"success": bool, "data": {...}, "error": str}` |

#### 理论类（5个）

| 工具名 | 参数 | 返回 |
|--------|------|------|
| `bsd_query_theory` | `query: str, layer: str` | `{"success": bool, "data": [...], "error": str}` |
| `bsd_list_theories` | `layer: str` | `{"success": bool, "data": [...], "error": str}` |
| `bsd_search_theory` | `keyword: str` | `{"success": bool, "data": [...], "error": str}` |
| `bsd_get_origin_info` | - | `{"success": bool, "data": {...}, "error": str}` |
| `bsd_theory_chain` | `axiom_id: int` | `{"success": bool, "data": {...}, "error": str}` |

#### 论文导出类（1个）

| 工具名 | 参数 | 返回 |
|--------|------|------|
| `bsd_export_paper` | `paper_type: str, output_path: str` | `{"success": bool, "data": {...}, "error": str}` |

---

## 命令行工具

| 命令 | 功能 |
|------|------|
| `bsd-verify-hash` | 校验理论库哈希完整性 |
| `bsd-verify-axiom` | 验证公理合规性 |
| `bsd-millennium` | 运行千禧年难题验证 |
| `bsd-mcp-server` | 启动MCP Server |
