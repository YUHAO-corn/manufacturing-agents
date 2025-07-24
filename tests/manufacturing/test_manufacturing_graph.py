#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业LangGraph工作流测试脚本
验证新的工作流系统是否能正确处理工具调用和多轮对话
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_manufacturing_graph():
    """测试制造业LangGraph工作流"""
    print("🏭 制造业LangGraph工作流测试")
    print("=" * 50)
    
    try:
        # 导入制造业图
        from manufacturingagents.manufacturingagents.graph.manufacturing_graph import create_manufacturing_graph
        
        print("✅ 成功导入制造业图模块")
        
        # 配置参数
        config = {
            "llm_provider": "dashscope",
            "llm_model": "qwen-turbo",
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        # 创建制造业图实例
        print("\n🔧 创建制造业图实例...")
        manufacturing_graph = create_manufacturing_graph(
            selected_analysts=["market_environment"],  # 先只测试一个分析师
            debug=True,
            config=config
        )
        
        print("✅ 制造业图实例创建成功")
        
        # 执行补货分析
        print("\n🚀 开始执行补货分析...")
        result = manufacturing_graph.analyze_manufacturing_replenishment(
            brand_name="美的",
            product_category="空调",
            target_quarter="2025Q2",
            special_focus="关注工具调用和多轮对话"
        )
        
        print("✅ 补货分析执行完成")
        
        # 检查结果
        print("\n📊 分析结果检查:")
        print(f"产品类型: {result.get('product_type', 'N/A')}")
        print(f"公司名称: {result.get('company_name', 'N/A')}")
        print(f"目标季度: {result.get('target_quarter', 'N/A')}")
        
        # 检查报告内容
        market_report = result.get('market_environment_report', '')
        print(f"\n市场环境报告长度: {len(market_report)} 字符")
        if len(market_report) > 100:
            print("✅ 市场环境报告内容丰富")
            print(f"报告前200字符: {market_report[:200]}...")
        else:
            print("⚠️ 市场环境报告内容较少，可能工具调用未成功")
        
        # 检查消息历史
        messages = result.get('messages', [])
        print(f"\n消息历史数量: {len(messages)}")
        
        # 检查工具调用痕迹
        tool_call_found = False
        for i, msg in enumerate(messages):
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"✅ 发现工具调用在消息 {i}: {len(msg.tool_calls)} 个工具")
                tool_call_found = True
        
        if not tool_call_found:
            print("⚠️ 未发现工具调用，可能需要进一步调试")
        
        # 获取分析摘要
        print("\n📋 获取分析摘要...")
        summary = manufacturing_graph.get_analysis_summary(result)
        print(f"摘要获取成功: {len(str(summary))} 字符")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保已正确创建制造业图模块")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """测试各个组件的独立功能"""
    print("\n🔧 === 组件独立测试 ===")
    
    # 测试LLM初始化
    print("\n🧠 测试LLM初始化...")
    try:
        from manufacturingagents.llm_adapters.dashscope_adapter import ChatDashScope
        llm = ChatDashScope(model="qwen-turbo")
        print("✅ LLM初始化成功")
    except Exception as e:
        print(f"❌ LLM初始化失败: {e}")
        return False
    
    # 测试工具包
    print("\n🛠️ 测试工具包...")
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        toolkit = Toolkit()
        
        # 测试一个制造业工具
        result = toolkit.get_manufacturing_pmi_data("最近3个月")
        print(f"✅ 工具包测试成功: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 工具包测试失败: {e}")
        return False
    
    # 测试智能体创建
    print("\n🤖 测试智能体创建...")
    try:
        from manufacturingagents.manufacturingagents.analysts.market_environment_analyst import create_market_environment_analyst
        analyst = create_market_environment_analyst(llm, toolkit)
        print("✅ 智能体创建成功")
    except Exception as e:
        print(f"❌ 智能体创建失败: {e}")
        return False
    
    # 测试工具节点
    print("\n🔗 测试工具节点...")
    try:
        from langgraph.prebuilt import ToolNode
        
        tools = [
            toolkit.get_manufacturing_pmi_data,
            toolkit.get_manufacturing_ppi_data,
        ]
        tool_node = ToolNode(tools)
        print("✅ 工具节点创建成功")
    except Exception as e:
        print(f"❌ 工具节点创建失败: {e}")
        return False
    
    print("✅ 所有组件测试通过")
    return True

def main():
    """主测试函数"""
    print("🧪 制造业LangGraph工作流全面测试")
    print("=" * 60)
    
    # 检查环境变量
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    if not dashscope_key:
        print("⚠️ 警告: DASHSCOPE_API_KEY未配置，测试可能无法完全执行")
    
    # 1. 组件独立测试
    components_ok = test_individual_components()
    if not components_ok:
        print("❌ 组件测试失败，终止图工作流测试")
        return
    
    # 2. 完整图工作流测试
    graph_ok = test_manufacturing_graph()
    
    # 总结
    print("\n📋 === 测试总结 ===")
    if components_ok and graph_ok:
        print("🎉 所有测试通过！制造业LangGraph工作流系统正常")
        print("💡 现在可以集成到Web界面中")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")
        print("💡 建议:")
        print("  1. 检查API密钥配置")
        print("  2. 确认所有依赖模块正确导入")
        print("  3. 检查LangGraph和智能体的实现")

if __name__ == "__main__":
    main() 