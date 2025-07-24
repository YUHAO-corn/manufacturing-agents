#!/usr/bin/env python3
"""
TradingAgents 演示脚本 - 使用阿里百炼大模型
这个脚本展示了如何使用阿里百炼大模型运行 TradingAgents 框架
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
    print("🚀 TradingAgents 演示 - 阿里百炼版本")
    print("=" * 50)
    
    # 检查API密钥
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    
    if not dashscope_key:
        print("❌ 错误: 未找到 DASHSCOPE_API_KEY 环境变量")
        print("请设置您的阿里百炼 API 密钥:")
        print("  Windows: set DASHSCOPE_API_KEY=your_api_key")
        print("  Linux/Mac: export DASHSCOPE_API_KEY=your_api_key")
        print("  或创建 .env 文件")
        print()
        print("🔗 获取API密钥:")
        print("  1. 访问 https://dashscope.aliyun.com/")
        print("  2. 注册/登录阿里云账号")
        print("  3. 开通百炼服务")
        print("  4. 在控制台获取API密钥")
        return
    
    if not finnhub_key:
        print("❌ 错误: 未找到 FINNHUB_API_KEY 环境变量")
        print("请设置您的 FinnHub API 密钥:")
        print("  Windows: set FINNHUB_API_KEY=your_api_key")
        print("  Linux/Mac: export FINNHUB_API_KEY=your_api_key")
        print("  或创建 .env 文件")
        print()
        print("🔗 获取API密钥:")
        print("  访问 https://finnhub.io/ 注册免费账户")
        return
    
    print(f"✅ 阿里百炼 API 密钥: {dashscope_key[:10]}...")
    print(f"✅ FinnHub API 密钥: {finnhub_key[:10]}...")
    print()
    
    # 创建阿里百炼配置
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "dashscope"
    config["backend_url"] = "https://dashscope.aliyuncs.com/api/v1"
    config["deep_think_llm"] = "qwen-plus-latest"  # 使用通义千问Plus进行深度思考
    config["quick_think_llm"] = "qwen-turbo"  # 使用通义千问Turbo进行快速任务
    config["max_debate_rounds"] = 1  # 减少辩论轮次以降低成本
    config["online_tools"] = True
    
    print("📊 配置信息:")
    print(f"  LLM 提供商: {config['llm_provider']}")
    print(f"  深度思考模型: {config['deep_think_llm']} (通义千问Plus)")
    print(f"  快速思考模型: {config['quick_think_llm']} (通义千问Turbo)")
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

        # 设置中文输出提示
        import os
        os.environ['TRADINGAGENTS_LANGUAGE'] = 'zh-CN'
        
        print(f"📈 开始分析股票: {stock_symbol}")
        print(f"📅 分析日期: {analysis_date}")
        print("⏳ 正在进行多智能体分析，请稍候...")
        print("🧠 使用阿里百炼大模型进行智能分析...")
        print()
        
        # 执行分析
        state, decision = ta.propagate(stock_symbol, analysis_date)
        
        print("🎯 分析结果:")
        print("=" * 30)
        print(decision)
        print()
        
        print("✅ 分析完成!")
        print("💡 提示: 您可以修改 stock_symbol 和 analysis_date 来分析其他股票")
        print()
        print("🌟 阿里百炼大模型特色:")
        print("  - 中文理解能力强")
        print("  - 金融领域知识丰富")
        print("  - 推理能力出色")
        print("  - 成本相对较低")
        
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
        print("4. 查看详细错误信息进行调试")
        print()
        print("📞 如需帮助:")
        print("  - 阿里百炼官方文档: https://help.aliyun.com/zh/dashscope/")
        print("  - 控制台: https://dashscope.console.aliyun.com/")

if __name__ == "__main__":
    main()
