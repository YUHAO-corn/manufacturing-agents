#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试脚本 - 验证601127股票名称修复效果
模拟Web应用的完整数据获取流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manufacturingagents.dataflows.tdx_utils import get_china_stock_data

def test_601127_complete_flow():
    """
    测试601127的完整数据流程
    """
    print("🧪 测试601127完整数据流程...")
    print("=" * 50)
    
    try:
        # 获取601127的完整数据（模拟Web应用调用）
        result = get_china_stock_data(
            stock_code="601127",
            start_date="2025-06-01",
            end_date="2025-07-03"
        )
        
        if result and "股票名称:" in result:
            # 从格式化字符串中提取股票名称
            import re
            name_match = re.search(r'股票名称: (.+)', result)
            stock_name = name_match.group(1).strip() if name_match else 'N/A'
            
            # 提取其他信息用于显示
            price_match = re.search(r'当前价格: ¥([\d.]+)', result)
            change_match = re.search(r'涨跌幅: ([\d.-]+)%', result)
            
            print(f"📊 实时数据获取结果:")
            print(f"   股票代码: 601127")
            print(f"   股票名称: {stock_name}")
            if price_match:
                print(f"   当前价格: ¥{price_match.group(1)}")
            if change_match:
                print(f"   涨跌幅: {change_match.group(1)}%")
            
            # 验证股票名称
            if stock_name == "小康股份":
                print("\n✅ 成功！601127股票名称正确显示为'小康股份'")
                return True
            else:
                print(f"\n❌ 失败！601127股票名称显示为'{stock_name}'，期望'小康股份'")
                return False
        else:
            print("❌ 无法获取601127的实时数据")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        return False

def test_other_stocks_sample():
    """
    测试其他几个股票的名称显示
    """
    print("\n🧪 测试其他股票名称显示...")
    print("=" * 50)
    
    test_stocks = ['000001', '600519', '300750']  # 平安银行、贵州茅台、宁德时代
    expected_names = ['平安银行', '贵州茅台', '宁德时代']
    
    all_passed = True
    
    for stock_code, expected_name in zip(test_stocks, expected_names):
        try:
            result = get_china_stock_data(
                stock_code=stock_code,
                start_date="2025-06-01",
                end_date="2025-07-03"
            )
            
            if result and "股票名称:" in result:
                # 从格式化字符串中提取股票名称
                import re
                name_match = re.search(r'股票名称: (.+)', result)
                actual_name = name_match.group(1).strip() if name_match else 'N/A'
                
                status = "✅" if actual_name == expected_name else "❌"
                print(f"   {status} {stock_code}: {actual_name} (期望: {expected_name})")
                
                if actual_name != expected_name:
                    all_passed = False
            else:
                print(f"   ❌ {stock_code}: 无法获取数据")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ {stock_code}: 异常 - {e}")
            all_passed = False
    
    return all_passed

def main():
    """
    主测试函数
    """
    print("🚀 开始最终验证测试")
    print("=" * 60)
    
    # 测试601127
    test1_passed = test_601127_complete_flow()
    
    # 测试其他股票
    test2_passed = test_other_stocks_sample()
    
    print("\n" + "=" * 60)
    print("📊 最终测试结果")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("🎉 所有测试通过！")
        print("\n✅ 修复总结:")
        print("   • 601127股票名称已正确修复为'小康股份'")
        print("   • 股票名称映射功能正常工作")
        print("   • 完整数据流程验证通过")
        print("\n📋 下一步:")
        print("   1. 重启Web应用服务器")
        print("   2. 清除Redis缓存（如果有）")
        print("   3. 在Web界面重新查询601127验证效果")
    else:
        print("❌ 部分测试失败，需要进一步检查")
        if not test1_passed:
            print("   • 601127测试失败")
        if not test2_passed:
            print("   • 其他股票测试失败")

if __name__ == "__main__":
    main()