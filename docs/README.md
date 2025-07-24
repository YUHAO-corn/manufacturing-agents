# 制造业智能补货决策系统文档中心

欢迎来到制造业智能补货决策系统的文档中心。本系统基于多智能体大语言模型技术，为制造业企业提供智能化、数据驱动的补货决策支持。

## 🎯 项目概览

### 核心定位
基于多智能体大语言模型的制造业智能补货决策系统，通过AI智能体团队协作，为企业提供精准、高效的补货决策支持。

### 技术特色
- **🤖 多智能体协作**: 8个专业智能体模拟企业决策团队
- **🧠 ReAct推理模式**: 基于LangGraph的智能推理和工具调用
- **📊 真实数据驱动**: 集成PMI、PPI、天气、新闻等多源数据
- **🏭 制造业专业化**: 针对制造业场景深度定制的分析框架

## 📚 文档导航

### 🚀 快速开始
- [项目概述](./overview/project-overview.md) - 制造业智能补货系统介绍
- [快速开始](./overview/quick-start.md) - 5分钟启动指南
- [安装指南](./overview/installation.md) - 详细安装部署说明

### 🏗️ 系统架构
- [整体架构](./architecture/system-architecture.md) - 制造业智能体系统架构
- [智能体设计](./architecture/agent-architecture.md) - 8个核心智能体设计理念
- [数据流架构](./architecture/data-flow-architecture.md) - 从数据获取到决策输出的完整流程
- [工作流设计](./architecture/graph-structure.md) - LangGraph协作流程设计
- [ReAct模式](./architecture/react-pattern.md) - 推理-行动-观察循环设计
- [配置优化](./architecture/configuration-optimization.md) - 系统性能优化指南

### 🤖 智能体团队
- [分析师团队](./agents/analysts.md) - 市场环境、趋势预测、新闻、舆情分析师
- [决策顾问](./agents/advisors.md) - 乐观建议师、谨慎建议师
- [决策协调](./agents/coordinator.md) - 决策协调员的整合职责
- [风险管控](./agents/risk-management.md) - 风险评估团队
- [工具集成](./agents/tools-integration.md) - ReAct工具调用机制

### 📊 业务应用
- [应用场景](./business/use-cases.md) - 制造业补货决策典型场景
- [案例分析](./business/case-studies.md) - 电子制造、汽车配件等案例
- [ROI分析](./business/roi-analysis.md) - 投资回报和业务价值量化
- [行业适配](./business/industry-adaptation.md) - 不同制造业子行业适配指南

### 📊 数据与集成
- [数据源集成](./data/data-sources.md) - PMI、PPI、天气、新闻等数据源
- [外部API](./data/external-apis.md) - TuShare Pro、聚合数据等API集成
- [数据处理](./data/data-processing.md) - 数据清洗、验证、缓存机制
- [知识库](./data/knowledge-base.md) - 制造业专业知识RAG集成

### ⚙️ 配置与部署
- [环境配置](./configuration/environment-setup.md) - 开发和生产环境配置
- [LLM配置](./configuration/llm-models.md) - 阿里百炼、Google AI等模型配置
- [数据库配置](./configuration/database-setup.md) - MongoDB、Redis配置
- [Web界面配置](./configuration/web-interface.md) - Streamlit界面自定义
- [生产部署](./deployment/production-deployment.md) - 生产环境部署指南
- [Docker部署](./deployment/docker-setup.md) - 容器化部署方案

### 🔧 开发指南
- [开发环境](./development/dev-setup.md) - 开发环境搭建
- [代码结构](./development/code-structure.md) - 项目代码组织结构
- [智能体开发](./development/agent-development.md) - 自定义智能体开发
- [工具开发](./development/tool-development.md) - 自定义工具开发
- [测试指南](./development/testing.md) - 单元测试和集成测试
- [调试技巧](./development/debugging.md) - 常见问题调试方法

### 📚 API参考
- [核心API](./api/core-api.md) - 主要类和方法API文档
- [智能体API](./api/agents-api.md) - 智能体接口和调用方法
- [数据API](./api/data-api.md) - 数据处理和工具接口
- [Web API](./api/web-api.md) - Web界面后端API

### 🌐 使用指南
- [Web界面使用](./usage/web-interface.md) - 完整的Web界面操作指南
- [补货分析流程](./usage/analysis-workflow.md) - 从输入到决策的完整流程
- [结果解读](./usage/result-interpretation.md) - 如何理解和应用分析结果
- [最佳实践](./usage/best-practices.md) - 系统使用最佳实践

### 💡 示例教程
- [基础示例](./examples/basic-examples.md) - 基本功能使用示例
- [高级示例](./examples/advanced-examples.md) - 复杂场景应用示例
- [自定义示例](./examples/custom-examples.md) - 自定义智能体和工具示例
- [集成示例](./examples/integration-examples.md) - 与其他系统集成示例

### ❓ 故障排除
- [常见问题](./troubleshooting/faq.md) - 常见问题和解决方案
- [错误诊断](./troubleshooting/error-diagnosis.md) - 问题诊断和修复指南
- [性能优化](./troubleshooting/performance-tuning.md) - 系统性能优化
- [日志分析](./troubleshooting/log-analysis.md) - 日志查看和问题定位

### 📋 维护指南
- [系统监控](./maintenance/monitoring.md) - 系统状态监控
- [数据备份](./maintenance/backup.md) - 数据备份和恢复
- [版本升级](./maintenance/version-upgrade.md) - 系统版本升级
- [安全维护](./maintenance/security.md) - 安全策略和维护

## 🎯 核心特性一览

### 智能体角色
| 智能体 | 职责 | 核心能力 |
|--------|------|----------|
| 📊 市场环境分析师 | 宏观指标分析 | PMI、PPI、政策分析 |
| 📈 趋势预测分析师 | 需求趋势预测 | 季节性、事件驱动分析 |
| 📰 新闻资讯分析师 | 行业资讯监控 | 政策变化、行业动态 |
| 💭 舆情洞察分析师 | 消费者情绪 | 社交媒体、搜索趋势 |
| 😊 乐观建议师 | 机会识别 | 积极因素挖掘 |
| 😐 谨慎建议师 | 风险识别 | 风险因素评估 |
| 🎯 决策协调员 | 决策整合 | 综合决策制定 |
| 🛡️ 风险评估团队 | 风险管控 | 全面风险评估 |

### 技术架构
- **🧠 AI框架**: LangChain + LangGraph
- **🌐 Web界面**: Streamlit
- **🗄️ 数据存储**: MongoDB + Redis
- **📊 数据处理**: Pandas + NumPy
- **🧠 大模型**: 阿里百炼 + Google AI

## 📞 获取帮助

### 文档贡献
如果您想为文档做出贡献，请参考 [贡献指南](../CONTRIBUTING.md)。

### 联系方式
- **GitHub Issues**: [提交问题和建议](https://github.com/your-username/manufacturing-ai-agents/issues)
- **项目仓库**: [GitHub Repository](https://github.com/your-username/manufacturing-ai-agents)

---

<div align="center">

**📖 开始探索**：推荐先阅读 [项目概述](./overview/project-overview.md) 了解系统整体情况

**💼 商业价值**：这是一个AI产品经理作品，展示了将成熟AI技术应用于具体业务场景的产品思维

</div>
