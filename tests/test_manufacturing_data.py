#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据API测试
获取真实的输入输出格式，用于预处理助手设计
"""

import tushare as ts
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

def load_token_from_env():
    """从.env文件读取TUSHARE_TOKEN"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('TUSHARE_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    return token
    return os.getenv('TUSHARE_TOKEN')

def test_pmi_data():
    """测试PMI制造业采购经理指数"""
    print("\n🔍 测试PMI制造业采购经理指数...")
    try:
        pro = ts.pro_api()
        
        # 输入参数记录
        input_params = {
            "api_name": "cn_pmi",
            "start_m": "202301",
            "end_m": "202512",
            "fields": "month,pmi"
        }
        print(f"📥 输入参数:")
        print(json.dumps(input_params, indent=2, ensure_ascii=False))
        
        # API调用
        result = pro.cn_pmi(start_m='202301', end_m='202512', fields='month,pmi')
        
        # 输出结果记录
        print(f"📤 返回数据类型: {type(result)}")
        print(f"📤 返回数据形状: {result.shape}")
        print(f"📤 返回数据列名: {list(result.columns)}")
        print(f"📤 返回数据示例:")
        sample_data = result.head().to_dict('records')
        print(json.dumps(sample_data, indent=2, ensure_ascii=False, default=str))
        
        return {
            "api": "cn_pmi",
            "input": input_params,
            "output_type": str(type(result)),
            "output_shape": result.shape,
            "output_columns": list(result.columns),
            "output_sample": sample_data,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ PMI测试失败: {str(e)}")
        return {"api": "cn_pmi", "error": str(e), "status": "failed"}

def test_ppi_data():
    """测试PPI工业生产者出厂价格指数"""
    print("\n🔍 测试PPI工业生产者出厂价格指数...")
    try:
        pro = ts.pro_api()
        
        # 输入参数记录
        input_params = {
            "api_name": "cn_ppi",
            "start_m": "202301",
            "end_m": "202512",
            "fields": "month,ppi_yoy,ppi_mp"
        }
        print(f"📥 输入参数:")
        print(json.dumps(input_params, indent=2, ensure_ascii=False))
        
        # API调用
        result = pro.cn_ppi(start_m='202301', end_m='202512', fields='month,ppi_yoy,ppi_mp')
        
        # 输出结果记录
        print(f"📤 返回数据类型: {type(result)}")
        print(f"📤 返回数据形状: {result.shape}")
        print(f"📤 返回数据列名: {list(result.columns)}")
        print(f"📤 返回数据示例:")
        sample_data = result.head().to_dict('records')
        print(json.dumps(sample_data, indent=2, ensure_ascii=False, default=str))
        
        return {
            "api": "cn_ppi",
            "input": input_params,
            "output_type": str(type(result)),
            "output_shape": result.shape,
            "output_columns": list(result.columns),
            "output_sample": sample_data,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ PPI测试失败: {str(e)}")
        return {"api": "cn_ppi", "error": str(e), "status": "failed"}

def test_copper_futures():
    """测试铜期货价格数据"""
    print("\n🔍 测试铜期货价格数据...")
    try:
        pro = ts.pro_api()
        
        # 获取最近的铜期货合约
        current_date = datetime.now()
        current_month = current_date.strftime("%m")
        next_month = (current_date + timedelta(days=30)).strftime("%m")
        
        # 生成合约代码
        cu_current = f"CU25{current_month}.SHF"
        cu_next = f"CU25{next_month}.SHF"
        
        print(f"📊 测试合约: {cu_current} 和 {cu_next}")
        
        # 输入参数记录
        input_params = {
            "api_name": "fut_daily",
            "ts_code": cu_current,
            "start_date": "20250101",
            "end_date": "20251231",
            "fields": "ts_code,trade_date,close,vol,amount"
        }
        print(f"📥 输入参数:")
        print(json.dumps(input_params, indent=2, ensure_ascii=False))
        
        # API调用 - 获取当前月合约
        result_current = pro.fut_daily(
            ts_code=cu_current,
            start_date='20250101',
            end_date='20251231',
            fields='ts_code,trade_date,close,vol,amount'
        )
        
        # 获取下月合约数据
        result_next = pro.fut_daily(
            ts_code=cu_next,
            start_date='20250101', 
            end_date='20251231',
            fields='ts_code,trade_date,close,vol,amount'
        )
        
        # 输出结果记录
        print(f"📤 当前月合约 ({cu_current}) 数据:")
        print(f"   数据类型: {type(result_current)}")
        print(f"   数据形状: {result_current.shape}")
        print(f"   数据列名: {list(result_current.columns)}")
        current_sample = result_current.head().to_dict('records')
        print(f"   数据示例:")
        print(json.dumps(current_sample, indent=4, ensure_ascii=False, default=str))
        
        print(f"📤 下月合约 ({cu_next}) 数据:")
        print(f"   数据类型: {type(result_next)}")
        print(f"   数据形状: {result_next.shape}")
        next_sample = result_next.head().to_dict('records')
        print(f"   数据示例:")
        print(json.dumps(next_sample, indent=4, ensure_ascii=False, default=str))
        
        return {
            "api": "fut_daily",
            "input": input_params,
            "contracts": [cu_current, cu_next],
            "current_contract": {
                "ts_code": cu_current,
                "output_type": str(type(result_current)),
                "output_shape": result_current.shape,
                "output_columns": list(result_current.columns),
                "output_sample": current_sample
            },
            "next_contract": {
                "ts_code": cu_next,
                "output_type": str(type(result_next)),
                "output_shape": result_next.shape,
                "output_columns": list(result_next.columns),
                "output_sample": next_sample
            },
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ 铜期货测试失败: {str(e)}")
        return {"api": "fut_daily", "error": str(e), "status": "failed"}

def test_gdp_data():
    """测试GDP数据"""
    print("\n🔍 测试GDP数据...")
    try:
        pro = ts.pro_api()
        
        # 输入参数记录
        input_params = {
            "api_name": "cn_gdp",
            "start_q": "20230101",
            "end_q": "20251231",
            "fields": "quarter,gdp,gdp_yoy"
        }
        print(f"📥 输入参数:")
        print(json.dumps(input_params, indent=2, ensure_ascii=False))
        
        # API调用
        result = pro.cn_gdp(start_q='20230101', end_q='20251231', fields='quarter,gdp,gdp_yoy')
        
        # 输出结果记录
        print(f"📤 返回数据类型: {type(result)}")
        print(f"📤 返回数据形状: {result.shape}")
        print(f"📤 返回数据列名: {list(result.columns)}")
        print(f"📤 返回数据示例:")
        sample_data = result.head().to_dict('records')
        print(json.dumps(sample_data, indent=2, ensure_ascii=False, default=str))
        
        return {
            "api": "cn_gdp",
            "input": input_params,
            "output_type": str(type(result)),
            "output_shape": result.shape,
            "output_columns": list(result.columns),
            "output_sample": sample_data,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ GDP测试失败: {str(e)}")
        return {"api": "cn_gdp", "error": str(e), "status": "failed"}

def run_all_manufacturing_tests():
    """运行所有制造业数据API测试"""
    print("🚀 开始制造业数据API完整测试...")
    
    # 初始化token
    token = load_token_from_env()
    if not token:
        print("❌ 无法获取TUSHARE_TOKEN")
        return None
    
    ts.set_token(token)
    print(f"✅ 使用Token: {token[:10]}...")
    
    # 运行所有测试
    results = {
        "test_time": datetime.now().isoformat(),
        "token_prefix": token[:10],
        "tests": {
            "pmi_test": test_pmi_data(),
            "ppi_test": test_ppi_data(),
            "copper_futures_test": test_copper_futures(),
            "gdp_test": test_gdp_data()
        }
    }
    
    # 测试结果汇总
    print("\n📊 制造业数据API测试结果汇总:")
    success_count = 0
    for test_name, result in results["tests"].items():
        status = "✅ 成功" if result.get("status") == "success" else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result.get("status") == "success":
            success_count += 1
    
    print(f"\n🎯 测试通过率: {success_count}/4 ({success_count/4*100:.0f}%)")
    
    return results

if __name__ == "__main__":
    print("开始制造业数据API测试...")
    test_results = run_all_manufacturing_tests()
    
    if test_results:
        # 保存测试结果到文件
        with open("manufacturing_data_test_results.json", "w", encoding="utf-8") as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n💾 测试结果已保存到: manufacturing_data_test_results.json")
        
        # 根据测试结果创建API输入输出文档
        success_tests = [test for test in test_results["tests"].values() if test.get("status") == "success"]
        if success_tests:
            print(f"\n🎉 成功获取 {len(success_tests)} 个制造业数据API的真实输入输出格式！")
            print("📝 现在可以基于这些数据创建预处理助手的输入输出规范")
    else:
        print("\n❌ 制造业数据API测试失败") 