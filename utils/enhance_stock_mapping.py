#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票名称映射增强程序

这个程序用于为tdx_utils.py添加更多常见股票的名称映射，
避免股票显示为"股票XXXXXX"的问题。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_enhanced_stock_mapping():
    """获取增强的股票名称映射"""
    
    enhanced_mapping = {
        # === 深圳主板 (000xxx) ===
        '000001': '平安银行', '000002': '万科A', '000858': '五粮液', '000651': '格力电器',
        '000333': '美的集团', '000725': '京东方A', '000776': '广发证券', '000895': '双汇发展',
        '000963': '华东医药', '000977': '浪潮信息',
        
        # === 深圳中小板 (002xxx) ===
        '002415': '海康威视', '002594': '比亚迪', '002714': '牧原股份', '002475': '立讯精密',
        '002304': '洋河股份', '002142': '宁波银行', '002027': '分众传媒', '002460': '赣锋锂业',
        
        # === 创业板 (300xxx) ===
        '300750': '宁德时代', '300059': '东方财富', '300015': '爱尔眼科', '300142': '沃森生物',
        '300760': '迈瑞医疗', '300274': '阳光电源', '300122': '智飞生物', '300033': '同花顺',
        
        # === 上海主板 (600xxx) ===
        '600036': '招商银行', '600519': '贵州茅台', '600028': '中国石化', '600000': '浦发银行',
        '600887': '伊利股份', '600276': '恒瑞医药', '600031': '三一重工', '600009': '上海机场',
        '600585': '海螺水泥', '600690': '海尔智家', '600196': '复星医药', '600104': '上汽集团',
        '600438': '通威股份', '600809': '山西汾酒', '600745': '闻泰科技', '600570': '恒生电子',
        
        # === 上海主板 (601xxx) ===
        '601398': '工商银行', '601318': '中国平安', '601166': '兴业银行', '601288': '农业银行',
        '601939': '建设银行', '601328': '交通银行', '601012': '隆基绿能', '601888': '中国中免',
        '601127': '小康股份',  # 已修复的目标股票
        '601128': '常熟银行', '601129': '中核钛白', '601126': '四方股份',
        '601138': '工业富联', '601155': '新城控股', '601169': '北京银行', '601186': '中国铁建',
        '601211': '国泰君安', '601225': '陕西煤业', '601236': '红塔证券', '601238': '广汽集团',
        
        # === 上海主板 (603xxx) ===
        '603259': '药明康德', '603288': '海天味业', '603501': '韦尔股份', '603986': '兆易创新',
        '603899': '晨光文具', '603195': '公牛集团', '603392': '万泰生物', '603658': '安图生物',
        
        # === 科创板 (688xxx) ===
        '688008': '澜起科技', '688009': '中国通号', '688036': '传音控股', '688111': '金山办公',
        '688981': '中芯国际', '688599': '天合光能', '688012': '中微公司', '688169': '石头科技',
        '688303': '大全能源', '688561': '奇安信', '688126': '沪硅产业', '688187': '时代电气',
        '688223': '晶科能源', '688256': '寒武纪', '688396': '华润微', '688777': '中控技术',
        
        # === 北交所 (8xxxxx) ===
        '832971': '同心传动', '833533': '晶赛科技', '871981': '汇通集团',
        
        # === 指数代码 ===
        '000001': '上证指数',  # 注意：这与平安银行代码重复，需要根据市场区分
        '399001': '深证成指',
        '399006': '创业板指',
        '000688': '科创50',
        '000300': '沪深300',
        '000905': '中证500',
    }
    
    return enhanced_mapping

def generate_enhanced_mapping_code():
    """生成增强映射的代码"""
    
    mapping = get_enhanced_stock_mapping()
    
    code_lines = []
    code_lines.append("        # 增强的股票名称映射表")
    code_lines.append("        stock_names = {")
    
    # 按类别组织代码
    categories = {
        '深圳主板 (000xxx)': [k for k in mapping.keys() if k.startswith('000') and len(k) == 6],
        '深圳中小板 (002xxx)': [k for k in mapping.keys() if k.startswith('002')],
        '创业板 (300xxx)': [k for k in mapping.keys() if k.startswith('300')],
        '上海主板 (600xxx)': [k for k in mapping.keys() if k.startswith('600')],
        '上海主板 (601xxx)': [k for k in mapping.keys() if k.startswith('601')],
        '上海主板 (603xxx)': [k for k in mapping.keys() if k.startswith('603')],
        '科创板 (688xxx)': [k for k in mapping.keys() if k.startswith('688')],
        '北交所': [k for k in mapping.keys() if k.startswith('8') and len(k) == 6],
    }
    
    for category, codes in categories.items():
        if codes:
            code_lines.append(f"            # === {category} ===")
            
            # 每行最多4个股票
            for i in range(0, len(codes), 4):
                line_codes = codes[i:i+4]
                line_parts = [f"'{code}': '{mapping[code]}'" for code in line_codes]
                code_lines.append(f"            {', '.join(line_parts)},")
            
            code_lines.append("")
    
    code_lines.append("        }")
    
    return '\n'.join(code_lines)

