# TradingAgents 示例程序

本目录包含了 TradingAgents 框架的各种示例程序，帮助用户快速上手和理解如何使用不同的LLM提供商。

## 目录结构

```
examples/
├── README.md                 # 本文件
├── dashscope/               # 阿里百炼大模型示例
│   ├── demo_dashscope.py           # 完整的阿里百炼演示
│   ├── demo_dashscope_chinese.py   # 中文优化版本
│   ├── demo_dashscope_simple.py    # 简化版本（仅LLM测试）
│   └── demo_dashscope_no_memory.py # 禁用记忆功能版本
└── openai/                  # OpenAI 模型示例
    └── demo_openai.py              # OpenAI 演示程序
```

## 快速开始

### 🇨🇳 使用阿里百炼大模型（推荐）

阿里百炼是国产大模型，具有以下优势：
- 无需翻墙，网络稳定
- 中文理解能力强
- 成本相对较低
- 符合国内合规要求

#### 1. 配置API密钥

```bash
# 设置环境变量
set DASHSCOPE_API_KEY=your_dashscope_api_key
set FINNHUB_API_KEY=your_finnhub_api_key

# 或编辑项目根目录的 .env 文件
```

#### 2. 运行示例

```bash
# 中文优化版本（推荐）
python examples/dashscope/demo_dashscope_chinese.py

# 完整功能版本
python examples/dashscope/demo_dashscope.py

# 简化测试版本
python examples/dashscope/demo_dashscope_simple.py

# 无记忆功能版本（兼容性更好）
python examples/dashscope/demo_dashscope_no_memory.py
```

### 🌍 使用OpenAI模型

如果您有OpenAI API密钥，可以使用：

#### 1. 配置API密钥

```bash
set OPENAI_API_KEY=your_openai_api_key
set FINNHUB_API_KEY=your_finnhub_api_key
```

#### 2. 运行示例

```bash
python examples/openai/demo_openai.py
```

## 示例程序说明

### 阿里百炼示例

| 文件名 | 功能描述 | 适用场景 |
|--------|----------|----------|
| `demo_dashscope_chinese.py` | 专门优化的中文股票分析 | 中文用户，完整分析报告 |
| `demo_dashscope.py` | 完整的TradingAgents演示 | 完整功能测试 |
| `demo_dashscope_simple.py` | 简化的LLM测试 | 快速验证模型连接 |
| `demo_dashscope_no_memory.py` | 禁用记忆功能的版本 | 兼容性问题排查 |

### OpenAI示例

| 文件名 | 功能描述 | 适用场景 |
|--------|----------|----------|
| `demo_openai.py` | OpenAI模型演示 | 有OpenAI API密钥的用户 |

## 获取API密钥

### 阿里百炼 API 密钥

1. 访问 [阿里百炼控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通百炼服务
4. 在控制台获取API密钥

### FinnHub API 密钥

1. 访问 [FinnHub官网](https://finnhub.io/)
2. 注册免费账户
3. 在仪表板获取API密钥

### OpenAI API 密钥

1. 访问 [OpenAI平台](https://platform.openai.com/)
2. 注册账户并完成验证
3. 在API密钥页面创建新密钥

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查密钥是否正确复制
   - 确认已开通相应服务

2. **网络连接问题**
   - 阿里百炼：检查国内网络连接
   - OpenAI：可能需要科学上网

3. **依赖包问题**
   - 确保已安装所有依赖：`pip install -r requirements.txt`
   - 检查虚拟环境是否激活

4. **记忆功能错误**
   - 使用 `demo_dashscope_no_memory.py` 版本
   - 或参考测试目录的集成测试

### 获取帮助

- 查看项目文档：`docs/` 目录
- 运行集成测试：`tests/integration/` 目录
- 提交Issue：项目GitHub页面

## 贡献

欢迎提交新的示例程序！请确保：

1. 代码清晰易懂
2. 包含详细注释
3. 提供使用说明
4. 遵循项目代码规范

## 许可证

本项目遵循项目根目录的LICENSE文件。
