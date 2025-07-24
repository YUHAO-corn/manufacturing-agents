#!/usr/bin/env python3
"""
测试Gemini 2.5 Flash和Pro模型
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

# Gemini 2.5模型列表
GEMINI_25_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro", 
    "gemini-2.5-flash-002",
    "gemini-2.5-pro-002"
]

def test_gemini_25_availability():
    """测试Gemini 2.5模型的可用性"""
    print("🧪 测试Gemini 2.5模型可用性")
    print("=" * 60)
    
    try:
        import google.generativeai as genai
        
        # 配置API密钥
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            print("❌ Google API密钥未配置")
            return []
        
        genai.configure(api_key=google_api_key)
        
        # 获取所有可用模型
        print("📋 获取所有可用模型...")
        all_models = genai.list_models()
        
        available_25_models = []
        
        print("🔍 检查Gemini 2.5模型:")
        for model_name in GEMINI_25_MODELS:
            found = False
            for model in all_models:
                if model_name in model.name:
                    print(f"✅ {model_name}: 可用")
                    print(f"   完整名称: {model.name}")
                    print(f"   显示名称: {model.display_name}")
                    print(f"   支持方法: {model.supported_generation_methods}")
                    available_25_models.append(model.name)
                    found = True
                    break
            
            if not found:
                print(f"❌ {model_name}: 不可用")
        
        return available_25_models
        
    except Exception as e:
        print(f"❌ 检查模型可用性失败: {e}")
        return []

def test_specific_gemini_25_model(model_name):
    """测试特定的Gemini 2.5模型"""
    try:
        print(f"\n🧪 测试模型: {model_name}")
        print("=" * 60)
        
        import google.generativeai as genai
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # 配置API密钥
        google_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        
        # 测试1: 直接API
        print("📝 测试直接API...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                "请用中文分析苹果公司(AAPL)的投资价值，包括技术创新、市场地位和财务状况"
            )
            
            if response and response.text:
                print("✅ 直接API调用成功")
                print(f"   响应长度: {len(response.text)} 字符")
                print(f"   响应预览: {response.text[:200]}...")
                direct_success = True
            else:
                print("❌ 直接API调用失败：无响应内容")
                direct_success = False
        except Exception as e:
            print(f"❌ 直接API调用失败: {e}")
            direct_success = False
        
        # 测试2: LangChain集成
        print("\n📝 测试LangChain集成...")
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.1,
                max_tokens=1000,
                google_api_key=google_api_key
            )
            
            response = llm.invoke(
                "请用中文分析当前人工智能行业的投资机会，重点关注大型科技公司的AI战略"
            )
            
            if response and response.content:
                print("✅ LangChain调用成功")
                print(f"   响应长度: {len(response.content)} 字符")
                print(f"   响应预览: {response.content[:200]}...")
                langchain_success = True
            else:
                print("❌ LangChain调用失败：无响应内容")
                langchain_success = False
        except Exception as e:
            print(f"❌ LangChain调用失败: {e}")
            langchain_success = False
        
        # 测试3: 复杂推理能力
        print("\n📝 测试复杂推理能力...")
        try:
            complex_prompt = """
            请用中文进行复杂的股票分析推理：
            
            假设场景：
            - 当前时间：2025年6月
            - 美联储刚刚降息0.25%
            - 中美贸易关系有所缓解
            - AI技术快速发展
            - 通胀率降至2.5%
            
            请分析在这种宏观环境下，苹果公司(AAPL)的投资价值，包括：
            1. 宏观经济因素的影响
            2. 行业竞争态势
            3. 公司特有优势
            4. 风险因素
            5. 投资建议和目标价位
            
            请提供详细的逻辑推理过程。
            """
            
            response = llm.invoke(complex_prompt)
            
            if response and response.content and len(response.content) > 500:
                print("✅ 复杂推理测试成功")
                print(f"   响应长度: {len(response.content)} 字符")
                print(f"   响应预览: {response.content[:300]}...")
                complex_success = True
            else:
                print("❌ 复杂推理测试失败：响应过短或无内容")
                complex_success = False
        except Exception as e:
            print(f"❌ 复杂推理测试失败: {e}")
            complex_success = False
        
        return direct_success, langchain_success, complex_success
        
    except Exception as e:
        print(f"❌ 模型测试失败: {e}")
        return False, False, False

def test_gemini_25_in_tradingagents(model_name):
    """测试Gemini 2.5在TradingAgents中的使用"""
    try:
        print(f"\n🧪 测试{model_name}在TradingAgents中的使用")
        print("=" * 60)
        
        from manufacturingagents.graph.trading_graph import TradingAgentsGraph
        from manufacturingagents.default_config import DEFAULT_CONFIG
        
        # 创建配置
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "google"
        config["deep_think_llm"] = model_name
        config["quick_think_llm"] = model_name
        config["online_tools"] = False  # 避免API限制
        config["memory_enabled"] = True  # 启用内存功能
        config["max_debate_rounds"] = 1
        config["max_risk_discuss_rounds"] = 1
        
        # 修复路径
        config["data_dir"] = str(project_root / "data")
        config["results_dir"] = str(project_root / "results")
        config["data_cache_dir"] = str(project_root / "tradingagents" / "dataflows" / "data_cache")
        
        # 创建目录
        os.makedirs(config["data_dir"], exist_ok=True)
        os.makedirs(config["results_dir"], exist_ok=True)
        os.makedirs(config["data_cache_dir"], exist_ok=True)
        
        print("✅ 配置创建成功")
        print(f"   模型: {model_name}")
        print(f"   内存功能: {config['memory_enabled']}")
        
        # 创建TradingAgentsGraph实例
        print("🚀 初始化TradingAgents图...")
        graph = TradingAgentsGraph(["market"], config=config, debug=False)
        
        print("✅ TradingAgents图初始化成功")
        
        # 测试分析
        print("📊 开始股票分析...")
        
        try:
            state, decision = graph.propagate("AAPL", "2025-06-27")
            
            if state and decision:
                print(f"✅ {model_name}驱动的股票分析成功！")
                print(f"   最终决策: {decision}")
                
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
        print(f"❌ TradingAgents测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 Gemini 2.5模型测试")
    print("=" * 70)
    
    # 检查API密钥
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print("❌ Google API密钥未配置")
        return
    
    print(f"✅ Google API密钥已配置: {google_api_key[:20]}...")
    
    # 检查可用的Gemini 2.5模型
    available_models = test_gemini_25_availability()
    
    if not available_models:
        print("\n❌ 没有找到可用的Gemini 2.5模型")
        return
    
    print(f"\n🎯 找到 {len(available_models)} 个可用的Gemini 2.5模型")
    
    # 测试每个可用模型
    best_model = None
    best_score = 0
    
    for model_name in available_models:
        print(f"\n{'='*70}")
        
        # 基础功能测试
        direct, langchain, complex = test_specific_gemini_25_model(model_name)
        score = sum([direct, langchain, complex])
        
        print(f"\n📊 {model_name} 基础测试结果:")
        print(f"   直接API: {'✅' if direct else '❌'}")
        print(f"   LangChain: {'✅' if langchain else '❌'}")
        print(f"   复杂推理: {'✅' if complex else '❌'}")
        print(f"   得分: {score}/3")
        
        if score > best_score:
            best_score = score
            best_model = model_name
        
        # 如果基础功能全部通过，测试TradingAgents集成
        if score == 3:
            tradingagents_success = test_gemini_25_in_tradingagents(model_name)
            if tradingagents_success:
                print(f"   TradingAgents: ✅")
                total_score = score + 1
            else:
                print(f"   TradingAgents: ❌")
                total_score = score
            
            print(f"   总得分: {total_score}/4")
    
    # 最终推荐
    print(f"\n📊 最终测试结果:")
    print("=" * 50)
    print(f"  最佳模型: {best_model}")
    print(f"  最高得分: {best_score}/3")
    
    if best_score >= 2:
        print(f"\n🎉 推荐使用: {best_model}")
        print(f"\n💡 配置建议:")
        print(f"   1. 在Web界面中选择'Google'作为LLM提供商")
        print(f"   2. 使用模型名称: {best_model}")
        print(f"   3. Gemini 2.5具有更强的推理和分析能力")
        print(f"   4. 支持更复杂的金融分析任务")
    else:
        print(f"\n⚠️ 所有Gemini 2.5模型测试不理想")
        print(f"   建议检查API密钥权限和网络连接")

if __name__ == "__main__":
    main()
