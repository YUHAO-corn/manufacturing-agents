#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
严格数据策略测试
Test Strict Data Policy

验证只允许舆情数据使用模拟降级，其他必须使用真实API
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_data_policy_classification():
    """测试数据分类策略"""
    try:
        from manufacturingagents.manufacturingagents.utils.strict_data_policy import (
            get_strict_data_policy, DataSource, DataType
        )
        
        print("🧪 [测试] 数据分类策略...")
        
        policy = get_strict_data_policy()
        
        # 测试数据分类
        test_cases = [
            ("pmi_data", DataType.ECONOMIC_DATA),
            ("ppi_data", DataType.ECONOMIC_DATA),
            ("futures_data", DataType.ECONOMIC_DATA),
            ("weather_data", DataType.WEATHER_DATA),
            ("news_data", DataType.NEWS_DATA),
            ("holiday_data", DataType.HOLIDAY_DATA),
            ("sentiment_data", DataType.SENTIMENT_DATA),
            ("consumer_behavior", DataType.SENTIMENT_DATA)
        ]
        
        print("📋 数据分类测试:")
        for data_name, expected_type in test_cases:
            actual_type = policy._get_data_type(data_name)
            if actual_type == expected_type:
                print(f"  ✅ {data_name} -> {expected_type.value}")
            else:
                print(f"  ❌ {data_name} -> 期望{expected_type.value}, 实际{actual_type.value if actual_type else None}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 数据分类策略测试失败: {e}")
        return False

