#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供应链数据提供器
专门处理供应链相关数据的获取和分析
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class SupplyChainDataProvider:
    """
    供应链数据提供器
    提供供应商信息、交货数据、质量数据等
    """
    
    def __init__(self):
        self.data_cache = {}
        
    def get_supplier_info(self, supplier_code: str) -> Dict[str, Any]:
        """
        获取供应商信息
        
        Args:
            supplier_code: 供应商代码
            
        Returns:
            Dict: 供应商详细信息
        """
        return {
            'supplier_code': supplier_code,
            'supplier_name': f'供应商_{supplier_code}',
            'contact_person': f'联系人_{supplier_code}',
            'phone': f'138{random.randint(10000000, 99999999)}',
            'email': f'{supplier_code.lower()}@supplier.com',
            'address': f'供应商地址_{supplier_code}',
            'business_license': f'营业执照_{supplier_code}',
            'established_date': '2020-01-01',
            'annual_revenue': random.randint(1000000, 50000000),
            'employee_count': random.randint(50, 500),
            'certification': random.choice(['ISO9001', 'ISO14001', 'OHSAS18001']),
            'credit_rating': random.choice(['AAA', 'AA', 'A', 'BBB']),
            'payment_terms': random.choice(['货到付款', '月结30天', '月结60天']),
            'updated_at': datetime.now().isoformat()
        }
    
    def get_delivery_performance(self, supplier_code: str, months: int = 6) -> Dict[str, Any]:
        """
        获取供应商交货表现数据
        
        Args:
            supplier_code: 供应商代码
            months: 查询月数
            
        Returns:
            Dict: 交货表现数据
        """
        # 生成月度交货数据
        monthly_data = []
        for i in range(months):
            month_date = datetime.now() - timedelta(days=30*i)
            monthly_data.append({
                'month': month_date.strftime('%Y-%m'),
                'orders_count': random.randint(10, 50),
                'on_time_delivery_rate': round(random.uniform(0.85, 0.98), 3),
                'quality_pass_rate': round(random.uniform(0.90, 0.99), 3),
                'average_lead_time': random.randint(5, 20),
                'defect_rate': round(random.uniform(0.001, 0.05), 4)
            })
        
        # 计算整体表现
        avg_on_time = sum(d['on_time_delivery_rate'] for d in monthly_data) / len(monthly_data)
        avg_quality = sum(d['quality_pass_rate'] for d in monthly_data) / len(monthly_data)
        avg_lead_time = sum(d['average_lead_time'] for d in monthly_data) / len(monthly_data)
        
        return {
            'supplier_code': supplier_code,
            'evaluation_period': f'{months}个月',
            'monthly_performance': monthly_data,
            'overall_performance': {
                'average_on_time_delivery_rate': round(avg_on_time, 3),
                'average_quality_pass_rate': round(avg_quality, 3),
                'average_lead_time': round(avg_lead_time, 1),
                'performance_trend': random.choice(['改善', '稳定', '下降']),
                'recommendation': random.choice(['继续合作', '需要改进', '考虑更换'])
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_supply_risk_assessment(self, product_code: str) -> Dict[str, Any]:
        """
        获取供应风险评估
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 供应风险评估数据
        """
        risk_factors = [
            {
                'factor': '供应商地理集中度',
                'risk_level': random.choice(['低', '中', '高']),
                'description': '主要供应商集中在同一地区',
                'impact': random.choice(['低', '中', '高']),
                'probability': random.uniform(0.1, 0.8)
            },
            {
                'factor': '单一供应商依赖',
                'risk_level': random.choice(['低', '中', '高']),
                'description': '对单一供应商的依赖程度',
                'impact': random.choice(['低', '中', '高']),
                'probability': random.uniform(0.1, 0.8)
            },
            {
                'factor': '原材料价格波动',
                'risk_level': random.choice(['低', '中', '高']),
                'description': '原材料价格波动对供应成本的影响',
                'impact': random.choice(['低', '中', '高']),
                'probability': random.uniform(0.1, 0.8)
            },
            {
                'factor': '供应商财务状况',
                'risk_level': random.choice(['低', '中', '高']),
                'description': '供应商的财务健康状况',
                'impact': random.choice(['低', '中', '高']),
                'probability': random.uniform(0.1, 0.8)
            }
        ]
        
        # 计算整体风险等级
        risk_scores = {'低': 1, '中': 2, '高': 3}
        avg_risk_score = sum(risk_scores[factor['risk_level']] for factor in risk_factors) / len(risk_factors)
        
        if avg_risk_score <= 1.5:
            overall_risk = '低'
        elif avg_risk_score <= 2.5:
            overall_risk = '中'
        else:
            overall_risk = '高'
        
        return {
            'product_code': product_code,
            'risk_factors': risk_factors,
            'overall_risk_level': overall_risk,
            'risk_score': round(avg_risk_score, 2),
            'recommendations': [
                '建议多元化供应商',
                '定期评估供应商财务状况',
                '建立应急供应方案',
                '签订长期合同锁定价格'
            ][:random.randint(2, 4)],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_supply_capacity_analysis(self, supplier_code: str) -> Dict[str, Any]:
        """
        获取供应商产能分析
        
        Args:
            supplier_code: 供应商代码
            
        Returns:
            Dict: 供应商产能分析数据
        """
        return {
            'supplier_code': supplier_code,
            'production_capacity': {
                'daily_capacity': random.randint(1000, 10000),
                'current_utilization': round(random.uniform(0.60, 0.95), 2),
                'available_capacity': random.randint(500, 3000),
                'peak_capacity': random.randint(12000, 15000),
                'capacity_trend': random.choice(['增长', '稳定', '下降'])
            },
            'production_schedule': {
                'current_orders': random.randint(5, 20),
                'production_queue_days': random.randint(10, 30),
                'next_available_slot': (datetime.now() + timedelta(days=random.randint(5, 25))).strftime('%Y-%m-%d'),
                'rush_order_capability': random.choice(['可以', '有限', '不可以'])
            },
            'quality_metrics': {
                'defect_rate': round(random.uniform(0.001, 0.05), 4),
                'first_pass_yield': round(random.uniform(0.85, 0.98), 3),
                'quality_certifications': random.choice(['ISO9001', 'ISO14001', 'OHSAS18001']),
                'inspection_standards': '严格'
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_alternative_suppliers(self, product_code: str) -> List[Dict[str, Any]]:
        """
        获取备选供应商列表
        
        Args:
            product_code: 产品代码
            
        Returns:
            List: 备选供应商列表
        """
        alternatives = []
        for i in range(random.randint(2, 5)):
            supplier_code = f'ALT{i+1:03d}'
            alternatives.append({
                'supplier_code': supplier_code,
                'supplier_name': f'备选供应商_{supplier_code}',
                'location': f'城市_{i+1}',
                'distance_km': random.randint(50, 500),
                'unit_price': round(random.uniform(80, 120), 2),
                'lead_time': random.randint(5, 20),
                'min_order_quantity': random.randint(100, 1000),
                'quality_rating': round(random.uniform(3.0, 5.0), 1),
                'delivery_rating': round(random.uniform(3.0, 5.0), 1),
                'financial_stability': random.choice(['优秀', '良好', '一般']),
                'cooperation_history': random.choice(['有', '无']),
                'evaluation_status': random.choice(['已评估', '待评估', '评估中']),
                'recommendation_level': random.choice(['强烈推荐', '推荐', '可考虑', '不推荐'])
            })
        
        return alternatives 