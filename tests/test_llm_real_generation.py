#!/usr/bin/env python3
"""
测试大模型真实生成功能
验证预处理助手能否通过大模型生成预期的API参数
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), 'TradingAgents-CN')
sys.path.insert(0, project_root)

def test_real_llm_generation():
    """测试大模型真实生成功能"""
    print("🎯 测试目标: 验证大模型能否生成预期的API参数（不使用降级方案）")
    print("=" * 70)
    
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        # 初始化预处理助手
        assistant = PreprocessingAssistant(model_provider="dashscope")
        print("✅ PreprocessingAssistant 初始化成功")
        
        # 准备测试输入
        test_cases = [
            {
                "name": "深圳格力空调",
                "input": {
                    "city_name": "深圳市",
                    "brand_name": "格力",
                    "product_type": "变频空调",
                    "special_focus": "关注夏季销售",
                    "current_time": datetime(2025, 7, 19)
                }
            },
            {
                "name": "北京海尔冰箱",
                "input": {
                    "city_name": "北京市",
                    "brand_name": "海尔",
                    "product_type": "智能冰箱",
                    "special_focus": "节能政策",
                    "current_time": datetime(2025, 9, 15)
                }
            }
        ]
        
        success_count = 0
        total_count = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 测试案例 {i}: {test_case['name']}")
            print("-" * 50)
            
            try:
                # 直接调用大模型生成参数（绕过降级方案）
                user_input = {
                    "city_name": test_case["input"]["city_name"],
                    "brand_name": test_case["input"]["brand_name"],
                    "product_type": test_case["input"]["product_type"],
                    "special_focus": test_case["input"]["special_focus"],
                    "current_time": test_case["input"]["current_time"].strftime("%Y-%m-%d")
                }
                
                print(f"🔄 调用大模型生成参数...")
                print(f"   城市: {user_input['city_name']}")
                print(f"   品牌: {user_input['brand_name']}")
                print(f"   产品: {user_input['product_type']}")
                print(f"   关注: {user_input['special_focus']}")
                print(f"   时间: {user_input['current_time']}")
                
                # 直接调用大模型（不使用generate_api_parameters，因为它有降级逻辑）
                print("🔄 正在构建提示词...")
                try:
                    api_params = assistant._call_llm_for_parameters(user_input)
                except Exception as llm_error:
                    print(f"❌ 大模型调用过程出错: {str(llm_error)}")
                    print(f"❌ 错误类型: {type(llm_error).__name__}")
                    
                    # 尝试查看是否是提示词问题
                    try:
                        prompt = assistant._build_prompt(user_input)
                        print(f"✅ 提示词构建成功，长度: {len(prompt)} 字符")
                        print(f"🔍 提示词前200字符: {prompt[:200]}")
                    except Exception as prompt_error:
                        print(f"❌ 提示词构建失败: {str(prompt_error)}")
                    
                    raise llm_error
                
                print("🎉 大模型成功生成参数！")
                
                # 验证参数格式
                if assistant.validate_parameters(api_params):
                    print("✅ 大模型生成的参数格式验证通过")
                    
                    # 验证关键内容
                    expected_checks = [
                        ("天气城市", api_params["weather"]["place"], test_case["input"]["city_name"]),
                        ("品牌查询", api_params["news"]["area_news_query"], test_case["input"]["brand_name"]),
                        ("产品查询", api_params["news"]["area_news_query"], test_case["input"]["product_type"]),
                        ("时间格式", api_params["holiday"]["start_date"], user_input["current_time"]),
                    ]
                    
                    content_valid = True
                    for check_name, actual_value, expected_content in expected_checks:
                        if expected_content.replace("市", "").replace("省", "") in str(actual_value):
                            print(f"  ✅ {check_name}: {actual_value}")
                        else:
                            print(f"  ❌ {check_name}: {actual_value} (期望包含: {expected_content})")
                            content_valid = False
                    
                    if content_valid:
                        print(f"✅ 测试案例 {i} 完全成功 - 大模型生成了预期的参数")
                        success_count += 1
                        
                        # 保存成功的参数到文件
                        filename = f"llm_generated_params_{test_case['name'].replace(' ', '_')}.json"
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(api_params, f, ensure_ascii=False, indent=2)
                        print(f"📄 参数已保存到: {filename}")
                    else:
                        print(f"❌ 测试案例 {i} 内容验证失败")
                else:
                    print(f"❌ 测试案例 {i} 格式验证失败")
                    
            except Exception as e:
                print(f"❌ 测试案例 {i} 失败: {str(e)}")
                print(f"   错误类型: {type(e).__name__}")
                
                # 如果是JSON解析错误，显示原始输出
                if "JSON" in str(e):
                    print("   这可能是大模型输出格式问题，不是降级方案")
        
        print("\n" + "=" * 70)
        print(f"🎯 大模型真实生成测试结果: {success_count}/{total_count} 成功")
        
        if success_count == total_count:
            print("🎉 所有测试成功！大模型能够生成预期的API参数")
            print("✅ 预处理助手的大模型调用功能完全正常")
            return True
        elif success_count > 0:
            print("⚠️ 部分测试成功，大模型有时能生成正确结果")
            print("💡 可能需要调整提示词或处理逻辑")
            return False
        else:
            print("❌ 所有测试失败，大模型无法生成预期结果")
            print("🔧 需要修复大模型调用逻辑")
            return False
            
    except ImportError as e:
        print(f"❌ 导入失败: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始大模型真实生成功能测试")
    print("🎯 目标: 验证大模型能否直接生成预期的API参数（非降级方案）")
    
    success = test_real_llm_generation()
    
    if success:
        print("\n🚀 结论: 预处理助手的大模型调用功能完全可用！")
    else:
        print("\n🔧 结论: 需要进一步优化大模型调用功能")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 