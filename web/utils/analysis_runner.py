"""
股票分析执行工具
"""

import sys
import os
import uuid
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 确保环境变量正确加载
load_dotenv(project_root / ".env", override=True)

# 添加配置管理器
try:
    from manufacturingagents.config.config_manager import token_tracker
    TOKEN_TRACKING_ENABLED = True
except ImportError:
    TOKEN_TRACKING_ENABLED = False
    print("⚠️ Token跟踪功能未启用")

def extract_risk_assessment(state):
    """从分析状态中提取风险评估数据"""
    try:
        risk_debate_state = state.get('risk_debate_state', {})

        if not risk_debate_state:
            return None

        # 提取各个风险分析师的观点
        risky_analysis = risk_debate_state.get('risky_history', '')
        safe_analysis = risk_debate_state.get('safe_history', '')
        neutral_analysis = risk_debate_state.get('neutral_history', '')
        judge_decision = risk_debate_state.get('judge_decision', '')

        # 格式化风险评估报告
        risk_assessment = f"""
## ⚠️ 风险评估报告

### 🔴 激进风险分析师观点
{risky_analysis if risky_analysis else '暂无激进风险分析'}

### 🟡 中性风险分析师观点
{neutral_analysis if neutral_analysis else '暂无中性风险分析'}

### 🟢 保守风险分析师观点
{safe_analysis if safe_analysis else '暂无保守风险分析'}

### 🏛️ 风险管理委员会最终决议
{judge_decision if judge_decision else '暂无风险管理决议'}

---
*风险评估基于多角度分析，请结合个人风险承受能力做出投资决策*
        """.strip()

        return risk_assessment

    except Exception as e:
        print(f"提取风险评估数据时出错: {e}")
        return None

