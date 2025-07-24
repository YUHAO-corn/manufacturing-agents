#!/usr/bin/env python3
"""
真正调用大模型的预处理助手测试
"""

import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 加载环境变量
load_dotenv()

def build_preprocessing_prompt(user_input):
    """构建预处理助手的完整提示词（基于文档33）"""
    
    current_time_dt = datetime.strptime(user_input['current_time'], "%Y-%m-%d")
    current_year = current_time_dt.year
    current_month = current_time_dt.month
    
    # 动态生成时间范围示例
    news_example_start_month = current_month
    news_example_end_month = (current_month + 2) if (current_month + 2) <= 12 else (current_month + 2 - 12)
    news_time_range_example = f"{news_example_start_month}-{news_example_end_month}月"
    
    pmi_ppi_example_start_month = (current_month - 2) if (current_month - 2) > 0 else (current_month - 2 + 12)
    pmi_ppi_example_start_year = current_year if (current_month - 2) > 0 else (current_year - 1)
    pmi_ppi_time_range_example = f"{pmi_ppi_example_start_year}{pmi_ppi_example_start_month:02d}-{current_year}{current_month:02d}"
    
    # 动态生成期货合约示例
    cu_current_month_example = f"CU{current_year%100:02d}{current_month:02d}.SHF"
    cu_next_month_example = f"CU{current_year%100:02d}{((current_month)%12)+1:02d}.SHF"

    prompt = f"""你是制造业补货系统的参数预处理助手。你的任务是将用户输入转换为精确的API调度参数。

### 用户输入格式
系统会提供以下信息：
- 城市名称：{user_input['city_name']}
- 品牌名称：{user_input['brand_name']}  
- 产品类型：{user_input['product_type']}
- 特殊关注点：{user_input['special_focus']}
- **当前时间：{user_input['current_time']}**

### 你需要生成的参数

#### 1. 天气API参数
```json
{{
  "dailyForecast": true,
  "hourlyForecast": false,
  "nowcasting": false,
  "place": "标准城市名",
  "realtime": false
}}
```

#### 2. 新闻API参数
```json
{{
  "activity_query": "城市+时间范围+产品+促销活动",
  "area_news_query": "品牌+产品",
  "new_building_query": "城市+时间范围+新楼盘交付",
  "policy_query": "年份+时间范围+城市+产品大类+购买优惠政策"
}}
```

#### 3. 节假日API参数
```json
{{
  "start_date": "当前日期 YYYY-M-D格式",
  "end_date": "3个月后日期 YYYY-M-D格式"
}}
```

#### 4. PMI制造业采购经理指数
```json
{{
  "start_m": "最近3个月开始(YYYYMM)",
  "end_m": "当前月份(YYYYMM)",
  "fields": "month,pmi010000"
}}
```

#### 5. PPI工业生产者出厂价格指数
```json
{{
  "start_m": "最近3个月开始(YYYYMM)",
  "end_m": "当前月份(YYYYMM)",
  "fields": "month,ppi_yoy,ppi_mp"
}}
```

#### 6. 铜期货价格数据（简化版）
```json
{{
  "copper_futures": {{
    "current_month": "CU + 当前月合约代码",
    "next_month": "CU + 下月合约代码", 
    "freq": "week",
    "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
  }}
}}
```

### 处理规则

**城市名标准化**：
- "上海市浦东新区" → "上海"

**时间范围生成**：
- **基于当前时间`{user_input['current_time']}`进行计算**
- 新闻查询：当前月+未来2个月（如：`{user_input['current_time']}` → "{news_time_range_example}"）
- PMI/PPI查询：当前月-2到当前月（如：`{user_input['current_time']}` → "{pmi_ppi_time_range_example}"）

**产品抽象化**：
- "家用中央空调" → "家电"

**期货合约生成（简化策略）**：
- **基于当前时间`{user_input['current_time']}`进行计算**
- 当前月合约：{cu_current_month_example}（基准价格）
- 下月合约：{cu_next_month_example}（对比价格）  
- 趋势判断：通过价差分析未来价格预期

### 输出格式要求
严格按照JSON格式输出，包含所有6个API的参数。

### 完整示例
**输入**：
- 城市：{user_input['city_name']}
- 品牌：{user_input['brand_name']}  
- 产品：{user_input['product_type']}
- 关注点：{user_input['special_focus']}
- **当前时间：{user_input['current_time']}**

**输出示例**：
```json
{{
  "weather": {{
    "dailyForecast": true,
    "hourlyForecast": false,
    "nowcasting": false,
    "place": "上海",
    "realtime": false
  }},
  "news": {{
    "activity_query": "上海{news_time_range_example}有哪些厂商做家用中央空调促销活动",
    "area_news_query": "格力家用中央空调",
    "new_building_query": "上海{news_time_range_example}有哪些新楼盘交付",
    "policy_query": "{current_year}年{news_time_range_example}上海市家电购买优惠政策"
  }},
  "holiday": {{
    "start_date": "{user_input['current_time']}",
    "end_date": "{ (current_time_dt + timedelta(days=90)).strftime("%Y-%m-%d") }"
  }},
  "pmi": {{
    "start_m": "{pmi_ppi_time_range_example.split('-')[0]}",
    "end_m": "{pmi_ppi_time_range_example.split('-')[1]}",
    "fields": "month,pmi010000"
  }},
  "ppi": {{
    "start_m": "{pmi_ppi_time_range_example.split('-')[0]}", 
    "end_m": "{pmi_ppi_time_range_example.split('-')[1]}",
    "fields": "month,ppi_yoy,ppi_mp"
  }},
  "copper_futures": {{
    "current_month": "{cu_current_month_example}",
    "next_month": "{cu_next_month_example}",
    "freq": "week",
    "fields": "ts_code,trade_date,freq,open,high,low,close,vol,amount"
  }}
}}
```

请根据上述用户输入生成对应的API参数："""

    return prompt

