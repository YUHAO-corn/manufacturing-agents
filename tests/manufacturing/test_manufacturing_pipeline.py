#!/usr/bin/env python3
"""
制造业补货决策系统 - 全流程测试脚本
Manufacturing Replenishment Decision System - Full Pipeline Test

测试目标：
1. 验证从用户输入到最终报告的完整流程
2. 评估系统响应速度和报告质量  
3. 检验智能体协作效果
4. 测试真实数据获取能力
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_manufacturing_pipeline():
    """测试制造业管道"""
    print("🚀 制造业补货决策系统全流程测试")
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试用例
    test_case = {
        "brand_name": "美的",
        "product_category": "空调",
        "target_quarter": "2024Q3",
        "special_focus": "夏季高温天气影响",
        "analysts": ["market_environment_analyst", "trend_prediction_analyst"],
        "research_depth": 1
    }
    
    print(f"\n📊 测试场景：{test_case['brand_name']} {test_case['product_category']} 补货分析")
    print(f"目标季度：{test_case['target_quarter']}")
    print(f"特殊关注：{test_case['special_focus']}")
    
    try:
        # 导入分析模块
        from web.utils.analysis_runner import run_manufacturing_analysis
        
        print("\n⏰ 开始运行分析...")
        start_time = time.time()
        
        # 执行分析
        results = run_manufacturing_analysis(
            brand_name=test_case['brand_name'],
            product_category=test_case['product_category'],
            target_quarter=test_case['target_quarter'],
            special_focus=test_case['special_focus'],
            analysts=test_case['analysts'],
            research_depth=test_case['research_depth'],
            llm_provider='dashscope',
            llm_model='qwen-max'
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ 分析完成！耗时：{duration:.2f}秒")
        
        # 分析结果
        print("\n📋 结果分析：")
        if results.get('success', False):
            print("✅ 流程执行成功")
            
            state = results.get('state', {})
            decision = results.get('decision', '')
            
            # 检查报告完整性
            reports = {
                "市场环境分析": state.get('market_environment_report', ''),
                "趋势预测分析": state.get('trend_prediction_report', ''),
                "行业资讯分析": state.get('industry_news_report', ''),
                "消费者洞察": state.get('consumer_insight_report', '')
            }
            
            print(f"\n📊 报告完成情况：")
            for name, report in reports.items():
                status = "✅" if len(report) > 100 else "❌"
                length = len(report)
                print(f"  {status} {name}: {length} 字符")
            
            # 最终决策
            print(f"\n🎯 最终决策：")
            if decision:
                print(f"决策长度：{len(decision)} 字符")
                print(f"包含量化数据：{'✅' if any(keyword in decision for keyword in ['%', '万台', '元', '月']) else '❌'}")
                print(f"包含风险评估：{'✅' if '风险' in decision else '❌'}")
                
                # 显示决策摘要（前500字符）
                print(f"\n📄 决策摘要：")
                print("-" * 60)
                print(decision[:500] + "..." if len(decision) > 500 else decision)
                print("-" * 60)
            else:
                print("❌ 未生成最终决策")
                
        else:
            print("❌ 流程执行失败")
            error = results.get('error', '未知错误')
            print(f"错误信息：{error}")
            
        # 保存详细结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"test_result_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "test_case": test_case,
                "duration": duration,
                "results": results
            }, f, ensure_ascii=False, indent=2)
            
        print(f"\n📄 详细结果已保存至：{report_file}")
        
        return True, duration, results
        
    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        import traceback
        print(f"错误详情：{traceback.format_exc()}")
        return False, 0, None


def main():
    """主函数"""
    print("=" * 60)
    print("🏭 制造业智能补货决策系统")
    print("   全流程功能验证测试")
    print("=" * 60)
    
    success, duration, results = test_manufacturing_pipeline()
    
    print(f"\n{'='*60}")
    print("📊 测试总结")
    print(f"{'='*60}")
    
    if success:
        print("✅ 系统功能验证：通过")
        print(f"⏱️  响应时间：{duration:.2f}秒")
        
        if duration < 300:
            print("🚀 性能评级：优秀（<5分钟）")
        elif duration < 600:
            print("⚡ 性能评级：良好（5-10分钟）")
        else:
            print("🐌 性能评级：需优化（>10分钟）")
            
        # 根据结果给出建议
        if results and results.get('success'):
            print("\n💡 系统状态：已可投入使用")
            print("📈 建议：可以开始业务验证和用户试用")
        else:
            print("\n⚠️  系统状态：需要调试优化")
            print("🔧 建议：检查错误日志，优化智能体配置")
    else:
        print("❌ 系统功能验证：失败")
        print("🔧 建议：检查配置和依赖项")
    
    print(f"\n🎯 下一步行动建议：")
    print("1. 基于测试结果调优智能体参数")
    print("2. 测试更多业务场景")
    print("3. 进行用户试用和反馈收集")
    

if __name__ == "__main__":
    main() 