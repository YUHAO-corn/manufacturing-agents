#!/usr/bin/env python3
"""
TradingAgents 简化演示脚本 - 使用阿里百炼大模型
这个脚本展示了如何使用阿里百炼大模型进行简单的LLM测试
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def test_simple_llm():
    """测试简单的LLM调用"""
    print("🚀 阿里百炼大模型简单测试")
    print("=" * 50)
    
    # 检查API密钥
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not dashscope_key:
        print("❌ 错误: 未找到 DASHSCOPE_API_KEY 环境变量")
        return
    
    print(f"✅ 阿里百炼 API 密钥: {dashscope_key[:10]}...")
    print()
    
    try:
        from manufacturingagents.llm_adapters import ChatDashScope
        from langchain_core.messages import HumanMessage
        
        print("🤖 正在初始化阿里百炼模型...")
        
        # 创建模型实例
        llm = ChatDashScope(
            model="qwen-plus",
            temperature=0.1,
            max_tokens=1000
        )
        
        print("✅ 模型初始化成功!")
        print()
        
        # 测试金融分析能力
        print("📈 测试金融分析能力...")
        
        messages = [HumanMessage(content="""
请分析特斯拉公司(TSLA)的投资价值，从以下几个角度：
1. 公司基本面 - 财务状况、盈利能力、现金流
2. 技术面分析 - 股价趋势、技术指标、支撑阻力位
3. 市场前景 - 电动车市场、自动驾驶、能源业务
4. 风险因素 - 竞争风险、监管风险、执行风险
5. 投资建议 - 评级、目标价、投资时间框架

请用中文回答，提供具体的数据和分析，保持专业和客观。
""")]
        
        print("⏳ 正在生成分析报告...")
        response = llm.invoke(messages)
        
        print("🎯 分析结果:")
        print("=" * 50)
        print(response.content)
        print("=" * 50)
        
        print("✅ 测试完成!")
        print()
        print("🌟 阿里百炼大模型特色:")
        print("  - 中文理解能力强")
        print("  - 金融领域知识丰富")
        print("  - 推理能力出色")
        print("  - 响应速度快")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        print("🔍 详细错误信息:")
        traceback.print_exc()

def test_multiple_models():
    """测试多个模型"""
    print("\n🔄 测试不同的通义千问模型")
    print("=" * 50)
    
    models = [
        ("qwen-turbo", "通义千问 Turbo - 快速响应"),
        ("qwen-plus-latest", "通义千问 Plus - 平衡性能"),
        ("qwen-max", "通义千问 Max - 最强性能")
    ]
    
    question = "请用一句话总结苹果公司的核心竞争优势。"
    
    for model_id, model_name in models:
        try:
            print(f"\n🧠 测试 {model_name}...")
            
            from manufacturingagents.llm_adapters import ChatDashScope
            from langchain_core.messages import HumanMessage
            
            llm = ChatDashScope(model=model_id, temperature=0.1, max_tokens=200)
            response = llm.invoke([HumanMessage(content=question)])
            
            print(f"✅ {model_name}: {response.content}")
            
        except Exception as e:
            print(f"❌ {model_name} 测试失败: {str(e)}")

def main():
    """主函数"""
    test_simple_llm()
    test_multiple_models()
    
    print("\n💡 下一步:")
    print("  1. 如果测试成功，说明阿里百炼集成正常")
    print("  2. 完整的TradingAgents需要解决记忆系统的兼容性")
    print("  3. 可以考虑为阿里百炼添加嵌入模型支持")

if __name__ == "__main__":
    main()
