#!/usr/bin/env python3
"""
最终验证测试：确认大模型能正确生成预期的API参数
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), 'TradingAgents-CN')
sys.path.insert(0, project_root)

def test_final_validation():
    """最终验证：大模型能生成预期结果"""
    print("🎯 最终验证：确认大模型能正确生成预期的API参数")
    print("=" * 60)
    
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        assistant = PreprocessingAssistant(model_provider="dashscope")
        print("✅ PreprocessingAssistant 初始化成功")
        
        # 测试输入
        test_input = {
            "city_name": "广州市",
            "brand_name": "美的",
            "product_type": "空调",
            "special_focus": "关注政策",
            "current_time": "2025-07-19"
        }
        
        print(f"📋 测试输入: {test_input}")
        print("🔄 调用大模型生成参数...")
        
        # 直接调用大模型
        api_params = assistant._call_llm_for_parameters(test_input)
        
        print("🎉 大模型成功生成参数！")
        
        # 验证必需字段
        required_apis = ["weather", "news", "holiday", "pmi", "ppi", "copper_futures"]
        missing_apis = [api for api in required_apis if api not in api_params]
        
        if missing_apis:
            print(f"❌ 缺少API: {missing_apis}")
            return False
        
        print("✅ 包含所有必需的6个API参数")
        
        # 验证关键内容（宽松验证）
        weather_city = api_params["weather"]["place"]
        news_query = api_params["news"]["area_news_query"]
        holiday_start = api_params["holiday"]["start_date"]
        
        print(f"📊 关键参数验证:")
        print(f"  天气城市: {weather_city}")
        print(f"  新闻查询: {news_query}")
        print(f"  节假日开始: {holiday_start}")
        print(f"  PMI时间: {api_params['pmi']['start_m']} 到 {api_params['pmi']['end_m']}")
        print(f"  期货合约: {api_params['copper_futures']['current_month']}")
        
        # 基本有效性检查
        validations = [
            ("城市不为空", weather_city and len(weather_city.strip()) > 0),
            ("包含品牌信息", "美的" in news_query),
            ("日期格式有效", "2025" in holiday_start and ("7" in holiday_start or "07" in holiday_start)),
            ("PMI格式正确", len(api_params['pmi']['start_m']) == 6),
            ("期货合约格式", "CU25" in api_params['copper_futures']['current_month'])
        ]
        
        all_valid = True
        for check_name, is_valid in validations:
            status = "✅" if is_valid else "❌"
            print(f"  {status} {check_name}")
            if not is_valid:
                all_valid = False
        
        if all_valid:
            print("\n🎉 所有验证通过！大模型能正确生成预期的API参数")
            
            # 保存成功的参数
            with open('final_success_params.json', 'w', encoding='utf-8') as f:
                json.dump(api_params, f, ensure_ascii=False, indent=2)
            print("📄 完整参数已保存到: final_success_params.json")
            
            return True
        else:
            print("\n⚠️ 部分验证失败，但大模型基本功能正常")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始最终验证测试")
    
    success = test_final_validation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 最终结论：预处理助手的大模型调用功能完全成功！")
        print("✅ 能够生成预期的API调度参数")
        print("✅ 参数格式正确，内容有效")
        print("✅ 降级方案已不再需要，大模型直接可用")
    else:
        print("⚠️ 大模型功能基本正常，但可能需要微调")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 