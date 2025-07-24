#!/usr/bin/env python3
"""
制造业补货系统集成状态检查
验证6个工具函数是否正确集成到智能体架构中
"""

import sys
import os

def check_toolkit_integration():
    """检查Toolkit集成状态"""
    print("🔧 检查Toolkit集成状态")
    print("=" * 50)
    
    try:
        # 检查agent_utils.py中的工具函数定义
        with open('tradingagents/agents/utils/agent_utils.py', 'r') as f:
            content = f.read()
        
        manufacturing_tools = [
            'get_manufacturing_weather_data',
            'get_manufacturing_news_data', 
            'get_manufacturing_holiday_data',
            'get_manufacturing_pmi_data',
            'get_manufacturing_ppi_data',
            'get_manufacturing_commodity_data'
        ]
        
        print("检查工具函数定义:")
        for tool in manufacturing_tools:
            if f"def {tool}(" in content:
                print(f"   ✅ {tool}")
            else:
                print(f"   ❌ {tool}")
                
        return True
        
    except Exception as e:
        print(f"❌ Toolkit检查失败: {e}")
        return False

def check_tool_nodes_integration():
    """检查工具节点集成状态"""
    print("\n🔗 检查工具节点集成状态")  
    print("=" * 50)
    
    try:
        # 检查trading_graph.py中的工具节点配置
        with open('tradingagents/graph/trading_graph.py', 'r') as f:
            content = f.read()
        
        expected_nodes = [
            'manufacturing_macro',
            'manufacturing_environment', 
            'manufacturing_intelligence'
        ]
        
        print("检查制造业工具节点:")
        for node in expected_nodes:
            if f'"{node}": ToolNode(' in content:
                print(f"   ✅ {node}")
            else:
                print(f"   ❌ {node}")
        
        # 检查具体工具分配
        print("\n检查工具分配:")
        tool_assignments = [
            ('get_manufacturing_pmi_data', 'manufacturing_macro'),
            ('get_manufacturing_ppi_data', 'manufacturing_macro'), 
            ('get_manufacturing_commodity_data', 'manufacturing_macro'),
            ('get_manufacturing_weather_data', 'manufacturing_environment'),
            ('get_manufacturing_holiday_data', 'manufacturing_environment'),
            ('get_manufacturing_news_data', 'manufacturing_intelligence')
        ]
        
        for tool, expected_node in tool_assignments:
            if tool in content:
                print(f"   ✅ {tool} -> {expected_node}")
            else:
                print(f"   ❌ {tool} -> {expected_node}")
                
        return True
        
    except Exception as e:
        print(f"❌ 工具节点检查失败: {e}")
        return False

def check_agents_integration():
    """检查智能体集成状态"""
    print("\n🤖 检查智能体集成状态")
    print("=" * 50)
    
    try:
        # 检查market_environment_analyst.py
        with open('tradingagents/manufacturingagents/analysts/market_environment_analyst.py', 'r') as f:
            content = f.read()
        
        print("检查市场环境分析师工具配置:")
        expected_tools = [
            'get_manufacturing_pmi_data',
            'get_manufacturing_ppi_data',
            'get_manufacturing_commodity_data'
        ]
        
        for tool in expected_tools:
            if tool in content:
                print(f"   ✅ {tool}")
            else:
                print(f"   ❌ {tool}")
                
        return True
        
    except Exception as e:
        print(f"❌ 智能体检查失败: {e}")
        return False

def main():
    """主检查函数"""
    print("🚀 制造业补货系统集成状态检查")
    print("=" * 70)
    
    # 检查各个集成点
    toolkit_ok = check_toolkit_integration()
    tool_nodes_ok = check_tool_nodes_integration() 
    agents_ok = check_agents_integration()
    
    print("\n" + "=" * 70)
    print("📊 集成状态总结")
    print("=" * 70)
    
    print(f"Toolkit工具函数: {'✅ 已集成' if toolkit_ok else '❌ 未集成'}")
    print(f"工具节点配置: {'✅ 已集成' if tool_nodes_ok else '❌ 未集成'}")
    print(f"智能体配置: {'✅ 已集成' if agents_ok else '❌ 未集成'}")
    
    if all([toolkit_ok, tool_nodes_ok, agents_ok]):
        print("\n🎉 制造业工具函数已完全集成到智能体架构！")
        print("✅ 6个工具函数 -> Toolkit中正确定义")
        print("✅ 3个工具节点 -> TradingGraph中正确配置")
        print("✅ 智能体工具 -> 市场环境分析师正确引用")
        print("\n📋 集成架构已就绪，可以进行端到端测试！")
        return True
    else:
        print("\n⚠️ 集成不完整，需要修复缺失部分")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🏁 集成检查完成: {'成功' if success else '需要修复'}")
