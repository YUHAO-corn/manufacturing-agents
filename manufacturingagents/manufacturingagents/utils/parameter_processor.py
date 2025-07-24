#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业智能参数预处理器
Manufacturing Intelligent Parameter Processor

使用LLM动态生成API调用参数，替换硬编码机制
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Tongyi


class ManufacturingParameterProcessor:
    """制造业参数预处理器 - LLM驱动的智能参数生成"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._initialize_llm()
        self._load_preprocessing_prompt()
    
    def _initialize_llm(self):
        """初始化LLM"""
        self.llm = Tongyi()
        self.llm.model_name = self.config.get("quick_think_llm", "qwen-plus")
        print(f"🧠 参数预处理器LLM初始化: {self.llm.model_name}")
    
    def _load_preprocessing_prompt(self):
        """加载预处理提示词"""
        try:
            from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager
            self.preprocessing_prompt = prompt_manager.get_prompt("preprocessing_assistant")
            if not self.preprocessing_prompt:
                # 使用默认提示词
                self.preprocessing_prompt = self._get_default_preprocessing_prompt()
        except Exception as e:
            print(f"⚠️ 加载预处理提示词失败: {e}")
            self.preprocessing_prompt = self._get_default_preprocessing_prompt()
    
    def _get_default_preprocessing_prompt(self):
        """默认预处理提示词"""
        return """你是制造业补货系统的参数预处理助手。你的任务是将用户输入转换为精确的API调度参数。

### 核心任务
根据用户输入和当前时间，生成以下API参数：

1. **天气API参数** - 标准化城市名
2. **新闻API参数** - 生成4类新闻查询语句
3. **节假日API参数** - 计算未来3个月日期范围
4. **PMI数据参数** - 考虑1个月延迟，计算过往6个月
5. **PPI数据参数** - 考虑1个月延迟，计算过往6个月  
6. **期货数据参数** - 生成当月和下月合约代码

### 重要规则
- PMI/PPI数据延迟1个月发布
- 期货代码格式：CU+年月.SHF（如CU2507.SHF）
- 城市名标准化：去除"市"、"区"等后缀
- 新闻查询需包含城市、产品、时间范围

请严格按照JSON格式输出，确保参数精确无误。"""

    def generate_api_parameters(
        self, 
        city_name: str, 
        brand_name: str, 
        product_category: str, 
        special_focus: str = "",
        current_date: str = None
    ) -> Dict[str, Any]:
        """
        生成所有API调用参数
        
        Args:
            city_name: 城市名称
            brand_name: 品牌名称  
            product_category: 产品类别
            special_focus: 特殊关注点
            current_date: 当前日期，默认为今天
            
        Returns:
            Dict: 包含所有API参数的字典
        """
        if not current_date:
            current_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"🔄 [预处理器] 开始生成API参数...")
        print(f"📍 输入: {city_name} {brand_name} {product_category} ({current_date})")
        
        # 构建LLM查询
        prompt = ChatPromptTemplate.from_template(
            self.preprocessing_prompt + """

### 用户输入
- 城市: {city_name}
- 品牌: {brand_name}  
- 产品类别: {product_category}
- 特殊关注点: {special_focus}
- 当前日期: {current_date}

### 要求输出
请生成完整的JSON格式参数，包含：
```json
{
  "weather_params": {...},
  "news_params": {...},
  "holiday_params": {...},
  "pmi_params": {...},
  "ppi_params": {...},
  "futures_params": [...]
}
```

