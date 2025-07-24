#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业智能体工具管理器
Manufacturing Agent Tool Manager

统一管理各智能体的工具配置、调用规范和参数传递
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import logging


class AgentRole(Enum):
    """智能体角色定义"""
    MARKET_ANALYST = "market_analyst"           # 市场分析师
    SUPPLY_CHAIN_ANALYST = "supply_chain"      # 供应链分析师
    DEMAND_FORECASTER = "demand_forecaster"    # 需求预测师
    INVENTORY_MANAGER = "inventory_manager"    # 库存管理师
    PRODUCTION_PLANNER = "production_planner"  # 生产计划师


class ToolType(Enum):
    """工具类型定义"""
    ECONOMIC_DATA = "economic_data"    # 经济数据工具
    WEATHER_DATA = "weather_data"      # 天气数据工具
    NEWS_DATA = "news_data"           # 新闻数据工具
    HOLIDAY_DATA = "holiday_data"     # 节假日数据工具
    SENTIMENT_DATA = "sentiment_data" # 舆情数据工具


@dataclass
class ToolConfig:
    """工具配置类"""
    tool_name: str
    tool_type: ToolType
    required_params: List[str]
    optional_params: List[str]
    output_format: str
    description: str


@dataclass
class AgentToolMapping:
    """智能体工具映射"""
    agent_role: AgentRole
    primary_tools: List[str]      # 主要工具
    secondary_tools: List[str]    # 次要工具
    context_requirements: Dict[str, Any]  # 上下文要求


