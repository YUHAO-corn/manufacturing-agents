#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据适配器
基于现有dataflows架构，复用所有缓存和降级机制
只需要适配数据源和接口，不重新造轮子
"""

import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# 复用现有的数据架构
try:
    from manufacturingagents.dataflows.stock_data_service import StockDataService
    from manufacturingagents.dataflows.cache_manager import get_cache
    from manufacturingagents.dataflows.config import get_config
    from manufacturingagents.config.database_manager import get_database_manager
    DATA_INFRASTRUCTURE_AVAILABLE = True
except ImportError:
    DATA_INFRASTRUCTURE_AVAILABLE = False

logger = logging.getLogger(__name__)

class ManufacturingDataAdapter:
    """
    制造业数据适配器
    基于现有StockDataService架构，复用所有底层能力
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 复用现有的基础服务
        if DATA_INFRASTRUCTURE_AVAILABLE:
            self.cache = get_cache()
            self.config = get_config()
            self.db_manager = get_database_manager()
            self.stock_service = StockDataService()  # 复用现有服务
        else:
            self.logger.warning("数据基础设施不可用，将使用模拟数据")
            self.cache = None
            self.config = None
            self.db_manager = None
            self.stock_service = None
        
        # 制造业数据源映射（复用现有API连接）
        self.data_source_mapping = {
            # 原股票数据源 -> 制造业数据应用
            'stock_price': 'raw_material_price',      # 股价 -> 原材料价格
            'stock_volume': 'production_volume',      # 成交量 -> 生产量
            'financial_data': 'cost_analysis',        # 财务数据 -> 成本分析
            'news_sentiment': 'market_sentiment',     # 新闻情绪 -> 市场情绪
            'analyst_reports': 'industry_reports',    # 分析师报告 -> 行业报告
            'insider_trading': 'supply_chain_intel',  # 内幕交易 -> 供应链情报
        }
        
        self.logger.info("制造业数据适配器初始化完成")
    
    def get_product_data(self, product_code: str, start_date: str, end_date: str) -> str:
        """
        获取产品数据（复用股票数据获取逻辑）
        
        Args:
            product_code: 产品代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            格式化的产品数据
        """
        self.logger.info(f"获取产品数据: {product_code} ({start_date} 到 {end_date})")
        
        # 复用现有缓存机制
        if self.cache:
            cache_key = self.cache.find_cached_stock_data(
                symbol=product_code,
                start_date=start_date,
                end_date=end_date,
                data_source="manufacturing"
            )
            
            if cache_key:
                cached_data = self.cache.load_stock_data(cache_key)
                if cached_data is not None:
                    self.logger.info(f"从缓存加载产品数据: {product_code}")
                    # 确保数据是字符串格式
                    if isinstance(cached_data, pd.DataFrame):
                        cached_data = cached_data.to_string()
                    elif not isinstance(cached_data, str):
                        cached_data = str(cached_data)
                    return self._adapt_to_manufacturing_format(cached_data, product_code)
        
        # 直接调用通达信API获取股票数据（绕过有问题的stock_service）
        try:
            # 将产品代码映射为股票代码格式
            stock_code = self._map_product_to_stock_code(product_code)
            
            # 直接调用通达信API
            from manufacturingagents.dataflows.tdx_utils import get_china_stock_data
            raw_data = get_china_stock_data(stock_code, start_date, end_date)
            
            # 检查数据是否有效
            if raw_data and "❌" not in raw_data and len(raw_data) > 100:
                # 适配为制造业格式
                manufacturing_data = self._adapt_to_manufacturing_format(raw_data, product_code)
                
                # 缓存结果
                if self.cache:
                    self.cache.save_stock_data(
                        symbol=product_code,
                        data=manufacturing_data,
                        start_date=start_date,
                        end_date=end_date,
                        data_source="manufacturing"
                    )
                
                self.logger.info(f"✅ 成功获取并适配真实数据: {product_code}")
                return manufacturing_data
            else:
                self.logger.warning(f"通达信API返回数据无效: {product_code}")
                
        except Exception as e:
            self.logger.error(f"通达信API调用失败: {e}")
        
        # 降级到模拟数据
        self.logger.info(f"降级到模拟数据: {product_code}")
        return self._generate_manufacturing_fallback(product_code, start_date, end_date)
    
    def get_supplier_data(self, supplier_code: str) -> Dict[str, Any]:
        """
        获取供应商数据（复用基础信息获取逻辑）
        """
        self.logger.info(f"获取供应商数据: {supplier_code}")
        
        # 复用现有基础信息获取
        if self.stock_service:
            stock_info = self.stock_service.get_stock_basic_info(supplier_code)
            if stock_info:
                return self._adapt_to_supplier_format(stock_info, supplier_code)
        
        # 模拟数据
        return {
            'supplier_code': supplier_code,
            'supplier_name': f'供应商_{supplier_code}',
            'reliability_score': 85,
            'delivery_performance': 92,
            'quality_rating': 'A',
            'capacity_utilization': 78,
            'lead_time_days': 15,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_market_news(self, product_category: str, days_back: int = 7) -> str:
        """
        获取市场新闻（复用现有新闻获取逻辑）
        """
        self.logger.info(f"获取市场新闻: {product_category}")
        
        # 复用现有新闻API
        try:
            from manufacturingagents.dataflows.interface import get_finnhub_news, get_google_news
            
            # 将产品类别映射为相关股票代码
            stock_symbol = self._map_category_to_stock(product_category)
            
            # 获取新闻（复用现有接口）
            curr_date = datetime.now().strftime('%Y-%m-%d')
            news_data = get_finnhub_news(stock_symbol, curr_date, days_back)
            
            # 适配为制造业新闻格式
            return self._adapt_to_manufacturing_news(news_data, product_category)
            
        except Exception as e:
            self.logger.error(f"获取市场新闻失败: {e}")
            return self._generate_news_fallback(product_category)
    
    def get_industry_analysis(self, industry_code: str) -> str:
        """
        获取行业分析（复用现有分析能力）
        """
        self.logger.info(f"获取行业分析: {industry_code}")
        
        try:
            from manufacturingagents.dataflows.interface import get_fundamentals_openai
            
            # 映射行业代码到相关股票
            stock_symbol = self._map_industry_to_stock(industry_code)
            
            # 获取基本面分析
            curr_date = datetime.now().strftime('%Y-%m-%d')
            analysis_data = get_fundamentals_openai(stock_symbol, curr_date)
            
            # 适配为制造业行业分析
            return self._adapt_to_industry_analysis(analysis_data, industry_code)
            
        except Exception as e:
            self.logger.error(f"获取行业分析失败: {e}")
            return self._generate_industry_fallback(industry_code)
    
    def _map_product_to_stock_code(self, product_code: str) -> str:
        """将产品代码映射为股票代码"""
        # 示例映射逻辑，实际可根据需要调整
        product_to_stock_mapping = {
            'STEEL_001': '600019',  # 宝钢股份
            'COPPER_001': '600362', # 江西铜业
            'PLASTIC_001': '000301', # 东方盛虹
            'RUBBER_001': '600623', # 华谊集团
        }
        
        return product_to_stock_mapping.get(product_code, '000001')  # 默认平安银行
    
    def _map_category_to_stock(self, category: str) -> str:
        """将产品类别映射为相关股票代码"""
        category_mapping = {
            'steel': 'X',      # 美国钢铁
            'copper': 'FCX',   # 自由港
            'plastic': 'DOW',  # 陶氏化学
            'rubber': 'TROX',  # 泰瑞橡胶
        }
        return category_mapping.get(category.lower(), 'SPY')  # 默认S&P 500
    
    def _map_industry_to_stock(self, industry_code: str) -> str:
        """将行业代码映射为代表性股票"""
        industry_mapping = {
            'MANUFACTURING': 'GE',    # 通用电气
            'AUTOMOTIVE': 'F',        # 福特
            'ELECTRONICS': 'AAPL',    # 苹果
            'CHEMICALS': 'DD',        # 杜邦
        }
        return industry_mapping.get(industry_code, 'SPY')
    
    def _adapt_to_manufacturing_format(self, raw_data: str, product_code: str) -> str:
        """将股票数据格式适配为制造业格式"""
        if not raw_data or "❌" in raw_data:
            return raw_data
        
        # 简单的文本替换适配
        adapted_data = raw_data.replace("股票", "产品")
        adapted_data = adapted_data.replace("股价", "价格")
        adapted_data = adapted_data.replace("成交量", "需求量")
        adapted_data = adapted_data.replace("涨跌幅", "价格变动")
        
        # 添加制造业特有信息
        manufacturing_header = f"""
# 产品数据分析报告 - {product_code}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 数据来源: 制造业数据适配器
# 基础数据: 复用现有金融数据API

"""
        return manufacturing_header + adapted_data
    
    def _adapt_to_supplier_format(self, stock_info: Dict[str, Any], supplier_code: str) -> Dict[str, Any]:
        """将股票信息适配为供应商格式"""
        return {
            'supplier_code': supplier_code,
            'supplier_name': stock_info.get('name', f'供应商_{supplier_code}'),
            'market_type': stock_info.get('market', '制造业'),
            'category': stock_info.get('category', '供应商'),
            'reliability_score': 85,  # 模拟评分
            'delivery_performance': 92,
            'quality_rating': 'A',
            'source': 'adapted_from_stock_data',
            'last_updated': datetime.now().isoformat()
        }
    
    def _adapt_to_manufacturing_news(self, news_data: str, product_category: str) -> str:
        """将股票新闻适配为制造业新闻格式"""
        if not news_data:
            return f"# {product_category} 相关新闻\n\n暂无相关新闻数据"
        
        # 文本适配
        adapted_news = news_data.replace("股票", "产品")
        adapted_news = adapted_news.replace("投资", "采购")
        adapted_news = adapted_news.replace("股东", "客户")
        
        return f"# {product_category} 市场新闻\n\n{adapted_news}"
    
    def _adapt_to_industry_analysis(self, analysis_data: str, industry_code: str) -> str:
        """将基本面分析适配为行业分析"""
        if not analysis_data:
            return f"# {industry_code} 行业分析\n\n暂无分析数据"
        
        # 文本适配
        adapted_analysis = analysis_data.replace("财务", "运营")
        adapted_analysis = adapted_analysis.replace("营收", "产能")
        adapted_analysis = adapted_analysis.replace("股东权益", "运营效率")
        
        return f"# {industry_code} 行业分析报告\n\n{adapted_analysis}"
    
    def _generate_manufacturing_fallback(self, product_code: str, start_date: str, end_date: str) -> str:
        """生成制造业模拟数据"""
        return f"""
# 制造业产品数据 - {product_code}
# 时间范围: {start_date} 到 {end_date}
# 状态: 模拟数据（所有数据源不可用）

## 产品基本信息
产品代码: {product_code}
产品名称: 制造业产品_{product_code}
产品类别: 标准制造业产品

## 价格趋势
当前价格: ¥158.50/单位
价格变动: +2.3%
历史最高: ¥165.20
历史最低: ¥142.80

## 需求分析
当前需求量: 12,500单位
需求变化: +5.2%
季节性指数: 1.15

## 供应情况
主要供应商: 3家
供应稳定性: 85%
平均交货期: 15天

⚠️ 注意: 这是模拟数据，仅用于演示目的
"""
    
    def _generate_news_fallback(self, product_category: str) -> str:
        """生成新闻模拟数据"""
        return f"""
# {product_category} 市场新闻 (模拟)

## 行业动态
- 【今日】{product_category}行业整体需求稳定，价格小幅上涨
- 【昨日】主要供应商产能利用率达到85%，供应充足
- 【本周】原材料价格波动，建议关注成本控制

## 市场分析
- 需求端：下游制造业复苏，订单量持续增长
- 供给端：主要产区生产正常，库存水平合理
- 价格：短期内预计保持稳定，长期看涨

⚠️ 注意: 这是模拟新闻，仅用于演示目的
"""
    
    def _generate_industry_fallback(self, industry_code: str) -> str:
        """生成行业分析模拟数据"""
        return f"""
# {industry_code} 行业分析报告 (模拟)

## 行业概况
- 行业代码: {industry_code}
- 市场规模: 稳步增长
- 竞争格局: 适度竞争
- 发展阶段: 成熟期

## 关键指标
- 产能利用率: 78%
- 平均毛利率: 15.2%
- 行业集中度: 中等
- 技术创新度: 中高

## 风险因素
- 原材料价格波动
- 环保政策变化
- 国际贸易摩擦
- 技术更新迭代

⚠️ 注意: 这是模拟分析，仅用于演示目的
"""

# 全局适配器实例
_manufacturing_adapter = None

def get_manufacturing_adapter() -> ManufacturingDataAdapter:
    """获取制造业数据适配器实例（单例模式）"""
    global _manufacturing_adapter
    if _manufacturing_adapter is None:
        _manufacturing_adapter = ManufacturingDataAdapter()
    return _manufacturing_adapter

# 对外接口函数（与原有接口保持一致）
def get_manufacturing_data(product_code: str, start_date: str, end_date: str) -> str:
    """获取制造业数据的主要接口"""
    adapter = get_manufacturing_adapter()
    return adapter.get_product_data(product_code, start_date, end_date)

def get_supplier_info(supplier_code: str) -> Dict[str, Any]:
    """获取供应商信息"""
    adapter = get_manufacturing_adapter()
    return adapter.get_supplier_data(supplier_code)

def get_manufacturing_news(product_category: str, days_back: int = 7) -> str:
    """获取制造业新闻"""
    adapter = get_manufacturing_adapter()
    return adapter.get_market_news(product_category, days_back)

def get_industry_report(industry_code: str) -> str:
    """获取行业报告"""
    adapter = get_manufacturing_adapter()
    return adapter.get_industry_analysis(industry_code) 