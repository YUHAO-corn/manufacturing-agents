#!/usr/bin/env python3
"""
系统状态检查脚本
检查数据库配置和缓存系统状态
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def check_system_status():
    """检查系统状态"""
    print("🔍 TradingAgents 系统状态检查")
    print("=" * 50)
    
    # 检查配置文件
    print("\n📁 检查配置文件...")
    config_file = project_root / "config" / "database_config.json"
    if config_file.exists():
        print(f"✅ 配置文件存在: {config_file}")
        
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print("📊 配置内容:")
            print(f"  数据库启用: {config['database']['enabled']}")
            print(f"  自动检测: {config['database']['auto_detect']}")
            print(f"  MongoDB启用: {config['database']['mongodb']['enabled']}")
            print(f"  Redis启用: {config['database']['redis']['enabled']}")
            print(f"  主要缓存后端: {config['cache']['primary_backend']}")
            print(f"  降级支持: {config['cache']['fallback_enabled']}")
            
        except Exception as e:
            print(f"❌ 配置文件解析失败: {e}")
    else:
        print(f"❌ 配置文件不存在: {config_file}")
    
    # 检查数据库管理器
    print("\n🔧 检查数据库管理器...")
    try:
        from manufacturingagents.config.database_manager import get_database_manager
        
        db_manager = get_database_manager()
        status = db_manager.get_status_report()
        
        print("📊 数据库状态:")
        print(f"  数据库可用: {'✅ 是' if status['database_available'] else '❌ 否'}")
        print(f"  MongoDB: {'✅ 可用' if status['mongodb']['available'] else '❌ 不可用'}")
        print(f"  Redis: {'✅ 可用' if status['redis']['available'] else '❌ 不可用'}")
        print(f"  缓存后端: {status['cache_backend']}")
        print(f"  降级支持: {'✅ 启用' if status['fallback_enabled'] else '❌ 禁用'}")
        
    except Exception as e:
        print(f"❌ 数据库管理器检查失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 检查缓存系统
    print("\n💾 检查缓存系统...")
    try:
        from manufacturingagents.dataflows.integrated_cache import get_cache
        
        cache = get_cache()
        backend_info = cache.get_cache_backend_info()
        
        print("📊 缓存系统状态:")
        print(f"  缓存系统: {backend_info['system']}")
        print(f"  主要后端: {backend_info['primary_backend']}")
        print(f"  降级支持: {'✅ 启用' if backend_info['fallback_enabled'] else '❌ 禁用'}")
        print(f"  性能模式: {cache.get_performance_mode()}")
        
        # 获取详细统计
        stats = cache.get_cache_stats()
        if 'adaptive_cache' in stats:
            adaptive_stats = stats['adaptive_cache']
            print(f"  文件缓存数量: {adaptive_stats.get('file_cache_count', 0)}")
            if 'redis_keys' in adaptive_stats:
                print(f"  Redis键数量: {adaptive_stats['redis_keys']}")
            if 'mongodb_cache_count' in adaptive_stats:
                print(f"  MongoDB缓存数量: {adaptive_stats['mongodb_cache_count']}")
        
    except Exception as e:
        print(f"❌ 缓存系统检查失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试缓存功能
    print("\n🧪 测试缓存功能...")
    try:
        from manufacturingagents.dataflows.integrated_cache import get_cache
        from datetime import datetime
        
        cache = get_cache()
        
        # 测试数据保存
        test_data = f"测试数据 - {datetime.now()}"
        cache_key = cache.save_stock_data(
            symbol="TEST",
            data=test_data,
            start_date="2024-01-01",
            end_date="2024-12-31",
            data_source="system_test"
        )
        print(f"✅ 数据保存成功: {cache_key}")
        
        # 测试数据加载
        loaded_data = cache.load_stock_data(cache_key)
        if loaded_data == test_data:
            print("✅ 数据加载成功，内容匹配")
        else:
            print("❌ 数据加载失败或内容不匹配")
        
        # 测试数据查找
        found_key = cache.find_cached_stock_data(
            symbol="TEST",
            start_date="2024-01-01",
            end_date="2024-12-31",
            data_source="system_test"
        )
        
        if found_key:
            print(f"✅ 缓存查找成功: {found_key}")
        else:
            print("❌ 缓存查找失败")
        
    except Exception as e:
        print(f"❌ 缓存功能测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 性能测试
    print("\n⚡ 简单性能测试...")
    try:
        import time
        from manufacturingagents.dataflows.integrated_cache import get_cache
        
        cache = get_cache()
        
        # 保存性能测试
        start_time = time.time()
        cache_key = cache.save_stock_data(
            symbol="PERF",
            data="性能测试数据",
            start_date="2024-01-01",
            end_date="2024-12-31",
            data_source="perf_test"
        )
        save_time = time.time() - start_time
        
        # 加载性能测试
        start_time = time.time()
        data = cache.load_stock_data(cache_key)
        load_time = time.time() - start_time
        
        print(f"📊 性能测试结果:")
        print(f"  保存时间: {save_time:.4f}秒")
        print(f"  加载时间: {load_time:.4f}秒")
        
        if load_time < 0.1:
            print("✅ 缓存性能良好 (<0.1秒)")
        else:
            print("⚠️ 缓存性能需要优化")
        
        # 计算性能改进
        api_simulation_time = 2.0  # 假设API调用需要2秒
        if load_time < api_simulation_time:
            improvement = ((api_simulation_time - load_time) / api_simulation_time) * 100
            print(f"🚀 相比API调用性能提升: {improvement:.1f}%")
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
    
    # 系统建议
    print("\n💡 系统建议:")
    try:
        from manufacturingagents.dataflows.integrated_cache import get_cache
        
        cache = get_cache()
        
        if cache.is_database_available():
            print("✅ 数据库可用，系统运行在最佳性能模式")
        else:
            print("ℹ️ 数据库不可用，系统使用文件缓存模式")
            print("💡 建议:")
            print("  1. 安装MongoDB和Redis以获得更好的性能")
            print("  2. 运行: pip install pymongo redis")
            print("  3. 启动数据库服务:")
            print("     - MongoDB: docker run -d -p 27017:27017 mongo:4.4")
            print("     - Redis: docker run -d -p 6379:6379 redis:alpine")
        
        performance_mode = cache.get_performance_mode()
        print(f"🎯 当前性能模式: {performance_mode}")
        
    except Exception as e:
        print(f"⚠️ 无法生成系统建议: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 系统状态检查完成!")

def main():
    """主函数"""
    try:
        check_system_status()
        return True
    except Exception as e:
        print(f"❌ 系统检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
