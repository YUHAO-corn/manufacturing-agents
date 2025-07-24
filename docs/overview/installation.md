# 制造业智能补货决策系统安装指南

## 📋 概述

本指南提供了制造业智能补货决策系统的详细安装说明，包括不同操作系统的安装步骤、依赖管理、环境配置和常见问题解决方案。

## 💻 系统要求

### 硬件要求
- **CPU**: 双核 2.0GHz 或更高 (推荐四核)
- **内存**: 最少 4GB RAM (推荐 8GB 或更高)
- **存储**: 至少 3GB 可用磁盘空间
- **网络**: 稳定的互联网连接 (用于API调用和数据获取)

### 软件要求
- **操作系统**: 
  - Windows 10/11 (64位)
  - macOS 10.15 (Catalina) 或更高版本
  - Linux (Ubuntu 18.04+, CentOS 7+, 或其他主流发行版)
- **Python**: 3.10, 3.11, 或 3.12 (推荐 3.11)
- **Git**: 用于克隆代码仓库

## 🚀 安装步骤

### 1. 安装 Python

#### Windows
```powershell
# 方法1: 从官网下载安装包
# 访问 https://www.python.org/downloads/windows/
# 下载 Python 3.11.x 安装包并运行

# 方法2: 使用 Chocolatey
choco install python311

# 方法3: 使用 Microsoft Store
# 在 Microsoft Store 搜索 "Python 3.11" 并安装

# 验证安装
python --version
pip --version
```

#### macOS
```bash
# 方法1: 使用 Homebrew (推荐)
brew install python@3.11

# 方法2: 使用 pyenv
brew install pyenv
pyenv install 3.11.7
pyenv global 3.11.7

# 方法3: 从官网下载
# 访问 https://www.python.org/downloads/macos/

# 验证安装
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# 更新包列表
sudo apt update

# 安装 Python 3.11
sudo apt install python3.11 python3.11-pip python3.11-venv

# 设置默认 Python 版本 (可选)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# 验证安装
python3 --version
pip3 --version
```

#### Linux (CentOS/RHEL)
```bash
# 安装 EPEL 仓库
sudo yum install epel-release

# 安装 Python 3.11
sudo yum install python311 python311-pip

# 或使用 dnf (较新版本)
sudo dnf install python3.11 python3.11-pip

# 验证安装
python3.11 --version
pip3.11 --version
```

### 2. 克隆项目

```bash
# 克隆项目仓库
git clone https://github.com/your-org/manufacturing-ai-agents.git

# 进入项目目录
cd manufacturing-ai-agents
```

### 3. 创建虚拟环境

#### 使用 venv (推荐)
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 使用 conda
```bash
# 创建虚拟环境
conda create -n manufacturing-ai python=3.11

# 激活环境
conda activate manufacturing-ai
```

### 4. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 如果遇到依赖冲突，可以尝试
pip install -r requirements.txt --force-reinstall
```

### 5. 环境配置

#### 创建配置文件
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
# Windows
notepad .env

# macOS/Linux
nano .env
# 或
vim .env
```

#### 必需的API密钥配置
```bash
# .env 文件内容示例

# =============================================================================
# 🤖 LLM 服务配置 (至少配置一个)
# =============================================================================

# 🇨🇳 阿里百炼 (推荐，国内访问速度快)
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DASHSCOPE_MODEL=qwen-max

# Google AI (免费额度大)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-1.5-pro

# OpenAI (可选)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# =============================================================================
# 📊 数据源配置
# =============================================================================

# TuShare Pro (经济数据，需要注册)
TUSHARE_TOKEN=your_tushare_token_here

# 聚合数据 (新闻和天气数据)
JUHE_API_KEY=your_juhe_api_key_here

# Google News (可选，用于补充新闻数据)
GOOGLE_NEWS_API_KEY=your_google_news_api_key_here

# =============================================================================
# 🗄️ 数据库配置 (可选)
# =============================================================================

# MongoDB (用于数据持久化)
MONGODB_ENABLED=false
MONGODB_URI=mongodb://localhost:27017/manufacturing_ai

# Redis (用于缓存)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0

# =============================================================================
# 🔧 系统配置
# =============================================================================

# 日志级别
LOG_LEVEL=INFO

# 是否启用调试模式
DEBUG=false

# Web界面端口
STREAMLIT_PORT=8501
```

