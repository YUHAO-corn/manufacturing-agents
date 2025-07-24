# 制造业智能体模块
# Manufacturing Agents Module
# 基于 TradingAgents-CN 改造的制造业智能补货决策系统

from .analysts.market_environment_analyst import create_market_environment_analyst
from .analysts.trend_prediction_analyst import create_trend_prediction_analyst
from .analysts.news_analyst import create_news_analyst
from .analysts.sentiment_insight_analyst import create_sentiment_insight_analyst

from .advisors.optimistic_advisor import create_optimistic_advisor
from .advisors.cautious_advisor import create_cautious_advisor

from .coordinator.decision_coordinator import create_decision_coordinator

from .risk_mgmt.risk_assessment import create_risk_assessment_team

from .utils.manufacturing_states import ManufacturingState
from .utils.conclusion_extractor import create_conclusion_extractor

__all__ = [
    # 分析师团队
    "create_market_environment_analyst",
    "create_trend_prediction_analyst", 
    "create_news_analyst",
    "create_sentiment_insight_analyst",
    
    # 决策顾问团队
    "create_optimistic_advisor",
    "create_cautious_advisor",
    
    # 决策协调
    "create_decision_coordinator",
    
    # 风险评估
    "create_risk_assessment_team",
    
    # 结论提取
    "create_conclusion_extractor",
    
    # 工具和状态
    "ManufacturingState",
] 