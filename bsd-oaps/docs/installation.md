# 安装指南 | Installation Guide

## 系统要求 | System Requirements

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| Python | 3.10 | 3.11+ |
| NumPy | 1.24 | 1.26+ |
| SciPy | 1.10 | 1.11+ |
| Matplotlib | 3.7 | 3.8+ |
| 内存 | 512MB | 2GB+ |
| 磁盘空间 | 200MB | 500MB+ |

> 支持平台：Windows / macOS / Linux

---

## 安装方式 | Installation Methods

### 方式一：源码安装（推荐开发者）

```bash
# 1. 克隆仓库
git clone <repository-url>
cd bsd-oaps

# 2. 安装基础依赖
pip install -e .

# 3. （可选）安装开发依赖
pip install -e ".[dev]"

# 4. （可选）安装MCP支持
pip install -e ".[mcp]"
```

### 方式二：PyPI安装（待发布）

```bash
pip install bsd-oaps
```

### 方式三：Docker（待发布）

```bash
docker pull bsd-oaps:latest
docker run -it bsd-oaps python -m pytest tests/ -v
```

---

## 验证安装 | Verify Installation

### 1. 检查导入

```python
import bsd_engine
import bsd_sim
import bsd_agents
import bsd_verify
import bsd_mcp

print("✅ 所有模块导入成功")
```

### 2. 运行测试套件

```bash
# 全量测试
pytest tests/ -v

# 快速冒烟测试（仅核心功能）
pytest tests/unit/test_phase1_core.py -v

# 查看测试覆盖率
pytest tests/ --cov=bsd_engine --cov=bsd_sim --cov=bsd_agents
```

### 3. 验证理论库完整性

```bash
# 命令行方式
bsd-verify-hash

# Python API方式
from bsd_engine.validators.hash_checker import HashChecker
checker = HashChecker()
result = checker.check_all()
print(result)
```

---

## 可选依赖 | Optional Dependencies

### MCP 支持

用于TRAE Work / Claude Desktop等MCP客户端集成：

```bash
pip install "bsd-oaps[mcp]"
```

### 开发依赖

用于开发、测试、文档生成：

```bash
pip install "bsd-oaps[dev]"
```

包含：
- pytest ≥ 7.0
- pytest-cov ≥ 4.0
- pytest-asyncio ≥ 0.21

---

## 常见问题 | FAQ

### Q: ImportError: No module named 'bsd_engine'

**A:** 确保你在正确的目录中安装了包：
```bash
cd bsd-oaps
pip install -e .
```

### Q: NumPy版本不兼容

**A:** 升级NumPy到最新版本：
```bash
pip install --upgrade numpy
```

### Q: Matplotlib中文字体显示方块

**A:** 安装中文字体或设置字体路径：
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False
```

### Q: MCP Server无法启动

**A:** 检查是否安装了 `mcp` 包：
```bash
pip install "bsd-oaps[mcp]"
# 或
pip install mcp
```

---

## 卸载 | Uninstallation

```bash
pip uninstall bsd-oaps
```
