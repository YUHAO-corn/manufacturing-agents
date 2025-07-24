#!/usr/bin/env python3
"""
TradingAgents-CN Streamlit Web界面
基于Streamlit的股票分析Web应用程序
"""

import streamlit as st
import os
import sys
from pathlib import Path
import datetime
import time
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv(project_root / ".env", override=True)

# 导入自定义组件
from components.sidebar import render_sidebar
from components.header import render_header
from components.analysis_form import render_analysis_form
from components.results_display import render_results
from utils.api_checker import check_api_keys
from utils.analysis_runner import run_stock_analysis, run_manufacturing_analysis, validate_analysis_params, format_analysis_results
from utils.progress_tracker import StreamlitProgressDisplay, create_progress_callback
from utils.simple_progress_tracker import SimpleProgressTracker

# 导入文案管理器
from utils.text_manager import text_manager

# 设置页面配置
st.set_page_config(
    page_title=text_manager.get_text("page_title", "制造业智能补货决策系统"),
    page_icon=text_manager.get_text("page_icon", "🏭"),
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/TauricResearch/TradingAgents',
        'Report a bug': 'https://github.com/TauricResearch/TradingAgents/issues',
        'About': f"""
        # {text_manager.get_text("page_title", "制造业智能补货决策系统")}
        
        {text_manager.get_text("page_subtitle", "基于多智能体大语言模型的制造业补货决策框架")}
        
        **主要特性:**
        - 🤖 多智能体协作分析
        - 🏭 制造业场景优化
        - 📊 实时制造业数据分析
        - 🎯 专业补货决策建议
        
        **版本:** {text_manager.get_text("system_info.version", "1.0.0")}
        **开发团队:** Manufacturing AI Team
        """
    }
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 隐藏Streamlit顶部工具栏和Deploy按钮 - 多种选择器确保兼容性 */
    .stAppToolbar {
        display: none !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    /* 新版本Streamlit的Deploy按钮选择器 */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* 隐藏整个顶部区域 */
    .stApp > header {
        display: none !important;
    }
    
    .stApp > div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* 隐藏主菜单按钮 */
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 隐藏页脚 */
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 隐藏"Made with Streamlit"标识 */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    /* 隐藏所有可能的工具栏元素 */
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* 隐藏右上角的所有按钮 */
    .stApp > div > div > div > div > section > div {
        padding-top: 0 !important;
    }
    
    /* 应用样式 - 制造业主题 */
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #4682B4);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin: 0.5rem 0;
    }
    
    .analysis-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """初始化会话状态"""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analysis_running' not in st.session_state:
        st.session_state.analysis_running = False
    if 'last_analysis_time' not in st.session_state:
        st.session_state.last_analysis_time = None

