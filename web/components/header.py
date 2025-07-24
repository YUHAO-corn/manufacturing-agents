"""
页面头部组件
"""

import streamlit as st
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

def render_header():
    """渲染页面头部"""
    
    # 获取文案
    if text_manager:
        page_title = text_manager.get_text("page_title", "制造业智能补货决策系统")
        page_subtitle = text_manager.get_text("page_subtitle", "基于多智能体大语言模型的制造业补货决策框架")
        page_icon = text_manager.get_text("page_icon", "🏭")
    else:
        page_title = "制造业智能补货决策系统"
        page_subtitle = "基于多智能体大语言模型的制造业补货决策框架"
        page_icon = "🏭"
    
    # 主标题
    st.markdown(f"""
    <div class="main-header">
        <h1>{page_icon} {page_title}</h1>
        <p>{page_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能特性展示
    col1, col2, col3, col4 = st.columns(4)
    
    # 获取特性配置
    if text_manager:
        features = [
            text_manager.get_feature_text("multi_agent"),
            text_manager.get_feature_text("manufacturing_optimized"),
            text_manager.get_feature_text("real_time_data"),
            text_manager.get_feature_text("professional_advice")
        ]
    else:
        features = [
            {"icon": "🤖", "title": "多智能体协作", "description": "专业分析师团队协同工作"},
            {"icon": "🏭", "title": "制造业优化", "description": "针对制造业场景深度优化"},
            {"icon": "📊", "title": "实时数据", "description": "获取最新的制造业数据"},
            {"icon": "🎯", "title": "专业建议", "description": "基于AI的补货决策建议"}
        ]
    
    columns = [col1, col2, col3, col4]
    
    for i, feature in enumerate(features):
        if i < len(columns) and feature:
            with columns[i]:
                icon = feature.get("icon", "🔧")
                title = feature.get("title", "功能特性")
                description = feature.get("description", "专业功能")
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{icon} {title}</h4>
                    <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # 分隔线
    st.markdown("---")
