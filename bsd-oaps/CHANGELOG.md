# 变更日志 | CHANGELOG

所有重要的变更都会记录在这个文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

---

## [0.1.0] - 2026-07-17

### Added - 新增

#### Layer 0: 理论基底迁移层
- T01-T80 共 80 个理论模块迁移完成
- T86 化学基础理论篇（七大诺奖级难题BSD统一验证）
- T87 化学工程应用篇（七大产业级悬赏难题BSD统一验证）
- T88 数理经济制度分析（三元制度范式·驻波动力学·制度质量量化）
- 共 83 个理论模块，覆盖L0-L4全层级
- 255 篇理论文档结构化索引
- SHA256 哈希确权机制
- 理论-代码绑定检查器

#### Layer 1: 核心计算层
- **39 条公理**（7本源+3意义+12基础+9专项+8统一）
- **11 个核心方程求解器**
  - 驻波方程 (standing_wave)
  - 相变方程 (phase_transition)
  - 涌现方程 (emergence)
  - 四力统一方程 (four_force_unification)
  - 熵流方程 (entropy_flow)
  - 宇宙学常数方程 (cosmological_constant)
  - 结构熵方程 (structural_entropy)
  - 生命稳态方程 (life_steady_state)
  - 全局相干方程 (global_coherence)
  - 稳态势方程 (steady_state_potential)
  - κ相位方程 (kappa_phase)
- **26 个核心理论模块**（theory_hub 等）
- 常量注册表与锁档机制（κ, γ, α, E1, E2, E3）
- 三大验证器（哈希/合规/绑定）

#### Layer 2: 仿真引擎层
- **8 大仿真器**
  - 驻波仿真器 (standing_wave_sim)
  - 相变仿真器 (phase_transition_sim)
  - 涌现仿真器 (emergence_sim)
  - 四力统一仿真器 (four_force_sim)
  - 化学系统仿真器 (chemistry_sim)
  - 生命稳态仿真器 (life_steady_sim)
  - 文明演化仿真器 (civilization_sim)
  - 宇宙学仿真器 (cosmology_sim)
- **4 类可视化模块**
  - 波动图 (wave_plots)
  - 相位涌现图 (phase_emergence_plots)
  - 熵文明图 (entropy_civilization_plots)
  - 生命宇宙图 (life_cosmology_plots)

#### Layer 3: 智能体协议层
- **7 大 Agent**
  - 元本体 Agent (meta_ontology_agent)
  - 理论演化 Agent (theory_evolution_agent)
  - 应用 Agent (application_agent)
  - 交叉验证 Agent (cross_validation_agent)
  - 千禧年验证 Agent (millennium_agent)
  - 化学验证 Agent (chemistry_agent)
  - 制度经济学 Agent (institutional_economics_agent)
- **3 类通信协议**
  - 消息格式 (agent_message)
  - 任务调度 (task_dispatch)
  - 结果聚合 (result_aggregation)

#### Layer 4: 千禧年验证层
- **8 大千禧年难题验证器**
  - P vs NP 验证器 (verifier_p_vs_np)
  - Navier-Stokes 验证器 (verifier_navier_stokes)
  - 黎曼猜想验证器 (verifier_riemann)
  - 杨-米尔斯质量间隙验证器 (verifier_yang_mills)
  - 霍奇猜想验证器 (verifier_hodge)
  - BSD 猜想验证器 (verifier_bsd_conjecture)
  - 庞加莱猜想验证器 (verifier_poincare)
  - 比尔猜想验证器 (verifier_beal)
- **14 大化学难题验证器**（7基础理论 + 7工程悬赏）
- **5 大制度经济学验证器**（三元范式/驻波/产业政策/关税/质量评估）
- 完整证明链与数值证据
- 集成测试套件（10 个用例）
- 回归测试套件（14 个用例）

#### Layer 5: TRAE 发布层
- **MCP Server 主入口**（双模式：真实MCP + Standalone CLI）
- **工具注册中心** (tool_registry)
- **28 个 MCP 工具**（6大类）
  - 公理类：bsd_query_axiom, bsd_list_all_axioms, bsd_get_constants, bsd_verify_params, bsd_search_axiom
  - 方程类：bsd_solve_equation, bsd_list_equations, bsd_compute_entropy, bsd_compute_lambda, bsd_compute_coherence
  - 仿真类：bsd_run_simulation, bsd_list_simulations, bsd_sim_results, bsd_sim_snapshot, bsd_sim_visualize
  - 验证类：bsd_verify_millennium, bsd_verify_hash, bsd_verify_compliance, bsd_verify_binding, bsd_full_validation, bsd_verify_chemistry, bsd_verify_institutional
  - 理论类：bsd_query_theory, bsd_list_theories, bsd_search_theory, bsd_get_origin_info, bsd_theory_chain
  - 论文导出类：bsd_export_paper
- TRAE MCP 配置文件 (.trae/mcp.json)

#### 文档
- 项目主 README（中英文双语）
- 安装指南 (docs/installation.md)
- 快速开始 (docs/quickstart.md)
- 架构设计文档 (docs/architecture.md)
- API 参考文档 (docs/api_reference.md)
- 贡献指南 (CONTRIBUTING.md)
- 变更日志 (CHANGELOG.md)

#### 测试
- 168+ 个测试用例全部通过
- 单元测试、集成测试、回归测试全覆盖

---

[0.1.0]: https://github.com/bsd-oaps/bsd-oaps/releases/tag/v0.1.0