def main():
    """主应用程序"""

    # 初始化会话状态
    initialize_session_state()

    # 渲染页面头部
    render_header()

    # 页面导航
    st.sidebar.title(f"{text_manager.get_text('page_icon', '🏭')} 制造业AI系统")
    st.sidebar.markdown("---")

    # 获取可见的导航项
    navigation_options = []
    nav_mapping = {}
    
    # 主要功能
    replenishment_nav = text_manager.get_navigation_text("replenishment_analysis")
    if replenishment_nav:
        navigation_options.append(replenishment_nav)
        nav_mapping[replenishment_nav] = "replenishment_analysis"
    
    # 配置管理
    config_nav = text_manager.get_navigation_text("config_management")
    if config_nav:
        navigation_options.append(config_nav)
        nav_mapping[config_nav] = "config_management"
    
    # 缓存管理
    cache_nav = text_manager.get_navigation_text("cache_management")
    if cache_nav:
        navigation_options.append(cache_nav)
        nav_mapping[cache_nav] = "cache_management"
    
    # Token统计
    token_nav = text_manager.get_navigation_text("token_statistics")
    if token_nav:
        navigation_options.append(token_nav)
        nav_mapping[token_nav] = "token_statistics"
    
    # 历史记录和系统状态被隐藏（在配置中设为None）

    page = st.sidebar.selectbox(
        "选择功能",
        navigation_options
    )

    # 根据选择的页面渲染不同内容
    page_key = nav_mapping.get(page, "replenishment_analysis")
    
    if page_key == "config_management":
        try:
            from pages.config_management import render_config_management
            render_config_management()
        except ImportError as e:
            st.error(f"配置管理模块加载失败: {e}")
            st.info("请确保已安装所有依赖包")
        return
    elif page_key == "cache_management":
        try:
            from pages.cache_management import main as cache_main
            cache_main()
        except ImportError as e:
            st.error(f"缓存管理页面加载失败: {e}")
        return
    elif page_key == "token_statistics":
        try:
            from pages.token_statistics import render_token_statistics
            render_token_statistics()
        except ImportError as e:
            st.error(f"Token统计页面加载失败: {e}")
            st.info("请确保已安装所有依赖包")
        return
    
    # 历史记录和系统状态功能已被隐藏

    # 默认显示补货分析页面
    # 🏭 制造业分析专用API检查
    api_status = check_api_keys(analysis_type="manufacturing")
    
    if not api_status['all_configured']:
        st.error(f"⚠️ {text_manager.get_text('status.api_not_configured', '制造业分析API密钥配置不完整，请先配置必要的API密钥')}")
        
        with st.expander("📋 制造业分析API密钥配置指南", expanded=True):
            st.markdown("""
            ### 🔑 制造业分析必需的API密钥
            
            1. **阿里百炼API密钥** (DASHSCOPE_API_KEY)
               - 获取地址: https://dashscope.aliyun.com/
               - 用途: AI智能体分析
               - 状态: 🆓 有免费额度
            
            2. **TuShare API密钥** (TUSHARE_TOKEN)  
               - 获取地址: https://tushare.pro/
               - 用途: PMI/PPI/期货等经济数据
               - 状态: 🆓 注册即可使用
            
            3. **Coze API密钥** (COZE_API_KEY)
               - 获取地址: https://www.coze.cn/
               - 用途: 天气/新闻/节假日数据
               - 状态: 🆓 字节跳动免费服务
            
            ### ⚙️ 配置方法
            
            1. 复制项目根目录的 `.env.example` 为 `.env`
            2. 编辑 `.env` 文件，填入您的真实API密钥
            3. 重启Web应用
            
            ```bash
            # .env 文件示例（制造业分析）
            DASHSCOPE_API_KEY=sk-your-dashscope-key
            TUSHARE_TOKEN=your-tushare-token
            COZE_API_KEY=your-coze-key
            
            # 以下为可选（制造业分析不需要）
            # FINNHUB_API_KEY=your-finnhub-key
            ```
            
            ### 💡 特别说明
            - **FINNHUB_API_KEY 不是必需的**：制造业分析不依赖美股数据
            - **所有API都有免费额度**：无需付费即可体验完整功能
            """)
        
        # 显示当前API密钥状态
        st.subheader("🔍 当前API密钥状态")
        for key, status in api_status['details'].items():
            if status['required']:
                if status['configured']:
                    st.success(f"✅ {key}: {status['display']} - {status['description']}")
                else:
                    st.error(f"❌ {key}: 未配置 - {status['description']}")
            else:
                if status['configured']:
                    st.info(f"ℹ️ {key}: {status['display']} - {status['description']}")
                else:
                    st.info(f"ℹ️ {key}: 未配置 - {status['description']}")
        
        return
    
    # 渲染侧边栏
    config = render_sidebar()
    
    # 主内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"{text_manager.get_text('main_function_icon', '📦')} {text_manager.get_text('main_function', '补货决策分析')}")
        
        # 渲染分析表单
        form_data = render_analysis_form()

        # 检查是否提交了表单
        if form_data.get('submitted', False):
            # 检查制造业分析的必要参数
            if form_data.get('market_type') == '制造业':
                if not form_data.get('brand_name'):
                    st.error("请输入品牌名称")
                elif not form_data.get('product_category'):
                    st.error("请选择产品大类")
                elif not form_data['analysts']:
                    st.error("请至少选择一个分析师")
                else:
                    # 执行制造业分析
                    st.session_state.analysis_running = True

                    # 🎯 新增：进度展示区域
                    st.markdown("---")
                    st.subheader("🎯 分析进度")
                    
                    # 总进度条区域 - 使用唯一容器避免重复
                    progress_container_key = f"progress_container_{hash(str(form_data))}"
                    progress_header_container = st.container()
                    with progress_header_container:
                        progress_bar = st.progress(0)  # progress组件不支持key参数
                        current_status = st.empty()
                    
                    # 过程日志区域
                    st.subheader("📋 分析过程")
                    log_container = st.container()
                    with log_container:
                        process_log = st.empty()
                    
                    # 创建正式的进度追踪器
                    progress_callback = SimpleProgressTracker(progress_bar, current_status, process_log)
                    
                    # 初始化进度
                    progress_callback.log_event("start", "🏭 制造业补货分析启动")
                    progress_callback.update_progress(0)

                    try:
                        # 自动计算目标季度（基于当前日期的短期预测）
                        current_date = datetime.datetime.now()
                        current_quarter = f"{current_date.year}Q{(current_date.month-1)//3 + 1}"
                        
                        results = run_manufacturing_analysis(
                            city_name=form_data['city_name'],  # 🎯 修复：传递用户输入的城市
                            brand_name=form_data['brand_name'],
                            product_category=form_data['product_category'],
                            target_quarter=current_quarter,
                            special_focus=form_data.get('special_focus', ''),
                            analysts=form_data['analysts'],
                            research_depth=form_data['research_depth'],
                            llm_provider=config['llm_provider'],
                            llm_model=config['llm_model'],
                            progress_callback=progress_callback
                        )

                        # 记录分析完成
                        progress_callback.log_analysis_complete()

                        # 格式化结果
                        formatted_results = format_analysis_results(results)

                        st.session_state.analysis_results = formatted_results
                        st.session_state.last_analysis_time = datetime.datetime.now()
                        st.success("✅ 制造业补货策略分析完成！")

                    except Exception as e:
                        # 记录错误
                        progress_callback.log_error(str(e))

                        st.error(f"❌ 分析失败: {str(e)}")
                        st.markdown("""
                        **可能的解决方案:**
                        1. 检查API密钥是否正确配置
                        2. 确认网络连接正常
                        3. 尝试减少研究深度或更换模型
                        """)
                    finally:
                        st.session_state.analysis_running = False
            else:
                # 原有股票分析逻辑（兼容性）
                if not form_data.get('stock_symbol'):
                    st.error("请输入股票代码")
                elif not form_data['analysts']:
                    st.error("请至少选择一个分析师")
                else:
                    # 执行分析
                    st.session_state.analysis_running = True

                    # 创建进度显示
                    progress_container = st.container()
                    progress_display = StreamlitProgressDisplay(progress_container)
                    progress_callback = create_progress_callback(progress_display)

                    try:
                        results = run_stock_analysis(
                            stock_symbol=form_data['stock_symbol'],
                            analysis_date=form_data.get('analysis_date'),
                            analysts=form_data['analysts'],
                            research_depth=form_data['research_depth'],
                            llm_provider=config['llm_provider'],
                            market_type='美股',  # 兼容模式固定为美股
                            llm_model=config['llm_model'],
                            progress_callback=progress_callback
                        )

                        # 清除进度显示
                        progress_display.clear()

                        # 格式化结果
                        formatted_results = format_analysis_results(results)

                        st.session_state.analysis_results = formatted_results
                        st.session_state.last_analysis_time = datetime.datetime.now()
                        st.success("✅ 分析完成！")

                    except Exception as e:
                        # 清除进度显示
                        progress_display.clear()

                        st.error(f"❌ 分析失败: {str(e)}")
                        st.markdown("""
                        **可能的解决方案:**
                        1. 检查API密钥是否正确配置
                        2. 确认网络连接正常
                        3. 验证股票代码是否有效
                        4. 尝试减少研究深度或更换模型
                        """)
                    finally:
                        st.session_state.analysis_running = False
        
        # 显示分析结果
        if st.session_state.analysis_results:
            render_results(st.session_state.analysis_results)
    
    with col2:
        st.header(f"{text_manager.get_text('usage_guide.icon', 'ℹ️')} {text_manager.get_text('usage_guide.title', '使用指南')}")
        
        # 快速开始指南
        quick_start = text_manager.get_dict('usage_guide.quick_start')
        with st.expander(f"{quick_start.get('icon', '🎯')} {quick_start.get('title', '快速开始')}", expanded=True):
            steps = quick_start.get('steps', [])
            if steps:
                steps_text = "\n".join([f"{i+1}. **{step}**" for i, step in enumerate(steps)])
                st.markdown(steps_text)
            else:
                st.markdown("""
                1. **输入产品代码** (如 AC001, REF002, WM003)
                2. **选择分析日期** (默认今天)
                3. **选择分析师团队** (至少一个)
                4. **设置研究深度** (1-5级)
                5. **点击开始分析**
                """)
        
        # 分析师说明
        analyst_guide = text_manager.get_dict('usage_guide.analyst_team_guide')
        with st.expander(f"{analyst_guide.get('icon', '👥')} {analyst_guide.get('title', '分析师团队说明')}"):
            descriptions = analyst_guide.get('description', {})
            if descriptions:
                desc_text = "\n".join([f"- **{desc}**" for desc in descriptions.values()])
                st.markdown(desc_text)
            else:
                st.markdown("""
                - **🌍 市场环境分析师**: 市场环境分析，供需关系
                - **📈 趋势预测分析师**: 需求趋势预测，市场预测
                - **📰 行业资讯分析师**: 行业新闻分析，政策影响
                - **👥 消费者洞察分析师**: 消费者行为分析，市场洞察
                """)
        
        # 模型选择说明
        model_guide = text_manager.get_dict('usage_guide.model_guide')
        with st.expander(f"{model_guide.get('icon', '🧠')} {model_guide.get('title', 'AI模型说明')}"):
            model_descriptions = model_guide.get('description', {})
            if model_descriptions:
                model_text = "\n".join([f"- **{desc}**" for desc in model_descriptions.values()])
                st.markdown(model_text)
            else:
                st.markdown("""
                - **Turbo**: 快速响应，适合快速查询
                - **Plus**: 平衡性能，推荐日常使用  
                - **Max**: 最强性能，适合深度分析
                """)
        
        # 风险提示
        st.warning("""
        ⚠️ **投资风险提示**
        
        - 分析结果仅供参考，不构成投资建议
        - 投资有风险，入市需谨慎
        - 请结合多方信息进行决策
        - 重大投资建议咨询专业顾问
        """)
        
        # 显示系统状态
        if st.session_state.last_analysis_time:
            st.info(f"🕒 上次分析时间: {st.session_state.last_analysis_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
