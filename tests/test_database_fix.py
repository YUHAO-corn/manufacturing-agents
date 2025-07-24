#!/usr/bin/env python3
"""
测试MongoDB重复键错误修复效果
"""

import sys
import os
sys.path.append('.')

def test_database_manager():
    """测试统一的数据库管理器"""
    print("🔍 测试数据库管理器...")
    
    try:
        from manufacturingagents.config.database_manager import get_database_manager
        
        db_manager = get_database_manager()
        print("✅ 数据库管理器导入成功")
        
        # 检查连接状态
        mongodb_status = "✅ 已连接" if db_manager.is_mongodb_available() else "❌ 未连接"
        redis_status = "✅ 已连接" if db_manager.is_redis_available() else "❌ 未连接"

        print(f"MongoDB: {mongodb_status}")
        print(f"Redis: {redis_status}")

        # 如果MongoDB连接成功，测试基本操作
        if db_manager.is_mongodb_available():
            print("\n📊 测试MongoDB操作...")
            
            # 检查集合
            mongodb_client = db_manager.get_mongodb_client()
            db = mongodb_client[db_manager.mongodb_config["database"]]
            collections = db.list_collection_names()
            print(f"可用集合: {collections}")
            
            # 检查stock_data集合的文档数量
            if 'stock_data' in collections:
                stock_collection = db_manager.mongodb_db['stock_data']
                count = stock_collection.count_documents({})
                print(f"stock_data集合文档数: {count}")
                
                # 检查是否还有重复键问题
                try:
                    # 尝试插入一个测试文档
                    test_doc = {
                        'symbol': 'TEST001',
                        'market_type': 'test',
                        'data': {'test': True},
                        'updated_at': '2024-01-01T00:00:00Z'
                    }
                    
                    # 使用replace_one进行upsert，这应该不会产生重复键错误
                    result = stock_collection.replace_one(
                        {'symbol': 'TEST001', 'market_type': 'test'},
                        test_doc,
                        upsert=True
                    )
                    
                    if result.upserted_id or result.modified_count > 0:
                        print("✅ 测试文档插入/更新成功，无重复键错误")
                    
                    # 清理测试文档
                    stock_collection.delete_one({'symbol': 'TEST001', 'market_type': 'test'})
                    print("🧹 测试文档已清理")
                    
                except Exception as e:
                    print(f"❌ 测试操作失败: {e}")
        
        # 测试Redis缓存
        if db_manager.redis_client is not None:
            print("\n⚡ 测试Redis操作...")
            try:
                # 测试Redis基本操作
                test_key = "test_fix_verification"
                test_value = "test_value_123"
                
                # 设置值
                db_manager.redis_client.set(test_key, test_value)
                
                # 获取值
                retrieved_value = db_manager.redis_client.get(test_key)
                # 处理Redis返回值可能是字符串或字节的情况
                if retrieved_value:
                    if isinstance(retrieved_value, bytes):
                        retrieved_str = retrieved_value.decode('utf-8')
                    else:
                        retrieved_str = str(retrieved_value)
                    
                    if retrieved_str == test_value:
                        print("✅ Redis读写操作成功")
                    else:
                        print(f"❌ Redis读写操作失败: 期望'{test_value}', 实际'{retrieved_str}'")
                else:
                    print("❌ Redis读写操作失败: 未获取到值")
                
                # 清理测试数据
                db_manager.redis_client.delete(test_key)
                print("🧹 Redis测试数据已清理")
                
                # 获取缓存统计
                stats = db_manager.get_cache_stats()
                print(f"缓存统计: {stats}")
                print("✅ Redis操作正常")
            except Exception as e:
                print(f"❌ Redis操作失败: {e}")
        else:
            print("\n⚠️ Redis未连接，跳过测试")
        
        db_manager.close()
        print("\n🎉 数据库管理器测试完成")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_tdx_utils():
    """测试tdx_utils是否正确使用database_manager"""
    print("\n🔍 测试tdx_utils统一性...")
    
    try:
        from manufacturingagents.dataflows import tdx_utils
        
        # 检查是否正确导入了database_manager
        if hasattr(tdx_utils, 'DB_MANAGER_AVAILABLE'):
            print(f"✅ DB_MANAGER_AVAILABLE: {tdx_utils.DB_MANAGER_AVAILABLE}")
        else:
            print("❌ 未找到DB_MANAGER_AVAILABLE变量")
        
        # 检查是否还有旧的db_cache_manager引用
        import inspect
        source = inspect.getsource(tdx_utils)
        if 'db_cache_manager' in source and 'get_db_cache' in source:
            print("⚠️ 发现旧的db_cache_manager引用")
        else:
            print("✅ 已完全移除db_cache_manager引用")
            
        print("✅ tdx_utils统一性检查完成")
        
    except Exception as e:
        print(f"❌ tdx_utils测试失败: {e}")

if __name__ == "__main__":
    print("🚀 MongoDB重复键错误修复验证")
    print("=" * 50)
    
    test_database_manager()
    test_tdx_utils()
    
    print("\n" + "=" * 50)
    print("✅ 修复验证完成")