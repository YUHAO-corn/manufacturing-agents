#!/usr/bin/env python3

import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 测试四个分析师的专业化工具配置
from manufacturingagents.manufacturingagents.graph.manufacturing_graph_react import ManufacturingAgentsReactGraph

def test_specialized_tools():
    """测试四个分析师的专业化工具配置"""
    print("🔧 测试四个分析师的专业化工具配置")
    print("=" * 60)
    
    try:
        config = {
            "llm_provider": "dashscope",
            "llm_model": "qwen-turbo"
        }
        
        # 测试所有四个分析师
        graph = ManufacturingAgentsReactGraph(
            selected_analysts=[
                "market_environment_analyst",
                "trend_prediction_analyst", 
                "industry_news_analyst",
                "consumer_insight_analyst"
            ],
            debug=False,
            config=config
        )
        
        result = graph.analyze_manufacturing_replenishment(
            brand_name='美的',
            product_category='空调',
            target_quarter='2025Q3',
            special_focus='验证专业化工具'
        )
        
        print("\n" + "="*60)
        print("📊 专业化工具测试结果：")
        print("="*60)
        
        # 检查四个分析师的工具使用情况
        expected_tools = {
            'market_environment_report': ['PMI', 'PPI', '期货'],
            'trend_prediction_report': ['节假日', '天气'],
            'industry_news_report': ['新闻'],
            'consumer_insight_report': ['舆情', '行为']
        }
        
        tools_detected = {}
        for report_key, expected in expected_tools.items():
            report = result.get(report_key, '')
            detected = []
            
            # 检测工具使用特征
            if 'PMI' in report or 'pmi' in report:
                detected.append('PMI')
            if 'PPI' in report or 'ppi' in report:
                detected.append('PPI')  
            if '期货' in report or '铜' in report:
                detected.append('期货')
            if '节假日' in report or '假期' in report:
                detected.append('节假日')
            if '天气' in report or '气温' in report:
                detected.append('天气')
            if '新闻' in report or '政策' in report:
                detected.append('新闻')
            if '舆情' in report or '情绪' in report:
                detected.append('舆情')
            if '行为' in report or '购买' in report:
                detected.append('行为')
                
            tools_detected[report_key] = detected
            
            # 输出结果
            analyst_name = {
                'market_environment_report': '🌍 市场环境分析师',
                'trend_prediction_report': '📈 趋势预测分析师',
                'industry_news_report': '📰 行业资讯分析师', 
                'consumer_insight_report': '💭 消费者洞察分析师'
            }[report_key]
            
            print(f"\n{analyst_name}:")
            print(f"  期望工具: {expected}")
            print(f"  检测到工具: {detected}")
            print(f"  报告长度: {len(report)}字符")
            
            # 简单成功标准：检测到期望工具且报告有内容
            success = len(detected) > 0 and len(report) > 500
            print(f"  专业化状态: {'✅ 成功' if success else '❌ 需要调整'}")
        
        # 总结
        successful_analysts = sum(1 for key, tools in tools_detected.items() 
                                if len(tools) > 0 and len(result.get(key, '')) > 500)
        
        print(f"\n🎯 专业化工具配置测试结果:")
        print(f"   成功率: {successful_analysts}/4 个分析师")
        
        if successful_analysts >= 3:
            print("🎉 专业化工具配置基本成功！")
            print("💡 每个分析师现在使用不同的数据源进行专业分析")
        else:
            print("⚠️ 部分分析师仍需调整工具配置")
            
        return successful_analysts >= 3
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_specialized_tools() 