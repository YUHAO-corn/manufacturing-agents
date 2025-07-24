"""
解耦的提示词工具模块

提供独立的提示词获取功能，避免智能体对特定提示词管理器的依赖
"""

import os
from pathlib import Path
from typing import Optional


def get_agent_prompt(agent_name: str, default_prompt: Optional[str] = None) -> str:
    """
    获取智能体提示词的解耦函数
    
    Args:
        agent_name: 智能体名称
        default_prompt: 默认提示词（如果文件不存在时使用）
    
    Returns:
        提示词内容
    """
    try:
        # 尝试从提示词管理器获取
        from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager
        prompt = prompt_manager.get_prompt(agent_name)
        if prompt:
            return prompt
    except (ImportError, Exception) as e:
        # 如果提示词管理器不可用，使用默认方案
        print(f"提示词管理器不可用，使用默认提示词: {e}")
    
    # 尝试直接读取文件
    try:
        current_dir = Path(__file__).parent.parent
        prompt_file_map = {
            "market_environment_analyst": "prompts/analysts/market_environment_analyst.txt",
            "trend_prediction_analyst": "prompts/analysts/trend_prediction_analyst.txt",
            "news_analyst": "prompts/analysts/news_analyst.txt",
            "sentiment_insight_analyst": "prompts/analysts/sentiment_insight_analyst.txt",
            "optimistic_advisor": "prompts/advisors/optimistic_advisor.txt",
            "cautious_advisor": "prompts/advisors/cautious_advisor.txt",
            "decision_coordinator": "prompts/coordinator/decision_coordinator.txt",
            "risk_assessment": "prompts/risk_mgmt/risk_assessment.txt",
        }
        
        if agent_name in prompt_file_map:
            prompt_file = current_dir / prompt_file_map[agent_name]
            if prompt_file.exists():
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
    except Exception as e:
        print(f"直接读取提示词文件失败: {e}")
    
    # 返回默认提示词
    if default_prompt:
        return default_prompt
    
    # 最后的后备提示词
    return f"你是一位专业的{agent_name}，请根据输入信息进行分析。"


def get_default_prompts():
    """获取所有默认提示词的字典"""
    return {
        "market_environment_analyst": "你是一位专业的市场环境分析师，负责分析宏观经济指标、制造业景气度、原材料价格、汇率波动、政策变化等影响制造业的环境因素。",
        "trend_prediction_analyst": "你是一位专业的趋势预测分析师，负责预测未来可能影响需求的事件，如天气预报、节假日安排等。",
        "news_analyst": "你是一位专业的新闻分析师，负责分析制造业相关新闻、政策变化和行业资讯，通过事件驱动分析识别连锁反应。",
        "sentiment_insight_analyst": "你是一位专业的情感洞察分析师，负责收集社交媒体、论坛、搜索指数等数据，从个体消费者视角监控消费者讨论趋势。",
        "optimistic_advisor": "你是一位专业的乐观决策顾问，负责识别制造业补货决策中的积极因素和机会。",
        "cautious_advisor": "你是一位专业的谨慎决策顾问，负责识别制造业补货决策中的风险因素和不确定性。",
        "decision_coordinator": "你是一位专业的制造业补货决策协调员，负责整合各方分析和建议，协调决策过程。",
        "risk_assessment": "你是一位专业的制造业补货风险评估专家，负责对补货决策进行全面的风险评估。"
    } 