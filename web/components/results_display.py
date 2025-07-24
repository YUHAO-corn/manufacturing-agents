"""
分析结果显示组件
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

def render_results(results):
    """渲染分析结果"""

    if not results:
        st.warning("暂无分析结果")
        return

    # 兼容股票和制造业分析结果
    if 'stock_symbol' in results:
        # 股票分析结果
        symbol_name = results.get('stock_symbol', 'N/A')
        header_emoji = "📊"
        analysis_type = "股票"
    else:
        # 制造业分析结果
        brand_name = results.get('brand_name', 'N/A')
        product_category = results.get('product_category', 'N/A')
        symbol_name = f"{brand_name} {product_category}"
        header_emoji = "🏭"
        analysis_type = "制造业补货"
    
    decision = results.get('decision', {})
    state = results.get('state', {})
    is_demo = results.get('is_demo', False)

    st.markdown("---")
    st.header(f"{header_emoji} {symbol_name} {analysis_type}分析结果")

    # 如果是演示数据，显示提示
    if is_demo:
        st.info("🎭 **演示模式**: 当前显示的是模拟分析数据，用于界面演示。要获取真实分析结果，请配置正确的API密钥。")
        if results.get('demo_reason'):
            with st.expander("查看详细信息"):
                st.text(results['demo_reason'])

    # 补货决策摘要
    render_decision_summary(decision, symbol_name)

    # 分析配置信息
    render_analysis_info(results)

    # 详细分析报告
    render_detailed_analysis(state)

    # 风险提示
    render_risk_warning(is_demo)

def render_analysis_info(results):
    """渲染分析配置信息"""

    with st.expander("📋 分析配置信息", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            llm_provider = results.get('llm_provider', 'dashscope')
            provider_name = {
                'dashscope': '阿里百炼',
                'google': 'Google AI'
            }.get(llm_provider, llm_provider)

            st.metric(
                label="LLM提供商",
                value=provider_name,
                help="使用的AI模型提供商"
            )

        with col2:
            llm_model = results.get('llm_model', 'N/A')
            print(f"🔍 [DEBUG] llm_model from results: {llm_model}")
            model_display = {
                'qwen-turbo': 'Qwen Turbo',
                'qwen-plus': 'Qwen Plus',
                'qwen-max': 'Qwen Max',
                'gemini-2.0-flash': 'Gemini 2.0 Flash',
                'gemini-1.5-pro': 'Gemini 1.5 Pro',
                'gemini-1.5-flash': 'Gemini 1.5 Flash'
            }.get(llm_model, llm_model)

            st.metric(
                label="AI模型",
                value=model_display,
                help="使用的具体AI模型"
            )

        with col3:
            analysts = results.get('analysts', [])
            print(f"🔍 [DEBUG] analysts from results: {analysts}")
            analysts_count = len(analysts) if analysts else 0

            st.metric(
                label="分析师数量",
                value=f"{analysts_count}个",
                help="参与分析的AI分析师数量"
            )

        # 显示分析师列表
        if analysts:
            st.write("**参与的分析师:**")
            analyst_names = {
                'market': '📈 市场技术分析师',
                'fundamentals': '💰 基本面分析师',
                'news': '📰 新闻分析师',
                'social_media': '💭 社交媒体分析师',
                'risk': '⚠️ 风险评估师'
            }

            analyst_list = [analyst_names.get(analyst, analyst) or analyst for analyst in analysts]
            st.write(" • ".join(filter(None, analyst_list)))

def render_decision_summary(decision, stock_symbol=None):
    """渲染补货决策摘要"""

    st.subheader("🎯 补货决策摘要")

    # 🎯 优化为3列布局：补货策略 | 置信度 | 风险评级
    col1, col2, col3 = st.columns(3)

    with col1:
        action = decision.get('action', 'N/A')
        
        # 🎯 制造业补货决策中文映射（更直观）
        action_mapping = {
            'BUY': '📈 扩张',      # 增加补货
            'SELL': '📉 收缩',      # 减少库存  
            'HOLD': '📊 维持',    # 维持现状
            'INCREASE': '📈 扩张', # 增加补货
            'DECREASE': '📉 收缩',  # 减少库存
            'MAINTAIN': '📊 维持' # 维持现状
        }
        
        display_action = action_mapping.get(action.upper(), f"📊 {action}")
        
        # 根据策略类型设置颜色
        if '扩张' in display_action:
            action_delta = "↗️ 增加库存"
            delta_color = "normal"
        elif '收缩' in display_action:
            action_delta = "↘️ 减少库存"
            delta_color = "inverse"
        else:
            action_delta = "→ 保持稳定"
            delta_color = "off"

        st.metric(
            label="💡 补货策略",
            value=display_action,
            delta=action_delta,
            delta_color=delta_color,
            help="基于AI多智能体分析的补货决策建议"
        )

    with col2:
        confidence = decision.get('confidence', 0)
        if isinstance(confidence, (int, float)):
            confidence_str = f"{confidence:.1%}"
            confidence_delta = f"{confidence-0.5:.1%}" if confidence != 0 else None
        else:
            confidence_str = str(confidence)
            confidence_delta = None

        st.metric(
            label="置信度",
            value=confidence_str,
            delta=confidence_delta,
            help="AI对分析结果的置信度"
        )

    with col3:
        risk_score = decision.get('risk_score', 0)
        if isinstance(risk_score, (int, float)):
            risk_percentage = risk_score * 100
            
            # 🎯 风险等级分类显示
            if risk_score <= 0.3:
                risk_level = "🟢 低风险"
                risk_delta = "✅ 安全区间"
                delta_color = "normal"
            elif risk_score <= 0.6:
                risk_level = "🟡 中等风险"
                risk_delta = "⚠️ 需关注"
                delta_color = "off"
            else:
                risk_level = "🔴 高风险"
                risk_delta = "⛔ 需谨慎"
                delta_color = "inverse"
                
            risk_display = f"{risk_percentage:.0f}分"
        else:
            risk_level = "📊 评估中"
            risk_display = str(risk_score)
            risk_delta = "计算中..."
            delta_color = "off"

        st.metric(
            label="⚠️ 风险评级",
            value=f"{risk_display} {risk_level.split(' ')[1]}",
            delta=risk_delta,
            delta_color=delta_color,
            help=f"决策风险评估：{risk_level}（{risk_display}/100分）"
        )


    
    # 分析推理
    if 'reasoning' in decision and decision['reasoning']:
        with st.expander("🧠 AI分析推理", expanded=True):
            st.markdown(decision['reasoning'])

def render_detailed_analysis(state):
    """渲染详细分析报告"""
    
    st.subheader("📋 详细分析报告")
    
    # 定义分析模块
    analysis_modules = [
        {
            'key': 'market_report',
            'title': '🌍 市场环境分析',
            'icon': '🌍',
            'description': '宏观经济环境、制造业景气度、原材料价格分析'
        },
        {
            'key': 'fundamentals_report', 
            'title': '📈 趋势预测分析',
            'icon': '📈',
            'description': '需求趋势、市场预测、季节性因素分析'
        },
        {
            'key': 'sentiment_report',
            'title': '💭 消费者洞察分析', 
            'icon': '💭',
            'description': '消费者情绪、购买意愿、舆情监控'
        },
        {
            'key': 'news_report',
            'title': '📰 行业资讯分析',
            'icon': '📰', 
            'description': '行业新闻、政策变化、竞争对手动态'
        },
        {
            'key': 'decision_debate',
            'title': '🎭 决策辩论',
            'icon': '🎭',
            'description': '乐观vs谨慎决策顾问的完整辩论过程'
        },
        {
            'key': 'risk_assessment',
            'title': '⚠️ 风险评估',
            'icon': '⚠️',
            'description': '补货风险因素识别、风险等级评估'
        },
        {
            'key': 'investment_plan',
            'title': '📋 补货建议',
            'icon': '📋',
            'description': '具体补货策略、库存管理建议'
        }
    ]
    
    # 创建标签页
    tabs = st.tabs([f"{module['icon']} {module['title']}" for module in analysis_modules])
    
    for i, (tab, module) in enumerate(zip(tabs, analysis_modules)):
        with tab:
            if module['key'] in state and state[module['key']]:
                st.markdown(f"*{module['description']}*")
                
                # 🎯 特殊处理：决策辩论Tab
                if module['key'] == 'decision_debate':
                    render_debate_content(state[module['key']])
                else:
                    # 原有的格式化显示内容
                    content = state[module['key']]
                    if isinstance(content, str):
                        st.markdown(content)
                    elif isinstance(content, dict):
                        # 如果是字典，格式化显示
                        for key, value in content.items():
                            st.subheader(key.replace('_', ' ').title())
                            st.write(value)
                    else:
                        st.write(content)
            else:
                st.info(f"暂无{module['title']}数据")

def render_debate_content(debate_data):
    """渲染决策辩论内容的专门函数"""
    
    if isinstance(debate_data, dict):
        # 如果是字典格式，提取辩论历史
        optimistic_history = debate_data.get('optimistic_history', '')
        cautious_history = debate_data.get('cautious_history', '')
        debate_count = debate_data.get('count', 0)
        
        if optimistic_history or cautious_history:
            # 显示辩论统计
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎭 辩论轮次", f"{debate_count} 轮")
            with col2:
                optimistic_count = len([line for line in optimistic_history.split('\n') if '乐观决策顾问:' in line])
                st.metric("🌟 乐观发言", f"{optimistic_count} 次")
            with col3:
                cautious_count = len([line for line in cautious_history.split('\n') if '谨慎决策顾问:' in line])
                st.metric("🛡️ 谨慎发言", f"{cautious_count} 次")
            
            st.markdown("---")
            
            # 🎯 交替显示辩论内容（时间顺序）
            st.subheader("💬 辩论过程回放")
            
            # 解析并时间排序辩论内容
            all_statements = []
            
            # 解析乐观观点
            if optimistic_history:
                optimistic_statements = [s.strip() for s in optimistic_history.split('\n') if s.strip() and '乐观决策顾问:' in s]
                for i, stmt in enumerate(optimistic_statements):
                    all_statements.append({
                        'round': i + 1,
                        'type': 'optimistic',
                        'content': stmt.replace('乐观决策顾问:', '').strip(),
                        'order': i * 2  # 乐观顾问总是先发言
                    })
            
            # 解析谨慎观点
            if cautious_history:
                cautious_statements = [s.strip() for s in cautious_history.split('\n') if s.strip() and '谨慎决策顾问:' in s]
                for i, stmt in enumerate(cautious_statements):
                    all_statements.append({
                        'round': i + 1,
                        'type': 'cautious',
                        'content': stmt.replace('谨慎决策顾问:', '').strip(),
                        'order': i * 2 + 1  # 谨慎顾问总是回应
                    })
            
            # 按顺序显示辩论
            all_statements.sort(key=lambda x: x['order'])
            
            for stmt in all_statements:
                if stmt['type'] == 'optimistic':
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #4CAF50;">
                        <h4>🌟 乐观决策顾问 - 第{stmt['round']}轮发言</h4>
                        <p>{stmt['content']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #ff9800;">
                        <h4>🛡️ 谨慎决策顾问 - 第{stmt['round']}轮回应</h4>
                        <p>{stmt['content']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ 本次分析中未进行决策辩论")
    
    elif isinstance(debate_data, str):
        # 如果是字符串格式，直接显示
        st.markdown(debate_data)
    else:
        st.error("⚠️ 辩论数据格式异常")

def render_risk_warning(is_demo=False):
    """渲染风险提示"""

    st.markdown("---")
    st.subheader("⚠️ 重要风险提示")

    # 使用Streamlit的原生组件而不是HTML
    if is_demo:
        st.warning("**演示数据**: 当前显示的是模拟数据，仅用于界面演示")
        st.info("**真实分析**: 要获取真实分析结果，请配置正确的API密钥")

    st.error("""
    **补货风险提示**:
    - **仅供参考**: 本分析结果仅供参考，不构成补货决策建议
    - **运营风险**: 制造业补货有风险，可能导致库存积压或供应不足
    - **理性决策**: 请结合多方信息进行理性补货决策
    - **专业咨询**: 重大补货决策建议咨询专业供应链顾问
    - **自担风险**: 补货决策及其后果由决策者自行承担
    """)

    # 添加时间戳
    st.caption(f"分析生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def create_price_chart(price_data):
    """创建价格走势图"""
    
    if not price_data:
        return None
    
    fig = go.Figure()
    
    # 添加价格线
    fig.add_trace(go.Scatter(
        x=price_data['date'],
        y=price_data['price'],
        mode='lines',
        name='股价',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # 设置图表样式
    fig.update_layout(
        title="股价走势图",
        xaxis_title="日期",
        yaxis_title="价格 ($)",
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def create_sentiment_gauge(sentiment_score):
    """创建情绪指标仪表盘"""
    
    if sentiment_score is None:
        return None
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "市场情绪指数"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightgreen"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    return fig
