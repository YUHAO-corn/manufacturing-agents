#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业智能体状态管理
Manufacturing Agents State Management

定义制造业补货决策分析过程中的状态结构
"""

from typing import TypedDict, List, Any, Dict, Optional
from langchain_core.messages import BaseMessage


class ManufacturingState(TypedDict):
    """制造业智能体状态定义"""
    
    # === 基础信息 ===
    city_name: str                       # 🎯 修复：目标城市名称（用户输入）
    product_type: str                    # 产品类型（如：空调、冰箱、洗衣机等）
    company_name: str                    # 公司/品牌名称
    analysis_date: str                   # 分析日期
    target_quarter: str                  # 目标季度（如：2025Q2）
    special_focus: str                   # 特殊关注点
    
    # === 消息和通信 ===
    messages: List[BaseMessage]          # 智能体间的消息历史
    external_data: Dict[str, Any]        # 外部数据存储
    
    # === 分析报告 ===
    market_environment_report: str       # 市场环境分析报告
    trend_prediction_report: str         # 趋势预测分析报告
    industry_news_report: str           # 行业新闻分析报告
    consumer_insight_report: str        # 消费者洞察报告
    
    # === 决策过程状态 ===
    decision_debate_state: Dict[str, Any] # 决策辩论状态
    decision_coordination_plan: str      # 决策协调方案
    final_replenishment_decision: str    # 最终补货决策
    risk_assessment_report: str          # 🎯 新增：风险评估报告
    
    # === 结论提取 ===
    conclusion_json: Dict[str, Any]      # 🎯 新增：结构化结论数据
    conclusion_raw: str                  # 🎯 新增：结论提取原始输出
    
    # === 评估指标 ===
    confidence_score: float             # 决策置信度 (0-1)
    risk_level: str                     # 风险等级（低、中、高）
    
    # === 进度追踪 ===
    progress_callback: Any              # 🎯 新增：进度追踪回调函数


class DecisionDebateState(TypedDict):
    """决策辩论状态"""
    optimistic_history: str             # 乐观顾问历史观点
    cautious_history: str               # 谨慎顾问历史观点
    history: str                        # 整体辩论历史
    current_response: str               # 当前回应
    decision_consensus: str             # 决策共识
    count: int                          # 辩论轮次计数


# 便捷的状态创建函数
def create_initial_manufacturing_state(
    product_type: str,
    company_name: str,
    target_quarter: str,
    special_focus: str = "",
    analysis_date: Optional[str] = None
) -> ManufacturingState:
    """创建初始的制造业状态"""
    
    if analysis_date is None:
        from datetime import datetime
        analysis_date = datetime.now().strftime('%Y-%m-%d')
    
    return ManufacturingState(
        # 基础信息
        product_type=product_type,
        company_name=company_name,
        analysis_date=analysis_date,
        target_quarter=target_quarter,
        special_focus=special_focus,
        
        # 消息和通信
        messages=[],
        external_data={},
        
        # 分析报告
        market_environment_report="",
        trend_prediction_report="",
        industry_news_report="",
        consumer_insight_report="",
        
        # 决策过程状态
        decision_debate_state=DecisionDebateState(
            optimistic_history="",
            cautious_history="",
            history="",
            current_response="",
            decision_consensus="",
            count=0
        ),
        decision_coordination_plan="",
        final_replenishment_decision="",
        
        # 结论提取
        conclusion_json={},
        conclusion_raw="",
        
        # 评估指标
        confidence_score=0.0,
        risk_level="中等"
    )


def update_analysis_report(
    state: ManufacturingState,
    report_type: str,
    content: str
) -> ManufacturingState:
    """更新分析报告"""
    
    report_mapping = {
        "market_environment": "market_environment_report",
        "trend_prediction": "trend_prediction_report", 
        "industry_news": "industry_news_report",
        "consumer_insight": "consumer_insight_report"
    }
    
    field_name = report_mapping.get(report_type)
    if field_name and field_name in state:
        state[field_name] = content
    
    return state


def get_analysis_completeness(state: ManufacturingState) -> Dict[str, Any]:
    """获取分析完整性评估"""
    
    reports = {
        "market_environment": state.get("market_environment_report", ""),
        "trend_prediction": state.get("trend_prediction_report", ""),
        "industry_news": state.get("industry_news_report", ""),
        "consumer_insight": state.get("consumer_insight_report", ""),
    }
    
    completed_reports = sum(1 for content in reports.values() if len(content) > 100)
    total_reports = len(reports)
    
    completeness_percentage = (completed_reports / total_reports) * 100
    
    return {
        "completed_reports": completed_reports,
        "total_reports": total_reports,
        "completeness_percentage": completeness_percentage,
        "report_status": reports,
        "is_ready_for_decision": completeness_percentage >= 75
    } 