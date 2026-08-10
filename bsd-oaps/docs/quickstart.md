# 快速开始 | Quick Start

本指南将帮助你在 5 分钟内上手 BSD-OAPS。

---

## 🚀 第一步：安装

```bash
# 克隆并安装
git clone <repository-url>
cd bsd-oaps
pip install -e .
```

验证安装：
```bash
python -c "import bsd_engine; print('✅ BSD-OAPS 安装成功')"
```

---

## 🧮 第二步：体验核心方程

### 求解驻波方程

```python
from bsd_engine.equations.standing_wave import standing_wave_solver

# 求解驻波动力学
result = standing_wave_solver(omega=1.0, kappa=0.35, t_max=10.0)
print(f"驻波振幅: {result['amplitude']:.4f}")
print(f"相干度: {result['coherence']:.4f}")
```

### 计算宇宙学常数 Λ

```python
from bsd_engine.equations.cosmological_constant import lambda_theoretical

Lambda, rho_vac, units = lambda_theoretical()
print(f"理论Λ值: {Lambda:.4e} m^-2")
print(f"真空能量密度: {rho_vac:.4e} J/m³")
```

### 熵流计算

```python
from bsd_engine.equations.entropy_flow import entropy_flow_equation

result = entropy_flow_equation(steps=200)
print(f"总熵增量: {result['total_entropy']:.4f}")
print(f"熵流速率: {result['entropy_rate']:.4f}")
```

---

## 🔬 第三步：运行仿真

### 驻波仿真

```python
from bsd_sim.standing_wave_sim import StandingWaveSimulator

sim = StandingWaveSimulator()
sim.run(steps=1000)
results = sim.get_results()

print(f"仿真步数: {results['steps']}")
print(f"最终振幅: {results['final_amplitude']:.4f}")
print(f"稳态达成: {results['steady_state_reached']}")
```

### 相变仿真

```python
from bsd_sim.phase_transition_sim import PhaseTransitionSimulator

sim = PhaseTransitionSimulator()
sim.run(steps=500)
results = sim.get_results()

print(f"相变点: {results['phase_transition_point']}")
print(f"序参量: {results['order_parameter'][-1]:.4f}")
```

---

## 🏛️ 第四步：验证千禧年难题

### 验证单个难题

```python
from bsd_verify.millennium.verifier_p_vs_np import PvsNPVerifier

verifier = PvsNPVerifier()
result = verifier.verify()

print(f"难题: {result.problem_name}")
print(f"结论: {result.verdict}")
print(f"置信度: {result.confidence:.4f}")
print(f"证明链步数: {len(result.proof_chain)}")
print(f"耗时: {result.verification_time:.4f}s")
```

### 批量验证所有难题

```python
from bsd_agents.millennium_agent import MillenniumVerificationAgent

agent = MillenniumVerificationAgent()
results = agent.verify_all()

for name, result in results.items():
    print(f"【{name}】 {result['verdict']} "
          f"(置信度: {result['confidence']:.2%})")
```

---

## 🤖 第五步：使用智能体

### 元本体Agent

```python
from bsd_agents.meta_ontology_agent import MetaOntologyAgent

agent = MetaOntologyAgent()
result = agent.run_task("查询第1条公理")
print(result)
```

### 交叉验证Agent

```python
from bsd_agents.cross_validation_agent import CrossValidationAgent

agent = CrossValidationAgent()
result = agent.validate_theory("t01_meta_origin_foundation")
print(f"理论名称: {result['theory_name']}")
print(f"验证状态: {result['status']}")
print(f"得分: {result['score']}")
```

---

## 🔧 第六步：MCP工具调用

### Standalone 模式

```bash
# 列出所有工具
python -m bsd_mcp.server list

# 调用单个工具
python -m bsd_mcp.server call bsd_verify_millennium '{"problem": "p_vs_np", "detail_level": "summary"}'

# 调用方程求解
python -m bsd_mcp.server call bsd_solve_equation '{"equation_name": "standing_wave", "params": {"omega": 1.0}}'
```

### Python API 调用

```python
from bsd_mcp.tool_registry import get_global_registry

reg = get_global_registry()

# 查询公理
result = reg.call_tool("bsd_query_axiom", {"axiom_id": 1})
print(result)

# 计算熵流
result = reg.call_tool("bsd_compute_entropy", {"steps": 100})
print(result)
```

---

## ✅ 第七步：运行完整测试

```bash
# 全量测试
pytest tests/ -v

# 查看测试覆盖率
pytest tests/ --cov=bsd_engine --cov=bsd_sim --cov=bsd_agents --cov=bsd_verify --cov=bsd_mcp

# 只跑失败的测试
pytest tests/ --lf
```

---

## 📚 下一步 | Next Steps

- 阅读 [架构文档](architecture.md) 了解五层架构设计
- 查看 [API 参考](api_reference.md) 了解完整API
- 探索 [theory_base/](../theory_base/) 理论库
- 阅读 [贡献指南](../CONTRIBUTING.md) 参与开发

---

## 💡 小技巧 | Tips

1. **快速验证**：使用 `bsd-verify-hash` 命令快速校验理论库完整性
2. **参数锁档**：核心常量已锁档，任何修改都会被哈希校验检测到
3. **仿真加速**：减少 `steps` 参数可加快仿真速度（默认1000步）
4. **调试模式**：设置 `BSD_LOG_LEVEL=DEBUG` 查看详细日志
