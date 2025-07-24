#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产数据提供器
专门处理生产相关数据的获取和分析
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class ProductionDataProvider:
    """
    生产数据提供器
    提供生产计划、产能分析、生产效率等数据
    """
    
    def __init__(self):
        self.data_cache = {}
        
    def get_production_schedule(self, product_code: str, days: int = 30) -> Dict[str, Any]:
        """
        获取生产计划
        
        Args:
            product_code: 产品代码
            days: 查询天数
            
        Returns:
            Dict: 生产计划数据
        """
        schedules = []
        for i in range(days):
            schedule_date = datetime.now() + timedelta(days=i)
            
            # 模拟生产计划
            planned_quantity = random.randint(100, 1000)
            actual_quantity = random.randint(int(planned_quantity * 0.8), int(planned_quantity * 1.1))
            
            schedules.append({
                'date': schedule_date.strftime('%Y-%m-%d'),
                'planned_quantity': planned_quantity,
                'actual_quantity': actual_quantity if i <= 0 else None,  # 过去的日期有实际数据
                'completion_rate': round(actual_quantity / planned_quantity * 100, 1) if i <= 0 else None,
                'shift': random.choice(['白班', '夜班', '全天']),
                'production_line': f'生产线{random.randint(1, 5)}',
                'status': random.choice(['正常', '延期', '提前', '暂停']) if i <= 0 else '计划中'
            })
        
        return {
            'product_code': product_code,
            'schedule_period': f'{days}天',
            'schedules': schedules,
            'summary': {
                'total_planned': sum(s['planned_quantity'] for s in schedules),
                'total_actual': sum(s['actual_quantity'] for s in schedules if s['actual_quantity'] is not None),
                'average_completion_rate': round(sum(s['completion_rate'] for s in schedules if s['completion_rate'] is not None) / len([s for s in schedules if s['completion_rate'] is not None]), 1) if any(s['completion_rate'] is not None for s in schedules) else None,
                'on_time_deliveries': len([s for s in schedules if s['status'] == '正常']),
                'delays': len([s for s in schedules if s['status'] == '延期'])
            },
            'updated_at': datetime.now().isoformat()
        }
    
    def get_production_capacity(self, product_code: str) -> Dict[str, Any]:
        """
        获取生产产能分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 生产产能数据
        """
        production_lines = []
        for i in range(random.randint(3, 6)):
            line_code = f'LINE{i+1:02d}'
            theoretical_capacity = random.randint(1000, 3000)
            actual_capacity = random.randint(int(theoretical_capacity * 0.7), int(theoretical_capacity * 0.95))
            
            production_lines.append({
                'line_code': line_code,
                'line_name': f'生产线{i+1}',
                'theoretical_capacity': theoretical_capacity,
                'actual_capacity': actual_capacity,
                'utilization_rate': round(actual_capacity / theoretical_capacity * 100, 1),
                'efficiency_rating': round(random.uniform(0.7, 0.95), 2),
                'downtime_hours': random.randint(0, 8),
                'maintenance_status': random.choice(['正常', '维护中', '故障', '待修']),
                'operator_count': random.randint(5, 20),
                'shift_pattern': random.choice(['单班', '双班', '三班'])
            })
        
        total_theoretical = sum(line['theoretical_capacity'] for line in production_lines)
        total_actual = sum(line['actual_capacity'] for line in production_lines)
        
        return {
            'product_code': product_code,
            'production_lines': production_lines,
            'capacity_summary': {
                'total_theoretical_capacity': total_theoretical,
                'total_actual_capacity': total_actual,
                'overall_utilization': round(total_actual / total_theoretical * 100, 1),
                'available_capacity': total_theoretical - total_actual,
                'capacity_constraint': '高' if total_actual / total_theoretical > 0.9 else '中' if total_actual / total_theoretical > 0.7 else '低'
            },
            'recommendations': [
                '优化生产线配置',
                '减少设备停机时间',
                '提高操作员技能',
                '实施预防性维护'
            ][:random.randint(2, 4)],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_production_efficiency(self, product_code: str, months: int = 6) -> Dict[str, Any]:
        """
        获取生产效率分析
        
        Args:
            product_code: 产品代码
            months: 分析月数
            
        Returns:
            Dict: 生产效率数据
        """
        monthly_data = []
        for i in range(months):
            month_date = datetime.now() - timedelta(days=30*i)
            
            planned_output = random.randint(10000, 30000)
            actual_output = random.randint(int(planned_output * 0.8), int(planned_output * 1.05))
            
            monthly_data.append({
                'month': month_date.strftime('%Y-%m'),
                'planned_output': planned_output,
                'actual_output': actual_output,
                'efficiency_rate': round(actual_output / planned_output * 100, 1),
                'defect_rate': round(random.uniform(0.01, 0.05), 3),
                'rework_rate': round(random.uniform(0.02, 0.08), 3),
                'on_time_delivery_rate': round(random.uniform(0.85, 0.98), 2),
                'labor_productivity': round(actual_output / random.randint(50, 150), 2),
                'equipment_utilization': round(random.uniform(0.70, 0.95), 2)
            })
        
        # 计算平均值
        avg_efficiency = sum(d['efficiency_rate'] for d in monthly_data) / len(monthly_data)
        avg_defect_rate = sum(d['defect_rate'] for d in monthly_data) / len(monthly_data)
        avg_on_time = sum(d['on_time_delivery_rate'] for d in monthly_data) / len(monthly_data)
        
        return {
            'product_code': product_code,
            'monthly_efficiency': monthly_data,
            'efficiency_metrics': {
                'average_efficiency_rate': round(avg_efficiency, 1),
                'average_defect_rate': round(avg_defect_rate, 3),
                'average_on_time_delivery': round(avg_on_time, 2),
                'efficiency_trend': random.choice(['改善', '稳定', '下降']),
                'quality_trend': random.choice(['改善', '稳定', '下降'])
            },
            'performance_rating': '优秀' if avg_efficiency > 95 else '良好' if avg_efficiency > 85 else '一般',
            'improvement_areas': [
                '减少设备停机时间',
                '提高产品质量',
                '优化生产流程',
                '加强员工培训'
            ][:random.randint(2, 4)],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_production_cost_analysis(self, product_code: str) -> Dict[str, Any]:
        """
        获取生产成本分析
        
        Args:
            product_code: 产品代码
            
        Returns:
            Dict: 生产成本分析数据
        """
        # 成本构成
        material_cost = random.uniform(40, 80)
        labor_cost = random.uniform(15, 35)
        overhead_cost = random.uniform(8, 20)
        equipment_cost = random.uniform(5, 15)
        
        total_cost = material_cost + labor_cost + overhead_cost + equipment_cost
        
        # 成本趋势
        cost_trends = []
        for i in range(6):
            month = datetime.now() - timedelta(days=30*i)
            trend_factor = random.uniform(0.95, 1.05)
            
            cost_trends.append({
                'month': month.strftime('%Y-%m'),
                'material_cost': round(material_cost * trend_factor, 2),
                'labor_cost': round(labor_cost * trend_factor, 2),
                'overhead_cost': round(overhead_cost * trend_factor, 2),
                'equipment_cost': round(equipment_cost * trend_factor, 2),
                'total_cost': round(total_cost * trend_factor, 2),
                'cost_per_unit': round(total_cost * trend_factor / random.randint(100, 1000), 2)
            })
        
        return {
            'product_code': product_code,
            'current_cost_structure': {
                'material_cost': round(material_cost, 2),
                'labor_cost': round(labor_cost, 2),
                'overhead_cost': round(overhead_cost, 2),
                'equipment_cost': round(equipment_cost, 2),
                'total_cost': round(total_cost, 2)
            },
            'cost_percentages': {
                'material_cost_pct': round(material_cost / total_cost * 100, 1),
                'labor_cost_pct': round(labor_cost / total_cost * 100, 1),
                'overhead_cost_pct': round(overhead_cost / total_cost * 100, 1),
                'equipment_cost_pct': round(equipment_cost / total_cost * 100, 1)
            },
            'cost_trends': cost_trends,
            'cost_optimization': {
                'material_savings_potential': round(random.uniform(5, 15), 1),
                'labor_efficiency_improvement': round(random.uniform(8, 20), 1),
                'overhead_reduction_potential': round(random.uniform(3, 10), 1),
                'total_savings_potential': round(random.uniform(15, 45), 1)
            },
            'recommendations': [
                '优化原材料采购',
                '提高生产效率',
                '减少浪费',
                '自动化改造'
            ],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_quality_metrics(self, product_code: str, days: int = 30) -> Dict[str, Any]:
        """
        获取质量指标
        
        Args:
            product_code: 产品代码
            days: 查询天数
            
        Returns:
            Dict: 质量指标数据
        """
        daily_quality = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            
            daily_quality.append({
                'date': date.strftime('%Y-%m-%d'),
                'produced_quantity': random.randint(500, 2000),
                'defect_quantity': random.randint(5, 100),
                'defect_rate': round(random.uniform(0.01, 0.05), 3),
                'first_pass_yield': round(random.uniform(0.85, 0.98), 3),
                'rework_quantity': random.randint(10, 150),
                'rework_rate': round(random.uniform(0.02, 0.08), 3),
                'customer_returns': random.randint(0, 20),
                'quality_score': round(random.uniform(7.5, 9.5), 1)
            })
        
        # 计算统计指标
        total_produced = sum(d['produced_quantity'] for d in daily_quality)
        total_defects = sum(d['defect_quantity'] for d in daily_quality)
        total_rework = sum(d['rework_quantity'] for d in daily_quality)
        
        avg_defect_rate = total_defects / total_produced if total_produced > 0 else 0
        avg_first_pass_yield = sum(d['first_pass_yield'] for d in daily_quality) / len(daily_quality)
        avg_quality_score = sum(d['quality_score'] for d in daily_quality) / len(daily_quality)
        
        return {
            'product_code': product_code,
            'analysis_period': f'{days}天',
            'daily_quality': daily_quality,
            'quality_summary': {
                'total_produced': total_produced,
                'total_defects': total_defects,
                'total_rework': total_rework,
                'average_defect_rate': round(avg_defect_rate, 4),
                'average_first_pass_yield': round(avg_first_pass_yield, 3),
                'average_quality_score': round(avg_quality_score, 1),
                'quality_trend': random.choice(['改善', '稳定', '下降'])
            },
            'quality_targets': {
                'target_defect_rate': 0.02,
                'target_first_pass_yield': 0.95,
                'target_quality_score': 9.0,
                'defect_rate_status': '达标' if avg_defect_rate <= 0.02 else '未达标',
                'first_pass_yield_status': '达标' if avg_first_pass_yield >= 0.95 else '未达标',
                'quality_score_status': '达标' if avg_quality_score >= 9.0 else '未达标'
            },
            'quality_issues': [
                {
                    'issue_type': '材料缺陷',
                    'frequency': random.randint(1, 20),
                    'impact': random.choice(['高', '中', '低']),
                    'root_cause': '供应商质量问题'
                },
                {
                    'issue_type': '工艺偏差',
                    'frequency': random.randint(1, 15),
                    'impact': random.choice(['高', '中', '低']),
                    'root_cause': '设备参数不稳定'
                },
                {
                    'issue_type': '人为错误',
                    'frequency': random.randint(1, 10),
                    'impact': random.choice(['高', '中', '低']),
                    'root_cause': '操作培训不足'
                }
            ],
            'improvement_actions': [
                '加强供应商质量管理',
                '优化生产工艺参数',
                '提高员工培训',
                '完善质量检测流程'
            ],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_maintenance_schedule(self, product_code: Optional[str] = None) -> Dict[str, Any]:
        """
        获取维护计划
        
        Args:
            product_code: 产品代码，可选
            
        Returns:
            Dict: 维护计划数据
        """
        equipment_list = []
        for i in range(random.randint(8, 15)):
            equipment_code = f'EQ{i+1:03d}'
            last_maintenance = datetime.now() - timedelta(days=random.randint(1, 90))
            next_maintenance = last_maintenance + timedelta(days=random.randint(90, 180))
            
            equipment_list.append({
                'equipment_code': equipment_code,
                'equipment_name': f'设备_{equipment_code}',
                'equipment_type': random.choice(['生产设备', '检测设备', '包装设备', '运输设备']),
                'location': f'生产线{random.randint(1, 5)}',
                'last_maintenance_date': last_maintenance.strftime('%Y-%m-%d'),
                'next_maintenance_date': next_maintenance.strftime('%Y-%m-%d'),
                'maintenance_type': random.choice(['预防性维护', '故障维修', '大修', '校准']),
                'maintenance_duration': random.randint(2, 24),
                'maintenance_cost': round(random.uniform(500, 5000), 2),
                'equipment_status': random.choice(['正常', '需维护', '故障', '维护中']),
                'priority_level': random.choice(['高', '中', '低']),
                'maintenance_team': f'维护组{random.randint(1, 3)}'
            })
        
        # 按维护日期排序
        equipment_list.sort(key=lambda x: x['next_maintenance_date'])
        
        # 统计维护计划
        upcoming_maintenance = [eq for eq in equipment_list if datetime.strptime(eq['next_maintenance_date'], '%Y-%m-%d') <= datetime.now() + timedelta(days=30)]
        overdue_maintenance = [eq for eq in equipment_list if datetime.strptime(eq['next_maintenance_date'], '%Y-%m-%d') < datetime.now()]
        
        return {
            'product_code': product_code or '全部产品',
            'equipment_list': equipment_list,
            'maintenance_summary': {
                'total_equipment': len(equipment_list),
                'upcoming_maintenance': len(upcoming_maintenance),
                'overdue_maintenance': len(overdue_maintenance),
                'normal_status': len([eq for eq in equipment_list if eq['equipment_status'] == '正常']),
                'needs_attention': len([eq for eq in equipment_list if eq['equipment_status'] in ['需维护', '故障']]),
                'total_maintenance_cost': round(sum(eq['maintenance_cost'] for eq in equipment_list), 2)
            },
            'urgent_actions': [
                f'设备{eq["equipment_code"]}需要立即维护' for eq in equipment_list 
                if eq['equipment_status'] == '故障' or eq['priority_level'] == '高'
            ],
            'maintenance_recommendations': [
                '制定预防性维护计划',
                '优化维护资源配置',
                '加强设备监控',
                '建立维护知识库'
            ],
            'updated_at': datetime.now().isoformat()
        } 