现在请开始生成参数："""
        )
        
        # 调用LLM生成参数
        try:
            response = self.llm.invoke(prompt.format(
                city_name=city_name,
                brand_name=brand_name,
                product_category=product_category,
                special_focus=special_focus,
                current_date=current_date
            ))
            
            # 解析LLM响应
            parameters = self._parse_llm_response(response)
            
            # 验证参数格式
            validated_params = self._validate_parameters(parameters, current_date)
            
            print(f"✅ [预处理器] 参数生成成功")
            return validated_params
            
        except Exception as e:
            print(f"❌ [预处理器] LLM生成失败: {e}")
            # 降级到计算生成
            return self._generate_fallback_parameters(
                city_name, brand_name, product_category, current_date
            )
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """解析LLM响应，提取JSON参数"""
        try:
            # 提取JSON部分
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                parameters = json.loads(json_str)
                return parameters
            else:
                raise ValueError("未找到有效的JSON格式")
                
        except Exception as e:
            print(f"❌ [预处理器] JSON解析失败: {e}")
            raise
    
    def _validate_parameters(self, parameters: Dict[str, Any], current_date: str) -> Dict[str, Any]:
        """验证和修正参数格式"""
        validated = {}
        
        # 验证天气参数
        if "weather_params" in parameters:
            validated["weather_params"] = {
                "dailyForecast": True,
                "hourlyForecast": False,
                "nowcasting": False,
                "place": parameters["weather_params"].get("place", "未知城市"),
                "realtime": False
            }
        
        # 验证新闻参数
        if "news_params" in parameters:
            validated["news_params"] = parameters["news_params"]
        
        # 验证节假日参数
        if "holiday_params" in parameters:
            # 确保日期格式正确
            start_date = datetime.strptime(current_date, '%Y-%m-%d')
            end_date = start_date + timedelta(days=90)  # 3个月
            
            validated["holiday_params"] = {
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d')
            }
        
        # 验证PMI/PPI参数
        current_dt = datetime.strptime(current_date, '%Y-%m-%d')
        # 考虑1个月数据延迟
        end_month = (current_dt.replace(day=1) - timedelta(days=1))
        start_month = end_month - timedelta(days=150)  # 约5个月前
        
        validated["pmi_params"] = {
            "api_name": "cn_pmi",
            "start_m": start_month.strftime('%Y%m'),
            "end_m": end_month.strftime('%Y%m'),
            "fields": "month,pmi010000"
        }
        
        validated["ppi_params"] = {
            "api_name": "cn_ppi", 
            "start_m": start_month.strftime('%Y%m'),
            "end_m": end_month.strftime('%Y%m'),
            "fields": "month,ppi_yoy,ppi_mp"
        }
        
        # 验证期货参数
        current_month = current_dt.strftime('%y%m')
        next_month = (current_dt.replace(day=1) + timedelta(days=32)).strftime('%y%m')
        
        validated["futures_params"] = [
            {
                "api_name": "fut_weekly_monthly",
                "ts_code": f"CU{current_month}.SHF",
                "freq": "week",
                "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
            },
            {
                "api_name": "fut_weekly_monthly", 
                "ts_code": f"CU{next_month}.SHF",
                "freq": "week",
                "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
            }
        ]
        
        return validated
    
    def _generate_fallback_parameters(
        self, 
        city_name: str, 
        brand_name: str, 
        product_category: str, 
        current_date: str
    ) -> Dict[str, Any]:
        """降级方案：计算生成参数"""
        print(f"🔄 [预处理器] 使用计算生成参数...")
        
        current_dt = datetime.strptime(current_date, '%Y-%m-%d')
        
        # 标准化城市名（简单规则）
        clean_city = city_name.replace('市', '').replace('区', '').replace('县', '')
        
        # 计算时间范围
        end_date_3months = current_dt + timedelta(days=90)
        
        # 计算PMI/PPI月份（考虑1个月延迟）
        end_month = (current_dt.replace(day=1) - timedelta(days=1))
        start_month = end_month - timedelta(days=150)
        
        # 计算期货月份
        current_month = current_dt.strftime('%y%m')
        next_month = (current_dt.replace(day=1) + timedelta(days=32)).strftime('%y%m')
        
        return {
            "weather_params": {
                "dailyForecast": True,
                "hourlyForecast": False,
                "nowcasting": False,
                "place": clean_city,
                "realtime": False
            },
            "news_params": {
                "activity_query": f"{clean_city}{current_dt.month}-{(current_dt.month+2)%12+1}月近期有哪些厂商做{product_category}的促销活动",
                "area_news_query": f"{brand_name} {product_category}",
                "new_building_query": f"{clean_city}{current_dt.month}-{(current_dt.month+2)%12+1}月有哪些新楼盘交付",
                "policy_query": f"{current_dt.year}年{current_dt.month}-{(current_dt.month+2)%12+1}月{clean_city}{product_category}购买优惠政策"
            },
            "holiday_params": {
                "start_date": current_date,
                "end_date": end_date_3months.strftime('%Y-%m-%d')
            },
            "pmi_params": {
                "api_name": "cn_pmi",
                "start_m": start_month.strftime('%Y%m'),
                "end_m": end_month.strftime('%Y%m'),
                "fields": "month,pmi010000"
            },
            "ppi_params": {
                "api_name": "cn_ppi",
                "start_m": start_month.strftime('%Y%m'), 
                "end_m": end_month.strftime('%Y%m'),
                "fields": "month,ppi_yoy,ppi_mp"
            },
            "futures_params": [
                {
                    "api_name": "fut_weekly_monthly",
                    "ts_code": f"CU{current_month}.SHF",
                    "freq": "week", 
                    "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
                },
                {
                    "api_name": "fut_weekly_monthly",
                    "ts_code": f"CU{next_month}.SHF", 
                    "freq": "week",
                    "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
                }
            ]
        }

    def generate_single_api_params(self, api_type: str, **kwargs) -> Dict[str, Any]:
        """生成单个API的参数"""
        current_date = kwargs.get('current_date', datetime.now().strftime('%Y-%m-%d'))
        
        if api_type == "weather":
            city_name = kwargs.get('city_name', '')
            return {
                "dailyForecast": True,
                "hourlyForecast": False,
                "nowcasting": False,
                "place": city_name.replace('市', '').replace('区', ''),
                "realtime": False
            }
        
        elif api_type == "pmi":
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            end_month = (current_dt.replace(day=1) - timedelta(days=1))
            start_month = end_month - timedelta(days=150)
            
            return {
                "api_name": "cn_pmi",
                "start_m": start_month.strftime('%Y%m'),
                "end_m": end_month.strftime('%Y%m'),
                "fields": "month,pmi010000"
            }
        
        elif api_type == "ppi":
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            end_month = (current_dt.replace(day=1) - timedelta(days=1))
            start_month = end_month - timedelta(days=150)
            
            return {
                "api_name": "cn_ppi",
                "start_m": start_month.strftime('%Y%m'),
                "end_m": end_month.strftime('%Y%m'),
                "fields": "month,ppi_yoy,ppi_mp"
            }
        
        elif api_type == "futures":
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            current_month = current_dt.strftime('%y%m')
            next_month = (current_dt.replace(day=1) + timedelta(days=32)).strftime('%y%m')
            
            return [
                {
                    "api_name": "fut_weekly_monthly",
                    "ts_code": f"CU{current_month}.SHF",
                    "freq": "week",
                    "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
                },
                {
                    "api_name": "fut_weekly_monthly",
                    "ts_code": f"CU{next_month}.SHF",
                    "freq": "week", 
                    "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
                }
            ]
        
        else:
            raise ValueError(f"不支持的API类型: {api_type}")


# 全局实例
_parameter_processor = None

def get_parameter_processor(config: Dict[str, Any] = None) -> ManufacturingParameterProcessor:
    """获取参数预处理器实例"""
    global _parameter_processor
    if _parameter_processor is None:
        _parameter_processor = ManufacturingParameterProcessor(config)
    return _parameter_processor 