# 制造业智能补货决策系统配置指南

## 📋 概述

制造业智能补货决策系统提供了完整的配置系统，所有配置通过 `.env` 文件管理。本指南详细介绍了所有可用的配置选项和最佳实践。

## 🎯 配置特色

### 统一配置管理
- ✅ **单一配置源**: 只使用 `.env` 文件
- ✅ **智能降级**: 自动检测并降级到可用的数据源
- ✅ **Web界面管理**: 通过Web界面管理配置
- ✅ **环境隔离**: 支持开发、测试、生产环境

## 🔧 配置文件结构

### .env 配置文件 (推荐)
```bash
# ===========================================
# 制造业智能补货决策系统配置文件
# ===========================================

# 🤖 LLM 服务配置 (至少配置一个)
# ===========================================

# 🇨🇳 阿里百炼 (推荐，国内访问速度快)
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DASHSCOPE_MODEL=qwen-max
DASHSCOPE_ENABLED=true

# Google AI (免费额度大)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-1.5-pro
GOOGLE_ENABLED=true

# OpenAI (可选)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_ENABLED=false

# ===========================================
# 📊 数据源配置
# ===========================================

# TuShare Pro (经济数据，推荐)
TUSHARE_TOKEN=your_tushare_token_here
TUSHARE_ENABLED=true

# 聚合数据 (新闻和天气数据)
JUHE_API_KEY=your_juhe_api_key_here
JUHE_ENABLED=true

# Google News (补充新闻数据)
GOOGLE_NEWS_API_KEY=your_google_news_api_key_here
GOOGLE_NEWS_ENABLED=false

# Coze插件 (可选扩展数据源)
COZE_API_KEY=your_coze_api_key_here
COZE_ENABLED=false

# Dify知识库 (可选RAG功能)
DIFY_API_KEY=your_dify_api_key_here
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_ENABLED=false

# ===========================================
# 🗄️ 数据库配置 (可选)
# ===========================================

# MongoDB (数据持久化)
MONGODB_ENABLED=false
MONGODB_URI=mongodb://localhost:27017/manufacturing_ai
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB_NAME=manufacturing_ai

# Redis (缓存加速)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# ===========================================
# 🔧 系统配置
# ===========================================

# 系统环境
ENVIRONMENT=development
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/manufacturing_ai.log

# Web界面配置
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost
WEB_TITLE=制造业智能补货决策系统

# 文件路径配置
MANUFACTURING_RESULTS_DIR=./results
MANUFACTURING_DATA_DIR=./data
MANUFACTURING_CACHE_DIR=./cache
MANUFACTURING_LOG_DIR=./logs

# ===========================================
# ⚡ 性能配置
# ===========================================

# 并发控制
MAX_CONCURRENT_AGENTS=3
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=300

# 缓存配置
ENABLE_CACHING=true
CACHE_TTL=3600
ENABLE_LOCAL_CACHE=true
LOCAL_CACHE_SIZE=1000

# 内存管理
ENABLE_MEMORY_CLEANUP=true
MEMORY_CLEANUP_INTERVAL=600
MAX_MEMORY_USAGE_MB=2048

# ===========================================
# 🤖 智能体配置
# ===========================================

# 智能体启用控制
MARKET_ANALYST_ENABLED=true
TREND_ANALYST_ENABLED=true
NEWS_ANALYST_ENABLED=true
CONSUMER_ANALYST_ENABLED=true
OPTIMISTIC_ADVISOR_ENABLED=true
CAUTIOUS_ADVISOR_ENABLED=true
COORDINATOR_ENABLED=true
RISK_MANAGER_ENABLED=true

# 分析深度配置
ANALYSIS_DEPTH=standard
ENABLE_DEBATE=true
MAX_DEBATE_ROUNDS=2
MAX_RISK_DISCUSS_ROUNDS=1

# 决策配置
DECISION_THRESHOLD=0.7
RISK_THRESHOLD=0.5
CONFIDENCE_THRESHOLD=0.6
```

## 📖 配置选项详解

### 1. LLM 服务配置

#### 阿里百炼 (DashScope)
```bash
# 基础配置
DASHSCOPE_API_KEY=sk-your-api-key
DASHSCOPE_MODEL=qwen-max        # 可选: qwen-max, qwen-plus, qwen-turbo
DASHSCOPE_ENABLED=true

# 高级配置
DASHSCOPE_MAX_TOKENS=2000
DASHSCOPE_TEMPERATURE=0.7
DASHSCOPE_TOP_P=0.9
```

**模型选择建议**:
- **qwen-max**: 最高质量，适合复杂分析
- **qwen-plus**: 平衡性能和成本
- **qwen-turbo**: 最快速度，适合简单任务

