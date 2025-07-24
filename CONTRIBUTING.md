# 贡献指南

感谢您对 TradingAgents 中文增强版的关注和支持！我们欢迎各种形式的贡献，包括但不限于代码、文档、测试、反馈和建议。

## 🤝 如何贡献

### 贡献类型

我们欢迎以下类型的贡献：

- 🐛 **Bug 修复** - 发现并修复代码中的问题
- ✨ **新功能** - 添加新的功能特性
- 📚 **文档改进** - 完善文档、教程和示例
- 🌐 **本地化** - 翻译和本地化工作
- 🎨 **代码优化** - 性能优化和代码重构
- 🧪 **测试** - 添加或改进测试用例
- 💡 **建议** - 提出改进建议和功能请求

### 贡献流程

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   git clone https://github.com/YourUsername/TradingAgents-CN.git
   cd TradingAgents-CN
   ```

2. **设置开发环境**
   ```bash
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   
   # 安装依赖
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # 如果存在
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   # 或
   git checkout -b docs/your-documentation-update
   ```

4. **进行开发**
   - 编写代码或文档
   - 添加必要的测试
   - 确保代码符合项目规范

5. **测试您的更改**
   ```bash
   # 运行测试
   python -m pytest tests/
   
   # 检查代码风格
   flake8 tradingagents/
   black tradingagents/
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   # 或
   git commit -m "fix: 修复某个问题"
   # 或
   git commit -m "docs: 更新文档内容"
   ```

7. **推送到您的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 填写详细的描述
   - 等待代码审查

## 📝 代码规范

### Python 代码规范

我们遵循 PEP 8 Python 代码规范：

```python
# 好的示例
class TradingAgent:
    """交易智能体类
    
    负责执行交易决策和风险管理。
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logger()
    
    def analyze_market(self, symbol: str, date: str) -> Dict[str, Any]:
        """分析市场数据
        
        Args:
            symbol: 股票代码
            date: 分析日期
            
        Returns:
            分析结果字典
        """
        # 实现分析逻辑
        pass
```

### 提交信息规范

使用语义化提交信息：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

**类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat(agents): 添加量化分析师智能体

- 实现基于统计套利的分析方法
- 添加动量因子分析功能
- 包含完整的单元测试

Closes #123
```

### 文档规范

- 使用清晰的中文表达
- 提供完整的代码示例
- 包含必要的图表和说明
- 遵循 Markdown 格式规范

## 🧪 测试指南

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_agents.py

# 运行带覆盖率的测试
python -m pytest --cov=tradingagents tests/
```

### 编写测试

```python
import pytest
from manufacturingagents.agents.analysts.base_analyst import BaseAnalyst

class TestBaseAnalyst:
    """基础分析师测试类"""
    
    def setup_method(self):
        """测试前的设置"""
        self.config = {"test": True}
        self.analyst = BaseAnalyst(llm=None, config=self.config)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.analyst.config == self.config
        assert hasattr(self.analyst, 'memory')
    
    def test_analysis_method(self):
        """测试分析方法"""
        # 模拟测试数据
        test_data = {"symbol": "AAPL", "price": 150.0}
        
        # 执行测试
        result = self.analyst.perform_analysis(test_data)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "analysis_score" in result
```

## 📋 Issue 指南

### 报告 Bug

使用以下模板报告 Bug：

```markdown
## Bug 描述
简要描述遇到的问题

## 复现步骤
1. 执行的代码或操作
2. 使用的配置
3. 输入的参数

## 预期行为
描述期望的结果

## 实际行为
描述实际发生的情况

## 环境信息
- Python 版本:
- TradingAgents 版本:
- 操作系统:
- 相关依赖版本:

## 错误日志
```
粘贴完整的错误信息
```

## 附加信息
任何其他相关信息
```

### 功能请求

使用以下模板提出功能请求：

```markdown
## 功能描述
清晰描述您希望添加的功能

## 使用场景
描述这个功能的使用场景和价值

## 建议的实现方式
如果有想法，可以描述建议的实现方式

## 替代方案
描述您考虑过的替代解决方案

## 附加信息
任何其他相关信息或参考资料
```

## 🎯 开发重点

### 当前优先级

1. **中国市场支持**
   - A股、港股数据集成
   - 中文金融术语优化
   - 交易时间和节假日适配

2. **国产LLM集成**
   - 文心一言 API 集成
   - 通义千问 API 集成
   - 智谱清言 API 集成

3. **中文数据源**
   - Tushare 数据源集成
   - AkShare 数据源集成
   - 东方财富数据源集成

4. **性能优化**
   - 缓存机制优化
   - 并发处理改进
   - 内存使用优化

### 技术栈

- **核心框架**: LangChain, LangGraph
- **数据处理**: Pandas, NumPy
- **API集成**: Requests, aiohttp
- **测试**: pytest, unittest
- **代码质量**: black, flake8, mypy
- **文档**: Markdown, Mermaid

## 🏆 贡献者认可

我们会在以下地方认可贡献者的工作：

- **README.md** 中的贡献者列表
- **CHANGELOG.md** 中的版本更新说明
- **GitHub Releases** 中的感谢名单
- 项目文档中的作者信息

### 贡献者等级

- 🥉 **贡献者**: 提交过 PR 或 Issue
- 🥈 **活跃贡献者**: 多次贡献且质量较高
- 🥇 **核心贡献者**: 长期活跃且有重要贡献
- 👑 **维护者**: 拥有仓库写权限的核心团队成员

## 📞 联系方式

如果您有任何问题或需要帮助，可以通过以下方式联系我们：

- **GitHub Issues**: [提交问题](https://github.com/hsliuping/TradingAgents-CN/issues)
- **GitHub Discussions**: [参与讨论](https://github.com/hsliuping/TradingAgents-CN/discussions)
- **邮箱**: hsliup@163.com

## 🙏 感谢

感谢每一位为 TradingAgents 中文增强版做出贡献的开发者！您的贡献让这个项目变得更好。

---

再次感谢您的贡献！让我们一起构建更好的金融AI工具！ 🚀
