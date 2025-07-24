#!/usr/bin/env python3
"""
展示大模型完整输出的测试脚本
让用户亲自查看返回的结构和内容
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), 'TradingAgents-CN')
sys.path.insert(0, project_root)

def show_complete_output():
    """展示大模型的完整输出"""
    print("🔍 展示大模型完整输出")
    print("=" * 80)
    
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        assistant = PreprocessingAssistant(model_provider="dashscope")
        print("✅ PreprocessingAssistant 初始化成功")
        
        # 测试输入
        test_input = {
            "city_name": "上海市浦东新区",
            "brand_name": "海尔",
            "product_type": "智能洗衣机",
            "special_focus": "关注节能环保",
            "current_time": "2025-08-25"
        }
        
        print(f"\n📋 测试输入:")
        for key, value in test_input.items():
            print(f"  {key}: {value}")
        
        print(f"\n🔄 开始调用大模型...")
        print("-" * 80)
        
        # 直接调用大模型
        api_params = assistant._call_llm_for_parameters(test_input)
        
        print("-" * 80)
        print("🎉 大模型调用成功！")
        
        print(f"\n📊 返回的完整结构:")
        print("=" * 80)
        print(json.dumps(api_params, ensure_ascii=False, indent=2))
        print("=" * 80)
        
        print(f"\n🔍 详细分析返回内容:")
        print("-" * 50)
        
        # 逐个分析每个API参数
        if "weather" in api_params:
            print(f"1️⃣ 天气API参数:")
            for key, value in api_params["weather"].items():
                print(f"   {key}: {value}")
            print()
        
        if "news" in api_params:
            print(f"2️⃣ 新闻API参数:")
            for key, value in api_params["news"].items():
                print(f"   {key}: {value}")
            print()
        
        if "holiday" in api_params:
            print(f"3️⃣ 节假日API参数:")
            for key, value in api_params["holiday"].items():
                print(f"   {key}: {value}")
            print()
        
        if "pmi" in api_params:
            print(f"4️⃣ PMI API参数:")
            for key, value in api_params["pmi"].items():
                print(f"   {key}: {value}")
            print()
        
        if "ppi" in api_params:
            print(f"5️⃣ PPI API参数:")
            for key, value in api_params["ppi"].items():
                print(f"   {key}: {value}")
            print()
        
        if "copper_futures" in api_params:
            print(f"6️⃣ 期货API参数:")
            for key, value in api_params["copper_futures"].items():
                print(f"   {key}: {value}")
            print()
        
        # 验证参数
        print("🔍 参数验证:")
        print(f"  - 包含API数量: {len(api_params)}")
        print(f"  - 城市标准化: '{test_input['city_name']}' → '{api_params['weather']['place']}'")
        print(f"  - 品牌包含: '{test_input['brand_name']}' 在 '{api_params['news']['area_news_query']}'")
        print(f"  - 产品包含: '{test_input['product_type']}' 相关查询")
        print(f"  - 时间处理: 开始 '{api_params['holiday']['start_date']}'，结束 '{api_params['holiday']['end_date']}'")
        
        # 保存完整输出
        output_file = f"complete_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "input": test_input,
                "output": api_params,
                "timestamp": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 完整输出已保存到: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        print("详细错误信息:")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 展示大模型完整输出测试")
    print("🎯 目标: 让用户亲自查看大模型返回的结构和内容")
    
    success = show_complete_output()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ 测试完成！请查看上方的完整输出内容")
    else:
        print("❌ 测试失败")
    
    return success

if __name__ == "__main__":
    main() 