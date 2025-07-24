#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业消费者洞察分析师 - ReAct Agent版本
Consumer Insight Analyst for Manufacturing - ReAct Agent Version

专为阿里百炼LLM优化的ReAct Agent实现
"""

from langchain_core.tools import BaseTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json
# 🎯 新增：导入提示词管理器
from manufacturingagents.manufacturingagents.prompts.prompt_manager import prompt_manager


def create_consumer_insight_analyst_react(llm, toolkit):
    """创建ReAct模式的制造业消费者洞察分析师（适用于阿里百炼）"""
    
    def consumer_insight_analyst_react_node(state):
        print(f"💭 [DEBUG] ===== ReAct消费者洞察分析师节点开始 =====")
        
        current_date = state["analysis_date"]
        product_type = state["product_type"]
        company_name = state["company_name"]
        target_quarter = state["target_quarter"]
        
        # 🎯 新增：获取进度追踪器并记录分析师启动
        progress_callback = state.get('progress_callback')
        if progress_callback:
            progress_callback.log_agent_start("💭 消费者洞察分析师")
            progress_callback.update_progress(4)
            progress_callback.log_agent_thinking("💭 消费者洞察分析师", "需要消费者舆情和行为数据")
        
        print(f"💭 [DEBUG] 输入参数: product_type={product_type}, company={company_name}, target_quarter={target_quarter}")
        
        # 创建消费者洞察专用工具：舆情和行为数据
        class ManufacturingConsumerSentimentTool(BaseTool):
            name: str = "get_manufacturing_consumer_sentiment"
            description: str = f"获取消费者舆情数据，分析{product_type}品牌的消费者情绪和品牌偏好。参数：品牌关键词"
            
            def _run(self, brand_keyword: str = "") -> str:
                try:
                    # 🎯 新增：记录API调用
                    if progress_callback:
                        progress_callback.log_api_call("消费者舆情数据", "调用中")
                    
                    print(f"💭 [DEBUG] ManufacturingConsumerSentimentTool调用，产品类型: {product_type}")
                    # 暂时使用模拟数据，后续可接入真实舆情API
                    if not brand_keyword:
                        brand_keyword = f"{company_name} {product_type}"
                    
                    # 模拟舆情数据
                    sentiment_data = f"""
## 消费者舆情分析数据 ({brand_keyword})

### 社交媒体情绪分析 (最近30天)
- 正面情绪: 68%
- 中性情绪: 22% 
- 负面情绪: 10%

### 品牌提及热词
- 节能: 出现562次
- 静音: 出现438次
- 智能: 出现721次
- 价格: 出现892次
- 售后: 出现234次

### 竞品对比舆情
- {company_name}品牌情绪指数: 7.2/10
- 行业平均情绪指数: 6.8/10
- 主要优势: 技术创新、性价比
- 主要问题: 部分用户反馈安装服务

### 购买决策因素分析
1. 价格敏感度: 中等 (65%)
2. 品牌忠诚度: 较高 (72%)
3. 功能需求: 节能环保 (78%)
4. 购买时机: 夏季促销期 (83%)

### 消费者画像洞察
- 主力消费群体: 25-45岁家庭用户
- 购买渠道偏好: 线上63%, 线下37%
- 决策周期: 平均2.3周
- 复购意愿: 76%
"""
                    # 🎯 新增：记录API调用成功
                    if progress_callback:
                        progress_callback.log_api_call("消费者舆情数据", "成功")
                    
                    return sentiment_data
                except Exception as e:
                    # 🎯 新增：记录API调用失败
                    if progress_callback:
                        progress_callback.log_api_call("消费者舆情数据", "失败")
                    return f"获取消费者舆情数据失败: {str(e)}"

        class ManufacturingConsumerBehaviorTool(BaseTool):
            name: str = "get_manufacturing_consumer_behavior"  
            description: str = f"获取消费者行为数据，分析{product_type}的购买模式和市场偏好趋势。参数：行为分析维度"
            
            def _run(self, behavior_dimension: str = "") -> str:
                try:
                    print(f"💭 [DEBUG] ManufacturingConsumerBehaviorTool调用，产品类型: {product_type}")
                    
                    # 模拟消费者行为数据
                    behavior_data = f"""
## 消费者行为分析数据 ({company_name} {product_type})

