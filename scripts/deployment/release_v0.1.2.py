#!/usr/bin/env python3
"""
TradingAgents-CN v0.1.2 版本发布脚本
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(command, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """检查Git状态"""
    print("🔍 检查Git状态...")
    
    success, stdout, stderr = run_command("git status --porcelain")
    if not success:
        print(f"❌ Git状态检查失败: {stderr}")
        return False
    
    if stdout.strip():
        print("📝 发现未提交的更改:")
        print(stdout)
        return True
    else:
        print("✅ 工作目录干净")
        return True

def create_release_tag():
    """创建发布标签"""
    print("🏷️ 创建版本标签...")
    
    tag_name = "cn-v0.1.2"
    tag_message = "TradingAgents-CN v0.1.2 - Web管理界面和Google AI支持"
    
    # 检查标签是否已存在
    success, stdout, stderr = run_command(f"git tag -l {tag_name}")
    if success and tag_name in stdout:
        print(f"⚠️ 标签 {tag_name} 已存在")
        return True
    
    # 创建标签
    success, stdout, stderr = run_command(f'git tag -a {tag_name} -m "{tag_message}"')
    if success:
        print(f"✅ 标签 {tag_name} 创建成功")
        return True
    else:
        print(f"❌ 标签创建失败: {stderr}")
        return False

def generate_release_notes():
    """生成发布说明"""
    print("📝 生成发布说明...")
    
    release_notes = """
# TradingAgents-CN v0.1.2 发布说明

## 🌐 Web管理界面和Google AI支持

### ✨ 主要新功能

#### 🌐 Streamlit Web管理界面
- 完整的Web股票分析平台
- 直观的用户界面和实时进度显示
- 支持多种分析师组合选择
- 可视化的分析结果展示
- 响应式设计，支持移动端访问

#### 🤖 Google AI模型集成
- 完整的Google Gemini模型支持
- 支持gemini-2.0-flash、gemini-1.5-pro等模型
- 智能混合嵌入服务（Google AI + 阿里百炼）
- 完美的中文分析能力
- 稳定的LangChain集成

#### 🔧 多LLM提供商支持
- Web界面支持LLM提供商选择
- 阿里百炼和Google AI无缝切换
- 自动配置最优嵌入服务
- 统一的配置管理界面

### 🔧 改进优化

- 📊 新增分析配置信息显示
- 🗂️ 项目结构优化（tests/docs/web目录规范化）
- 🔑 多种API服务配置支持
- 🧪 完整的测试体系（25+个测试文件）

### 🚀 快速开始

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置API密钥
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加您的API密钥
# DASHSCOPE_API_KEY=your_dashscope_key
# GOOGLE_API_KEY=your_google_key  # 可选
```

#### 启动Web界面
```bash
# Windows
start_web.bat

# Linux/Mac
python -m streamlit run web/app.py
```

#### 使用CLI工具
```bash
python cli/main.py --stock AAPL --analysts market fundamentals
```

### 📚 文档和支持

- 📖 [完整文档](./docs/)
- 🧪 [测试指南](./tests/README.md)
- 🌐 [Web界面指南](./web/README.md)
- 💡 [示例代码](./examples/)

### 🙏 致谢

感谢 [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) 原始项目的开发者们，为金融AI领域提供了优秀的开源框架。

### 📄 许可证

本项目遵循 Apache 2.0 许可证。
"""
    
    # 保存发布说明
    release_file = Path("RELEASE_NOTES_v0.1.2.md")
    with open(release_file, 'w', encoding='utf-8') as f:
        f.write(release_notes.strip())
    
    print(f"✅ 发布说明已保存到: {release_file}")
    return True

def show_release_summary():
    """显示发布摘要"""
    print("\n" + "="*60)
    print("🎉 TradingAgents-CN v0.1.2 发布准备完成！")
    print("="*60)
    
    print("\n📋 本次发布包含:")
    print("  🌐 Streamlit Web管理界面")
    print("  🤖 Google AI模型集成")
    print("  🔧 多LLM提供商支持")
    print("  🧪 完整的测试体系")
    print("  🗂️ 项目结构优化")
    
    print("\n📁 主要文件更新:")
    print("  ✅ VERSION: 0.1.1 → 0.1.2")
    print("  ✅ CHANGELOG.md: 新增v0.1.2更新日志")
    print("  ✅ README-CN.md: 新增Web界面和Google AI使用说明")
    print("  ✅ web/README.md: 完整的Web界面使用指南")
    print("  ✅ docs/configuration/google-ai-setup.md: Google AI配置指南")
    print("  ✅ web/: 完整的Web界面，支持多LLM提供商")
    print("  ✅ tests/: 25+个测试文件，规范化目录结构")
    
    print("\n🚀 下一步操作:")
    print("  1. 检查所有更改: git status")
    print("  2. 提交更改: git add . && git commit -m 'Release v0.1.2'")
    print("  3. 推送标签: git push origin cn-v0.1.2")
    print("  4. 创建GitHub Release")
    
    print("\n💡 使用方法:")
    print("  Web界面: python -m streamlit run web/app.py")
    print("  CLI工具: python cli/main.py --help")
    print("  测试: python tests/test_web_interface.py")

def main():
    """主函数"""
    print("🚀 TradingAgents-CN v0.1.2 版本发布")
    print("="*50)
    
    # 检查Git状态
    if not check_git_status():
        return False
    
    # 创建发布标签
    if not create_release_tag():
        return False
    
    # 生成发布说明
    if not generate_release_notes():
        return False
    
    # 显示发布摘要
    show_release_summary()
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 版本发布准备完成！")
    else:
        print("\n❌ 版本发布准备失败")
        sys.exit(1)
