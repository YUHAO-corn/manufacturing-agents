#!/usr/bin/env python3
"""
Streamlit文件监控错误修复脚本

这个脚本用于修复Streamlit应用中的文件监控错误：
FileNotFoundError: [WinError 2] 系统找不到指定的文件。: '__pycache__\\*.pyc.*'

使用方法:
python scripts/fix_streamlit_watcher.py
"""

import os
import sys
import shutil
from pathlib import Path

def clean_pycache_files():
    """清理所有__pycache__目录和.pyc文件"""
    
    project_root = Path(__file__).parent.parent
    print(f"🔍 扫描项目目录: {project_root}")
    
    # 查找所有__pycache__目录
    cache_dirs = list(project_root.rglob("__pycache__"))
    pyc_files = list(project_root.rglob("*.pyc"))
    pyo_files = list(project_root.rglob("*.pyo"))
    
    total_cleaned = 0
    
    # 清理__pycache__目录
    if cache_dirs:
        print(f"\n🧹 发现 {len(cache_dirs)} 个__pycache__目录")
        for cache_dir in cache_dirs:
            try:
                shutil.rmtree(cache_dir)
                print(f"  ✅ 已删除: {cache_dir.relative_to(project_root)}")
                total_cleaned += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {cache_dir.relative_to(project_root)} - {e}")
    
    # 清理单独的.pyc文件
    if pyc_files:
        print(f"\n🧹 发现 {len(pyc_files)} 个.pyc文件")
        for pyc_file in pyc_files:
            try:
                pyc_file.unlink()
                print(f"  ✅ 已删除: {pyc_file.relative_to(project_root)}")
                total_cleaned += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {pyc_file.relative_to(project_root)} - {e}")
    
    # 清理.pyo文件
    if pyo_files:
        print(f"\n🧹 发现 {len(pyo_files)} 个.pyo文件")
        for pyo_file in pyo_files:
            try:
                pyo_file.unlink()
                print(f"  ✅ 已删除: {pyo_file.relative_to(project_root)}")
                total_cleaned += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {pyo_file.relative_to(project_root)} - {e}")
    
    if total_cleaned == 0:
        print("\n✅ 没有发现需要清理的缓存文件")
    else:
        print(f"\n✅ 总共清理了 {total_cleaned} 个文件/目录")

def check_streamlit_config():
    """检查Streamlit配置文件"""
    
    project_root = Path(__file__).parent.parent
    config_file = project_root / ".streamlit" / "config.toml"
    
    print(f"\n🔍 检查Streamlit配置文件: {config_file}")
    
    if config_file.exists():
        print("  ✅ 配置文件存在")
        
        # 检查配置内容
        try:
            content = config_file.read_text(encoding='utf-8')
            if "excludePatterns" in content and "__pycache__" in content:
                print("  ✅ 配置文件包含__pycache__排除规则")
            else:
                print("  ⚠️ 配置文件可能缺少__pycache__排除规则")
        except Exception as e:
            print(f"  ❌ 读取配置文件失败: {e}")
    else:
        print("  ❌ 配置文件不存在")
        print("  💡 建议运行: python web/run_web.py 来创建配置文件")

def set_environment_variables():
    """设置环境变量禁用字节码生成"""
    
    print("\n🔧 设置环境变量...")
    
    # 设置当前会话的环境变量
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    print("  ✅ 已设置 PYTHONDONTWRITEBYTECODE=1")
    
    # 检查.env文件
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        content = env_file.read_text(encoding='utf-8')
        if 'PYTHONDONTWRITEBYTECODE' not in content:
            print("  💡 建议在.env文件中添加: PYTHONDONTWRITEBYTECODE=1")
        else:
            print("  ✅ .env文件已包含PYTHONDONTWRITEBYTECODE设置")
    else:
        print("  💡 建议创建.env文件并添加: PYTHONDONTWRITEBYTECODE=1")

def main():
    """主函数"""
    
    print("🔧 Streamlit文件监控错误修复工具")
    print("=" * 50)
    
    print("\n📋 此工具将执行以下操作:")
    print("  1. 清理所有Python缓存文件(__pycache__, *.pyc, *.pyo)")
    print("  2. 检查Streamlit配置文件")
    print("  3. 设置环境变量禁用字节码生成")
    
    response = input("\n是否继续? (y/n): ").lower().strip()
    if response != 'y':
        print("❌ 操作已取消")
        return
    
    try:
        # 步骤1: 清理缓存文件
        print("\n" + "=" * 30)
        print("步骤1: 清理Python缓存文件")
        print("=" * 30)
        clean_pycache_files()
        
        # 步骤2: 检查配置文件
        print("\n" + "=" * 30)
        print("步骤2: 检查Streamlit配置")
        print("=" * 30)
        check_streamlit_config()
        
        # 步骤3: 设置环境变量
        print("\n" + "=" * 30)
        print("步骤3: 设置环境变量")
        print("=" * 30)
        set_environment_variables()
        
        print("\n" + "=" * 50)
        print("🎉 修复完成!")
        print("\n📝 建议:")
        print("  1. 重启Streamlit应用")
        print("  2. 如果问题仍然存在，请查看文档:")
        print("     docs/troubleshooting/streamlit-file-watcher-fix.md")
        print("  3. 考虑使用虚拟环境隔离Python包")
        
    except Exception as e:
        print(f"\n❌ 修复过程中出现错误: {e}")
        print("请手动执行以下操作:")
        print("  1. 删除所有__pycache__目录")
        print("  2. 检查.streamlit/config.toml配置文件")
        print("  3. 设置环境变量 PYTHONDONTWRITEBYTECODE=1")

if __name__ == "__main__":
    main()