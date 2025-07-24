# 制造业智能补货决策系统快速开始

## 🎯 概述

本指南将帮助您在15分钟内快速上手制造业智能补货决策系统，从安装到运行第一个补货分析。

## 📋 前置要求

### 系统要求
- **操作系统**: Windows 10+, macOS 10.15+, 或 Linux
- **Python**: 3.10 或更高版本
- **内存**: 至少 4GB RAM (推荐 8GB+)
- **存储**: 至少 2GB 可用空间

### API 密钥准备
在开始之前，您需要获取以下API密钥（至少配置一个LLM服务）：

1. **🇨🇳 阿里百炼 API Key** (推荐首选)
   - 访问 [阿里云百炼平台](https://dashscope.aliyun.com/)
   - 注册账户并获取API密钥
   - ✅ 国产模型，无需科学上网，响应速度快

2. **Google AI API Key** (推荐备选)
   - 访问 [Google AI Studio](https://aistudio.google.com/)
   - 获取免费API密钥，支持Gemini模型
   - ✅ 免费额度大，性能优秀

3. **TuShare Pro Token** (可选，用于真实经济数据)
   - 访问 [TuShare Pro](https://tushare.pro/)
   - 注册并获取Token，可接入PMI、PPI等数据

4. **聚合数据API** (可选，用于新闻天气数据)
   - 访问 [聚合数据](https://www.juhe.cn/)
   - 注册并申请相关API服务

## 🚀 5分钟快速安装

### 1. 克隆项目
```bash
# 克隆项目仓库
git clone https://github.com/your-org/manufacturing-ai-agents.git
cd manufacturing-ai-agents
```

### 2. 创建虚拟环境
```bash
# 使用 venv (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 或使用 conda
conda create -n manufacturing-ai python=3.11
conda activate manufacturing-ai
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件：
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件，最少配置：
# 🇨🇳 阿里百炼 (推荐)
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# 或者 Google AI
GOOGLE_API_KEY=your_google_api_key_here

# 可选: 经济数据
TUSHARE_TOKEN=your_tushare_token_here
```

## 🌐 第一次运行 - Web界面体验

最简单的开始方式是使用Web管理界面：

```bash
# 启动Web界面
streamlit run web/app.py
```

然后在浏览器中访问 `http://localhost:8501`

### Web界面功能
1. 🎛️ **直观的补货分析界面** - 输入产品信息，一键生成决策报告
2. ⚙️ **配置管理** - API密钥和系统参数配置
3. 📊 **实时分析进度** - 可视化智能体工作过程
4. 📄 **决策报告** - 详细的补货建议和风险评估
5. 💾 **历史记录** - 查看和管理历史分析结果

## 🤖 第一次运行 - 命令行体验

如果您偏好命令行界面：

```bash
# 运行基础补货分析
python cli/main.py --product "汽车配件-制动器" --company "某汽车制造公司"

# 查看详细帮助
python cli/main.py --help
```

### 命令行参数说明
```bash
python cli/main.py [options]

选项:
  --product TEXT        产品名称 (必需)
  --company TEXT        公司名称 (可选)
  --analysis-type TEXT  分析类型: basic/detailed/comprehensive
  --output-format TEXT  输出格式: console/json/markdown
  --save-results        是否保存结果到文件
  --debug              启用调试模式
```

## 📊 示例分析场景

### 场景一: 汽车零部件补货决策
```bash
# Web界面输入示例:
产品名称: 汽车制动片
公司名称: 博世汽车部件
当前库存: 5000件
安全库存: 1000件
平均月销量: 2000件
```

### 场景二: 电子元器件补货分析  
```bash
# 命令行示例:
python cli/main.py \
  --product "电子芯片-CPU" \
  --company "英特尔中国" \
  --analysis-type comprehensive \
  --save-results
```

### 场景三: 快消品补货策略
```bash
# Web界面输入示例:
产品名称: 矿泉水
公司名称: 农夫山泉
季节因素: 夏季
特殊事件: 促销活动
```

## 📈 理解分析结果

系统会生成包含以下内容的智能补货报告：

### 1. 市场环境分析
- 宏观经济指标 (PMI、PPI等)
- 行业发展趋势
- 季节性因素影响

### 2. 需求预测分析
- 历史需求趋势
- 未来需求预测
- 影响因素分析

### 3. 新闻情报分析
- 行业重要新闻
- 政策法规变化
- 竞争对手动态

### 4. 消费者洞察
- 市场情绪变化
- 消费者行为分析
- 需求偏好趋势

### 5. 决策建议
- **乐观建议**: 基于积极因素的补货建议
- **谨慎建议**: 基于风险因素的保守建议
- **综合决策**: 平衡各种因素的最终建议

### 6. 风险评估
- 库存风险评估
- 市场风险分析
- 供应链风险预警

## 🔧 常用配置优化

### 提升分析速度
```bash
# 在 .env 文件中添加
MAX_CONCURRENT_AGENTS=3
ENABLE_CACHING=true
CACHE_TTL=3600
```

### 提高分析质量
```bash
# 使用更强的模型
DASHSCOPE_MODEL=qwen-max
GOOGLE_MODEL=gemini-1.5-pro

# 启用详细分析
ANALYSIS_DEPTH=comprehensive
ENABLE_DEBATE=true
```

### 节省API成本
```bash
# 使用更经济的模型
DASHSCOPE_MODEL=qwen-plus
GOOGLE_MODEL=gemini-1.5-flash

# 启用缓存减少重复调用
ENABLE_CACHING=true
USE_LOCAL_CACHE=true
```

## 🛠️ 常见问题快速解决

### Q1: API密钥无效
```bash
# 测试API连接
python tests/test_llm_connection.py

# 重新配置密钥
cp .env.example .env
# 重新编辑 .env 文件
```

### Q2: 分析速度慢
```bash
# 检查网络连接
ping google.com

# 启用本地缓存
echo "ENABLE_LOCAL_CACHE=true" >> .env

# 减少并发数
echo "MAX_CONCURRENT_AGENTS=2" >> .env
```

### Q3: 内存不足
```bash
# 释放内存
echo "ENABLE_MEMORY_CLEANUP=true" >> .env
echo "MEMORY_CLEANUP_INTERVAL=300" >> .env

# 使用轻量级模型
echo "DASHSCOPE_MODEL=qwen-turbo" >> .env
```

### Q4: 端口冲突
```bash
# 使用其他端口
streamlit run web/app.py --server.port 8502
```

## 📚 下一步学习

### 深入了解系统
1. [系统架构文档](../architecture/system-architecture.md) - 了解技术架构
2. [智能体设计](../architecture/agent-architecture.md) - 理解AI决策机制
3. [数据流架构](../architecture/data-flow-architecture.md) - 掌握数据处理流程

### 高级使用技巧
1. [配置指南](../configuration/config-guide.md) - 详细配置选项
2. [使用指南](../usage/web-interface-guide.md) - Web界面高级功能
3. [开发指南](../development/development-workflow.md) - 自定义开发

### 实际应用案例
1. [基础示例](../examples/basic-examples.md) - 简单补货场景
2. [高级示例](../examples/advanced-examples.md) - 复杂业务场景
3. [故障排除](../troubleshooting/streamlit-file-watcher-fix.md) - 常见问题解决

## 🎉 成功运行检查清单

- [ ] 成功启动Web界面 (`http://localhost:8501`)
- [ ] 配置至少一个LLM API密钥
- [ ] 运行第一个补货分析
- [ ] 查看生成的决策报告
- [ ] 理解智能体协作过程
- [ ] 保存分析结果

## 💬 获取支持

如果遇到任何问题：

1. 查看 [FAQ文档](../faq/faq.md)
2. 搜索 [GitHub Issues](https://github.com/your-org/manufacturing-ai-agents/issues)
3. 提交新的Issue描述问题

欢迎加入我们的社区，一起探索制造业AI应用的无限可能！🚀
