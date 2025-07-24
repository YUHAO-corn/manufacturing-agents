#!/usr/bin/env python3
"""
TradingAgents-CN Web应用启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """检查必要的依赖是否已安装"""

    required_packages = ['streamlit', 'plotly']
    missing_packages = []

    for package in required_packages:
        try:
            if package == 'streamlit':
                import streamlit
            elif package == 'plotly':
                import plotly
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ 缺少必要的依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    print("✅ 依赖包检查通过")
    return True

def clean_cache_files():
    """清理Python缓存文件，避免Streamlit文件监控错误"""
    
    project_root = Path(__file__).parent.parent
    cache_dirs = list(project_root.rglob("__pycache__"))
    
    if cache_dirs:
        print("🧹 清理Python缓存文件...")
        for cache_dir in cache_dirs:
            try:
                import shutil
                shutil.rmtree(cache_dir)
                print(f"  ✅ 已清理: {cache_dir.relative_to(project_root)}")
            except Exception as e:
                print(f"  ⚠️ 清理失败: {cache_dir.relative_to(project_root)} - {e}")
        print("✅ 缓存文件清理完成")
    else:
        print("✅ 无需清理缓存文件")

def check_api_keys():
    """检查API密钥配置"""
    
    from dotenv import load_dotenv
    
    # 加载环境变量
    project_root = Path(__file__).parent.parent
    load_dotenv(project_root / ".env")
    
    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    if not dashscope_key or not finnhub_key:
        print("⚠️ API密钥配置不完整")
        print("请确保在.env文件中配置以下密钥:")
        if not dashscope_key:
            print("  - DASHSCOPE_API_KEY (阿里百炼)")
        if not finnhub_key:
            print("  - FINNHUB_API_KEY (金融数据)")
        print("\n配置方法:")
        print("1. 复制 .env.example 为 .env")
        print("2. 编辑 .env 文件，填入真实API密钥")
        return False
    
    print("✅ API密钥配置完成")
    return True

# 在文件顶部添加导入
import signal
import psutil

# 修改 main() 函数中的启动部分
def main():
    """主函数"""
    
    print("🚀 TradingAgents-CN Web应用启动器")
    print("=" * 50)
    
    # 清理缓存文件（避免Streamlit文件监控错误）
    clean_cache_files()
    
    # 检查依赖
    print("🔍 检查依赖包...")
    if not check_dependencies():
        return
    
    # 检查API密钥
    print("🔑 检查API密钥...")
    if not check_api_keys():
        print("\n💡 提示: 您仍可以启动Web应用查看界面，但无法进行实际分析")
        response = input("是否继续启动? (y/n): ").lower().strip()
        if response != 'y':
            return
    
    # 启动Streamlit应用
    print("\n🌐 启动Web应用...")
    
    web_dir = Path(__file__).parent
    app_file = web_dir / "app.py"
    
    if not app_file.exists():
        print(f"❌ 找不到应用文件: {app_file}")
        return
    
    # 构建Streamlit命令
    config_dir = web_dir.parent / ".streamlit"
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        str(app_file),
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false",
        "--server.fileWatcherType", "auto",
        "--server.runOnSave", "true"
    ]
    
    # 如果配置目录存在，添加配置路径
    if config_dir.exists():
        print(f"📁 使用配置目录: {config_dir}")
        # Streamlit会自动查找.streamlit/config.toml文件
    
    print(f"执行命令: {' '.join(cmd)}")
    print("\n🎉 Web应用启动中...")
    print("📱 浏览器将自动打开 http://localhost:8501")
    print("⏹️  按 Ctrl+C 停止应用")
    print("=" * 50)
    
    # 创建进程对象而不是直接运行
    process = None
    
    def signal_handler(signum, frame):
        """信号处理函数"""
        print("\n\n⏹️ 接收到停止信号，正在关闭Web应用...")
        if process:
            try:
                # 终止进程及其子进程
                parent = psutil.Process(process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
                
                # 等待进程结束
                parent.wait(timeout=5)
                print("✅ Web应用已成功停止")
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                print("⚠️ 强制终止进程")
                if process:
                    process.kill()
        sys.exit(0)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # 启动Streamlit进程
        process = subprocess.Popen(cmd, cwd=web_dir)
        process.wait()  # 等待进程结束
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
