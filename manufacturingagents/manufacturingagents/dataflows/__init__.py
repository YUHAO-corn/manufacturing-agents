#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业数据流模块
提供制造业补货决策所需的各种数据接口
"""

from .supply_chain_data import SupplyChainDataProvider
from .demand_forecast_data import DemandForecastDataProvider
from .market_price_data import MarketPriceDataProvider
from .inventory_data import InventoryDataProvider
from .production_data import ProductionDataProvider

# 新增：制造业数据适配器（基于现有架构）
from .manufacturing_data_adapter import (
    ManufacturingDataAdapter,
    get_manufacturing_adapter,
    get_manufacturing_data,
    get_supplier_info,
    get_manufacturing_news,
    get_industry_report
)

__all__ = [
    'SupplyChainDataProvider',
    'DemandForecastDataProvider', 
    'MarketPriceDataProvider',
    'InventoryDataProvider',
    'ProductionDataProvider',
    # 新增适配器
    'ManufacturingDataAdapter',
    'get_manufacturing_adapter',
    'get_manufacturing_data',
    'get_supplier_info',
    'get_manufacturing_news',
    'get_industry_report'
] 