def call_dashscope_api(prompt):
    """调用DashScope API"""
    try:
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            raise ValueError("未找到DASHSCOPE_API_KEY环境变量")
        
        dashscope.api_key = api_key
        
        print("🔄 调用DashScope API...")
        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            result_format='message'
        )
        
        print(f"🔍 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 获取内容
            content = response.output.choices[0]['message']['content']
            print(f"🤖 大模型原始输出: {content[:300]}...")
            
            # 解析JSON
            try:
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_str = content[json_start:json_end]
                    api_params = json.loads(json_str)
                    return api_params
                else:
                    raise ValueError("未找到JSON格式")
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {str(e)}")
                print(f"原始内容: {content}")
                return None
        else:
            print(f"❌ API调用失败: {response.message}")
            return None
            
    except Exception as e:
        print(f"❌ API调用异常: {str(e)}")
        return None

def validate_parameters(api_params):
    """验证API参数"""
    if not api_params:
        return False
        
    required_apis = ["weather", "news", "holiday", "pmi", "ppi", "copper_futures"]
    
    for api in required_apis:
        if api not in api_params:
            print(f"❌ 缺少API参数: {api}")
            return False
    
    print("✅ API参数格式验证通过")
    return True

def main():
    """主测试函数"""
    print("🚀 开始测试真实大模型调用...")
    
    # 测试用例
    test_input = {
        "city_name": "上海市浦东新区",
        "brand_name": "格力",
        "product_type": "家用中央空调",
        "special_focus": "极端天气影响",
        "current_time": "2025-09-15"
    }
    
    print(f"📋 测试输入: {test_input}")
    
    # 构建提示词
    prompt = build_preprocessing_prompt(test_input)
    print(f"📝 提示词长度: {len(prompt)} 字符")
    
    # 调用大模型
    api_params = call_dashscope_api(prompt)
    
    if api_params:
        print("\n✅ 大模型成功生成参数！")
        print("📊 生成的API参数:")
        print(json.dumps(api_params, ensure_ascii=False, indent=2))
        
        # 验证参数
        if validate_parameters(api_params):
            print("\n🎯 关键字段检查:")
            
            # 检查城市名标准化
            place = api_params.get("weather", {}).get("place", "")
            if place == "上海":
                print(f"  ✅ 城市名标准化正确: {place}")
            else:
                print(f"  ⚠️ 城市名标准化: {place} (期望: 上海)")
            
            # 检查PMI时间格式
            pmi_start = api_params.get("pmi", {}).get("start_m", "")
            if pmi_start == "202507" and len(pmi_start) == 6 and pmi_start.isdigit():
                print(f"  ✅ PMI时间格式正确: {pmi_start}")
            else:
                print(f"  ⚠️ PMI时间格式: {pmi_start} (期望: 202507)")
            
            # 检查期货合约
            current_month_contract = f"CU{25}{9:02d}.SHF"
            next_month_contract = f"CU{25}{(9%12)+1:02d}.SHF"

            llm_current_month = api_params.get("copper_futures", {}).get("current_month", "")
            llm_next_month = api_params.get("copper_futures", {}).get("next_month", "")
            
            if llm_current_month == current_month_contract and llm_next_month == next_month_contract:
                print(f"  ✅ 期货合约生成正确: {llm_current_month}, {llm_next_month}")
            else:
                print(f"  ⚠️ 期货合约生成: {llm_current_month}, {llm_next_month} (期望: {current_month_contract}, {next_month_contract})")
            
            print("\n🎉 真实大模型调用测试成功！")
            return True
        else:
            print("❌ 参数验证失败")
            return False
    else:
        print("❌ 大模型调用失败")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ 测试通过")
    else:
        print("❌ 测试失败")
        exit(1) 