#!/usr/bin/env python3
"""
配置管理功能演示
展示如何使用配置管理和成本统计功能
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from manufacturingagents.config.config_manager import config_manager, token_tracker


def demo_model_management():
    """演示模型管理功能"""
    print("🤖 模型管理演示")
    print("=" * 50)
    
    # 查看当前模型配置
    models = config_manager.get_enabled_models()
    print(f"📋 当前启用的模型数量: {len(models)}")
    
    for model in models:
        print(f"  🔹 {model.provider} - {model.model_name}")
        print(f"     最大Token: {model.max_tokens}, 温度: {model.temperature}")
    
    # 获取特定模型配置
    qwen_model = config_manager.get_model_by_name("dashscope", "qwen-plus-latest")
    if qwen_model:
        print(f"\n🎯 通义千问Plus配置:")
        print(f"  API密钥: {'已配置' if qwen_model.api_key else '未配置'}")
        print(f"  最大Token: {qwen_model.max_tokens}")
        print(f"  状态: {'启用' if qwen_model.enabled else '禁用'}")


def demo_cost_calculation():
    """演示成本计算功能"""
    print("\n💰 成本计算演示")
    print("=" * 50)
    
    # 测试不同模型的成本
    test_cases = [
        ("dashscope", "qwen-turbo", 1000, 500, "快速分析"),
        ("dashscope", "qwen-plus", 2000, 1000, "标准分析"),
        ("dashscope", "qwen-max", 3000, 1500, "深度分析"),
        ("openai", "gpt-3.5-turbo", 1000, 500, "GPT-3.5分析"),
        ("google", "gemini-pro", 1000, 500, "Gemini分析"),
    ]
    
    print("📊 不同模型成本对比:")
    print(f"{'模型':<20} {'输入Token':<10} {'输出Token':<10} {'成本(¥)':<10} {'用途'}")
    print("-" * 70)
    
    for provider, model, input_tokens, output_tokens, purpose in test_cases:
        cost = config_manager.calculate_cost(provider, model, input_tokens, output_tokens)
        model_name = f"{provider}/{model}"
        print(f"{model_name:<20} {input_tokens:<10} {output_tokens:<10} {cost:<10.4f} {purpose}")


def demo_usage_tracking():
    """演示使用跟踪功能"""
    print("\n📈 使用跟踪演示")
    print("=" * 50)
    
    # 模拟几次分析的Token使用
    demo_sessions = [
        {
            "provider": "dashscope",
            "model": "qwen-turbo",
            "input_tokens": 1500,
            "output_tokens": 800,
            "analysis_type": "美股_analysis",
            "stock": "AAPL"
        },
        {
            "provider": "dashscope", 
            "model": "qwen-plus",
            "input_tokens": 2500,
            "output_tokens": 1200,
            "analysis_type": "A股_analysis",
            "stock": "000001"
        },
        {
            "provider": "google",
            "model": "gemini-pro",
            "input_tokens": 1800,
            "output_tokens": 900,
            "analysis_type": "美股_analysis",
            "stock": "TSLA"
        }
    ]
    
    print("🔄 模拟分析会话...")
    total_cost = 0
    
    for i, session in enumerate(demo_sessions, 1):
        session_id = f"demo_session_{i}_{datetime.now().strftime('%H%M%S')}"
        
        # 记录使用
        record = token_tracker.track_usage(
            provider=session["provider"],
            model_name=session["model"],
            input_tokens=session["input_tokens"],
            output_tokens=session["output_tokens"],
            session_id=session_id,
            analysis_type=session["analysis_type"]
        )
        
        if record:
            total_cost += record.cost
            print(f"  📝 会话{i}: {session['stock']} - {session['provider']}/{session['model']}")
            print(f"      Token: {session['input_tokens']}+{session['output_tokens']}, 成本: ¥{record.cost:.4f}")
    
    print(f"\n💰 总成本: ¥{total_cost:.4f}")


def demo_usage_statistics():
    """演示使用统计功能"""
    print("\n📊 使用统计演示")
    print("=" * 50)
    
    # 获取使用统计
    stats = config_manager.get_usage_statistics(30)
    
    print(f"📈 最近30天统计:")
    print(f"  总请求数: {stats['total_requests']}")
    print(f"  总成本: ¥{stats['total_cost']:.4f}")
    print(f"  输入Token: {stats['total_input_tokens']:,}")
    print(f"  输出Token: {stats['total_output_tokens']:,}")
    
    if stats['provider_stats']:
        print(f"\n🏢 按供应商统计:")
        for provider, data in stats['provider_stats'].items():
            print(f"  {provider}:")
            print(f"    请求数: {data['requests']}")
            print(f"    成本: ¥{data['cost']:.4f}")
            print(f"    平均成本: ¥{data['cost']/data['requests']:.6f}/请求")


def demo_cost_estimation():
    """演示成本估算功能"""
    print("\n🔮 成本估算演示")
    print("=" * 50)
    
    # 估算不同分析场景的成本
    scenarios = [
        {
            "name": "快速分析 (1个分析师)",
            "analysts": 1,
            "depth": "快速",
            "input_per_analyst": 1000,
            "output_per_analyst": 500
        },
        {
            "name": "标准分析 (3个分析师)",
            "analysts": 3,
            "depth": "标准", 
            "input_per_analyst": 2000,
            "output_per_analyst": 1000
        },
        {
            "name": "深度分析 (5个分析师)",
            "analysts": 5,
            "depth": "深度",
            "input_per_analyst": 3000,
            "output_per_analyst": 1500
        }
    ]
    
    models_to_test = [
        ("dashscope", "qwen-turbo"),
        ("dashscope", "qwen-plus"),
        ("openai", "gpt-3.5-turbo"),
        ("google", "gemini-pro")
    ]
    
    print("💡 不同分析场景的成本估算:")
    print()
    
    for scenario in scenarios:
        print(f"📋 {scenario['name']}")
        print(f"{'模型':<20} {'预估成本':<10} {'说明'}")
        print("-" * 40)
        
        total_input = scenario['analysts'] * scenario['input_per_analyst']
        total_output = scenario['analysts'] * scenario['output_per_analyst']
        
        for provider, model in models_to_test:
            cost = token_tracker.estimate_cost(provider, model, total_input, total_output)
            model_name = f"{provider}/{model}"
            print(f"{model_name:<20} ¥{cost:<9.4f} {total_input}+{total_output} tokens")
        
        print()


def demo_settings_management():
    """演示设置管理功能"""
    print("\n⚙️ 设置管理演示")
    print("=" * 50)
    
    # 查看当前设置
    settings = config_manager.load_settings()
    
    print("🔧 当前系统设置:")
    for key, value in settings.items():
        print(f"  {key}: {value}")
    
    # 演示设置修改
    print(f"\n📝 当前成本警告阈值: ¥{settings.get('cost_alert_threshold', 100)}")
    print(f"📝 当前默认模型: {settings.get('default_provider', 'dashscope')}/{settings.get('default_model', 'qwen-turbo')}")
    print(f"📝 成本跟踪状态: {'启用' if settings.get('enable_cost_tracking', True) else '禁用'}")


def main():
    """主演示函数"""
    print("🎯 TradingAgents-CN 配置管理功能演示")
    print("=" * 60)
    print("本演示将展示配置管理和成本统计的各项功能")
    print()
    
    try:
        # 演示各项功能
        demo_model_management()
        demo_cost_calculation()
        demo_usage_tracking()
        demo_usage_statistics()
        demo_cost_estimation()
        demo_settings_management()
        
        print("\n🎉 演示完成！")
        print("=" * 60)
        print("💡 使用建议:")
        print("  1. 通过Web界面管理配置更加直观")
        print("  2. 定期查看使用统计，优化成本")
        print("  3. 根据需求选择合适的模型")
        print("  4. 设置合理的成本警告阈值")
        print()
        print("🌐 启动Web界面: python -m streamlit run web/app.py")
        print("📚 详细文档: docs/guides/config-management-guide.md")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        print(f"错误详情: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
