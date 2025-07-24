#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于QUANTAXIS QATdx.py的增强股票列表获取器
参考QA_fetch_get_stock_list函数实现完整的股票信息获取
"""

import pandas as pd
from pytdx.hq import TdxHq_API
import datetime
import time
import json
import os
import random


def for_sz(code):
    """深市代码分类
    Arguments:
        code {str} -- 股票代码
    Returns:
        str -- 股票类型
    """
    if str(code)[0:2] in ['00', '30', '02']:
        return 'stock_cn'
    elif str(code)[0:2] in ['39']:
        return 'index_cn'
    elif str(code)[0:2] in ['15', '16']:
        return 'etf_cn'
    elif str(code)[0:3] in ['101', '104', '105', '106', '107', '108', '109',
                            '111', '112', '114', '115', '116', '117', '118', '119',
                            '123', '127', '128', '131', '139']:
        return 'bond_cn'
    else:
        return 'undefined'


def for_sh(code):
    """沪市代码分类
    Arguments:
        code {str} -- 股票代码
    Returns:
        str -- 股票类型
    """
    if str(code)[0] == '6':
        return 'stock_cn'
    elif str(code)[0:3] in ['000', '880']:
        return 'index_cn'
    elif str(code)[0:2] in ['51', '58']:
        return 'etf_cn'
    elif str(code)[0:3] in ['102', '110', '113', '120', '122', '124',
                            '130', '132', '133', '134', '135', '136',
                            '140', '141', '143', '144', '147', '148']:
        return 'bond_cn'
    else:
        return 'undefined'


def _select_market_code(code):
    """选择市场代码
    Arguments:
        code {str} -- 股票代码
    Returns:
        int -- 市场代码 (0=深圳, 1=上海)
    """
    if str(code)[0] in ['0', '1', '2', '3']:
        return 0  # 深圳
    elif str(code)[0] in ['5', '6', '7', '8', '9']:
        return 1  # 上海
    else:
        return 0  # 默认深圳


def load_tdx_servers_config():
    """从配置文件加载通达信服务器列表
    
    Returns:
        list: 服务器配置列表
    """
    config_file = 'tdx_servers_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('working_servers', [])
        except Exception as e:
            print(f"⚠️ 读取服务器配置文件失败: {e}")
    
    # 如果配置文件不存在或读取失败，返回默认服务器
    return [
        {"ip": "119.147.212.81", "port": 7709, "name": "默认服务器1"},
        {"ip": "115.238.56.198", "port": 7709, "name": "默认服务器2"}
    ]


def get_mainmarket_ip(ip=None, port=None):
    """获取主市场IP
    优先使用配置文件中的服务器，支持随机选择和故障转移
    """
    if ip is not None and port is not None:
        return ip, port
    
    servers = load_tdx_servers_config()
    if servers:
        # 随机选择一个服务器
        server = random.choice(servers)
        return server['ip'], server['port']
    
    # 兜底方案
    return '119.147.212.81', 7709


def enhanced_fetch_stock_list(type_='stock', ip=None, port=None, max_retries=3, enable_server_failover=True):
    """
    增强版股票列表获取函数
    基于QUANTAXIS的QA_fetch_get_stock_list实现
    
    Args:
        type_ (str): 股票类型 ('stock', 'index', 'etf', 'bond', 'all')
        ip (str): 通达信服务器IP
        port (int): 通达信服务器端口
        max_retries (int): 最大重试次数
        enable_server_failover (bool): 是否启用服务器故障转移
    
    Returns:
        pd.DataFrame: 包含完整股票信息的DataFrame
    """
    # 如果指定了IP和端口，直接使用
    if ip is not None and port is not None:
        servers_to_try = [{'ip': ip, 'port': port, 'name': '指定服务器'}]
    elif enable_server_failover:
        # 启用故障转移，获取所有可用服务器
        servers_to_try = load_tdx_servers_config()
        random.shuffle(servers_to_try)  # 随机打乱服务器顺序
    else:
        # 不启用故障转移，只使用一个服务器
        ip, port = get_mainmarket_ip(ip, port)
        servers_to_try = [{'ip': ip, 'port': port, 'name': '单一服务器'}]
    
    for server_idx, server in enumerate(servers_to_try):
        server_ip = server['ip']
        server_port = server['port']
        server_name = server.get('name', f'{server_ip}:{server_port}')
        
        print(f"🔗 尝试连接服务器: {server_name} ({server_ip}:{server_port})")
        
        for attempt in range(max_retries):
            try:
                api = TdxHq_API()
                with api.connect(server_ip, server_port, time_out=10):
                    print(f"✅ 成功连接通达信服务器: {server_name} ({server_ip}:{server_port})")
                    
                    # 使用与原始QA_fetch_get_stock_list相同的逻辑
                    data = pd.concat(
                        [pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(
                            sse='sz' if j == 0 else 'sh') for i in
                            range(int(api.get_security_count(j) / 1000) + 1)], axis=0, sort=False) for
                            j in range(2)], axis=0, sort=False)
                    
                    print(f"📈 总共获取到 {len(data)} 条股票数据")
                    print(f"📋 数据列: {list(data.columns)}")
                    
                    # 去重
                    data = data.drop_duplicates()
                    
                    # 选择需要的列并设置索引
                    data = data.loc[:, ['code', 'volunit', 'decimal_point', 'name', 'pre_close', 'sse']].set_index(
                        ['code', 'sse'], drop=False)
                    
                    # 分别处理深圳和上海数据
                    sz = data.query('sse=="sz"')
                    sh = data.query('sse=="sh"')
                    
                    # 添加股票分类
                    sz = sz.assign(sec=sz.code.apply(for_sz))
                    sh = sh.assign(sec=sh.code.apply(for_sh))
                    
                    # 根据类型过滤并返回结果
                    if type_ in ['stock', 'gp']:
                        result = pd.concat([sz, sh], sort=False).query(
                            'sec=="stock_cn"').sort_index().assign(
                            name=data['name'].apply(lambda x: str(x)[0:6]))
                        print(f"🏢 筛选出 {len(result)} 只股票")
                    elif type_ in ['index', 'zs']:
                        result = pd.concat([sz, sh], sort=False).query(
                            'sec=="index_cn"').sort_index().assign(
                            name=data['name'].apply(lambda x: str(x)[0:6]))
                        print(f"📊 筛选出 {len(result)} 个指数")
                    elif type_ in ['etf', 'ETF']:
                        result = pd.concat([sz, sh], sort=False).query(
                            'sec=="etf_cn"').sort_index().assign(
                            name=data['name'].apply(lambda x: str(x)[0:6]))
                        print(f"📈 筛选出 {len(result)} 个ETF")
                    elif type_ in ['bond']:
                        result = pd.concat([sz, sh], sort=False).query(
                            'sec=="bond_cn"').sort_index().assign(
                            name=data['name'].apply(lambda x: str(x)[0:6]))
                        print(f"💰 筛选出 {len(result)} 个债券")
                    else:
                        result = data.assign(
                            code=data['code'].apply(lambda x: str(x))).assign(
                            name=data['name'].apply(lambda x: str(x)[0:6]))
                        print(f"📋 返回所有 {len(result)} 条数据")
                    
                    # 添加详细分类信息
                    if 'sec' in result.columns:
                        result = result.assign(
                            market=result['sse'].apply(lambda x: '深圳' if x == 'sz' else '上海'),
                            category=result['sec'].apply(lambda x: {
                                'stock_cn': '股票',
                                'index_cn': '指数', 
                                'etf_cn': 'ETF',
                                'bond_cn': '债券',
                                'undefined': '未定义'
                            }.get(x, '未知'))
                        )
                    
                    return result
                    
            except Exception as e:
                print(f"❌ 服务器 {server_name} 第{attempt + 1}次尝试失败: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 0.1  # 递增等待时间
                    print(f"⏳ 等待 {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ 服务器 {server_name} 所有重试都失败")
                    break  # 跳出重试循环，尝试下一个服务器
        
        # 如果当前服务器失败，尝试下一个服务器
        if server_idx < len(servers_to_try) - 1:
            print(f"🔄 尝试下一个服务器...")
        else:
            print(f"❌ 所有服务器都无法连接，获取股票列表失败")
    
    return pd.DataFrame()


def test_enhanced_stock_list():
    """测试增强版股票列表获取函数"""
    print("=== 测试增强版股票列表获取函数 ===")
    
    # 测试获取股票列表
    print("\n1. 获取股票列表:")
    stocks = enhanced_fetch_stock_list(type_='stock')
    if not stocks.empty:
        print(f"获取到 {len(stocks)} 只股票")
        print("\n前10只股票:")
        print(stocks[['code', 'name', 'market', 'category']].head(10))
        
        # 查找特定股票
        test_codes = ['000001', '600519', '300750']
        print("\n查找特定股票:")
        for code in test_codes:
            if code in stocks.index.get_level_values('code'):
                stock_info = stocks[stocks['code'] == code].iloc[0]
                print(f"  {code}: {stock_info['name']} ({stock_info['market']}市场)")
            else:
                print(f"  {code}: 未找到")
    
    # 测试获取指数列表
    print("\n2. 获取指数列表:")
    indices = enhanced_fetch_stock_list(type_='index')
    if not indices.empty:
        print(f"获取到 {len(indices)} 个指数")
        print("\n前5个指数:")
        print(indices[['code', 'name', 'market', 'category']].head(5))
    
    # 测试获取ETF列表
    print("\n3. 获取ETF列表:")
    etfs = enhanced_fetch_stock_list(type_='etf')
    if not etfs.empty:
        print(f"获取到 {len(etfs)} 个ETF")
        print("\n前5个ETF:")
        print(etfs[['code', 'name', 'market', 'category']].head(5))


if __name__ == "__main__":
    test_enhanced_stock_list()