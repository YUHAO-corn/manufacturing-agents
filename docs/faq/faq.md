# 制造业智能补货决策系统常见问题解答 (FAQ)

## 📋 概述

本文档收集了用户在使用制造业智能补货决策系统时最常遇到的问题和解答，帮助您快速解决常见问题。

## 🚀 安装和配置

### Q1: 安装时出现依赖冲突怎么办？

**A:** 依赖冲突通常是由于不同包的版本要求不兼容导致的。解决方法：

```bash
# 方法1: 使用新的虚拟环境
conda create -n manufacturing-ai-clean python=3.11
conda activate manufacturing-ai-clean
pip install -r requirements.txt

# 方法2: 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 方法3: 逐个安装核心依赖
pip install langchain-openai langgraph streamlit pandas requests
```

### Q2: API 密钥设置后仍然报错？

**A:** 检查以下几个方面：

1. **环境变量设置**：
```bash
# 检查环境变量是否正确设置
echo $DASHSCOPE_API_KEY
echo $TUSHARE_TOKEN
echo $JUHE_API_KEY

# Windows 用户
echo %DASHSCOPE_API_KEY%
echo %TUSHARE_TOKEN%
```

2. **密钥格式验证**：
```python
import os
# 阿里百炼密钥应该以 'sk-' 开头
dashscope_key = os.getenv('DASHSCOPE_API_KEY')
print(f"DashScope Key: {dashscope_key[:10]}..." if dashscope_key else "Not set")

# TuShare Token是字母数字组合
tushare_token = os.getenv('TUSHARE_TOKEN')
print(f"TuShare Token: {tushare_token[:10]}..." if tushare_token else "Not set")
```

3. **API连接测试**：
```python
# 测试阿里百炼连接
import dashscope
try:
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt='测试连接',
        max_tokens=10
    )
    print("阿里百炼API连接成功")
except Exception as e:
    print(f"阿里百炼API错误: {e}")

# 测试TuShare连接
import tushare as ts
try:
    pro = ts.pro_api(os.getenv('TUSHARE_TOKEN'))
    df = pro.daily(ts_code='000001.SZ', limit=1)
    print("TuShare API连接成功")
except Exception as e:
    print(f"TuShare API错误: {e}")
```

### Q3: 支持哪些 Python 版本？

**A:** 制造业智能补货决策系统支持 Python 3.10, 3.11, 和 3.12。推荐使用 Python 3.11 以获得最佳性能和兼容性。

```bash
# 检查 Python 版本
python --version

# 如果版本不符合要求，使用 pyenv 安装
pyenv install 3.11.7
pyenv global 3.11.7
```

### Q4: Web界面无法启动怎么办？

**A:** 常见的Web界面启动问题：

```bash
# 问题1: 端口被占用
streamlit run web/app.py --server.port 8502

# 问题2: 依赖缺失
pip install streamlit plotly

# 问题3: 权限问题
streamlit run web/app.py --server.headless true

# 问题4: 防火墙拦截
streamlit run web/app.py --server.address 0.0.0.0
```

## 💰 成本和使用

### Q5: 使用系统的成本是多少？

**A:** 成本主要来自 LLM API 调用：

**阿里百炼 (推荐)**:
- qwen-turbo: ¥0.003/1K tokens (最经济)
- qwen-plus: ¥0.008/1K tokens (平衡)
- qwen-max: ¥0.02/1K tokens (最强性能)

**单次分析成本估算**:
- 简单分析 (basic): ¥0.1-0.3
- 标准分析 (standard): ¥0.3-0.8
- 深度分析 (comprehensive): ¥0.8-2.0

**数据源成本**:
- TuShare Pro: 免费版本足够使用
- 聚合数据: 大部分API免费或低成本

### Q6: 如何降低使用成本？

**A:** 成本优化策略：

1. **选择经济模型**：
```bash
# 在 .env 文件中设置
DASHSCOPE_MODEL=qwen-turbo
GOOGLE_MODEL=gemini-1.5-flash
```

