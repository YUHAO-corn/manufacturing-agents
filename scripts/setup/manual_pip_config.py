#!/usr/bin/env python3
"""
手动创建pip配置文件
适用于老版本pip不支持config命令的情况
"""

import os
import sys
from pathlib import Path

def create_pip_config():
    """手动创建pip配置文件"""
    print("🔧 手动创建pip配置文件")
    print("=" * 40)
    
    # 检查pip版本
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"📦 当前pip版本: {result.stdout.strip()}")
        else:
            print("⚠️ 无法获取pip版本")
    except Exception as e:
        print(f"⚠️ 检查pip版本失败: {e}")
    
    # 确定配置文件路径
    if sys.platform == "win32":
        # Windows: %APPDATA%\pip\pip.ini
        config_dir = Path(os.environ.get('APPDATA', '')) / "pip"
        config_file = config_dir / "pip.ini"
    else:
        # Linux/macOS: ~/.pip/pip.conf
        config_dir = Path.home() / ".pip"
        config_file = config_dir / "pip.conf"
    
    print(f"📁 配置目录: {config_dir}")
    print(f"📄 配置文件: {config_file}")
    
    # 创建配置目录
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        print("✅ 配置目录已创建")
    except Exception as e:
        print(f"❌ 创建配置目录失败: {e}")
        return False
    
    # 配置内容
    config_content = """[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 120

[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
"""
    
    # 写入配置文件
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ pip配置文件已创建")
        print(f"📄 配置文件位置: {config_file}")
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return False
    
    # 显示配置内容
    print("\n📊 配置内容:")
    print(config_content)
    
    # 测试配置
    print("🧪 测试pip配置...")
    try:
        # 尝试使用新配置安装一个小包进行测试
        import subprocess
        
        # 先检查是否已安装
        result = subprocess.run([sys.executable, "-m", "pip", "show", "six"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            # 如果没安装，尝试安装six包测试
            print("📦 测试安装six包...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "six"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ 配置测试成功，可以正常安装包")
            else:
                print("❌ 配置测试失败")
                print(f"错误信息: {result.stderr}")
        else:
            print("✅ pip配置正常（six包已安装）")
    
    except subprocess.TimeoutExpired:
        print("⏰ 测试超时，但配置文件已创建")
    except Exception as e:
        print(f"⚠️ 无法测试配置: {e}")
    
    return True

def install_packages():
    """安装必要的包"""
    print("\n📦 安装必要的包...")
    
    packages = ["pymongo", "redis"]
    
    for package in packages:
        print(f"\n📥 安装 {package}...")
        try:
            import subprocess
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ {package} 安装成功")
            else:
                print(f"❌ {package} 安装失败:")
                print(result.stderr)
                
                # 如果失败，尝试使用临时镜像
                print(f"🔄 尝试使用临时镜像安装 {package}...")
                result2 = subprocess.run([
                    sys.executable, "-m", "pip", "install", 
                    "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/",
                    "--trusted-host", "pypi.tuna.tsinghua.edu.cn",
                    package
                ], capture_output=True, text=True, timeout=120)
                
                if result2.returncode == 0:
                    print(f"✅ {package} 使用临时镜像安装成功")
                else:
                    print(f"❌ {package} 仍然安装失败")
        
        except subprocess.TimeoutExpired:
            print(f"⏰ {package} 安装超时")
        except Exception as e:
            print(f"❌ {package} 安装异常: {e}")

def check_pip_version():
    """检查并建议升级pip"""
    print("\n🔍 检查pip版本...")
    
    try:
        import subprocess
        
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            version_info = result.stdout.strip()
            print(f"📦 当前版本: {version_info}")
            
            # 提取版本号
            import re
            version_match = re.search(r'pip (\d+)\.(\d+)', version_info)
            if version_match:
                major, minor = int(version_match.group(1)), int(version_match.group(2))
                
                if major < 10:
                    print("⚠️ pip版本较老，建议升级")
                    print("💡 升级命令:")
                    print("   python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn")
                else:
                    print("✅ pip版本较新，支持config命令")
                    print("💡 可以使用以下命令配置:")
                    print("   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/")
                    print("   pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn")
    
    except Exception as e:
        print(f"❌ 检查pip版本失败: {e}")

def main():
    """主函数"""
    try:
        # 检查pip版本
        check_pip_version()
        
        # 创建配置文件
        success = create_pip_config()
        
        if success:
            # 安装包
            install_packages()
            
            print("\n🎉 pip源配置完成!")
            print("\n💡 使用说明:")
            print("1. 配置文件已创建，以后安装包会自动使用清华镜像")
            print("2. 如果仍然很慢，可以临时使用:")
            print("   pip install -i https://pypi.douban.com/simple/ --trusted-host pypi.douban.com package_name")
            print("3. 其他可用镜像:")
            print("   - 豆瓣: https://pypi.douban.com/simple/")
            print("   - 中科大: https://pypi.mirrors.ustc.edu.cn/simple/")
            print("   - 华为云: https://mirrors.huaweicloud.com/repository/pypi/simple/")
            
            print("\n🎯 下一步:")
            print("1. 运行系统初始化: python scripts/setup/initialize_system.py")
            print("2. 检查系统状态: python scripts/validation/check_system_status.py")
        
        return success
        
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
