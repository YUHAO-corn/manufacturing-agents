#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据验证器
Manufacturing Data Validator

验证API返回数据是否符合业务预期，避免垃圾数据污染分析结果
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd


class ManufacturingDataValidator:
    """制造业数据验证器 - 确保API数据质量"""
    
    def __init__(self):
        self.validation_rules = self._init_validation_rules()
        self.min_data_quality_score = 0.6  # 最低数据质量分数
    
    def _init_validation_rules(self) -> Dict[str, Dict]:
        """初始化各类数据的验证规则"""
        return {
            "weather": {
                "required_fields": ["date", "weather", "temperature"],
                "optional_fields": ["humidity", "wind", "forecast"],
                "data_types": {"temperature": (int, float)},
                "date_range_days": 10,  # 天气数据应覆盖未来7-10天
                "min_records": 5
            },
            "news": {
                "required_fields": ["activity_results", "area_results", "new_building_results", "policy_results"],
                "min_news_per_category": 1,  # 每类新闻至少1条
                "max_news_per_category": 20,  # 每类新闻最多20条
                "content_min_length": 10,  # 新闻内容最少10字符
                "relevance_keywords": ["促销", "政策", "楼盘", "厂商", "优惠"]
            },
            "holiday": {
                "required_fields": ["date", "name", "type"],
                "date_range_days": 90,  # 应覆盖未来3个月
                "min_holidays": 3,  # 3个月至少有3个节假日
                "holiday_types": ["法定节假日", "传统节日", "调休"]
            },
            "pmi": {
                "required_fields": ["month", "pmi010000"],
                "data_range": (30.0, 80.0),  # PMI合理范围30-80
                "required_months": 6,  # 应有6个月数据
                "trend_check": True  # 检查数据趋势是否合理
            },
            "ppi": {
                "required_fields": ["month", "ppi_yoy", "ppi_mp"],
                "data_range": (-30.0, 30.0),  # PPI同比增长合理范围
                "required_months": 6,  # 应有6个月数据
                "trend_check": True
            },
            "futures": {
                "required_fields": ["ts_code", "trade_date", "close"],
                "price_range": (20000, 100000),  # 铜期货价格合理范围(元/吨)
                "required_contracts": 2,  # 应有当月和下月两个合约
                "min_records_per_contract": 5  # 每个合约至少5条记录
            },
            # 🎯 修复：添加commodity作为futures的别名
            "commodity": {
                "required_fields": ["ts_code", "trade_date", "close"],
                "price_range": (20000, 100000),  # 铜期货价格合理范围(元/吨)
                "required_contracts": 2,  # 应有当月和下月两个合约
                "min_records_per_contract": 5  # 每个合约至少5条记录
            }
        }
    
    def validate_api_data(self, data_type: str, raw_data: Any, context: Dict[str, Any] = None) -> Tuple[bool, float, List[str]]:
        """
        验证API返回数据
        
        Args:
            data_type: 数据类型 (weather/news/holiday/pmi/ppi/futures)
            raw_data: API返回的原始数据
            context: 验证上下文（如预期日期范围等）
            
        Returns:
            Tuple[是否通过, 质量分数, 问题列表]
        """
        if data_type not in self.validation_rules:
            return False, 0.0, [f"不支持的数据类型: {data_type}"]
        
        try:
            # 解析数据
            parsed_data = self._parse_raw_data(data_type, raw_data)
            if parsed_data is None:
                return False, 0.0, ["数据解析失败"]
            
            # 执行验证
            validation_result = self._validate_data_by_type(data_type, parsed_data, context)
            
            return validation_result
            
        except Exception as e:
            return False, 0.0, [f"验证过程异常: {str(e)}"]
    
    def _parse_raw_data(self, data_type: str, raw_data: Any) -> Optional[Any]:
        """解析原始数据"""
        try:
            if isinstance(raw_data, str):
                # 如果是字符串，尝试解析JSON
                if raw_data.strip().startswith('{') or raw_data.strip().startswith('['):
                    return json.loads(raw_data)
                else:
                    # 可能是格式化文本，保持原样
                    return raw_data
            else:
                return raw_data
        except Exception as e:
            print(f"❌ [验证器] 数据解析失败: {e}")
            return None
    
    def _validate_data_by_type(self, data_type: str, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """根据数据类型执行具体验证"""
        
        if data_type == "weather":
            return self._validate_weather_data(data, context)
        elif data_type == "news":
            return self._validate_news_data(data, context)
        elif data_type == "holiday":
            return self._validate_holiday_data(data, context)
        elif data_type == "pmi":
            return self._validate_pmi_data(data, context)
        elif data_type == "ppi":
            return self._validate_ppi_data(data, context)
        elif data_type == "futures":
            return self._validate_futures_data(data, context)
        elif data_type == "commodity":
            # 🎯 修复：commodity使用和futures相同的验证逻辑
            return self._validate_futures_data(data, context)
        else:
            return False, 0.0, [f"未实现的验证类型: {data_type}"]
    
    def _validate_weather_data(self, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证天气数据"""
        issues = []
        quality_score = 1.0
        
        # 检查数据结构
        if not isinstance(data, (dict, str)):
            issues.append("天气数据格式错误")
            return False, 0.0, issues
        
        # 如果是字符串，检查是否包含天气相关信息
        if isinstance(data, str):
            weather_keywords = ["温度", "天气", "预报", "度", "晴", "雨", "云", "wind", "temperature"]
            if not any(keyword in data for keyword in weather_keywords):
                issues.append("天气数据缺少关键信息")
                quality_score -= 0.3
            
            # 检查日期信息
            date_patterns = [r'\d{4}-\d{1,2}-\d{1,2}', r'\d{1,2}月\d{1,2}日']
            if not any(re.search(pattern, data) for pattern in date_patterns):
                issues.append("天气数据缺少日期信息")
                quality_score -= 0.2
        
        # 检查数据量
        if isinstance(data, str) and len(data) < 100:
            issues.append("天气数据过少")
            quality_score -= 0.2
        
        return quality_score >= self.min_data_quality_score, quality_score, issues
    
    def _validate_news_data(self, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证新闻数据"""
        issues = []
        quality_score = 1.0
        
        # 检查数据结构
        if isinstance(data, str):
            # 字符串格式，检查是否包含新闻相关信息
            news_keywords = ["新闻", "政策", "促销", "楼盘", "厂商", "活动"]
            if not any(keyword in data for keyword in news_keywords):
                issues.append("新闻数据缺少相关内容")
                quality_score -= 0.4
        
        elif isinstance(data, dict):
            # JSON格式，检查必需字段
            rules = self.validation_rules["news"]
            required_fields = rules["required_fields"]
            
            for field in required_fields:
                if field not in data:
                    issues.append(f"新闻数据缺少字段: {field}")
                    quality_score -= 0.2
                elif not data[field]:
                    issues.append(f"新闻字段为空: {field}")
                    quality_score -= 0.1
        
        # 检查新闻内容长度
        content_length = len(str(data))
        if content_length < 200:
            issues.append("新闻内容过少")
            quality_score -= 0.2
        
        return quality_score >= self.min_data_quality_score, quality_score, issues
    
    def _validate_holiday_data(self, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证节假日数据"""
        issues = []
        quality_score = 1.0
        
        # 检查数据结构
        if isinstance(data, str):
            # 字符串格式，检查是否包含节假日信息
            holiday_keywords = ["节假日", "假期", "节日", "休息", "调休", "放假"]
            if not any(keyword in data for keyword in holiday_keywords):
                issues.append("节假日数据缺少相关信息")
                quality_score -= 0.3
            
            # 检查是否包含日期
            date_patterns = [r'\d{4}-\d{1,2}-\d{1,2}', r'\d{1,2}月\d{1,2}日']
            dates_found = sum(1 for pattern in date_patterns if re.search(pattern, data))
            
            if dates_found < 3:
                issues.append("节假日数据中日期信息过少")
                quality_score -= 0.2
        
        elif isinstance(data, (list, dict)):
            # 结构化数据，检查数量
            if isinstance(data, list) and len(data) < 3:
                issues.append("节假日数量过少（3个月应有3个以上）")
                quality_score -= 0.3
        
        return quality_score >= self.min_data_quality_score, quality_score, issues
    
    def _validate_pmi_data(self, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证PMI数据"""
        issues = []
        quality_score = 1.0
        
        try:
            # 尝试解析为DataFrame或结构化数据
            if isinstance(data, str):
                # 检查字符串是否包含PMI相关信息
                if "pmi" not in data.lower() and "采购经理" not in data:
                    issues.append("PMI数据缺少相关标识")
                    quality_score -= 0.2
                
                # 检查是否包含数值数据
                numbers = re.findall(r'\d+\.?\d*', data)
                valid_pmi_values = [float(n) for n in numbers if 30.0 <= float(n) <= 80.0]
                
                if len(valid_pmi_values) < 3:
                    issues.append("PMI数据中有效数值过少")
                    quality_score -= 0.3
                else:
                    # 检查数据合理性
                    avg_pmi = sum(valid_pmi_values) / len(valid_pmi_values)
                    if not (40.0 <= avg_pmi <= 65.0):
                        issues.append("PMI数据数值异常")
                        quality_score -= 0.2
            
            # 检查时间覆盖
            if "202501" not in str(data) or "202506" not in str(data):
                issues.append("PMI数据时间范围不符合预期")
                quality_score -= 0.2
        
        except Exception as e:
            issues.append(f"PMI数据验证异常: {e}")
            quality_score -= 0.5
        
        return quality_score >= self.min_data_quality_score, quality_score, issues
    
    def _validate_ppi_data(self, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证PPI数据"""
        issues = []
        quality_score = 1.0
        
        try:
            # 检查PPI相关标识
            if isinstance(data, str):
                if "ppi" not in data.lower() and "生产者价格" not in data:
                    issues.append("PPI数据缺少相关标识")
                    quality_score -= 0.2
                
                # 检查数值数据
                numbers = re.findall(r'-?\d+\.?\d*', data)
                valid_ppi_values = [float(n) for n in numbers if -30.0 <= float(n) <= 30.0]
                
                if len(valid_ppi_values) < 3:
                    issues.append("PPI数据中有效数值过少")
                    quality_score -= 0.3
            
            # 检查时间覆盖
            if "202501" not in str(data) or "202506" not in str(data):
                issues.append("PPI数据时间范围不符合预期")
                quality_score -= 0.2
        
        except Exception as e:
            issues.append(f"PPI数据验证异常: {e}")
            quality_score -= 0.5
        
        return quality_score >= self.min_data_quality_score, quality_score, issues
    
    def _validate_futures_data(self, data: Any, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证期货数据"""
        issues = []
        quality_score = 1.0
        
        try:
            # 检查期货代码
            if isinstance(data, str):
                if "CU2507" not in data or "CU2508" not in data:
                    issues.append("期货数据缺少预期合约代码")
                    quality_score -= 0.3
                
                # 检查价格数据
                numbers = re.findall(r'\d+\.?\d*', data)
                valid_prices = [float(n) for n in numbers if 20000 <= float(n) <= 100000]
                
                if len(valid_prices) < 5:
                    issues.append("期货价格数据过少")
                    quality_score -= 0.3
                else:
                    # 检查价格合理性
                    avg_price = sum(valid_prices) / len(valid_prices)
                    if not (40000 <= avg_price <= 80000):
                        issues.append("期货价格异常")
                        quality_score -= 0.2
        
        except Exception as e:
            issues.append(f"期货数据验证异常: {e}")
            quality_score -= 0.5
        
        return quality_score >= self.min_data_quality_score, quality_score, issues
    
    def generate_validation_report(self, validations: Dict[str, Tuple[bool, float, List[str]]]) -> str:
        """生成数据验证报告"""
        report = "## 📊 数据质量验证报告\n\n"
        
        total_score = 0
        total_types = len(validations)
        
        for data_type, (passed, score, issues) in validations.items():
            status = "✅ 通过" if passed else "❌ 失败"
            report += f"### {data_type.upper()} 数据\n"
            report += f"- **验证状态**: {status}\n"
            report += f"- **质量分数**: {score:.2f}\n"
            
            if issues:
                report += f"- **问题列表**:\n"
                for issue in issues:
                    report += f"  - {issue}\n"
            else:
                report += f"- **质量评估**: 数据质量良好\n"
            
            report += "\n"
            total_score += score
        
        # 总体评估
        avg_score = total_score / total_types if total_types > 0 else 0
        overall_status = "良好" if avg_score >= 0.8 else "一般" if avg_score >= 0.6 else "较差"
        
        report += f"### 📈 总体数据质量\n"
        report += f"- **平均质量分数**: {avg_score:.2f}\n"
        report += f"- **总体评估**: {overall_status}\n"
        
        if avg_score < 0.6:
            report += f"- **⚠️ 建议**: 数据质量较差，建议检查API配置或数据源\n"
        
        return report

    def validate_all_manufacturing_data(self, all_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """验证所有制造业数据"""
        print("🔍 [验证器] 开始验证所有制造业数据...")
        
        validations = {}
        context = context or {}
        
        # 数据类型映射
        data_mapping = {
            "weather_data": "weather",
            "news_data": "news", 
            "holiday_data": "holiday",
            "pmi_data": "pmi",
            "ppi_data": "ppi",
            "futures_data": "futures"
        }
        
        for data_key, data_type in data_mapping.items():
            if data_key in all_data:
                passed, score, issues = self.validate_api_data(data_type, all_data[data_key], context)
                validations[data_type] = (passed, score, issues)
                
                status = "✅ 通过" if passed else "❌ 失败"
                print(f"🔍 [验证器] {data_type}: {status} (分数: {score:.2f})")
        
        # 生成验证报告
        validation_report = self.generate_validation_report(validations)
        
        return {
            "validations": validations,
            "report": validation_report,
            "overall_passed": all(v[0] for v in validations.values()),
            "average_score": sum(v[1] for v in validations.values()) / len(validations) if validations else 0
        }


# 全局实例
_data_validator = None

def get_data_validator() -> ManufacturingDataValidator:
    """获取数据验证器实例"""
    global _data_validator
    if _data_validator is None:
        _data_validator = ManufacturingDataValidator()
    return _data_validator 