2. **启用缓存**：
```bash
ENABLE_CACHING=true
CACHE_TTL=3600
ENABLE_LOCAL_CACHE=true
```

3. **降低分析深度**：
```bash
ANALYSIS_DEPTH=basic
MAX_DEBATE_ROUNDS=1
```

4. **减少并发数**：
```bash
MAX_CONCURRENT_AGENTS=2
```

## 🏭 业务应用

### Q7: 适用于哪些制造业场景？

**A:** 系统适用于多种制造业补货决策场景：

**适用行业**:
- 汽车制造业 (零部件补货)
- 电子制造业 (元器件采购)
- 家电制造业 (原材料管理)
- 纺织服装业 (面料库存)
- 食品制造业 (原料补货)

**适用场景**:
- 原材料补货决策
- 零部件库存管理
- 季节性需求预测
- 紧急补货决策
- 供应商选择

### Q8: 分析结果的准确性如何？

**A:** 分析准确性取决于多个因素：

**影响因素**:
- 数据质量和完整性
- 市场环境的复杂性
- 智能体配置的合理性
- 历史数据的丰富程度

**提升准确性的方法**:
1. 使用高质量数据源
2. 启用多智能体辩论
3. 配置合适的决策阈值
4. 定期更新系统配置

**建议**:
- 将AI建议作为决策参考，而非最终决策
- 结合企业实际情况进行判断
- 建立反馈机制优化模型

### Q9: 如何处理特殊的业务需求？

**A:** 系统提供多种自定义选项：

1. **智能体配置定制**：
```bash
# 禁用不需要的智能体
NEWS_ANALYST_ENABLED=false
CONSUMER_ANALYST_ENABLED=false

# 调整分析重点
MARKET_ANALYST_WEIGHT=0.4
TREND_ANALYST_WEIGHT=0.6
```

2. **数据源选择**：
```bash
# 启用特定数据源
TUSHARE_ENABLED=true
JUHE_WEATHER_ENABLED=true
GOOGLE_NEWS_ENABLED=false
```

3. **决策阈值调整**：
```bash
DECISION_THRESHOLD=0.8  # 提高决策门槛
RISK_THRESHOLD=0.3      # 降低风险容忍度
```

## ⚡ 性能和优化

### Q10: 分析速度慢怎么办？

**A:** 性能优化方法：

1. **硬件优化**：
```bash
# 增加内存和CPU资源
# 使用SSD存储
# 确保网络连接稳定
```

2. **配置优化**：
```bash
# 增加并发数 (在资源允许的情况下)
MAX_CONCURRENT_AGENTS=5
MAX_CONCURRENT_REQUESTS=15

# 启用缓存
ENABLE_CACHING=true
REDIS_ENABLED=true
```

3. **模型选择**：
```bash
# 使用更快的模型
DASHSCOPE_MODEL=qwen-turbo
GOOGLE_MODEL=gemini-1.5-flash
```

### Q11: 内存占用过高怎么办？

**A:** 内存优化策略：

1. **启用内存清理**：
```bash
ENABLE_MEMORY_CLEANUP=true
MEMORY_CLEANUP_INTERVAL=300
MAX_MEMORY_USAGE_MB=1024
```

2. **减少并发**：
```bash
MAX_CONCURRENT_AGENTS=2
```

3. **使用轻量级模型**：
```bash
DASHSCOPE_MODEL=qwen-turbo
```

## 🔧 技术问题

### Q12: 数据库连接失败怎么办？

**A:** 数据库问题排查：

1. **检查数据库状态**：
```bash
# MongoDB
sudo systemctl status mongod

# Redis
sudo systemctl status redis
```

2. **测试连接**：
```python
# MongoDB 连接测试
from pymongo import MongoClient
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.manufacturing_ai
    print("MongoDB 连接成功")
except Exception as e:
    print(f"MongoDB 连接失败: {e}")

# Redis 连接测试
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print("Redis 连接成功")
except Exception as e:
    print(f"Redis 连接失败: {e}")
```

