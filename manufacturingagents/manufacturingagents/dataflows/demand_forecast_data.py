#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求预测数据提供器
专门处理需求预测相关数据的获取和分析
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import math
import logging

logger = logging.getLogger(__name__)

class DemandForecastDataProvider:
    """
    需求预测数据提供器
    提供需求预测、趋势分析、季节性分析等数据
    """
    
    def __init__(self):
        self.data_cache = {}
        
    def get_demand_forecast(self, product_code: str, days: int = 30) -> Dict[str, Any]:
        """
        获取需求预测数据
        
        Args:
            product_code: 产品代码
            days: 预测天数
            
        Returns:
            Dict: 需求预测数据
        """
        # 基础需求量
        base_demand = random.randint(100, 1000)
        
        forecasts = []
        for i in range(days):
            forecast_date = datetime.now() + timedelta(days=i)
            
            # 添加趋势
            trend_factor = 1 + (i * 0.01)  # 每天增长1%
            
            # 添加季节性
            seasonal_factor = 1 + 0.2 * math.sin(i * 0.1)  # 季节性波动
            
            # 添加随机波动
            random_factor = random.uniform(0.8, 1.2)
            
            demand = int(base_demand * trend_factor * seasonal_factor * random_factor)
            
            forecasts.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'forecasted_demand': demand,
                'confidence_level': round(random.uniform(0.7, 0.95), 2),
                'trend_component': round(trend_factor, 3),
                'seasonal_component': round(seasonal_factor, 3),
                'random_component': round(random_factor, 3)
            })
        
        return {
            'product_code': product_code,
            'forecast_horizon': f'{days}天',
            'forecasts': forecasts,
            'model_info': {
                'model_type': 'ARIMA+季节性分解',
                'accuracy': round(random.uniform(0.75, 0.95), 2),
                'last_updated': datetime.now().isoformat(),
                'next_update': (datetime.now() + timedelta(days=1)).isoformat()
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_demand_trend_analysis(self, product_code: str, months: int = 12) -> Dict[str, Any]:
        """
        获取需求趋势分析
        
        Args:
            product_code: 产品代码
            months: 分析月数
            
        Returns:
            Dict: 需求趋势分析数据
        """
        monthly_data = []
        base_demand = random.randint(1000, 5000)
        
        for i in range(months):
            month_date = datetime.now() - timedelta(days=30*i)
            
            # 添加趋势
            trend_factor = 1 + (i * 0.02)  # 每月增长2%
            
            # 添加季节性
            season_factor = 1 + 0.3 * math.sin(i * 0.5)
            
            demand = int(base_demand * trend_factor * season_factor)
            
            monthly_data.append({
                'month': month_date.strftime('%Y-%m'),
                'actual_demand': demand,
                'trend_value': round(trend_factor, 3),
                'seasonal_index': round(season_factor, 3),
                'growth_rate': round(random.uniform(-0.1, 0.15), 3)
            })
        
        # 计算总体趋势
        recent_3_months = sum(d['actual_demand'] for d in monthly_data[:3]) / 3
        previous_3_months = sum(d['actual_demand'] for d in monthly_data[3:6]) / 3
        trend_direction = '上升' if recent_3_months > previous_3_months else '下降'
        
        return {
            'product_code': product_code,
            'analysis_period': f'{months}个月',
            'monthly_data': monthly_data,
            'trend_analysis': {
                'overall_trend': trend_direction,
                'trend_strength': random.choice(['强', '中', '弱']),
                'seasonality_detected': random.choice([True, False]),
                'cyclical_pattern': random.choice(['年度', '季度', '无']),
                'volatility': round(random.uniform(0.1, 0.3), 2)
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_market_demand_drivers(self, product_code: str) -> Dict[str, Any]:
        """
        获取市场需求驱动因素分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 市场需求驱动因素数据
        """
        drivers = [
            {
                'factor': '经济环境',
                'impact_weight': round(random.uniform(0.15, 0.25), 2),
                'current_trend': random.choice(['正面', '负面', '中性']),
                'description': '宏观经济环境对需求的影响',
                'forecast_impact': random.choice(['增长', '稳定', '下降'])
            },
            {
                'factor': '季节性',
                'impact_weight': round(random.uniform(0.10, 0.20), 2),
                'current_trend': random.choice(['正面', '负面', '中性']),
                'description': '季节性因素对需求的影响',
                'forecast_impact': random.choice(['增长', '稳定', '下降'])
            },
            {
                'factor': '技术升级',
                'impact_weight': round(random.uniform(0.05, 0.15), 2),
                'current_trend': random.choice(['正面', '负面', '中性']),
                'description': '技术升级对产品需求的影响',
                'forecast_impact': random.choice(['增长', '稳定', '下降'])
            },
            {
                'factor': '竞争环境',
                'impact_weight': round(random.uniform(0.10, 0.20), 2),
                'current_trend': random.choice(['正面', '负面', '中性']),
                'description': '市场竞争对需求的影响',
                'forecast_impact': random.choice(['增长', '稳定', '下降'])
            },
            {
                'factor': '原材料价格',
                'impact_weight': round(random.uniform(0.05, 0.15), 2),
                'current_trend': random.choice(['正面', '负面', '中性']),
                'description': '原材料价格变化对需求的影响',
                'forecast_impact': random.choice(['增长', '稳定', '下降'])
            }
        ]
        
        return {
            'product_code': product_code,
            'demand_drivers': drivers,
            'key_insights': [
                '经济环境是主要驱动因素',
                '季节性影响较为明显',
                '技术升级带来新的需求',
                '竞争加剧影响需求'
            ][:random.randint(2, 4)],
            'recommendations': [
                '密切关注经济指标',
                '制定季节性库存策略',
                '投资技术升级',
                '加强市场竞争分析'
            ][:random.randint(2, 4)],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_demand_volatility_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取需求波动性分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 需求波动性分析数据
        """
        # 生成历史波动数据
        volatility_data = []
        for i in range(30):  # 30天的波动数据
            date = datetime.now() - timedelta(days=i)
            volatility_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'daily_volatility': round(random.uniform(0.05, 0.30), 3),
                'demand_variance': round(random.uniform(100, 1000), 2),
                'coefficient_of_variation': round(random.uniform(0.1, 0.5), 3)
            })
        
        avg_volatility = sum(d['daily_volatility'] for d in volatility_data) / len(volatility_data)
        
        # 波动性等级
        if avg_volatility <= 0.1:
            volatility_level = '低'
        elif avg_volatility <= 0.2:
            volatility_level = '中'
        else:
            volatility_level = '高'
        
        return {
            'product_code': product_code,
            'volatility_data': volatility_data,
            'volatility_metrics': {
                'average_volatility': round(avg_volatility, 3),
                'volatility_level': volatility_level,
                'max_volatility': round(max(d['daily_volatility'] for d in volatility_data), 3),
                'min_volatility': round(min(d['daily_volatility'] for d in volatility_data), 3),
                'volatility_trend': random.choice(['增加', '稳定', '减少'])
            },
            'risk_assessment': {
                'demand_predictability': random.choice(['高', '中', '低']),
                'inventory_risk': random.choice(['高', '中', '低']),
                'supply_chain_impact': random.choice(['重大', '中等', '轻微']),
                'recommended_safety_stock': random.randint(100, 500)
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_demand_scenario_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取需求情景分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 需求情景分析数据
        """
        base_demand = random.randint(500, 2000)
        
        scenarios = [
            {
                'scenario': '乐观情景',
                'probability': 0.25,
                'demand_change': '+20%',
                'forecasted_demand': int(base_demand * 1.2),
                'key_factors': ['经济增长', '市场扩张', '技术创新'],
                'impact_description': '市场需求大幅增长'
            },
            {
                'scenario': '基础情景',
                'probability': 0.50,
                'demand_change': '±5%',
                'forecasted_demand': int(base_demand * 1.0),
                'key_factors': ['正常运营', '稳定市场', '常规增长'],
                'impact_description': '需求保持稳定增长'
            },
            {
                'scenario': '悲观情景',
                'probability': 0.25,
                'demand_change': '-15%',
                'forecasted_demand': int(base_demand * 0.85),
                'key_factors': ['经济衰退', '市场萎缩', '竞争加剧'],
                'impact_description': '需求显著下降'
            }
        ]
        
        # 计算加权平均需求
        weighted_demand = sum(s['forecasted_demand'] * s['probability'] for s in scenarios)
        
        return {
            'product_code': product_code,
            'scenarios': scenarios,
            'weighted_forecast': {
                'expected_demand': int(weighted_demand),
                'confidence_interval': {
                    'lower_bound': int(weighted_demand * 0.8),
                    'upper_bound': int(weighted_demand * 1.2)
                },
                'risk_level': random.choice(['低', '中', '高'])
            },
            'recommendations': [
                '制定多情景应对策略',
                '建立灵活的供应链',
                '优化库存管理',
                '加强市场监测'
            ],
            'updated_at': datetime.now().isoformat()
        } 