### 购买行为模式分析
- 首次购买动机: 新装修(45%), 替换旧产品(38%), 功能升级(17%)
- 平均决策时间: 2.3周
- 信息搜集渠道: 官网(32%), 电商平台(41%), 社交媒体(27%)
- 价格对比频次: 平均对比3.7个品牌

### 购买时机分析
- 旺季购买: 5-8月 (占全年62%)
- 促销敏感度: 高 (74%用户等待促销)
- 节假日购买: 五一、国庆期间增长35%
- 换季购买: 春季(18%), 夏季(52%), 秋季(21%), 冬季(9%)

### 产品偏好特征
- 功率需求: 1.5匹(38%), 1匹(28%), 2匹(24%), 其他(10%)
- 功能偏好: 变频(67%), 智能控制(54%), 除湿(41%), 自清洁(33%)
- 价格区间: 2000-3000元(42%), 3000-5000元(35%), 5000+元(23%)

### 购买决策影响因素
1. 品牌信任度: 权重25%
2. 价格合理性: 权重23%  
3. 节能效果: 权重18%
4. 售后服务: 权重16%
5. 外观设计: 权重12%
6. 朋友推荐: 权重6%

### 忠诚度与复购
- 品牌忠诚度: 72% (行业平均68%)
- 推荐意愿: 78%
- 复购周期: 6-8年
- 服务满意度: 84%
"""
                    return behavior_data
                except Exception as e:
                    return f"获取消费者行为数据失败: {str(e)}"

        # 配置消费者洞察专用工具
        tools = [
            ManufacturingConsumerSentimentTool(),
            ManufacturingConsumerBehaviorTool()
        ]
        
        # 🎯 关键修复：使用txt文件中的专业提示词
        base_system_prompt = prompt_manager.get_prompt("sentiment_insight_analyst")
        if not base_system_prompt:
            # 降级处理：如果提示词文件不可用，使用简化版本
            base_system_prompt = "你是一位专业的情感洞察分析师，负责收集社交媒体、论坛、搜索指数等数据，从个体消费者视角监控消费者讨论趋势。"
        
        # 🎯 修复：使用专业提示词 + 具体任务参数
        query = f"""{base_system_prompt}

🎯 当前分析任务：
- 分析产品类型: {product_type}
- 分析公司: {company_name}
- 分析日期: {current_date}
- 目标季度: {target_quarter}

🔧 工具使用说明：
- 必须调用get_manufacturing_consumer_sentiment获取消费者舆情数据
- 必须调用get_manufacturing_consumer_behavior获取消费者行为数据

📋 执行要求：
- 必须严格按照提示词中的报告格式输出
- 必须在每个章节包含具体的数据支撑
- 必须使用**粗体**标记关键信息和结论
- 必须在报告开头提供"💡 核心决策建议"
- 报告长度不少于800字
- 重点分析对{target_quarter}季度补货的影响

现在请开始执行分析任务！"""

        print(f"💭 [DEBUG] 执行ReAct Agent查询...")
        
        try:
            # 🎯 新增：记录开始分析
            if progress_callback:
                progress_callback.log_event("progress", "💭 消费者洞察分析师：开始数据分析...")
            
            # 创建ReAct Agent
            prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,  # 🎯 修复：减少迭代次数，避免重复调用
                max_execution_time=300,
                return_intermediate_steps=True
            )
            
            result = agent_executor.invoke({'input': query})
            
            report = result.get('output', '分析失败')
            print(f"💭 [消费者洞察分析师] ReAct Agent完成，报告长度: {len(report)}")
            
            # 🎯 新增：记录分析完成
            if progress_callback:
                progress_callback.log_agent_complete("💭 消费者洞察分析师", f"生成{len(report)}字分析报告")
            
        except Exception as e:
            print(f"💭 [ERROR] ReAct Agent执行失败: {str(e)}")
            
            # 🎯 新增：记录分析失败
            if progress_callback:
                progress_callback.log_error(f"💭 消费者洞察分析师失败: {str(e)}")
            
            report = f"消费者洞察分析失败：{str(e)}"
        
        print(f"💭 [DEBUG] ===== ReAct消费者洞察分析师节点结束 =====")
        
        # 更新状态
        new_state = state.copy()
        new_state["consumer_insight_report"] = report
        print(f"💭 [DEBUG] 状态更新完成，报告长度: {len(report)}")
        
        return new_state
    
    return consumer_insight_analyst_react_node 