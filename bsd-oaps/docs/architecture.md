# 架构设计 | Architecture Design

## 概述 | Overview

BSD-OAPS 采用五层架构设计，从理论基底到发布层逐层递进，每一层都建立在下层的基础之上。

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: TRAE发布层 (TRAE Publishing)                  │
│  MCP Server · 28个MCP工具 · Skill配置                    │
├─────────────────────────────────────────────────────────┤
│  Layer 4: 千禧年验证层 (Millennium Verification)        │
│  8千禧年+14化学+5经济 · 证明链 · 集成测试 · 回归测试      │
├─────────────────────────────────────────────────────────┤
│  Layer 3: 智能体协议层 (Agent Protocol)                 │
│  7大Agent · 3类通信协议 · 任务调度 · 结果聚合             │
├─────────────────────────────────────────────────────────┤
│  Layer 2: 仿真引擎层 (Simulation Engine)                │
│  8大仿真器 · 4类可视化 · 驻波/相变/涌现/四力/化学/生命    │
├─────────────────────────────────────────────────────────┤
│  Layer 1: 核心计算层 (Core Computation)                 │
│  39条公理 · 11个方程 · 26个核心模块 · 常量锁档            │
├─────────────────────────────────────────────────────────┤
│  Layer 0: 理论基底迁移 (Theory Foundation)              │
│  T01-T88理论模块 · 255篇文档 · SHA256确权                │
└─────────────────────────────────────────────────────────┘
```

---

## Layer 0: 理论基底迁移层

### 职责
- 将「新四位一体3.0元本体本源知识库」的理论文档转化为可索引的Python模块
- 维护理论库的完整性和不可篡改性
- 提供理论检索、关联、追溯能力

### 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 理论模块集合 | `bsd_engine/theories/t01-t88` | 83个理论模块，覆盖L0-L4全层级（含T86化学基础/T87化学工程/T88制度经济学） |
| 哈希校验器 | `bsd_engine/validators/hash_checker.py` | SHA256完整性校验 |
| 绑定检查器 | `bsd_engine/validators/binding_checker.py` | 理论-代码绑定验证 |
| 合规检查器 | `bsd_engine/validators/compliance_checker.py` | 公理合规性检查 |

### 设计原则
- **不可篡改性**：所有理论文档生成后计算SHA256哈希并锁档
- **完整映射**：理论锚 ↔ 代码锚 一一对应
- **可追溯性**：任何代码变更都可追溯到对应理论依据

---

## Layer 1: 核心计算层

### 职责
- 实现BSD公理体系的可计算表达
- 提供核心方程的数值求解器
- 维护基础理论模块和常量注册表

### 核心模块

#### 公理系统（39条）

| 公理集 | 数量 | 文件 |
|--------|------|------|
| 七大本源公理 | 7 | `axioms/seven_origin_axioms.py` |
| 三大意义公理 | 3 | `axioms/three_meaning_axioms.py` |
| 十二基础公理 | 12 | `axioms/twelve_bsd_axioms.py` |
| 九大专项公理 | 9 | `axioms/nine_special_axioms.py` |
| 八大统一公理 | 8 | `axioms/eight_unification_axioms.py` |

#### 核心方程（11个）

| 方程 | 文件 | 物理意义 |
|------|------|---------|
| 驻波方程 | `equations/standing_wave.py` | 驻波动力学与共振 |
| 相变方程 | `equations/phase_transition.py` | 相变动力学与临界现象 |
| 涌现方程 | `equations/emergence.py` | 层级涌现与自组织 |
| 四力统一方程 | `equations/four_force_unification.py` | 四大基本力统一 |
| 熵流方程 | `equations/entropy_flow.py` | 熵增/减与耗散 |
| 宇宙学常数方程 | `equations/cosmological_constant.py` | Λ与真空能 |
| 结构熵方程 | `equations/structural_entropy.py` | 结构与信息熵 |
| 生命稳态方程 | `equations/life_steady_state.py` | 生命自稳机制 |
| 全局相干方程 | `equations/global_coherence.py` | 全局相干度计算 |
| 稳态势方程 | `equations/steady_state_potential.py` | 稳态势能面 |
| κ相位方程 | `equations/kappa_phase.py` | 本源耦合相位 |

#### 核心模块（26个）

位于 `bsd_engine/core/` 目录，包括：
- 理论集线器（theory_hub）
- 双向相变（bidirectional_phase_transition）
- 对偶映射矩阵（dual_mapping_matrix）
- 九界涌现（nine_realms_emergence）
- 全局熵守恒（global_entropy_conservation）
- ...等26个核心模块

#### 常量注册表

- 文件：`registry/constants.py`
- 功能：锁档核心常量（κ, γ, α, E1, E2, E3等）
- 机制：修改即触发哈希校验失败

---

## Layer 2: 仿真引擎层

### 职责
- 基于核心方程构建各领域的动态仿真器
- 提供时间步进、状态演化、数据采集能力
- 提供可视化接口展示仿真结果

### 8大仿真器

| 仿真器 | 文件 | 领域 | 核心方程 |
|--------|------|------|---------|
| 驻波仿真器 | `bsd_sim/standing_wave_sim.py` | 基础物理 | 驻波方程 |
| 相变仿真器 | `bsd_sim/phase_transition_sim.py` | 相变动力学 | 相变方程 |
| 涌现仿真器 | `bsd_sim/emergence_sim.py` | 复杂系统 | 涌现方程 |
| 四力统一仿真器 | `bsd_sim/four_force_sim.py` | 粒子物理 | 四力统一方程 |
| 化学系统仿真器 | `bsd_sim/chemistry_sim.py` | 化学 | 结构熵方程 |
| 生命稳态仿真器 | `bsd_sim/life_steady_sim.py` | 生物学 | 生命稳态方程 |
| 文明演化仿真器 | `bsd_sim/civilization_sim.py` | 社会学 | 熵流方程 |
| 宇宙学仿真器 | `bsd_sim/cosmology_sim.py` | 宇宙学 | Λ方程 |

### 4类可视化

| 可视化模块 | 文件 | 功能 |
|-----------|------|------|
| 波动图 | `visualization/wave_plots.py` | 驻波/波动可视化 |
| 相位涌现图 | `visualization/phase_emergence_plots.py` | 相变/涌现可视化 |
| 熵文明图 | `visualization/entropy_civilization_plots.py` | 熵流/文明演化可视化 |
| 生命宇宙图 | `visualization/life_cosmology_plots.py` | 生命/宇宙学可视化 |

### 仿真器基类设计

所有仿真器继承自 `BaseSimulator`，统一接口：
- `run(steps)`: 运行仿真
- `step()`: 单步推进
- `get_results()`: 获取结果
- `reset()`: 重置状态
- `get_snapshot(step)`: 获取快照

---

## Layer 3: 智能体协议层

### 职责
- 提供多智能体协作框架
- 定义Agent间通信协议
- 实现任务调度与结果聚合

### 7大Agent

| Agent | 文件 | 职责 |
|-------|------|------|
| 元本体Agent | `agents/meta_ontology_agent.py` | 公理体系维护、理论溯源 |
| 理论演化Agent | `agents/theory_evolution_agent.py` | 理论发展、新定理推导 |
| 应用Agent | `agents/application_agent.py` | 应用场景适配、接口封装 |
| 交叉验证Agent | `agents/cross_validation_agent.py` | 跨领域验证、一致性检查 |
| 千禧年验证Agent | `agents/millennium_agent.py` | 千禧年难题验证协调 |
| 化学验证Agent | `agents/chemistry_agent.py` | 化学全域14大难题验证 |
| 制度经济学Agent | `agents/institutional_economics_agent.py` | T88制度经济学验证 |

### Agent基类设计

```python
class BaseAgent:
    agent_id: str
    name: str
    role: str

    def run_task(self, task: str, **kwargs) -> dict
    def receive_message(self, message: AgentMessage) -> None
    def send_message(self, to: str, content: dict) -> None
