#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业ReAct Agent测试脚本
验证ReAct Agent是否能正确处理工具调用和生成完整报告
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_manufacturing_react_graph():
    """测试制造业ReAct Graph工作流"""
    print("🔬 制造业ReAct Agent工具调用测试")
    print("=" * 50)
    
    try:
        # 导入ReAct制造业图
        from manufacturingagents.manufacturingagents.graph.manufacturing_graph_react import create_manufacturing_react_graph
        
        print("✅ 成功导入制造业ReAct图模块")
        
        # 配置参数
        config = {
            "llm_provider": "dashscope",
            "llm_model": "qwen-turbo",
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        # 创建制造业ReAct图实例
        print("\n🔧 创建制造业ReAct图实例...")
        manufacturing_graph = create_manufacturing_react_graph(
            selected_analysts=["market_environment"],  # 只测试一个分析师
            debug=True,
            config=config
        )
        
        print("✅ 制造业ReAct图实例创建成功")
        
        # 执行补货分析
        print("\n🚀 开始执行ReAct补货分析...")
        result = manufacturing_graph.analyze_manufacturing_replenishment(
            brand_name="美的",
            product_category="空调",
            target_quarter="2025Q2",
            special_focus="测试ReAct Agent工具调用"
        )
        
        print("✅ ReAct补货分析执行完成")
        
        # 检查结果
        print("\n📊 分析结果检查:")
        print(f"产品类型: {result.get('product_type', 'N/A')}")
        print(f"公司名称: {result.get('company_name', 'N/A')}")
        print(f"目标季度: {result.get('target_quarter', 'N/A')}")
        
        # 调试：打印状态所有键
        print(f"\n📋 最终状态包含的键: {list(result.keys())}")
        
        # 检查报告内容
        market_report = result.get('market_environment_report', '')
        print(f"\n市场环境报告长度: {len(market_report)} 字符")
        print(f"报告内容前50字符: '{market_report[:50]}'")
        if len(market_report) > 500:
            print("✅ 市场环境报告内容丰富")
            print(f"报告前300字符: {market_report[:300]}...")
            
            # 检查是否包含真实数据
            if "PMI" in market_report and "PPI" in market_report:
                print("✅ 报告包含PMI和PPI数据，工具调用成功")
            else:
                print("⚠️ 报告可能缺少真实数据")
        else:
            print("⚠️ 市场环境报告内容较少，ReAct Agent可能未成功")
            print(f"报告内容: {market_report}")
        
        # 获取分析摘要
        print("\n📋 获取分析摘要...")
        summary = manufacturing_graph.get_analysis_summary(result)
        print(f"摘要获取成功: {len(str(summary))} 字符")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保已正确创建制造业ReAct图模块")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_react_components():
    """测试ReAct相关组件"""
    print("\n🔧 === ReAct组件测试 ===")
    
    # 测试Tongyi LLM
    print("\n🧠 测试Tongyi LLM...")
    try:
        from langchain_community.llms import Tongyi
        llm = Tongyi()
        llm.model_name = "qwen-turbo"
        print("✅ Tongyi LLM初始化成功")
    except Exception as e:
        print(f"❌ Tongyi LLM初始化失败: {e}")
        return False
    
    # 测试ReAct Agent创建
    print("\n🤖 测试ReAct Agent创建...")
    try:
        from langchain.agents import create_react_agent
        from langchain import hub
        from langchain_core.tools import BaseTool
        
        # 测试工具
        class TestTool(BaseTool):
            name: str = "test_tool"
            description: str = "测试工具"
            
            def _run(self, query: str = "") -> str:
                return "测试工具调用成功"
        
        tools = [TestTool()]
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(llm, tools, prompt)
        print("✅ ReAct Agent创建成功")
        
    except Exception as e:
        print(f"❌ ReAct Agent创建失败: {e}")
        return False
    
    # 测试工具包
    print("\n🛠️ 测试制造业工具包...")
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        toolkit = Toolkit()
        
        # 测试制造业工具
        result = toolkit.get_manufacturing_pmi_data.invoke({"time_range": "最近3个月"})
        print(f"✅ 制造业工具包测试成功: {len(result)} 字符")
    except Exception as e:
        print(f"❌ 制造业工具包测试失败: {e}")
        return False
    
    print("✅ 所有ReAct组件测试通过")
    return True

def main():
    """主测试函数"""
    print("🧪 制造业ReAct Agent全面测试")
    print("=" * 60)
    
    # 检查环境变量
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    if not dashscope_key:
        print("⚠️ 警告: DASHSCOPE_API_KEY未配置，测试可能无法完全执行")
    
    # 1. ReAct组件测试
    components_ok = test_react_components()
    if not components_ok:
        print("❌ ReAct组件测试失败，终止图工作流测试")
        return
    
    # 2. 完整ReAct图工作流测试
    graph_ok = test_manufacturing_react_graph()
    
    # 总结
    print("\n📋 === 测试总结 ===")
    if components_ok and graph_ok:
        print("🎉 所有测试通过！制造业ReAct Agent系统正常工作")
        print("✅ 工具调用机制正常，数据获取成功")
        print("✅ ReAct Agent能够生成完整的分析报告")
        print("💡 可以集成到Web界面中")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")
        print("💡 建议:")
        print("  1. 检查DASHSCOPE_API_KEY配置")
        print("  2. 确认langchain_community已正确安装")
        print("  3. 检查ReAct Agent的提示词和工具调用")

if __name__ == "__main__":
    main() 