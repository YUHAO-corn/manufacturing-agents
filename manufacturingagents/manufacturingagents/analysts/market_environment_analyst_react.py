#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业市场环境分析师 - ReAct Agent版本
Market Environment Analyst for Manufacturing - ReAct Agent Version

专为阿里百炼LLM优化的ReAct Agent实现
"""

from langchain_core.tools import BaseTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json
# 🎯 新增：导入提示词管理器
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_market_environment_analyst_react(llm, toolkit):
    """创建ReAct模式的制造业市场环境分析师（适用于阿里百炼）"""
    
    def market_environment_analyst_react_node(state):
        print(f"🌍 [DEBUG] ===== ReAct市场环境分析师节点开始 =====")
        
        current_date = state["analysis_date"]
        product_type = state["product_type"]
        company_name = state["company_name"]
        
        # 🎯 新增：获取进度追踪器并记录分析师启动
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.log_agent_start("🌍 市场环境分析师")
            progress_callback.update_progress(1)
            progress_callback.log_agent_thinking("🌍 市场环境分析师", "需要PMI、PPI、原材料价格数据")
        
        print(f"🌍 [DEBUG] 输入参数: product_type={product_type}, company={company_name}, date={current_date}")
        
        # 创建制造业专用工具
        class ManufacturingPMITool(BaseTool):
            name: str = "get_manufacturing_pmi_data"
            description: str = f"获取制造业PMI指数数据，分析{product_type}行业的宏观经济环境。直接调用，无需参数。"
            
            def _run(self, query: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call("PMI指数数据", "调用中")
                    
                    print(f"🌍 [DEBUG] ManufacturingPMITool调用，产品类型: {product_type}")
                    result = toolkit.get_manufacturing_pmi_data.invoke({"time_range": "最近6个月"})
                    
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call("PMI指数数据", "成功")
                    
                    return result
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call("PMI指数数据", "失败")
                    return f"获取PMI数据失败: {str(e)}"
        
        class ManufacturingPPITool(BaseTool):
            name: str = "get_manufacturing_ppi_data"
            description: str = f"获取制造业PPI价格指数数据，分析{product_type}行业的成本压力和价格趋势。直接调用，无需参数。"
            
            def _run(self, query: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call("PPI价格指数", "调用中")
                    
                    print(f"🌍 [DEBUG] ManufacturingPPITool调用，产品类型: {product_type}")
                    result = toolkit.get_manufacturing_ppi_data.invoke({"time_range": "最近6个月"})
                    
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call("PPI价格指数", "成功")
                    
                    return result
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call("PPI价格指数", "失败")
                    return f"获取PPI数据失败: {str(e)}"
        
        class ManufacturingCommodityTool(BaseTool):
            name: str = "get_manufacturing_commodity_data"
            description: str = f"获取制造业大宗商品价格数据，分析影响{product_type}生产成本的原材料价格变化。直接调用，无需参数。"
            
            def _run(self, query: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call("大宗商品价格", "调用中")
                    
                    print(f"🌍 [DEBUG] ManufacturingCommodityTool调用，产品类型: {product_type}")
                    result = toolkit.get_manufacturing_commodity_data.invoke({"commodity_type": "铜期货"})
                    
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call("大宗商品价格", "成功")
                    
                    return result
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call("大宗商品价格", "失败")
                    return f"获取大宗商品数据失败: {str(e)}"
        
        # 工具列表
        tools = [ManufacturingPMITool(), ManufacturingPPITool(), ManufacturingCommodityTool()]
        
        # 🎯 关键修复：使用txt文件中的专业提示词
        base_system_prompt = prompt_manager.get_prompt("market_environment_analyst")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的制造业市场环境分析师，负责分析宏观经济环境、原材料市场和制造业整体运营环境。"
        
        # 🎯 修复：使用专业提示词 + 具体任务参数
        query = f"""{base_system_prompt}

🎯 当前分析任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}
- 分析日期: {current_date}

🔧 工具使用说明：
- 必须调用get_manufacturing_pmi_data获取制造业PMI指数数据
- 必须调用get_manufacturing_ppi_data获取制造业PPI价格指数数据
- 必须调用get_manufacturing_commodity_data获取大宗商品价格数据

📋 执行要求：
- 必须严格按照提示词中的报告格式输出
- 必须在每个章节包含具体的数据支撑
- 必须使用**粗体**标记关键信息和结论
- 必须在报告开头提供"💡 核心决策建议"
- 报告长度不少于800字

现在请开始执行分析任务！"""
        
        try:
            # 创建ReAct Agent
            prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,  # 🎯 修复：减少迭代次数，避免重复调用
                max_execution_time=180,  # 3分钟超时
                return_intermediate_steps=True  # 返回中间步骤便于调试
            )
            
            print(f"🌍 [DEBUG] 执行ReAct Agent查询...")
            
            # 🎯 新增：记录开始分析
            if progress_callback:
                progress_callback.log_event("progress", "🌍 市场环境分析师：开始数据分析...")
            
            result = agent_executor.invoke({'input': query})
            
            report = result['output']
            print(f"🌍 [市场环境分析师] ReAct Agent完成，报告长度: {len(report)}")
            
            # 🎯 新增：记录分析完成
            if progress_callback:
                progress_callback.log_agent_complete("🌍 市场环境分析师", f"生成{len(report)}字分析报告")
            
            # 检查是否包含格式错误信息
            if "Invalid Format" in report or "Missing 'Action:'" in report:
                print(f"⚠️ [DEBUG] 检测到格式错误，但Agent已处理")
                print(f"🌍 [DEBUG] 中间步骤数量: {len(result.get('intermediate_steps', []))}")
            
        except Exception as e:
            print(f"🌍 [ERROR] ReAct Agent执行失败: {str(e)}")
            
            # 🎯 新增：记录分析失败
            if progress_callback:
                progress_callback.log_error(f"🌍 市场环境分析师失败: {str(e)}")
            
            report = f"市场环境分析失败：{str(e)}"
        
        print(f"🌍 [DEBUG] ===== ReAct市场环境分析师节点结束 =====")
        
        # 更新状态
        new_state = state.copy()
        new_state["market_environment_report"] = report
        print(f"🌍 [DEBUG] 状态更新完成，报告长度: {len(report)}")
        
        return new_state
    
    return market_environment_analyst_react_node


# 为了兼容性，也保留原始版本的创建函数
def create_market_environment_analyst(llm, toolkit):
    """创建标准版本的市场环境分析师（兼容性保留）"""
    # 如果是阿里百炼，直接使用ReAct版本
    return create_market_environment_analyst_react(llm, toolkit) 