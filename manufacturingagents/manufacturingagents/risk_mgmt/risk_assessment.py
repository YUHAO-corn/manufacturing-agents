# 风险评估团队
# Risk Assessment Team for Manufacturing

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
import time
import json
from datetime import datetime
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_risk_assessment_team(llm, memory):
    """创建风险评估团队"""
    
    def risk_assessment_node(state):
        print(f"⚠️ [DEBUG] ===== 风险评估团队节点开始 =====")
        
        # 🎯 新增：获取进度追踪器并记录风险评估阶段
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.update_progress(5)
            progress_callback.log_risk_assessment("风险评估团队开始全面评估")
        
        product_type = state.get('product_type', 'Unknown')
        company_name = state.get('company_name', 'Unknown')
        
        print(f"⚠️ [DEBUG] 输入参数: product_type={product_type}, company={company_name}")
        
        # 🎯 改进：使用提示词管理器获取基础提示词
        base_system_prompt = prompt_manager.get_prompt("risk_assessment")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的制造业补货风险评估专家，负责对补货决策进行全面的风险评估。"
        
        # 获取所有分析报告和决策建议
        market_environment_report = state.get("market_environment_report", "")
        trend_prediction_report = state.get("trend_prediction_report", "")
        industry_news_report = state.get("industry_news_report", "")
        consumer_insight_report = state.get("consumer_insight_report", "")
        decision_coordination_plan = state.get("decision_coordination_plan", "")
        
        # 结合具体任务信息构建完整的系统提示词
        system_message = f"""{base_system_prompt}

🎯 当前风险评估任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}

📊 需要评估的分析报告：
### 市场环境分析报告
{market_environment_report}

### 趋势预测分析报告
{trend_prediction_report}

### 行业资讯分析报告
{industry_news_report}

### 消费者洞察分析报告
{consumer_insight_report}

### 决策协调方案
{decision_coordination_plan}

📋 特别要求：
- 对上述所有分析结果进行全面的风险评估
- 识别补货决策中的各类风险点和不确定性
- 量化风险概率和影响程度
- 提供具体的风险控制和缓解措施
- 形成最终的综合风险评估和补货建议
- 报告长度控制在1000-1500字

现在请基于这些综合信息，进行全面的风险评估并提供最终的补货建议！"""

        # 创建提示词模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # 创建链
        chain = prompt | llm
        
        print(f"⚠️ [DEBUG] 调用LLM链...")
        result = chain.invoke(state["messages"])
        
        print(f"⚠️ [DEBUG] LLM调用完成")
        
        # 兼容不同LLM响应格式
        if hasattr(result, 'content'):
            llm_content = result.content
        elif isinstance(result, str):
            llm_content = result
        else:
            llm_content = str(result)
        
        # 🎯 修复：直接使用LLM的真实输出作为风险评估报告
        risk_assessment_report = llm_content
        
        # 更新状态
        state["risk_assessment_report"] = risk_assessment_report
        state["messages"].append(AIMessage(content=risk_assessment_report))
        
        print(f"⚠️ [DEBUG] 风险评估完成，报告长度: {len(risk_assessment_report)}")
        
        return state
    
    return risk_assessment_node 