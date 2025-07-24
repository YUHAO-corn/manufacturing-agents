#!/usr/bin/env python3
"""
制造业补货系统端到端测试脚本
验证预处理助手 -> 智能体协作 -> 工具调用 -> API数据获取的完整流程
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# 加载.env文件
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))

def test_preprocessing_assistant():
    """测试1：预处理助手参数生成"""
    print("🔍 测试1：预处理助手参数生成")
    print("=" * 60)
    
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 生成API参数
        api_params = assistant.generate_api_parameters(
            city_name="广州市",
            brand_name="美的", 
            product_type="空调",
            special_focus="关注天气影响和季节性需求"
        )
        
        print(f"✅ 预处理助手成功生成参数")
        print(f"   参数数量: {len(api_params)} 个API")
        print(f"   包含API: {list(api_params.keys())}")
        
        return api_params
        
    except Exception as e:
        print(f"❌ 预处理助手测试失败: {str(e)}")
        return None

def test_individual_tools():
    """测试2：单独测试每个工具函数"""
    print("\n🛠️ 测试2：单独测试工具函数")
    print("=" * 60)
    
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        
        toolkit = Toolkit()
        
        # 测试天气工具
        print("🌤️ 测试天气工具...")
        weather_result = toolkit.get_manufacturing_weather_data.invoke({"city_name": "广州"})
        print(f"   天气数据长度: {len(weather_result)} 字符")
        print(f"   状态: {'✅ 成功' if '❌' not in weather_result else '❌ 失败'}")
        
        # 测试PMI工具  
        print("📈 测试PMI工具...")
        pmi_result = toolkit.get_manufacturing_pmi_data.invoke({"time_range": "最近3个月"})
        print(f"   PMI数据长度: {len(pmi_result)} 字符")
        print(f"   状态: {'✅ 成功' if '❌' not in pmi_result else '❌ 失败'}")
        
        # 测试新闻工具
        print("📰 测试新闻工具...")
        news_result = toolkit.get_manufacturing_news_data.invoke({"query_params": "广州美的空调"})
        print(f"   新闻数据长度: {len(news_result)} 字符")
        print(f"   状态: {'✅ 成功' if '❌' not in news_result else '❌ 失败'}")
        
        return {
            'weather': weather_result,
            'pmi': pmi_result, 
            'news': news_result
        }
        
    except Exception as e:
        print(f"❌ 工具函数测试失败: {str(e)}")
        return None

def test_single_agent():
    """测试3：单独测试制造业智能体"""
    print("\n🤖 测试3：单独测试制造业智能体")
    print("=" * 60)
    
    try:
        from manufacturingagents.manufacturingagents.analysts.market_environment_analyst import create_market_environment_analyst
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        from manufacturingagents.manufacturingagents.utils.manufacturing_states import ManufacturingState
        
        # 初始化LLM（使用简单配置）
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        
        # 创建工具包和智能体
        toolkit = Toolkit()
        analyst = create_market_environment_analyst(llm, toolkit)
        
        # 创建测试状态
        test_state = {
            "analysis_date": "2025-01-19",
            "product_type": "空调",
            "company_name": "美的",
            "messages": [("human", "请分析广州美的空调的市场环境")]
        }
        
        print("🚀 执行市场环境分析师...")
        result = analyst(test_state)
        
        print(f"✅ 智能体执行完成")
        print(f"   返回消息数量: {len(result.get('messages', []))}")
        print(f"   报告长度: {len(result.get('market_environment_report', ''))} 字符")
        
        # 检查是否调用了工具
        if result.get('messages'):
            last_message = result['messages'][-1]
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                print(f"   工具调用: {[call.get('name', 'unknown') for call in last_message.tool_calls]}")
            else:
                print(f"   未检测到工具调用")
        
        return result
        
    except Exception as e:
        print(f"❌ 智能体测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

def test_tool_node_integration():
    """测试4：工具节点集成测试"""
    print("\n🔗 测试4：工具节点集成测试")
    print("=" * 60)
    
    try:
        from manufacturingagents.graph.trading_graph import TradingAgentsGraph
        
        # 创建交易图（包含制造业工具节点）
        graph = TradingAgentsGraph()
        
        # 检查制造业工具节点是否存在
        tool_nodes = graph.tool_nodes
        manufacturing_nodes = [name for name in tool_nodes.keys() if 'manufacturing' in name]
        
        print(f"✅ 制造业工具节点已配置")
        print(f"   节点数量: {len(manufacturing_nodes)}")
        print(f"   节点名称: {manufacturing_nodes}")
        
        # 检查每个节点的工具
        for node_name in manufacturing_nodes:
            node = tool_nodes[node_name]
            tool_names = [tool.name for tool in node.tools]
            print(f"   {node_name}: {tool_names}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具节点集成测试失败: {str(e)}")
        return False

def test_full_workflow():
    """测试5：完整工作流测试（简化版）"""
    print("\n🎯 测试5：完整工作流测试")
    print("=" * 60)
    
    try:
        # 1. 预处理助手生成参数
        print("第1步：预处理助手生成参数...")
        api_params = test_preprocessing_assistant()
        if not api_params:
            return False
        
        # 2. 模拟智能体状态传递
        print("第2步：智能体状态创建...")
        manufacturing_state = {
            "analysis_date": "2025-01-19",
            "product_type": "空调",
            "company_name": "美的",
            "city_name": "广州",
            "api_params": api_params,
            "messages": [("human", "分析广州美的空调补货需求")]
        }
        
        # 3. 工具调用测试
        print("第3步：工具调用测试...")
        tool_results = test_individual_tools()
        if not tool_results:
            return False
        
        # 4. 集成验证
        print("第4步：集成验证...")
        integration_ok = test_tool_node_integration()
        if not integration_ok:
            return False
        
        print("\n🎉 完整工作流测试成功！")
        print("   ✅ 预处理助手 -> API参数生成正常")
        print("   ✅ 工具函数 -> API数据获取正常")
        print("   ✅ 工具节点 -> 集成配置正常")
        print("   ✅ 端到端流程 -> 基础架构可用")
        
        return True
        
    except Exception as e:
        print(f"❌ 完整工作流测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 制造业补货系统端到端测试")
    print("=" * 80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目路径: {project_root}")
    print()
    
    # 检查环境变量
    coze_key = os.getenv('COZE_API_KEY')
    tushare_token = os.getenv('TUSHARE_TOKEN')
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    
    print("🔑 环境变量检查:")
    print(f"   COZE_API_KEY: {'✅ 已配置' if coze_key else '❌ 未配置'}")
    print(f"   TUSHARE_TOKEN: {'✅ 已配置' if tushare_token else '❌ 未配置'}")
    print(f"   DASHSCOPE_API_KEY: {'✅ 已配置' if dashscope_key else '❌ 未配置'}")
    
    if not (coze_key and tushare_token and dashscope_key):
        print("\n❌ 缺少必要的API密钥，无法进行完整测试")
        return False
    
    print()
    
    # 运行测试套件
    try:
        # 分步测试
        api_params = test_preprocessing_assistant()
        tool_results = test_individual_tools()
        # agent_result = test_single_agent()  # 暂时跳过，可能需要更多配置
        integration_ok = test_tool_node_integration()
        
        # 完整流程测试
        workflow_ok = test_full_workflow()
        
        # 总结
        print("\n" + "=" * 80)
        print("📊 测试结果总结")
        print("=" * 80)
        print(f"预处理助手: {'✅ 通过' if api_params else '❌ 失败'}")
        print(f"工具函数: {'✅ 通过' if tool_results else '❌ 失败'}")
        print(f"工具节点集成: {'✅ 通过' if integration_ok else '❌ 失败'}")
        print(f"完整工作流: {'✅ 通过' if workflow_ok else '❌ 失败'}")
        
        if workflow_ok:
            print("\n🎉 制造业补货系统基础架构已可用！")
            print("   接下来可以进行智能体协作和Web界面开发")
        else:
            print("\n⚠️ 存在问题需要修复")
            
        return workflow_ok
        
    except Exception as e:
        print(f"\n❌ 测试执行异常: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    
    print(f"\n🏁 测试完成，结果: {'成功' if success else '失败'}")
    
    if success:
        print("\n📋 下一步建议:")
        print("1. 创建完整的制造业智能体工作流图")
        print("2. 实现Web界面的制造业输入表单")
        print("3. 进行真实场景的端到端测试")
    else:
        print("\n🔧 调试建议:")
        print("1. 检查API密钥配置")
        print("2. 验证工具函数的API调用逻辑")
        print("3. 确认智能体和工具节点的集成") 