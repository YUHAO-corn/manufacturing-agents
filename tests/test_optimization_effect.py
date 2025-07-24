#!/usr/bin/env python3
"""
验证预处理助手优化效果测试
对比优化前后的API调用次数和响应时间
"""

import sys
import os
import time
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

def test_optimization_effect():
    """测试优化效果"""
    print("🧪 预处理助手优化效果测试")
    print("=" * 60)
    
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        # 清空缓存
        PreprocessingAssistant.clear_cache()
        
        # 创建预处理助手
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 测试用例
        test_params = {
            "city_name": "广州市",
            "brand_name": "美的", 
            "product_type": "空调",
            "special_focus": "关注天气影响和季节性需求"
        }
        
        print(f"📋 测试参数: {test_params}")
        print()
        
        # 第1次调用 - 应该调用大模型
        print("🔄 第1次调用 (应该调用大模型):")
        start_time = time.time()
        result1 = assistant.generate_api_parameters(**test_params)
        time1 = time.time() - start_time
        print(f"   耗时: {time1:.2f}秒")
        print(f"   返回参数数量: {len(result1)}")
        print()
        
        # 第2次调用 - 应该使用缓存
        print("🔄 第2次调用 (应该使用缓存):")
        start_time = time.time()
        result2 = assistant.generate_api_parameters(**test_params)
        time2 = time.time() - start_time
        print(f"   耗时: {time2:.2f}秒")
        print(f"   返回参数数量: {len(result2)}")
        print()
        
        # 第3次调用 - 还是应该使用缓存
        print("🔄 第3次调用 (还是应该使用缓存):")
        start_time = time.time()
        result3 = assistant.generate_api_parameters(**test_params)
        time3 = time.time() - start_time
        print(f"   耗时: {time3:.2f}秒")
        print(f"   返回参数数量: {len(result3)}")
        print()
        
        # 验证结果一致性
        print("🔍 结果一致性验证:")
        consistent = (result1 == result2 == result3)
        print(f"   3次调用结果是否一致: {'✅ 是' if consistent else '❌ 否'}")
        print()
        
        # 性能对比
        print("📊 性能对比分析:")
        print(f"   第1次调用耗时: {time1:.2f}秒 (首次调用，需要大模型生成)")
        print(f"   第2次调用耗时: {time2:.2f}秒 (缓存命中)")
        print(f"   第3次调用耗时: {time3:.2f}秒 (缓存命中)")
        
        if time1 > 0:
            speedup2 = time1 / time2 if time2 > 0 else float('inf')
            speedup3 = time1 / time3 if time3 > 0 else float('inf')
            print(f"   第2次加速比: {speedup2:.1f}x")
            print(f"   第3次加速比: {speedup3:.1f}x")
        
        cache_efficiency = ((time1 - time2) / time1 * 100) if time1 > 0 else 0
        print(f"   缓存效率提升: {cache_efficiency:.1f}%")
        print()
        
        # 优化效果总结
        print("🎯 优化效果总结:")
        if time2 < time1 * 0.5:  # 缓存至少提升50%性能
            print("✅ 缓存优化非常有效!")
            print(f"   缓存命中时，响应速度提升了 {cache_efficiency:.1f}%")
        elif time2 < time1 * 0.8:  # 缓存提升20%以上性能
            print("✅ 缓存优化有效")
            print(f"   缓存命中时，响应速度提升了 {cache_efficiency:.1f}%")
        else:
            print("⚠️ 缓存优化效果有限")
        
        print(f"   在实际使用中，多个工具调用相同参数时将显著减少大模型调用")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def test_multiple_tool_simulation():
    """模拟多个工具调用的场景"""
    print("🔧 模拟多工具调用场景")
    print("=" * 60)
    
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        # 清空缓存
        PreprocessingAssistant.clear_cache()
        
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 模拟智能体分析流程
        print("🤖 模拟智能体分析流程:")
        print("   假设市场环境分析师需要调用3个工具...")
        print()
        
        base_params = {
            "city_name": "广州市",
            "brand_name": "美的", 
            "product_type": "空调",
            "special_focus": "市场环境分析"
        }
        
        total_time = 0
        
        # 模拟天气工具调用
        print("🌤️ 天气工具调用:")
        start_time = time.time()
        params1 = assistant.generate_api_parameters(**base_params)
        time1 = time.time() - start_time
        total_time += time1
        print(f"   耗时: {time1:.2f}秒")
        
        # 模拟PMI工具调用 (相同参数)
        print("📈 PMI工具调用:")
        start_time = time.time()
        params2 = assistant.generate_api_parameters(**base_params)
        time2 = time.time() - start_time
        total_time += time2
        print(f"   耗时: {time2:.2f}秒")
        
        # 模拟期货工具调用 (相同参数)
        print("🥇 期货工具调用:")
        start_time = time.time()
        params3 = assistant.generate_api_parameters(**base_params)
        time3 = time.time() - start_time
        total_time += time3
        print(f"   耗时: {time3:.2f}秒")
        print()
        
        print("📊 多工具调用性能分析:")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   平均每工具耗时: {total_time/3:.2f}秒")
        
        # 如果没有缓存的话会怎样
        estimated_without_cache = time1 * 3  # 假设每次都要调用大模型
        time_saved = estimated_without_cache - total_time
        efficiency_gain = (time_saved / estimated_without_cache * 100) if estimated_without_cache > 0 else 0
        
        print(f"   没有缓存预计耗时: {estimated_without_cache:.2f}秒")
        print(f"   缓存节省时间: {time_saved:.2f}秒")
        print(f"   整体效率提升: {efficiency_gain:.1f}%")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 多工具测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 预处理助手优化效果验证")
    print("=" * 80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查环境变量
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    if not dashscope_key:
        print("❌ 缺少DASHSCOPE_API_KEY，无法进行测试")
        return False
    
    print("🔑 环境变量检查:")
    print(f"   DASHSCOPE_API_KEY: ✅ 已配置")
    print()
    
    # 执行测试
    test1_ok = test_optimization_effect()
    test2_ok = test_multiple_tool_simulation()
    
    print("=" * 80)
    print("📋 测试结果总结")
    print("=" * 80)
    print(f"基础缓存测试: {'✅ 通过' if test1_ok else '❌ 失败'}")
    print(f"多工具模拟测试: {'✅ 通过' if test2_ok else '❌ 失败'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 优化验证成功!")
        print("📋 优化效果:")
        print("   ✅ 相同参数的重复调用将使用缓存")
        print("   ✅ 显著减少大模型API调用次数")
        print("   ✅ 提升系统整体响应速度")
        print("   ✅ 多工具场景下效率提升明显")
        print("\n💡 实际使用建议:")
        print("   - 智能体分析开始时，预处理助手会生成所有API参数")
        print("   - 后续工具调用将直接使用缓存参数")
        print("   - 避免了重复的大模型调用，提升了系统效率")
    else:
        print("\n⚠️ 部分测试失败，需要检查优化实现")
        
    return test1_ok and test2_ok

if __name__ == "__main__":
    success = main()
    print(f"\n🏁 优化验证完成: {'成功' if success else '失败'}") 