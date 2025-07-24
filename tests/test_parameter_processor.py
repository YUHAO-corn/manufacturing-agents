#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数预处理器测试
Test Parameter Processor

验证LLM驱动的参数生成是否符合预期
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_parameter_processor():
    """测试参数预处理器功能"""
    try:
        from manufacturingagents.manufacturingagents.utils.parameter_processor import get_parameter_processor
        from manufacturingagents.default_config import DEFAULT_CONFIG
        
        print("🧪 [测试] 开始测试参数预处理器...")
        
        # 初始化预处理器
        config = DEFAULT_CONFIG.copy()
        processor = get_parameter_processor(config)
        
        # 测试用例
        test_cases = [
            {
                "city_name": "厦门",
                "brand_name": "格力", 
                "product_category": "空调",
                "special_focus": "",
                "current_date": "2025-07-21"
            },
            {
                "city_name": "广州市",
                "brand_name": "美的",
                "product_category": "冰箱", 
                "special_focus": "关注节能效果",
                "current_date": "2025-07-21"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 [测试用例 {i}] {test_case['city_name']} {test_case['brand_name']} {test_case['product_category']}")
            
            # 生成参数
            result = processor.generate_api_parameters(**test_case)
            
            # 验证结果结构
            required_keys = ['weather_params', 'news_params', 'holiday_params', 'pmi_params', 'ppi_params', 'futures_params']
            
            for key in required_keys:
                if key not in result:
                    print(f"❌ 缺少必需的参数: {key}")
                    return False
                else:
                    print(f"✅ {key}: 存在")
            
            # 验证具体参数格式
            # 1. 验证天气参数
            weather = result['weather_params']
            if weather.get('place') and weather.get('dailyForecast') == True:
                print(f"✅ 天气参数: 城市={weather['place']}")
            else:
                print(f"❌ 天气参数格式错误: {weather}")
                return False
            
            # 2. 验证新闻参数
            news = result['news_params']
            required_news_keys = ['activity_query', 'area_news_query', 'new_building_query', 'policy_query']
            for news_key in required_news_keys:
                if news_key in news and news[news_key]:
                    print(f"✅ 新闻参数 {news_key}: 已生成")
                else:
                    print(f"❌ 新闻参数 {news_key}: 缺失或为空")
                    return False
            
            # 3. 验证节假日参数
            holiday = result['holiday_params']
            if 'start_date' in holiday and 'end_date' in holiday:
                print(f"✅ 节假日参数: {holiday['start_date']} 到 {holiday['end_date']}")
            else:
                print(f"❌ 节假日参数格式错误: {holiday}")
                return False
            
            # 4. 验证PMI/PPI参数
            for data_type in ['pmi_params', 'ppi_params']:
                params = result[data_type]
                if all(key in params for key in ['start_m', 'end_m', 'fields']):
                    print(f"✅ {data_type}: {params['start_m']} 到 {params['end_m']}")
                else:
                    print(f"❌ {data_type}格式错误: {params}")
                    return False
            
            # 5. 验证期货参数
            futures = result['futures_params']
            if isinstance(futures, list) and len(futures) == 2:
                for j, future in enumerate(futures):
                    if 'ts_code' in future and future['ts_code'].startswith('CU'):
                        print(f"✅ 期货参数{j+1}: {future['ts_code']}")
                    else:
                        print(f"❌ 期货参数{j+1}格式错误: {future}")
                        return False
            else:
                print(f"❌ 期货参数结构错误: {futures}")
                return False
            
            # 验证时间逻辑
            current_dt = datetime.strptime(test_case['current_date'], '%Y-%m-%d')
            
            # PMI/PPI应该是过往月份（考虑延迟）
            pmi_end_month = result['pmi_params']['end_m']
            expected_end_month = (current_dt.replace(day=1) - timedelta(days=1)).strftime('%Y%m')
            
            if pmi_end_month == expected_end_month:
                print(f"✅ PMI时间逻辑正确: 数据延迟已考虑")
            else:
                print(f"❌ PMI时间逻辑错误: 期望{expected_end_month}, 实际{pmi_end_month}")
                return False
            
            # 期货应该是当月和下月
            current_month = current_dt.strftime('%y%m')
            next_month = (current_dt.replace(day=1) + timedelta(days=32)).strftime('%y%m')
            
            futures_codes = [f['ts_code'] for f in futures]
            expected_codes = [f"CU{current_month}.SHF", f"CU{next_month}.SHF"]
            
            if set(futures_codes) == set(expected_codes):
                print(f"✅ 期货时间逻辑正确: {futures_codes}")
            else:
                print(f"❌ 期货时间逻辑错误: 期望{expected_codes}, 实际{futures_codes}")
                return False
        
        print(f"\n🎉 [测试结果] 参数预处理器测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ [测试失败] 参数预处理器测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_single_api_generation():
    """测试单个API参数生成"""
    try:
        from manufacturingagents.manufacturingagents.utils.parameter_processor import get_parameter_processor
        
        print("\n🔧 [测试] 单个API参数生成...")
        
        processor = get_parameter_processor()
        current_date = "2025-07-21"
        
        # 测试各个API类型
        api_tests = [
            ("weather", {"city_name": "厦门市", "current_date": current_date}),
            ("pmi", {"current_date": current_date}),
            ("ppi", {"current_date": current_date}),
            ("futures", {"current_date": current_date})
        ]
        
        for api_type, kwargs in api_tests:
            result = processor.generate_single_api_params(api_type, **kwargs)
            print(f"✅ {api_type}参数生成: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 单个API参数生成测试失败: {e}")
        return False

def test_parameter_validation():
    """测试参数验证功能"""
    print("\n🔍 [测试] 参数验证功能...")
    
    # 测试日期范围验证
    current_date = "2025-07-21"
    current_dt = datetime.strptime(current_date, '%Y-%m-%d')
    
    # PMI/PPI应该考虑1个月延迟
    expected_end_month = (current_dt.replace(day=1) - timedelta(days=1))
    expected_start_month = expected_end_month - timedelta(days=150)
    
    print(f"📅 当前日期: {current_date}")
    print(f"📅 PMI/PPI预期时间范围: {expected_start_month.strftime('%Y%m')} 到 {expected_end_month.strftime('%Y%m')}")
    
    # 期货应该是当月和下月
    current_month = current_dt.strftime('%y%m')
    next_month = (current_dt.replace(day=1) + timedelta(days=32)).strftime('%y%m')
    
    print(f"📅 期货预期合约: CU{current_month}.SHF, CU{next_month}.SHF")
    
    return True

if __name__ == "__main__":
    print("🧪 开始参数预处理器全面测试...")
    
    # 运行所有测试
    tests = [
        test_parameter_validation,
        test_single_api_generation, 
        test_parameter_processor
    ]
    
    all_passed = True
    for test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 异常: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有测试通过！参数预处理器功能正常")
    else:
        print("\n❌ 部分测试失败，需要进一步调试") 