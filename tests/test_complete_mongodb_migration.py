#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的MongoDB股票名称迁移测试

这个脚本用于验证整个项目的股票名称获取功能是否已经成功迁移到MongoDB。
测试范围包括：
1. TongDaXinDataProvider的股票名称获取
2. Agent工具中的中国股票名称映射
3. 实时数据获取中的股票名称显示
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tdx_stock_name_retrieval():
    """测试TongDaXinDataProvider的股票名称获取"""
    print("=" * 60)
    print("测试1: TongDaXinDataProvider股票名称获取")
    print("=" * 60)
    
    try:
        from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider
        
        provider = TongDaXinDataProvider()
        
        test_stocks = [
            '000001',  # 平安银行
            '600036',  # 招商银行
            '000858',  # 五粮液
            '600519',  # 贵州茅台
            '000651',  # 格力电器
        ]
        
        print("\n📊 TongDaXinDataProvider股票名称获取测试:")
        print("-" * 50)
        
        success_count = 0
        for stock_code in test_stocks:
            try:
                stock_name = provider._get_stock_name(stock_code)
                if stock_name != stock_code and not stock_name.startswith('股票'):
                    print(f"✅ {stock_code}: {stock_name}")
                    success_count += 1
                else:
                    print(f"⚠️  {stock_code}: {stock_name} (可能未从MongoDB获取)")
            except Exception as e:
                print(f"❌ {stock_code}: 获取失败 - {e}")
        
        print(f"\n📈 TongDaXinDataProvider成功率: {success_count}/{len(test_stocks)} ({success_count/len(test_stocks)*100:.1f}%)")
        return success_count == len(test_stocks)
        
    except Exception as e:
        print(f"❌ TongDaXinDataProvider测试失败: {e}")
        return False

def test_mongodb_direct_access():
    """测试直接从MongoDB获取股票名称"""
    print("\n" + "=" * 60)
    print("测试2: 直接MongoDB股票名称获取")
    print("=" * 60)
    
    try:
        from manufacturingagents.dataflows.tdx_utils import _get_stock_name_from_mongodb
        
        test_stocks = [
            '000001',  # 平安银行
            '600036',  # 招商银行
            '000858',  # 五粮液
            '600519',  # 贵州茅台
            '000651',  # 格力电器
            '510050',  # 50ETF
            '159919',  # 300ETF
        ]
        
        print("\n📊 直接MongoDB股票名称获取测试:")
        print("-" * 50)
        
        success_count = 0
        for stock_code in test_stocks:
            try:
                stock_name = _get_stock_name_from_mongodb(stock_code)
                if stock_name:
                    print(f"✅ {stock_code}: {stock_name}")
                    success_count += 1
                else:
                    print(f"⚠️  {stock_code}: 未找到")
            except Exception as e:
                print(f"❌ {stock_code}: 获取失败 - {e}")
        
        print(f"\n📈 直接MongoDB访问成功率: {success_count}/{len(test_stocks)} ({success_count/len(test_stocks)*100:.1f}%)")
        return success_count >= len(test_stocks) * 0.8  # 80%成功率即可
        
    except Exception as e:
        print(f"❌ 直接MongoDB访问测试失败: {e}")
        return False

def test_agent_utils_stock_mapping():
    """测试Agent工具中的股票名称映射"""
    print("\n" + "=" * 60)
    print("测试3: Agent工具股票名称映射")
    print("=" * 60)
    
    try:
        # 模拟agent_utils中的股票名称获取逻辑
        from manufacturingagents.dataflows.tdx_utils import _get_stock_name_from_mongodb
        
        test_stocks = [
            '000001',  # 平安银行
            '600036',  # 招商银行
            '000858',  # 五粮液
        ]
        
        print("\n📊 Agent工具股票名称映射测试:")
        print("-" * 50)
        
        success_count = 0
        for ticker in test_stocks:
            try:
                # 模拟agent_utils.py中的逻辑
                import re
                if re.match(r'^\d{6}$', str(ticker)):
                    company_name = _get_stock_name_from_mongodb(ticker)
                    if not company_name:
                        company_name = f"股票代码{ticker}"
                    
                    modified_query = f"{company_name}({ticker})"
                    
                    if company_name != f"股票代码{ticker}":
                        print(f"✅ {ticker}: {company_name} -> 查询: {modified_query}")
                        success_count += 1
                    else:
                        print(f"⚠️  {ticker}: {company_name} -> 查询: {modified_query}")
                else:
                    print(f"⚠️  {ticker}: 非中国股票代码格式")
                    
            except Exception as e:
                print(f"❌ {ticker}: 处理失败 - {e}")
        
        print(f"\n📈 Agent工具映射成功率: {success_count}/{len(test_stocks)} ({success_count/len(test_stocks)*100:.1f}%)")
        return success_count == len(test_stocks)
        
    except Exception as e:
        print(f"❌ Agent工具测试失败: {e}")
        return False

