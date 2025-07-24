#!/usr/bin/env python3
"""
全面清理所有缓存数据
包括：Redis缓存、文件缓存、MongoDB缓存、Python缓存
"""

import os
import sys
import shutil
from pathlib import Path

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def clear_redis_cache():
    """清理Redis缓存"""
    print("\n🧹 清理Redis缓存...")
    try:
        from manufacturingagents.dataflows.database_manager import get_database_manager
        
        db_manager = get_database_manager()
        
        if not db_manager.redis_client:
            print("❌ Redis未连接")
            return False
        
        # 获取所有键
        all_keys = db_manager.redis_client.keys('*')
        if all_keys:
            deleted = db_manager.redis_client.delete(*all_keys)
            print(f"✅ 清理Redis缓存: {deleted}个键")
        else:
            print("✅ Redis缓存已为空")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis缓存清理失败: {e}")
        return False

def clear_file_cache():
    """清理文件缓存"""
    print("\n🧹 清理文件缓存...")
    
    cache_dirs = [
        Path(project_root) / "tradingagents" / "dataflows" / "data_cache",
        Path(project_root) / "dataflows" / "data_cache",
        Path(project_root) / "data" / "cache",
        Path(project_root) / "cache",
        Path(project_root) / "finnhub_data",
        Path(project_root) / "data" / "finnhub_data"
    ]
    
    total_cleared = 0
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            try:
                # 清理缓存文件
                cache_files = list(cache_dir.rglob("*.txt")) + \
                             list(cache_dir.rglob("*.json")) + \
                             list(cache_dir.rglob("*.cache")) + \
                             list(cache_dir.rglob("*.pkl"))
                
                for cache_file in cache_files:
                    try:
                        cache_file.unlink()
                        total_cleared += 1
                    except Exception as e:
                        print(f"⚠️ 无法删除文件 {cache_file}: {e}")
                
                print(f"✅ 清理目录 {cache_dir.name}: {len(cache_files)}个文件")
                
            except Exception as e:
                print(f"❌ 清理目录 {cache_dir} 失败: {e}")
    
    print(f"✅ 总共清理文件缓存: {total_cleared}个文件")
    return total_cleared > 0

def clear_mongodb_cache():
    """清理MongoDB缓存"""
    print("\n🧹 清理MongoDB缓存...")
    try:
        from manufacturingagents.dataflows.database_manager import get_database_manager
        
        db_manager = get_database_manager()
        
        if not db_manager.mongodb_db:
            print("❌ MongoDB未连接")
            return False
        
        # 清理各个集合
        collections_to_clear = [
            'stock_data',
            'news_data', 
            'fundamentals_data',
            'analysis_results'
        ]
        
        total_cleared = 0
        
        for collection_name in collections_to_clear:
            try:
                collection = db_manager.mongodb_db[collection_name]
                count = collection.count_documents({})
                if count > 0:
                    result = collection.delete_many({})
                    print(f"✅ 清理集合 {collection_name}: {result.deleted_count}条记录")
                    total_cleared += result.deleted_count
                else:
                    print(f"✅ 集合 {collection_name} 已为空")
            except Exception as e:
                print(f"⚠️ 清理集合 {collection_name} 失败: {e}")
        
        print(f"✅ 总共清理MongoDB: {total_cleared}条记录")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB缓存清理失败: {e}")
        return False

