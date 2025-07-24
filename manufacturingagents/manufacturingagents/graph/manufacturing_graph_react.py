#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业智能体 ReAct Graph 工作流系统
Manufacturing Agents ReAct Graph Workflow System

使用ReAct Agent模式，适配阿里百炼LLM
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, StateGraph, START

# 导入ReAct版本的制造业智能体
from manufacturingagents.manufacturingagents.analysts.market_environment_analyst_react import create_market_environment_analyst_react
from manufacturingagents.manufacturingagents.analysts.trend_prediction_analyst_react import create_trend_prediction_analyst_react  
from manufacturingagents.manufacturingagents.analysts.industry_news_analyst_react import create_industry_news_analyst_react
from manufacturingagents.manufacturingagents.analysts.consumer_insight_analyst_react import create_consumer_insight_analyst_react

# 导入决策层智能体
from manufacturingagents.manufacturingagents.advisors.optimistic_advisor import create_optimistic_advisor
from manufacturingagents.manufacturingagents.advisors.cautious_advisor import create_cautious_advisor
from manufacturingagents.manufacturingagents.coordinator.decision_coordinator import create_decision_coordinator
from manufacturingagents.manufacturingagents.risk_mgmt.risk_assessment import create_risk_assessment_team

# 导入结论提取智能体
from manufacturingagents.manufacturingagents.utils.conclusion_extractor import create_conclusion_extractor

# 导入状态和工具
from manufacturingagents.manufacturingagents.utils.manufacturing_states import ManufacturingState
from manufacturingagents.agents.utils.agent_utils import Toolkit

# 导入LLM适配器
from manufacturingagents.llm_adapters.dashscope_adapter import ChatDashScope


