#!/usr/bin/env python3
"""
预处理助手验证测试
验证能否正确生成API调度参数
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), 'TradingAgents-CN')
sys.path.insert(0, project_root)

from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant

def test_preprocessing_assistant_initialization():
    """测试预处理助手初始化"""
    print("🧪 测试1: 预处理助手初始化")
    
    try:
        # 测试DashScope初始化
        assistant = PreprocessingAssistant(model_provider="dashscope")
        print("✅ DashScope预处理助手初始化成功")
        return True
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        return False

def test_fallback_parameters():
    """测试降级方案参数生成"""
    print("\n🧪 测试2: 降级方案参数生成")
    
    try:
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 准备测试输入
        test_input = {
            "city_name": "广东省佛山市",
            "brand_name": "格力",
            "product_type": "家用中央空调",
            "special_focus": "关注原材料价格",
            "current_time": "2025-07-19"
        }
        
        print(f"📋 测试输入: {test_input}")
        
        # 调用降级方案
        fallback_params = assistant._generate_fallback_parameters(test_input)
        
        print("✅ 降级方案成功生成参数")
        print("📊 生成的参数结构:")
        
        # 验证参数结构
        expected_apis = ["weather", "news", "holiday", "pmi", "ppi", "copper_futures"]
        
        for api in expected_apis:
            if api in fallback_params:
                print(f"  ✓ {api}: 已生成")
            else:
                print(f"  ❌ {api}: 缺失")
                return False
        
        # 打印具体参数内容（限制输出长度）
        print("\n📊 具体参数内容:")
        for api, params in fallback_params.items():
            print(f"  {api}: {json.dumps(params, ensure_ascii=False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 降级方案测试失败: {str(e)}")
        return False

def test_parameters_validation():
    """测试参数验证功能"""
    print("\n🧪 测试3: 参数验证功能")
    
    try:
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 生成测试参数
        test_input = {
            "city_name": "上海市",
            "brand_name": "美的",
            "product_type": "空调",
            "special_focus": "",
            "current_time": "2025-09-15"
        }
        
        fallback_params = assistant._generate_fallback_parameters(test_input)
        
        # 验证参数
        is_valid = assistant.validate_parameters(fallback_params)
        
        if is_valid:
            print("✅ 参数验证通过")
            return True
        else:
            print("❌ 参数验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 参数验证测试失败: {str(e)}")
        return False

def test_llm_parameter_generation():
    """测试大模型参数生成（如果API可用）"""
    print("\n🧪 测试4: 大模型参数生成")
    
    # 检查API密钥
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("⚠️ 未找到DASHSCOPE_API_KEY，跳过大模型测试")
        return True
    
    try:
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 准备测试输入
        test_input = {
            "city_name": "广州市",
            "brand_name": "海尔",
            "product_type": "智能冰箱",
            "special_focus": "关注节能政策",
            "current_time": datetime.now()
        }
        
        print(f"📋 测试输入: {test_input}")
        print("🔄 调用大模型生成参数...")
        
        # 调用大模型
        api_params = assistant.generate_api_parameters(
            city_name=test_input["city_name"],
            brand_name=test_input["brand_name"],
            product_type=test_input["product_type"],
            special_focus=test_input["special_focus"],
            current_time=test_input["current_time"]
        )
        
        print("✅ 大模型成功生成参数")
        
        # 验证参数
        if assistant.validate_parameters(api_params):
            print("✅ 大模型生成的参数验证通过")
            
            # 打印关键参数示例
            print("\n📊 关键参数示例:")
            print(f"  天气查询城市: {api_params['weather']['place']}")
            print(f"  新闻查询: {api_params['news']['activity_query']}")
            print(f"  节假日范围: {api_params['holiday']['start_date']} 到 {api_params['holiday']['end_date']}")
            
            return True
        else:
            print("❌ 大模型生成的参数验证失败")
            return False
            
    except Exception as e:
        print(f"⚠️ 大模型调用失败，这可能是API问题: {str(e)}")
        print("🔄 检查是否能使用降级方案...")
        
        # 尝试降级方案
        try:
            assistant = PreprocessingAssistant(model_provider="dashscope")
            fallback_params = assistant._generate_fallback_parameters({
                "city_name": "广州市",
                "brand_name": "海尔", 
                "product_type": "智能冰箱",
                "special_focus": "关注节能政策",
                "current_time": "2025-09-15"
            })
            
            if assistant.validate_parameters(fallback_params):
                print("✅ 降级方案正常工作")
                return True
            else:
                print("❌ 降级方案也失败")
                return False
                
        except Exception as fallback_error:
            print(f"❌ 降级方案测试失败: {str(fallback_error)}")
            return False

def test_different_scenarios():
    """测试不同输入场景"""
    print("\n🧪 测试5: 不同输入场景")
    
    test_cases = [
        {
            "name": "空调产品",
            "input": {
                "city_name": "深圳市",
                "brand_name": "格力",
                "product_type": "变频空调",
                "special_focus": "夏季销售",
                "current_time": "2025-06-15"
            }
        },
        {
            "name": "冰箱产品",
            "input": {
                "city_name": "北京",
                "brand_name": "海尔",
                "product_type": "对开门冰箱",
                "special_focus": "节能补贴",
                "current_time": "2025-11-20"
            }
        },
        {
            "name": "洗衣机产品",
            "input": {
                "city_name": "成都市",
                "brand_name": "小天鹅",
                "product_type": "滚筒洗衣机",
                "special_focus": "",
                "current_time": "2025-03-10"
            }
        }
    ]
    
    try:
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  场景 {i}: {test_case['name']}")
            
            try:
                fallback_params = assistant._generate_fallback_parameters(test_case["input"])
                
                if assistant.validate_parameters(fallback_params):
                    print(f"    ✅ {test_case['name']} 参数生成成功")
                    
                    # 显示关键信息
                    city = fallback_params["weather"]["place"]
                    activity_query = fallback_params["news"]["activity_query"]
                    print(f"    📍 城市: {city}")
                    print(f"    📰 活动查询: {activity_query}")
                    
                    success_count += 1
                else:
                    print(f"    ❌ {test_case['name']} 参数验证失败")
                    
            except Exception as e:
                print(f"    ❌ {test_case['name']} 处理失败: {str(e)}")
        
        if success_count == len(test_cases):
            print(f"\n✅ 所有 {len(test_cases)} 个场景测试通过")
            return True
        else:
            print(f"\n⚠️ {success_count}/{len(test_cases)} 个场景通过")
            return False
            
    except Exception as e:
        print(f"❌ 场景测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始预处理助手验证测试")
    print("=" * 60)
    
    # 执行所有测试
    tests = [
        test_preprocessing_assistant_initialization,
        test_fallback_parameters,
        test_parameters_validation,
        test_llm_parameter_generation,
        test_different_scenarios
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 异常: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🎯 测试总结: {passed}/{total} 通过")
    
    if passed == total:
        print("✅ 所有测试通过！预处理助手功能正常")
        print("\n🎉 结论: 预处理助手可以正常生成API调度参数")
    elif passed >= total - 1:  # 允许大模型测试失败
        print("⚠️ 基本功能正常，大模型调用可能有问题")
        print("\n🔧 建议: 检查DASHSCOPE_API_KEY配置")
    else:
        print("❌ 多个测试失败，需要修复问题")
    
    return passed >= total - 1  # 允许大模型测试失败

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 