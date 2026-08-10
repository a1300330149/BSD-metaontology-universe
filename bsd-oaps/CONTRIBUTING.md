# 贡献指南 | Contributing Guide

感谢您对 BSD-OAPS 的关注！我们欢迎各种形式的贡献。

---

## 📋 行为准则 | Code of Conduct

参与本项目即表示您同意：
- 尊重所有贡献者和用户
- 保持专业和友善的交流
- 接受建设性的批评
- 以社区整体利益为重

---

## 🎯 如何贡献 | How to Contribute

### 1. 报告 Bug

如果您发现了 bug，请通过 Issue 报告，并包含以下信息：

- **复现步骤**：如何复现该问题
- **预期行为**：您期望的正常行为
- **实际行为**：实际发生了什么
- **环境信息**：
  - 操作系统：Windows/macOS/Linux
  - Python 版本：`python --version`
  - BSD-OAPS 版本：`pip show bsd-oaps`
- **最小复现代码**：能复现问题的最简代码

### 2. 提出新特性

欢迎提出新特性建议！请在 Issue 中说明：

- **功能描述**：您希望添加什么功能
- **使用场景**：这个功能解决了什么问题
- **设计思路**：您设想的实现方式（可选）
- **替代方案**：有没有其他实现方式（可选）

### 3. 提交代码

#### 开发流程

1. **Fork 仓库**
   ```bash
   git clone <your-fork-url>
   cd bsd-oaps
   ```

2. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **编写代码**
   - 遵循现有代码风格
   - 添加适当的注释（中文为主）
   - 确保所有BSD标准标注头完整

5. **编写测试**
   - 为新功能添加单元测试
   - 确保测试覆盖率不降低
   - 运行全量测试确保通过
     ```bash
     pytest tests/ -v
     ```

6. **验证合规性**
   ```bash
   # 验证参数未被篡改
   bsd-verify-hash

   # 验证公理合规性
   bsd-verify-axiom
   ```

7. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加xxx功能"
   ```

8. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   然后在 GitHub 上创建 Pull Request。

---

## 📐 代码规范 | Code Standards

### 编码风格

- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 缩进使用 4 个空格
- 行宽不超过 120 字符
- 使用有意义的变量名和函数名

### BSD标准标注头

**所有 Python 文件**顶部必须包含 BSD 标准标注头：

```python
"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理X·xxx公理 / 公理Y·xxx公理
对应九维维度：元理维·逻辑维·验证维·时间流·命运维
理论出处：theory_base/L0_总本源层/...
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

模块名称
—— 模块简要描述
"""
```

### 类型注解

- 公共 API 必须有完整的类型注解
- 推荐对所有函数添加类型注解
- 使用 `from typing import ...` 标准库类型

### 文档字符串

- 所有公共类和函数必须有 docstring
- 使用 Google 风格或 NumPy 风格
- 包含参数、返回值、异常说明

---

## 🧪 测试规范 | Testing Standards

### 测试框架

- 使用 `pytest` 作为测试框架
- 测试文件命名：`test_*.py`
- 测试函数命名：`test_*`

### 测试分类

| 类别 | 目录 | 说明 |
|------|------|------|
| 单元测试 | `tests/unit/` | 单个模块/类/函数的测试 |
| 集成测试 | `tests/integration/` | 多模块协作测试 |
| 回归测试 | `tests/regression/` | 确保历史功能稳定 |

### 编写测试的原则

1. **每个新功能必须有对应测试**
2. **每个 bug 修复必须添加回归测试**
3. **测试应该独立且可重复**
4. **测试用例应该覆盖边界条件**
5. **测试命名应该清晰描述测试内容**

---

## 📝 提交规范 | Commit Convention

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[可选的正文]

[可选的页脚]
```

### Type 类型

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug修复 |
| `docs` | 文档更新 |
| `style` | 代码风格调整（不影响功能） |
| `refactor` | 重构（不新增功能，不修bug） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖相关 |
| `revert` | 回滚提交 |

### 示例

```
feat(equations): 添加新的结构熵方程求解器

- 实现结构熵数值计算
- 添加单元测试
- 更新API文档

Closes #123
```

---

## 📚 理论贡献 | Theory Contributions

BSD-OAPS 的理论基底是「新四位一体3.0元本体本源知识库」。如果您有理论层面的贡献建议：

1. **确保理论一致性**：新理论必须与现有公理体系自洽
2. **提供完整推导**：包含完整的推导过程和数值验证
3. **联系作者**：理论层面的重大变更请先通过邮件联系作者讨论

> **重要**：理论库的核心常量和基础公理已锁档，任何修改都将破坏哈希校验。

---

## 🤝 社区 | Community

- **Issue 追踪**：GitHub Issues
- **讨论区**：GitHub Discussions（待开通）
- **邮件列表**：（待开通）

---

## 📄 许可证 | License

通过贡献代码，您同意您的贡献将根据项目的 **Apache License 2.0** 许可证发布。

---

## 🙏 致谢 | Acknowledgments

感谢所有为 BSD-OAPS 做出贡献的人！

---

如有任何疑问，欢迎通过 Issue 或邮件联系我们。
