#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具管理器测试
Test Tool Manager

验证各智能体的工具配置和调用规范是否正确
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_tool_configurations():
    """测试工具配置"""
    try:
        from manufacturingagents.manufacturingagents.utils.tool_manager import (
            get_tool_manager, AgentRole, ToolType
        )
        
        print("🧪 [测试] 工具配置...")
        
        manager = get_tool_manager()
        
        # 验证工具配置
        expected_tools = [
            ("pmi_tool", ToolType.ECONOMIC_DATA, ["start_m", "end_m"]),
            ("ppi_tool", ToolType.ECONOMIC_DATA, ["start_m", "end_m"]),
            ("futures_tool", ToolType.ECONOMIC_DATA, ["ts_code", "freq"]),
            ("weather_tool", ToolType.WEATHER_DATA, ["place"]),
            ("news_tool", ToolType.NEWS_DATA, ["queries"]),
            ("holiday_tool", ToolType.HOLIDAY_DATA, ["start_date", "end_date"]),
            ("sentiment_tool", ToolType.SENTIMENT_DATA, ["keywords"])
        ]
        
        print("🔧 工具配置验证:")
        for tool_name, expected_type, expected_params in expected_tools:
            if tool_name in manager.tool_configs:
                config = manager.tool_configs[tool_name]
                
                # 验证工具类型
                if config.tool_type == expected_type:
                    print(f"  ✅ {tool_name}: 类型正确 ({expected_type.value})")
                else:
                    print(f"  ❌ {tool_name}: 类型错误，期望{expected_type.value}，实际{config.tool_type.value}")
                    return False
                
                # 验证必需参数
                for param in expected_params:
                    if param in config.required_params:
                        print(f"    ✅ 必需参数: {param}")
                    else:
                        print(f"    ❌ 缺少必需参数: {param}")
                        return False
            else:
                print(f"  ❌ 工具配置缺失: {tool_name}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 工具配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_tool_mappings():
    """测试智能体工具映射"""
    try:
        from manufacturingagents.manufacturingagents.utils.tool_manager import (
            get_tool_manager, AgentRole, ToolType
        )
        
        print("\n🧪 [测试] 智能体工具映射...")
        
        manager = get_tool_manager()
        
        # 验证每个智能体的工具配置
        test_cases = [
            (AgentRole.MARKET_ANALYST, ["pmi_tool", "ppi_tool", "news_tool"], ["weather_tool", "holiday_tool"]),
            (AgentRole.SUPPLY_CHAIN_ANALYST, ["futures_tool", "weather_tool"], ["news_tool", "holiday_tool"]),
            (AgentRole.DEMAND_FORECASTER, ["sentiment_tool", "holiday_tool", "weather_tool"], ["news_tool", "pmi_tool"]),
            (AgentRole.INVENTORY_MANAGER, ["holiday_tool", "weather_tool"], ["sentiment_tool", "news_tool"]),
            (AgentRole.PRODUCTION_PLANNER, ["pmi_tool", "futures_tool", "holiday_tool"], ["weather_tool", "news_tool"])
        ]
        
        print("👥 智能体工具映射验证:")
        for agent_role, expected_primary, expected_secondary in test_cases:
            agent_tools = manager.get_agent_tools(agent_role)
            
            # 验证主要工具
            actual_primary = [tool.tool_name for tool in agent_tools["primary_tools"]]
            if set(actual_primary) == set(expected_primary):
                print(f"  ✅ {agent_role.value}: 主要工具正确 ({len(expected_primary)}个)")
            else:
                print(f"  ❌ {agent_role.value}: 主要工具错误")
                print(f"    期望: {expected_primary}")
                print(f"    实际: {actual_primary}")
                return False
            
            # 验证次要工具
            actual_secondary = [tool.tool_name for tool in agent_tools["secondary_tools"]]
            if set(actual_secondary) == set(expected_secondary):
                print(f"    ✅ 次要工具正确 ({len(expected_secondary)}个)")
            else:
                print(f"    ❌ 次要工具错误")
                print(f"    期望: {expected_secondary}")
                print(f"    实际: {actual_secondary}")
                return False
            
            # 验证上下文要求
            context_reqs = agent_tools["context_requirements"]
            required_count = sum(1 for importance in context_reqs.values() if importance == "required")
            print(f"    ✅ 上下文要求: {required_count}个必需，{len(context_reqs)-required_count}个可选")
        
        return True
        
    except Exception as e:
        print(f"❌ 智能体工具映射测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tool_call_validation():
    """测试工具调用验证"""
    try:
        from manufacturingagents.manufacturingagents.utils.tool_manager import get_tool_manager
        
        print("\n🧪 [测试] 工具调用验证...")
        
        manager = get_tool_manager()
        
        # 测试用例：[工具名, 参数, 是否应该通过]
        test_cases = [
            # PMI工具测试
            ("pmi_tool", {"start_m": "202501", "end_m": "202506"}, True),
            ("pmi_tool", {"start_m": "202501"}, False),  # 缺少end_m
            ("pmi_tool", {"start_m": "", "end_m": "202506"}, False),  # 空参数
            
            # 天气工具测试
            ("weather_tool", {"place": "厦门"}, True),
            ("weather_tool", {}, False),  # 缺少place
            ("weather_tool", {"place": None}, False),  # place为None
            
            # 新闻工具测试
            ("news_tool", {"queries": ["格力空调", "美的冰箱"]}, True),
            ("news_tool", {"queries": "单个查询"}, True),  # 字符串也可以
            ("news_tool", {}, False),  # 缺少queries
            
            # 期货工具测试
            ("futures_tool", {"ts_code": "CU2507.SHF", "freq": "week"}, True),
            ("futures_tool", {"ts_code": "CU2507.SHF"}, False),  # 缺少freq
            
            # 未知工具测试
            ("unknown_tool", {"param": "value"}, False)
        ]
        
        print("✅ 工具调用验证:")
        for tool_name, params, expected_valid in test_cases:
            is_valid, issues = manager.validate_tool_call(tool_name, params)
            
            if is_valid == expected_valid:
                status = "✅ 正确"
                result = "通过" if is_valid else "拒绝"
                print(f"  {status}: {tool_name} = {result}")
            else:
                status = "❌ 错误"
                expected_result = "通过" if expected_valid else "拒绝"
                actual_result = "通过" if is_valid else "拒绝"
                print(f"  {status}: {tool_name} = 期望{expected_result}，实际{actual_result}")
                if issues:
                    print(f"    问题: {issues}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 工具调用验证测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tool_call_plan_generation():
    """测试工具调用计划生成"""
    try:
        from manufacturingagents.manufacturingagents.utils.tool_manager import (
            get_tool_manager, AgentRole
        )
        
        print("\n🧪 [测试] 工具调用计划生成...")
        
        manager = get_tool_manager()
        
        # 测试用例1: 市场分析师 - 完整上下文
        context1 = {
            "location": "厦门",
            "product_category": "空调",
            "time_range": "2025Q3",
            "api_parameters": {
                "pmi_params": {"start_m": "202501", "end_m": "202506"},
                "ppi_params": {"start_m": "202501", "end_m": "202506"},
                "news_params": {"activity_query": "空调促销", "area_news_query": "厦门制造业"}
            }
        }
        
        plan1 = manager.generate_tool_call_plan(AgentRole.MARKET_ANALYST, context1)
        
        if plan1["status"] == "success":
            print(f"  ✅ 市场分析师: 计划生成成功")
            print(f"    工具调用数: {plan1['total_calls']}")
            print(f"    主要工具: {sum(1 for call in plan1['tool_calls'] if call['priority'] == 'primary')}")
            print(f"    次要工具: {sum(1 for call in plan1['tool_calls'] if call['priority'] == 'secondary')}")
        else:
            print(f"  ❌ 市场分析师: 计划生成失败 - {plan1['reason']}")
            return False
        
        # 测试用例2: 需求预测师 - 缺少必需上下文
        context2 = {
            "product_category": "冰箱"
            # 缺少target_market
        }
        
        plan2 = manager.generate_tool_call_plan(AgentRole.DEMAND_FORECASTER, context2)
        
        if plan2["status"] == "failed":
            print(f"  ✅ 需求预测师: 正确识别缺少上下文")
            print(f"    失败原因: {plan2['reason']}")
        else:
            print(f"  ❌ 需求预测师: 应该失败但成功了")
            return False
        
        # 测试用例3: 供应链分析师 - 有次要工具
        context3 = {
            "supply_chain_region": "华南",
            "materials": ["铜", "铝"],
            "market_intelligence": True,  # 触发次要工具
            "api_parameters": {
                "futures_params": [{"ts_code": "CU2507.SHF", "freq": "week"}],
                "weather_params": {"place": "广州"}
            }
        }
        
        plan3 = manager.generate_tool_call_plan(AgentRole.SUPPLY_CHAIN_ANALYST, context3)
        
        if plan3["status"] == "success":
            print(f"  ✅ 供应链分析师: 计划生成成功")
            print(f"    总工具调用: {plan3['total_calls']}")
            
            # 验证是否包含次要工具
            has_secondary = any(call['priority'] == 'secondary' for call in plan3['tool_calls'])
            if has_secondary:
                print(f"    ✅ 正确包含次要工具")
            else:
                print(f"    ⚠️ 未包含次要工具")
        else:
            print(f"  ❌ 供应链分析师: 计划生成失败 - {plan3['reason']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 工具调用计划生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tool_usage_report():
    """测试工具使用报告生成"""
    try:
        from manufacturingagents.manufacturingagents.utils.tool_manager import (
            get_tool_manager, AgentRole
        )
        
        print("\n🧪 [测试] 工具使用报告生成...")
        
        manager = get_tool_manager()
        
        # 模拟工具调用
        mock_tool_calls = [
            {
                "tool_name": "pmi_tool",
                "tool_type": "economic_data",
                "priority": "primary",
                "params": {"start_m": "202501", "end_m": "202506", "fields": "month,pmi010000"},
                "description": "获取PMI制造业采购经理指数数据"
            },
            {
                "tool_name": "weather_tool",
                "tool_type": "weather_data",
                "priority": "secondary",
                "params": {"place": "厦门", "dailyForecast": True},
                "description": "获取天气预报数据"
            },
            {
                "tool_name": "news_tool",
                "tool_type": "news_data",
                "priority": "primary",
                "params": {},  # 空参数 - 应该验证失败
                "description": "获取新闻数据"
            }
        ]
        
        # 生成报告
        report = manager.generate_tool_usage_report(AgentRole.MARKET_ANALYST, mock_tool_calls)
        
        print("📊 报告生成验证:")
        
        # 验证报告内容
        if "市场分析师" in report.upper() or "MARKET_ANALYST" in report:
            print("  ✅ 包含智能体角色信息")
        else:
            print("  ❌ 缺少智能体角色信息")
            return False
        
        if "工具配置" in report:
            print("  ✅ 包含工具配置信息")
        else:
            print("  ❌ 缺少工具配置信息")
            return False
        
        if "参数验证" in report:
            print("  ✅ 包含参数验证信息")
        else:
            print("  ❌ 缺少参数验证信息")
            return False
        
        if len(report) > 500:
            print(f"  ✅ 报告内容充实 ({len(report)}字符)")
        else:
            print(f"  ❌ 报告内容过少 ({len(report)}字符)")
            return False
        
        print(f"\n📄 报告摘要 (前200字符):")
        print(f"  {report[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具使用报告测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_parameter_processor():
    """测试与参数预处理器的集成"""
    try:
        from manufacturingagents.manufacturingagents.utils.tool_manager import (
            get_tool_manager, AgentRole
        )
        
        print("\n🧪 [测试] 与参数预处理器集成...")
        
        manager = get_tool_manager()
        
        # 模拟参数预处理器的输出
        context_with_api_params = {
            "location": "厦门",
            "product_category": "空调",
            "time_range": "2025Q3",
            "api_parameters": {
                "pmi_params": {
                    "start_m": "202501",
                    "end_m": "202506",
                    "fields": "month,pmi010000"
                },
                "ppi_params": {
                    "start_m": "202501",
                    "end_m": "202506",
                    "fields": "month,ppi_yoy,ppi_mp"
                },
                "weather_params": {
                    "place": "厦门",
                    "dailyForecast": True,
                    "hourlyForecast": False
                },
                "news_params": {
                    "activity_query": "厦门7-9月空调促销活动",
                    "area_news_query": "格力 空调",
                    "new_building_query": "厦门7-9月新楼盘交付",
                    "policy_query": "2025年7-9月厦门空调购买优惠政策"
                }
            }
        }
        
        # 生成工具调用计划
        plan = manager.generate_tool_call_plan(AgentRole.MARKET_ANALYST, context_with_api_params)
        
        if plan["status"] == "success":
            print("  ✅ 集成测试: 计划生成成功")
            
            # 验证参数是否正确传递
            for tool_call in plan["tool_calls"]:
                tool_name = tool_call["tool_name"]
                params = tool_call["params"]
                
                if tool_name == "pmi_tool":
                    if params.get("start_m") == "202501" and params.get("end_m") == "202506":
                        print("    ✅ PMI工具参数正确传递")
                    else:
                        print("    ❌ PMI工具参数传递错误")
                        return False
                
                elif tool_name == "weather_tool":
                    if params.get("place") == "厦门":
                        print("    ✅ 天气工具参数正确传递")
                    else:
                        print("    ❌ 天气工具参数传递错误")
                        return False
                
                elif tool_name == "news_tool":
                    queries = params.get("queries", [])
                    if isinstance(queries, list) and len(queries) > 0:
                        print("    ✅ 新闻工具参数正确传递")
                    else:
                        print("    ❌ 新闻工具参数传递错误")
                        return False
            
            # 验证所有工具调用的参数
            all_valid = True
            for tool_call in plan["tool_calls"]:
                is_valid, issues = manager.validate_tool_call(tool_call["tool_name"], tool_call["params"])
                if not is_valid:
                    print(f"    ❌ {tool_call['tool_name']}参数验证失败: {issues}")
                    all_valid = False
            
            if all_valid:
                print("    ✅ 所有工具调用参数验证通过")
            else:
                return False
        else:
            print(f"  ❌ 集成测试失败: {plan['reason']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 开始工具管理器全面测试...")
    
    # 运行所有测试
    tests = [
        test_tool_configurations,
        test_agent_tool_mappings,
        test_tool_call_validation,
        test_tool_call_plan_generation,
        test_tool_usage_report,
        test_integration_with_parameter_processor
    ]
    
    all_passed = True
    for test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 异常: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有测试通过！工具管理器功能正常")
        print("\n🔧 核心功能验证:")
        print("  ✅ 工具配置管理正确")
        print("  ✅ 智能体工具映射准确")
        print("  ✅ 工具调用参数验证有效")
        print("  ✅ 工具调用计划生成智能")
        print("  ✅ 工具使用报告完整")
        print("  ✅ 与参数预处理器集成成功")
    else:
        print("\n❌ 部分测试失败，需要进一步调试") 