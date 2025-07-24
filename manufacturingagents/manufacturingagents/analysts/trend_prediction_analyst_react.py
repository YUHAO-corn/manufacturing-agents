#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业趋势预测分析师 - ReAct Agent版本
Trend Prediction Analyst for Manufacturing - ReAct Agent Version

专为阿里百炼LLM优化的ReAct Agent实现
"""

from langchain_core.tools import BaseTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json
# 🎯 新增：导入提示词管理器
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_trend_prediction_analyst_react(llm, toolkit):
    """创建ReAct模式的制造业趋势预测分析师（适用于阿里百炼）"""
    
    def trend_prediction_analyst_react_node(state):
        print(f"📈 [DEBUG] ===== ReAct趋势预测分析师节点开始 =====")
        
        current_date = state["analysis_date"]
        product_type = state["product_type"]
        company_name = state["company_name"]
        target_quarter = state["target_quarter"]
        # 🎯 修复：严格从状态获取用户输入的城市，不使用默认值
        city_name = state["city_name"]  # 如果缺失则报错，避免硬编码
        
        # 🎯 新增：获取进度追踪器并记录分析师启动
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.log_agent_start("📈 趋势预测分析师")
            progress_callback.update_progress(2)
            progress_callback.log_agent_thinking("📈 趋势预测分析师", f"需要{city_name}的天气和节假日数据")
        
        print(f"📈 [DEBUG] 输入参数: product_type={product_type}, company={company_name}, target_quarter={target_quarter}, city_name={city_name}")
        
        # 创建趋势预测专用工具：节假日和天气数据
        class ManufacturingHolidayTool(BaseTool):
            name: str = "get_manufacturing_holiday_data"
            description: str = f"获取节假日数据，分析节假日对{product_type}产品需求的季节性影响。自动计算基于当前日期的未来3个月"
            
            def _run(self, unused_param: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call("节假日数据", "调用中")
                    
                    print(f"📈 [DEBUG] ManufacturingHolidayTool调用，产品类型: {product_type}")
                    
                    # 🎯 修复：基于当前日期动态计算未来3个月
                    from datetime import datetime, timedelta
                    current_date_obj = datetime.now()
                    end_date_obj = current_date_obj + timedelta(days=90)  # 未来3个月
                    
                    # 生成符合接口要求的日期格式
                    dynamic_date_range = f"{current_date_obj.strftime('%Y-%m-%d')} to {end_date_obj.strftime('%Y-%m-%d')}"
                    print(f"📈 [DEBUG] 动态计算日期范围: {dynamic_date_range}")
                    
                    result = toolkit.get_manufacturing_holiday_data.invoke({"date_range": dynamic_date_range})
                    
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call("节假日数据", "成功")
                    
                    return result
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call("节假日数据", "失败")
                    return f"获取节假日数据失败: {str(e)}"

        class ManufacturingWeatherTool(BaseTool):
            name: str = "get_manufacturing_weather_data"
            description: str = f"获取天气预报数据，分析天气变化对{product_type}产品需求趋势的影响。直接调用即可，会自动使用用户输入的城市{city_name}"
            
            def _run(self, unused_param: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call(f"{city_name}天气数据", "调用中")
                    
                    # 🎯 修复：回归统一架构，通过toolkit调用
                    target_city = city_name  # 使用状态中的城市
                    print(f"📈 [DEBUG] ManufacturingWeatherTool调用，产品类型: {product_type}, 目标城市: {target_city}")
                    
                    # 通过统一的toolkit调用，保持架构一致性
                    result = toolkit.get_manufacturing_weather_data.invoke({"city_name": target_city})
                    
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call(f"{city_name}天气数据", "成功")
                    
                    return result
                        
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call(f"{city_name}天气数据", "失败")
                    return f"获取天气数据失败: {str(e)}"

        # 配置趋势预测专用工具
        tools = [
            ManufacturingHolidayTool(),
            ManufacturingWeatherTool()
        ]
        
        # 🎯 关键修复：使用txt文件中的专业提示词
        base_system_prompt = prompt_manager.get_prompt("trend_prediction_analyst")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的制造业趋势预测分析师，专门负责基于未来事件预测（天气预报、节假日等），为补货决策提供前瞻性趋势分析支持。"
        
        # 🎯 修复：使用专业提示词 + 具体任务参数
        query = f"""{base_system_prompt}

🎯 当前分析任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}
- 分析日期: {current_date}
- 目标季度: {target_quarter}
- 目标城市: {city_name}

🔧 工具使用说明：
- 必须调用get_manufacturing_holiday_data获取节假日数据（自动计算未来3个月）
- 必须调用get_manufacturing_weather_data获取{city_name}的天气数据

📋 执行要求：
- 必须严格按照提示词中的报告格式输出
- 必须在每个章节包含具体的数据支撑
- 必须使用**粗体**标记关键信息和结论
- 必须在报告开头提供"💡 核心决策建议"
- 报告长度不少于800字
- 重点预测对{target_quarter}季度补货的影响

现在请开始执行分析任务！"""

        print(f"📈 [DEBUG] 执行ReAct Agent查询...")
        
        try:
            # 🎯 新增：记录开始分析
            if progress_callback:
                progress_callback.log_event("progress", "📈 趋势预测分析师：开始数据分析...")
            
            # 创建ReAct Agent
            prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,  # 🎯 修复：减少迭代次数，避免重复调用
                max_execution_time=300,
                return_intermediate_steps=True
            )
            
            result = agent_executor.invoke({'input': query})
            
            report = result.get('output', '分析失败')
            print(f"📈 [趋势预测分析师] ReAct Agent完成，报告长度: {len(report)}")
            
            # 🎯 新增：记录分析完成
            if progress_callback:
                progress_callback.log_agent_complete("📈 趋势预测分析师", f"生成{len(report)}字分析报告")
            
        except Exception as e:
            print(f"📈 [ERROR] ReAct Agent执行失败: {str(e)}")
            
            # 🎯 新增：记录分析失败
            if progress_callback:
                progress_callback.log_error(f"📈 趋势预测分析师失败: {str(e)}")
            
            report = f"趋势预测分析失败：{str(e)}"
        
        print(f"📈 [DEBUG] ===== ReAct趋势预测分析师节点结束 =====")
        
        # 更新状态
        new_state = state.copy()
        new_state["trend_prediction_report"] = report
        print(f"📈 [DEBUG] 状态更新完成，报告长度: {len(report)}")
        
        return new_state
    
    return trend_prediction_analyst_react_node 