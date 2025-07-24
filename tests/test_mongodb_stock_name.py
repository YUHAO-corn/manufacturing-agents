#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试从MongoDB获取股票名称的功能

这个脚本用于验证修改后的TongDaXinDataProvider是否能够正确从MongoDB获取股票名称。
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider

def test_stock_name_retrieval():
    """测试股票名称获取功能"""
    print("=" * 60)
    print("测试从MongoDB获取股票名称功能")
    print("=" * 60)
    
    # 创建通达信数据提供者实例
    provider = TongDaXinDataProvider()
    
    # 测试股票代码列表
    test_stocks = [
        '000001',  # 平安银行
        '000002',  # 万科A
        '600000',  # 浦发银行
        '600036',  # 招商银行
        '000858',  # 五粮液
        '600519',  # 贵州茅台
        '000166',  # 申万宏源
        '601318',  # 中国平安
        '510050',  # 50ETF
        '159919',  # 300ETF
        '000300',  # 沪深300指数
        '399001',  # 深证成指
        '999999',  # 不存在的股票代码
    ]
    
    print("\n📊 测试股票名称获取:")
    print("-" * 50)
    
    success_count = 0
    total_count = len(test_stocks)
    
    for stock_code in test_stocks:
        try:
            stock_name = provider._get_stock_name(stock_code)
            
            # 判断是否成功获取到名称（不是返回股票代码本身）
            if stock_name != stock_code:
                print(f"✅ {stock_code}: {stock_name}")
                success_count += 1
            else:
                print(f"⚠️  {stock_code}: 未找到名称，返回代码本身")
                
        except Exception as e:
            print(f"❌ {stock_code}: 获取失败 - {e}")
    
    print("-" * 50)
    print(f"📈 成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    # 测试缓存功能
    print("\n🔄 测试缓存功能:")
    print("-" * 30)
    
    # 第二次获取同一个股票名称，应该从缓存中获取
    test_code = '000001'
    print(f"第一次获取 {test_code}: {provider._get_stock_name(test_code)}")
    print(f"第二次获取 {test_code}: {provider._get_stock_name(test_code)} (应该从缓存获取)")
    
    print("\n✅ 股票名称获取功能测试完成")

def test_real_time_data_with_names():
    """测试实时数据获取中的股票名称显示"""
    print("\n" + "=" * 60)
    print("测试实时数据中的股票名称显示")
    print("=" * 60)
    
    provider = TongDaXinDataProvider()
    
    # 测试获取实时数据
    test_stocks = ['000001', '600036', '000858']
    
    for stock_code in test_stocks:
        try:
            print(f"\n📊 获取 {stock_code} 的实时数据:")
            real_time_data = provider.get_real_time_data(stock_code)
            
            if real_time_data:
                print(f"  股票代码: {real_time_data.get('code', 'N/A')}")
                print(f"  股票名称: {real_time_data.get('name', 'N/A')}")
                print(f"  当前价格: {real_time_data.get('price', 'N/A')}")
                print(f"  涨跌幅: {real_time_data.get('change_percent', 'N/A')}%")
            else:
                print(f"  ⚠️ 未获取到 {stock_code} 的实时数据")
                
        except Exception as e:
            print(f"  ❌ 获取 {stock_code} 实时数据失败: {e}")
    
    print("\n✅ 实时数据股票名称测试完成")

if __name__ == "__main__":
    try:
        # 测试股票名称获取
        test_stock_name_retrieval()
        
        # 测试实时数据中的股票名称
        test_real_time_data_with_names()
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n👋 测试结束")