#### Google AI (Gemini)
```bash
# 基础配置
GOOGLE_API_KEY=your-google-api-key
GOOGLE_MODEL=gemini-1.5-pro     # 可选: gemini-1.5-pro, gemini-1.5-flash
GOOGLE_ENABLED=true

# 高级配置
GOOGLE_MAX_TOKENS=2000
GOOGLE_TEMPERATURE=0.7
GOOGLE_TOP_P=0.9
GOOGLE_TOP_K=40
```

#### OpenAI
```bash
# 基础配置
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4              # 可选: gpt-4, gpt-4-turbo, gpt-3.5-turbo
OPENAI_ENABLED=false

# 高级配置
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
```

### 2. 数据源配置

#### TuShare Pro (经济数据)
```bash
# 基础配置
TUSHARE_TOKEN=your-tushare-token
TUSHARE_ENABLED=true

# 数据类型控制
TUSHARE_PMI_ENABLED=true        # PMI指数
TUSHARE_PPI_ENABLED=true        # PPI指数
TUSHARE_CPI_ENABLED=true        # CPI指数
TUSHARE_GDP_ENABLED=true        # GDP数据

# 缓存配置
TUSHARE_CACHE_TTL=86400         # 24小时缓存
```

#### 聚合数据 (Juhe)
```bash
# 基础配置
JUHE_API_KEY=your-juhe-key
JUHE_ENABLED=true

# 服务控制
JUHE_NEWS_ENABLED=true          # 新闻数据
JUHE_WEATHER_ENABLED=true       # 天气数据
JUHE_HOLIDAY_ENABLED=true       # 节假日数据

# 接口配置
JUHE_NEWS_TYPE=manufacturing    # 新闻类型筛选
JUHE_NEWS_COUNT=20              # 每次获取新闻数量
```

#### Google News
```bash
# 基础配置
GOOGLE_NEWS_API_KEY=your-google-news-key
GOOGLE_NEWS_ENABLED=false

# 搜索配置
GOOGLE_NEWS_LANGUAGE=zh-CN      # 语言设置
GOOGLE_NEWS_COUNTRY=CN          # 国家设置
GOOGLE_NEWS_CATEGORY=business   # 新闻分类
```

### 3. 数据库配置

#### MongoDB 配置
```bash
# 基础配置
MONGODB_ENABLED=false
MONGODB_URI=mongodb://localhost:27017/manufacturing_ai

# 详细配置
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB_NAME=manufacturing_ai
MONGODB_USERNAME=admin
MONGODB_PASSWORD=password

# 连接池配置
MONGODB_MAX_POOL_SIZE=50
MONGODB_MIN_POOL_SIZE=5
MONGODB_CONNECT_TIMEOUT=30000
```

#### Redis 配置
```bash
# 基础配置
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0

# 详细配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 缓存配置
REDIS_DEFAULT_TTL=3600          # 默认过期时间(秒)
REDIS_MAX_CONNECTIONS=20        # 最大连接数
```

### 4. 智能体配置

#### 智能体启用控制
```bash
# 分析师团队 (并行执行)
MARKET_ANALYST_ENABLED=true     # 市场环境分析师
TREND_ANALYST_ENABLED=true      # 趋势预测分析师
NEWS_ANALYST_ENABLED=true       # 新闻资讯分析师
CONSUMER_ANALYST_ENABLED=true   # 消费者洞察分析师

# 决策团队 (辩论执行)
OPTIMISTIC_ADVISOR_ENABLED=true # 乐观建议师
CAUTIOUS_ADVISOR_ENABLED=true   # 谨慎建议师

# 协调层
COORDINATOR_ENABLED=true        # 决策协调员
RISK_MANAGER_ENABLED=true       # 风险管理员
```

#### 分析深度配置
```bash
# 分析级别
ANALYSIS_DEPTH=standard         # basic/standard/comprehensive/detailed

# 辩论配置
ENABLE_DEBATE=true              # 是否启用智能体辩论
MAX_DEBATE_ROUNDS=2             # 辩论轮次 (1-5)
MAX_RISK_DISCUSS_ROUNDS=1       # 风险讨论轮次 (1-3)

# 决策阈值
DECISION_THRESHOLD=0.7          # 决策置信度阈值
RISK_THRESHOLD=0.5              # 风险接受阈值
CONFIDENCE_THRESHOLD=0.6        # 最低置信度要求
```

### 5. 性能配置

#### 并发控制
```bash
# 智能体并发
MAX_CONCURRENT_AGENTS=3         # 同时运行的智能体数量
AGENT_TIMEOUT=300               # 智能体超时时间(秒)

# 请求并发
MAX_CONCURRENT_REQUESTS=10      # 最大并发请求数
REQUEST_TIMEOUT=300             # 请求超时时间(秒)
RETRY_ATTEMPTS=3                # 重试次数
```

