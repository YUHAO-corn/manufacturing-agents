#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证器测试
Test Data Validator

验证数据质量检查功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_data_validator():
    """测试数据验证器功能"""
    try:
        from manufacturingagents.manufacturingagents.utils.data_validator import get_data_validator
        
        print("🧪 [测试] 开始测试数据验证器...")
        
        validator = get_data_validator()
        
        # 测试用例：模拟各种API返回数据
        test_cases = {
            "weather": {
                "good_data": """
                ## 厦门制造业天气预报数据 (2025-07-21)
                
                {
                  "daily_forecast": [
                    {"date": "2025-07-21", "weather": "晴天", "temperature": "28-35度"},
                    {"date": "2025-07-22", "weather": "多云", "temperature": "26-33度"},
                    {"date": "2025-07-23", "weather": "小雨", "temperature": "24-30度"}
                  ]
                }
                """,
                "bad_data": "无效数据",
                "empty_data": ""
            },
            "news": {
                "good_data": """
                ## 制造业新闻数据 - 格力 空调 (2025-07-21)
                
                {
                  "activity_results": [
                    {"title": "格力空调夏季促销活动启动", "content": "格力电器宣布启动夏季促销活动..."}
                  ],
                  "area_results": [
                    {"title": "厦门制造业发展良好", "content": "厦门市制造业继续保持良好发展态势..."}
                  ],
                  "new_building_results": [
                    {"title": "厦门新楼盘集中交付", "content": "近期厦门多个新楼盘集中交付..."}
                  ],
                  "policy_results": [
                    {"title": "家电购买补贴政策", "content": "政府出台家电购买补贴政策..."}
                  ]
                }
                """,
                "bad_data": "这是一些无关的文本内容",
                "empty_data": "{}"
            },
            "holiday": {
                "good_data": """
                ## 制造业节假日数据 (2025-07-21到2025-10-19)
                
                {
                  "holidays": [
                    {"date": "2025-08-01", "name": "建军节", "type": "纪念日"},
                    {"date": "2025-09-15", "name": "中秋节", "type": "法定节假日"},
                    {"date": "2025-10-01", "name": "国庆节", "type": "法定节假日"},
                    {"date": "2025-10-07", "name": "国庆假期结束", "type": "调休"}
                  ]
                }
                """,
                "bad_data": "没有节假日信息",
                "empty_data": "[]"
            },
            "pmi": {
                "good_data": """
                ## PMI制造业采购经理指数 (202501到202506)
                
                month     pmi010000
                202501    50.1
                202502    50.5
                202503    50.8
                202504    50.3
                202505    50.6
                202506    51.2
                """,
                "bad_data": "PMI数据获取失败",
                "empty_data": ""
            },
            "ppi": {
                "good_data": """
                ## PPI工业生产者价格指数 (202501到202506)
                
                month     ppi_yoy    ppi_mp
                202501    -2.1       -0.3
                202502    -1.8       -0.1
                202503    -1.5        0.1
                202504    -1.2        0.2
                202505    -0.9        0.3
                202506    -0.6        0.4
                """,
                "bad_data": "PPI数据异常",
                "empty_data": ""
            },
            "futures": {
                "good_data": """
                ## 铜期货数据 (2025-07-21)
                
                ts_code      trade_date   close
                CU2507.SHF   2025-07-15   58000
                CU2507.SHF   2025-07-16   58200
                CU2507.SHF   2025-07-17   57800
                CU2508.SHF   2025-07-15   58100
                CU2508.SHF   2025-07-16   58300
                CU2508.SHF   2025-07-17   57900
                """,
                "bad_data": "期货数据获取失败",
                "empty_data": ""
            }
        }
        
        # 测试每种数据类型
        for data_type, test_data in test_cases.items():
            print(f"\n📋 [测试] {data_type.upper()} 数据验证")
            
            # 测试好数据
            passed, score, issues = validator.validate_api_data(data_type, test_data["good_data"])
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"  好数据: {status} (分数: {score:.2f})")
            if issues:
                print(f"    问题: {issues}")
            
            # 测试坏数据
            passed, score, issues = validator.validate_api_data(data_type, test_data["bad_data"])
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"  坏数据: {status} (分数: {score:.2f})")
            if issues:
                print(f"    问题: {issues}")
            
            # 测试空数据
            passed, score, issues = validator.validate_api_data(data_type, test_data["empty_data"])
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"  空数据: {status} (分数: {score:.2f})")
            if issues:
                print(f"    问题: {issues}")
        
        return True
        
    except Exception as e:
        print(f"❌ [测试失败] 数据验证器测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation_report():
    """测试验证报告生成"""
    try:
        from manufacturingagents.manufacturingagents.utils.data_validator import get_data_validator
        
        print("\n🧪 [测试] 验证报告生成...")
        
        validator = get_data_validator()
        
        # 模拟验证结果
        validations = {
            "weather": (True, 0.85, []),
            "news": (True, 0.75, ["新闻内容略少"]),
            "holiday": (False, 0.45, ["节假日数据缺少相关信息", "节假日数据中日期信息过少"]),
            "pmi": (True, 0.90, []),
            "ppi": (True, 0.88, []),
            "futures": (False, 0.50, ["期货数据缺少预期合约代码"])
        }
        
        # 生成报告
        report = validator.generate_validation_report(validations)
        print("📊 验证报告:")
        print(report)
        
        return True
        
    except Exception as e:
        print(f"❌ 验证报告测试失败: {e}")
        return False

def test_all_data_validation():
    """测试完整数据验证流程"""
    try:
        from manufacturingagents.manufacturingagents.utils.data_validator import get_data_validator
        
        print("\n🧪 [测试] 完整数据验证流程...")
        
        validator = get_data_validator()
        
        # 模拟完整的制造业数据
        all_data = {
            "weather_data": "厦门天气预报：明天晴天，温度28-35度，后天多云，温度26-33度",
            "news_data": "制造业新闻：格力空调促销活动启动，厦门新楼盘交付，政府出台家电补贴政策",
            "holiday_data": "节假日信息：8月1日建军节，9月15日中秋节，10月1日国庆节",
            "pmi_data": "PMI数据：202501月50.1，202502月50.5，202503月50.8，202504月50.3",
            "ppi_data": "PPI数据：202501月-2.1%，202502月-1.8%，202503月-1.5%，202504月-1.2%",
            "futures_data": "期货数据：CU2507.SHF价格58000，CU2508.SHF价格58100"
        }
        
        # 执行完整验证
        result = validator.validate_all_manufacturing_data(all_data)
        
        print(f"📊 验证结果:")
        print(f"  总体通过: {result['overall_passed']}")
        print(f"  平均分数: {result['average_score']:.2f}")
        print(f"  详细验证:")
        for data_type, (passed, score, issues) in result['validations'].items():
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"    {data_type}: {status} ({score:.2f})")
        
        print("\n📋 完整验证报告:")
        print(result['report'])
        
        return True
        
    except Exception as e:
        print(f"❌ 完整数据验证测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_quality_standards():
    """测试数据质量标准"""
    print("\n🔍 [测试] 数据质量标准...")
    
    from manufacturingagents.manufacturingagents.utils.data_validator import get_data_validator
    
    validator = get_data_validator()
    
    print("📏 数据质量标准:")
    print(f"  最低质量分数: {validator.min_data_quality_score}")
    
    print("\n📋 验证规则:")
    for data_type, rules in validator.validation_rules.items():
        print(f"  {data_type.upper()}:")
        if "required_fields" in rules:
            print(f"    必需字段: {rules['required_fields']}")
        if "data_range" in rules:
            print(f"    数据范围: {rules['data_range']}")
        if "min_records" in rules:
            print(f"    最少记录数: {rules['min_records']}")
    
    return True

if __name__ == "__main__":
    print("🧪 开始数据验证器全面测试...")
    
    # 运行所有测试
    tests = [
        test_data_quality_standards,
        test_data_validator,
        test_validation_report,
        test_all_data_validation
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
        print("\n🎉 所有测试通过！数据验证器功能正常")
    else:
        print("\n❌ 部分测试失败，需要进一步调试") 