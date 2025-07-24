#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业行业资讯分析师 - ReAct Agent版本
Industry News Analyst for Manufacturing - ReAct Agent Version

专为阿里百炼LLM优化的ReAct Agent实现
"""

from langchain_core.tools import BaseTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json
# 🎯 新增：导入提示词管理器
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_industry_news_analyst_react(llm, toolkit):
    """创建ReAct模式的制造业行业资讯分析师（适用于阿里百炼）"""
    
    def industry_news_analyst_react_node(state):
        print(f"📰 [DEBUG] ===== ReAct行业资讯分析师节点开始 =====")
        
        current_date = state["analysis_date"]
        product_type = state["product_type"]
        company_name = state["company_name"]
        target_quarter = state["target_quarter"]
        # 🎯 修复：严格从状态获取用户输入的城市，不使用默认值
        city_name = state["city_name"]  # 如果缺失则报错，避免硬编码
        
        # 🎯 新增：获取进度追踪器并记录分析师启动
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.log_agent_start("📰 行业资讯分析师")
            progress_callback.update_progress(3)
            progress_callback.log_agent_thinking("📰 行业资讯分析师", "需要政策环境、竞争格局和行业动态数据")
        
        print(f"📰 [DEBUG] 输入参数: product_type={product_type}, company={company_name}, target_quarter={target_quarter}, city_name={city_name}")
        
        # 🎯 修复：创建符合预期格式的新闻工具
        class ManufacturingNewsTool(BaseTool):
            name: str = "get_manufacturing_news_data"
            description: str = f"🎯【一次性完整获取】制造业相关新闻数据，包含促销活动、区域新闻、新楼盘、政策动态等全部4类新闻。调用一次即可获得分析所需的所有新闻信息，无需重复调用。直接调用，无需参数。"
            
            def _run(self, unused_param: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call("行业新闻数据", "调用中")
                    
                    print(f"📰 [DEBUG] ManufacturingNewsTool调用，城市: {city_name}, 产品: {product_type}")
                    
                    # 🎯 修复：回归到统一toolkit架构，传递结构化参数
                    from datetime import datetime, timedelta
                    
                    # 基于当前日期计算未来3个月的时间范围
                    current_date_obj = datetime.now()
                    end_date_obj = current_date_obj + timedelta(days=90)
                    
                    # 🎯 生成符合预期的结构化查询参数
                    structured_query = {
                        "activity_query": f"{city_name}近期有哪些厂商做{product_type}的促销活动",
                        "area_news_query": f"{company_name}{product_type}",
                        "new_building_query": f"{city_name}近期有哪些新楼盘交付",
                        "policy_query": f"2025年{city_name}市{product_type}购买优惠政策"
                    }
                    
                    print(f"📰 [DEBUG] 使用结构化查询: {structured_query}")
                    
                    # 🎯 修复：回归统一架构，通过toolkit调用
                    result = toolkit.get_manufacturing_news_data.invoke({"query_params": structured_query})
                    
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call("行业新闻数据", "成功")
                    
                    return result
                        
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call("行业新闻数据", "失败")
                    return f"获取新闻数据失败: {str(e)}"

        # 配置行业资讯专用工具
        tools = [
            ManufacturingNewsTool()
        ]
        
        # 🎯 关键修复：使用txt文件中的专业提示词
        base_system_prompt = prompt_manager.get_prompt("news_analyst")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的新闻分析师，负责分析制造业相关新闻、政策变化和行业资讯，通过事件驱动分析识别连锁反应。"
        
        # 🎯 修复：使用专业提示词 + 具体任务参数
        query = f"""{base_system_prompt}

🎯 当前分析任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}
- 分析日期: {current_date}
- 目标季度: {target_quarter}
- 目标城市: {city_name}

🔧 工具使用说明：
- 必须调用get_manufacturing_news_data获取完整新闻数据（只需调用一次）
- 工具会一次性返回4类新闻：促销活动、区域新闻、新楼盘、政策动态

📋 执行要求：
- 必须严格按照提示词中的报告格式输出
- 必须在每个章节包含具体的数据支撑
- 必须使用**粗体**标记关键信息和结论
- 必须在报告开头提供"💡 核心决策建议"
- 报告长度不少于800字
- 重点分析对{target_quarter}季度补货的影响

🚨 关键执行约束：
- 严格禁止多次调用同一工具
- 一次工具调用后立即进入分析模式
- 不要因为"需要更多信息"而重复调用工具
- 工具返回的数据已经包含所有必要信息

现在请开始执行分析任务！"""

        print(f"📰 [DEBUG] 执行ReAct Agent查询...")
        
        try:
            # 🎯 新增：记录开始分析
            if progress_callback:
                progress_callback.log_event("progress", "📰 行业资讯分析师：开始数据分析...")
            
            # 创建ReAct Agent
            prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, prompt)
            # 🎯 修复：进一步限制迭代次数，避免重复调用
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=3,  # 🎯 关键修复：从5减少到3，强制限制调用次数
                max_execution_time=120,  # 🎯 修复：从300秒减少到120秒，控制时间
                return_intermediate_steps=True
            )
            
            result = agent_executor.invoke({'input': query})
            
            report = result.get('output', '分析失败')
            print(f"📰 [行业资讯分析师] ReAct Agent完成，报告长度: {len(report)}")
            
            # 🎯 新增：记录分析完成
            if progress_callback:
                progress_callback.log_agent_complete("📰 行业资讯分析师", f"生成{len(report)}字分析报告")
            
        except Exception as e:
            print(f"📰 [ERROR] ReAct Agent执行失败: {str(e)}")
            
            # 🎯 新增：记录分析失败
            if progress_callback:
                progress_callback.log_error(f"📰 行业资讯分析师失败: {str(e)}")
            
            report = f"行业资讯分析失败：{str(e)}"
        
        print(f"📰 [DEBUG] ===== ReAct行业资讯分析师节点结束 =====")
        
        # 更新状态
        new_state = state.copy()
        new_state["industry_news_report"] = report
        print(f"📰 [DEBUG] 状态更新完成，报告长度: {len(report)}")
        
        return new_state
    
    return industry_news_analyst_react_node 