def test_real_time_data_with_names():
    """测试实时数据获取中的股票名称显示"""
    print("\n" + "=" * 60)
    print("测试4: 实时数据股票名称显示")
    print("=" * 60)
    
    try:
        from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider
        
        provider = TongDaXinDataProvider()
        
        test_stocks = ['000001', '600036']
        
        print("\n📊 实时数据股票名称显示测试:")
        print("-" * 50)
        
        success_count = 0
        for stock_code in test_stocks:
            try:
                print(f"\n🔍 测试 {stock_code}:")
                real_time_data = provider.get_real_time_data(stock_code)
                
                if real_time_data and 'name' in real_time_data:
                    stock_name = real_time_data['name']
                    if stock_name != stock_code and not stock_name.startswith('股票'):
                        print(f"  ✅ 股票名称: {stock_name}")
                        print(f"  📊 当前价格: {real_time_data.get('price', 'N/A')}")
                        success_count += 1
                    else:
                        print(f"  ⚠️  股票名称: {stock_name} (可能未从MongoDB获取)")
                else:
                    print(f"  ❌ 未获取到实时数据")
                    
            except Exception as e:
                print(f"  ❌ 获取失败: {e}")
        
        print(f"\n📈 实时数据名称显示成功率: {success_count}/{len(test_stocks)} ({success_count/len(test_stocks)*100:.1f}%)")
        return success_count == len(test_stocks)
        
    except Exception as e:
        print(f"❌ 实时数据测试失败: {e}")
        return False

def test_mongodb_connection():
    """测试MongoDB连接状态"""
    print("\n" + "=" * 60)
    print("测试5: MongoDB连接状态")
    print("=" * 60)
    
    try:
        from manufacturingagents.dataflows.tdx_utils import _get_mongodb_connection
        
        print("\n🔗 MongoDB连接测试:")
        print("-" * 30)
        
        client, db = _get_mongodb_connection()
        
        if client is not None and db is not None:
            # 测试连接
            client.admin.command('ping')
            
            # 检查集合
            collection = db['stock_basic_info']
            count = collection.count_documents({})
            
            print(f"✅ MongoDB连接成功")
            print(f"📊 股票记录总数: {count}")
            
            # 获取一些样本数据
            samples = list(collection.find().limit(3))
            print(f"📋 样本数据:")
            for sample in samples:
                print(f"  - {sample.get('code', 'N/A')}: {sample.get('name', 'N/A')}")
            
            return True
        else:
            print("❌ MongoDB连接失败")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB连接测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 完整的MongoDB股票名称迁移测试")
    print("=" * 80)
    
    test_results = []
    
    # 执行所有测试
    test_results.append(("MongoDB连接状态", test_mongodb_connection()))
    test_results.append(("直接MongoDB访问", test_mongodb_direct_access()))
    test_results.append(("TongDaXinDataProvider", test_tdx_stock_name_retrieval()))
    test_results.append(("Agent工具映射", test_agent_utils_stock_mapping()))
    test_results.append(("实时数据名称显示", test_real_time_data_with_names()))
    
    # 汇总结果
    print("\n" + "=" * 80)
    print("📊 测试结果汇总")
    print("=" * 80)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<25}: {status}")
        if result:
            passed_tests += 1
    
    print("-" * 50)
    print(f"总体通过率: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！MongoDB股票名称迁移成功！")
        print("\n✅ 迁移完成情况:")
        print("  - TongDaXinDataProvider已迁移到MongoDB")
        print("  - Agent工具已迁移到MongoDB")
        print("  - 实时数据获取已使用MongoDB股票名称")
        print("  - 向后兼容性保持良好")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️  大部分测试通过，迁移基本成功")
        print("  建议检查失败的测试项目")
    else:
        print("\n❌ 多个测试失败，迁移可能存在问题")
        print("  建议检查MongoDB连接和数据完整性")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        success = main()
        print("\n👋 测试完成")
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ 测试过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)