#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
严格数据策略管理器
Strict Data Policy Manager

实施严格的数据获取策略：只允许舆情数据使用模拟降级，其他必须是真实API
"""

from typing import Dict, Any, List, Tuple, Optional
from enum import Enum
from datetime import datetime
import logging


class DataSource(Enum):
    """数据源类型"""
    REAL_API = "real_api"           # 真实API
    CACHED_DATA = "cached_data"     # 缓存数据
    SIMULATED_DATA = "simulated"    # 模拟数据
    UNAVAILABLE = "unavailable"     # 不可用


class DataType(Enum):
    """数据类型分类"""
    ECONOMIC_DATA = "economic"      # 经济数据(PMI/PPI/期货) - 必须真实
    WEATHER_DATA = "weather"        # 天气数据 - 必须真实
    NEWS_DATA = "news"             # 新闻数据 - 必须真实
    HOLIDAY_DATA = "holiday"        # 节假日数据 - 必须真实
    SENTIMENT_DATA = "sentiment"    # 舆情数据 - 允许模拟


class StrictDataPolicy:
    """严格数据策略管理器"""
    
    def __init__(self, allow_cache_hours: int = 24):
        self.allow_cache_hours = allow_cache_hours
        self.logger = logging.getLogger(__name__)
        
        # 数据类型分类规则
        self.data_type_mapping = {
            "pmi": DataType.ECONOMIC_DATA,
            "ppi": DataType.ECONOMIC_DATA,
            "futures": DataType.ECONOMIC_DATA,
            "weather": DataType.WEATHER_DATA,
            "news": DataType.NEWS_DATA,
            "holiday": DataType.HOLIDAY_DATA,
            "sentiment": DataType.SENTIMENT_DATA,
            "consumer_behavior": DataType.SENTIMENT_DATA
        }
        
        # 允许的数据源策略
        self.allowed_sources = {
            DataType.ECONOMIC_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.WEATHER_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.NEWS_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.HOLIDAY_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.SENTIMENT_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA, DataSource.SIMULATED_DATA]
        }
        
        # 数据获取策略优先级
        self.source_priority = {
            DataType.ECONOMIC_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.WEATHER_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.NEWS_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.HOLIDAY_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA],
            DataType.SENTIMENT_DATA: [DataSource.REAL_API, DataSource.CACHED_DATA, DataSource.SIMULATED_DATA]
        }
    
    def validate_data_request(self, data_name: str, requested_source: DataSource) -> Tuple[bool, str]:
        """
        验证数据请求是否符合策略
        
        Args:
            data_name: 数据名称
            requested_source: 请求的数据源
            
        Returns:
            Tuple[是否允许, 原因说明]
        """
        # 确定数据类型
        data_type = self._get_data_type(data_name)
        if data_type is None:
            return False, f"未知的数据类型: {data_name}"
        
        # 检查是否允许该数据源
        allowed_sources = self.allowed_sources.get(data_type, [])
        
        if requested_source not in allowed_sources:
            if data_type == DataType.SENTIMENT_DATA:
                if requested_source == DataSource.SIMULATED_DATA:
                    return True, f"舆情数据允许使用模拟数据"
                else:
                    return False, f"{data_name}({data_type.value})不允许使用{requested_source.value}"
            else:
                return False, f"{data_name}({data_type.value})不允许使用{requested_source.value}，只能使用{[s.value for s in allowed_sources]}"
        
        return True, f"{data_name}允许使用{requested_source.value}"
    
    def get_fallback_strategy(self, data_name: str, failed_source: DataSource) -> Optional[DataSource]:
        """
        获取降级策略
        
        Args:
            data_name: 数据名称
            failed_source: 失败的数据源
            
        Returns:
            下一个可尝试的数据源，None表示无降级选项
        """
        data_type = self._get_data_type(data_name)
        if data_type is None:
            return None
        
        priority_list = self.source_priority.get(data_type, [])
        
        try:
            current_index = priority_list.index(failed_source)
            # 返回下一个优先级的数据源
            if current_index + 1 < len(priority_list):
                return priority_list[current_index + 1]
        except ValueError:
            # 如果失败的源不在优先级列表中，返回第一个可用源
            if priority_list:
                return priority_list[0]
        
        return None
    
    def enforce_data_policy(self, data_requests: Dict[str, Any]) -> Dict[str, Any]:
        """
        强制执行数据策略
        
        Args:
            data_requests: 数据请求字典 {data_name: {source, data, ...}}
            
        Returns:
            策略执行结果
        """
        self.logger.info("🔒 [策略] 开始强制执行严格数据策略...")
        
        policy_results = {}
        violations = []
        
        for data_name, request_info in data_requests.items():
            source = request_info.get('source', DataSource.UNAVAILABLE)
            
            # 验证数据请求
            is_allowed, reason = self.validate_data_request(data_name, source)
            
            if not is_allowed:
                violations.append({
                    'data_name': data_name,
                    'source': source.value,
                    'reason': reason
                })
                
                # 尝试获取降级策略
                fallback_source = self.get_fallback_strategy(data_name, source)
                if fallback_source:
                    self.logger.warning(f"⚠️ [策略] {data_name}: {reason}，尝试降级到{fallback_source.value}")
                    policy_results[data_name] = {
                        'status': 'fallback',
                        'source': fallback_source,
                        'original_source': source,
                        'reason': reason
                    }
                else:
                    self.logger.error(f"❌ [策略] {data_name}: {reason}，无可用降级策略")
                    policy_results[data_name] = {
                        'status': 'rejected',
                        'source': DataSource.UNAVAILABLE,
                        'original_source': source,
                        'reason': reason
                    }
            else:
                self.logger.info(f"✅ [策略] {data_name}: {reason}")
                policy_results[data_name] = {
                    'status': 'approved',
                    'source': source,
                    'reason': reason
                }
        
        return {
            'policy_results': policy_results,
            'violations': violations,
            'total_requests': len(data_requests),
            'approved_count': sum(1 for r in policy_results.values() if r['status'] == 'approved'),
            'fallback_count': sum(1 for r in policy_results.values() if r['status'] == 'fallback'),
            'rejected_count': sum(1 for r in policy_results.values() if r['status'] == 'rejected')
        }
    
    def generate_policy_report(self, enforcement_result: Dict[str, Any]) -> str:
        """生成策略执行报告"""
        results = enforcement_result['policy_results']
        violations = enforcement_result['violations']
        
        report = "## 🔒 严格数据策略执行报告\n\n"
        
        # 总体统计
        report += f"### 📊 执行统计\n"
        report += f"- **总请求数**: {enforcement_result['total_requests']}\n"
        report += f"- **通过数**: {enforcement_result['approved_count']}\n"
        report += f"- **降级数**: {enforcement_result['fallback_count']}\n"
        report += f"- **拒绝数**: {enforcement_result['rejected_count']}\n\n"
        
        # 详细结果
        report += f"### 📋 详细执行结果\n"
        for data_name, result in results.items():
            status_icon = {
                'approved': '✅',
                'fallback': '⚠️',
                'rejected': '❌'
            }.get(result['status'], '❓')
            
            report += f"#### {status_icon} {data_name.upper()}\n"
            report += f"- **状态**: {result['status']}\n"
            report += f"- **数据源**: {result['source'].value if hasattr(result['source'], 'value') else result['source']}\n"
            
            if 'original_source' in result:
                report += f"- **原始请求**: {result['original_source'].value}\n"
            
            report += f"- **说明**: {result['reason']}\n\n"
        
        # 违规情况
        if violations:
            report += f"### ⚠️ 策略违规情况\n"
            for violation in violations:
                report += f"- **{violation['data_name']}**: {violation['reason']}\n"
            report += "\n"
        
        # 建议
        if enforcement_result['rejected_count'] > 0:
            report += f"### 💡 改进建议\n"
            report += f"- 检查被拒绝的数据源配置\n"
            report += f"- 确保真实API密钥正确配置\n"
            report += f"- 优化数据缓存策略\n"
            
            if any(r['status'] == 'rejected' and 'sentiment' not in data_name.lower() 
                   for data_name, r in results.items()):
                report += f"- **⚠️ 重要**: 非舆情数据不允许使用模拟数据\n"
        
        return report
    
    def _get_data_type(self, data_name: str) -> Optional[DataType]:
        """根据数据名称确定数据类型"""
        data_name_lower = data_name.lower()
        
        for key, data_type in self.data_type_mapping.items():
            if key in data_name_lower:
                return data_type
        
        return None
    
    def check_data_compliance(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查所有数据是否符合策略"""
        self.logger.info("🔍 [策略] 检查数据合规性...")
        
        compliance_results = {}
        
        for data_key, data_info in all_data.items():
            # 判断数据来源
            if isinstance(data_info, dict) and 'source' in data_info:
                source = data_info['source']
            elif isinstance(data_info, str):
                # 根据数据内容推断来源
                if "模拟" in data_info or "演示" in data_info:
                    source = DataSource.SIMULATED_DATA
                elif "API调用失败" in data_info:
                    source = DataSource.UNAVAILABLE
                else:
                    source = DataSource.REAL_API
            else:
                source = DataSource.REAL_API  # 默认假设是真实API
            
            # 验证合规性
            is_compliant, reason = self.validate_data_request(data_key, source)
            
            compliance_results[data_key] = {
                'compliant': is_compliant,
                'source': source,
                'reason': reason,
                'data_type': self._get_data_type(data_key)
            }
            
            status = "✅ 合规" if is_compliant else "❌ 违规"
            self.logger.info(f"🔍 [策略] {data_key}: {status}")
        
        return compliance_results
    
    def suggest_data_source_fixes(self, compliance_results: Dict[str, Any]) -> List[str]:
        """建议数据源修复方案"""
        suggestions = []
        
        for data_key, result in compliance_results.items():
            if not result['compliant']:
                data_type = result['data_type']
                current_source = result['source']
                
                if data_type and data_type != DataType.SENTIMENT_DATA:
                    if current_source == DataSource.SIMULATED_DATA:
                        suggestions.append(f"🔧 {data_key}: 配置真实API替换模拟数据")
                    elif current_source == DataSource.UNAVAILABLE:
                        suggestions.append(f"🔧 {data_key}: 检查API密钥和网络连接")
                
                # 提供具体的降级建议
                fallback = self.get_fallback_strategy(data_key, current_source)
                if fallback:
                    suggestions.append(f"💡 {data_key}: 可降级使用{fallback.value}")
        
        return suggestions


# 全局实例
_strict_policy = None

def get_strict_data_policy() -> StrictDataPolicy:
    """获取严格数据策略实例"""
    global _strict_policy
    if _strict_policy is None:
        _strict_policy = StrictDataPolicy()
    return _strict_policy

def enforce_manufacturing_data_policy(data_requests: Dict[str, Any]) -> Dict[str, Any]:
    """强制执行制造业数据策略的便捷函数"""
    policy = get_strict_data_policy()
    return policy.enforce_data_policy(data_requests) 