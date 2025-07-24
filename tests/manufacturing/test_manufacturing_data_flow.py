#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据流诊断测试脚本
帮助检查从API到智能体的完整数据链路
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """检查环境变量配置"""
    print("🔍 === 1. 环境变量检查 ===")
    
    required_keys = {
        'DASHSCOPE_API_KEY': 'DashScope API密钥（阿里百炼）',
        'COZE_API_KEY': 'Coze API密钥（天气、新闻、节假日）',
        'TUSHARE_TOKEN': 'TuShare Token（PMI、PPI数据）'
    }
    
    all_configured = True
    for key, description in required_keys.items():
        value = os.getenv(key)
        if value:
            print(f"✅ {key}: {description} - 已配置")
        else:
            print(f"❌ {key}: {description} - 未配置")
            all_configured = False
    
    return all_configured

def test_direct_api_calls():
    """测试直接API调用"""
    print("\n🌐 === 2. 直接API调用测试 ===")
    
    # 测试Coze天气API
    print("\n🌤️ 测试Coze天气API...")
    try:
        import requests
        coze_api_key = os.getenv('COZE_API_KEY')
        if coze_api_key:
            headers = {
                "Authorization": f"Bearer {coze_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "workflow_id": "7528239823611281448",
                "parameters": {
                    'dailyForecast': True,
                    'place': '广州',
                    'realtime': False
                }
            }
            response = requests.post("https://api.coze.cn/v1/workflow/run", 
                                   headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Coze天气API调用成功: {response.status_code}")
            else:
                print(f"❌ Coze天气API调用失败: HTTP {response.status_code}")
        else:
            print("❌ COZE_API_KEY未配置，跳过测试")
    except Exception as e:
        print(f"❌ Coze天气API测试异常: {str(e)}")
    
    # 测试TuShare API
    print("\n📈 测试TuShare API...")
    try:
        import tushare as ts
        tushare_token = os.getenv('TUSHARE_TOKEN')
        if tushare_token:
            ts.set_token(tushare_token)
            pro = ts.pro_api()
            result = pro.cn_pmi(start_m='202501', end_m='202501', fields='month,pmi010000')
            if not result.empty:
                print(f"✅ TuShare API调用成功: 获取到{len(result)}条PMI数据")
            else:
                print("⚠️ TuShare API调用成功但无数据")
        else:
            print("❌ TUSHARE_TOKEN未配置，跳过测试")
    except Exception as e:
        print(f"❌ TuShare API测试异常: {str(e)}")

def test_interface_layer():
    """测试interface层函数"""
    print("\n🔧 === 3. Interface层函数测试 ===")
    
    try:
        from manufacturingagents.dataflows import interface
        
        # 测试天气接口
        print("\n🌤️ 测试interface天气函数...")
        try:
            result = interface.get_manufacturing_weather_interface("广州", "2025-01-17")
            if "❌" not in result:
                print(f"✅ interface天气函数正常: 返回{len(result)}字符")
            else:
                print(f"❌ interface天气函数错误: {result[:200]}...")
        except Exception as e:
            print(f"❌ interface天气函数异常: {str(e)}")
        
        # 测试经济数据接口
        print("\n📈 测试interface经济数据函数...")
        try:
            result = interface.get_manufacturing_economic_interface("pmi", "最近3个月")
            if "❌" not in result:
                print(f"✅ interface经济数据函数正常: 返回{len(result)}字符")
            else:
                print(f"❌ interface经济数据函数错误: {result[:200]}...")
        except Exception as e:
            print(f"❌ interface经济数据函数异常: {str(e)}")
            
    except ImportError as e:
        print(f"❌ 无法导入interface模块: {e}")

def test_toolkit_layer():
    """测试toolkit层工具"""
    print("\n🛠️ === 4. Toolkit层工具测试 ===")
    
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        toolkit = Toolkit()
        
        # 测试制造业天气工具
        print("\n🌤️ 测试toolkit天气工具...")
        try:
            result = toolkit.get_manufacturing_weather_data("广州")
            if "❌" not in result:
                print(f"✅ toolkit天气工具正常: 返回{len(result)}字符")
            else:
                print(f"❌ toolkit天气工具错误: {result[:200]}...")
        except Exception as e:
            print(f"❌ toolkit天气工具异常: {str(e)}")
        
        # 测试制造业PMI工具
        print("\n📈 测试toolkit PMI工具...")
        try:
            result = toolkit.get_manufacturing_pmi_data("最近3个月")
            if "❌" not in result:
                print(f"✅ toolkit PMI工具正常: 返回{len(result)}字符")
            else:
                print(f"❌ toolkit PMI工具错误: {result[:200]}...")
        except Exception as e:
            print(f"❌ toolkit PMI工具异常: {str(e)}")
            
    except ImportError as e:
        print(f"❌ 无法导入toolkit模块: {e}")

def test_agent_layer():
    """测试智能体层调用"""
    print("\n🤖 === 5. 智能体层测试 ===")
    
    try:
        from manufacturingagents.manufacturingagents.analysts.market_environment_analyst import create_market_environment_analyst
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        from manufacturingagents.llm_adapters.dashscope_adapter import create_llm
        
        # 创建LLM和工具包
        print("\n🧠 初始化LLM和工具包...")
        llm = create_llm("qwen-turbo")
        toolkit = Toolkit()
        
        # 创建市场环境分析师
        print("\n🌍 测试市场环境分析师...")
        analyst = create_market_environment_analyst(llm, toolkit)
        
        # 模拟状态
        test_state = {
            "product_type": "空调",
            "company_name": "美的",
            "analysis_date": "2025-01-17",
            "messages": [("human", "分析美的空调的市场环境")]
        }
        
        # 执行分析师节点
        try:
            result = analyst(test_state)
            if result:
                print(f"✅ 市场环境分析师测试成功")
                print(f"📊 返回消息数量: {len(result.get('messages', []))}")
            else:
                print("❌ 市场环境分析师返回空结果")
        except Exception as e:
            print(f"❌ 市场环境分析师测试异常: {str(e)}")
            
    except ImportError as e:
        print(f"❌ 无法导入智能体模块: {e}")

def test_web_integration():
    """测试Web界面集成"""
    print("\n🌐 === 6. Web界面集成测试 ===")
    
    try:
        from web.utils.analysis_runner import run_manufacturing_analysis
        
        print("\n📦 测试制造业分析执行器...")
        try:
            # 模拟简单的分析参数
            result = run_manufacturing_analysis(
                brand_name="美的",
                product_category="空调",
                target_quarter="2025Q2",
                special_focus="市场环境分析",
                analysts=["market_environment_analyst"],
                research_depth=3,
                llm_provider="dashscope",
                llm_model="qwen-turbo",
                progress_callback=lambda msg, step=None, total=None: print(f"进度: {msg}")
            )
            
            if result and 'state' in result:
                print(f"✅ Web集成测试成功")
                print(f"📊 分析状态: {result['state'].get('product_type', 'N/A')}")
            else:
                print("❌ Web集成测试返回空结果")
                
        except Exception as e:
            print(f"❌ Web集成测试异常: {str(e)}")
            
    except ImportError as e:
        print(f"❌ 无法导入Web模块: {e}")

def main():
    """主诊断函数"""
    print("🏭 制造业数据流诊断工具")
    print("=" * 50)
    
    # 1. 环境检查
    env_ok = check_environment()
    
    # 2. 直接API测试
    test_direct_api_calls()
    
    # 3. Interface层测试
    test_interface_layer()
    
    # 4. Toolkit层测试
    test_toolkit_layer()
    
    # 5. 智能体层测试
    test_agent_layer()
    
    # 6. Web集成测试
    test_web_integration()
    
    print("\n📋 === 诊断总结 ===")
    if not env_ok:
        print("⚠️ 主要问题: API密钥配置不完整")
        print("💡 解决方案: 在.env文件中配置所有必需的API密钥")
    else:
        print("🎯 环境配置正常，请查看上述各层测试结果")
        print("💡 如果某一层失败，问题就在那一层的实现中")

if __name__ == "__main__":
    main() 