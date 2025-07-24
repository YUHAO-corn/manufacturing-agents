#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试get_security_quotes返回的字段结构
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider

def debug_quotes_fields():
    """调试实时数据字段结构"""
    print("=== 调试实时数据字段结构 ===")
    
    try:
        provider = TongDaXinDataProvider()
        
        if not provider.connect():
            print("❌ 通达信API连接失败")
            return
            
        print("✅ 通达信API连接成功")
        
        # 测试不同市场的股票
        test_stocks = [
            ('000001', 0, '深圳主板'),
            ('000002', 0, '深圳主板'),
            ('002594', 0, '深圳中小板'),
            ('300750', 0, '深圳创业板'),
            ('600519', 1, '上海主板'),
            ('600036', 1, '上海主板'),
            ('601127', 1, '上海主板'),
            ('601398', 1, '上海主板')
        ]
        
        for code, market, market_name in test_stocks:
            print(f"\n📊 测试 {code} ({market_name})")
            try:
                quotes = provider.api.get_security_quotes([(market, code)])
                if quotes and len(quotes) > 0:
                    quote = quotes[0]
                    print(f"  返回数据类型: {type(quote)}")
                    print(f"  所有字段: {list(quote.keys()) if isinstance(quote, dict) else 'Not a dict'}")
                    
                    # 打印所有字段和值
                    if isinstance(quote, dict):
                        for key, value in quote.items():
                            print(f"    {key}: {value} (类型: {type(value)})")
                    else:
                        print(f"  原始数据: {quote}")
                        # 如果不是字典，尝试获取属性
                        if hasattr(quote, '__dict__'):
                            print(f"  对象属性: {quote.__dict__}")
                        # 尝试常见的属性名
                        for attr in ['code', 'name', 'price', 'last_close', 'open', 'high', 'low']:
                            try:
                                value = getattr(quote, attr, None)
                                if value is not None:
                                    print(f"    {attr}: {value}")
                            except:
                                pass
                else:
                    print(f"  ❌ 无数据返回")
            except Exception as e:
                print(f"  ❌ 获取失败: {e}")
        
        provider.disconnect()
        
    except Exception as e:
        print(f"❌ 调试过程中出错: {e}")

if __name__ == "__main__":
    debug_quotes_fields()