def run_manufacturing_analysis(city_name, brand_name, product_category, target_quarter, special_focus, 
                             analysts, research_depth, llm_provider, llm_model, progress_callback=None):
    """执行制造业补货策略分析"""
    
    def update_progress(message, step=None, total_steps=None):
        """更新进度"""
        if progress_callback:
            progress_callback(message, step, total_steps)
        print(f"[制造业分析] {message}")

    update_progress("开始制造业补货策略分析...")

    # 生成会话ID用于Token跟踪
    session_id = f"manufacturing_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 估算Token使用
    if TOKEN_TRACKING_ENABLED:
        estimated_input = 3000 * len(analysts)  # 制造业分析更复杂
        estimated_output = 1500 * len(analysts)
        estimated_cost = token_tracker.estimate_cost(llm_provider, llm_model, estimated_input, estimated_output)
        update_progress(f"预估分析成本: ¥{estimated_cost:.4f}")

    # 验证环境变量
    update_progress("检查环境变量配置...")
    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    
    if not dashscope_key:
        raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")

    update_progress("环境变量验证通过")

    try:
        # 导入制造业智能体
        from manufacturingagents.manufacturingagents import (
            create_market_environment_analyst,
            create_trend_prediction_analyst,
            create_news_analyst,
            create_sentiment_insight_analyst,
            create_optimistic_advisor,
            create_cautious_advisor,
            create_decision_coordinator,
            ManufacturingState
        )
        from manufacturingagents.agents.utils.agent_utils import Toolkit
        from manufacturingagents.default_config import DEFAULT_CONFIG
        from manufacturingagents.llm_adapters import ChatDashScope
        from manufacturingagents.agents.utils.memory import FinancialSituationMemory

        # 创建配置
        update_progress("配置制造业分析参数...")
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = llm_provider
        config["deep_think_llm"] = llm_model
        config["quick_think_llm"] = llm_model
        
        # 根据研究深度调整配置
        if research_depth == 1:
            config["max_debate_rounds"] = 1
            config["memory_enabled"] = False
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-turbo"
                config["deep_think_llm"] = "qwen-plus"
        elif research_depth == 2:
            config["max_debate_rounds"] = 1
            config["memory_enabled"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-plus"
                config["deep_think_llm"] = "qwen-plus"
        elif research_depth == 3:
            config["max_debate_rounds"] = 2
            config["memory_enabled"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-plus"
                config["deep_think_llm"] = "qwen-max"
        elif research_depth == 4:
            config["max_debate_rounds"] = 2
            config["memory_enabled"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-plus"
                config["deep_think_llm"] = "qwen-max"
        else:
            config["max_debate_rounds"] = 3
            config["memory_enabled"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-max"
                config["deep_think_llm"] = "qwen-max"

        # 🚀 使用新的ReAct制造业图系统
        update_progress("初始化制造业ReAct分析系统...")
        
        # 调试信息：显示选择的分析师
        update_progress(f"选择的分析师: {analysts} (共{len(analysts)}个)")
        
        # 导入ReAct制造业图
        from manufacturingagents.manufacturingagents.graph.manufacturing_graph_react import ManufacturingAgentsReactGraph
        
        # 创建ReAct图实例
        react_graph = ManufacturingAgentsReactGraph(
            selected_analysts=analysts,  # ✅ 传递前端选择的分析师
            debug=False, 
            config=config
        )
        
        # 执行ReAct分析
        update_progress("开始ReAct多智能体协作分析...")
        state = react_graph.analyze_manufacturing_replenishment(
            city_name=city_name,  # 🎯 修复：传递用户输入的城市
            brand_name=brand_name,
            product_category=product_category,
            target_quarter=target_quarter,
            special_focus=special_focus,
            progress_callback=progress_callback  # 🎯 新增：传递进度追踪器
        )

        # 记录Token使用
        if TOKEN_TRACKING_ENABLED:
            actual_input_tokens = len(analysts) * (2000 if research_depth <= 2 else 3000)
            actual_output_tokens = len(analysts) * (1000 if research_depth <= 2 else 1500)

            usage_record = token_tracker.track_usage(
                provider=llm_provider,
                model_name=llm_model,
                input_tokens=actual_input_tokens,
                output_tokens=actual_output_tokens,
                session_id=session_id,
                analysis_type="manufacturing_analysis"
            )

            if usage_record:
                update_progress(f"记录使用成本: ¥{usage_record.cost:.4f}")

        # 生成最终决策
        decision = generate_manufacturing_decision(state, brand_name, product_category, target_quarter)

        results = {
            'brand_name': brand_name,
            'product_category': product_category,
            'target_quarter': target_quarter,
            'special_focus': special_focus,
            'analysts': analysts,
            'research_depth': research_depth,
            'llm_provider': llm_provider,
            'llm_model': llm_model,
            'state': state,
            'decision': decision,
            'success': True,
            'error': None,
            'session_id': session_id if TOKEN_TRACKING_ENABLED else None
        }

        update_progress("✅ 制造业补货策略分析完成！")
        return results

    except Exception as e:
        print(f"制造业分析失败，错误详情: {str(e)}")
        import traceback
        print(f"完整错误堆栈: {traceback.format_exc()}")
        
        # 返回模拟数据用于演示
        return generate_manufacturing_demo_results(brand_name, product_category, target_quarter, special_focus, analysts, research_depth, llm_provider, llm_model, str(e))

def generate_manufacturing_decision(state, brand_name, product_category, target_quarter):
    """基于分析状态生成制造业补货决策"""
    try:
        # 分析各个报告的内容
        market_report = state.get('market_environment_report', '')
        trend_report = state.get('trend_prediction_report', '')
        news_report = state.get('industry_news_report', '')
        consumer_report = state.get('consumer_insight_report', '')
        
        # 简单的决策逻辑（实际应用中会更复杂）
        positive_indicators = 0
        negative_indicators = 0
        
        # 检查积极指标
        positive_keywords = ['增长', '上升', '积极', '乐观', '扩张', '需求增加', '市场向好']
        negative_keywords = ['下降', '减少', '风险', '谨慎', '收缩', '需求下降', '市场疲软']
        
        all_reports = f"{market_report} {trend_report} {news_report} {consumer_report}"
        
        for keyword in positive_keywords:
            positive_indicators += all_reports.count(keyword)
        
        for keyword in negative_keywords:
            negative_indicators += all_reports.count(keyword)
        
        # 生成决策
        if positive_indicators > negative_indicators * 1.5:
            action = "EXPAND"
            confidence = min(0.9, 0.6 + (positive_indicators - negative_indicators) * 0.1)
            recommendation = f"建议{brand_name}在{target_quarter}积极扩张{product_category}的库存，增加15-25%的补货量"
        elif negative_indicators > positive_indicators * 1.5:
            action = "CONTRACT"
            confidence = min(0.9, 0.6 + (negative_indicators - positive_indicators) * 0.1)
            recommendation = f"建议{brand_name}在{target_quarter}谨慎收缩{product_category}的库存，减少10-20%的补货量"
        else:
            action = "MAINTAIN"
            confidence = 0.7
            recommendation = f"建议{brand_name}在{target_quarter}维持{product_category}的现有库存策略，保持稳定的补货节奏"
        
        return {
            'action': action,
            'confidence': confidence,
            'recommendation': recommendation,
            'risk_score': 1.0 - confidence,
            'reasoning': f'基于市场环境、趋势预测、行业资讯和消费者洞察的综合分析，{recommendation}'
        }
        
    except Exception as e:
        print(f"生成制造业决策失败: {e}")
        return {
            'action': 'MAINTAIN',
            'confidence': 0.5,
            'recommendation': f"由于分析过程中出现问题，建议{brand_name}在{target_quarter}保持{product_category}的现有补货策略",
            'risk_score': 0.5,
            'reasoning': '分析过程中遇到技术问题，建议保持现有策略并进一步收集数据'
        }

def generate_manufacturing_demo_results(brand_name, product_category, target_quarter, special_focus, analysts, research_depth, llm_provider, llm_model, error_msg):
    """生成制造业分析的演示结果"""
    
    demo_state = {
        'product_type': product_category,
        'company_name': brand_name,
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'target_quarter': target_quarter,
        'special_focus': special_focus,
        'market_environment_report': f"""
# 市场环境分析报告 - {brand_name} {product_category}

## 宏观经济环境
当前宏观经济环境对{product_category}行业整体有利。制造业PMI指数保持在50.2，显示行业持续扩张。
消费者信心指数上升至108.5，表明消费需求稳定增长。

## 原材料价格趋势
{product_category}相关原材料价格在过去三个月中保持相对稳定，钢材价格上涨3.2%，塑料原料价格下降1.8%。
预计{target_quarter}原材料成本压力适中。

## 制造业整体运营环境
制造业整体产能利用率达到78%，处于较为健康的水平。
政府对制造业的支持政策持续，包括减税降费和绿色制造激励措施。

## 对{brand_name}的影响评估
基于当前市场环境，{brand_name}的{product_category}产品面临良好的外部环境。
建议在{target_quarter}适度增加库存以应对预期的需求增长。
        """,
        'trend_prediction_report': f"""
# 趋势预测分析报告 - {brand_name} {product_category}

## 需求趋势预测
基于历史数据和季节性分析，{product_category}在{target_quarter}预计需求增长8-12%。
消费者对{brand_name}品牌的偏好度持续上升，市场份额有望扩大。

## 季节性因素分析
{target_quarter}是{product_category}的传统销售旺季，预计销量环比增长15%。
节假日促销活动将进一步推动需求增长。

## 竞争格局预测
主要竞争对手在{target_quarter}预计推出新产品，但{brand_name}的技术优势和品牌影响力依然突出。
预计市场竞争将加剧，但{brand_name}有望保持领先地位。

## 预测结论
综合各项因素，预测{brand_name}的{product_category}在{target_quarter}需求增长10%左右。
建议提前做好产能规划和库存准备。
        """,
        'industry_news_report': f"""
# 行业资讯分析报告 - {brand_name} {product_category}

## 重要新闻事件
1. 政府发布新的制造业支持政策，对{product_category}行业给予税收优惠
2. 主要供应商宣布扩产计划，有助于稳定原材料供应
3. 行业协会发布{product_category}行业发展指导意见，看好未来前景

## 政策环境变化
环保政策趋严，对{product_category}制造企业提出更高要求。
{brand_name}在绿色制造方面的投入将获得政策支持。

## 竞争对手动态
主要竞争对手在技术创新和市场营销方面加大投入。
{brand_name}需要保持技术领先优势，加强品牌建设。

## 市场环境评估
整体市场环境积极向好，{product_category}行业迎来发展机遇期。
建议{brand_name}抓住机遇，在{target_quarter}积极扩张。
        """,
        'consumer_insight_report': f"""
# 消费者洞察分析报告 - {brand_name} {product_category}

## 消费者行为分析
消费者对{product_category}的需求呈现升级趋势，更加注重品质和品牌。
{brand_name}在消费者心目中的品牌形象良好，忠诚度较高。

## 市场情绪分析
社交媒体上关于{brand_name} {product_category}的讨论以正面评价为主。
消费者对{target_quarter}的产品期待较高，预购意愿强烈。

## 购买行为趋势
线上购买比例持续上升，{brand_name}的电商渠道表现优异。
消费者更倾向于在促销期间集中购买，对价格敏感度适中。

## 消费者建议
基于消费者反馈，建议{brand_name}在{target_quarter}：
1. 加强产品质量管控
2. 优化用户体验
3. 适度增加库存以满足需求
        """
    }
    
    demo_decision = {
        'action': 'EXPAND',
        'confidence': 0.75,
        'recommendation': f"基于演示数据分析，建议{brand_name}在{target_quarter}适度扩张{product_category}的库存，增加10-15%的补货量",
        'risk_score': 0.25,
        'reasoning': '演示模式：基于模拟数据的分析结果，实际使用时请配置真实的API密钥获取准确数据'
    }
    
    return {
        'brand_name': brand_name,
        'product_category': product_category,
        'target_quarter': target_quarter,
        'special_focus': special_focus,
        'analysts': analysts,
        'research_depth': research_depth,
        'llm_provider': llm_provider,
        'llm_model': llm_model,
        'state': demo_state,
        'decision': demo_decision,
        'success': False,  # 标记为演示模式
        'error': f"演示模式 - 原始错误: {error_msg}",
        'session_id': None
    }

def run_stock_analysis(brand_name=None, product_category=None, target_quarter=None, special_focus=None, 
                       stock_symbol=None, analysis_date=None, analysts=None, research_depth=None, 
                       llm_provider=None, llm_model=None, market_type="制造业", progress_callback=None, **kwargs):
    """执行分析 - 支持制造业补货分析和股票分析

    Args:
        # 制造业补货分析参数
        brand_name: 品牌名称 (制造业)
        product_category: 产品大类 (制造业)
        target_quarter: 目标季度 (制造业)
        special_focus: 特殊关注点 (制造业)
        
        # 通用参数
        stock_symbol: 股票代码 (兼容性)
        analysis_date: 分析日期
        analysts: 分析师列表
        research_depth: 研究深度
        llm_provider: LLM提供商 (dashscope/google)
        llm_model: 大模型名称
        market_type: 市场类型 (制造业/美股/A股)
        progress_callback: 进度回调函数，用于更新UI状态
    """
    
    # 根据市场类型决定分析方式
    if market_type == "制造业" and brand_name and product_category and target_quarter:
        # 制造业补货分析
        return run_manufacturing_analysis(
            brand_name=brand_name,
            product_category=product_category,
            target_quarter=target_quarter,
            special_focus=special_focus,
            analysts=analysts,
            research_depth=research_depth,
            llm_provider=llm_provider,
            llm_model=llm_model,
            progress_callback=progress_callback
        )
    else:
        # 原有股票分析逻辑（保持兼容性）
        return run_original_stock_analysis(
            stock_symbol=stock_symbol or brand_name,
            analysis_date=analysis_date,
            analysts=analysts,
            research_depth=research_depth,
            llm_provider=llm_provider,
            llm_model=llm_model,
            market_type=market_type,
            progress_callback=progress_callback
        )

def run_original_stock_analysis(stock_symbol, analysis_date, analysts, research_depth, llm_provider, llm_model, market_type="美股", progress_callback=None):
    """原有的股票分析逻辑"""

    def update_progress(message, step=None, total_steps=None):
        """更新进度"""
        if progress_callback:
            progress_callback(message, step, total_steps)
        print(f"[进度] {message}")

    update_progress("开始股票分析...")

    # 生成会话ID用于Token跟踪
    session_id = f"analysis_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 估算Token使用（用于成本预估）
    if TOKEN_TRACKING_ENABLED:
        estimated_input = 2000 * len(analysts)  # 估算每个分析师2000个输入token
        estimated_output = 1000 * len(analysts)  # 估算每个分析师1000个输出token
        estimated_cost = token_tracker.estimate_cost(llm_provider, llm_model, estimated_input, estimated_output)

        update_progress(f"预估分析成本: ¥{estimated_cost:.4f}")

    # 验证环境变量
    update_progress("检查环境变量配置...")
    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")

    print(f"环境变量检查:")
    print(f"  DASHSCOPE_API_KEY: {'已设置' if dashscope_key else '未设置'}")
    print(f"  FINNHUB_API_KEY: {'已设置' if finnhub_key else '未设置'}")

    if not dashscope_key:
        raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
    if not finnhub_key:
        raise ValueError("FINNHUB_API_KEY 环境变量未设置")

    update_progress("环境变量验证通过")

    try:
        # 导入必要的模块
        from manufacturingagents.graph.trading_graph import TradingAgentsGraph
        from manufacturingagents.default_config import DEFAULT_CONFIG

        # 创建配置
        update_progress("配置分析参数...")
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = llm_provider
        config["deep_think_llm"] = llm_model
        config["quick_think_llm"] = llm_model
        # 根据研究深度调整配置
        if research_depth == 1:  # 1级 - 快速分析
            config["max_debate_rounds"] = 1
            config["max_risk_discuss_rounds"] = 1
            config["memory_enabled"] = False  # 禁用记忆功能加速
            config["online_tools"] = False  # 使用缓存数据加速
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-turbo"  # 使用最快模型
                config["deep_think_llm"] = "qwen-plus"
        elif research_depth == 2:  # 2级 - 基础分析
            config["max_debate_rounds"] = 1
            config["max_risk_discuss_rounds"] = 1
            config["memory_enabled"] = True
            config["online_tools"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-plus"
                config["deep_think_llm"] = "qwen-plus"
        elif research_depth == 3:  # 3级 - 标准分析 (默认)
            config["max_debate_rounds"] = 1
            config["max_risk_discuss_rounds"] = 2
            config["memory_enabled"] = True
            config["online_tools"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-plus"
                config["deep_think_llm"] = "qwen-max"
        elif research_depth == 4:  # 4级 - 深度分析
            config["max_debate_rounds"] = 2
            config["max_risk_discuss_rounds"] = 2
            config["memory_enabled"] = True
            config["online_tools"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-plus"
                config["deep_think_llm"] = "qwen-max"
        else:  # 5级 - 全面分析
            config["max_debate_rounds"] = 3
            config["max_risk_discuss_rounds"] = 3
            config["memory_enabled"] = True
            config["online_tools"] = True
            if llm_provider == "dashscope":
                config["quick_think_llm"] = "qwen-max"
                config["deep_think_llm"] = "qwen-max"

        # 根据LLM提供商设置不同的配置
        if llm_provider == "dashscope":
            config["backend_url"] = "https://dashscope.aliyuncs.com/api/v1"
        elif llm_provider == "google":
            # Google AI不需要backend_url，使用默认的OpenAI格式
            config["backend_url"] = "https://api.openai.com/v1"

        # 修复路径问题
        config["data_dir"] = str(project_root / "data")
        config["results_dir"] = str(project_root / "results")
        config["data_cache_dir"] = str(project_root / "tradingagents" / "dataflows" / "data_cache")

        # 确保目录存在
        update_progress("创建必要的目录...")
        os.makedirs(config["data_dir"], exist_ok=True)
        os.makedirs(config["results_dir"], exist_ok=True)
        os.makedirs(config["data_cache_dir"], exist_ok=True)

        print(f"使用配置: {config}")
        print(f"分析师列表: {analysts}")
        print(f"股票代码: {stock_symbol}")
        print(f"分析日期: {analysis_date}")

        # 根据市场类型调整股票代码格式
        if market_type == "A股":
            # A股代码不需要特殊处理，保持原样
            formatted_symbol = stock_symbol
            update_progress(f"准备分析A股: {formatted_symbol}")
        else:
            # 美股代码转为大写
            formatted_symbol = stock_symbol.upper()
            update_progress(f"准备分析美股: {formatted_symbol}")

        # 初始化交易图
        update_progress("初始化分析引擎...")
        graph = TradingAgentsGraph(analysts, config=config, debug=False)

        # 执行分析
        update_progress(f"开始分析 {formatted_symbol} 股票，这可能需要几分钟时间...")
        state, decision = graph.propagate(formatted_symbol, analysis_date)

        # 调试信息
        print(f"🔍 [DEBUG] 分析完成，decision类型: {type(decision)}")
        print(f"🔍 [DEBUG] decision内容: {decision}")

        # 格式化结果
        update_progress("分析完成，正在整理结果...")

        # 提取风险评估数据
        risk_assessment = extract_risk_assessment(state)

        # 将风险评估添加到状态中
        if risk_assessment:
            state['risk_assessment'] = risk_assessment

        # 记录Token使用（实际使用量，这里使用估算值）
        if TOKEN_TRACKING_ENABLED:
            # 在实际应用中，这些值应该从LLM响应中获取
            # 这里使用基于分析师数量和研究深度的估算
            actual_input_tokens = len(analysts) * (1500 if research_depth == "快速" else 2500 if research_depth == "标准" else 4000)
            actual_output_tokens = len(analysts) * (800 if research_depth == "快速" else 1200 if research_depth == "标准" else 2000)

            usage_record = token_tracker.track_usage(
                provider=llm_provider,
                model_name=llm_model,
                input_tokens=actual_input_tokens,
                output_tokens=actual_output_tokens,
                session_id=session_id,
                analysis_type=f"{market_type}_analysis"
            )

            if usage_record:
                update_progress(f"记录使用成本: ¥{usage_record.cost:.4f}")

        results = {
            'stock_symbol': stock_symbol,
            'analysis_date': analysis_date,
            'analysts': analysts,
            'research_depth': research_depth,
            'llm_provider': llm_provider,
            'llm_model': llm_model,
            'state': state,
            'decision': decision,
            'success': True,
            'error': None,
            'session_id': session_id if TOKEN_TRACKING_ENABLED else None
        }

        update_progress("✅ 分析成功完成！")
        return results

    except Exception as e:
        # 打印详细错误信息用于调试
        print(f"真实分析失败，错误详情: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"完整错误堆栈: {traceback.format_exc()}")

        # 如果真实分析失败，返回模拟数据用于演示
        return generate_demo_results(stock_symbol, analysis_date, analysts, research_depth, llm_provider, llm_model, str(e))

def format_analysis_results(results):
    """格式化分析结果用于显示"""
    
    if not results['success']:
        return {
            'error': results['error'],
            'success': False
        }
    
    state = results['state']
    decision = results['decision']

    # 提取关键信息
    # decision 可能是字符串（如 "BUY", "SELL", "HOLD"）或字典
    if isinstance(decision, str):
        formatted_decision = {
            'action': decision.strip().upper(),
            'confidence': 0.7,  # 默认置信度
            'risk_score': 0.3,  # 默认风险分数
            'target_price': None,  # 字符串格式没有目标价格
            'reasoning': f'基于AI分析，建议{decision.strip().upper()}'
        }
    elif isinstance(decision, dict):
        # 处理目标价格 - 确保正确提取数值
        target_price = decision.get('target_price')
        if target_price is not None and target_price != 'N/A':
            try:
                # 尝试转换为浮点数
                if isinstance(target_price, str):
                    # 移除货币符号和空格
                    clean_price = target_price.replace('$', '').replace('¥', '').replace('￥', '').strip()
                    target_price = float(clean_price) if clean_price and clean_price != 'None' else None
                elif isinstance(target_price, (int, float)):
                    target_price = float(target_price)
                else:
                    target_price = None
            except (ValueError, TypeError):
                target_price = None
        else:
            target_price = None

        formatted_decision = {
            'action': decision.get('action', 'HOLD'),
            'confidence': decision.get('confidence', 0.5),
            'risk_score': decision.get('risk_score', 0.3),
            'target_price': target_price,
            'reasoning': decision.get('reasoning', '暂无分析推理')
        }
    else:
        # 处理其他类型
        formatted_decision = {
            'action': 'HOLD',
            'confidence': 0.5,
            'risk_score': 0.3,
            'target_price': None,
            'reasoning': f'分析结果: {str(decision)}'
        }
    
    # 格式化状态信息
    formatted_state = {}
    
    # 处理各个分析模块的结果 - 支持股票和制造业分析
    stock_analysis_keys = [
        'market_report',
        'fundamentals_report', 
        'sentiment_report',
        'news_report',
        'risk_assessment',
        'investment_plan'
    ]
    
    manufacturing_analysis_keys = [
        'market_environment_report',
        'trend_prediction_report',
        'industry_news_report',
        'consumer_insight_report',
        'decision_debate_state',
        'decision_coordination_plan',
        'final_replenishment_decision',
        'risk_assessment_report'  # 🎯 新增：风险评估报告
    ]
    
    # 根据分析类型使用不同的字段映射
    if 'brand_name' in results:
        # 制造业分析
        analysis_keys = manufacturing_analysis_keys
        # 为了前端兼容，将制造业字段映射到标准字段
        field_mapping = {
            'market_environment_report': 'market_report',
            'trend_prediction_report': 'fundamentals_report',
            'industry_news_report': 'news_report',
            'consumer_insight_report': 'sentiment_report'
        }
        
        for original_key, mapped_key in field_mapping.items():
            if original_key in state:
                formatted_state[mapped_key] = state[original_key]
        
        # 🎯 新增：决策层结果映射到前端标签页
        decision_field_mapping = {
            'decision_coordination_plan': 'investment_plan',  # 决策协调方案 → 补货建议标签页
            'final_replenishment_decision': 'final_decision',  # 最终决策 → 决策摘要
        }
        
        for original_key, mapped_key in decision_field_mapping.items():
            if original_key in state and state[original_key]:
                formatted_state[mapped_key] = state[original_key]
                print(f"🎯 [字段映射] {original_key} → {mapped_key}: {len(str(state[original_key]))} 字符")
        
        # 🎯 新增：风险评估映射
        if 'risk_assessment_report' in state and state['risk_assessment_report']:
            formatted_state['risk_assessment'] = state['risk_assessment_report']
            print(f"⚠️ [字段映射] risk_assessment_report → risk_assessment: {len(str(state['risk_assessment_report']))} 字符")
        
        # 🎯 新增：决策辩论单独处理（专门的辩论Tab）
        if 'decision_debate_state' in state:
            debate_state = state['decision_debate_state']
            if debate_state.get('optimistic_history') or debate_state.get('cautious_history'):
                # 单独提取辩论数据给专门的Tab使用
                formatted_state['decision_debate'] = {
                    'optimistic_history': debate_state.get('optimistic_history', ''),
                    'cautious_history': debate_state.get('cautious_history', ''),
                    'count': debate_state.get('count', 0),
                    'history': debate_state.get('history', ''),
                    'decision_consensus': debate_state.get('decision_consensus', '')
                }
                print(f"🎭 [字段映射] decision_debate_state → decision_debate: {debate_state.get('count', 0)} 轮辩论")
                
                # 同时为investment_plan创建辩论摘要（如果需要）
                if 'investment_plan' not in formatted_state:
                    debate_summary = f"""
# 决策协调结果

基于 {debate_state.get('count', 0)} 轮乐观vs谨慎观点的充分辩论，形成最终补货建议。

详细辩论过程请查看"🎭 决策辩论"标签页。
                    """.strip()
                    formatted_state['investment_plan'] = debate_summary
                    print(f"🎭 [字段映射] 辞论摘要 → investment_plan: {len(debate_summary)} 字符")
        
        # 保持原始字段
        for key in manufacturing_analysis_keys:
            if key in state:
                formatted_state[key] = state[key]
    else:
        # 股票分析
        analysis_keys = stock_analysis_keys
        for key in analysis_keys:
            if key in state:
                formatted_state[key] = state[key]
    
    # 格式化返回结果，兼容股票和制造业分析
    formatted_results = {
        'decision': formatted_decision,
        'state': formatted_state,
        'success': True,
        # 将配置信息放在顶层，供前端直接访问
        'analysts': results['analysts'],
        'research_depth': results['research_depth'],
        'llm_provider': results.get('llm_provider', 'dashscope'),
        'llm_model': results['llm_model'],
        'metadata': {
            'analysts': results['analysts'],
            'research_depth': results['research_depth'],
            'llm_provider': results.get('llm_provider', 'dashscope'),
            'llm_model': results['llm_model']
        }
    }
    
    # 根据分析类型添加相应字段
    if 'stock_symbol' in results:
        # 股票分析
        formatted_results.update({
            'stock_symbol': results['stock_symbol'],
            'analysis_date': results['analysis_date'],
        })
        formatted_results['metadata']['analysis_date'] = results['analysis_date']
    elif 'brand_name' in results and 'product_category' in results:
        # 制造业分析
        formatted_results.update({
            'brand_name': results['brand_name'],
            'product_category': results['product_category'],
            'target_quarter': results['target_quarter'],
        })
        formatted_results['metadata'].update({
            'brand_name': results['brand_name'],
            'product_category': results['product_category'],
            'target_quarter': results['target_quarter']
        })
    
    return formatted_results

def validate_analysis_params(stock_symbol, analysis_date, analysts, research_depth):
    """验证分析参数"""
    
    errors = []
    
    # 验证股票代码
    if not stock_symbol or len(stock_symbol.strip()) == 0:
        errors.append("股票代码不能为空")
    elif len(stock_symbol.strip()) > 10:
        errors.append("股票代码长度不能超过10个字符")
    
    # 验证分析师列表
    if not analysts or len(analysts) == 0:
        errors.append("必须至少选择一个分析师")
    
    valid_analysts = ['market', 'social', 'news', 'fundamentals']
    invalid_analysts = [a for a in analysts if a not in valid_analysts]
    if invalid_analysts:
        errors.append(f"无效的分析师类型: {', '.join(invalid_analysts)}")
    
    # 验证研究深度
    if not isinstance(research_depth, int) or research_depth < 1 or research_depth > 5:
        errors.append("研究深度必须是1-5之间的整数")
    
    # 验证分析日期
    try:
        from datetime import datetime
        datetime.strptime(analysis_date, '%Y-%m-%d')
    except ValueError:
        errors.append("分析日期格式无效，应为YYYY-MM-DD格式")
    
    return len(errors) == 0, errors

def get_supported_stocks():
    """获取支持的股票列表"""
    
    # 常见的美股股票代码
    popular_stocks = [
        {'symbol': 'AAPL', 'name': '苹果公司', 'sector': '科技'},
        {'symbol': 'MSFT', 'name': '微软', 'sector': '科技'},
        {'symbol': 'GOOGL', 'name': '谷歌', 'sector': '科技'},
        {'symbol': 'AMZN', 'name': '亚马逊', 'sector': '消费'},
        {'symbol': 'TSLA', 'name': '特斯拉', 'sector': '汽车'},
        {'symbol': 'NVDA', 'name': '英伟达', 'sector': '科技'},
        {'symbol': 'META', 'name': 'Meta', 'sector': '科技'},
        {'symbol': 'NFLX', 'name': '奈飞', 'sector': '媒体'},
        {'symbol': 'AMD', 'name': 'AMD', 'sector': '科技'},
        {'symbol': 'INTC', 'name': '英特尔', 'sector': '科技'},
        {'symbol': 'SPY', 'name': 'S&P 500 ETF', 'sector': 'ETF'},
        {'symbol': 'QQQ', 'name': '纳斯达克100 ETF', 'sector': 'ETF'},
    ]
    
    return popular_stocks

def generate_demo_results(stock_symbol, analysis_date, analysts, research_depth, llm_provider, llm_model, error_msg):
    """生成演示分析结果"""

    import random

    # 生成模拟决策
    actions = ['BUY', 'HOLD', 'SELL']
    action = random.choice(actions)

    demo_decision = {
        'action': action,
        'confidence': round(random.uniform(0.6, 0.9), 2),
        'risk_score': round(random.uniform(0.2, 0.7), 2),
        'target_price': round(random.uniform(100, 300), 2),
        'reasoning': f"""
基于对{stock_symbol}的综合分析，我们的AI分析团队得出以下结论：

**投资建议**: {action}

**主要分析要点**:
1. **技术面分析**: 当前价格趋势显示{'上涨' if action == 'BUY' else '下跌' if action == 'SELL' else '横盘'}信号
2. **基本面评估**: 公司财务状况{'良好' if action == 'BUY' else '一般' if action == 'HOLD' else '需关注'}
3. **市场情绪**: 投资者情绪{'乐观' if action == 'BUY' else '中性' if action == 'HOLD' else '谨慎'}
4. **风险评估**: 当前风险水平为{'中等' if action == 'HOLD' else '较低' if action == 'BUY' else '较高'}

**注意**: 这是演示数据，实际分析需要配置正确的API密钥。
        """
    }

    # 生成模拟状态数据
    demo_state = {}

    if 'market' in analysts:
        demo_state['market_report'] = f"""
## 📈 {stock_symbol} 技术面分析报告

### 价格趋势分析
- **当前价格**: ${round(random.uniform(100, 300), 2)}
- **日内变化**: {random.choice(['+', '-'])}{round(random.uniform(0.5, 5), 2)}%
- **52周高点**: ${round(random.uniform(200, 400), 2)}
- **52周低点**: ${round(random.uniform(50, 150), 2)}

### 技术指标
- **RSI (14日)**: {round(random.uniform(30, 70), 1)}
- **MACD**: {'看涨' if action == 'BUY' else '看跌' if action == 'SELL' else '中性'}
- **移动平均线**: 价格{'高于' if action == 'BUY' else '低于' if action == 'SELL' else '接近'}20日均线

### 支撑阻力位
- **支撑位**: ${round(random.uniform(80, 120), 2)}
- **阻力位**: ${round(random.uniform(250, 350), 2)}

*注意: 这是演示数据，实际分析需要配置API密钥*
        """

    if 'fundamentals' in analysts:
        demo_state['fundamentals_report'] = f"""
## 💰 {stock_symbol} 基本面分析报告

### 财务指标
- **市盈率 (P/E)**: {round(random.uniform(15, 35), 1)}
- **市净率 (P/B)**: {round(random.uniform(1, 5), 1)}
- **净资产收益率 (ROE)**: {round(random.uniform(10, 25), 1)}%
- **毛利率**: {round(random.uniform(20, 60), 1)}%

### 盈利能力
- **营收增长**: {random.choice(['+', '-'])}{round(random.uniform(5, 20), 1)}%
- **净利润增长**: {random.choice(['+', '-'])}{round(random.uniform(10, 30), 1)}%
- **每股收益**: ${round(random.uniform(2, 15), 2)}

### 财务健康度
- **负债率**: {round(random.uniform(20, 60), 1)}%
- **流动比率**: {round(random.uniform(1, 3), 1)}
- **现金流**: {'正向' if action != 'SELL' else '需关注'}

*注意: 这是演示数据，实际分析需要配置API密钥*
        """

    if 'social' in analysts:
        demo_state['sentiment_report'] = f"""
## 💭 {stock_symbol} 市场情绪分析报告

### 社交媒体情绪
- **整体情绪**: {'积极' if action == 'BUY' else '消极' if action == 'SELL' else '中性'}
- **情绪强度**: {round(random.uniform(0.5, 0.9), 2)}
- **讨论热度**: {'高' if random.random() > 0.5 else '中等'}

### 投资者情绪指标
- **恐慌贪婪指数**: {round(random.uniform(20, 80), 0)}
- **看涨看跌比**: {round(random.uniform(0.8, 1.5), 2)}
- **期权Put/Call比**: {round(random.uniform(0.5, 1.2), 2)}

### 机构投资者动向
- **机构持仓变化**: {random.choice(['增持', '减持', '维持'])}
- **分析师评级**: {'买入' if action == 'BUY' else '卖出' if action == 'SELL' else '持有'}

*注意: 这是演示数据，实际分析需要配置API密钥*
        """

    if 'news' in analysts:
        demo_state['news_report'] = f"""
## 📰 {stock_symbol} 新闻事件分析报告

### 近期重要新闻
1. **财报发布**: 公司发布{'超预期' if action == 'BUY' else '低于预期' if action == 'SELL' else '符合预期'}的季度财报
2. **行业动态**: 所在行业面临{'利好' if action == 'BUY' else '挑战' if action == 'SELL' else '稳定'}政策环境
3. **公司公告**: 管理层{'乐观' if action == 'BUY' else '谨慎' if action == 'SELL' else '稳健'}展望未来

### 新闻情绪分析
- **正面新闻占比**: {round(random.uniform(40, 80), 0)}%
- **负面新闻占比**: {round(random.uniform(10, 40), 0)}%
- **中性新闻占比**: {round(random.uniform(20, 50), 0)}%

### 市场影响评估
- **短期影响**: {'正面' if action == 'BUY' else '负面' if action == 'SELL' else '中性'}
- **长期影响**: {'积极' if action != 'SELL' else '需观察'}

*注意: 这是演示数据，实际分析需要配置API密钥*
        """

    # 添加风险评估和投资建议
    demo_state['risk_assessment'] = f"""
## ⚠️ {stock_symbol} 风险评估报告

### 主要风险因素
1. **市场风险**: {'低' if action == 'BUY' else '高' if action == 'SELL' else '中等'}
2. **行业风险**: {'可控' if action != 'SELL' else '需关注'}
3. **公司特定风险**: {'较低' if action == 'BUY' else '中等'}

### 风险等级评估
- **总体风险等级**: {'低风险' if action == 'BUY' else '高风险' if action == 'SELL' else '中等风险'}
- **建议仓位**: {random.choice(['轻仓', '标准仓位', '重仓']) if action != 'SELL' else '建议减仓'}

*注意: 这是演示数据，实际分析需要配置API密钥*
    """

    demo_state['investment_plan'] = f"""
## 📋 {stock_symbol} 投资建议

### 具体操作建议
- **操作方向**: {action}
- **建议价位**: ${round(random.uniform(90, 310), 2)}
- **止损位**: ${round(random.uniform(80, 200), 2)}
- **目标价位**: ${round(random.uniform(150, 400), 2)}

### 投资策略
- **投资期限**: {'短期' if research_depth <= 2 else '中长期'}
- **仓位管理**: {'分批建仓' if action == 'BUY' else '分批减仓' if action == 'SELL' else '维持现状'}

*注意: 这是演示数据，实际分析需要配置API密钥*
    """

    return {
        'stock_symbol': stock_symbol,
        'analysis_date': analysis_date,
        'analysts': analysts,
        'research_depth': research_depth,
        'llm_provider': llm_provider,
        'llm_model': llm_model,
        'state': demo_state,
        'decision': demo_decision,
        'success': True,
        'error': None,
        'is_demo': True,
        'demo_reason': f"API调用失败，显示演示数据。错误信息: {error_msg}"
    }
