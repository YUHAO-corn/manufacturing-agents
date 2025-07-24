#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试当前601127股票名称显示状态
验证修复是否生效，以及是否存在缓存问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_stock_name_mapping():
    """测试股票名称映射字典"""
    print("\n=== 测试1: 检查_common_stock_names映射 ===")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import _common_stock_names
        
        print(f"📋 _common_stock_names字典中的601127映射:")
        if '601127' in _common_stock_names:
            print(f"   ✅ 601127 -> {_common_stock_names['601127']}")
            return True
        else:
            print(f"   ❌ 601127不在_common_stock_names字典中")
            print(f"   📋 字典中的上海股票:")
            for code, name in _common_stock_names.items():
                if code.startswith('60'):
                    print(f"      {code} -> {name}")
            return False
            
    except Exception as e:
        print(f"   ❌ 导入_common_stock_names失败: {e}")
        return False

def test_get_stock_name_method():
    """测试_get_stock_name方法"""
    print("\n=== 测试2: 测试_get_stock_name方法 ===")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider
        
        provider = TongDaXinDataProvider()
        
        # 直接测试_get_stock_name方法（不需要连接API）
        name = provider._get_stock_name('601127')
        print(f"   📊 _get_stock_name('601127') 返回: {name}")
        
        if name == '小康股份':
            print(f"   ✅ 股票名称正确")
            return True
        else:
            print(f"   ❌ 股票名称错误，期望'小康股份'，实际'{name}'")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试_get_stock_name方法失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_status():
    """测试缓存状态"""
    print("\n=== 测试3: 检查缓存状态 ===")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import _stock_name_cache
        
        print(f"   📋 当前_stock_name_cache内容:")
        if _stock_name_cache:
            for code, name in _stock_name_cache.items():
                print(f"      {code} -> {name}")
        else:
            print(f"      缓存为空")
            
        # 检查601127是否在缓存中
        if '601127' in _stock_name_cache:
            cached_name = _stock_name_cache['601127']
            print(f"   📊 601127在缓存中: {cached_name}")
            if cached_name == '小康股份':
                print(f"   ✅ 缓存中的名称正确")
                return True
            else:
                print(f"   ❌ 缓存中的名称错误，需要清除缓存")
                return False
        else:
            print(f"   📊 601127不在缓存中")
            return True
            
    except Exception as e:
        print(f"   ❌ 检查缓存状态失败: {e}")
        return False

def test_get_china_stock_data():
    """测试get_china_stock_data函数"""
    print("\n=== 测试4: 测试get_china_stock_data函数 ===")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import get_china_stock_data
        from datetime import datetime, timedelta
        
        # 获取最近几天的数据
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        print(f"   📊 调用get_china_stock_data('601127', '{start_date}', '{end_date}')")
        result = get_china_stock_data('601127', start_date, end_date)
        
        # 检查结果中的股票名称
        if '小康股份' in result:
            print(f"   ✅ 结果中包含正确的股票名称'小康股份'")
            return True
        elif '股票601127' in result:
            print(f"   ❌ 结果中显示错误的股票名称'股票601127'")
            print(f"   💡 这可能是缓存问题")
            return False
        else:
            print(f"   ⚠️ 结果中未找到明确的股票名称")
            print(f"   📋 结果前200字符: {result[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试get_china_stock_data失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def clear_stock_name_cache():
    """清除股票名称缓存"""
    print("\n=== 清除股票名称缓存 ===")
    
    try:
        from manufacturingagents.dataflows import tdx_utils
        
        # 清除全局缓存
        tdx_utils._stock_name_cache.clear()
        print(f"   ✅ 已清除_stock_name_cache")
        
        # 如果有数据库缓存，也尝试清除
        try:
            from manufacturingagents.dataflows.database_manager import get_database_manager
            db_manager = get_database_manager()
            if db_manager.redis_client:
                # 清除Redis中的股票相关缓存
                keys = db_manager.redis_client.keys('*601127*')
                if keys:
                    db_manager.redis_client.delete(*keys)
                    print(f"   ✅ 已清除Redis中的601127相关缓存 ({len(keys)}个键)")
                else:
                    print(f"   📊 Redis中没有601127相关缓存")
        except Exception as e:
            print(f"   ⚠️ 清除Redis缓存失败: {e}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ 清除缓存失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔍 检查601127股票名称当前状态")
    print("=" * 60)
    
    test_results = []
    
    # 执行测试
    test_results.append(("股票名称映射字典", test_stock_name_mapping()))
    test_results.append(("_get_stock_name方法", test_get_stock_name_method()))
    test_results.append(("缓存状态检查", test_cache_status()))
    test_results.append(("get_china_stock_data函数", test_get_china_stock_data()))
    
    # 如果发现问题，尝试清除缓存
    if not all(result for _, result in test_results):
        print("\n⚠️ 发现问题，尝试清除缓存...")
        clear_stock_name_cache()
        
        # 重新测试关键功能
        print("\n🔄 清除缓存后重新测试...")
        test_results.append(("清除缓存后_get_stock_name", test_get_stock_name_method()))
    
    # 测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！601127股票名称应该正确显示为'小康股份'")
    else:
        print("\n⚠️ 存在问题，需要进一步调查")
        print("\n💡 建议:")
        print("   1. 重启应用程序以重新加载模块")
        print("   2. 检查是否有其他缓存层")
        print("   3. 确认tdx_utils.py文件是否正确保存")

if __name__ == '__main__':
    main()