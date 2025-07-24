#!/usr/bin/env python3
"""
诊断Gemini 2.5模型问题
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

def test_gemini_models():
    """测试不同的Gemini模型"""
    print("🧪 诊断Gemini模型问题")
    print("=" * 60)
    
    models_to_test = [
        "gemini-2.5-pro",
        "gemini-2.5-flash", 
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
    
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print("❌ Google API密钥未配置")
        return
    
    print(f"✅ Google API密钥已配置: {google_api_key[:20]}...")
    
    working_models = []
    
    for model_name in models_to_test:
        print(f"\n🔍 测试模型: {model_name}")
        print("-" * 40)
        
        try:
            # 测试直接API
            print("📝 测试直接Google API...")
            import google.generativeai as genai
            genai.configure(api_key=google_api_key)
            
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("请用中文说：你好，我是Gemini模型")
            
            if response and response.text:
                print(f"✅ 直接API成功: {response.text[:100]}...")
                direct_success = True
            else:
                print("❌ 直接API失败：无响应")
                direct_success = False
                
        except Exception as e:
            print(f"❌ 直接API失败: {e}")
            direct_success = False
        
        try:
            # 测试LangChain
            print("📝 测试LangChain集成...")
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.1,
                max_tokens=200,
                google_api_key=google_api_key
            )
            
            response = llm.invoke("请用中文简单介绍一下你自己")
            
            if response and response.content:
                print(f"✅ LangChain成功: {response.content[:100]}...")
                langchain_success = True
            else:
                print("❌ LangChain失败：无响应")
                langchain_success = False
                
        except Exception as e:
            print(f"❌ LangChain失败: {e}")
            langchain_success = False
        
        # 记录结果
        if direct_success or langchain_success:
            working_models.append({
                'name': model_name,
                'direct': direct_success,
                'langchain': langchain_success
            })
            print(f"✅ {model_name} 部分或完全可用")
        else:
            print(f"❌ {model_name} 完全不可用")
    
    return working_models

def test_best_working_model(working_models):
    """测试最佳可用模型"""
    if not working_models:
        print("\n❌ 没有找到可用的模型")
        return None
    
    # 选择最佳模型（优先选择2.5版本，然后是LangChain可用的）
    best_model = None
    for model in working_models:
        if model['langchain']:  # LangChain可用
            if '2.5' in model['name']:  # 优先2.5版本
                best_model = model['name']
                break
            elif best_model is None:  # 如果还没有选择，就选这个
                best_model = model['name']
    
    if best_model is None:
        # 如果没有LangChain可用的，选择直接API可用的
        for model in working_models:
            if model['direct']:
                best_model = model['name']
                break
    
    if best_model:
        print(f"\n🎯 选择最佳模型进行详细测试: {best_model}")
        print("=" * 60)
        
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            llm = ChatGoogleGenerativeAI(
                model=best_model,
                temperature=0.1,
                max_tokens=800,
                google_api_key=os.getenv('GOOGLE_API_KEY')
            )
            
            # 测试股票分析
            print("📊 测试股票分析能力...")
            response = llm.invoke("""
            请用中文分析苹果公司(AAPL)的投资价值。
            请简要分析：
            1. 公司优势
            2. 主要风险
            3. 投资建议
            """)
            
            if response and response.content and len(response.content) > 100:
                print("✅ 股票分析测试成功")
                print(f"   响应长度: {len(response.content)} 字符")
                print(f"   响应预览: {response.content[:200]}...")
                return best_model
            else:
                print("❌ 股票分析测试失败")
                return None
                
        except Exception as e:
            print(f"❌ 详细测试失败: {e}")
            return None
    
    return None

def main():
    """主函数"""
    print("🧪 Gemini模型诊断")
    print("=" * 70)
    
    # 测试所有模型
    working_models = test_gemini_models()
    
    # 显示结果
    print(f"\n📊 测试结果总结:")
    print("=" * 50)
    
    if working_models:
        print(f"✅ 找到 {len(working_models)} 个可用模型:")
        for model in working_models:
            direct_status = "✅" if model['direct'] else "❌"
            langchain_status = "✅" if model['langchain'] else "❌"
            print(f"   {model['name']}: 直接API {direct_status} | LangChain {langchain_status}")
        
        # 测试最佳模型
        best_model = test_best_working_model(working_models)
        
        if best_model:
            print(f"\n🎉 推荐使用模型: {best_model}")
            print(f"\n💡 配置建议:")
            print(f"   1. 在Web界面中选择'Google'作为LLM提供商")
            print(f"   2. 使用模型名称: {best_model}")
            print(f"   3. 该模型已通过股票分析测试")
        else:
            print(f"\n⚠️ 虽然找到可用模型，但详细测试失败")
            print(f"   建议使用: {working_models[0]['name']}")
    else:
        print("❌ 没有找到任何可用的Gemini模型")
        print("💡 可能的原因:")
        print("   1. API密钥权限不足")
        print("   2. 网络连接问题")
        print("   3. 模型名称已更新")
        print("   4. API配额限制")

if __name__ == "__main__":
    main()
