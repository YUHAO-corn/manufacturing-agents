#!/usr/bin/env python3
"""
TradingAgents 演示脚本 - 使用 OpenAI 模型
这个脚本展示了如何使用 OpenAI 模型运行 TradingAgents 框架
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from manufacturingagents.graph.trading_graph import TradingAgentsGraph
from manufacturingagents.default_config import DEFAULT_CONFIG

def main():
    """主函数"""
    print("🚀 TradingAgents 演示 - OpenAI 版本")
    print("=" * 50)
    
    # 检查API密钥
    openai_key = os.getenv('OPENAI_API_KEY')
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    
    if not openai_key:
        print("❌ 错误: 未找到 OPENAI_API_KEY 环境变量")
        print("请设置您的 OpenAI API 密钥:")
        print("  Windows: set OPENAI_API_KEY=your_api_key")
        print("  Linux/Mac: export OPENAI_API_KEY=your_api_key")
        print("  或创建 .env 文件")
        return
    
    if not finnhub_key:
        print("❌ 错误: 未找到 FINNHUB_API_KEY 环境变量")
        print("请设置您的 FinnHub API 密钥:")
        print("  Windows: set FINNHUB_API_KEY=your_api_key")
        print("  Linux/Mac: export FINNHUB_API_KEY=your_api_key")
        print("  或创建 .env 文件")
        return
    
    print(f"✅ OpenAI API 密钥: {openai_key[:10]}...")
    print(f"✅ FinnHub API 密钥: {finnhub_key[:10]}...")
    print()
    
    # 创建 OpenAI 配置
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "openai"
    config["backend_url"] = "https://api.openai.com/v1"
    config["deep_think_llm"] = "gpt-4o-mini"  # 使用更经济的模型
    config["quick_think_llm"] = "gpt-4o-mini"
    config["max_debate_rounds"] = 1  # 减少辩论轮次以降低成本
    config["online_tools"] = True
    
    print("📊 配置信息:")
    print(f"  LLM 提供商: {config['llm_provider']}")
    print(f"  深度思考模型: {config['deep_think_llm']}")
    print(f"  快速思考模型: {config['quick_think_llm']}")
    print(f"  最大辩论轮次: {config['max_debate_rounds']}")
    print(f"  在线工具: {config['online_tools']}")
    print()
    
    try:
        print("🤖 正在初始化 TradingAgents...")
        ta = TradingAgentsGraph(debug=True, config=config)
        print("✅ TradingAgents 初始化成功!")
        print()
        
        # 分析股票
        stock_symbol = "AAPL"  # 苹果公司
        analysis_date = "2024-05-10"
        
        print(f"📈 开始分析股票: {stock_symbol}")
        print(f"📅 分析日期: {analysis_date}")
        print("⏳ 正在进行多智能体分析，请稍候...")
        print()
        
        # 执行分析
        state, decision = ta.propagate(stock_symbol, analysis_date)
        
        print("🎯 分析结果:")
        print("=" * 30)
        print(decision)
        print()
        
        print("✅ 分析完成!")
        print("💡 提示: 您可以修改 stock_symbol 和 analysis_date 来分析其他股票")
        
    except Exception as e:
        print(f"❌ 运行时错误: {str(e)}")
        print()
        print("🔧 可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 检查网络连接")
        print("3. 确认API账户有足够的额度")
        print("4. 查看详细错误信息进行调试")

if __name__ == "__main__":
    main()
