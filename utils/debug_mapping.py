#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider

provider = TongDaXinDataProvider()

test_stocks = [
    ('000001', '平安银行'),
    ('002594', '比亚迪'),
    ('300750', '宁德时代'),
    ('600519', '贵州茅台'),
    ('601127', '小康股份'),
    ('603259', '药明康德'),
    ('688981', '中芯国际'),
    ('601398', '工商银行'),
    ('000858', '五粮液'),
    ('002415', '海康威视')
]

print('详细检查每个股票映射:')
for code, expected in test_stocks:
    actual = provider._get_stock_name(code)
    status = "✅" if actual == expected else "❌"
    print(f'{status} {code}: 实际="{actual}" vs 期望="{expected}"')
    if actual != expected:
        print(f'   >>> 不匹配: "{actual}" != "{expected}"')