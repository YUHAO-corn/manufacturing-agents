#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据流测试
验证数据源架构是否正常工作
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_manufacturing_data_service():
    """测试制造业数据服务"""
    print("🔄 测试制造业数据服务...")
    
    try:
        from manufacturing_data_service import ManufacturingDataService
        
        service = ManufacturingDataService()
        
        # 测试产品基础信息
        product_info = service.get_product_basic_info('P0001')
        if product_info:
            print(f"✅ 产品基础信息: {product_info['name']}")
        else:
            print("❌ 产品基础信息获取失败")
            return False
        
        # 测试供应链数据
        supply_chain = service.get_supply_chain_data('P0001')
        print(f"✅ 供应链数据: {len(supply_chain['suppliers'])}个供应商")
        
        # 测试需求预测
        demand_forecast = service.get_demand_forecast_data('P0001', '2024-01-01', '2024-01-31')
        print(f"✅ 需求预测: {len(demand_forecast['forecasts'])}天预测")
        
        # 测试库存数据
        inventory = service.get_inventory_data('P0001')
        print(f"✅ 库存数据: {len(inventory['warehouses'])}个仓库")
        
        # 测试市场价格
        market_price = service.get_market_price_data('P0001', '2024-01-01', '2024-01-31')
        print(f"✅ 市场价格: {len(market_price['price_history'])}天价格")
        
        return True
        
    except Exception as e:
        print(f"❌ 制造业数据服务测试失败: {e}")
        return False

def test_supply_chain_provider():
    """测试供应链数据提供器"""
    print("\n🔄 测试供应链数据提供器...")
    
    try:
        from supply_chain_data import SupplyChainDataProvider
        
        provider = SupplyChainDataProvider()
        
        # 测试供应商信息
        supplier_info = provider.get_supplier_info('SUP001')
        print(f"✅ 供应商信息: {supplier_info['supplier_name']}")
        
        # 测试交货表现
        delivery_performance = provider.get_delivery_performance('SUP001')
        print(f"✅ 交货表现: {delivery_performance['evaluation_period']}")
        
        # 测试风险评估
        risk_assessment = provider.get_supply_risk_assessment('P0001')
        print(f"✅ 风险评估: {risk_assessment['overall_risk_level']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 供应链数据提供器测试失败: {e}")
        return False

def test_demand_forecast_provider():
    """测试需求预测数据提供器"""
    print("\n🔄 测试需求预测数据提供器...")
    
    try:
        from demand_forecast_data import DemandForecastDataProvider
        
        provider = DemandForecastDataProvider()
        
        # 测试需求预测
        demand_forecast = provider.get_demand_forecast('P0001', 30)
        print(f"✅ 需求预测: {len(demand_forecast['forecasts'])}天预测")
        
        # 测试趋势分析
        trend_analysis = provider.get_demand_trend_analysis('P0001')
        print(f"✅ 趋势分析: {trend_analysis['trend_analysis']['overall_trend']}")
        
        # 测试驱动因素
        demand_drivers = provider.get_market_demand_drivers('P0001')
        print(f"✅ 驱动因素: {len(demand_drivers['demand_drivers'])}个因素")
        
        return True
        
    except Exception as e:
        print(f"❌ 需求预测数据提供器测试失败: {e}")
        return False

def test_inventory_provider():
    """测试库存数据提供器"""
    print("\n🔄 测试库存数据提供器...")
    
    try:
        from inventory_data import InventoryDataProvider
        
        provider = InventoryDataProvider()
        
        # 测试库存状态
        inventory_status = provider.get_inventory_status('P0001')
        print(f"✅ 库存状态: {inventory_status['total_inventory']['current_stock']}库存")
        
        # 测试周转率
        turnover = provider.get_inventory_turnover('P0001')
        print(f"✅ 周转率: {turnover['annual_metrics']['annual_turnover_rate']}")
        
        # 测试ABC分析
        abc_analysis = provider.get_abc_analysis()
        print(f"✅ ABC分析: {len(abc_analysis['products'])}个产品")
        
        return True
        
    except Exception as e:
        print(f"❌ 库存数据提供器测试失败: {e}")
        return False

def test_production_provider():
    """测试生产数据提供器"""
    print("\n🔄 测试生产数据提供器...")
    
    try:
        from production_data import ProductionDataProvider
        
        provider = ProductionDataProvider()
        
        # 测试生产计划
        production_schedule = provider.get_production_schedule('P0001')
        print(f"✅ 生产计划: {len(production_schedule['schedules'])}天计划")
        
        # 测试产能分析
        capacity = provider.get_production_capacity('P0001')
        print(f"✅ 产能分析: {capacity['capacity_summary']['overall_utilization']}%利用率")
        
        # 测试质量指标
        quality = provider.get_quality_metrics('P0001')
        print(f"✅ 质量指标: {quality['quality_summary']['average_quality_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 生产数据提供器测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始测试制造业数据流架构...")
    print("=" * 60)
    
    tests = [
        ("制造业数据服务", test_manufacturing_data_service),
        ("供应链数据提供器", test_supply_chain_provider),
        ("需求预测数据提供器", test_demand_forecast_provider),
        ("库存数据提供器", test_inventory_provider),
        ("生产数据提供器", test_production_provider)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(tests)} 测试通过")
    
    if passed == len(tests):
        print("🎉 所有测试通过! 数据流架构正常工作!")
    else:
        print("⚠️  部分测试失败，请检查相关组件")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 