3. **使用文件缓存降级**：
```bash
# 如果数据库不可用，系统会自动降级到文件缓存
MONGODB_ENABLED=false
REDIS_ENABLED=false
ENABLE_LOCAL_CACHE=true
```

### Q13: 如何调试智能体执行过程？

**A:** 调试方法：

1. **启用调试模式**：
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

2. **查看日志**：
```bash
# 实时查看日志
tail -f logs/manufacturing_ai.log

# 搜索特定错误
grep "ERROR" logs/manufacturing_ai.log
```

3. **Web界面调试**：
- 在Web界面中查看实时进度
- 检查每个智能体的输出
- 查看决策过程的详细信息

### Q14: 如何备份和恢复数据？

**A:** 数据备份策略：

1. **结果数据备份**：
```bash
# 备份分析结果
tar -czf results_backup_$(date +%Y%m%d).tar.gz ./results/

# 定期备份脚本
#!/bin/bash
BACKUP_DIR="/backup/manufacturing_ai"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/results_$DATE.tar.gz" ./results/
```

2. **数据库备份**：
```bash
# MongoDB 备份
mongodump --db manufacturing_ai --out /backup/mongodb/

# Redis 备份
redis-cli --rdb /backup/redis/dump.rdb
```

3. **配置备份**：
```bash
# 备份配置文件
cp .env .env.backup.$(date +%Y%m%d)
```

## 🆘 寻求帮助

### Q15: 遇到问题时如何获取帮助？

**A:** 获取帮助的途径：

1. **查看文档**：
   - [安装指南](../overview/installation.md)
   - [配置指南](../configuration/config-guide.md)
   - [故障排除](../troubleshooting/)

2. **GitHub支持**：
   - 搜索 [已有Issues](https://github.com/your-org/manufacturing-ai-agents/issues)
   - 提交新的 [Issue](https://github.com/your-org/manufacturing-ai-agents/issues/new)

3. **提交Issue时请包含**：
   - 系统信息 (操作系统、Python版本)
   - 完整的错误日志
   - 复现步骤
   - 配置信息 (隐藏敏感信息)

4. **技术支持邮箱**：
   - manufacturing-ai@example.com

### Q16: 如何为项目做贡献？

**A:** 贡献方式：

1. **代码贡献**：
   - Fork项目仓库
   - 创建特性分支
   - 提交Pull Request

2. **文档改进**：
   - 修正文档错误
   - 添加使用示例
   - 翻译文档

3. **问题反馈**：
   - 报告Bug
   - 提出功能建议
   - 分享使用经验

4. **社区建设**：
   - 帮助其他用户解答问题
   - 分享最佳实践
   - 推广项目应用

## 🔄 版本更新

### Q17: 如何更新到最新版本？

**A:** 更新方法：

1. **备份当前配置**：
```bash
cp .env .env.backup
cp -r results/ results_backup/
```

2. **更新代码**：
```bash
git fetch origin
git pull origin main
```

3. **更新依赖**：
```bash
pip install -r requirements.txt --upgrade
```

4. **检查配置兼容性**：
```bash
python scripts/validate_config.py
```

### Q18: 版本升级后出现兼容性问题？

**A:** 兼容性问题解决：

1. **查看版本变更日志**：
   - 检查 CHANGELOG.md
   - 了解破坏性变更

2. **更新配置文件**：
   - 对比新的 .env.example
   - 添加新增的配置项

3. **重新生成缓存**：
```bash
rm -rf ./cache/*
rm -rf ./data/cache/*
```

4. **如果问题持续存在**：
   - 回滚到之前版本
   - 提交Issue报告问题

---

**💡 小贴士**: 建议定期查看此FAQ文档的更新，我们会根据用户反馈持续完善内容。

如果您的问题未在此FAQ中找到答案，请随时通过GitHub Issues或邮箱联系我们！
