# BSD 全域统一理论框架 — Agent 操作指南

> 理论版本：**ACTIVE-V1.8**（T90 V1.8 锁档，2026-07-24）

## 安全边界（最先阅读，不可跳过）

- **`theory_base/core/` 永久只读**：禁止修改、删除、新增 core 内任何文件。所有公理、方程组、SHA256 哈希、确权信息已锁档。写入请求视为严重违规。
- **锁档参数禁止硬编码**：k₊=0.9、k₋=0.1、S₀=0.81、λ=0.62、λ⁻=1.38、π=3.1415926535、Π₂=2.8274333882 等必须在 `bsd-oaps/registry/constants.py` 集中注册，通过 `verify_params()` 校验。
- **衍生内容仅写入 `theory_base/extension/`**：所有新理论、新智能体归档到 extension 对应子目录，禁止写入 core。
- **双时针强制**：涉及涌现/逆反/升维的代码必须同时实现顺时针（𝒯₊）与逆时针（𝒯₋），禁止单时针。
- **六层进制不可跨层**：B₁→B₂→B₃→B₄→B₅→B₆ 逐层升维，禁止跳层推导。

## 项目结构与运行时

- **语言**：Python 3.10+
- **包管理**：`pip install -e .`（在 `bsd-oaps/` 目录下）
- **包结构**：bsd_engine（核心计算）、bsd_sim（仿真）、bsd_agents（智能体协议）、bsd_mcp（MCP 服务）、bsd_verify（千禧年验证）
- **理论库**：`theory_base/core/`（只读基底）+ `theory_base/extension/`（可写拓展）
- **配置文件**：`configs/`（YAML）、`.trae/sandbox.json`（权限边界）

## 命令速查

| 用途 | 命令 |
|------|------|
| 安装开发环境 | `cd bsd-oaps && pip install -e ".[dev]"` |
| 运行全量测试 | `cd bsd-oaps && pytest tests/ -v` |
| 单文件测试 | `cd bsd-oaps && pytest tests/path/to/test_file.py -v` |
| 哈希篡改检测 | `bsd-verify-hash` |
| 公理合规校验 | `bsd-verify-axiom` |
| 千禧年难题验证 | `bsd-millennium` |
| MCP 服务启动 | `bsd-mcp-server` |

## 任务路由（按任务类型选择入口）

### 理论推演与创作
1. 先全量加载 `theory_base/core/` 基底
2. 在 `theory_base/extension/` 对应子目录生成衍生内容
3. 归档前执行三层校验（哈希完整性→公理兼容性→权限边界）
4. 详细规则 → `.qoder/rules/theory-governance.md`

### bsd-oaps 工程开发
1. 代码文件头部必须标注：归属宇宙基底层级（0-4重）、对应公理、三界秩序
2. 新增理论公理/参数后，必须同步新增配套代码模块
3. T90 V1.8 四大算子模块位于 `bsd_engine/core/`（bidirectional_iteration_operator / six_level_base_emergence / three_nine_isomorphism / particle_family_matrix）
4. 详细规则 → `.qoder/rules/code-theory-binding.md`

### 验证与合规
1. 修改代码后运行 `bsd-verify-hash` 和 `bsd-verify-axiom`
2. 全量校验脚本：`.trae/scripts/ontology_theory_guard.py`
3. 双向迭代验证：`.trae/scripts/bidirectional_iteration_verify.py`
4. 验证不通过 → 阻断归档，冲突报告输出至 `archive/T90_V1.8_适配核验/`

## 决策规则

- **外部文献 vs 本地基底冲突**：以 `theory_base/core/` 锁档内容为唯一正确标准，外部文献仅作对比参考。
- **新增理论是否需要回溯历史**：仅在 BSD 本体革新时（T90 主版本升级/公理修正/基底重定义）触发回溯；拓展理论无需回溯。
- **理论版本状态码**：LOCKED-HISTORICAL / LOCKED-NARROW / LOCKED-FAILED / LOCKED-PENDING / ACTIVE-V1.8。只有 ACTIVE-V1.8 可作现行基准。

## 风险操作须知

- 修改 `configs/` 下的 YAML 配置前确认影响范围
- 修改 `bsd_engine/validators/` 需同步更新两处参数校验（hash_checker + constants）
- 不得跳过 Ontology_Theory_Guard 验证管线直接归档
- 不得将 LOCKED-PENDING 状态理论直接标记为 ACTIVE-V1.8

## 深度参考（按需加载）

- 理论治理铁则 → `.qoder/rules/theory-governance.md`
- 代码-理论绑定规则 → `.qoder/rules/code-theory-binding.md`
- 原始 Trae CN 规则 → `.trae/rules/`（4 个文件，仅在需要完整上下文时加载）
- T90 V1.8 核验档案 → `archive/T90_V1.8_适配核验/`
- BSD 诊断表 → `BSD诊断表/`