#### 缓存配置
```bash
# 全局缓存
ENABLE_CACHING=true             # 启用缓存
CACHE_TTL=3600                  # 缓存过期时间(秒)

# 本地缓存
ENABLE_LOCAL_CACHE=true         # 启用本地缓存
LOCAL_CACHE_SIZE=1000           # 本地缓存条目数
LOCAL_CACHE_TTL=1800            # 本地缓存过期时间(秒)

# 缓存策略
CACHE_STRATEGY=lru              # 缓存策略: lru/fifo/random
```

#### 内存管理
```bash
# 内存限制
MAX_MEMORY_USAGE_MB=2048        # 最大内存使用(MB)
ENABLE_MEMORY_CLEANUP=true      # 启用内存清理

# 清理策略
MEMORY_CLEANUP_INTERVAL=600     # 清理间隔(秒)
MEMORY_CLEANUP_THRESHOLD=80     # 内存使用阈值(%)
```

## 🌟 配置最佳实践

### 开发环境配置
```bash
# 开发环境 (.env.development)
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# 使用经济模型
DASHSCOPE_MODEL=qwen-plus
GOOGLE_MODEL=gemini-1.5-flash

# 减少并发和缓存
MAX_CONCURRENT_AGENTS=2
ANALYSIS_DEPTH=basic
MAX_DEBATE_ROUNDS=1

# 禁用数据库
MONGODB_ENABLED=false
REDIS_ENABLED=false
```

### 测试环境配置
```bash
# 测试环境 (.env.testing)
ENVIRONMENT=testing
DEBUG=false
LOG_LEVEL=INFO

# 使用平衡模型
DASHSCOPE_MODEL=qwen-plus
GOOGLE_MODEL=gemini-1.5-pro

# 标准配置
MAX_CONCURRENT_AGENTS=3
ANALYSIS_DEPTH=standard
MAX_DEBATE_ROUNDS=2

# 启用缓存
MONGODB_ENABLED=true
REDIS_ENABLED=true
```

### 生产环境配置
```bash
# 生产环境 (.env.production)
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# 使用高性能模型
DASHSCOPE_MODEL=qwen-max
GOOGLE_MODEL=gemini-1.5-pro

# 高性能配置
MAX_CONCURRENT_AGENTS=5
ANALYSIS_DEPTH=comprehensive
MAX_DEBATE_ROUNDS=3

# 完整数据库支持
MONGODB_ENABLED=true
REDIS_ENABLED=true
```

## 🔍 配置验证

### 自动验证脚本
```bash
# 运行配置验证
python scripts/validate_config.py

# 测试API连接
python scripts/test_connections.py

# 检查依赖
python scripts/check_dependencies.py
```

### Web界面验证
1. 启动Web界面: `streamlit run web/app.py`
2. 访问配置页面
3. 点击"测试配置"按钮
4. 查看验证结果

## ❗ 常见配置问题

### 1. API密钥问题
```bash
# 问题: API密钥无效
# 解决: 重新获取并检查格式
echo $DASHSCOPE_API_KEY | wc -c  # 检查长度
```

### 2. 网络连接问题
```bash
# 问题: API连接超时
# 解决: 增加超时时间
REQUEST_TIMEOUT=600
AGENT_TIMEOUT=600
```

### 3. 内存不足
```bash
# 问题: 内存溢出
# 解决: 降低并发数和使用轻量模型
MAX_CONCURRENT_AGENTS=2
DASHSCOPE_MODEL=qwen-turbo
ENABLE_MEMORY_CLEANUP=true
```

### 4. 缓存问题
```bash
# 问题: 缓存失效
# 解决: 清理缓存目录
rm -rf ./cache/*
CACHE_TTL=1800  # 减少缓存时间
```

## 🔧 高级配置

### 自定义模型配置
```bash
# 按智能体类型配置不同模型
MARKET_ANALYST_MODEL=qwen-max     # 市场分析使用最强模型
TREND_ANALYST_MODEL=qwen-plus     # 趋势分析使用平衡模型
NEWS_ANALYST_MODEL=qwen-turbo     # 新闻分析使用快速模型
```

### 动态配置更新
```python
# Python代码中动态更新配置
from manufacturingagents.config import get_config, update_config

# 获取当前配置
config = get_config()

# 更新配置
update_config({
    "MAX_CONCURRENT_AGENTS": 5,
    "ANALYSIS_DEPTH": "comprehensive"
})
```

### 环境变量优先级
1. 环境变量 (最高优先级)
2. .env 文件
3. 默认配置 (最低优先级)

## 📞 获取帮助

如果配置过程中遇到问题：
1. 查看 [故障排除指南](../troubleshooting/)
2. 参考 [FAQ文档](../faq/faq.md)
3. 提交 [GitHub Issue](https://github.com/your-org/manufacturing-ai-agents/issues)

配置完成后，建议阅读 [使用指南](../usage/web-interface-guide.md) 开始使用系统。