```

### 3类通信协议

| 协议模块 | 文件 | 功能 |
|---------|------|------|
| 消息格式 | `protocols/agent_message.py` | Agent消息数据结构定义 |
| 任务调度 | `protocols/task_dispatch.py` | 任务分配与负载均衡 |
| 结果聚合 | `protocols/result_aggregation.py` | 多Agent结果融合 |

### 工作流程

```
任务输入 → 任务调度器 → Agent A → 消息总线 → Agent B
                                       ↓
                                  结果聚合器 → 最终输出
```

---

## Layer 4: 千禧年验证层

### 职责
- 基于BSD理论验证8大千禧年难题
- 提供完整的证明链和数值证据
- 集成测试与回归测试保障

### 8大验证器

| # | 难题 | 验证器 | BSD推导路径 |
|---|------|--------|------------|
| 1 | P vs NP | `verifier_p_vs_np.py` | 熵流方程→不可逆耗散 |
| 2 | Navier-Stokes | `verifier_navier_stokes.py` | 驻波动力学→高频模态不收敛 |
| 3 | 黎曼猜想 | `verifier_riemann.py` | 量子驻波→零点分布对称 |
| 4 | 杨-米尔斯质量间隙 | `verifier_yang_mills.py` | 四力统一→耦合守恒 |
| 5 | 霍奇猜想 | `verifier_hodge.py` | 结构熵→拓扑稳态收敛 |
| 6 | BSD猜想 | `verifier_bsd_conjecture.py` | 正气存内→离散连续对偶 |
| 7 | 庞加莱猜想 | `verifier_poincare.py` | Λ解析式→拓扑稳态收敛 |
| 8 | 比尔猜想 | `verifier_beal.py` | 四力配比→个体基底锚定 |

### 验证器基类

```python
class MillenniumVerifierBase:
    problem_name: str
    bsd_derivation_path: str

    def verify() -> VerificationResult
    def get_proof_chain() -> List[Dict]
    def get_summary() -> Dict
