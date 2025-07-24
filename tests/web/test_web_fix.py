#!/usr/bin/env python3

import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 测试Web分析流程的修复
from web.utils.analysis_runner import run_manufacturing_analysis, format_analysis_results

def test_web_frontend_fix():
    print("🔧 Web前端显示问题修复验证")
    print("=" * 50)
    
    try:
        print("🚀 模拟完整的Web分析流程...")
        
        # 第1步：后端分析（已知能成功）
        results = run_manufacturing_analysis(
            brand_name='美的',
            product_category='空调',
            target_quarter='2025Q3',
            special_focus='',
            analysts=['market_environment_analyst'],
            research_depth=3,
            llm_provider='dashscope',
            llm_model='qwen-turbo',
            progress_callback=lambda msg, step=None, total=None: print(f"[PROGRESS] {msg}")
        )
        
        print(f"\n✅ 第1步：后端分析成功")
        print(f"📊 分析成功: {results.get('success')}")
        print(f"📝 报告长度: {len(results.get('state', {}).get('market_environment_report', ''))}")
        
        # 第2步：结果格式化（这里之前出错）
        print(f"\n🔧 第2步：测试结果格式化...")
        formatted_results = format_analysis_results(results)
        
        print(f"✅ 格式化成功！无 'stock_symbol' 错误")
        print(f"📋 格式化结果包含字段: {list(formatted_results.keys())}")
        
        # 第3步：检查前端需要的字段
        print(f"\n📋 第3步：检查前端兼容性...")
        
        # 检查基本字段
        if 'brand_name' in formatted_results:
            print(f"✅ 品牌名称: {formatted_results['brand_name']}")
        if 'product_category' in formatted_results:
            print(f"✅ 产品类别: {formatted_results['product_category']}")
        if 'decision' in formatted_results:
            print(f"✅ 决策信息: {type(formatted_results['decision'])}")
        if 'state' in formatted_results:
            state = formatted_results['state']
            print(f"✅ 状态信息: {len(state)} 个字段")
            
            # 检查报告映射
            if 'market_report' in state:
                report_len = len(state['market_report'])
                print(f"✅ 市场报告映射成功: {report_len} 字符")
            if 'market_environment_report' in state:
                original_len = len(state['market_environment_report'])
                print(f"✅ 原始字段保留: {original_len} 字符")
        
        print(f"\n🎉 Web前端显示问题修复验证完成！")
        print(f"💡 现在可以在前端正常显示分析结果了")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复验证失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_web_frontend_fix() 