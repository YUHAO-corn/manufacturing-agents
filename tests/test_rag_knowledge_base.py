#!/usr/bin/env python3
"""
RAG知识库集成测试
验证Dify知识库的实际可用性
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
tradingagents_root = project_root / "TradingAgents-CN"
sys.path.insert(0, str(tradingagents_root))

# 加载环境变量
load_dotenv(tradingagents_root / ".env", override=True)

def test_dify_api_connection():
    """测试Dify API连接"""
    print("🔗 测试Dify API连接...")
    
    try:
        # 使用默认配置
        api_key = "dataset-GBsvcytxCi8fl4eDYfsV7Rfq"
        dataset_id = "727a9b2e-37cb-4971-bb9b-83955cc464b5"
        base_url = "https://api.dify.ai/v1"
        
        url = f"{base_url}/datasets/{dataset_id}/retrieve"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 简单测试查询
        payload = {
            "query": "制造业",
            "retrieval_model": {
                "search_method": "hybrid_search",
                "reranking_enable": False,
                "top_k": 3,
                "score_threshold_enabled": True,
                "score_threshold": 0.6
            }
        }
        
        print(f"📡 调用Dify API: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print(f"🌐 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            records_count = len(data.get("records", []))
            print(f"✅ Dify API连接成功")
            print(f"📊 查询结果数量: {records_count}")
            return True, data
        else:
            print(f"❌ Dify API错误: {response.status_code}")
            print(f"错误内容: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Dify API连接异常: {str(e)}")
        return False, None

def test_manufacturing_toolkit_integration():
    """测试ManufacturingToolkit集成"""
    print("\n🔧 测试ManufacturingToolkit集成...")
    
    try:
        from manufacturingagents.manufacturingagents.utils.manufacturing_toolkit import ManufacturingToolkit
        from manufacturingagents.default_config import DEFAULT_CONFIG
        
        # 创建配置
        config = DEFAULT_CONFIG.copy()
        
        # 创建工具包实例
        toolkit = ManufacturingToolkit(config)
        print("✅ ManufacturingToolkit实例创建成功")
        
        # 测试知识库查询
        test_queries = [
            "什么是EOQ模型？",
            "制造业补货决策的关键因素",
            "安全库存如何计算？"
        ]
        
        results = {}
        for query in test_queries:
            print(f"\n📝 测试查询: {query}")
            result = toolkit.query_manufacturing_knowledge(query)
            
            try:
                result_data = json.loads(result)
                data_source = result_data.get("data_source", "unknown")
                total_results = result_data.get("total_results", 0)
                
                print(f"   数据源: {data_source}")
                print(f"   结果数量: {total_results}")
                
                if total_results > 0:
                    first_result = result_data.get("results", [{}])[0]
                    title = first_result.get("title", "无标题")
                    content_preview = first_result.get("content", "")[:100]
                    print(f"   首个结果: {title}")
                    print(f"   内容预览: {content_preview}...")
                
                results[query] = {
                    "success": True,
                    "data_source": data_source,
                    "total_results": total_results
                }
                
            except json.JSONDecodeError:
                print(f"   ❌ 返回结果不是有效JSON")
                results[query] = {"success": False, "error": "Invalid JSON"}
        
        return True, results
        
    except Exception as e:
        print(f"❌ ManufacturingToolkit测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False, None

def test_intelligent_agent_integration():
    """测试智能体集成"""
    print("\n🤖 测试智能体集成...")
    
    try:
        from manufacturingagents.manufacturingagents.analysts.market_environment_analyst import create_market_environment_analyst
        from manufacturingagents.manufacturingagents.utils.manufacturing_toolkit import ManufacturingToolkit
        from manufacturingagents.default_config import DEFAULT_CONFIG
        
        # 创建配置
        config = DEFAULT_CONFIG.copy()
        toolkit = ManufacturingToolkit(config)
        
        print("✅ 工具包创建成功")
        
        # 检查智能体是否能获取工具
        tools = [
            toolkit.get_macro_economic_data,
            toolkit.get_raw_material_prices,
            toolkit.query_manufacturing_knowledge,
        ]
        
        print(f"📊 市场环境分析师可用工具数量: {len(tools)}")
        
        # 检查知识库查询工具是否存在
        knowledge_tool = toolkit.query_manufacturing_knowledge
        print(f"✅ 知识库查询工具: {knowledge_tool.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 智能体集成测试失败: {str(e)}")
        return False

def analyze_rag_architecture_status():
    """分析RAG架构搭建状态"""
    print("\n📊 RAG架构搭建状态分析")
    print("=" * 50)
    
    # 检查代码文件是否存在
    files_to_check = [
        "TradingAgents-CN/tradingagents/manufacturingagents/utils/manufacturing_toolkit.py",
        "TradingAgents-CN/tradingagents/manufacturingagents/analysts/market_environment_analyst.py",
        "TradingAgents-CN/tradingagents/manufacturingagents/prompts/prompt_manager.py",
    ]
    
    for file_path in files_to_check:
        full_path = project_root / file_path
        exists = full_path.exists()
        print(f"{'✅' if exists else '❌'} {file_path}: {'存在' if exists else '不存在'}")
    
    return True

def main():
    """主测试函数"""
    print("🧪 制造业RAG知识库集成测试")
    print("=" * 60)
    
    # 分析架构状态
    analyze_rag_architecture_status()
    
    # 运行测试
    results = {}
    
    # 测试1: Dify API连接
    print("\n" + "="*60)
    api_success, api_data = test_dify_api_connection()
    results['Dify API连接'] = api_success
    
    # 测试2: ManufacturingToolkit集成  
    print("\n" + "="*60)
    toolkit_success, toolkit_data = test_manufacturing_toolkit_integration()
    results['ManufacturingToolkit集成'] = toolkit_success
    
    # 测试3: 智能体集成
    print("\n" + "="*60)
    agent_success = test_intelligent_agent_integration()
    results['智能体集成'] = agent_success
    
    # 总结结果
    print(f"\n📊 RAG知识库测试结果总结:")
    print("=" * 50)
    
    for test_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    successful_tests = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 总体结果: {successful_tests}/{total_tests} 测试通过")
    
    # 详细分析
    print(f"\n💡 架构搭建情况分析:")
    if successful_tests == total_tests:
        print("🎉 RAG知识库架构完全搭建成功！")
        print("   ✅ 代码架构已完成")
        print("   ✅ API集成已就绪") 
        print("   ✅ 智能体已配置")
        print("   ✅ 知识库查询功能正常")
    elif successful_tests >= 2:
        print("⚠️ RAG架构基本搭建完成，但存在问题:")
        if not results['Dify API连接']:
            print("   ❌ Dify知识库可能未创建或API密钥有误")
        if not results['ManufacturingToolkit集成']:
            print("   ❌ 工具包集成存在问题")
        if not results['智能体集成']:
            print("   ❌ 智能体配置存在问题")
    else:
        print("❌ RAG架构搭建存在重大问题，需要进一步排查")
    
    print(f"\n📋 下一步行动建议:")
    if not results.get('Dify API连接', False):
        print("   1. 创建真实的Dify知识库并上传制造业文档")
        print("   2. 获取正确的API密钥和dataset ID")
    if results.get('ManufacturingToolkit集成', False):
        print("   3. 架构代码已就绪，可以开始填充真实知识库内容")
    else:
        print("   3. 检查ManufacturingToolkit代码实现")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    main() 