def clear_python_cache():
    """清理Python缓存"""
    print("\n🧹 清理Python缓存...")
    
    # 查找所有__pycache__目录
    cache_dirs = list(Path(project_root).rglob("__pycache__"))
    pyc_files = list(Path(project_root).rglob("*.pyc"))
    pyo_files = list(Path(project_root).rglob("*.pyo"))
    
    total_cleared = 0
    
    # 清理__pycache__目录
    if cache_dirs:
        print(f"🔍 找到 {len(cache_dirs)} 个__pycache__目录")
        for cache_dir in cache_dirs:
            try:
                shutil.rmtree(cache_dir)
                total_cleared += 1
                print(f"  ✅ 已清理: {cache_dir.relative_to(Path(project_root))}")
            except Exception as e:
                print(f"  ❌ 清理失败 {cache_dir}: {e}")
    
    # 清理.pyc文件
    if pyc_files:
        print(f"🔍 找到 {len(pyc_files)} 个.pyc文件")
        for pyc_file in pyc_files:
            try:
                pyc_file.unlink()
                total_cleared += 1
            except Exception as e:
                print(f"  ❌ 清理失败 {pyc_file}: {e}")
    
    # 清理.pyo文件
    if pyo_files:
        print(f"🔍 找到 {len(pyo_files)} 个.pyo文件")
        for pyo_file in pyo_files:
            try:
                pyo_file.unlink()
                total_cleared += 1
            except Exception as e:
                print(f"  ❌ 清理失败 {pyo_file}: {e}")
    
    print(f"✅ 总共清理Python缓存: {total_cleared}个项目")
    return total_cleared > 0

def clear_streamlit_cache():
    """清理Streamlit缓存"""
    print("\n🧹 清理Streamlit缓存...")
    
    streamlit_cache_dirs = [
        Path.home() / ".streamlit",
        Path(project_root) / ".streamlit"
    ]
    
    total_cleared = 0
    
    for cache_dir in streamlit_cache_dirs:
        if cache_dir.exists():
            try:
                # 查找缓存文件
                cache_files = list(cache_dir.rglob("*.cache")) + \
                             list(cache_dir.rglob("*.pkl")) + \
                             list(cache_dir.rglob("*.json"))
                
                for cache_file in cache_files:
                    try:
                        cache_file.unlink()
                        total_cleared += 1
                    except Exception as e:
                        print(f"⚠️ 无法删除Streamlit缓存文件 {cache_file}: {e}")
                
                if cache_files:
                    print(f"✅ 清理Streamlit目录 {cache_dir}: {len(cache_files)}个文件")
                
            except Exception as e:
                print(f"❌ 清理Streamlit目录 {cache_dir} 失败: {e}")
    
    print(f"✅ 总共清理Streamlit缓存: {total_cleared}个文件")
    return total_cleared > 0

def main():
    """主函数 - 执行全面缓存清理"""
    print("🚀 开始全面清理所有缓存...")
    print("=" * 50)
    
    results = {
        'redis': False,
        'file_cache': False,
        'mongodb': False,
        'python_cache': False,
        'streamlit_cache': False
    }
    
    # 1. 清理Redis缓存
    results['redis'] = clear_redis_cache()
    
    # 2. 清理文件缓存
    results['file_cache'] = clear_file_cache()
    
    # 3. 清理MongoDB缓存
    results['mongodb'] = clear_mongodb_cache()
    
    # 4. 清理Python缓存
    results['python_cache'] = clear_python_cache()
    
    # 5. 清理Streamlit缓存
    results['streamlit_cache'] = clear_streamlit_cache()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 缓存清理总结:")
    print("=" * 50)
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    for cache_type, success in results.items():
        status = "✅ 成功" if success else "❌ 失败/跳过"
        cache_name = {
            'redis': 'Redis缓存',
            'file_cache': '文件缓存',
            'mongodb': 'MongoDB缓存',
            'python_cache': 'Python缓存',
            'streamlit_cache': 'Streamlit缓存'
        }[cache_type]
        print(f"{cache_name}: {status}")
    
    print(f"\n🎯 清理完成: {success_count}/{total_count} 项成功")
    
    if success_count == total_count:
        print("🎉 所有缓存清理完成！")
    elif success_count > 0:
        print("⚠️ 部分缓存清理完成，请检查失败项目")
    else:
        print("❌ 缓存清理失败，请检查系统配置")
    
    print("\n💡 建议：")
    print("- 重启Web应用以确保缓存完全清除")
    print("- 下次查询股票数据时将重新从API获取")
    print("- 如有问题，请检查数据库连接配置")

if __name__ == "__main__":
    main()