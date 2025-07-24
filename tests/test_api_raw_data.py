#!/usr/bin/env python3
"""
API原始数据测试脚本
获取所有6个API的原始数据并保存到文件中供检查
"""

import os
import sys
import json
import requests
from datetime import datetime

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), 'TradingAgents-CN')
sys.path.insert(0, project_root)

# 加载.env文件
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))

def test_and_save_raw_data():
    """测试所有API并保存原始数据"""
    
    print("🔍 测试所有API并获取原始数据")
    print("=" * 80)
    
    # 检查API密钥
    coze_api_key = os.getenv('COZE_API_KEY')
    tushare_token = os.getenv('TUSHARE_TOKEN')
    
    if not coze_api_key:
        print("❌ COZE_API_KEY未配置")
        return
    if not tushare_token:
        print("❌ TUSHARE_TOKEN未配置")
        return
    
    print("✅ API密钥配置检查通过")
    
    # 初始化预处理助手获取参数
    try:
        from manufacturingagents.manufacturingagents.utils.preprocessing_assistant import PreprocessingAssistant
        assistant = PreprocessingAssistant(model_provider="dashscope")
        
        # 生成API参数
        api_params = assistant.generate_api_parameters(
            city_name="广州市",
            brand_name="美的", 
            product_type="空调",
            special_focus="关注天气影响"
        )
        print("✅ API参数生成成功")
        
    except Exception as e:
        print(f"❌ 参数生成失败: {e}")
        return
    
    # 创建输出文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"api_raw_data_{timestamp}.txt"
    
    results = {}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("制造业补货系统 - 6个API原始数据测试报告\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 100 + "\n\n")
        
        # 1. 测试Coze天气API
        print("\n🌤️ 测试Coze天气API...")
        f.write("1. Coze天气API (工作流ID: 7528239823611281448)\n")
        f.write("-" * 60 + "\n")
        f.write(f"发送参数: {json.dumps(api_params['weather'], ensure_ascii=False, indent=2)}\n\n")
        
        try:
            headers = {
                "Authorization": f"Bearer {coze_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "workflow_id": "7528239823611281448",
                "parameters": api_params['weather']
            }
            response = requests.post("https://api.coze.cn/v1/workflow/run", headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                f.write("API调用状态: ✅ 成功\n")
                f.write(f"响应代码: {result.get('code', 'N/A')}\n")
                f.write(f"响应消息: {result.get('msg', 'N/A')}\n\n")
                
                if result.get('code') == 0:
                    data_str = result.get('data', '{}')
                    if isinstance(data_str, str):
                        data = json.loads(data_str)
                    else:
                        data = data_str
                    
                    f.write("原始数据结构:\n")
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))
                    f.write("\n\n")
                    
                    results['weather'] = {'success': True, 'data_keys': list(data.keys()), 'data_size': len(str(data))}
                    print(f"✅ 天气API成功 - 数据大小: {len(str(data))} 字符")
                else:
                    f.write(f"❌ API返回错误: {result}\n\n")
                    results['weather'] = {'success': False, 'error': str(result)}
            else:
                f.write(f"❌ HTTP错误: {response.status_code} - {response.text}\n\n")
                results['weather'] = {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            f.write(f"❌ 调用异常: {str(e)}\n\n")
            results['weather'] = {'success': False, 'error': str(e)}
        
        # 2. 测试Coze新闻API
        print("\n📰 测试Coze新闻API...")
        f.write("2. Coze新闻API (工作流ID: 7528253601837481984)\n")
        f.write("-" * 60 + "\n")
        f.write(f"发送参数: {json.dumps(api_params['news'], ensure_ascii=False, indent=2)}\n\n")
        
        try:
            payload = {
                "workflow_id": "7528253601837481984",
                "parameters": api_params['news']
            }
            response = requests.post("https://api.coze.cn/v1/workflow/run", headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                f.write("API调用状态: ✅ 成功\n")
                f.write(f"响应代码: {result.get('code', 'N/A')}\n\n")
                
                if result.get('code') == 0:
                    data_str = result.get('data', '{}')
                    if isinstance(data_str, str):
                        data = json.loads(data_str)
                    else:
                        data = data_str
                    
                    f.write("原始数据结构:\n")
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))
                    f.write("\n\n")
                    
                    results['news'] = {'success': True, 'data_keys': list(data.keys()), 'data_size': len(str(data))}
                    print(f"✅ 新闻API成功 - 数据大小: {len(str(data))} 字符")
                else:
                    f.write(f"❌ API返回错误: {result}\n\n")
                    results['news'] = {'success': False, 'error': str(result)}
            else:
                f.write(f"❌ HTTP错误: {response.status_code}\n\n")
                results['news'] = {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            f.write(f"❌ 调用异常: {str(e)}\n\n")
            results['news'] = {'success': False, 'error': str(e)}
        
        # 3. 测试Coze节假日API
        print("\n📅 测试Coze节假日API...")
        f.write("3. Coze节假日API (工作流ID: 7528250308326260762)\n")
        f.write("-" * 60 + "\n")
        f.write(f"发送参数: {json.dumps(api_params['holiday'], ensure_ascii=False, indent=2)}\n\n")
        
        try:
            payload = {
                "workflow_id": "7528250308326260762",
                "parameters": api_params['holiday']
            }
            response = requests.post("https://api.coze.cn/v1/workflow/run", headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                f.write("API调用状态: ✅ 成功\n")
                f.write(f"响应代码: {result.get('code', 'N/A')}\n\n")
                
                if result.get('code') == 0:
                    data_str = result.get('data', '{}')
                    if isinstance(data_str, str):
                        data = json.loads(data_str)
                    else:
                        data = data_str
                    
                    f.write("原始数据结构:\n")
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))
                    f.write("\n\n")
                    
                    results['holiday'] = {'success': True, 'data_keys': list(data.keys()), 'data_size': len(str(data))}
                    print(f"✅ 节假日API成功 - 数据大小: {len(str(data))} 字符")
                else:
                    f.write(f"❌ API返回错误: {result}\n\n")
                    results['holiday'] = {'success': False, 'error': str(result)}
            else:
                f.write(f"❌ HTTP错误: {response.status_code}\n\n")
                results['holiday'] = {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            f.write(f"❌ 调用异常: {str(e)}\n\n")
            results['holiday'] = {'success': False, 'error': str(e)}
        
        # 4-6. 测试TuShare API
        tushare_apis = [
            ("PMI", "pmi", "PMI制造业采购经理指数"),
            ("PPI", "ppi", "PPI工业生产者价格指数"), 
            ("期货", "copper_futures", "铜期货价格数据")
        ]
        
        for api_name, param_key, description in tushare_apis:
            print(f"\n📈 测试TuShare {api_name} API...")
            f.write(f"{4 + tushare_apis.index((api_name, param_key, description))}. TuShare {api_name} API - {description}\n")
            f.write("-" * 60 + "\n")
            f.write(f"发送参数: {json.dumps(api_params[param_key], ensure_ascii=False, indent=2)}\n\n")
            
            try:
                import tushare as ts
                ts.set_token(tushare_token)
                pro = ts.pro_api()
                
                if api_name == "PMI":
                    # PMI数据 - 使用正确的cn_pmi接口
                    result = pro.cn_pmi(
                        start_m=api_params[param_key].get('start_m', '202505'),
                        end_m=api_params[param_key].get('end_m', '202507'),
                        fields=api_params[param_key].get('fields', 'month,pmi010000')
                    )
                elif api_name == "PPI":
                    # PPI数据 - 使用正确的cn_ppi接口
                    result = pro.cn_ppi(
                        start_m=api_params[param_key].get('start_m', '202505'),
                        end_m=api_params[param_key].get('end_m', '202507'),
                        fields=api_params[param_key].get('fields', 'month,ppi_yoy,ppi_mp')
                    )
                elif api_name == "期货":
                    # 期货数据 - 分别获取当月和下月合约
                    current_month = api_params[param_key].get('current_month', 'CU2507.SHF')
                    next_month = api_params[param_key].get('next_month', 'CU2508.SHF')
                    
                    # 获取当月合约数据
                    result_current = pro.fut_weekly_monthly(
                        ts_code=current_month,
                        freq='week',
                        fields='ts_code,trade_date,close'
                    ).head(5)  # 最近5周
                    
                    # 获取下月合约数据  
                    result_next = pro.fut_weekly_monthly(
                        ts_code=next_month,
                        freq='week',
                        fields='ts_code,trade_date,close'
                    ).head(5)  # 最近5周
                    
                    # 合并两个DataFrame
                    import pandas as pd
                    result = pd.concat([result_current, result_next], ignore_index=True)
                
                f.write(f"API调用状态: ✅ 成功\n")
                f.write(f"数据形状: {result.shape if hasattr(result, 'shape') else 'N/A'}\n")
                f.write(f"数据列名: {list(result.columns) if hasattr(result, 'columns') else 'N/A'}\n\n")
                f.write("原始数据内容:\n")
                f.write(str(result))
                f.write("\n\n")
                
                record_count = len(result) if hasattr(result, '__len__') else 1
                results[param_key] = {'success': True, 'records': record_count, 'columns': list(result.columns) if hasattr(result, 'columns') else []}
                print(f"✅ {api_name} API成功 - {record_count} 条记录")
                
            except ImportError:
                f.write("❌ tushare包未安装\n\n")
                results[param_key] = {'success': False, 'error': 'tushare not installed'}
            except Exception as e:
                f.write(f"❌ 调用异常: {str(e)}\n\n")
                results[param_key] = {'success': False, 'error': str(e)}
        
        # 写入总结
        f.write("=" * 100 + "\n")
        f.write("测试总结\n")
        f.write("=" * 100 + "\n")
        for api_name, result in results.items():
            if result['success']:
                if 'records' in result:
                    f.write(f"{api_name}: ✅ 成功 - {result['records']} 条记录\n")
                else:
                    f.write(f"{api_name}: ✅ 成功 - {result['data_size']} 字符\n")
            else:
                f.write(f"{api_name}: ❌ 失败 - {result['error']}\n")
    
    print(f"\n✅ 原始数据测试完成")
    print(f"📄 详细数据已保存到: {output_file}")
    print("\n📊 数据概览:")
    
    for api_name, result in results.items():
        if result['success']:
            if 'records' in result:
                print(f"  {api_name}: ✅ {result['records']} 条记录")
            else:
                print(f"  {api_name}: ✅ {result['data_size']} 字符")
        else:
            print(f"  {api_name}: ❌ 失败")
    
    return output_file

if __name__ == "__main__":
    output_file = test_and_save_raw_data()
    
    print("\n🔍 请检查输出文件中的原始数据内容")
    print("📝 重点关注:")
    print("  1. PMI/PPI数据的实际记录数量是否合理")
    print("  2. 数据格式是否适合智能体分析")
    print("  3. 是否存在冗余或重复数据")
    print("  4. 上下文长度是否影响智能体工作") 