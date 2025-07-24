#!/usr/bin/env python3

import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 测试四个分析师的ReAct工作流
from manufacturingagents.manufacturingagents.graph.manufacturing_graph_react import ManufacturingAgentsReactGraph

def test_four_analysts():
    print("🚀 四个分析师ReAct工作流测试")
    print("=" * 60)
    
    try:
        # 测试配置
        config = {
            "llm_provider": "dashscope",
            "llm_model": "qwen-turbo"
        }
        
        print("🔧 第1步：测试单个分析师（市场环境）")
        # 测试单个分析师
        graph_single = ManufacturingAgentsReactGraph(
            selected_analysts=["market_environment_analyst"],
            debug=False,
            config=config
        )
        
        result_single = graph_single.analyze_manufacturing_replenishment(
            brand_name='美的',
            product_category='空调',
            target_quarter='2025Q3',
            special_focus='关注季节性因素'
        )
        
        print(f"✅ 单个分析师测试完成")
        print(f"📊 报告字段: {list(result_single.keys())}")
        market_report_len = len(result_single.get('market_environment_report', ''))
        print(f"📝 市场环境报告长度: {market_report_len}")
        
        print(f"\n🔧 第2步：测试两个分析师（市场环境+趋势预测）")
        # 测试两个分析师
        graph_double = ManufacturingAgentsReactGraph(
            selected_analysts=["market_environment_analyst", "trend_prediction_analyst"],
            debug=False,
            config=config
        )
        
        result_double = graph_double.analyze_manufacturing_replenishment(
            brand_name='美的',
            product_category='空调',
            target_quarter='2025Q3',
            special_focus='关注季节性因素'
        )
        
        print(f"✅ 两个分析师测试完成")
        market_report_len2 = len(result_double.get('market_environment_report', ''))
        trend_report_len = len(result_double.get('trend_prediction_report', ''))
        print(f"📝 市场环境报告长度: {market_report_len2}")
        print(f"📝 趋势预测报告长度: {trend_report_len}")
        
        print(f"\n🔧 第3步：测试四个分析师（完整团队）")
        # 测试四个分析师
        graph_full = ManufacturingAgentsReactGraph(
            selected_analysts=[
                "market_environment_analyst", 
                "trend_prediction_analyst",
                "industry_news_analyst",
                "consumer_insight_analyst"
            ],
            debug=False,
            config=config
        )
        
        result_full = graph_full.analyze_manufacturing_replenishment(
            brand_name='美的',
            product_category='空调',
            target_quarter='2025Q3',
            special_focus='关注原材料价格波动和消费者需求变化'
        )
        
        print(f"✅ 四个分析师测试完成")
        print(f"📊 完整报告字段: {list(result_full.keys())}")
        
        # 检查四个报告
        reports = [
            ('市场环境', 'market_environment_report'),
            ('趋势预测', 'trend_prediction_report'), 
            ('行业资讯', 'industry_news_report'),
            ('消费者洞察', 'consumer_insight_report')
        ]
        
        total_length = 0
        for name, key in reports:
            report_content = result_full.get(key, '')
            report_len = len(report_content)
            total_length += report_len
            status = "✅" if report_len > 100 else "❌"
            print(f"📝 {status} {name}报告长度: {report_len}")
        
        print(f"\n🎯 测试结果总结:")
        print(f"   📊 单个分析师报告: {market_report_len} 字符")
        print(f"   📊 两个分析师报告: {market_report_len2 + trend_report_len} 字符")
        print(f"   📊 四个分析师报告: {total_length} 字符")
        
        # 成功标准
        success_criteria = [
            market_report_len > 1000,
            trend_report_len > 1000,
            len(result_full.get('industry_news_report', '')) > 1000,
            len(result_full.get('consumer_insight_report', '')) > 1000
        ]
        
        if all(success_criteria):
            print(f"\n🎉 四个分析师ReAct工作流测试完全成功！")
            print(f"💡 每个分析师都生成了 >1000 字符的专业报告")
            print(f"🔗 状态传递正常，工作流运行稳定")
            print(f"🌐 现在可以在前端选择四个分析师进行分析了")
        else:
            print(f"\n⚠️ 测试结果有些分析师报告过短，需要检查")
            for i, (name, _) in enumerate(reports):
                if not success_criteria[i]:
                    print(f"   ❌ {name}分析师报告过短")
        
        return all(success_criteria)
        
    except Exception as e:
        print(f"❌ 四个分析师测试失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_four_analysts() 