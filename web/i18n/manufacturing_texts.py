#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业界面文案配置
Manufacturing UI Text Configuration
"""

MANUFACTURING_TEXTS = {
    # 页面基本信息
    "page_title": "制造业智能补货决策系统",
    "page_subtitle": "基于多智能体大语言模型的制造业补货决策框架",
    "page_icon": "🏭",
    
    # 主要功能
    "main_function": "补货决策分析",
    "main_function_icon": "📦",
    "analysis_config": "补货分析配置",
    "analysis_target": "产品代码",
    "analysis_target_icon": "📦",
    "analysis_date": "分析日期",
    "analysis_date_icon": "📅",
    
    # 分析师团队
    "analyst_team": {
        "title": "分析师团队",
        "icon": "👥",
        "market_environment_analyst": {
            "name": "市场环境分析师",
            "icon": "🌍",
            "description": "市场环境分析，供需关系"
        },
        "trend_prediction_analyst": {
            "name": "趋势预测分析师", 
            "icon": "📈",
            "description": "需求趋势预测，市场预测"
        },
        "news_analyst": {
            "name": "新闻资讯分析师",
            "icon": "📰",
            "description": "行业新闻和政策变化的事件驱动分析"
        },
        "sentiment_insight_analyst": {
            "name": "舆情洞察分析师",
            "icon": "💭",
            "description": "社交媒体、论坛、搜索指数等舆情监控"
        }
    },
    
    # 特性展示
    "features": {
        "multi_agent": {
            "title": "多智能体协作",
            "icon": "🤖",
            "description": "专业分析师团队协同工作"
        },
        "manufacturing_optimized": {
            "title": "制造业优化",
            "icon": "🏭", 
            "description": "针对制造业场景深度优化"
        },
        "real_time_data": {
            "title": "实时数据",
            "icon": "📊",
            "description": "获取最新的制造业数据"
        },
        "professional_advice": {
            "title": "专业建议",
            "icon": "🎯",
            "description": "基于AI的补货决策建议"
        }
    },
    
    # 导航菜单
    "navigation": {
        "replenishment_analysis": "📦 补货分析",
        "config_management": "⚙️ 配置管理", 
        "cache_management": "💾 缓存管理",
        "token_statistics": "💰 Token统计",
        # 隐藏的功能
        "history_records": None,  # 隐藏历史记录
        "system_status": None     # 隐藏系统状态
    },
    
    # 使用指南
    "usage_guide": {
        "title": "使用指南",
        "icon": "ℹ️",
        "quick_start": {
            "title": "快速开始",
            "icon": "🎯",
            "steps": [
                "输入产品代码 (如 AC001, REF002, WM003)",
                "选择分析日期 (默认今天)",
                "选择分析师团队 (至少一个)",
                "设置研究深度 (1-5级)",
                "点击开始分析"
            ]
        },
        "analyst_team_guide": {
            "title": "分析师团队说明",
            "icon": "👥",
            "description": {
                "market_environment_analyst": "🌍 市场环境分析师: 宏观指标分析，环境因素监控",
                "trend_prediction_analyst": "📈 趋势预测分析师: 未来事件预测，需求趋势分析",
                "news_analyst": "📰 新闻分析师: 事件驱动分析，连锁反应识别",
                "sentiment_insight_analyst": "💬 情感洞察分析师: 社媒监控，消费者情感分析"
            }
        },
        "model_guide": {
            "title": "AI模型说明",
            "icon": "🧠",
            "description": {
                "turbo": "Turbo: 快速响应，适合快速查询",
                "plus": "Plus: 平衡性能，推荐日常使用",
                "max": "Max: 最强性能，适合深度分析"
            }
        }
    },
    
    # 系统配置
    "system_config": {
        "title": "系统配置",
        "icon": "🔧",
        "api_status": {
            "title": "API密钥状态",
            "icon": "🔑",
            "dashscope": "阿里百炼",
            "manufacturing_data": "制造业数据"
        },
        "ai_model_config": {
            "title": "AI模型配置",
            "icon": "🧠",
            "provider_label": "选择LLM提供商",
            "model_label": "选择模型"
        },
        "advanced_settings": {
            "title": "高级设置",
            "icon": "⚙️",
            "enable_memory": "启用记忆功能",
            "debug_mode": "调试模式",
            "max_tokens": "最大输出长度"
        }
    },
    
    # 结果展示
    "results": {
        "title": "补货分析结果",
        "icon": "📊",
        "decision_summary": {
            "title": "补货决策摘要",
            "icon": "🎯",
            "actions": {
                "BUY": "增加库存",
                "SELL": "减少库存",
                "HOLD": "维持现状"
            }
        },
        "analysis_info": {
            "title": "分析配置信息",
            "icon": "📋"
        },
        "detailed_report": {
            "title": "详细分析报告",
            "icon": "📋"
        }
    },
    
    # 系统信息
    "system_info": {
        "version": "1.0.0",
        "framework": "Streamlit + LangGraph",
        "ai_model": "阿里百炼通义千问",
        "data_source": "制造业数据API"
    },
    
    # 帮助资源
    "help_resources": {
        "title": "帮助资源",
        "icon": "📚",
        "links": {
            "documentation": "📖 使用文档",
            "bug_report": "🐛 问题反馈", 
            "community": "💬 讨论社区",
            "api_config": "🔧 API配置指南"
        }
    },
    
    # 错误和状态信息
    "status": {
        "api_not_configured": "API密钥配置不完整，请先配置必要的API密钥",
        "analysis_failed": "分析失败",
        "analysis_completed": "分析完成",
        "demo_mode": "演示模式",
        "demo_mode_description": "当前显示的是模拟分析数据，用于界面演示。要获取真实分析结果，请配置正确的API密钥。"
    },
    
    # 表单标签
    "form_labels": {
        "product_code": {
            "label": "产品代码",
            "placeholder": "输入产品代码，如 AC001, REF002, WM003",
            "help": "输入要分析的产品代码"
        },
        "analysis_date": {
            "label": "分析日期",
            "help": "选择分析的基准日期"
        },
        "analyst_selection": {
            "label": "选择分析师团队",
            "help": "选择参与分析的AI分析师"
        },
        "research_depth": {
            "label": "研究深度",
            "help": "设置分析的详细程度（1-5级）"
        },
        "start_analysis": "开始分析"
    },
    
    # 主题色彩
    "theme": {
        "primary_color": "#2E8B57",      # 制造业主题绿色
        "secondary_color": "#4682B4",    # 辅助蓝色
        "background_color": "#f0f8f0",   # 背景色
        "accent_color": "#FF6B35"        # 强调色
    }
}

# 原始股票系统文案映射（用于替换）
ORIGINAL_TO_MANUFACTURING_MAPPING = {
    "TradingAgents-CN 股票分析平台": "制造业智能补货决策系统",
    "股票分析": "补货分析",
    "股票代码": "产品代码",
    "投资建议": "补货建议",
    "投资决策": "补货决策",
    "市场分析师": "市场环境分析师",
    "基本面分析师": "趋势预测分析师",
    "新闻分析师": "行业资讯分析师",
    "社交媒体分析师": "消费者洞察分析师",
    "📈": "��",
    "🚀": "🏭"
} 