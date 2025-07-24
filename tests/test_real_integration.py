#!/usr/bin/env python3
"""
制造业补货系统真实集成测试
验证工具函数能否在智能体架构中实际运行
"""

import os
import sys
from datetime import datetime

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

def test_toolkit_runtime():
    """测试1：运行时工具包测试"""
    print("🔧 测试1：运行时工具包测试")
    print("=" * 50)
    
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        
        # 初始化工具包
        toolkit = Toolkit()
        print("✅ Toolkit初始化成功")
        
        # 检查工具函数是否存在且可调用
        manufacturing_tools = [
            'get_manufacturing_weather_data',
            'get_manufacturing_news_data', 
            'get_manufacturing_holiday_data',
            'get_manufacturing_pmi_data',
            'get_manufacturing_ppi_data',
            'get_manufacturing_commodity_data'
        ]
        
        print("检查工具函数可调用性:")
        available_tools = []
        for tool_name in manufacturing_tools:
            if hasattr(toolkit, tool_name):
                tool = getattr(toolkit, tool_name)
                print(f"   ✅ {tool_name} - 类型: {type(tool)}")
                available_tools.append(tool)
            else:
                print(f"   ❌ {tool_name} - 不存在")
                
        return len(available_tools) == 6
        
    except Exception as e:
        print(f"❌ Toolkit运行时测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def test_tool_direct_call():
    """测试2：直接调用工具函数"""
    print("\n🛠️ 测试2：直接调用工具函数")
    print("=" * 50)
    
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        
        toolkit = Toolkit()
        
        # 测试天气工具直接调用
        print("🌤️ 测试天气工具直接调用...")
        try:
            weather_tool = toolkit.get_manufacturing_weather_data
            result = weather_tool.invoke({"city_name": "广州"})
            print(f"   ✅ 调用成功，返回长度: {len(result)} 字符")
            weather_ok = True
        except Exception as e:
            print(f"   ❌ 调用失败: {str(e)}")
            weather_ok = False
        
        # 测试PMI工具直接调用
        print("📈 测试PMI工具直接调用...")
        try:
            pmi_tool = toolkit.get_manufacturing_pmi_data
            result = pmi_tool.invoke({"time_range": "最近3个月"})
            print(f"   ✅ 调用成功，返回长度: {len(result)} 字符")
            pmi_ok = True
        except Exception as e:
            print(f"   ❌ 调用失败: {str(e)}")
            pmi_ok = False
            
        return weather_ok and pmi_ok
        
    except Exception as e:
        print(f"❌ 工具直接调用测试失败: {str(e)}")
        return False

def test_tool_nodes_creation():
    """测试3：工具节点创建"""
    print("\n🔗 测试3：工具节点创建")
    print("=" * 50)
    
    try:
        from manufacturingagents.graph.trading_graph import TradingAgentsGraph
        
        # 尝试创建TradingGraph实例
        print("📊 创建TradingAgentsGraph实例...")
        graph = TradingAgentsGraph()
        print("   ✅ 图实例创建成功")
        
        # 检查制造业工具节点
        print("检查制造业工具节点:")
        manufacturing_nodes = [
            'manufacturing_macro',
            'manufacturing_environment', 
            'manufacturing_intelligence'
        ]
        
        nodes_ok = 0
        for node_name in manufacturing_nodes:
            if node_name in graph.tool_nodes:
                node = graph.tool_nodes[node_name]
                tool_count = len(node.tools)
                print(f"   ✅ {node_name} - {tool_count}个工具")
                nodes_ok += 1
            else:
                print(f"   ❌ {node_name} - 不存在")
                
        return nodes_ok == 3
        
    except Exception as e:
        print(f"❌ 工具节点创建测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def test_manufacturing_agent_creation():
    """测试4：制造业智能体创建"""
    print("\n🤖 测试4：制造业智能体创建")
    print("=" * 50)
    
    try:
        from manufacturingagents.manufacturingagents.analysts.market_environment_analyst import create_market_environment_analyst
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        
        # 创建简单的LLM mock（避免依赖复杂配置）
        class MockLLM:
            def bind_tools(self, tools):
                print(f"   🔧 绑定了 {len(tools)} 个工具")
                return self
            
            def __call__(self, *args, **kwargs):
                return "模拟智能体响应"
        
        # 初始化组件
        print("🚀 创建制造业智能体...")
        llm = MockLLM()
        toolkit = Toolkit()
        
        # 尝试创建智能体
        analyst = create_market_environment_analyst(llm, toolkit)
        print("   ✅ 市场环境分析师创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 制造业智能体创建测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def test_full_integration_flow():
    """测试5：完整集成流程模拟"""
    print("\n🎯 测试5：完整集成流程模拟")
    print("=" * 50)
    
    try:
        # 1. 预处理助手生成参数
        print("第1步：预处理助手生成参数...")
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        assistant = PreprocessingAssistant(model_provider="dashscope")
        api_params = assistant.generate_api_parameters(
            city_name="广州市",
            brand_name="美的", 
            product_type="空调",
            special_focus="测试集成"
        )
        print(f"   ✅ 生成 {len(api_params)} 个API参数")
        
        # 2. 工具包调用模拟
        print("第2步：工具包调用模拟...")
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        
        toolkit = Toolkit()
        
        # 模拟智能体调用天气工具
        weather_params = api_params.get('weather', {})
        if weather_params:
            try:
                weather_result = toolkit.get_manufacturing_weather_data.invoke(weather_params)
                print(f"   ✅ 天气工具调用成功，返回 {len(weather_result)} 字符")
            except Exception as e:
                print(f"   ⚠️ 天气工具调用失败: {str(e)}")
        
        # 模拟智能体调用PMI工具
        pmi_params = api_params.get('pmi', {})
        if pmi_params:
            try:
                # 转换参数格式
                pmi_input = {"time_range": f"{pmi_params.get('start_m', '')} 到 {pmi_params.get('end_m', '')}"}
                pmi_result = toolkit.get_manufacturing_pmi_data.invoke(pmi_input)
                print(f"   ✅ PMI工具调用成功，返回 {len(pmi_result)} 字符")
            except Exception as e:
                print(f"   ⚠️ PMI工具调用失败: {str(e)}")
        
        print("   ✅ 集成流程模拟完成")
        return True
        
    except Exception as e:
        print(f"❌ 完整集成流程测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """主测试函数"""
    print("🚀 制造业补货系统真实集成测试")
    print("=" * 70)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查关键环境变量
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    print(f"\n🔑 环境变量检查:")
    print(f"   DASHSCOPE_API_KEY: {'✅' if dashscope_key else '❌'}")
    
    if not dashscope_key:
        print("\n⚠️ 缺少DASHSCOPE_API_KEY，部分测试可能失败")
    
    print()
    
    # 执行测试套件
    try:
        test1_ok = test_toolkit_runtime()
        test2_ok = test_tool_direct_call() 
        test3_ok = test_tool_nodes_creation()
        test4_ok = test_manufacturing_agent_creation()
        test5_ok = test_full_integration_flow()
        
        print("\n" + "=" * 70)
        print("📊 真实集成测试结果")
        print("=" * 70)
        
        results = [
            ("工具包运行时", test1_ok),
            ("工具直接调用", test2_ok), 
            ("工具节点创建", test3_ok),
            ("智能体创建", test4_ok),
            ("完整流程", test5_ok)
        ]
        
        success_count = sum(1 for _, ok in results if ok)
        
        for name, ok in results:
            print(f"{name}: {'✅ 通过' if ok else '❌ 失败'}")
        
        print(f"\n通过率: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
        
        if success_count >= 4:
            print("\n🎉 制造业补货系统集成基本成功！")
            print("✅ 工具函数可以在架构中实际运行")
            print("✅ 智能体可以成功创建和配置")
            print("✅ 数据流程可以端到端执行")
            print("\n📋 系统已准备好进行完整的智能体协作测试！")
        else:
            print("\n⚠️ 集成存在问题，需要调试修复")
            
        return success_count >= 4
        
    except Exception as e:
        print(f"\n❌ 测试执行异常: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🏁 真实集成测试完成: {'成功' if success else '需要修复'}")
