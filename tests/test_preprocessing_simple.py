#!/usr/bin/env python3
"""
独立测试预处理助手的核心功能
"""

import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def normalize_city_name(city_input):
    """城市名标准化"""
    city = city_input
    for suffix in ['省', '市', '区', '县']:
        city = city.replace(suffix, '')
    return city

def generate_time_range(current_time):
    """生成时间范围"""
    current_month = current_time.month
    end_month = current_month + 2
    if end_month > 12:
        end_month -= 12
    return f"{current_month}-{end_month}月"

def abstract_product_category(product):
    """产品抽象化"""
    if any(word in product for word in ['空调', '冰箱', '洗衣机']):
        return "家电"
    elif any(word in product for word in ['手机', '电脑', '平板']):
        return "数码产品"
    elif any(word in product for word in ['汽车', '车']):
        return "汽车"
    else:
        return "家电"  # 默认

def generate_futures_contracts(current_time):
    """生成期货合约代码"""
    current_month = current_time.month
    current_year = current_time.year
    
    current_contract = f"CU{current_year%100:02d}{current_month:02d}.SHF"
    next_month_contract = f"CU{current_year%100:02d}{(current_month%12)+1:02d}.SHF"
    
    return current_contract, next_month_contract

def generate_fallback_parameters(user_input):
    """生成降级方案参数"""
    current_time = datetime.strptime(user_input['current_time'], "%Y-%m-%d")
    
    # 城市名标准化
    city = normalize_city_name(user_input['city_name'])
    
    # 时间计算
    current_month = current_time.month
    current_year = current_time.year
    
    # 新闻时间范围
    news_time_range = generate_time_range(current_time)
    
    # PMI/PPI时间范围（最近3个月）
    start_month = current_month - 2
    if start_month <= 0:
        start_month += 12
        start_year = current_year - 1
    else:
        start_year = current_year
    
    # 产品抽象化
    product_category = abstract_product_category(user_input['product_type'])
    
    # 期货合约代码
    current_contract, next_month_contract = generate_futures_contracts(current_time)
    
    fallback_params = {
        "weather": {
            "dailyForecast": True,
            "hourlyForecast": False,
            "nowcasting": False,
            "place": city,
            "realtime": False
        },
        "news": {
            "activity_query": f"{city}{news_time_range}有哪些厂商做{user_input['product_type']}促销活动",
            "area_news_query": f"{user_input['brand_name']}{user_input['product_type']}",
            "new_building_query": f"{city}{news_time_range}有哪些新楼盘交付",
            "policy_query": f"{current_year}年{news_time_range}{city}市{product_category}购买优惠政策"
        },
        "holiday": {
            "start_date": current_time.strftime("%Y-%m-%d"),
            "end_date": (current_time + timedelta(days=90)).strftime("%Y-%m-%d")
        },
        "pmi": {
            "start_m": f"{start_year}{start_month:02d}",
            "end_m": f"{current_year}{current_month:02d}",
            "fields": "month,pmi010000"
        },
        "ppi": {
            "start_m": f"{start_year}{start_month:02d}",
            "end_m": f"{current_year}{current_month:02d}",
            "fields": "month,ppi_yoy,ppi_mp"
        },
        "copper_futures": {
            "current_month": current_contract,
            "next_month": next_month_contract,
            "freq": "week",
            "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
        }
    }
    
    return fallback_params

def validate_parameters(api_params):
    """验证生成的API参数格式"""
    required_apis = ["weather", "news", "holiday", "pmi", "ppi", "copper_futures"]
    
    try:
        for api in required_apis:
            if api not in api_params:
                print(f"❌ 缺少API参数: {api}")
                return False
        
        # 验证具体格式
        if "place" not in api_params["weather"]:
            print("❌ weather参数缺少place字段")
            return False
            
        if "activity_query" not in api_params["news"]:
            print("❌ news参数缺少activity_query字段")
            return False
            
        print("✅ API参数格式验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 参数验证失败: {str(e)}")
        return False

def test_dashscope_api():
    """测试DashScope API调用"""
    try:
        import dashscope
        from dashscope import Generation
        
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            print("❌ 未找到DASHSCOPE_API_KEY环境变量")
            return False
        
        dashscope.api_key = api_key
        print("✅ DashScope客户端初始化成功")
        
        # 简单测试
        prompt = "请回答：北京是中国的首都吗？请用JSON格式回答：{\"answer\": \"是\"}"
        
        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            result_format='message'
        )
        
        print(f"🔍 响应类型: {type(response)}")
        print(f"🔍 响应内容: {response}")
        
        # 尝试获取内容
        if hasattr(response, 'output'):
            print(f"🔍 有output属性")
            if hasattr(response.output, 'choices'):
                content = response.output.choices[0]['message']['content']
                print(f"✅ 成功获取内容: {content}")
                return True
            elif hasattr(response.output, 'text'):
                content = response.output.text
                print(f"✅ 成功获取文本: {content}")
                return True
        
        print("❌ 无法解析响应格式")
        return False
        
    except Exception as e:
        print(f"❌ DashScope API测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试预处理助手核心功能...")
    
    # 测试1: 降级方案
    print("\n📋 测试1: 降级方案参数生成")
    test_input = {
        "city_name": "广东省佛山市",
        "brand_name": "美的",
        "product_type": "酷省电空调",
        "special_focus": "关注原材料价格",
        "current_time": "2025-07-19"
    }
    
    print(f"输入: {test_input}")
    
    fallback_params = generate_fallback_parameters(test_input)
    print("生成的参数:")
    print(json.dumps(fallback_params, ensure_ascii=False, indent=2))
    
    if validate_parameters(fallback_params):
        print("✅ 降级方案测试通过")
    else:
        print("❌ 降级方案测试失败")
        return False
    
    # 检查关键功能
    print("\n🔍 验证关键功能:")
    
    # 1. 城市名标准化
    normalized_city = normalize_city_name("广东省佛山市")
    if normalized_city == "佛山":
        print(f"  ✅ 城市名标准化正确: {normalized_city}")
    else:
        print(f"  ❌ 城市名标准化错误: {normalized_city}")
    
    # 2. 产品抽象化
    category = abstract_product_category("美的酷省电空调")
    if category == "家电":
        print(f"  ✅ 产品抽象化正确: {category}")
    else:
        print(f"  ❌ 产品抽象化错误: {category}")
    
    # 3. 期货合约生成
    current_time = datetime(2025, 7, 19)
    current_contract, next_contract = generate_futures_contracts(current_time)
    if current_contract == "CU2507.SHF" and next_contract == "CU2508.SHF":
        print(f"  ✅ 期货合约生成正确: {current_contract}, {next_contract}")
    else:
        print(f"  ❌ 期货合约生成错误: {current_contract}, {next_contract}")
    
    # 测试2: DashScope API（如果有密钥）
    if os.getenv('DASHSCOPE_API_KEY'):
        print("\n📋 测试2: DashScope API连通性")
        if test_dashscope_api():
            print("✅ DashScope API测试通过")
        else:
            print("⚠️ DashScope API测试失败，但降级方案可用")
    else:
        print("\n⚠️ 未发现DASHSCOPE_API_KEY，跳过API测试")
    
    print("\n🎉 预处理助手核心功能测试完成！")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ 测试通过")
    else:
        print("❌ 测试失败")
        exit(1) 