#!/usr/bin/env python3
"""
验证docs/contribution目录的Git忽略配置
"""

import os
import subprocess
import sys
from pathlib import Path

def run_git_command(cmd, cwd=None):
    """运行Git命令"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    """主函数"""
    print("🔧 验证docs/contribution目录的Git配置")
    print("=" * 40)
    
    # 设置项目路径
    project_path = Path("C:/code/TradingAgentsCN")
    contribution_path = project_path / "docs" / "contribution"
    gitignore_path = project_path / ".gitignore"
    
    # 检查目录是否存在
    print("📁 检查目录状态...")
    if contribution_path.exists():
        file_count = len(list(contribution_path.rglob("*")))
        print(f"✅ docs/contribution 目录存在，包含 {file_count} 个项目")
    else:
        print("❌ docs/contribution 目录不存在")
        return False
    
    # 检查.gitignore配置
    print("\n📝 检查.gitignore配置...")
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        if "docs/contribution/" in gitignore_content:
            print("✅ .gitignore 已包含 docs/contribution/")
        else:
            print("❌ .gitignore 未包含 docs/contribution/")
            return False
    else:
        print("❌ .gitignore 文件不存在")
        return False
    
    # 检查Git跟踪状态
    print("\n🔍 检查Git跟踪状态...")
    
    # 检查是否有contribution文件被跟踪
    success, output, error = run_git_command(
        "git ls-files docs/contribution/", 
        cwd=str(project_path)
    )
    
    if success:
        if output:
            tracked_files = output.split('\n')
            print(f"⚠️ 仍有 {len(tracked_files)} 个文件被Git跟踪:")
            for file in tracked_files[:5]:  # 只显示前5个
                print(f"  - {file}")
            if len(tracked_files) > 5:
                print(f"  ... 还有 {len(tracked_files) - 5} 个文件")
            
            print("\n🔧 需要从Git跟踪中移除这些文件:")
            print("git rm -r --cached docs/contribution/")
            return False
        else:
            print("✅ 没有contribution文件被Git跟踪")
    else:
        print(f"⚠️ 无法检查Git跟踪状态: {error}")
    
    # 测试.gitignore是否生效
    print("\n🧪 测试.gitignore是否生效...")
    
    test_file = contribution_path / "test_ignore.txt"
    try:
        # 创建测试文件
        with open(test_file, 'w') as f:
            f.write("测试文件")
        
        # 检查Git是否忽略了这个文件
        success, output, error = run_git_command(
            f"git check-ignore {test_file.relative_to(project_path)}", 
            cwd=str(project_path)
        )
        
        if success:
            print("✅ .gitignore 正常工作，测试文件被忽略")
        else:
            print("❌ .gitignore 可能未生效")
            return False
        
        # 删除测试文件
        test_file.unlink()
        
    except Exception as e:
        print(f"⚠️ 测试失败: {e}")
    
    # 检查当前Git状态
    print("\n📊 检查当前Git状态...")
    
    success, output, error = run_git_command(
        "git status --porcelain", 
        cwd=str(project_path)
    )
    
    if success:
        if output:
            # 检查是否有contribution相关的更改
            contribution_changes = [
                line for line in output.split('\n') 
                if 'contribution' in line
            ]
            
            if contribution_changes:
                print("⚠️ 发现contribution相关的更改:")
                for change in contribution_changes:
                    print(f"  {change}")
                print("\n建议操作:")
                print("1. git add .gitignore")
                print("2. git commit -m 'chore: exclude docs/contribution from version control'")
            else:
                print("✅ 没有contribution相关的未提交更改")
        else:
            print("✅ 工作目录干净")
    else:
        print(f"⚠️ 无法检查Git状态: {error}")
    
    print("\n🎯 总结:")
    print("✅ docs/contribution 目录已成功配置为不被Git管理")
    print("📁 本地文件保留，但不会被版本控制")
    print("🔒 新增的contribution文件将自动被忽略")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 配置验证成功！")
    else:
        print("\n❌ 配置需要调整")
    
    sys.exit(0 if success else 1)
