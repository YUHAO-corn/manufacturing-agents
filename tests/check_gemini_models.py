#!/usr/bin/env python3
"""
检查可用的Gemini模型
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

def list_available_models():
    """列出可用的Gemini模型"""
    try:
        print("🔍 检查可用的Gemini模型")
        print("=" * 50)
        
        import google.generativeai as genai
        
        # 配置API密钥
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            print("❌ Google API密钥未配置")
            return []
        
        genai.configure(api_key=google_api_key)
        
        # 列出所有可用模型
        print("📋 获取可用模型列表...")
        models = genai.list_models()
        
        available_models = []
        for model in models:
            print(f"   模型名称: {model.name}")
            print(f"   显示名称: {model.display_name}")
            print(f"   支持的方法: {model.supported_generation_methods}")
            print(f"   描述: {model.description}")
            print("-" * 40)
            
            # 检查是否支持generateContent
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        
        print(f"\n✅ 支持generateContent的模型: {len(available_models)}")
        for model in available_models:
            print(f"   - {model}")
        
        return available_models
        
    except Exception as e:
        print(f"❌ 获取模型列表失败: {e}")
        import traceback
        print(traceback.format_exc())
        return []

def test_specific_model(model_name):
    """测试特定模型"""
    try:
        print(f"\n🧪 测试模型: {model_name}")
        print("=" * 50)
        
        import google.generativeai as genai
        
        # 配置API密钥
        google_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        
        # 创建模型实例
        model = genai.GenerativeModel(model_name)
        
        print("✅ 模型实例创建成功")
        
        # 测试生成内容
        print("📝 测试内容生成...")
        response = model.generate_content("请用中文简单介绍一下人工智能的发展")
        
        if response and response.text:
            print("✅ 模型调用成功")
            print(f"   响应长度: {len(response.text)} 字符")
            print(f"   响应预览: {response.text[:200]}...")
            return True
        else:
            print("❌ 模型调用失败：无响应内容")
            return False
            
    except Exception as e:
        print(f"❌ 模型测试失败: {e}")
        return False

def test_langchain_with_correct_model(model_name):
    """使用正确的模型名称测试LangChain"""
    try:
        print(f"\n🧪 测试LangChain与模型: {model_name}")
        print("=" * 50)
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # 创建LangChain Gemini实例
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1,
            max_tokens=1000,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        print("✅ LangChain Gemini实例创建成功")
        
        # 测试调用
        print("📝 测试LangChain调用...")
        response = llm.invoke("请用中文分析一下苹果公司的投资价值")
        
        if response and response.content:
            print("✅ LangChain Gemini调用成功")
            print(f"   响应长度: {len(response.content)} 字符")
            print(f"   响应预览: {response.content[:200]}...")
            return True
        else:
            print("❌ LangChain Gemini调用失败：无响应内容")
            return False
            
    except Exception as e:
        print(f"❌ LangChain测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🧪 Gemini模型检查和测试")
    print("=" * 60)
    
    # 检查API密钥
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print("❌ Google API密钥未配置")
        return
    
    print(f"✅ Google API密钥已配置: {google_api_key[:20]}...")
    
    # 获取可用模型
    available_models = list_available_models()
    
    if not available_models:
        print("❌ 没有找到可用的模型")
        return
    
    # 测试第一个可用模型
    test_model = available_models[0]
    print(f"\n🎯 选择测试模型: {test_model}")
    
    # 测试直接API
    direct_success = test_specific_model(test_model)
    
    # 测试LangChain集成
    langchain_success = test_langchain_with_correct_model(test_model)
    
    # 总结结果
    print(f"\n📊 测试结果总结:")
    print("=" * 50)
    print(f"  可用模型数量: {len(available_models)}")
    print(f"  推荐模型: {test_model}")
    print(f"  直接API测试: {'✅ 通过' if direct_success else '❌ 失败'}")
    print(f"  LangChain集成: {'✅ 通过' if langchain_success else '❌ 失败'}")
    
    if direct_success and langchain_success:
        print(f"\n🎉 Gemini模型 {test_model} 完全可用！")
        print(f"\n💡 使用建议:")
        print(f"   1. 在配置中使用模型名称: {test_model}")
        print(f"   2. 替换所有 'gemini-pro' 为 '{test_model}'")
        print(f"   3. 确保API密钥有效且有足够配额")
    else:
        print(f"\n⚠️ 模型测试部分失败，请检查API密钥和网络连接")

if __name__ == "__main__":
    main()
