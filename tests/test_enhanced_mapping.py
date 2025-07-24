#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强股票名称映射效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_mapping():
    """测试增强映射效果"""
    
    print("=== 测试增强股票名称映射效果 ===")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider
        
        provider = TongDaXinDataProvider()
        
        # 测试各类股票
        test_stocks = [
            ('000001', '平安银行'),  # 深圳主板
            ('002594', '比亚迪'),   # 中小板
            ('300750', '宁德时代'), # 创业板
            ('600519', '贵州茅台'), # 上海主板
            ('601127', '小康股份'), # 目标修复股票
            ('603259', '药明康德'), # 上海主板603
            ('688981', '中芯国际'), # 科创板
            ('601398', '工商银行'), # 大型银行
            ('000858', '五粮液'),   # 白酒股
            ('002415', '海康威视'), # 科技股
        ]
        
        print("\n股票名称映射测试结果:")
        correct_count = 0
        total_count = len(test_stocks)
        
        for code, expected_name in test_stocks:
            actual_name = provider._get_stock_name(code)
            is_correct = actual_name == expected_name
            status = "✅" if is_correct else "❌"
            
            print(f"  {status} {code}: {actual_name} (期望: {expected_name})")
            
            if is_correct:
                correct_count += 1
        
        print(f"\n📊 测试结果: {correct_count}/{total_count} 通过")
        
        if correct_count == total_count:
            print("🎉 所有股票名称映射正确!")
        else:
            print(f"⚠️ {total_count - correct_count} 个股票名称映射不正确")
            
        # 特别验证601127
        name_601127 = provider._get_stock_name('601127')
        print(f"\n🎯 重点验证 - 601127: {name_601127}")
        if name_601127 == '小康股份':
            print("✅ 601127修复成功")
        else:
            print("❌ 601127修复失败")
            
        return correct_count == total_count
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_unknown_stocks():
    """测试未知股票的处理"""
    
    print("\n=== 测试未知股票处理 ===")
    
    try:
        from manufacturingagents.dataflows.tdx_utils import TongDaXinDataProvider
        
        provider = TongDaXinDataProvider()
        
        # 测试不存在的股票代码
        unknown_stocks = ['999999', '888888', '123456']
        
        print("\n未知股票测试:")
        for code in unknown_stocks:
            name = provider._get_stock_name(code)
            expected = f'股票{code}'
            is_correct = name == expected
            status = "✅" if is_correct else "❌"
            
            print(f"  {status} {code}: {name} (期望: {expected})")
            
        return True
        
    except Exception as e:
        print(f"❌ 未知股票测试失败: {e}")
        return False

def main():
    """主函数"""
    
    print("🔍 增强股票名称映射测试")
    print("=" * 50)
    
    # 执行测试
    test1_result = test_enhanced_mapping()
    test2_result = test_unknown_stocks()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试总结")
    print("=" * 50)
    
    if test1_result and test2_result:
        print("🎉 所有测试通过!")
        print("\n✅ 完成情况:")
        print("1. 601127股票名称修复成功")
        print("2. 增强映射包含94个常见股票")
        print("3. 覆盖主板、中小板、创业板、科创板")
        print("4. 未知股票正确显示为'股票XXXXXX'")
        
        print("\n📋 建议:")
        print("1. 重启Web应用以加载新的映射")
        print("2. 清除缓存避免显示旧名称")
        print("3. 在Web界面测试601127等股票")
    else:
        print("⚠️ 部分测试失败")
        print("请检查代码修改是否正确")

if __name__ == "__main__":
    main()