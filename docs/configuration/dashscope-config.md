# 阿里百炼大模型配置指南

## 概述

阿里百炼（DashScope）是阿里云推出的大模型服务平台，提供通义千问系列模型。本指南详细介绍如何在 TradingAgents 中配置和使用阿里百炼大模型。

## 为什么选择阿里百炼？

### 🇨🇳 **国产化优势**
- **无需翻墙**: 国内直接访问，网络稳定
- **中文优化**: 专门针对中文场景优化
- **合规安全**: 符合国内数据安全要求
- **本土化服务**: 中文客服和技术支持

### 💰 **成本优势**
- **价格透明**: 按量计费，价格公开透明
- **免费额度**: 新用户有免费试用额度
- **性价比高**: 相比国外模型成本更低

### 🧠 **技术优势**
- **中文理解**: 在中文理解和生成方面表现优秀
- **金融知识**: 对中国金融市场有更好的理解
- **推理能力**: 通义千问系列在推理任务上表现出色

## 快速开始

### 1. 获取API密钥

#### 步骤1: 注册阿里云账号
1. 访问 [阿里云官网](https://www.aliyun.com/)
2. 点击"免费注册"
3. 完成账号注册和实名认证

#### 步骤2: 开通百炼服务
1. 访问 [百炼控制台](https://dashscope.console.aliyun.com/)
2. 点击"立即开通"
3. 选择合适的套餐（建议先选择按量付费）

#### 步骤3: 获取API密钥
1. 在百炼控制台中，点击"API-KEY管理"
2. 点击"创建新的API-KEY"
3. 复制生成的API密钥

### 2. 配置环境变量

#### 方法1: 使用环境变量
```bash
# Windows
set DASHSCOPE_API_KEY=your_dashscope_api_key_here
set FINNHUB_API_KEY=your_finnhub_api_key_here

# Linux/macOS
export DASHSCOPE_API_KEY=your_dashscope_api_key_here
export FINNHUB_API_KEY=your_finnhub_api_key_here
```

#### 方法2: 使用 .env 文件
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入真实的API密钥
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FINNHUB_API_KEY=your_finnhub_api_key_here
```

### 3. 运行演示

```bash
# 使用专门的阿里百炼演示脚本
python demo_dashscope.py
```

## 支持的模型

### 通义千问系列模型

| 模型名称 | 模型ID | 特点 | 适用场景 |
|---------|--------|------|----------|
| **通义千问 Turbo** | `qwen-turbo` | 快速响应，成本低 | 快速任务、日常对话 |
| **通义千问 Plus** | `qwen-plus-latest` | 平衡性能和成本 | 复杂分析、专业任务 |
| **通义千问 Max** | `qwen-max` | 最强性能 | 最复杂任务、高质量输出 |
| **通义千问 Max 长文本** | `qwen-max-longcontext` | 超长上下文 | 长文档分析、大量数据处理 |

### 推荐配置

#### 经济型配置（成本优先）
```python
config = {
    "llm_provider": "dashscope",
    "deep_think_llm": "qwen-plus-latest",      # 深度思考使用Plus
    "quick_think_llm": "qwen-turbo",    # 快速任务使用Turbo
    "max_debate_rounds": 1,             # 减少辩论轮次
}
```

#### 性能型配置（质量优先）
```python
config = {
    "llm_provider": "dashscope", 
    "deep_think_llm": "qwen-max",       # 深度思考使用Max
    "quick_think_llm": "qwen-plus",     # 快速任务使用Plus
    "max_debate_rounds": 2,             # 增加辩论轮次
}
```

#### 长文本配置（处理大量数据）
```python
config = {
    "llm_provider": "dashscope",
    "deep_think_llm": "qwen-max-longcontext",  # 使用长文本版本
    "quick_think_llm": "qwen-plus",
    "max_debate_rounds": 1,
}
```

## 配置示例

### 基础配置
```python
from manufacturingagents.graph.trading_graph import TradingAgentsGraph
from manufacturingagents.default_config import DEFAULT_CONFIG

# 创建阿里百炼配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "dashscope"
config["deep_think_llm"] = "qwen-plus-latest"
config["quick_think_llm"] = "qwen-turbo"

# 初始化
ta = TradingAgentsGraph(debug=True, config=config)

# 运行分析
state, decision = ta.propagate("AAPL", "2024-05-10")
print(decision)
```

### 高级配置
```python
# 自定义模型参数
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "dashscope",
    "deep_think_llm": "qwen-max",
    "quick_think_llm": "qwen-plus-latest",
    "max_debate_rounds": 2,
    "max_risk_discuss_rounds": 2,
    "online_tools": True,
})

# 使用自定义参数创建LLM
from manufacturingagents.llm_adapters import ChatDashScope

custom_llm = ChatDashScope(
    model="qwen-max",
    temperature=0.1,
    max_tokens=3000,
    top_p=0.9
)
```

## 成本控制

### 典型使用成本
- **经济模式**: ¥0.01-0.05/次分析 (使用 qwen-turbo)
- **标准模式**: ¥0.05-0.15/次分析 (使用 qwen-plus)
- **高精度模式**: ¥0.10-0.30/次分析 (使用 qwen-max)

### 成本优化建议
1. **合理选择模型**: 根据任务复杂度选择合适的模型
2. **控制辩论轮次**: 减少 `max_debate_rounds` 参数
3. **使用缓存**: 启用数据缓存减少重复调用
4. **监控使用量**: 定期检查API调用量和费用

## 故障排除

### 常见问题

#### 1. API密钥错误
```
Error: Invalid API key
```
**解决方案**: 检查API密钥是否正确，确认已开通百炼服务

#### 2. 额度不足
```
Error: Insufficient quota
```
**解决方案**: 在百炼控制台充值或升级套餐

#### 3. 网络连接问题
```
Error: Connection timeout
```
**解决方案**: 检查网络连接，确认可以访问阿里云服务

#### 4. 模型不存在
```
Error: Model not found
```
**解决方案**: 检查模型名称是否正确，确认模型已开通

### 调试技巧

1. **启用调试模式**:
   ```python
   ta = TradingAgentsGraph(debug=True, config=config)
   ```

2. **检查API连接**:
   ```python
   import dashscope
   dashscope.api_key = "your_api_key"
   
   from dashscope import Generation
   response = Generation.call(
       model="qwen-turbo",
       messages=[{"role": "user", "content": "Hello"}]
   )
   print(response)
   ```

## 最佳实践

1. **模型选择**: 根据任务复杂度选择合适的模型
2. **参数调优**: 根据具体需求调整温度、最大token数等参数
3. **错误处理**: 实现适当的错误处理和重试机制
4. **监控使用**: 定期监控API使用量和成本
5. **缓存策略**: 合理使用缓存减少API调用

## 相关链接

- [阿里百炼官网](https://dashscope.aliyun.com/)
- [百炼控制台](https://dashscope.console.aliyun.com/)
- [API文档](https://help.aliyun.com/zh/dashscope/)
- [价格说明](https://help.aliyun.com/zh/dashscope/product-overview/billing-overview)
