#!/usr/bin/env python3
"""
制造业补货系统预处理助手
将用户输入转换为精确的API调度参数
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class PreprocessingAssistant:
    """
    预处理助手：将用户输入转换为API参数
    """
    
    # 类级别的参数缓存
    _global_params_cache = {}
    
    def __init__(self, model_provider: str = "dashscope"):
        """
        初始化预处理助手
        
        Args:
            model_provider: 模型提供商，支持 "dashscope" 或 "openai"
        """
        self.model_provider = model_provider
        self._init_llm_client()
    
    @classmethod
    def get_cached_params(cls, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        获取缓存的API参数
        
        Args:
            cache_key: 缓存键
            
        Returns:
            缓存的API参数，如果不存在则返回None
        """
        return cls._global_params_cache.get(cache_key)
    
    @classmethod
    def set_cached_params(cls, cache_key: str, params: Dict[str, Any]):
        """
        设置缓存的API参数
        
        Args:
            cache_key: 缓存键
            params: API参数
        """
        cls._global_params_cache[cache_key] = params
        print(f"✅ [CACHE] API参数已缓存: {cache_key}")
    
    @classmethod
    def clear_cache(cls):
        """清空所有缓存"""
        cls._global_params_cache.clear()
        print("🗑️ [CACHE] 已清空所有API参数缓存")
        
    def _init_llm_client(self):
        """初始化大模型客户端"""
        if self.model_provider == "dashscope":
            try:
                import dashscope
                self.api_key = os.getenv('DASHSCOPE_API_KEY')
                if not self.api_key:
                    raise ValueError("未找到DASHSCOPE_API_KEY环境变量")
                dashscope.api_key = self.api_key
                self.llm_client = dashscope
                print("✅ DashScope客户端初始化成功")
            except ImportError:
                raise ImportError("请安装dashscope: pip install dashscope")
        else:
            raise ValueError(f"不支持的模型提供商: {self.model_provider}")
    
    def generate_api_parameters(
        self, 
        city_name: str,
        brand_name: str, 
        product_type: str,
        special_focus: str = "",
        current_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        生成API调度参数
        
        Args:
            city_name: 城市名称
            brand_name: 品牌名称
            product_type: 产品类型
            special_focus: 特殊关注点
            current_time: 当前时间，如果为None则使用系统时间
            
        Returns:
            包含6个API参数的字典
        """
        if current_time is None:
            current_time = datetime.now()
        
        # 构建用户输入
        user_input = {
            "city_name": city_name,
            "brand_name": brand_name,
            "product_type": product_type,
            "special_focus": special_focus or "无特殊要求",
            "current_time": current_time.strftime("%Y-%m-%d")
        }
        
        # ✅ 优化：检查缓存
        cache_key = f"{city_name}_{brand_name}_{product_type}_{hash(special_focus or '')}"
        cached_params = self.get_cached_params(cache_key)
        
        if cached_params:
            print(f"✅ [CACHE] 使用缓存的API参数: {cache_key}")
            return cached_params
        
        print(f"🔄 开始处理用户输入: {user_input}")
        
        # 调用大模型生成参数
        try:
            api_params = self._call_llm_for_parameters(user_input)
            # 缓存生成的参数
            self.set_cached_params(cache_key, api_params)
            print("✅ API参数生成成功")
            return api_params
        except Exception as e:
            print(f"⚠️ 大模型调用失败，使用降级方案: {str(e)}")
            # 返回降级方案
            fallback_params = self._generate_fallback_parameters(user_input)
            # 也缓存降级方案
            self.set_cached_params(cache_key, fallback_params)
            return fallback_params
    
    def _call_llm_for_parameters(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """调用大模型生成API参数"""
        
        # 构建提示词
        prompt = self._build_prompt(user_input)
        
        if self.model_provider == "dashscope":
            from dashscope import Generation
            
            try:
                response = Generation.call(
                    model='qwen-turbo',
                    prompt=prompt,
                    result_format='message'
                )
                
                if response.status_code == 200:
                    # 正确的DashScope响应访问方式
                    llm_output = response.output.choices[0].message.content
                    print(f"🤖 大模型原始输出长度: {len(llm_output)} 字符")
                    print(f"🤖 大模型原始输出前500字符: {llm_output[:500]}")
                    
                    # 确保llm_output是字符串
                    if not isinstance(llm_output, str):
                        llm_output = str(llm_output)
                    
                    # 解析JSON输出
                    try:
                        # 提取JSON部分
                        json_start = llm_output.find('{')
                        json_end = llm_output.rfind('}') + 1
                        print(f"🔍 JSON起始位置: {json_start}, 结束位置: {json_end}")
                        
                        if json_start != -1 and json_end != -1:
                            json_str = llm_output[json_start:json_end]
                            print(f"🔍 提取的JSON字符串长度: {len(json_str)}")
                            print(f"🔍 提取的JSON前200字符: {json_str[:200]}")
                            
                            api_params = json.loads(json_str)
                            print("✅ JSON解析成功")
                            return api_params
                        else:
                            raise ValueError("大模型输出中未找到有效JSON")
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON解析失败: {str(e)}")
                        print(f"❌ 完整原始输出:")
                        print("-" * 50)
                        print(llm_output)
                        print("-" * 50)
                        raise ValueError(f"大模型输出JSON解析失败: {str(e)}")
                else:
                    error_msg = getattr(response, 'message', f'状态码: {response.status_code}')
                    raise ValueError(f"大模型调用失败: {error_msg}")
                    
            except Exception as e:
                if "JSON" in str(e):
                    # JSON解析错误，重新抛出
                    raise e
                else:
                    # API调用错误，包装一下
                    raise ValueError(f"DashScope API调用异常: {str(e)}")
        
        raise ValueError("未实现的模型提供商")
    
    def _build_prompt(self, user_input: Dict[str, Any]) -> str:
        """构建大模型提示词（使用提示词管理器）"""
        from ..prompts.prompt_manager import prompt_manager
        
        # 从提示词管理器获取模板
        prompt_template = prompt_manager.get_prompt("preprocessing_assistant")
        
        if not prompt_template:
            raise ValueError("无法加载预处理助手提示词模板")
        
        # 格式化用户输入
        formatted_prompt = prompt_template.format(
            city_name=user_input['city_name'],
            brand_name=user_input['brand_name'],
            product_type=user_input['product_type'],
            special_focus=user_input['special_focus'],
            current_time=user_input['current_time']
        )
        
        return formatted_prompt
    
    def _generate_fallback_parameters(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """生成降级方案参数"""
        print("🔄 使用降级方案生成参数...")
        
        current_time = datetime.strptime(user_input['current_time'], "%Y-%m-%d")
        
        # 城市名标准化（简单去后缀）
        city = user_input['city_name']
        for suffix in ['省', '市', '区', '县']:
            city = city.replace(suffix, '')
        
        # 时间计算
        current_month = current_time.month
        current_year = current_time.year
        
        # 新闻时间范围（当前月+2个月）
        end_month = current_month + 2
        if end_month > 12:
            end_month -= 12
        news_time_range = f"{current_month}-{end_month}月"
        
        # PMI/PPI时间范围（最近3个月，考虑数据发布延迟）
        # 数据通常延迟1个月发布，所以7月获取4、5、6月数据
        latest_data_month = current_month - 1  # 最新数据月份
        start_month = latest_data_month - 2    # 往前推2个月，总共3个月
        if start_month <= 0:
            start_month += 12
            start_year = current_year - 1
        else:
            start_year = current_year
        
        # 确保end_month是最新数据月份
        end_month = latest_data_month
        end_year = current_year
        if end_month <= 0:
            end_month += 12
            end_year = current_year - 1
        
        # 产品抽象化
        product = user_input['product_type']
        if any(word in product for word in ['空调', '冰箱', '洗衣机']):
            product_category = "家电"
        elif any(word in product for word in ['手机', '电脑', '平板']):
            product_category = "数码产品"
        elif any(word in product for word in ['汽车', '车']):
            product_category = "汽车"
        else:
            product_category = "家电"  # 默认
        
        # 期货合约代码
        current_contract = f"CU{current_year%100:02d}{current_month:02d}.SHF"
        next_month_contract = f"CU{current_year%100:02d}{(current_month%12)+1:02d}.SHF"
        
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
                "end_m": f"{end_year}{end_month:02d}",
                "fields": "month,pmi010000"
            },
            "ppi": {
                "start_m": f"{start_year}{start_month:02d}",
                "end_m": f"{end_year}{end_month:02d}",
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
    
    def validate_parameters(self, api_params: Dict[str, Any]) -> bool:
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