def test_strict_policy_rules():
    """测试严格策略规则"""
    try:
        from manufacturingagents.manufacturingagents.utils.strict_data_policy import (
            get_strict_data_policy, DataSource, DataType
        )
        
        print("\n🧪 [测试] 严格策略规则...")
        
        policy = get_strict_data_policy()
        
        # 测试用例：[数据名, 数据源, 是否应该允许]
        test_cases = [
            # 经济数据 - 不允许模拟
            ("pmi_data", DataSource.REAL_API, True),
            ("pmi_data", DataSource.CACHED_DATA, True),
            ("pmi_data", DataSource.SIMULATED_DATA, False),
            ("ppi_data", DataSource.SIMULATED_DATA, False),
            ("futures_data", DataSource.SIMULATED_DATA, False),
            
            # 天气数据 - 不允许模拟
            ("weather_data", DataSource.REAL_API, True),
            ("weather_data", DataSource.CACHED_DATA, True),
            ("weather_data", DataSource.SIMULATED_DATA, False),
            
            # 新闻数据 - 不允许模拟
            ("news_data", DataSource.REAL_API, True),
            ("news_data", DataSource.CACHED_DATA, True),
            ("news_data", DataSource.SIMULATED_DATA, False),
            
            # 节假日数据 - 不允许模拟
            ("holiday_data", DataSource.REAL_API, True),
            ("holiday_data", DataSource.CACHED_DATA, True),
            ("holiday_data", DataSource.SIMULATED_DATA, False),
            
            # 舆情数据 - 允许模拟
            ("sentiment_data", DataSource.REAL_API, True),
            ("sentiment_data", DataSource.CACHED_DATA, True),
            ("sentiment_data", DataSource.SIMULATED_DATA, True),
            ("consumer_behavior", DataSource.SIMULATED_DATA, True),
        ]
        
        print("🔒 策略规则验证:")
        for data_name, source, expected_allowed in test_cases:
            is_allowed, reason = policy.validate_data_request(data_name, source)
            
            if is_allowed == expected_allowed:
                status = "✅ 正确"
                print(f"  {status}: {data_name} + {source.value} = {'允许' if is_allowed else '拒绝'}")
            else:
                status = "❌ 错误"
                print(f"  {status}: {data_name} + {source.value} = 期望{'允许' if expected_allowed else '拒绝'}, 实际{'允许' if is_allowed else '拒绝'}")
                print(f"    原因: {reason}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 严格策略规则测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_strategy():
    """测试降级策略"""
    try:
        from manufacturingagents.manufacturingagents.utils.strict_data_policy import (
            get_strict_data_policy, DataSource, DataType
        )
        
        print("\n🧪 [测试] 降级策略...")
        
        policy = get_strict_data_policy()
        
        # 测试降级策略
        test_cases = [
            # 经济数据降级: REAL_API -> CACHED_DATA -> None
            ("pmi_data", DataSource.REAL_API, DataSource.CACHED_DATA),
            ("pmi_data", DataSource.CACHED_DATA, None),
            
            # 舆情数据降级: REAL_API -> CACHED_DATA -> SIMULATED_DATA -> None
            ("sentiment_data", DataSource.REAL_API, DataSource.CACHED_DATA),
            ("sentiment_data", DataSource.CACHED_DATA, DataSource.SIMULATED_DATA),
            ("sentiment_data", DataSource.SIMULATED_DATA, None),
        ]
        
        print("🔄 降级策略验证:")
        for data_name, failed_source, expected_fallback in test_cases:
            actual_fallback = policy.get_fallback_strategy(data_name, failed_source)
            
            if actual_fallback == expected_fallback:
                fallback_str = expected_fallback.value if expected_fallback else "无降级"
                print(f"  ✅ {data_name}: {failed_source.value} -> {fallback_str}")
            else:
                expected_str = expected_fallback.value if expected_fallback else "无降级"
                actual_str = actual_fallback.value if actual_fallback else "无降级"
                print(f"  ❌ {data_name}: {failed_source.value} -> 期望{expected_str}, 实际{actual_str}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 降级策略测试失败: {e}")
        return False

def test_policy_enforcement():
    """测试策略执行"""
    try:
        from manufacturingagents.manufacturingagents.utils.strict_data_policy import (
            get_strict_data_policy, DataSource, DataType
        )
        
        print("\n🧪 [测试] 策略执行...")
        
        policy = get_strict_data_policy()
        
        # 模拟数据请求
        data_requests = {
            "pmi_data": {"source": DataSource.REAL_API, "content": "PMI真实数据"},
            "weather_data": {"source": DataSource.SIMULATED_DATA, "content": "模拟天气数据"},  # 违规
            "news_data": {"source": DataSource.CACHED_DATA, "content": "缓存新闻数据"},
            "sentiment_data": {"source": DataSource.SIMULATED_DATA, "content": "模拟舆情数据"},  # 允许
            "unknown_data": {"source": DataSource.REAL_API, "content": "未知数据"}  # 未知类型
        }
        
        # 执行策略
        result = policy.enforce_data_policy(data_requests)
        
        print("📊 策略执行结果:")
        print(f"  总请求: {result['total_requests']}")
        print(f"  通过: {result['approved_count']}")
        print(f"  降级: {result['fallback_count']}")
        print(f"  拒绝: {result['rejected_count']}")
        
        # 验证预期结果
        expected_results = {
            "pmi_data": "approved",      # 经济数据+真实API = 通过
            "weather_data": "fallback",  # 天气数据+模拟 = 降级到缓存
            "news_data": "approved",     # 新闻数据+缓存 = 通过
            "sentiment_data": "approved" # 舆情数据+模拟 = 通过
        }
        
        print("\n📋 详细验证:")
        for data_name, expected_status in expected_results.items():
            if data_name in result['policy_results']:
                actual_status = result['policy_results'][data_name]['status']
                if actual_status == expected_status:
                    print(f"  ✅ {data_name}: {expected_status}")
                else:
                    print(f"  ❌ {data_name}: 期望{expected_status}, 实际{actual_status}")
                    return False
            else:
                print(f"  ❌ {data_name}: 结果中未找到")
                return False
        
        # 生成报告测试
        report = policy.generate_policy_report(result)
        print(f"\n📄 策略执行报告 (长度: {len(report)}):")
        if len(report) > 100:
            print("  ✅ 报告生成成功")
        else:
            print("  ❌ 报告内容过少")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 策略执行测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_compliance_check():
    """测试合规性检查"""
    try:
        from manufacturingagents.manufacturingagents.utils.strict_data_policy import (
            get_strict_data_policy, DataSource, DataType
        )
        
        print("\n🧪 [测试] 合规性检查...")
        
        policy = get_strict_data_policy()
        
        # 模拟获取到的数据
        all_data = {
            "pmi_data": "PMI数据：202501月50.1，202502月50.5",  # 真实数据
            "weather_data": "天气数据：模拟天气预报",              # 模拟数据 - 违规
            "news_data": "新闻数据：真实新闻内容",               # 真实数据
            "sentiment_data": "舆情数据：模拟消费者情绪分析",      # 模拟数据 - 允许
            "holiday_data": "节假日数据：API调用失败"            # 不可用 - 违规
        }
        
        # 检查合规性
        compliance_results = policy.check_data_compliance(all_data)
        
        print("🔍 合规性检查结果:")
        for data_key, result in compliance_results.items():
            status = "✅ 合规" if result['compliant'] else "❌ 违规"
            print(f"  {status}: {data_key} ({result['source'].value})")
        
        # 验证预期结果
        expected_compliance = {
            "pmi_data": True,        # 经济数据使用真实API - 合规
            "weather_data": False,   # 天气数据使用模拟 - 违规
            "news_data": True,       # 新闻数据使用真实API - 合规
            "sentiment_data": True,  # 舆情数据使用模拟 - 合规
            "holiday_data": False    # 节假日数据不可用 - 违规
        }
        
        all_correct = True
        for data_key, expected in expected_compliance.items():
            actual = compliance_results[data_key]['compliant']
            if actual != expected:
                print(f"  ❌ {data_key}合规性判断错误: 期望{expected}, 实际{actual}")
                all_correct = False
        
        if all_correct:
            print("  ✅ 所有合规性判断正确")
        
        # 测试修复建议
        suggestions = policy.suggest_data_source_fixes(compliance_results)
        print(f"\n💡 修复建议 ({len(suggestions)}条):")
        for suggestion in suggestions:
            print(f"  {suggestion}")
        
        return all_correct
        
    except Exception as e:
        print(f"❌ 合规性检查测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_policy_scenarios():
    """测试完整策略场景"""
    print("\n🧪 [测试] 完整策略场景...")
    
    # 场景1: 全部使用真实API
    print("\n📋 场景1: 全部真实API")
    scenario1_requests = {
        "pmi_data": {"source": "real_api"},
        "weather_data": {"source": "real_api"},
        "news_data": {"source": "real_api"},
        "sentiment_data": {"source": "real_api"}
    }
    print("  预期: 全部通过 ✅")
    
    # 场景2: 混合策略违规
    print("\n📋 场景2: 混合策略(包含违规)")
    scenario2_requests = {
        "pmi_data": {"source": "simulated"},      # 违规
        "weather_data": {"source": "cached"},     # 合规
        "sentiment_data": {"source": "simulated"} # 合规
    }
    print("  预期: PMI拒绝，天气通过，舆情通过")
    
    # 场景3: 全部降级到模拟
    print("\n📋 场景3: 全部尝试使用模拟数据")
    scenario3_requests = {
        "pmi_data": {"source": "simulated"},       # 违规
        "weather_data": {"source": "simulated"},   # 违规
        "news_data": {"source": "simulated"},      # 违规
        "sentiment_data": {"source": "simulated"}  # 合规
    }
    print("  预期: 只有舆情通过，其他全部拒绝或降级")
    
    return True

if __name__ == "__main__":
    print("🧪 开始严格数据策略全面测试...")
    
    # 运行所有测试
    tests = [
        test_data_policy_classification,
        test_strict_policy_rules,
        test_fallback_strategy,
        test_policy_enforcement,
        test_compliance_check,
        test_policy_scenarios
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
        print("\n🎉 所有测试通过！严格数据策略功能正常")
        print("\n🔒 核心策略验证:")
        print("  ✅ 经济数据(PMI/PPI/期货)禁止模拟数据")
        print("  ✅ 天气/新闻/节假日数据禁止模拟数据") 
        print("  ✅ 舆情数据允许模拟数据")
        print("  ✅ 降级策略正确执行")
        print("  ✅ 合规性检查功能正常")
    else:
        print("\n❌ 部分测试失败，需要进一步调试") 