class ManufacturingAgentsReactGraph:
    """制造业智能体ReAct图工作流系统"""
    
    def __init__(
        self,
        selected_analysts=["market_environment_analyst"],  # 支持四个分析师
        debug=False,
        config: Dict[str, Any] = None,
    ):
        """初始化制造业智能体ReAct图系统"""
        self.debug = debug
        self.config = config or {}
        self.selected_analysts = selected_analysts
        
        # 初始化LLM
        self._initialize_llm()
        
        # 初始化工具包
        self.toolkit = Toolkit(config=self.config)
        
        # 创建制造业工作流图
        self.graph = self._setup_react_graph()
    
    def _should_continue_decision_debate(self, state):
        """控制乐观vs谨慎顾问的辩论轮次"""
        debate_state = state.get("decision_debate_state", {})
        count = debate_state.get("count", 0)
        current_response = debate_state.get("current_response", "")
        
        print(f"🎭 [辩论控制] 当前轮次: {count}, 最新发言: {current_response[:50]}...")
        
        # 最多2轮辩论（4次发言：乐观→谨慎→乐观→谨慎）
        if count >= 4:
            print("🎯 [辩论控制] 辩论轮次已满，转向决策协调员")
            return "Decision_Coordinator"
        
        # 第一次发言或没有发言者标识，默认开始乐观顾问
        if count == 0 or not current_response:
            print("🌟 [辩论控制] 开始辩论，首先乐观顾问发言")
            return "Optimistic_Advisor"
        
        # 根据当前发言者确定下一个发言者
        if "乐观决策顾问:" in current_response:
            print("🛡️ [辩论控制] 乐观顾问发言完毕，轮到谨慎顾问")
            return "Cautious_Advisor"
        elif "谨慎决策顾问:" in current_response:
            print("🌟 [辩论控制] 谨慎顾问发言完毕，轮到乐观顾问")
            return "Optimistic_Advisor"
        else:
            # 兜底逻辑：如果无法识别发言者，根据轮次判断
            if count % 2 == 0:
                print("🌟 [辩论控制] 兜底逻辑：偶数轮，乐观顾问发言")
                return "Optimistic_Advisor"
            else:
                print("🛡️ [辩论控制] 兜底逻辑：奇数轮，谨慎顾问发言")
                return "Cautious_Advisor"
    
    def _initialize_llm(self):
        """初始化LLM模型"""
        llm_provider = self.config.get("llm_provider", "dashscope")
        llm_model = self.config.get("llm_model", "qwen-turbo")
        
        if llm_provider.lower() in ["dashscope", "alibaba", "阿里百炼"]:
            # 使用通义千问ReAct专用配置
            from langchain_community.llms import Tongyi
            self.llm = Tongyi()
            self.llm.model_name = llm_model
            print(f"🧠 制造业ReAct LLM初始化: {llm_provider} - {llm_model}")
        else:
            raise ValueError(f"ReAct模式暂只支持阿里百炼，当前: {llm_provider}")
    
    def _create_dummy_callback(self):
        """创建默认的虚拟回调函数，处理progress_callback为None的情况"""
        class DummyProgressCallback:
            def log_event(self, event_type, message):
                pass
            def log_agent_start(self, agent_name):
                pass
            def log_agent_thinking(self, agent_name, thought):
                pass
            def log_api_call(self, api_name, status="调用中"):
                pass
            def log_agent_complete(self, agent_name, result_summary=""):
                pass
            def log_decision_phase(self, phase):
                pass
            def update_progress(self, step, total_steps=None):
                pass
            def __call__(self, message, step=None, total_steps=None):
                pass
        
        return DummyProgressCallback()
    
    def _setup_react_graph(self):
        """设置制造业ReAct智能体工作流图"""
        
        # 创建所有四个ReAct分析师节点
        market_environment_analyst_node = create_market_environment_analyst_react(
            self.llm, self.toolkit
        )
        trend_prediction_analyst_node = create_trend_prediction_analyst_react(
            self.llm, self.toolkit
        )
        industry_news_analyst_node = create_industry_news_analyst_react(
            self.llm, self.toolkit
        )
        consumer_insight_analyst_node = create_consumer_insight_analyst_react(
            self.llm, self.toolkit
        )
        
        # 创建决策层节点（需要memory参数，这里暂时传None）
        optimistic_advisor_node = create_optimistic_advisor(self.llm, None)
        cautious_advisor_node = create_cautious_advisor(self.llm, None)
        decision_coordinator_node = create_decision_coordinator(self.llm, None)
        risk_assessment_node = create_risk_assessment_team(self.llm, None)
        
        # 创建结论提取节点
        conclusion_extractor_node = create_conclusion_extractor(self.llm, None)
        
        # 创建工作流
        workflow = StateGraph(ManufacturingState)
        
        # 分析师名称映射
        analyst_mapping = {
            "market_environment_analyst": ("Market_Environment_Analyst", market_environment_analyst_node),
            "trend_prediction_analyst": ("Trend_Prediction_Analyst", trend_prediction_analyst_node),
            "industry_news_analyst": ("Industry_News_Analyst", industry_news_analyst_node),
            "consumer_insight_analyst": ("Consumer_Insight_Analyst", consumer_insight_analyst_node)
        }
        
        # 根据选择的分析师添加节点
        active_nodes = []
        for analyst_id in self.selected_analysts:
            if analyst_id in analyst_mapping:
                node_name, node_func = analyst_mapping[analyst_id]
                workflow.add_node(node_name, node_func)
                active_nodes.append(node_name)
                print(f"✅ 添加分析师节点: {node_name}")
        
        if not active_nodes:
            # 如果没有选择分析师，默认使用市场环境分析师
            workflow.add_node("Market_Environment_Analyst", market_environment_analyst_node)
            active_nodes = ["Market_Environment_Analyst"]
            print("⚠️ 未选择分析师，使用默认: Market_Environment_Analyst")
        
        # 添加决策层节点
        workflow.add_node("Optimistic_Advisor", optimistic_advisor_node)
        workflow.add_node("Cautious_Advisor", cautious_advisor_node)
        workflow.add_node("Decision_Coordinator", decision_coordinator_node)
        workflow.add_node("Risk_Assessment", risk_assessment_node)
        workflow.add_node("Conclusion_Extractor", conclusion_extractor_node)
        print("✅ 添加决策层节点: 乐观顾问、谨慎顾问、决策协调员、风险评估、结论提取")
        
        # 连接工作流 - 分析师层 → 决策层 → 结束
        if len(active_nodes) == 1:
            # 单个分析师：连接到决策层
            workflow.add_edge(START, active_nodes[0])
            workflow.add_edge(active_nodes[0], "Optimistic_Advisor")
        else:
            # 多个分析师：串行执行后连接到决策层
            workflow.add_edge(START, active_nodes[0])
            
            # 串行连接分析师
            for i in range(len(active_nodes) - 1):
                workflow.add_edge(active_nodes[i], active_nodes[i + 1])
            
            # 最后一个分析师连接到决策层
            workflow.add_edge(active_nodes[-1], "Optimistic_Advisor")
        
        # 连接决策层工作流
        # 乐观顾问 ⇄ 谨慎顾问 的辩论循环
        workflow.add_conditional_edges(
            "Optimistic_Advisor",
            self._should_continue_decision_debate,
            {
                "Cautious_Advisor": "Cautious_Advisor",
                "Decision_Coordinator": "Decision_Coordinator"
            }
        )
        
        workflow.add_conditional_edges(
            "Cautious_Advisor", 
            self._should_continue_decision_debate,
            {
                "Optimistic_Advisor": "Optimistic_Advisor",
                "Decision_Coordinator": "Decision_Coordinator"
            }
        )
        
        # 决策协调员 → 风险评估 → 结论提取 → 结束
        workflow.add_edge("Decision_Coordinator", "Risk_Assessment")
        workflow.add_edge("Risk_Assessment", "Conclusion_Extractor")
        workflow.add_edge("Conclusion_Extractor", END)
        
        # 编译图
        compiled_graph = workflow.compile()
        total_nodes = len(active_nodes) + 5  # 分析师 + 5个决策层节点（乐观、谨慎、协调、风险、结论提取）
        print(f"🏭 制造业ReAct智能体工作流图构建完成")
        print(f"   📊 分析层: {len(active_nodes)} 个分析师")
        print(f"   🎯 决策层: 5 个智能体（乐观顾问、谨慎顾问、协调员、风险评估、结论提取）")
        print(f"   📈 总计: {total_nodes} 个智能体节点")
        
        return compiled_graph
    
    def analyze_manufacturing_replenishment(
        self,
        city_name: str,
        brand_name: str,
        product_category: str,
        target_quarter: str,
        special_focus: str = "",
        progress_callback=None,  # 🎯 新增：进度追踪器参数
    ) -> Dict[str, Any]:
        """执行制造业补货策略分析"""
        
        print(f"🏭 开始制造业ReAct补货分析: {brand_name} {product_category} ({target_quarter})")
        
        # 初始化状态
        initial_state = {
            "city_name": city_name,  # 🎯 修复：添加用户输入的城市到状态
            "product_type": product_category,
            "company_name": brand_name,
            "analysis_date": datetime.now().strftime('%Y-%m-%d'),
            "target_quarter": target_quarter,
            "special_focus": special_focus,
            "messages": [],
            
            # 分析报告字段
            "market_environment_report": "",
            "trend_prediction_report": "",
            "industry_news_report": "",
            "consumer_insight_report": "",
            
            # 决策过程字段
            "decision_debate_state": {
                "optimistic_history": "",
                "cautious_history": "",
                "history": "",
                "current_response": "",
                "decision_consensus": "",
                "count": 0
            },
            "decision_coordination_plan": "",
            "final_replenishment_decision": "",
            "risk_assessment_report": "",  # 🎯 新增：风险评估报告字段
            
            # 其他字段
            "external_data": {},
            "confidence_score": 0.0,
            "risk_level": "中等",
            "progress_callback": progress_callback or self._create_dummy_callback()  # 🎯 新增：传递进度追踪器到状态
        }
        
        # 执行图工作流
        try:
            if self.debug:
                # 调试模式：流式输出 - 使用invoke避免状态累积问题
                print("🔄 调试模式：使用invoke确保状态正确传递")
                final_state = self.graph.invoke(initial_state)
            else:
                # 标准模式：直接调用
                final_state = self.graph.invoke(initial_state)
            
            print("✅ 制造业ReAct补货分析完成")
            return final_state
            
        except Exception as e:
            print(f"❌ 制造业ReAct分析失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return initial_state
    
    def get_analysis_summary(self, final_state: Dict[str, Any]) -> Dict[str, Any]:
        """获取分析摘要"""
        return {
            "product_info": {
                "brand": final_state.get("company_name"),
                "category": final_state.get("product_type"),
                "quarter": final_state.get("target_quarter"),
            },
            "analysis_reports": {
                "market_environment": final_state.get("market_environment_report", ""),
                "trend_prediction": final_state.get("trend_prediction_report", ""),
                "industry_news": final_state.get("industry_news_report", ""),
                "consumer_insight": final_state.get("consumer_insight_report", ""),
            },
            "final_decision": final_state.get("final_replenishment_decision", ""),
            "confidence_score": final_state.get("confidence_score", 0.0),
            "risk_level": final_state.get("risk_level", "中等"),
        }


# 创建制造业ReAct图实例的便捷函数
def create_manufacturing_react_graph(
    selected_analysts=None,
    debug=False,
    config=None
) -> ManufacturingAgentsReactGraph:
    """创建制造业ReAct智能体图实例"""
    if selected_analysts is None:
        selected_analysts = ["market_environment_analyst"]  # 默认只用一个分析师
    
    return ManufacturingAgentsReactGraph(
        selected_analysts=selected_analysts,
        debug=debug,
        config=config
    ) 