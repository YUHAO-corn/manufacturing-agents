# 决策协调员
# Decision Coordinator for Manufacturing

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
import time
import json
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_decision_coordinator(llm, memory):
    """创建决策协调员"""
    
    def decision_coordinator_node(state):
        print(f"⚖️ [DEBUG] ===== 决策协调员节点开始 =====")
        
        # 🎯 新增：获取进度追踪器并记录决策阶段
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.update_progress(6)
            progress_callback.log_decision_phase("决策协调员综合分析")
        
        current_date = state["analysis_date"]
        product_type = state["product_type"]
        company_name = state["company_name"]
        
        print(f"⚖️ [DEBUG] 输入参数: product_type={product_type}, company={company_name}, date={current_date}")
        
        # 从提示词管理器获取系统提示词
        base_system_prompt = prompt_manager.get_prompt("decision_coordinator")
        if not base_system_prompt:
            # 如果提示词文件不存在，使用默认提示词
            base_system_prompt = "你是一位专业的制造业补货决策协调员，负责整合各方分析和建议，协调决策过程。"
        
        # 结合具体任务信息构建完整的系统提示词
        system_message = f"""{base_system_prompt}

🎯 当前协调任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}
- 分析日期: {current_date}

📊 需要整合的信息：
- 市场环境分析报告
- 趋势预测分析报告
- 行业资讯分析报告
- 消费者洞察分析报告
- 乐观决策顾问建议
- 谨慎决策顾问建议

📋 特别要求：
- 综合考虑所有分析结果
- 平衡机会与风险
- 提供明确的决策建议
- 包含执行指导和应急预案
- 报告长度不少于1000字

请基于收集到的所有信息，提供最终的补货决策协调报告。"""

        # 创建提示词模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # 创建链
        chain = prompt | llm
        
        print(f"⚖️ [DEBUG] 调用LLM链...")
        result = chain.invoke(state["messages"])
        
        print(f"⚖️ [DEBUG] LLM调用完成")
        
        # 兼容不同LLM响应格式
        if hasattr(result, 'content'):
            llm_content = result.content
        elif isinstance(result, str):
            llm_content = result
        else:
            llm_content = str(result)
        
        # 🎯 修复：使用LLM的真实输出作为决策协调报告
        decision_coordination_report = llm_content
        
        # 更新状态
        state["decision_coordination_plan"] = decision_coordination_report
        state["messages"].append(AIMessage(content=decision_coordination_report))
        
        print(f"⚖️ [DEBUG] 决策协调完成，报告长度: {len(decision_coordination_report)}")
        
        return state
    
    return decision_coordinator_node 