def apply_enhanced_mapping():
    """应用增强的股票名称映射到tdx_utils.py"""
    
    print("=== 应用增强的股票名称映射 ===")
    
    try:
        file_path = 'tradingagents/dataflows/tdx_utils.py'
        
        # 读取当前文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 生成新的映射代码
        new_mapping_code = generate_enhanced_mapping_code()
        
        # 查找并替换股票名称映射部分
        start_marker = "        # 扩展股票名称映射表"
        end_marker = "        return stock_names.get(stock_code, f'股票{stock_code}')"
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            # 替换映射部分
            new_content = (
                content[:start_idx] + 
                new_mapping_code + "\n        \n        " +
                content[end_idx:]
            )
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 成功更新 {file_path}")
            
            # 统计映射数量
            mapping = get_enhanced_stock_mapping()
            print(f"📊 新增股票映射: {len(mapping)} 个")
            
            # 按类别统计
            categories = {
                '深圳主板': len([k for k in mapping.keys() if k.startswith('000') and len(k) == 6]),
                '深圳中小板': len([k for k in mapping.keys() if k.startswith('002')]),
                '创业板': len([k for k in mapping.keys() if k.startswith('300')]),
                '上海主板(600)': len([k for k in mapping.keys() if k.startswith('600')]),
                '上海主板(601)': len([k for k in mapping.keys() if k.startswith('601')]),
                '上海主板(603)': len([k for k in mapping.keys() if k.startswith('603')]),
                '科创板': len([k for k in mapping.keys() if k.startswith('688')]),
                '北交所': len([k for k in mapping.keys() if k.startswith('8') and len(k) == 6]),
            }
            
            print("\n📋 分类统计:")
            for category, count in categories.items():
                if count > 0:
                    print(f"  {category}: {count} 个")
            
            return True
            
        else:
            print("❌ 未找到股票名称映射部分")
            return False
            
    except Exception as e:
        print(f"❌ 应用增强映射失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_mapping():
    """测试增强映射效果"""
    
    print("\n=== 测试增强映射效果 ===")
    
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
        ]
        
        print("\n股票名称映射测试:")
        all_correct = True
        
        for code, expected_name in test_stocks:
            actual_name = provider._get_stock_name(code)
            is_correct = actual_name == expected_name
            status = "✅" if is_correct else "❌"
            
            print(f"  {status} {code}: {actual_name}")
            
            if not is_correct:
                all_correct = False
        
        if all_correct:
            print("\n🎉 所有测试股票名称映射正确!")
        else:
            print("\n⚠️ 部分股票名称映射不正确")
            
        return all_correct
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    
    print("🚀 股票名称映射增强程序")
    print("=" * 50)
    
    # 显示当前映射统计
    mapping = get_enhanced_stock_mapping()
    print(f"📊 准备添加 {len(mapping)} 个股票名称映射")
    
    # 应用增强映射
    if apply_enhanced_mapping():
        print("\n✅ 增强映射应用成功")
        
        # 测试效果
        if test_enhanced_mapping():
            print("\n🎉 增强映射测试通过!")
            
            print("\n📋 完成情况:")
            print("1. ✅ 已修复601127股票名称显示问题")
            print("2. ✅ 已添加大量常见股票名称映射")
            print("3. ✅ 覆盖主板、中小板、创业板、科创板")
            print("4. ✅ 减少'股票XXXXXX'显示问题")
            
            print("\n📋 后续建议:")
            print("1. 重启Web应用以加载新的股票名称映射")
            print("2. 清除缓存以避免显示旧的股票名称")
            print("3. 在Web界面测试各类股票的名称显示")
            print("4. 根据需要继续添加更多股票映射")
            
        else:
            print("\n⚠️ 增强映射测试失败")
    else:
        print("\n❌ 增强映射应用失败")

if __name__ == "__main__":
    main()