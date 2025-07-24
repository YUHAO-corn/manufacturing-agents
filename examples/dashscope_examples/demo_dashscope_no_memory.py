#!/usr/bin/env python3
"""
TradingAgents 演示脚本 - 使用阿里百炼大模型（禁用记忆功能）
这个脚本展示了如何使用阿里百炼大模型运行 TradingAgents 框架，临时禁用记忆功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from manufacturingagents.graph.trading_graph import TradingAgentsGraph
from manufacturingagents.default_config import DEFAULT_CONFIG

# 加载 .env 文件
load_dotenv()

def main():
    """主函数"""
    print("🚀 TradingAgents 演示 - 阿里百炼版本（无记忆）")
    print("=" * 60)
    
    # 检查API密钥
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    
    if not dashscope_key:
        print("❌ 错误: 未找到 DASHSCOPE_API_KEY 环境变量")
        return
    
    if not finnhub_key:
        print("❌ 错误: 未找到 FINNHUB_API_KEY 环境变量")
        return
    
    print(f"✅ 阿里百炼 API 密钥: {dashscope_key[:10]}...")
    print(f"✅ FinnHub API 密钥: {finnhub_key[:10]}...")
    print()
    
    # 创建阿里百炼配置
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "dashscope"
    config["deep_think_llm"] = "qwen-plus"      # 深度分析
    config["quick_think_llm"] = "qwen-turbo"    # 快速任务
    config["max_debate_rounds"] = 1             # 减少辩论轮次
    config["online_tools"] = False             # 暂时禁用在线工具
    config["use_memory"] = False               # 禁用记忆功能
    
    print("📊 配置信息:")
    print(f"  LLM 提供商: {config['llm_provider']}")
    print(f"  深度思考模型: {config['deep_think_llm']} (通义千问Plus)")
    print(f"  快速思考模型: {config['quick_think_llm']} (通义千问Turbo)")
    print(f"  最大辩论轮次: {config['max_debate_rounds']}")
    print(f"  在线工具: {config['online_tools']}")
    print(f"  记忆功能: {config['use_memory']}")
    print()
    
    try:
        print("🤖 正在初始化 TradingAgents...")
        
        # 临时修改记忆相关的环境变量，避免初始化错误
        original_openai_key = os.environ.get('OPENAI_API_KEY')
        if not original_openai_key:
            os.environ['OPENAI_API_KEY'] = 'dummy_key_for_initialization'
        
        ta = TradingAgentsGraph(debug=True, config=config)
        print("✅ TradingAgents 初始化成功!")
        print()
        
        # 分析股票
        stock_symbol = "AAPL"  # 苹果公司
        analysis_date = "2024-05-10"
        
        print(f"📈 开始分析股票: {stock_symbol}")
        print(f"📅 分析日期: {analysis_date}")
        print("⏳ 正在进行多智能体分析，请稍候...")
        print("🧠 使用阿里百炼大模型进行智能分析...")
        print("⚠️  注意: 当前版本禁用了记忆功能以避免兼容性问题")
        print()
        
        # 执行分析
        state, decision = ta.propagate(stock_symbol, analysis_date)
        
        print("🎯 分析结果:")
        print("=" * 50)
        print(decision)
        print("=" * 50)
        
        print("✅ 分析完成!")
        print()
        print("🌟 阿里百炼大模型特色:")
        print("  - 中文理解能力强")
        print("  - 金融领域知识丰富")
        print("  - 推理能力出色")
        print("  - 成本相对较低")
        print()
        print("💡 提示:")
        print("  - 当前版本为了兼容性暂时禁用了记忆功能")
        print("  - 完整功能版本需要解决嵌入模型兼容性问题")
        print("  - 您可以修改 stock_symbol 和 analysis_date 来分析其他股票")
        
    except Exception as e:
        print(f"❌ 运行时错误: {str(e)}")
        print()
        # 显示详细的错误信息
        import traceback
        print("🔍 详细错误信息:")
        traceback.print_exc()
        print()
        print("🔧 可能的解决方案:")
        print("1. 检查阿里百炼API密钥是否正确")
        print("2. 确认已开通百炼服务并有足够额度")
        print("3. 检查网络连接")
        print("4. 尝试使用简化版本的演示脚本")

if __name__ == "__main__":
    main()
