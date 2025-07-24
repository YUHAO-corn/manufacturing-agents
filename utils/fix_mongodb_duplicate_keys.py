#!/usr/bin/env python3
"""
MongoDB重复键错误修复脚本
解决database_manager和db_cache_manager之间的数据冲突问题
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def fix_mongodb_duplicate_keys():
    """修复MongoDB重复键错误"""
    print("🔧 开始修复MongoDB重复键错误...")
    
    try:
        # 导入必要的模块
        from pymongo import MongoClient
        from manufacturingagents.dataflows.database_manager import get_database_manager
        
        # 获取数据库管理器
        db_manager = get_database_manager()
        
        if db_manager.mongodb_db is None:
            print("❌ MongoDB未连接，请检查配置并启动MongoDB服务")
            return False
        
        # 使用现有的连接
        client = db_manager.mongodb_client
        db = db_manager.mongodb_db
        
        print(f"📊 使用现有MongoDB连接")
        
        # 测试连接
        client.admin.command('ping')
        print("✅ MongoDB连接成功")
        
        # 获取stock_data集合
        collection = db.stock_data
        
        # 步骤1: 查看当前数据状况
        print("\n📊 当前数据状况:")
        total_docs = collection.count_documents({})
        print(f"  总文档数: {total_docs}")
        
        # 查找重复的symbol+market_type组合
        pipeline = [
            {
                "$group": {
                    "_id": {"symbol": "$symbol", "market_type": "$market_type"},
                    "count": {"$sum": 1},
                    "docs": {"$push": "$_id"}
                }
            },
            {
                "$match": {"count": {"$gt": 1}}
            }
        ]
        
        duplicates = list(collection.aggregate(pipeline))
        print(f"  重复的symbol+market_type组合: {len(duplicates)}")
        
        if duplicates:
            print("\n🔍 发现的重复数据:")
            for dup in duplicates:
                symbol = dup['_id']['symbol']
                market_type = dup['_id']['market_type']
                count = dup['count']
                print(f"  - {symbol} ({market_type}): {count}条记录")
        
        # 步骤2: 备份现有数据
        print("\n💾 备份现有数据...")
        backup_collection = db.stock_data_backup
        
        # 清空备份集合
        backup_collection.drop()
        
        # 复制所有数据到备份集合
        if total_docs > 0:
            all_docs = list(collection.find({}))
            backup_collection.insert_many(all_docs)
            print(f"✅ 已备份 {len(all_docs)} 条记录到 stock_data_backup 集合")
        
        # 步骤3: 删除现有索引
        print("\n🗑️ 删除现有索引...")
        try:
            # 获取所有索引
            indexes = collection.list_indexes()
            index_names = [idx['name'] for idx in indexes if idx['name'] != '_id_']
            
            for index_name in index_names:
                collection.drop_index(index_name)
                print(f"  删除索引: {index_name}")
        except Exception as e:
            print(f"⚠️ 删除索引时出现错误: {e}")
        
        # 步骤4: 清理重复数据
        print("\n🧹 清理重复数据...")
        
        # 对于每个重复的symbol+market_type组合，只保留最新的一条记录
        removed_count = 0
        for dup in duplicates:
            symbol = dup['_id']['symbol']
            market_type = dup['_id']['market_type']
            doc_ids = dup['docs']
            
            # 找到这些文档，按updated_at排序，保留最新的
            docs = list(collection.find(
                {"_id": {"$in": doc_ids}}
            ).sort("updated_at", -1))
            
            if len(docs) > 1:
                # 保留第一个（最新的），删除其他的
                keep_doc = docs[0]
                remove_ids = [doc['_id'] for doc in docs[1:]]
                
                result = collection.delete_many({"_id": {"$in": remove_ids}})
                removed_count += result.deleted_count
                
                print(f"  清理 {symbol} ({market_type}): 保留1条，删除{len(remove_ids)}条")
        
        print(f"✅ 共删除 {removed_count} 条重复记录")
        
        # 步骤5: 重建索引
        print("\n🔨 重建索引...")
        
        # 创建新的索引策略，避免冲突
        try:
            # 为database_manager创建复合索引（非唯一）
            collection.create_index([("symbol", 1), ("market_type", 1)], background=True)
            print("  创建索引: (symbol, market_type) - 非唯一")
            
            # 创建时间索引
            collection.create_index([("created_at", -1)], background=True)
            print("  创建索引: created_at")
            
            collection.create_index([("updated_at", -1)], background=True)
            print("  创建索引: updated_at")
            
            # 为db_cache_manager创建数据源相关索引
            collection.create_index([
                ("symbol", 1),
                ("data_source", 1),
                ("start_date", 1),
                ("end_date", 1)
            ], background=True)
            print("  创建索引: (symbol, data_source, start_date, end_date)")
            
        except Exception as e:
            print(f"⚠️ 创建索引时出现错误: {e}")
        
        # 步骤6: 验证修复结果
        print("\n✅ 验证修复结果:")
        final_count = collection.count_documents({})
        print(f"  最终文档数: {final_count}")
        
        # 再次检查重复
        final_duplicates = list(collection.aggregate(pipeline))
        print(f"  剩余重复组合: {len(final_duplicates)}")
        
        if len(final_duplicates) == 0:
            print("🎉 重复键错误修复成功！")
        else:
            print("⚠️ 仍有重复数据，可能需要手动处理")
        
        # 步骤7: 更新mongo-init.js脚本
        print("\n📝 更新初始化脚本...")
        update_mongo_init_script()
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_mongo_init_script():
    """更新mongo-init.js脚本，移除唯一索引约束"""
    script_path = os.path.join(project_root, 'scripts', 'mongo-init.js')
    
    try:
        # 读取现有脚本
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换唯一索引为普通索引
        old_line = 'db.stock_data.createIndex({ "symbol": 1, "market_type": 1 }, { unique: true });'
        new_line = 'db.stock_data.createIndex({ "symbol": 1, "market_type": 1 });'
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # 写回文件
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新 {script_path}，移除唯一索引约束")
        else:
            print("⚠️ 未找到需要更新的索引定义")
            
    except Exception as e:
        print(f"⚠️ 更新初始化脚本失败: {e}")

def create_unified_database_manager():
    """创建统一的数据库管理器建议"""
    print("\n💡 统一数据库管理器建议:")
    print("")
    print("为了避免将来的冲突，建议:")
    print("1. 统一使用 database_manager.py 进行所有MongoDB操作")
    print("2. 在 tdx_utils.py 中修改为使用 database_manager 而不是 db_cache_manager")
    print("3. 或者修改 db_cache_manager 使用与 database_manager 兼容的文档结构")
    print("")
    print("具体修改建议:")
    print("- 在 tdx_utils.py 的 get_china_stock_data 函数中")
    print("- 将 db_cache_manager.save_stock_data 改为 database_manager.save_stock_data")
    print("- 这样可以确保所有股票数据使用统一的存储格式")

if __name__ == "__main__":
    print("🚀 MongoDB重复键错误修复工具")
    print("=" * 50)
    
    # 执行修复
    success = fix_mongodb_duplicate_keys()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 修复完成！")
        
        # 提供统一管理器建议
        create_unified_database_manager()
        
        print("\n建议重启应用程序以确保更改生效。")
    else:
        print("\n" + "=" * 50)
        print("❌ 修复失败，请检查错误信息并手动处理。")