```

### 验证结果结构

```python
@dataclass
class VerificationResult:
    problem_name: str
    verdict: str          # "verified" / "refuted" / "inconclusive" / "error"
    confidence: float     # 0.0 ~ 1.0
    proof_chain: List     # 证明链步骤
    key_equation: str     # 关键方程
    numerical_evidence: dict  # 数值证据
    verification_time: float  # 耗时(秒)
    error_message: str    # 错误信息
```

---

## Layer 5: TRAE发布层

### 职责
- 将BSD-OAPS能力封装为MCP Server
- 提供标准化Tool接口
- 支持TRAE Work / Claude Desktop等MCP客户端

### 28个MCP工具

| 类别 | 数量 | 工具前缀 |
|------|------|---------|
| 公理类 | 5 | `bsd_query_axiom`, `bsd_list_all_axioms`, `bsd_get_constants`, `bsd_verify_params`, `bsd_search_axiom` |
| 方程类 | 5 | `bsd_solve_equation`, `bsd_list_equations`, `bsd_compute_entropy`, `bsd_compute_lambda`, `bsd_compute_coherence` |
| 仿真类 | 5 | `bsd_run_simulation`, `bsd_list_simulations`, `bsd_sim_results`, `bsd_sim_snapshot`, `bsd_sim_visualize` |
| 验证类 | 7 | `bsd_verify_millennium`, `bsd_verify_hash`, `bsd_verify_compliance`, `bsd_verify_binding`, `bsd_full_validation`, `bsd_verify_chemistry`, `bsd_verify_institutional` |
| 理论类 | 5 | `bsd_query_theory`, `bsd_list_theories`, `bsd_search_theory`, `bsd_get_origin_info`, `bsd_theory_chain` |
| 论文导出类 | 1 | `bsd_export_paper` |

### 工具注册中心

- 文件：`bsd_mcp/tool_registry.py`
- 功能：统一管理工具注册、查找、调用
- 设计：插件化架构，新增工具只需调用 `register_tool()`

### 双模式运行

1. **真实MCP模式**：有 `mcp` 包时，启动标准MCP Server
2. **Standalone模式**：无 `mcp` 包时，提供CLI接口

---

## 数据流架构

```
理论文档 (Layer 0)
    ↓ (转化为)
公理/方程/模块 (Layer 1)
    ↓ (驱动)
仿真器 (Layer 2)
    ↓ (调用)
Agents (Layer 3)
    ↓ (验证)
验证器 (Layer 4)
    ↓ (暴露为)
MCP Tools (Layer 5)
    ↓ (供)
TRAE Work / 外部客户端 使用
```

---

## 设计原则

### 1. 理论优先原则
- 所有代码必须有理论依据
- 理论锚 ↔ 代码锚 双向绑定
- 违反公理的代码不允许合入

### 2. 分层解耦原则
- 各层之间通过清晰接口交互
- 上层依赖下层，下层不感知上层
- 可独立替换某一层的实现

### 3. 可验证原则
- 每个核心模块都有对应的验证器
- 哈希校验确保理论完整性
- 全链路测试覆盖各层

### 4. 可扩展原则
- 插件化架构，方便新增方程/仿真器/Agent
- 统一接口规范
- 配置驱动，参数可调

### 5. 性能原则
- 核心计算使用NumPy/SciPy优化
- 仿真器支持增量步进
- 避免不必要的全局计算
