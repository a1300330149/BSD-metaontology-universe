# 文档索引 | Documentation Index

## 入门指南 | Getting Started

- [README](../README.md) - 项目概述、快速开始、目录结构
- [安装指南](installation.md) - 系统要求、安装方式、验证安装
- [快速开始](quickstart.md) - 5 分钟上手 BSD-OAPS

## 架构文档 | Architecture

- [架构设计](architecture.md) - 五层架构详解、设计原则、数据流

## API 参考 | API Reference

- [API 参考](api_reference.md) - 完整的 API 文档

  - **bsd_engine** - 核心计算层
    - 公理系统 (axioms)
    - 方程求解器 (equations)
    - 核心模块 (core)
    - 常量注册表 (registry)
    - 验证器 (validators)

  - **bsd_sim** - 仿真引擎层
    - 8 大仿真器
    - 4 类可视化模块

  - **bsd_agents** - 智能体协议层
    - 7 大 Agent（含化学验证/制度经济学）
    - 3 类通信协议

  - **bsd_verify** - 千禧年验证层
    - 8 千禧年 + 14 化学 + 5 经济验证器
    - 验证结果数据结构

  - **bsd_mcp** - MCP 发布层
    - 28 个 MCP 工具
    - 工具注册中心

## 开发相关 | Development

- [贡献指南](../CONTRIBUTING.md) - 如何贡献代码、代码规范、测试规范
- [变更日志](../CHANGELOG.md) - 版本变更记录

## 理论资源 | Theory Resources

- 「新四位一体3.0元本体本源知识库」（理论基底）
- `theory_base/` 目录 - 255 篇理论文档

---

## 快速跳转 | Quick Links

| 我想... | 去... |
|--------|-------|
| 了解项目是什么 | [README](../README.md) |
| 开始安装 | [安装指南](installation.md) |
| 快速上手 | [快速开始](quickstart.md) |
| 了解架构设计 | [架构设计](architecture.md) |
| 查找 API | [API 参考](api_reference.md) |
| 贡献代码 | [贡献指南](../CONTRIBUTING.md) |
| 查看变更历史 | [变更日志](../CHANGELOG.md) |
| 验证千禧年难题 | [API参考: bsd_verify](api_reference.md#bsd_verify) |
| 使用 MCP 工具 | [API参考: bsd_mcp](api_reference.md#bsd_mcp) |
