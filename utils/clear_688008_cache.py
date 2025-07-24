#!/usr/bin/env python3
"""
清除688008股票的Redis缓存数据
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def clear_688008_cache():
    """清除688008股票的所有缓存数据"""
    try:
        from manufacturingagents.dataflows.database_manager import get_database_manager
        
        print("🧹 开始清除688008股票的Redis缓存...")
        
        db_manager = get_database_manager()
        
        if not db_manager.redis_client:
            print("❌ Redis未连接")
            return False
        
        # 清除股票相关的缓存模式
        patterns_to_clear = [
            "stock:688008:*",  # 股票数据缓存
            "*688008*",        # 包含688008的所有缓存
        ]
        
        total_deleted = 0
        for pattern in patterns_to_clear:
            deleted = db_manager.cache_clear_pattern(pattern)
            total_deleted += deleted
            print(f"🗑️ 清除模式 '{pattern}': {deleted}个键")
        
        print(f"✅ 总共清除了 {total_deleted} 个缓存键")
        
        # 显示剩余的相关键（用于验证）
        redis_config = db_manager.config.get('database', {}).get('redis', {})
        cache_config = redis_config.get('cache', {})
        key_prefix = cache_config.get('key_prefix', '')
        
        remaining_keys = db_manager.redis_client.keys(f"{key_prefix}*688008*")
        if remaining_keys:
            print(f"⚠️ 仍有 {len(remaining_keys)} 个相关键存在:")
            for key in remaining_keys[:10]:  # 只显示前10个
                print(f"  - {key}")
        else:
            print("✅ 所有688008相关的缓存已清除")
        
        return True
        
    except Exception as e:
        print(f"❌ 清除缓存失败: {e}")
        return False

if __name__ == "__main__":
    clear_688008_cache()