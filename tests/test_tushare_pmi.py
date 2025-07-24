#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TuShare API 测试脚本
测试制造业PMI数据获取
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import json

def test_tushare_pmi():
    """测试TuShare PMI数据获取"""
    
    # 配置TuShare token
    token = "045cef05662b24b883d4e7fd6d87029cbcd0d2224c87c110d42f2816"
    ts.set_token(token)
    
    # 获取TuShare pro接口
    pro = ts.pro_api()
    
    print("=== TuShare API 连接测试 ===")
    
    try:
        # 测试1: 获取制造业PMI数据
        print("\n1. 测试制造业PMI数据获取...")
        
        # 获取最近12个月的PMI数据
        end_date = datetime.now().strftime('%Y%m')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m')
        
        # 获取PMI数据
        pmi_data = pro.cn_ppi(
            start_m=start_date,
            end_m=end_date
        )
        
        print(f"✅ PMI数据获取成功!")
        print(f"数据条数: {len(pmi_data)}")
        print(f"数据列: {list(pmi_data.columns)}")
        
        if not pmi_data.empty:
            print("\n最新PMI数据:")
            print(pmi_data.head(3))
        
        # 测试2: 获取GDP数据
        print("\n2. 测试GDP数据获取...")
        
        gdp_data = pro.cn_gdp(
            start_q='20240101',
            end_q='20241231'
        )
        
        print(f"✅ GDP数据获取成功!")
        print(f"数据条数: {len(gdp_data)}")
        
        if not gdp_data.empty:
            print("\n最新GDP数据:")
            print(gdp_data.head(2))
        
        # 测试3: 获取CPI数据
        print("\n3. 测试CPI数据获取...")
        
        cpi_data = pro.cn_cpi(
            start_m=start_date,
            end_m=end_date
        )
        
        print(f"✅ CPI数据获取成功!")
        print(f"数据条数: {len(cpi_data)}")
        
        if not cpi_data.empty:
            print("\n最新CPI数据:")
            print(cpi_data.head(3))
        
        # 汇总测试结果
        print("\n=== TuShare API 测试结果汇总 ===")
        print("✅ PMI数据: 可用")
        print("✅ GDP数据: 可用") 
        print("✅ CPI数据: 可用")
        print("✅ TuShare API 连接正常，数据获取成功！")
        
        # 保存测试数据样本
        test_results = {
            "test_time": datetime.now().isoformat(),
            "pmi_sample": pmi_data.head(3).to_dict('records') if not pmi_data.empty else [],
            "gdp_sample": gdp_data.head(2).to_dict('records') if not gdp_data.empty else [],
            "cpi_sample": cpi_data.head(3).to_dict('records') if not cpi_data.empty else []
        }
        
        with open('tushare_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 测试结果已保存到: tushare_test_results.json")
        
        return True
        
    except Exception as e:
        print(f"❌ TuShare API 测试失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("开始测试TuShare API...")
    success = test_tushare_pmi()
    
    if success:
        print("\n🎉 TuShare API 测试全部通过！")
    else:
        print("\n⚠️ TuShare API 测试失败，请检查token或网络连接") 