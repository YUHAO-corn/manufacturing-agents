#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TuShare 基础API测试
测试最简单的API调用来诊断token问题
"""

import tushare as ts
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

def load_token_from_env():
    """从.env文件读取最新的TUSHARE_TOKEN"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('TUSHARE_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    print(f"✅ 从.env文件读取到新Token: {token[:10]}...")
                    return token
    
    # 如果.env文件中没有找到，使用环境变量
    token = os.getenv('TUSHARE_TOKEN')
    if token:
        print(f"✅ 从环境变量读取到Token: {token[:10]}...")
        return token
    
    print("❌ 无法从.env文件或环境变量获取TUSHARE_TOKEN")
    return None

def test_basic_apis():
    """测试基础API调用"""
    
    # 从.env文件读取最新token
    token = load_token_from_env()
    if not token:
        print("❌ 无法获取TUSHARE_TOKEN")
        return False
    
    ts.set_token(token)
    
    print("=== TuShare 基础API测试 ===")
    print(f"使用Token: {token[:10]}...")
    
    try:
        # 获取TuShare pro接口
        pro = ts.pro_api()
        
        # 测试1: 最基础的股票列表 (通常免费)
        print("\n1. 测试股票基本信息...")
        stock_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
        print(f"✅ 股票基本信息获取成功! 获取到{len(stock_basic)}只股票")
        print("前3只股票:")
        print(stock_basic.head(3))
        
        # 测试2: 交易日历 (通常免费)  
        print("\n2. 测试交易日历...")
        trade_cal = pro.trade_cal(exchange='SSE', start_date='20250101', end_date='20250131')
        print(f"✅ 交易日历获取成功! 获取到{len(trade_cal)}条记录")
        print("前3条记录:")
        print(trade_cal.head(3))
        
        # 测试3: 获取某只股票的基本信息
        print("\n3. 测试个股基本信息...")
        stock_info = pro.stock_basic(ts_code='000001.SZ')
        print(f"✅ 个股信息获取成功!")
        print(stock_info)
        
        print("\n🎉 基础API测试全部通过! Token有效!")
        return True
        
    except Exception as e:
        print(f"❌ 基础API测试失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        
        # 提供诊断信息
        print("\n🔍 可能的问题:")
        print("1. Token已过期或无效")
        print("2. 账户被冻结或限制")
        print("3. 网络连接问题")
        print("4. TuShare服务器问题")
        print("5. 需要升级账户等级")
        
        return False

if __name__ == "__main__":
    print("开始TuShare基础API测试...")
    success = test_basic_apis()
    
    if success:
        print("\n✅ Token验证成功，可以继续进行制造业数据API测试")
    else:
        print("\n❌ Token验证失败，请检查token状态") 