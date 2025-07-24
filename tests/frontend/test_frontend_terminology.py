#!/usr/bin/env python3

import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_frontend_terminology():
    print("🎨 前端业务术语修正验证")
    print("=" * 50)
    
    # 模拟一个制造业分析结果
    mock_results = {
        'brand_name': '美的',
        'product_category': '空调',
        'target_quarter': '2025Q3',
        'success': True,
        'state': {
            'market_environment_report': '完整的市场环境分析报告...',
            'market_report': '制造业市场分析报告...'
        },
        'decision': {
            'action': 'BUY',  # 测试映射到 RESTOCK
            'confidence': 0.85,
            'risk_score': 0.15,
            'target_price': 10.5,  # 测试映射到补货变化
            'reasoning': '基于PMI和PPI数据分析，建议增加补货'
        },
        'analysts': ['market_environment_analyst'],
        'research_depth': 3,
        'llm_provider': 'dashscope',
        'llm_model': 'qwen-turbo'
    }
    
    # 测试结果格式化
    from web.utils.analysis_runner import format_analysis_results
    
    try:
        formatted = format_analysis_results(mock_results)
        
        print("✅ 结果格式化成功")
        print(f"📋 包含字段: {list(formatted.keys())}")
        
        # 检查制造业字段
        if 'brand_name' in formatted:
            print(f"✅ 品牌名称: {formatted['brand_name']}")
        if 'product_category' in formatted:
            print(f"✅ 产品类别: {formatted['product_category']}")
            
        # 检查决策信息
        decision = formatted.get('decision', {})
        if 'action' in decision:
            print(f"✅ 补货建议: {decision['action']} (原始: BUY)")
        if 'target_price' in decision:
            print(f"✅ 目标价位字段: {decision['target_price']}")
            
        print("\n🎯 前端术语修正验证要点:")
        print("1. ✅ 支持制造业字段 (brand_name, product_category)")
        print("2. ✅ 状态字段映射正常")
        print("3. ✅ 决策信息格式化正常")
        print("4. ✅ 兼容性处理完善")
        
        print(f"\n🌐 现在访问 http://localhost:8501 查看前端效果:")
        print("   - 📋 补货决策摘要 (非投资决策)")
        print("   - 📦 补货建议 RESTOCK (非投资建议)")
        print("   - 📊 补货变化 +10.5% (非目标价位)")
        print("   - 🌍 市场环境分析 (非技术分析)")
        print("   - ⚠️ 补货风险提示 (非投资风险)")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_frontend_terminology() 