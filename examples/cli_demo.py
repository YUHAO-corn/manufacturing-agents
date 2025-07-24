#!/usr/bin/env python3
"""
CLI工具中文化演示脚本
展示TradingAgents CLI工具的中文支持功能
"""

import subprocess
import sys
import time

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"🎯 {description}")
    print(f"命令: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(
            command.split(), 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
    except subprocess.TimeoutExpired:
        print("⏰ 命令执行超时")
    except Exception as e:
        print(f"❌ 执行错误: {e}")
    
    time.sleep(1)

def main():
    """主演示函数"""
    print("🚀 TradingAgents CLI 中文化功能演示")
    print("=" * 60)
    print("本演示将展示CLI工具的各种中文化功能")
    print()
    
    # 演示各种命令
    commands = [
        ("python -m cli.main --help", "主帮助信息 - 显示所有可用命令"),
        ("python -m cli.main help", "中文帮助 - 详细的中文使用指南"),
        ("python -m cli.main config", "配置信息 - 显示LLM提供商和设置"),
        ("python -m cli.main version", "版本信息 - 显示软件版本和特性"),
        ("python -m cli.main examples", "示例程序 - 列出可用的演示程序"),
        ("python -m cli.main test", "测试功能 - 运行系统集成测试"),
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print("\n" + "="*60)
    print("🎉 CLI中文化演示完成！")
    print("="*60)
    print()
    print("💡 主要特色:")
    print("• ✅ 完整的中文用户界面")
    print("• ✅ 双语命令说明")
    print("• ✅ 中文错误提示")
    print("• ✅ 阿里百炼大模型支持")
    print("• ✅ 详细的使用指导")
    print()
    print("🚀 下一步:")
    print("1. 配置API密钥: 编辑 .env 文件")
    print("2. 运行测试: python -m cli.main test")
    print("3. 开始分析: python -m cli.main analyze")
    print()
    print("📖 获取更多帮助:")
    print("• python -m cli.main help")
    print("• 查看 examples/ 目录的演示程序")
    print("• 查看 docs/ 目录的详细文档")

if __name__ == "__main__":
    main()
