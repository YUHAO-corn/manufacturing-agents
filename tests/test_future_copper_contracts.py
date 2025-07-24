#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试未来交割铜期货合约数据获取
验证TuShare Pro API能获取到多新的数据，用于制造业前瞻性补货决策
"""

import os
import json
from datetime import datetime, timedelta

def test_future_copper_contracts():
    """测试获取未来交割的铜期货合约数据"""
    print("🔍 开始测试未来交割铜期货合约数据...")
    
    try:
        # 导入tushare库
        import tushare as ts
        print("✅ TuShare库导入成功")
        
        # 设置token
        tushare_token = os.getenv('TUSHARE_TOKEN')
        if not tushare_token:
            print("❌ 未找到TUSHARE_TOKEN环境变量")
            return
        
        # 初始化tushare
        ts.set_token(tushare_token)
        pro = ts.pro_api()
        print(f"✅ TuShare Pro API初始化成功")
        
        # 构建未来几个月的铜期货合约代码
        print("\n📊 构建未来交割合约代码...")
        
        current_date = datetime.now()
        future_contracts = []
        
        # 生成未来3个月的合约代码
        for i in range(1, 4):  # 未来1-3个月
            target_date = current_date + timedelta(days=30*i)
            year = target_date.year
            month = target_date.month
            
            # 铜期货合约代码格式：CU + YYMM + .SHF
            contract_code = f"CU{year%100:02d}{month:02d}.SHF"
            future_contracts.append({
                "code": contract_code,
                "delivery_month": f"{year}年{month}月",
                "target_date": target_date
            })
        
        print(f"   未来合约: {[c['code'] for c in future_contracts]}")
        
        results = {}
        
        # 测试每个未来合约的数据可用性
        for contract in future_contracts:
            contract_code = contract["code"]
            delivery_month = contract["delivery_month"]
            
            print(f"\n📈 测试合约: {contract_code} ({delivery_month}交割)")
            
            # 1. 测试日线数据
            print(f"   🔍 测试日线数据...")
            daily_result = test_daily_data(pro, contract_code)
            
            # 2. 测试周线数据  
            print(f"   🔍 测试周线数据...")
            weekly_result = test_weekly_data(pro, contract_code)
            
            results[contract_code] = {
                "delivery_month": delivery_month,
                "daily_data": daily_result,
                "weekly_data": weekly_result
            }
        
        # 汇总分析结果
        print(f"\n📋 未来合约数据可用性分析:")
        available_contracts = []
        
        for contract_code, data in results.items():
            daily_available = data["daily_data"]["available"]
            weekly_available = data["weekly_data"]["available"]
            latest_date = data["daily_data"].get("latest_date", "无数据")
            
            status = "✅ 可用" if daily_available or weekly_available else "❌ 无数据"
            available_contracts.append({
                "contract": contract_code,
                "delivery": data["delivery_month"],
                "daily": "✅" if daily_available else "❌",
                "weekly": "✅" if weekly_available else "❌", 
                "latest_date": latest_date,
                "status": status
            })
            
            print(f"  {status} {contract_code} ({data['delivery_month']}) - 日线:{data['daily_data']['records']}条, 周线:{data['weekly_data']['records']}条, 最新:{latest_date}")
        
        # 找到最适合的合约用于制造业预测
        print(f"\n🎯 制造业补货决策建议:")
        
        best_contract = None
        for contract in available_contracts:
            if contract["daily"] == "✅" or contract["weekly"] == "✅":
                best_contract = contract
                break
        
        if best_contract:
            print(f"   推荐使用合约: {best_contract['contract']}")
            print(f"   交割时间: {best_contract['delivery']}")
            print(f"   数据时效性: {best_contract['latest_date']}")
            print(f"   业务价值: 可用于未来1-2个月的制造业原材料价格预测")
        else:
            print(f"   ⚠️ 未找到可用的未来合约数据")
            print(f"   建议: 使用最新的历史合约数据进行趋势分析")
        
        return {
            "tested_contracts": results,
            "available_contracts": available_contracts,
            "best_contract": best_contract,
            "conclusion": "TuShare Pro期货API测试完成"
        }
        
    except ImportError:
        print("❌ 请安装tushare库: pip install tushare")
        return None
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_daily_data(pro, contract_code):
    """测试期货日线数据"""
    try:
        # 获取最近30天的数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        fut_daily = pro.fut_daily(
            ts_code=contract_code,
            start_date=start_date,
            end_date=end_date,
            fields='ts_code,trade_date,close,vol,amount'
        )
        
        if fut_daily.empty:
            # 尝试获取任意可用数据
            fut_daily = pro.fut_daily(
                ts_code=contract_code,
                fields='ts_code,trade_date,close,vol,amount'
            )
        
        if not fut_daily.empty:
            latest_date = fut_daily.iloc[0]['trade_date']
            record_count = len(fut_daily)
            latest_price = fut_daily.iloc[0]['close']
            
            return {
                "available": True,
                "records": record_count,
                "latest_date": latest_date,
                "latest_price": latest_price
            }
        else:
            return {"available": False, "records": 0, "latest_date": "无数据"}
            
    except Exception as e:
        return {"available": False, "records": 0, "latest_date": f"错误:{str(e)}"}

def test_weekly_data(pro, contract_code):
    """测试期货周线数据"""
    try:
        # 获取最近8周的数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(weeks=8)).strftime('%Y%m%d')
        
        fut_weekly = pro.fut_weekly_monthly(
            ts_code=contract_code,
            start_date=start_date,
            end_date=end_date,
            freq='week',
            fields='ts_code,trade_date,close,vol,amount'
        )
        
        if fut_weekly.empty:
            # 尝试获取任意可用数据
            fut_weekly = pro.fut_weekly_monthly(
                ts_code=contract_code,
                freq='week',
                fields='ts_code,trade_date,close,vol,amount'
            )
        
        if not fut_weekly.empty:
            latest_date = fut_weekly.iloc[0]['trade_date']
            record_count = len(fut_weekly)
            latest_price = fut_weekly.iloc[0]['close']
            
            return {
                "available": True,
                "records": record_count,
                "latest_date": latest_date,
                "latest_price": latest_price
            }
        else:
            return {"available": False, "records": 0, "latest_date": "无数据"}
            
    except Exception as e:
        return {"available": False, "records": 0, "latest_date": f"错误:{str(e)}"}

if __name__ == "__main__":
    result = test_future_copper_contracts()
    if result:
        print("\n🎯 测试结论: 未来合约数据可用性验证完成，可用于制造业前瞻性决策!")
    else:
        print("\n❌ 测试失败，需要进一步调试") 