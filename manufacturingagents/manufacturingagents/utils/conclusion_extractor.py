# 结论提取智能体
# Conclusion Extractor for Manufacturing

from langchain_core.messages import AIMessage
import time
import json
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_conclusion_extractor(llm, memory):
    """创建结论提取智能体"""
    
    def conclusion_extractor_node(state):
        print(f"📋 [DEBUG] ===== 结论提取智能体节点开始 =====")
        
        # 🎯 获取进度追踪器并记录阶段
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.update_progress(7)
            progress_callback.log_decision_phase("结论提取智能体生成结构化输出")
        
        current_date = state["analysis_date"]
        product_type = state["product_type"]
        company_name = state["company_name"]
        
        print(f"📋 [DEBUG] 输入参数: product_type={product_type}, company={company_name}, date={current_date}")
        
        # 获取决策协调报告和风险评估报告
        decision_coordination_plan = state.get("decision_coordination_plan", "")
        risk_assessment_report = state.get("risk_assessment_report", "")
        
        print(f"📋 [DEBUG] 决策协调报告长度: {len(decision_coordination_plan)}")
        print(f"📋 [DEBUG] 风险评估报告长度: {len(risk_assessment_report)}")
        
        # 🎯 使用提示词管理器获取基础提示词
        base_system_prompt = prompt_manager.get_prompt("conclusion_extractor")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的结论提取专家，负责从分析报告中提取关键结论并输出JSON格式数据。"
        
        # 结合具体任务信息构建完整的系统提示词
        system_message = f"""{base_system_prompt}

🎯 当前提取任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}
- 分析日期: {current_date}

📊 需要提取结论的报告内容：

### 决策协调员报告
{decision_coordination_plan}

### 风险评估报告
{risk_assessment_report}

📋 特别要求：
- 严格按照JSON格式输出，不得包含其他文字
- 确保策略、幅度、风险逻辑一致
- 所有数值必须准确反映报告内容
- emoji使用必须与策略匹配

现在请基于上述报告内容，提取关键结论并输出标准JSON格式！"""
        
        # 调用LLM
        response = llm.invoke(system_message)
        
        # 格式化回复 - 兼容不同LLM响应格式
        if hasattr(response, 'content'):
            content = response.content
        elif isinstance(response, str):
            content = response
        else:
            content = str(response)
        
        print(f"📋 [DEBUG] LLM原始输出: {content[:200]}...")
        
        # 🎯 尝试提取和验证JSON
        try:
            # 提取JSON内容（处理可能的markdown格式）
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                
                # 验证JSON格式
                conclusion_data = json.loads(json_content)
                
                print(f"📋 [DEBUG] JSON提取成功: {json.dumps(conclusion_data, ensure_ascii=False, indent=2)}")
                
                # 保存结构化结论
                state["conclusion_json"] = conclusion_data
                state["conclusion_raw"] = content
                
            else:
                print(f"📋 [WARNING] 无法提取有效JSON，使用原始输出")
                state["conclusion_raw"] = content
                state["conclusion_json"] = None
                
        except json.JSONDecodeError as e:
            print(f"📋 [ERROR] JSON解析失败: {e}")
            state["conclusion_raw"] = content
            state["conclusion_json"] = None
        
        # 更新消息
        state["messages"].append(AIMessage(content=content))
        
        print(f"📋 [DEBUG] 结论提取完成，输出长度: {len(content)}")
        
        return state
    
    return conclusion_extractor_node 