#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业文案管理器
Manufacturing Text Manager

提供统一的文案管理和替换功能
"""

from typing import Dict, Any, Optional, List
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from web.i18n.manufacturing_texts import MANUFACTURING_TEXTS, ORIGINAL_TO_MANUFACTURING_MAPPING
except ImportError:
    # 如果导入失败，使用默认配置
    MANUFACTURING_TEXTS = {}
    ORIGINAL_TO_MANUFACTURING_MAPPING = {}


class ManufacturingTextManager:
    """制造业文案管理器"""
    
    def __init__(self):
        self.texts = MANUFACTURING_TEXTS
        self.mapping = ORIGINAL_TO_MANUFACTURING_MAPPING
    
    def get_text(self, key: str, default: Optional[str] = None) -> str:
        """
        获取文案
        
        Args:
            key: 文案键，支持点分隔的嵌套键如 'features.multi_agent.title'
            default: 默认值
            
        Returns:
            str: 文案内容
        """
        keys = key.split('.')
        value = self.texts
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default or key
        
        return value if isinstance(value, str) else default or key
    
    def get_dict(self, key: str, default: Optional[Dict] = None) -> Dict:
        """
        获取字典类型的文案
        
        Args:
            key: 文案键
            default: 默认值
            
        Returns:
            Dict: 文案字典
        """
        keys = key.split('.')
        value = self.texts
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default or {}
        
        return value if isinstance(value, dict) else default or {}
    
    def get_feature_text(self, feature_key: str) -> Dict[str, str]:
        """
        获取特性文案
        
        Args:
            feature_key: 特性键
            
        Returns:
            Dict: 包含title, icon, description的字典
        """
        return self.get_dict(f'features.{feature_key}')
    
    def get_navigation_text(self, nav_key: str) -> Optional[str]:
        """
        获取导航文案
        
        Args:
            nav_key: 导航键
            
        Returns:
            str: 导航文案，如果为None则表示隐藏该导航
        """
        nav_texts = self.get_dict('navigation')
        return nav_texts.get(nav_key)
    
    def get_analyst_info(self, analyst_key: str) -> Dict[str, str]:
        """
        获取分析师信息
        
        Args:
            analyst_key: 分析师键
            
        Returns:
            Dict: 分析师信息
        """
        return self.get_dict(f'analyst_team.{analyst_key}')
    
    def get_form_label(self, field_key: str) -> Dict[str, str]:
        """
        获取表单标签信息
        
        Args:
            field_key: 表单字段键
            
        Returns:
            Dict: 表单标签信息
        """
        return self.get_dict(f'form_labels.{field_key}')
    
    def get_theme_color(self, color_key: str) -> str:
        """
        获取主题色彩
        
        Args:
            color_key: 色彩键
            
        Returns:
            str: 色彩值
        """
        return self.get_text(f'theme.{color_key}', '#2E8B57')
    
    def replace_original_text(self, text: str) -> str:
        """
        替换原始文案为制造业文案
        
        Args:
            text: 原始文案
            
        Returns:
            str: 替换后的文案
        """
        for original, manufacturing in self.mapping.items():
            text = text.replace(original, manufacturing)
        return text
    
    def get_visible_navigation_items(self) -> List[str]:
        """
        获取可见的导航项
        
        Returns:
            List[str]: 可见的导航项列表
        """
        nav_texts = self.get_dict('navigation')
        return [text for text in nav_texts.values() if text is not None]
    
    def get_analyst_options(self) -> Dict[str, str]:
        """
        获取分析师选项（用于表单选择）
        
        Returns:
            Dict[str, str]: 分析师选项，键为内部代码，值为显示名称
        """
        analyst_team = self.get_dict('analyst_team')
        options = {}
        
        for key, info in analyst_team.items():
            if isinstance(info, dict) and 'name' in info and 'icon' in info:
                options[key] = f"{info['icon']} {info['name']}"
        
        return options
    
    def get_analyst_descriptions(self) -> Dict[str, str]:
        """
        获取分析师描述（用于使用指南）
        
        Returns:
            Dict[str, str]: 分析师描述
        """
        guide_desc = self.get_dict('usage_guide.analyst_team_guide.description')
        return guide_desc
    
    def format_result_title(self, product_code: str) -> str:
        """
        格式化结果标题
        
        Args:
            product_code: 产品代码
            
        Returns:
            str: 格式化的标题
        """
        icon = self.get_text('results.icon', '📊')
        title = self.get_text('results.title', '补货分析结果')
        return f"{icon} {product_code} {title}"
    
    def get_decision_action_text(self, action: str) -> str:
        """
        获取决策动作文案
        
        Args:
            action: 动作代码 (BUY/SELL/HOLD)
            
        Returns:
            str: 动作文案
        """
        actions = self.get_dict('results.decision_summary.actions')
        return actions.get(action, action)


# 全局文案管理器实例
text_manager = ManufacturingTextManager()


def get_text(key: str, default: Optional[str] = None) -> str:
    """快捷函数：获取文案"""
    return text_manager.get_text(key, default)


def get_dict(key: str, default: Optional[Dict] = None) -> Dict:
    """快捷函数：获取字典"""
    return text_manager.get_dict(key, default)


def replace_text(text: str) -> str:
    """快捷函数：替换文案"""
    return text_manager.replace_original_text(text) 