### 6. API密钥获取指南

#### 🇨🇳 阿里百炼 API (推荐)
1. 访问 [阿里云百炼平台](https://dashscope.aliyun.com/)
2. 注册/登录阿里云账户
3. 开通百炼服务
4. 创建API密钥
5. 复制API密钥到 `.env` 文件

#### Google AI API
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 登录Google账户
3. 创建新的API密钥
4. 复制API密钥到 `.env` 文件

#### TuShare Pro Token (经济数据)
1. 访问 [TuShare Pro](https://tushare.pro/)
2. 注册账户并实名认证
3. 获取Token
4. 复制Token到 `.env` 文件

#### 聚合数据API (新闻/天气)
1. 访问 [聚合数据](https://www.juhe.cn/)
2. 注册账户
3. 申请相关API服务
4. 复制API密钥到 `.env` 文件

### 7. 验证安装

#### 运行测试命令
```bash
# 测试基础功能
python -c "import manufacturingagents; print('安装成功!')"

# 测试配置
python -c "from manufacturingagents.config import get_config; print('配置加载成功!')"

# 测试LLM连接
python tests/test_llm_connection.py
```

#### 启动Web界面
```bash
# 启动Streamlit界面
streamlit run web/app.py

# 或使用Python启动
python web/run_web.py
```

浏览器访问: `http://localhost:8501`

### 8. 数据库安装 (可选)

#### MongoDB (推荐用于生产环境)
```bash
# Ubuntu/Debian
sudo apt install mongodb

# macOS
brew install mongodb-community

# Windows
# 从官网下载安装包: https://www.mongodb.com/try/download/community

# 启动服务
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

#### Redis (缓存加速)
```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# Windows
# 从GitHub下载: https://github.com/MicrosoftArchive/redis/releases

# 启动服务
sudo systemctl start redis  # Linux
brew services start redis  # macOS
```

## 🔧 高级配置

### Docker 部署 (推荐用于生产环境)

#### 使用 Docker Compose
```bash
# 构建和启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 单独运行应用
```bash
# 构建镜像
docker build -t manufacturing-ai-agents .

# 运行容器
docker run -d \
  --name manufacturing-ai \
  -p 8501:8501 \
  --env-file .env \
  manufacturing-ai-agents
```

### 性能优化配置

#### 多进程配置
```bash
# 在 .env 文件中添加
WORKERS=4
MAX_CONCURRENT_REQUESTS=10
CACHE_TTL=3600
```

#### 内存优化
```bash
# 限制模型并发数
MAX_CONCURRENT_AGENTS=3

# 启用内存清理
ENABLE_MEMORY_CLEANUP=true
MEMORY_CLEANUP_INTERVAL=600
```

## ❗ 常见问题

### 1. Python 版本问题
```bash
# 问题: Python版本不兼容
# 解决: 使用pyenv管理多个Python版本
pyenv install 3.11.7
pyenv local 3.11.7
```

### 2. 依赖安装失败
```bash
# 问题: pip安装失败
# 解决: 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 3. API访问问题
```bash
# 问题: API连接超时
# 解决: 检查网络连接和API密钥
curl -H "Authorization: Bearer YOUR_API_KEY" https://dashscope.aliyuncs.com/api/v1/models
```

### 4. 内存不足
```bash
# 问题: 内存不足导致程序崩溃
# 解决: 减少并发数量或增加虚拟内存
export MAX_CONCURRENT_AGENTS=2
```

### 5. 端口冲突
```bash
# 问题: 端口被占用
# 解决: 修改端口配置
streamlit run web/app.py --server.port 8502
```

## 📚 下一步

安装完成后，建议继续阅读：

1. [快速开始指南](quick-start.md) - 运行第一个补货分析
2. [配置指南](../configuration/config-guide.md) - 详细配置说明
3. [使用指南](../usage/web-interface-guide.md) - Web界面使用说明
4. [开发指南](../development/development-workflow.md) - 参与项目开发

## 💬 获取帮助

如果在安装过程中遇到问题：

1. 查看 [常见问题解答](../faq/faq.md)
2. 搜索 [GitHub Issues](https://github.com/your-org/manufacturing-ai-agents/issues)
3. 提交新的 [Issue](https://github.com/your-org/manufacturing-ai-agents/issues/new)

祝您使用愉快！🎉
