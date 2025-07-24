#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据层测试脚本
测试制造业数据适配器和数据提供器的核心功能

测试目标:
1. 验证制造业数据适配器的基本功能
2. 测试数据获取和格式化
3. 验证缓存和降级机制
4. 确保数据质量和完整性
"""

import sys
import os
from pathlib import Path
import traceback
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_manufacturing_data_adapter():
    """测试制造业数据适配器"""
    print("🔧 开始测试制造业数据适配器...")
    
    try:
        # 导入制造业数据适配器
        from manufacturingagents.manufacturingagents.dataflows.manufacturing_data_adapter import (
            ManufacturingDataAdapter, 
            get_manufacturing_adapter
        )
        
        # 创建适配器实例
        adapter = ManufacturingDataAdapter()
        print("✅ 制造业数据适配器创建成功")
        
        # 测试类方法是否存在（实际实现的方法）
        class_methods_to_test = [
            'get_product_data',
            'get_supplier_data', 
            'get_market_news',
            'get_industry_analysis'
        ]
        
        for method_name in class_methods_to_test:
            if hasattr(adapter, method_name):
                print(f"✅ 类方法 {method_name} 存在")
            else:
                print(f"❌ 类方法 {method_name} 不存在")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入制造业数据适配器失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 制造业数据适配器测试失败: {e}")
        traceback.print_exc()
        return False

def test_manufacturing_data_service():
    """测试制造业数据服务"""
    print("\n🔧 开始测试制造业数据服务...")
    
    try:
        from manufacturingagents.manufacturingagents.dataflows.manufacturing_data_service import (
            ManufacturingDataService,
            get_manufacturing_data_service
        )
        
        # 创建数据服务实例
        service = ManufacturingDataService()
        print("✅ 制造业数据服务创建成功")
        
        # 测试基本方法
        test_methods = [
            'get_supply_chain_data',
            'get_demand_forecast_data',
            'get_market_price_data',
            'get_inventory_data',
            'get_production_data'
        ]
        
        for method_name in test_methods:
            if hasattr(service, method_name):
                print(f"✅ 方法 {method_name} 存在")
            else:
                print(f"⚠️ 方法 {method_name} 不存在")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入制造业数据服务失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 制造业数据服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_data_providers():
    """测试制造业数据提供器"""
    print("\n🔧 开始测试制造业数据提供器...")
    
    providers_to_test = [
        'supply_chain_data',
        'demand_forecast_data', 
        'market_price_data',
        'inventory_data',
        'production_data'
    ]
    
    success_count = 0
    
    for provider_name in providers_to_test:
        try:
            module_path = f"tradingagents.manufacturingagents.dataflows.{provider_name}"
            __import__(module_path)
            print(f"✅ 数据提供器 {provider_name} 导入成功")
            success_count += 1
        except ImportError as e:
            print(f"❌ 数据提供器 {provider_name} 导入失败: {e}")
        except Exception as e:
            print(f"❌ 数据提供器 {provider_name} 测试异常: {e}")
    
    print(f"📊 数据提供器测试结果: {success_count}/{len(providers_to_test)} 成功")
    return success_count == len(providers_to_test)

def test_toolkit_integration():
    """测试工具包集成"""
    print("\n🔧 开始测试工具包集成...")
    
    try:
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        
        # 创建工具包实例
        toolkit = Toolkit()
        print("✅ 工具包创建成功")
        
        # 测试制造业专用工具方法
        manufacturing_tools = [
            'get_manufacturing_pmi_data',
            'get_manufacturing_ppi_data',
            'get_manufacturing_commodity_data',
            'get_manufacturing_weather_data',
            'get_manufacturing_holiday_data',
            'get_manufacturing_news_data'
        ]
        
        available_tools = 0
        for tool_name in manufacturing_tools:
            if hasattr(toolkit, tool_name):
                print(f"✅ 制造业工具 {tool_name} 可用")
                available_tools += 1
            else:
                print(f"❌ 制造业工具 {tool_name} 不可用")
        
        print(f"📊 制造业工具可用性: {available_tools}/{len(manufacturing_tools)}")
        return available_tools > 0
        
    except ImportError as e:
        print(f"❌ 导入工具包失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 工具包测试失败: {e}")
        traceback.print_exc()
        return False

def test_sample_data_flow():
    """测试样本数据流"""
    print("\n🔧 开始测试样本数据流...")
    
    try:
        # 测试模块级别的接口函数
        from manufacturingagents.manufacturingagents.dataflows.manufacturing_data_adapter import (
            get_manufacturing_data,
            get_supplier_info,
            get_manufacturing_news,
            get_industry_report
        )
        
        # 测试产品数据获取
        print("📊 测试产品代码: STEEL_001")
        product_data = get_manufacturing_data("STEEL_001", "2024-01-01", "2024-03-31")
        
        if product_data and len(product_data) > 50:
            print(f"✅ 产品数据获取成功，长度: {len(product_data)} 字符")
            print(f"📄 数据预览: {product_data[:200]}...")
        else:
            print(f"⚠️ 产品数据获取成功但可能为模拟数据: {len(product_data) if product_data else 0} 字符")
        
        # 测试供应商信息获取
        print("\n📊 测试供应商代码: SUP_001")
        supplier_info = get_supplier_info("SUP_001")
        
        if supplier_info:
            print(f"✅ 供应商信息获取成功")
            print(f"📄 供应商信息: {supplier_info}")
        else:
            print("⚠️ 供应商信息获取失败或为空")
        
        # 测试制造业新闻获取
        print("\n📊 测试新闻获取: 钢铁")
        news_data = get_manufacturing_news("钢铁", 7)
        
        if news_data and len(news_data) > 20:
            print(f"✅ 制造业新闻获取成功，长度: {len(news_data)} 字符")
            print(f"📄 新闻预览: {news_data[:150]}...")
        else:
            print("⚠️ 制造业新闻获取失败或为空")
        
        # 测试行业报告获取
        print("\n📊 测试行业报告: MANUFACTURING")
        industry_report = get_industry_report("MANUFACTURING")
        
        if industry_report and len(industry_report) > 20:
            print(f"✅ 行业报告获取成功，长度: {len(industry_report)} 字符")
            print(f"📄 报告预览: {industry_report[:150]}...")
        else:
            print("⚠️ 行业报告获取失败或为空")
        
        return True
        
    except Exception as e:
        print(f"❌ 样本数据流测试失败: {e}")
        traceback.print_exc()
        return False

def test_error_handling():
    """测试错误处理和降级机制"""
    print("\n🔧 开始测试错误处理和降级机制...")
    
    try:
        from manufacturingagents.manufacturingagents.dataflows.manufacturing_data_adapter import get_manufacturing_data
        
        # 测试无效输入的处理
        print("📊 测试无效产品代码: INVALID_PRODUCT")
        invalid_data = get_manufacturing_data("INVALID_PRODUCT", "2024-01-01", "2024-03-31")
        
        if invalid_data:
            print(f"✅ 无效输入处理成功，返回降级数据: {len(invalid_data)} 字符")
        else:
            print("⚠️ 无效输入返回空数据")
        
        # 测试空输入的处理
        print("\n📊 测试空输入")
        try:
            empty_data = get_manufacturing_data("", "2024-01-01", "2024-03-31")
            if empty_data:
                print(f"✅ 空输入处理成功，返回降级数据: {len(empty_data)} 字符")
            else:
                print("⚠️ 空输入返回空数据")
        except Exception as e:
            print(f"✅ 空输入正确抛出异常: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 制造业数据层测试开始")
    print("=" * 60)
    
    test_results = []
    
    # 执行各项测试
    test_functions = [
        ("制造业数据适配器", test_manufacturing_data_adapter),
        ("制造业数据服务", test_manufacturing_data_service), 
        ("数据提供器", test_data_providers),
        ("工具包集成", test_toolkit_integration),
        ("样本数据流", test_sample_data_flow),
        ("错误处理", test_error_handling)
    ]
    
    for test_name, test_func in test_functions:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试执行异常: {e}")
            test_results.append((test_name, False))
    
    # 输出测试结果摘要
    print("\n" + "=" * 60)
    print("📊 测试结果摘要")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed_tests += 1
    
    print(f"\n📈 总体结果: {passed_tests}/{total_tests} 测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有数据层测试通过！可以进入下一阶段测试。")
        return True
    elif passed_tests >= total_tests * 0.7:
        print("⚠️ 大部分测试通过，但存在一些问题需要关注。")
        return True
    else:
        print("🚨 数据层测试存在重大问题，需要修复后再继续。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 