class ManufacturingToolManager:
    """制造业工具管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_tool_configs()
        self._initialize_agent_mappings()
    
    def _initialize_tool_configs(self):
        """初始化工具配置"""
        self.tool_configs = {
            "pmi_tool": ToolConfig(
                tool_name="pmi_tool",
                tool_type=ToolType.ECONOMIC_DATA,
                required_params=["start_m", "end_m"],
                optional_params=["fields"],
                output_format="DataFrame",
                description="获取PMI制造业采购经理指数数据"
            ),
            "ppi_tool": ToolConfig(
                tool_name="ppi_tool",
                tool_type=ToolType.ECONOMIC_DATA,
                required_params=["start_m", "end_m"],
                optional_params=["fields"],
                output_format="DataFrame",
                description="获取PPI工业生产者价格指数数据"
            ),
            "futures_tool": ToolConfig(
                tool_name="futures_tool",
                tool_type=ToolType.ECONOMIC_DATA,
                required_params=["ts_code", "freq"],
                optional_params=["fields", "trade_date"],
                output_format="DataFrame",
                description="获取期货价格数据"
            ),
            "weather_tool": ToolConfig(
                tool_name="weather_tool",
                tool_type=ToolType.WEATHER_DATA,
                required_params=["place"],
                optional_params=["dailyForecast", "hourlyForecast"],
                output_format="JSON",
                description="获取天气预报数据"
            ),
            "news_tool": ToolConfig(
                tool_name="news_tool",
                tool_type=ToolType.NEWS_DATA,
                required_params=["queries"],
                optional_params=["date_range", "max_results"],
                output_format="JSON",
                description="获取新闻数据"
            ),
            "holiday_tool": ToolConfig(
                tool_name="holiday_tool",
                tool_type=ToolType.HOLIDAY_DATA,
                required_params=["start_date", "end_date"],
                optional_params=["country", "region"],
                output_format="JSON",
                description="获取节假日数据"
            ),
            "sentiment_tool": ToolConfig(
                tool_name="sentiment_tool",
                tool_type=ToolType.SENTIMENT_DATA,
                required_params=["keywords"],
                optional_params=["platform", "date_range"],
                output_format="JSON",
                description="获取舆情数据"
            )
        }
    
    def _initialize_agent_mappings(self):
        """初始化智能体工具映射"""
        self.agent_mappings = {
            AgentRole.MARKET_ANALYST: AgentToolMapping(
                agent_role=AgentRole.MARKET_ANALYST,
                primary_tools=["pmi_tool", "ppi_tool", "news_tool"],
                secondary_tools=["weather_tool", "holiday_tool"],
                context_requirements={
                    "location": "required",
                    "product_category": "required",
                    "time_range": "required"
                }
            ),
            AgentRole.SUPPLY_CHAIN_ANALYST: AgentToolMapping(
                agent_role=AgentRole.SUPPLY_CHAIN_ANALYST,
                primary_tools=["futures_tool", "weather_tool"],
                secondary_tools=["news_tool", "holiday_tool"],
                context_requirements={
                    "supply_chain_region": "required",
                    "materials": "required",
                    "logistics_routes": "optional"
                }
            ),
            AgentRole.DEMAND_FORECASTER: AgentToolMapping(
                agent_role=AgentRole.DEMAND_FORECASTER,
                primary_tools=["sentiment_tool", "holiday_tool", "weather_tool"],
                secondary_tools=["news_tool", "pmi_tool"],
                context_requirements={
                    "target_market": "required",
                    "product_category": "required",
                    "seasonal_factors": "optional"
                }
            ),
            AgentRole.INVENTORY_MANAGER: AgentToolMapping(
                agent_role=AgentRole.INVENTORY_MANAGER,
                primary_tools=["holiday_tool", "weather_tool"],
                secondary_tools=["sentiment_tool", "news_tool"],
                context_requirements={
                    "warehouse_location": "required",
                    "product_types": "required",
                    "storage_capacity": "optional"
                }
            ),
            AgentRole.PRODUCTION_PLANNER: AgentToolMapping(
                agent_role=AgentRole.PRODUCTION_PLANNER,
                primary_tools=["pmi_tool", "futures_tool", "holiday_tool"],
                secondary_tools=["weather_tool", "news_tool"],
                context_requirements={
                    "production_facility": "required",
                    "capacity_constraints": "required",
                    "energy_costs": "optional"
                }
            )
        }
    
    def get_agent_tools(self, agent_role: AgentRole) -> Dict[str, Any]:
        """获取指定智能体的工具配置"""
        if agent_role not in self.agent_mappings:
            raise ValueError(f"未知的智能体角色: {agent_role}")
        
        mapping = self.agent_mappings[agent_role]
        
        return {
            "primary_tools": [self.tool_configs[tool] for tool in mapping.primary_tools],
            "secondary_tools": [self.tool_configs[tool] for tool in mapping.secondary_tools],
            "context_requirements": mapping.context_requirements,
            "total_tools": len(mapping.primary_tools) + len(mapping.secondary_tools)
        }
    
    def validate_tool_call(self, tool_name: str, params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证工具调用参数"""
        if tool_name not in self.tool_configs:
            return False, [f"未知的工具: {tool_name}"]
        
        config = self.tool_configs[tool_name]
        issues = []
        
        # 检查必需参数
        for required_param in config.required_params:
            if required_param not in params:
                issues.append(f"缺少必需参数: {required_param}")
            elif params[required_param] is None or params[required_param] == "":
                issues.append(f"必需参数不能为空: {required_param}")
        
        # 检查参数类型（简单验证）
        param_type_hints = {
            "start_m": str, "end_m": str,
            "ts_code": str, "freq": str,
            "place": str, "queries": (list, str),
            "start_date": str, "end_date": str,
            "keywords": (list, str)
        }
        
        for param_name, param_value in params.items():
            if param_name in param_type_hints:
                expected_type = param_type_hints[param_name]
                if not isinstance(param_value, expected_type):
                    issues.append(f"参数类型错误: {param_name} 应为 {expected_type}, 实际为 {type(param_value)}")
        
        return len(issues) == 0, issues
    
    def generate_tool_call_plan(self, agent_role: AgentRole, context: Dict[str, Any]) -> Dict[str, Any]:
        """为智能体生成工具调用计划"""
        if agent_role not in self.agent_mappings:
            raise ValueError(f"未知的智能体角色: {agent_role}")
        
        mapping = self.agent_mappings[agent_role]
        
        # 检查上下文要求
        missing_context = []
        for requirement, importance in mapping.context_requirements.items():
            if importance == "required" and requirement not in context:
                missing_context.append(requirement)
        
        if missing_context:
            return {
                "status": "failed",
                "reason": f"缺少必需的上下文: {missing_context}",
                "tool_calls": []
            }
        
        # 生成工具调用计划
        tool_calls = []
        
        # 主要工具调用
        for tool_name in mapping.primary_tools:
            tool_config = self.tool_configs[tool_name]
            call_params = self._generate_tool_params(tool_name, context)
            
            tool_calls.append({
                "tool_name": tool_name,
                "tool_type": tool_config.tool_type.value,
                "priority": "primary",
                "params": call_params,
                "description": tool_config.description
            })
        
        # 次要工具调用（条件性）
        for tool_name in mapping.secondary_tools:
            if self._should_use_secondary_tool(tool_name, context, agent_role):
                tool_config = self.tool_configs[tool_name]
                call_params = self._generate_tool_params(tool_name, context)
                
                tool_calls.append({
                    "tool_name": tool_name,
                    "tool_type": tool_config.tool_type.value,
                    "priority": "secondary",
                    "params": call_params,
                    "description": tool_config.description
                })
        
        return {
            "status": "success",
            "agent_role": agent_role.value,
            "tool_calls": tool_calls,
            "total_calls": len(tool_calls),
            "context_used": context
        }
    
    def _generate_tool_params(self, tool_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """根据上下文生成工具参数"""
        config = self.tool_configs[tool_name]
        params = {}
        
        # 使用参数预处理器生成的参数
        if "api_parameters" in context:
            api_params = context["api_parameters"]
            
            if tool_name == "pmi_tool" and "pmi_params" in api_params:
                pmi_params = api_params["pmi_params"]
                params.update({
                    "start_m": pmi_params.get("start_m"),
                    "end_m": pmi_params.get("end_m"),
                    "fields": pmi_params.get("fields", "month,pmi010000")
                })
            
            elif tool_name == "ppi_tool" and "ppi_params" in api_params:
                ppi_params = api_params["ppi_params"]
                params.update({
                    "start_m": ppi_params.get("start_m"),
                    "end_m": ppi_params.get("end_m"),
                    "fields": ppi_params.get("fields", "month,ppi_yoy,ppi_mp")
                })
            
            elif tool_name == "futures_tool" and "futures_params" in api_params:
                futures_params = api_params["futures_params"]
                if isinstance(futures_params, list) and len(futures_params) > 0:
                    # 使用第一个期货合约参数
                    first_contract = futures_params[0]
                    params.update({
                        "ts_code": first_contract.get("ts_code"),
                        "freq": first_contract.get("freq", "week"),
                        "fields": first_contract.get("fields")
                    })
            
            elif tool_name == "weather_tool" and "weather_params" in api_params:
                weather_params = api_params["weather_params"]
                params.update({
                    "place": weather_params.get("place"),
                    "dailyForecast": weather_params.get("dailyForecast", True),
                    "hourlyForecast": weather_params.get("hourlyForecast", False)
                })
            
            elif tool_name == "news_tool" and "news_params" in api_params:
                news_params = api_params["news_params"]
                # 将新闻查询转换为列表
                queries = []
                for query_type in ["activity_query", "area_news_query", "new_building_query", "policy_query"]:
                    if query_type in news_params:
                        queries.append(news_params[query_type])
                params.update({
                    "queries": queries,
                    "max_results": 5
                })
            
            elif tool_name == "holiday_tool" and "holiday_params" in api_params:
                holiday_params = api_params["holiday_params"]
                params.update({
                    "start_date": holiday_params.get("start_date"),
                    "end_date": holiday_params.get("end_date")
                })
        
        # 如果没有预处理参数，使用上下文直接生成
        if not params:
            if tool_name == "sentiment_tool":
                keywords = [context.get("brand_name", ""), context.get("product_category", "")]
                params = {"keywords": [k for k in keywords if k]}
        
        return params
    
    def _should_use_secondary_tool(self, tool_name: str, context: Dict[str, Any], agent_role: AgentRole) -> bool:
        """判断是否应该使用次要工具"""
        # 根据上下文和智能体角色判断是否需要次要工具
        
        if tool_name == "weather_tool":
            # 如果涉及户外作业或季节性产品，使用天气工具
            return context.get("seasonal_factors") or context.get("outdoor_operations")
        
        elif tool_name == "holiday_tool":
            # 如果涉及消费品或有时间敏感的计划，使用节假日工具
            return context.get("consumer_product") or agent_role == AgentRole.DEMAND_FORECASTER
        
        elif tool_name == "news_tool":
            # 如果需要市场情报或品牌监控，使用新闻工具
            return context.get("market_intelligence") or context.get("brand_monitoring")
        
        elif tool_name == "sentiment_tool":
            # 如果涉及消费者导向的决策，使用舆情工具
            return agent_role == AgentRole.DEMAND_FORECASTER or context.get("consumer_sentiment")
        
        return True  # 默认使用所有次要工具
    
    def generate_tool_usage_report(self, agent_role: AgentRole, tool_calls: List[Dict[str, Any]]) -> str:
        """生成工具使用报告"""
        mapping = self.agent_mappings[agent_role]
        
        report = f"## 🔧 {agent_role.value.upper()} 工具使用报告\n\n"
        
        # 工具配置总结
        report += f"### 📊 工具配置\n"
        report += f"- **主要工具**: {len(mapping.primary_tools)}个\n"
        report += f"- **次要工具**: {len(mapping.secondary_tools)}个\n"
        report += f"- **实际调用**: {len(tool_calls)}个\n\n"
        
        # 工具调用详情
        report += f"### 📋 调用详情\n"
        for i, call in enumerate(tool_calls, 1):
            tool_name = call.get("tool_name", "未知")
            priority = call.get("priority", "未知")
            params = call.get("params", {})
            
            report += f"#### {i}. {tool_name.upper()} ({priority})\n"
            report += f"- **描述**: {call.get('description', '无描述')}\n"
            report += f"- **参数数量**: {len(params)}\n"
            
            if params:
                report += f"- **主要参数**:\n"
                for param_name, param_value in list(params.items())[:3]:  # 只显示前3个参数
                    report += f"  - {param_name}: {param_value}\n"
            
            report += "\n"
        
        # 参数验证结果
        validation_results = []
        for call in tool_calls:
            tool_name = call.get("tool_name")
            params = call.get("params", {})
            is_valid, issues = self.validate_tool_call(tool_name, params)
            validation_results.append((tool_name, is_valid, issues))
        
        report += f"### ✅ 参数验证\n"
        for tool_name, is_valid, issues in validation_results:
            status = "✅ 通过" if is_valid else "❌ 失败"
            report += f"- **{tool_name}**: {status}\n"
            if issues:
                for issue in issues:
                    report += f"  - ⚠️ {issue}\n"
        
        return report


# 全局实例
_tool_manager = None

def get_tool_manager() -> ManufacturingToolManager:
    """获取工具管理器实例"""
    global _tool_manager
    if _tool_manager is None:
        _tool_manager = ManufacturingToolManager()
    return _tool_manager 