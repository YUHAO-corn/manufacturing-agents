#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试PMI数据的脚本
使用较短时间范围，确认数据返回是否完整
"""

import tushare as ts
import pandas as pd
import os
import json
from datetime import datetime
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

def test_pmi_short_range():
    """测试短时间范围的PMI数据"""
    print("🔍 测试PMI数据 - 短时间范围 (202505-202506)")
    
    token = load_token_from_env()
    ts.set_token(token)
    pro = ts.pro_api()
    
    try:
        # 使用较短的时间范围
        result = pro.cn_pmi(start_m='202505', end_m='202506', fields='month,pmi')
        
        print(f"📤 返回数据类型: {type(result)}")
        print(f"📤 返回数据形状: {result.shape}")
        print(f"📤 返回数据列名: {list(result.columns)}")
        print(f"📤 返回完整数据:")
        print(result.to_string())
        
        # 检查是否有pmi字段
        if 'pmi' in result.columns:
            print("✅ PMI字段存在！")
        else:
            print("❌ PMI字段缺失！")
        
        return result
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return None

def test_pmi_different_fields():
    """测试不同的PMI字段组合"""
    print("\n🔍 测试不同PMI字段组合")
    
    token = load_token_from_env()
    ts.set_token(token)
    pro = ts.pro_api()
    
    # 从TuShare文档截图看到的字段
    field_combinations = [
        "month,pmi",
        "month,pmi010000",
        "month,pmi010000,pmi010100,pmi010200",
        "month",  # 只要月份
    ]
    
    for fields in field_combinations:
        try:
            print(f"\n📥 测试字段组合: {fields}")
            result = pro.cn_pmi(start_m='202505', end_m='202506', fields=fields)
            
            print(f"   返回形状: {result.shape}")
            print(f"   返回列名: {list(result.columns)}")
            print(f"   前2行数据:")
            print(result.head(2).to_string())
            
        except Exception as e:
            print(f"   ❌ 失败: {str(e)}")

def test_pmi_no_fields():
    """测试不指定字段参数"""
    print("\n🔍 测试不指定fields参数（返回全部字段）")
    
    token = load_token_from_env()
    ts.set_token(token)
    pro = ts.pro_api()
    
    try:
        # 不指定fields参数，应该返回所有可用字段
        result = pro.cn_pmi(start_m='202505', end_m='202506')
        
        print(f"📤 返回数据类型: {type(result)}")
        print(f"📤 返回数据形状: {result.shape}")
        print(f"📤 返回数据列名: {list(result.columns)}")
        print(f"📤 前2行数据:")
        print(result.head(2).to_string())
        
        return result
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 开始PMI数据专项测试...")
    
    # 测试1: 短时间范围
    result1 = test_pmi_short_range()
    
    # 测试2: 不同字段组合
    test_pmi_different_fields()
    
    # 测试3: 不指定字段
    result3 = test_pmi_no_fields()
    
    print("\n📊 PMI测试总结:")
    if result1 is not None and 'pmi' in result1.columns:
        print("✅ 短时间范围测试：成功获取PMI数值")
    else:
        print("❌ 短时间范围测试：PMI数值缺失")
    
    if result3 is not None and result3.shape[1] > 1:
        print("✅ 全字段测试：返回多个字段")
        print(f"   可用字段: {list(result3.columns)}")
    else:
        print("❌ 全字段测试：字段数量不足") 