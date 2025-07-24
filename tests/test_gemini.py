#!/usr/bin/env python3
"""
测试Google Gemini模型
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv(project_root / ".env", override=True)

def check_gemini_setup():
    """检查Gemini模型设置"""
    print("🔍 检查Gemini模型设置")
    print("=" * 50)
    
    # 检查API密钥
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if google_api_key:
        print(f"✅ Google API密钥已配置: {google_api_key[:20]}...")
    else:
        print("❌ Google API密钥未配置")
        print("💡 请在.env文件中设置 GOOGLE_API_KEY")
        return False
    
    # 检查依赖库
    try:
        import google.generativeai as genai
        print("✅ google-generativeai库已安装")
    except ImportError:
        print("❌ google-generativeai库未安装")
        print("💡 运行: pip install google-generativeai")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain-google-genai库已安装")
    except ImportError:
        print("❌ langchain-google-genai库未安装")
        print("💡 运行: pip install langchain-google-genai")
        return False
    
    return True

def test_gemini_direct():
    """直接测试Gemini API"""
    try:
        print("\n🧪 直接测试Gemini API")
        print("=" * 50)
        
        import google.generativeai as genai
        
        # 配置API密钥
        google_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        
        # 创建模型实例
        model = genai.GenerativeModel('gemini-pro')
        
        print("✅ Gemini模型实例创建成功")
        
        # 测试生成内容
        print("📝 测试内容生成...")
        response = model.generate_content("请用中文简单介绍一下苹果公司(Apple Inc.)的业务")
        
        if response and response.text:
            print("✅ Gemini API调用成功")
            print(f"   响应长度: {len(response.text)} 字符")
            print(f"   响应预览: {response.text[:200]}...")
            return True
        else:
            print("❌ Gemini API调用失败：无响应内容")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_gemini_langchain():
    """测试通过LangChain使用Gemini"""
    try:
        print("\n🧪 测试LangChain Gemini集成")
        print("=" * 50)
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # 创建LangChain Gemini实例
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.1,
            max_tokens=1000,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        print("✅ LangChain Gemini实例创建成功")
        
        # 测试调用
        print("📝 测试LangChain调用...")
        response = llm.invoke("请用中文分析一下当前科技股的投资前景，重点关注人工智能领域")
        
        if response and response.content:
            print("✅ LangChain Gemini调用成功")
            print(f"   响应长度: {len(response.content)} 字符")
            print(f"   响应预览: {response.content[:200]}...")
            return True
        else:
            print("❌ LangChain Gemini调用失败：无响应内容")
            return False
            
    except Exception as e:
        print(f"❌ LangChain Gemini测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_gemini_in_tradingagents():
    """测试在TradingAgents中使用Gemini"""
    try:
        print("\n🧪 测试TradingAgents中的Gemini集成")
        print("=" * 50)
        
        from manufacturingagents.graph.trading_graph import TradingAgentsGraph
        from manufacturingagents.default_config import DEFAULT_CONFIG
        
        # 创建使用Gemini的配置
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "google"
        config["deep_think_llm"] = "gemini-pro"
        config["quick_think_llm"] = "gemini-pro"
        config["online_tools"] = True
        config["memory_enabled"] = True
        
        # 修复路径
        config["data_dir"] = str(project_root / "data")
        config["results_dir"] = str(project_root / "results")
        config["data_cache_dir"] = str(project_root / "tradingagents" / "dataflows" / "data_cache")
        
        # 创建目录
        os.makedirs(config["data_dir"], exist_ok=True)
        os.makedirs(config["results_dir"], exist_ok=True)
        os.makedirs(config["data_cache_dir"], exist_ok=True)
        
        print("✅ 配置创建成功")
        print(f"   LLM提供商: {config['llm_provider']}")
        print(f"   深度思考模型: {config['deep_think_llm']}")
        print(f"   快速思考模型: {config['quick_think_llm']}")
        
        # 创建TradingAgentsGraph实例
        print("🚀 初始化TradingAgents图...")
        graph = TradingAgentsGraph(["market"], config=config, debug=False)
        
        print("✅ TradingAgents图初始化成功")
        
        # 测试简单分析
        print("📊 测试简单股票分析...")
        try:
            state, decision = graph.propagate("AAPL", "2025-06-27")
            
            if state and decision:
                print("✅ Gemini驱动的股票分析成功")
                print(f"   决策结果: {decision}")
                
                # 检查市场报告
                if "market_report" in state and state["market_report"]:
                    market_report = state["market_report"]
                    print(f"   市场报告长度: {len(market_report)} 字符")
                    print(f"   报告预览: {market_report[:200]}...")
                
                return True
            else:
                print("❌ 分析完成但结果为空")
                return False
                
        except Exception as e:
            print(f"❌ 股票分析失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ TradingAgents Gemini集成测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """主测试函数"""
    print("🧪 Google Gemini模型测试")
    print("=" * 60)
    
    # 检查设置
    if not check_gemini_setup():
        print("\n❌ Gemini设置不完整，无法继续测试")
        return
    
    # 运行测试
    results = {}
    
    results['Gemini直接API'] = test_gemini_direct()
    results['LangChain集成'] = test_gemini_langchain()
    results['TradingAgents集成'] = test_gemini_in_tradingagents()
    
    # 总结结果
    print(f"\n📊 测试结果总结:")
    print("=" * 50)
    
    for test_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    successful_tests = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 总体结果: {successful_tests}/{total_tests} 测试通过")
    
    if successful_tests == total_tests:
        print("🎉 Gemini模型完全可用！")
        print("\n💡 使用建议:")
        print("   1. 可以在Web界面配置中选择Google作为LLM提供商")
        print("   2. 可以选择gemini-pro作为分析模型")
        print("   3. Gemini在多语言支持方面表现优秀")
    elif successful_tests > 0:
        print("⚠️ Gemini部分功能可用，建议检查失败的测试")
    else:
        print("❌ Gemini模型不可用，请检查API密钥和网络连接")

if __name__ == "__main__":
    main()
