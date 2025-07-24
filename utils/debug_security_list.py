#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试get_security_list API
检查通达信API获取股票列表的具体情况
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider

def debug_security_list():
    """调试股票列表获取"""
    print("=== 调试股票列表获取 ===")
    
    try:
        provider = TongDaXinDataProvider()
        
        if not provider.connect():
            print("❌ 通达信API连接失败")
            return
            
        print("✅ 通达信API连接成功")
        
        # 测试深圳市场 (market=0)
        print("\n📊 测试深圳市场 (market=0)")
        try:
            sz_list = provider.api.get_security_list(0, 0)  # 深圳市场，起始位置0
            print(f"  获取到 {len(sz_list)} 条深圳市场数据")
            
            if sz_list:
                print("  前5条数据:")
                for i, stock in enumerate(sz_list[:5]):
                    print(f"    {i+1}. 代码: {stock.get('code', 'N/A')}, 名称: {stock.get('name', 'N/A')}")
                
                # 查找特定股票
                target_stocks = ['000001', '000002', '002594', '300750']
                for target in target_stocks:
                    found = False
                    for stock in sz_list:
                        if stock.get('code') == target:
                            print(f"  ✅ 找到 {target}: {stock.get('name', 'N/A')}")
                            found = True
                            break
                    if not found:
                        print(f"  ❌ 未找到 {target}")
        except Exception as e:
            print(f"  ❌ 获取深圳市场数据失败: {e}")
        
        # 测试上海市场 (market=1)
        print("\n📊 测试上海市场 (market=1)")
        try:
            sh_list = provider.api.get_security_list(1, 0)  # 上海市场，起始位置0
            print(f"  获取到 {len(sh_list)} 条上海市场数据")
            
            if sh_list:
                print("  前5条数据:")
                for i, stock in enumerate(sh_list[:5]):
                    print(f"    {i+1}. 代码: {stock.get('code', 'N/A')}, 名称: {stock.get('name', 'N/A')}")
                
                # 查找特定股票
                target_stocks = ['600519', '600036', '601127', '601398']
                for target in target_stocks:
                    found = False
                    for stock in sh_list:
                        if stock.get('code') == target:
                            print(f"  ✅ 找到 {target}: {stock.get('name', 'N/A')}")
                            found = True
                            break
                    if not found:
                        print(f"  ❌ 未找到 {target}")
                        
                # 如果第一批没找到，尝试获取更多数据
                if not any(stock.get('code') in ['600519', '600036', '601127', '601398'] for stock in sh_list):
                    print("  🔍 第一批未找到目标股票，尝试获取更多数据...")
                    try:
                        sh_list_2 = provider.api.get_security_list(1, 1000)  # 从位置1000开始
                        print(f"  第二批获取到 {len(sh_list_2)} 条数据")
                        if sh_list_2:
                            for target in target_stocks:
                                found = False
                                for stock in sh_list_2:
                                    if stock.get('code') == target:
                                        print(f"  ✅ 在第二批找到 {target}: {stock.get('name', 'N/A')}")
                                        found = True
                                        break
                                if not found:
                                    print(f"  ❌ 第二批也未找到 {target}")
                    except Exception as e:
                        print(f"  ❌ 获取第二批数据失败: {e}")
                        
        except Exception as e:
            print(f"  ❌ 获取上海市场数据失败: {e}")
        
        # 测试实时数据获取
        print("\n📊 测试实时数据获取")
        test_codes = [('000001', 0), ('600519', 1), ('601127', 1)]
        
        for code, market in test_codes:
            try:
                quotes = provider.api.get_security_quotes([(market, code)])
                if quotes:
                    quote = quotes[0]
                    print(f"  {code} (市场{market}): 价格={quote.get('price', 'N/A')}, 数据有效: {quote.get('price', 0) > 0}")
                else:
                    print(f"  {code} (市场{market}): 无数据")
            except Exception as e:
                print(f"  {code} (市场{market}): 获取失败 - {e}")
        
        provider.disconnect()
        
    except Exception as e:
        print(f"❌ 调试过程中出错: {e}")

if __name__ == "__main__":
    debug_security_list()