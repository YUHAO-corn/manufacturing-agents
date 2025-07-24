#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存数据提供器
专门处理库存相关数据的获取和分析
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class InventoryDataProvider:
    """
    库存数据提供器
    提供库存状态、周转率、安全库存等数据
    """
    
    def __init__(self):
        self.data_cache = {}
        
    def get_inventory_status(self, product_code: str) -> Dict[str, Any]:
        """
        获取库存状态
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 库存状态数据
        """
        warehouses = []
        for i in range(random.randint(2, 5)):
            warehouse_code = f'WH{i+1:03d}'
            current_stock = random.randint(0, 2000)
            reserved_stock = random.randint(0, int(current_stock * 0.3))
            available_stock = current_stock - reserved_stock
            
            warehouses.append({
                'warehouse_code': warehouse_code,
                'warehouse_name': f'仓库_{warehouse_code}',
                'location': f'城市_{i+1}',
                'current_stock': current_stock,
                'reserved_stock': reserved_stock,
                'available_stock': available_stock,
                'safety_stock': random.randint(50, 300),
                'reorder_point': random.randint(100, 500),
                'max_capacity': random.randint(3000, 8000),
                'utilization_rate': round(current_stock / random.randint(3000, 8000), 2),
                'last_updated': datetime.now().isoformat()
            })
        
        total_current = sum(w['current_stock'] for w in warehouses)
        total_available = sum(w['available_stock'] for w in warehouses)
        total_reserved = sum(w['reserved_stock'] for w in warehouses)
        
        return {
            'product_code': product_code,
            'warehouses': warehouses,
            'total_inventory': {
                'current_stock': total_current,
                'available_stock': total_available,
                'reserved_stock': total_reserved,
                'total_capacity': sum(w['max_capacity'] for w in warehouses),
                'overall_utilization': round(total_current / sum(w['max_capacity'] for w in warehouses), 2)
            },
            'inventory_alerts': [
                f'仓库{w["warehouse_code"]}库存不足' for w in warehouses 
                if w['available_stock'] < w['safety_stock']
            ],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_inventory_turnover(self, product_code: str, months: int = 12) -> Dict[str, Any]:
        """
        获取库存周转率分析
        
        Args:
            product_code: 产品代码
            months: 分析月数
            
        Returns:
            Dict: 库存周转率数据
        """
        monthly_data = []
        for i in range(months):
            month_date = datetime.now() - timedelta(days=30*i)
            
            beginning_inventory = random.randint(1000, 3000)
            ending_inventory = random.randint(1000, 3000)
            cost_of_goods_sold = random.randint(5000, 15000)
            
            avg_inventory = (beginning_inventory + ending_inventory) / 2
            turnover_rate = cost_of_goods_sold / avg_inventory if avg_inventory > 0 else 0
            
            monthly_data.append({
                'month': month_date.strftime('%Y-%m'),
                'beginning_inventory': beginning_inventory,
                'ending_inventory': ending_inventory,
                'average_inventory': round(avg_inventory, 2),
                'cost_of_goods_sold': cost_of_goods_sold,
                'turnover_rate': round(turnover_rate, 2),
                'days_in_inventory': round(30 / turnover_rate if turnover_rate > 0 else 0, 1)
            })
        
        # 计算年度指标
        annual_cogs = sum(d['cost_of_goods_sold'] for d in monthly_data)
        annual_avg_inventory = sum(d['average_inventory'] for d in monthly_data) / len(monthly_data)
        annual_turnover = annual_cogs / annual_avg_inventory if annual_avg_inventory > 0 else 0
        
        return {
            'product_code': product_code,
            'monthly_turnover': monthly_data,
            'annual_metrics': {
                'annual_turnover_rate': round(annual_turnover, 2),
                'average_days_in_inventory': round(365 / annual_turnover if annual_turnover > 0 else 0, 1),
                'inventory_efficiency': '高' if annual_turnover > 8 else '中' if annual_turnover > 4 else '低'
            },
            'benchmark_comparison': {
                'industry_average': round(random.uniform(4, 8), 2),
                'performance_vs_industry': '优于' if annual_turnover > 6 else '符合' if annual_turnover > 4 else '低于'
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_abc_analysis(self, product_codes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        获取ABC分析
        
        Args:
            product_codes: 产品代码列表，如果为None则分析所有产品
            
        Returns:
            Dict: ABC分析数据
        """
        if product_codes is None:
            product_codes = [f'P{i:04d}' for i in range(1, 21)]  # 默认20个产品
        
        products = []
        for code in product_codes:
            annual_usage_value = random.randint(10000, 500000)
            products.append({
                'product_code': code,
                'annual_usage_value': annual_usage_value,
                'annual_usage_quantity': random.randint(100, 5000),
                'unit_cost': round(annual_usage_value / random.randint(100, 5000), 2),
                'current_stock': random.randint(50, 1000),
                'stock_value': 0  # 将被计算
            })
        
        # 计算库存价值
        for product in products:
            product['stock_value'] = round(product['current_stock'] * product['unit_cost'], 2)
        
        # 按年度使用价值排序
        products.sort(key=lambda x: x['annual_usage_value'], reverse=True)
        
        # 计算累计百分比
        total_value = sum(p['annual_usage_value'] for p in products)
        cumulative_value = 0
        
        for i, product in enumerate(products):
            cumulative_value += product['annual_usage_value']
            cumulative_percent = cumulative_value / total_value * 100
            
            # ABC分类
            if cumulative_percent <= 80:
                abc_category = 'A'
            elif cumulative_percent <= 95:
                abc_category = 'B'
            else:
                abc_category = 'C'
            
            product.update({
                'rank': i + 1,
                'value_percentage': round(product['annual_usage_value'] / total_value * 100, 2),
                'cumulative_percentage': round(cumulative_percent, 2),
                'abc_category': abc_category
            })
        
        # 分类汇总
        categories = {'A': [], 'B': [], 'C': []}
        for product in products:
            categories[product['abc_category']].append(product)
        
        category_summary = {}
        for category, items in categories.items():
            category_summary[category] = {
                'product_count': len(items),
                'total_value': sum(p['annual_usage_value'] for p in items),
                'percentage_of_total': round(sum(p['annual_usage_value'] for p in items) / total_value * 100, 2),
                'management_strategy': {
                    'A': '严格控制，频繁监控，精确预测',
                    'B': '适度控制，定期检查，标准管理',
                    'C': '简单控制，批量订购，低成本管理'
                }[category]
            }
        
        return {
            'analysis_date': datetime.now().isoformat(),
            'products': products,
            'category_summary': category_summary,
            'recommendations': [
                'A类产品需要严格的库存控制',
                'B类产品采用标准管理程序',
                'C类产品可以采用简化管理',
                '定期重新评估产品分类'
            ],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_safety_stock_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取安全库存分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 安全库存分析数据
        """
        # 历史需求数据
        daily_demand = []
        for i in range(30):
            demand = random.randint(20, 200)
            daily_demand.append({
                'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                'demand': demand
            })
        
        # 计算需求统计
        demands = [d['demand'] for d in daily_demand]
        avg_demand = sum(demands) / len(demands)
        max_demand = max(demands)
        min_demand = min(demands)
        
        # 计算标准差
        variance = sum((d - avg_demand) ** 2 for d in demands) / len(demands)
        std_dev = variance ** 0.5
        
        # 供应商数据
        lead_times = [random.randint(5, 20) for _ in range(10)]
        avg_lead_time = sum(lead_times) / len(lead_times)
        max_lead_time = max(lead_times)
        
        # 计算安全库存
        service_levels = [0.90, 0.95, 0.98, 0.99]
        safety_stocks = []
        
        for service_level in service_levels:
            # 简化的Z分数计算
            z_scores = {0.90: 1.28, 0.95: 1.65, 0.98: 2.05, 0.99: 2.33}
            z_score = z_scores[service_level]
            
            safety_stock = z_score * std_dev * (avg_lead_time ** 0.5)
            
            safety_stocks.append({
                'service_level': service_level,
                'z_score': z_score,
                'safety_stock': round(safety_stock, 0),
                'reorder_point': round(avg_demand * avg_lead_time + safety_stock, 0),
                'carrying_cost': round(safety_stock * random.uniform(5, 15), 2),
                'stockout_risk': round((1 - service_level) * 100, 1)
            })
        
        return {
            'product_code': product_code,
            'demand_analysis': {
                'average_daily_demand': round(avg_demand, 2),
                'max_daily_demand': max_demand,
                'min_daily_demand': min_demand,
                'demand_std_dev': round(std_dev, 2),
                'demand_coefficient_of_variation': round(std_dev / avg_demand, 3),
                'demand_pattern': '稳定' if std_dev / avg_demand < 0.3 else '波动' if std_dev / avg_demand < 0.6 else '高度波动'
            },
            'lead_time_analysis': {
                'average_lead_time': round(avg_lead_time, 1),
                'max_lead_time': max_lead_time,
                'lead_time_variability': round(max_lead_time - avg_lead_time, 1)
            },
            'safety_stock_options': safety_stocks,
            'current_status': {
                'current_safety_stock': random.randint(100, 300),
                'current_service_level': round(random.uniform(0.90, 0.98), 2),
                'recommended_safety_stock': round(safety_stocks[1]['safety_stock'], 0),  # 95%服务水平
                'optimization_potential': round(random.uniform(10, 30), 1)
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_inventory_aging_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取库存老化分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 库存老化分析数据
        """
        # 生成分批次库存数据
        batches = []
        total_quantity = 0
        
        for i in range(random.randint(5, 15)):
            batch_date = datetime.now() - timedelta(days=random.randint(1, 180))
            quantity = random.randint(50, 500)
            unit_cost = round(random.uniform(10, 50), 2)
            
            age_days = (datetime.now() - batch_date).days
            
            # 根据年龄确定状态
            if age_days <= 30:
                status = '新鲜'
            elif age_days <= 90:
                status = '正常'
            elif age_days <= 180:
                status = '老化'
            else:
                status = '过期风险'
            
            batches.append({
                'batch_number': f'BATCH{i+1:03d}',
                'received_date': batch_date.strftime('%Y-%m-%d'),
                'age_days': age_days,
                'quantity': quantity,
                'unit_cost': unit_cost,
                'total_value': round(quantity * unit_cost, 2),
                'status': status,
                'turnover_priority': 'high' if age_days > 90 else 'medium' if age_days > 30 else 'low'
            })
            
            total_quantity += quantity
        
        # 按年龄排序
        batches.sort(key=lambda x: x['age_days'], reverse=True)
        
        # 年龄分析
        age_groups = {
            '0-30天': {'quantity': 0, 'value': 0.0},
            '31-90天': {'quantity': 0, 'value': 0.0},
            '91-180天': {'quantity': 0, 'value': 0.0},
            '180天以上': {'quantity': 0, 'value': 0.0}
        }
        
        for batch in batches:
            age = batch['age_days']
            if age <= 30:
                group = '0-30天'
            elif age <= 90:
                group = '31-90天'
            elif age <= 180:
                group = '91-180天'
            else:
                group = '180天以上'
            
            age_groups[group]['quantity'] += batch['quantity']
            age_groups[group]['value'] += batch['total_value']
        
        # 计算百分比
        total_value = sum(batch['total_value'] for batch in batches)
        for group in age_groups.values():
            group['quantity_pct'] = round(group['quantity'] / total_quantity * 100, 1)
            group['value_pct'] = round(group['value'] / total_value * 100, 1)
        
        return {
            'product_code': product_code,
            'analysis_date': datetime.now().isoformat(),
            'batches': batches,
            'age_distribution': age_groups,
            'summary': {
                'total_batches': len(batches),
                'total_quantity': total_quantity,
                'total_value': round(total_value, 2),
                'average_age': round(sum(b['age_days'] for b in batches) / len(batches), 1),
                'oldest_batch_age': max(b['age_days'] for b in batches),
                'aging_risk_level': '高' if age_groups['180天以上']['quantity'] > 0 else '中' if age_groups['91-180天']['quantity'] > 0 else '低'
            },
            'recommendations': [
                '优先销售老化库存',
                '调整采购策略，减少过量库存',
                '考虑促销活动处理老化产品',
                '优化库存周转率'
            ],
            'updated_at': datetime.now().isoformat()
        } 