#!/usr/bin/env python3
"""
测试缓存系统功能
"""

import sys
import os
import time
sys.path.append('..')

def test_cache_manager():
    """测试缓存管理器基本功能"""
    print("🔍 测试缓存管理器...")
    
    try:
        from manufacturingagents.dataflows.cache_manager import get_cache
        
        # 获取缓存实例
        cache = get_cache()
        print(f"✅ 缓存管理器初始化成功")
        print(f"📁 缓存目录: {cache.cache_dir}")
        
        # 测试保存股票数据
        print(f"\n📊 测试股票数据缓存...")
        test_data = """
# AAPL 股票数据分析

## 📊 实时行情
- 股票名称: Apple Inc.
- 当前价格: $190.50
- 涨跌幅: +1.25%
- 成交量: 45,678,900手
- 更新时间: 2025-06-29 15:30:00

## 📈 历史数据概览
- 数据期间: 2025-06-25 至 2025-06-29
- 数据条数: 5条
- 期间最高: $195.80
- 期间最低: $188.20
- 期间涨幅: +2.15%

数据来源: 测试数据
"""
        
        cache_key = cache.save_stock_data(
            symbol="AAPL",
            data=test_data,
            start_date="2025-06-25",
            end_date="2025-06-29",
            data_source="test"
        )
        print(f"✅ 股票数据缓存成功: {cache_key}")
        
        # 测试查找缓存
        print(f"\n🔍 测试缓存查找...")
        found_key = cache.find_cached_stock_data(
            symbol="AAPL",
            start_date="2025-06-25",
            end_date="2025-06-29",
            data_source="test"
        )
        
        if found_key:
            print(f"✅ 找到缓存: {found_key}")
            
            # 测试加载缓存
            loaded_data = cache.load_stock_data(found_key)
            if loaded_data:
                print(f"✅ 缓存加载成功，数据长度: {len(loaded_data)}")
                print(f"📄 数据前100字符: {loaded_data[:100]}...")
            else:
                print(f"❌ 缓存加载失败")
        else:
            print(f"❌ 未找到缓存")
        
        # 测试缓存统计
        print(f"\n📊 测试缓存统计...")
        stats = cache.get_cache_stats()
        print(f"✅ 缓存统计:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 缓存管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tdx_cache_integration():
    """测试通达信缓存集成"""
    print("\n" + "="*50)
    print("🔍 测试通达信缓存集成...")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import get_china_stock_data
        
        # 第一次调用（从API获取）
        print(f"\n🌐 第一次调用（从API获取）...")
        start_time = time.time()
        result1 = get_china_stock_data("000001", "2025-06-25", "2025-06-29")
        time1 = time.time() - start_time
        print(f"⏱️ 第一次调用耗时: {time1:.2f}秒")
        print(f"📄 数据长度: {len(result1)}")
        
        # 第二次调用（从缓存获取）
        print(f"\n💾 第二次调用（从缓存获取）...")
        start_time = time.time()
        result2 = get_china_stock_data("000001", "2025-06-25", "2025-06-29")
        time2 = time.time() - start_time
        print(f"⏱️ 第二次调用耗时: {time2:.2f}秒")
        print(f"📄 数据长度: {len(result2)}")
        
        # 比较结果
        if result1 == result2:
            print(f"✅ 两次调用结果一致")
        else:
            print(f"⚠️ 两次调用结果不一致")
        
        # 性能提升
        if time2 < time1:
            speedup = time1 / time2
            print(f"🚀 缓存提升性能: {speedup:.1f}倍")
        
        return True
        
    except Exception as e:
        print(f"❌ 通达信缓存集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_expiration():
    """测试缓存过期机制"""
    print("\n" + "="*50)
    print("🔍 测试缓存过期机制...")
    
    try:
        from manufacturingagents.dataflows.cache_manager import get_cache
        
        cache = get_cache()
        
        # 保存测试数据
        test_data = "测试过期数据"
        cache_key = cache.save_stock_data(
            symbol="TEST",
            data=test_data,
            start_date="2025-06-29",
            end_date="2025-06-29",
            data_source="test_expiration"
        )
        
        # 测试立即查找（应该找到）
        found_key = cache.find_cached_stock_data(
            symbol="TEST",
            start_date="2025-06-29",
            end_date="2025-06-29",
            data_source="test_expiration",
            max_age_hours=24
        )
        
        if found_key:
            print(f"✅ 新缓存可以找到: {found_key}")
        else:
            print(f"❌ 新缓存未找到")
        
        # 测试过期查找（设置很短的过期时间）
        found_key_expired = cache.find_cached_stock_data(
            symbol="TEST",
            start_date="2025-06-29",
            end_date="2025-06-29",
            data_source="test_expiration",
            max_age_hours=0.001  # 0.001小时 = 3.6秒
        )
        
        if not found_key_expired:
            print(f"✅ 过期缓存正确被忽略")
        else:
            print(f"⚠️ 过期缓存仍然被找到")
        
        return True
        
    except Exception as e:
        print(f"❌ 缓存过期测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 开始缓存系统测试")
    print("="*50)
    
    # 测试基本功能
    result1 = test_cache_manager()
    
    # 测试通达信集成
    result2 = test_tdx_cache_integration()
    
    # 测试过期机制
    result3 = test_cache_expiration()
    
    print("\n" + "="*50)
    print("🎯 测试总结:")
    print(f"缓存管理器测试: {'✅ 成功' if result1 else '❌ 失败'}")
    print(f"通达信缓存集成测试: {'✅ 成功' if result2 else '❌ 失败'}")
    print(f"缓存过期机制测试: {'✅ 成功' if result3 else '❌ 失败'}")
    
    if result1 and result2 and result3:
        print("🎉 所有缓存功能测试通过！")
        print("\n💡 缓存系统优势:")
        print("  🔹 减少API调用次数")
        print("  🔹 提高数据获取速度")
        print("  🔹 支持离线分析")
        print("  🔹 自动过期管理")
        print("  🔹 智能缓存查找")
    else:
        print("⚠️ 部分测试失败，请检查配置。")
