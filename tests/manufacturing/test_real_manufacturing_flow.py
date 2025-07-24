#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实制造业补货决策流程测试
调用真实的智能体和LLM进行分析，获取真实的分析结果
"""

import sys
import os
from pathlib import Path
import traceback
from datetime import datetime
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_real_manufacturing_analysis():
    """测试真实的制造业分析流程"""
    print("🚀 开始真实制造业分析流程测试")
    print("=" * 80)
    
    try:
        # 1. 导入必要的模块
        from manufacturingagents.llm_adapters import ChatDashScope
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        from manufacturingagents.manufacturingagents import (
            create_market_environment_analyst,
            create_trend_prediction_analyst,
            create_news_analyst,
            create_sentiment_insight_analyst,
            create_optimistic_advisor,
            create_cautious_advisor,
            create_decision_coordinator,
            create_risk_assessment_team,
            ManufacturingState
        )
        
        # 2. 创建真实的LLM实例
        print("🔧 创建LLM实例...")
        llm = ChatDashScope(model="qwen-turbo")
        print("✅ LLM实例创建成功")
        
        # 3. 创建工具包
        print("🔧 创建工具包...")
        toolkit = Toolkit()
        print("✅ 工具包创建成功")
        
        # 4. 创建智能体
        print("\n🤖 创建智能体团队...")
        
        market_analyst = create_market_environment_analyst(llm, toolkit)
        print("✅ 市场环境分析师创建完成")
        
        trend_analyst = create_trend_prediction_analyst(llm, toolkit)
        print("✅ 趋势预测分析师创建完成")
        
        news_analyst = create_news_analyst(llm, toolkit)
        print("✅ 新闻资讯分析师创建完成")
        
        sentiment_analyst = create_sentiment_insight_analyst(llm, toolkit)
        print("✅ 舆情洞察分析师创建完成")
        
        # 5. 准备测试用例
        test_case = {
            "product_type": "空调",
            "company_name": "美的",
            "analysis_date": "2024-07-20",
            "target_quarter": "2024Q3",
            "sender": "system",
            "messages": [("human", "分析美的品牌的空调在2024Q3的补货策略")]
        }
        
        print(f"\n📊 测试用例: {test_case['company_name']} {test_case['product_type']} {test_case['target_quarter']}")
        print("=" * 50)
        
        # 6. 逐个调用智能体进行真实分析
        state = test_case.copy()
        
        # 调用市场环境分析师
        print("\n🌍 调用市场环境分析师...")
        print("📝 发送给LLM的消息:")
        print(f"   产品类型: {state['product_type']}")
        print(f"   公司名称: {state['company_name']}")
        print(f"   分析日期: {state['analysis_date']}")
        
        try:
            # 实际调用智能体节点
            start_time = time.time()
            result = market_analyst(state)
            end_time = time.time()
            
            print(f"⏱️ 分析耗时: {end_time - start_time:.2f}秒")
            
            if "market_environment_report" in result:
                report = result["market_environment_report"]
                print("✅ 市场环境分析完成!")
                print(f"📄 报告长度: {len(report)} 字符")
                print("📋 报告内容:")
                print("-" * 40)
                print(report[:500] + "..." if len(report) > 500 else report)
                print("-" * 40)
                state.update(result)
            else:
                print("❌ 市场环境分析失败，未生成报告")
                
        except Exception as e:
            print(f"❌ 市场环境分析出错: {e}")
            traceback.print_exc()
        
        # 调用趋势预测分析师
        print("\n📈 调用趋势预测分析师...")
        try:
            start_time = time.time()
            result = trend_analyst(state)
            end_time = time.time()
            
            print(f"⏱️ 分析耗时: {end_time - start_time:.2f}秒")
            
            if "trend_prediction_report" in result:
                report = result["trend_prediction_report"]
                print("✅ 趋势预测分析完成!")
                print(f"📄 报告长度: {len(report)} 字符")
                print("📋 报告内容:")
                print("-" * 40)
                print(report[:500] + "..." if len(report) > 500 else report)
                print("-" * 40)
                state.update(result)
            else:
                print("❌ 趋势预测分析失败，未生成报告")
                
        except Exception as e:
            print(f"❌ 趋势预测分析出错: {e}")
            traceback.print_exc()
        
        # 调用新闻分析师
        print("\n📰 调用新闻资讯分析师...")
        try:
            start_time = time.time()
            result = news_analyst(state)
            end_time = time.time()
            
            print(f"⏱️ 分析耗时: {end_time - start_time:.2f}秒")
            
            if "industry_news_report" in result:
                report = result["industry_news_report"]
                print("✅ 新闻资讯分析完成!")
                print(f"📄 报告长度: {len(report)} 字符")
                print("📋 报告内容:")
                print("-" * 40)
                print(report[:500] + "..." if len(report) > 500 else report)
                print("-" * 40)
                state.update(result)
            else:
                print("❌ 新闻资讯分析失败，未生成报告")
                
        except Exception as e:
            print(f"❌ 新闻资讯分析出错: {e}")
            traceback.print_exc()
        
        # 调用舆情分析师
        print("\n💭 调用舆情洞察分析师...")
        try:
            start_time = time.time()
            result = sentiment_analyst(state)
            end_time = time.time()
            
            print(f"⏱️ 分析耗时: {end_time - start_time:.2f}秒")
            
            if "consumer_insight_report" in result:
                report = result["consumer_insight_report"]
                print("✅ 舆情洞察分析完成!")
                print(f"📄 报告长度: {len(report)} 字符")
                print("📋 报告内容:")
                print("-" * 40)
                print(report[:500] + "..." if len(report) > 500 else report)
                print("-" * 40)
                state.update(result)
            else:
                print("❌ 舆情洞察分析失败，未生成报告")
                
        except Exception as e:
            print(f"❌ 舆情洞察分析出错: {e}")
            traceback.print_exc()
        
        # 7. 显示最终的分析状态
        print("\n" + "=" * 80)
        print("📊 完整分析结果摘要")
        print("=" * 80)
        
        reports = [
            ("市场环境报告", "market_environment_report"),
            ("趋势预测报告", "trend_prediction_report"),
            ("新闻资讯报告", "industry_news_report"),
            ("舆情洞察报告", "consumer_insight_report")
        ]
        
        for report_name, report_key in reports:
            if report_key in state:
                report = state[report_key]
                print(f"\n📋 {report_name} ({len(report)} 字符):")
                print("-" * 50)
                print(report)
                print("-" * 50)
            else:
                print(f"\n❌ {report_name}: 未生成")
        
        # 8. 分析总结
        generated_reports = sum(1 for _, key in reports if key in state)
        print(f"\n📈 分析完成度: {generated_reports}/{len(reports)} 个报告生成成功")
        
        if generated_reports >= 3:
            print("🎉 分析流程基本成功！大部分智能体正常工作。")
            return True
        elif generated_reports >= 1:
            print("⚠️ 分析流程部分成功，但存在一些问题。")
            return True
        else:
            print("❌ 分析流程失败，智能体未能正常工作。")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现严重错误: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_manufacturing_analysis()
    print(f"\n🎯 测试结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1) 