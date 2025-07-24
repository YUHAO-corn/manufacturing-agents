"""
分析表单组件
"""

import streamlit as st
import datetime
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from web.utils.text_manager import text_manager
except ImportError:
    # 如果导入失败，使用默认值
    text_manager = None

def render_analysis_form():
    """渲染补货分析表单"""
    
    # 获取文案
    if text_manager:
        config_title = text_manager.get_text("analysis_config", "补货分析配置")
    else:
        config_title = "补货分析配置"
    
    st.subheader(f"📋 {config_title}")
    
    # 时间信息展示（只读，不可编辑）
    current_date = datetime.date.today()
    forecast_end_date = current_date + datetime.timedelta(days=30)
    
    st.info(f"📅 **分析基准日期**: {current_date.strftime('%Y年%m月%d日')} | **预测周期**: 短期预测(未来一个月，至{forecast_end_date.strftime('%Y年%m月%d日')})")
    
    # 创建表单
    with st.form("analysis_form", clear_on_submit=False):
        # 核心输入区域
        st.markdown("### 🎯 核心分析参数")
        
        # 城市输入
        st.markdown("#### 🏙️ 目标城市")
        col1, col2 = st.columns([3, 1])
        with col1:
            city_name = st.text_input(
                "输入城市名称",
                value="广州",
                placeholder="输入目标城市名称，如：广州、深圳、北京、上海等",
                help="输入要分析的目标城市，支持全国所有城市",
                label_visibility="collapsed"
            ).strip()
        with col2:
            st.markdown("**快速填入:**")
            st.markdown("广州、深圳、北京、上海等")
        
        # 品牌输入
        st.markdown("#### 🏭 品牌名称")
        col1, col2 = st.columns([3, 1])
        with col1:
            brand_name = st.text_input(
                "输入品牌名称",
                value="美的",
                placeholder="输入品牌名称，如：美的、格力、海尔、小米、华为等",
                help="输入要分析的制造业品牌名称，支持任意品牌",
                label_visibility="collapsed"
            ).strip()
        with col2:
            st.markdown("**快速填入:**")
            st.markdown("美的、格力、海尔、小米等")
        
        # 产品输入
        st.markdown("#### 📦 产品大类")
        col1, col2 = st.columns([3, 1])
        with col1:
            product_category = st.text_input(
                "输入产品大类",
                value="空调",
                placeholder="输入产品大类，如：空调、冰箱、洗衣机、手机、汽车等",
                help="输入要分析的产品大类，支持任意产品类型",
                label_visibility="collapsed"
            ).strip()
        with col2:
            st.markdown("**快速填入:**")
            st.markdown("空调、冰箱、洗衣机、手机等")
        
        # 分割线
        st.markdown("---")
        
        # 其他设置
        col1, col2 = st.columns(2)
        
        with col1:
            # 研究深度
            research_depth = st.select_slider(
                "研究深度 🔍",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: {
                    1: "1级 - 快速分析",
                    2: "2级 - 基础分析",
                    3: "3级 - 标准分析",
                    4: "4级 - 深度分析",
                    5: "5级 - 全面分析"
                }[x],
                help="选择分析的深度级别，级别越高分析越详细但耗时更长"
            )
        
        with col2:
            # 分析师团队选择（紧凑显示）
            st.markdown("**👥 分析师团队**")
            market_analyst = st.checkbox("🌍 市场环境分析师", value=True, key="analyst_market")
            trend_analyst = st.checkbox("📈 趋势预测分析师", value=True, key="analyst_trend")
            news_analyst = st.checkbox("📰 新闻资讯分析师", value=True, key="analyst_news")
            sentiment_analyst = st.checkbox("💭 舆情洞察分析师", value=True, key="analyst_sentiment")
        
        # 特殊关注点输入
        st.markdown("### 🎯 分析定制（可选）")
        special_focus = st.text_area(
            "特殊关注点",
            value="",
            placeholder="如：关注原材料价格波动、重点分析竞争对手动态、注意政策变化影响、关注季节性因素等",
            help="输入特殊关注点，指导智能体重点关注某些分析维度（可选）",
            height=60
        )
        
        # 收集选中的分析师
        selected_analysts = []
        if market_analyst:
            selected_analysts.append(("market_environment_analyst", "市场环境分析师"))
        if trend_analyst:
            selected_analysts.append(("trend_prediction_analyst", "趋势预测分析师"))
        if news_analyst:
            selected_analysts.append(("industry_news_analyst", "行业资讯分析师"))
        if sentiment_analyst:
            selected_analysts.append(("consumer_insight_analyst", "消费者洞察分析师"))
        
        # 验证输入
        input_valid = True
        error_messages = []
        
        if not city_name:
            error_messages.append("请输入目标城市")
            input_valid = False
        if not brand_name:
            error_messages.append("请输入品牌名称")
            input_valid = False
        if not product_category:
            error_messages.append("请输入产品大类")
            input_valid = False
        if len(selected_analysts) == 0:
            error_messages.append("请至少选择一个分析师")
            input_valid = False
        
        # 显示验证状态
        if input_valid:
            st.success(f"✅ 准备分析: {city_name} {brand_name} {product_category} | 已选择 {len(selected_analysts)} 个分析师")
        else:
            for error in error_messages:
                st.error(f"❌ {error}")

        # 提交按钮
        if input_valid:
            submit_label = f"开始 {city_name} {brand_name} {product_category} 补货策略分析"
        else:
            submit_label = "请完善输入信息"
            
        submitted = st.form_submit_button(
            f"🚀 {submit_label}",
            type="primary",
            use_container_width=True,
            disabled=not input_valid  # 输入无效时禁用按钮
        )

    # 只有在提交时才返回数据
    if submitted and input_valid:
        return {
            'submitted': True,
            'city_name': city_name,
            'brand_name': brand_name,
            'product_category': product_category,
            'special_focus': special_focus,
            'analysis_date': current_date.strftime('%Y-%m-%d'),
            'forecast_period': 30,  # 固定30天预测周期
            'market_type': '制造业',  # 固定为制造业
            'analysts': [a[0] for a in selected_analysts],
            'research_depth': research_depth
        }
    else:
        return {'submitted': False}
