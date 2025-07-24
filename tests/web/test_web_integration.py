#!/usr/bin/env python3

import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 模拟Web界面调用
from web.utils.analysis_runner import run_manufacturing_analysis

def test_web_integration():
    print("🌐 Web集成测试：验证前端是否能正确调用ReAct系统")
    print("=" * 60)
    
    # 模拟Web表单数据
    web_params = {
        'brand_name': '美的',
        'product_category': '空调',
        'target_quarter': '2025Q2',
        'special_focus': '',
        'analysts': ['market_environment_analyst'],  # 只测试一个分析师
        'research_depth': 3,
        'llm_provider': 'dashscope',
        'llm_model': 'qwen-turbo'
    }
    
    try:
        print(f"🚀 模拟Web界面调用 run_manufacturing_analysis...")
        print(f"📋 参数: {web_params}")
        
        # 调用Web分析接口
        results = run_manufacturing_analysis(
            brand_name=web_params['brand_name'],
            product_category=web_params['product_category'],
            target_quarter=web_params['target_quarter'],
            special_focus=web_params['special_focus'],
            analysts=web_params['analysts'],
            research_depth=web_params['research_depth'],
            llm_provider=web_params['llm_provider'],
            llm_model=web_params['llm_model'],
            progress_callback=lambda msg, step=None, total=None: print(f"[PROGRESS] {msg}")
        )
        
        print("\n📊 Web集成测试结果:")
        print("=" * 40)
        
        if results.get('success'):
            print("✅ Web调用成功!")
            
            # 检查state
            state = results.get('state', {})
            report = state.get('market_environment_report', '')
            
            print(f"📝 报告长度: {len(report)} 字符")
            if len(report) > 1000:
                print("✅ ReAct系统成功生成完整报告")
                print(f"📄 报告前300字符: {report[:300]}...")
                
                # 检查是否包含真实数据
                if "PMI" in report and "PPI" in report:
                    print("✅ 报告包含真实PMI和PPI数据")
                else:
                    print("⚠️ 报告可能缺少真实数据")
                    
                print("\n🎉 Web集成测试完全成功!")
                print("💡 前端现在可以正常使用ReAct系统了")
                
            else:
                print("❌ 报告长度过短，ReAct系统可能未正常工作")
                print(f"报告内容: {report}")
        else:
            print("❌ Web调用失败")
            print(f"错误: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Web集成测试失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")

if __name__ == "__main__":
    test_web_integration() 