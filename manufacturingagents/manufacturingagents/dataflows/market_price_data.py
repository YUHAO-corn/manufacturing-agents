#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场价格数据提供器
专门处理市场价格相关数据的获取和分析
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import math
import logging

logger = logging.getLogger(__name__)

class MarketPriceDataProvider:
    """
    市场价格数据提供器
    提供市场价格、价格趋势、价格波动等数据
    """
    
    def __init__(self):
        self.data_cache = {}
        
    def get_price_history(self, product_code: str, days: int = 30) -> Dict[str, Any]:
        """
        获取价格历史数据
        
        Args:
            product_code: 产品代码
            days: 查询天数
            
        Returns:
            Dict: 价格历史数据
        """
        base_price = random.uniform(50, 200)
        price_history = []
        current_price = base_price
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            
            # 价格波动
            price_change = random.uniform(-0.05, 0.05)  # ±5%波动
            current_price *= (1 + price_change)
            
            # 确保价格不会过度偏离基准
            current_price = max(current_price, base_price * 0.7)
            current_price = min(current_price, base_price * 1.3)
            
            price_history.append({
                'date': date.strftime('%Y-%m-%d'),
                'market_price': round(current_price, 2),
                'supplier_price': round(current_price * 0.85, 2),
                'retail_price': round(current_price * 1.15, 2),
                'volume': random.randint(1000, 10000),
                'price_change': round(price_change, 4),
                'volatility': round(abs(price_change), 4)
            })
        
        return {
            'product_code': product_code,
            'price_history': price_history,
            'period': f'{days}天',
            'current_price': round(current_price, 2),
            'price_range': {
                'min_price': round(min(p['market_price'] for p in price_history), 2),
                'max_price': round(max(p['market_price'] for p in price_history), 2),
                'avg_price': round(sum(p['market_price'] for p in price_history) / len(price_history), 2)
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_price_trend_analysis(self, product_code: str, months: int = 12) -> Dict[str, Any]:
        """
        获取价格趋势分析
        
        Args:
            product_code: 产品代码
            months: 分析月数
            
        Returns:
            Dict: 价格趋势分析数据
        """
        base_price = random.uniform(80, 150)
        monthly_prices = []
        
        for i in range(months):
            month_date = datetime.now() - timedelta(days=30*i)
            
            # 添加长期趋势
            trend_factor = 1 + (i * 0.01)  # 每月增长1%
            
            # 添加季节性
            seasonal_factor = 1 + 0.1 * math.sin(i * 0.5)
            
            # 添加随机波动
            random_factor = random.uniform(0.9, 1.1)
            
            price = base_price * trend_factor * seasonal_factor * random_factor
            
            monthly_prices.append({
                'month': month_date.strftime('%Y-%m'),
                'average_price': round(price, 2),
                'trend_component': round(trend_factor, 3),
                'seasonal_component': round(seasonal_factor, 3),
                'volatility': round(abs(random_factor - 1), 3),
                'price_change_pct': round(random.uniform(-0.1, 0.1), 3)
            })
        
        # 计算趋势方向
        recent_avg = sum(p['average_price'] for p in monthly_prices[:3]) / 3
        past_avg = sum(p['average_price'] for p in monthly_prices[-3:]) / 3
        trend_direction = '上升' if recent_avg > past_avg else '下降'
        
        return {
            'product_code': product_code,
            'monthly_prices': monthly_prices,
            'trend_analysis': {
                'trend_direction': trend_direction,
                'trend_strength': random.choice(['强', '中', '弱']),
                'seasonality_impact': random.choice(['高', '中', '低']),
                'volatility_level': random.choice(['高', '中', '低']),
                'price_momentum': random.choice(['加速', '稳定', '减速'])
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_price_comparison(self, product_code: str) -> Dict[str, Any]:
        """
        获取价格比较分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 价格比较分析数据
        """
        base_price = random.uniform(90, 120)
        
        competitors = []
        for i in range(random.randint(3, 6)):
            competitor_price = base_price * random.uniform(0.8, 1.2)
            competitors.append({
                'competitor': f'竞争对手_{i+1}',
                'price': round(competitor_price, 2),
                'price_difference': round(competitor_price - base_price, 2),
                'price_difference_pct': round((competitor_price - base_price) / base_price * 100, 1),
                'market_share': round(random.uniform(0.05, 0.25), 2),
                'quality_rating': round(random.uniform(3.0, 5.0), 1),
                'competitive_advantage': random.choice(['价格', '质量', '服务', '品牌'])
            })
        
        # 计算市场位置
        all_prices = [base_price] + [c['price'] for c in competitors]
        price_rank = sorted(all_prices).index(base_price) + 1
        
        return {
            'product_code': product_code,
            'our_price': round(base_price, 2),
            'competitors': competitors,
            'market_position': {
                'price_rank': price_rank,
                'total_competitors': len(competitors) + 1,
                'price_percentile': round(price_rank / (len(competitors) + 1) * 100, 1),
                'competitive_status': '高' if price_rank <= 2 else '中' if price_rank <= 4 else '低'
            },
            'price_insights': [
                f'我们的价格排名第{price_rank}',
                f'价格优势：{"较强" if price_rank <= 2 else "一般"}',
                f'平均价格差异：{round(base_price - sum(c["price"] for c in competitors) / len(competitors), 2)}元'
            ],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_price_elasticity_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取价格弹性分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 价格弹性分析数据
        """
        base_price = random.uniform(100, 150)
        base_demand = random.randint(1000, 5000)
        
        # 模拟不同价格点的需求
        price_points = []
        for i in range(-5, 6):  # -50% to +50% price range
            price_change = i * 0.1
            new_price = base_price * (1 + price_change)
            
            # 价格弹性 - 价格上涨需求下降
            elasticity = -1.2  # 假设需求价格弹性为-1.2
            demand_change = elasticity * price_change
            new_demand = base_demand * (1 + demand_change)
            
            price_points.append({
                'price': round(new_price, 2),
                'price_change_pct': round(price_change * 100, 1),
                'demand': int(max(new_demand, 0)),
                'demand_change_pct': round(demand_change * 100, 1),
                'revenue': round(new_price * new_demand, 2),
                'elasticity': round(demand_change / price_change if price_change != 0 else 0, 2)
            })
        
        # 找到最优价格点
        optimal_point = max(price_points, key=lambda x: x['revenue'])
        
        return {
            'product_code': product_code,
            'price_elasticity_curve': price_points,
            'elasticity_metrics': {
                'price_elasticity': -1.2,
                'elasticity_type': '弹性' if abs(-1.2) > 1 else '非弹性',
                'optimal_price': optimal_point['price'],
                'optimal_demand': optimal_point['demand'],
                'max_revenue': optimal_point['revenue'],
                'current_position': '当前价格处于' + random.choice(['最优区间', '偏高', '偏低'])
            },
            'pricing_recommendations': [
                f'建议价格：{optimal_point["price"]}元',
                f'预期需求：{optimal_point["demand"]}单位',
                f'预期收入：{optimal_point["revenue"]}元',
                '考虑价格弹性进行动态定价'
            ],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_price_forecast(self, product_code: str, days: int = 30) -> Dict[str, Any]:
        """
        获取价格预测
        
        Args:
            product_code: 产品代码
            days: 预测天数
            
        Returns:
            Dict: 价格预测数据
        """
        current_price = random.uniform(80, 120)
        
        forecasts = []
        for i in range(days):
            forecast_date = datetime.now() + timedelta(days=i)
            
            # 添加趋势
            trend_factor = 1 + (i * 0.001)  # 每天增长0.1%
            
            # 添加季节性
            seasonal_factor = 1 + 0.05 * math.sin(i * 0.2)
            
            # 添加随机波动
            random_factor = random.uniform(0.98, 1.02)
            
            forecasted_price = current_price * trend_factor * seasonal_factor * random_factor
            
            forecasts.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'forecasted_price': round(forecasted_price, 2),
                'confidence_level': round(random.uniform(0.7, 0.9), 2),
                'price_range': {
                    'lower_bound': round(forecasted_price * 0.95, 2),
                    'upper_bound': round(forecasted_price * 1.05, 2)
                },
                'trend_component': round(trend_factor, 4),
                'seasonal_component': round(seasonal_factor, 4)
            })
        
        return {
            'product_code': product_code,
            'price_forecasts': forecasts,
            'forecast_summary': {
                'current_price': round(current_price, 2),
                'avg_forecasted_price': round(sum(f['forecasted_price'] for f in forecasts) / len(forecasts), 2),
                'price_trend': random.choice(['上升', '稳定', '下降']),
                'volatility_forecast': random.choice(['高', '中', '低']),
                'confidence_level': round(random.uniform(0.7, 0.9), 2)
            },
            'key_factors': [
                '供需关系变化',
                '原材料价格波动',
                '市场竞争态势',
                '季节性因素',
                '政策环境变化'
            ][:random.randint(3, 5)],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_cost_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取成本分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 成本分析数据
        """
        # 成本构成
        material_cost = random.uniform(40, 80)
        labor_cost = random.uniform(10, 30)
        overhead_cost = random.uniform(5, 15)
        total_cost = material_cost + labor_cost + overhead_cost
        
        return {
            'product_code': product_code,
            'cost_breakdown': {
                'material_cost': round(material_cost, 2),
                'labor_cost': round(labor_cost, 2),
                'overhead_cost': round(overhead_cost, 2),
                'total_cost': round(total_cost, 2)
            },
            'cost_structure': {
                'material_cost_pct': round(material_cost / total_cost * 100, 1),
                'labor_cost_pct': round(labor_cost / total_cost * 100, 1),
                'overhead_cost_pct': round(overhead_cost / total_cost * 100, 1)
            },
            'margin_analysis': {
                'current_selling_price': round(total_cost * 1.3, 2),  # 30%毛利率
                'gross_margin': round(total_cost * 0.3, 2),
                'gross_margin_pct': 30.0,
                'break_even_price': round(total_cost, 2),
                'target_margin_pct': 35.0,
                'target_selling_price': round(total_cost * 1.35, 2)
            },
            'cost_trends': {
                'material_cost_trend': random.choice(['上升', '稳定', '下降']),
                'labor_cost_trend': random.choice(['上升', '稳定', '下降']),
                'overall_cost_trend': random.choice(['上升', '稳定', '下降'])
            },
            'updated_at': datetime.now().isoformat()
        } 