#!/usr/bin/env python3
"""
测试预处理助手的连通性和参数生成功能
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 加载环境变量
load_dotenv()

def test_preprocessing_assistant():
    """测试预处理助手"""
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        print("🔄 初始化预处理助手...")
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        print("🔄 开始测试参数生成...")
        
        # 测试用例1：广州美的空调
        test_input = {
            "city_name": "广州",
            "brand_name": "美的",
            "product_type": "空调",
            "special_focus": "关注原材料价格",
            "current_time": datetime(2025, 7, 19)
        }
        
        print(f"📋 测试输入: {test_input}")
        
        # 生成API参数
        api_params = assistant.generate_api_parameters(
            city_name=test_input["city_name"],
            brand_name=test_input["brand_name"],
            product_type=test_input["product_type"],
            special_focus=test_input["special_focus"],
            current_time=test_input["current_time"]
        )
        
        print("✅ 参数生成成功！")
        print("📊 生成的API参数:")
        print(json.dumps(api_params, ensure_ascii=False, indent=2))
        
        # 验证参数格式
        if assistant.validate_parameters(api_params):
            print("✅ 参数格式验证通过！")
            
            # 检查关键字段
            expected_apis = ["weather", "news", "holiday", "pmi", "ppi", "copper_futures"]
            for api in expected_apis:
                if api in api_params:
                    print(f"  ✅ {api} API参数正常")
                else:
                    print(f"  ❌ 缺少 {api} API参数")
            
            # 检查城市名标准化
            if api_params.get("weather", {}).get("place") == "广州":
                print("  ✅ 城市名标准化正确")
            else:
                print(f"  ⚠️ 城市名标准化可能有问题: {api_params.get('weather', {}).get('place')}")
            
            # 检查时间格式
            pmi_start = api_params.get("pmi", {}).get("start_m")
            if pmi_start and len(pmi_start) == 6 and pmi_start.isdigit():
                print(f"  ✅ PMI时间格式正确: {pmi_start}")
            else:
                print(f"  ⚠️ PMI时间格式可能有问题: {pmi_start}")
            
            return True
        else:
            print("❌ 参数格式验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_only():
    """仅测试降级方案"""
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        print("🔄 测试降级方案...")
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 直接测试降级方案
        user_input = {
            "city_name": "佛山市",
            "brand_name": "海尔",
            "product_type": "冰箱",
            "special_focus": "无特殊要求",
            "current_time": "2025-01-19"
        }
        
        fallback_params = assistant._generate_fallback_parameters(user_input)
        
        print("🎯 降级方案生成成功！")
        print(json.dumps(fallback_params, ensure_ascii=False, indent=2))
        
        # 验证降级方案
        if assistant.validate_parameters(fallback_params):
            print("✅ 降级方案格式验证通过！")
            return True
        else:
            print("❌ 降级方案格式验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 降级方案测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试预处理助手...")
    
    # 检查环境变量
    if os.getenv('DASHSCOPE_API_KEY'):
        print("✅ 发现DASHSCOPE_API_KEY环境变量")
        
        # 测试完整功能（包含大模型调用）
        success = test_preprocessing_assistant()
    else:
        print("⚠️ 未发现DASHSCOPE_API_KEY环境变量，仅测试降级方案")
        
        # 仅测试降级方案
        success = test_fallback_only()
    
    if success:
        print("🎉 预处理助手测试通过！")
        sys.exit(0)
    else:
        print("💥 预处理助手测试失败！")
        sys.exit(1) 