# 谨慎决策顾问
# Cautious Decision Advisor for Manufacturing

from langchain_core.messages import AIMessage
import time
import json
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_cautious_advisor(llm, memory):
    """创建谨慎决策顾问"""
    
    def cautious_advisor_node(state):
        print(f"🛡️ [DEBUG] ===== 谨慎决策顾问节点开始 =====")
        
        # 🎯 新增：获取进度追踪器并记录决策阶段
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.update_progress(5)
            progress_callback.log_decision_phase("谨慎决策顾问发言")
        
        decision_debate_state = state["decision_debate_state"]
        history = decision_debate_state.get("history", "")
        cautious_history = decision_debate_state.get("cautious_history", "")
        current_response = decision_debate_state.get("current_response", "")
        
        # 获取分析报告
        market_environment_report = state["market_environment_report"]
        trend_prediction_report = state["trend_prediction_report"]
        industry_news_report = state["industry_news_report"]
        consumer_insight_report = state["consumer_insight_report"]
        
        # 获取产品信息
        product_type = state.get('product_type', 'Unknown')
        company_name = state.get('company_name', 'Unknown')
        
        print(f"🛡️ [DEBUG] 接收到的报告:")
        print(f"🛡️ [DEBUG] - 市场环境报告长度: {len(market_environment_report)}")
        print(f"🛡️ [DEBUG] - 趋势预测报告长度: {len(trend_prediction_report)}")
        print(f"🛡️ [DEBUG] - 行业资讯报告长度: {len(industry_news_report)}")
        print(f"🛡️ [DEBUG] - 消费者洞察报告长度: {len(consumer_insight_report)}")
        print(f"🛡️ [DEBUG] - 产品类型: {product_type}, 公司: {company_name}")
        
        # 🎯 改进：使用提示词管理器获取基础提示词
        base_system_prompt = prompt_manager.get_prompt("cautious_advisor")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的谨慎决策顾问，负责识别制造业补货决策中的风险因素和不确定性。"
        
        # 结合具体任务信息和历史记录构建完整的系统提示词
        system_message = f"""{base_system_prompt}

🎯 当前分析任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}

📊 基础分析报告：
### 市场环境分析
{market_environment_report}

### 趋势预测分析  
{trend_prediction_report}

### 行业资讯分析
{industry_news_report}

### 消费者洞察分析
{consumer_insight_report}

🎭 辩论历史记录：
{history}

📋 特别要求：
- 从风险控制角度识别补货风险和不确定性
- 基于上述分析报告中的真实数据进行风险评估
- 反驳过度乐观的观点，强调潜在风险
- 提供谨慎的补货建议和风险控制措施
- 报告长度控制在600-800字

现在请基于这些分析结果，从谨慎角度提供您的风险评估和补货建议！"""
        
        # 调用LLM
        response = llm.invoke(system_message)
        
        # 格式化回复 - 兼容不同LLM响应格式
        if hasattr(response, 'content'):
            content = response.content
        elif isinstance(response, str):
            content = response
        else:
            content = str(response)
        
        argument = f"谨慎决策顾问: {content}"
        
        # 更新决策辩论状态
        new_decision_debate_state = {
            "history": history + "\n" + argument,
            "optimistic_history": decision_debate_state.get("optimistic_history", ""),
            "cautious_history": cautious_history + "\n" + argument,
            "current_response": argument,
            "decision_consensus": decision_debate_state.get("decision_consensus", ""),
            "count": decision_debate_state.get("count", 0) + 1,
        }
        
        # 更新状态
        state["decision_debate_state"] = new_decision_debate_state
        state["messages"].append(AIMessage(content=argument))
        
        print(f"🛡️ [DEBUG] 谨慎决策顾问分析完成，回复长度: {len(argument)}")
        
        return state
    
    return cautious_advisor_node 