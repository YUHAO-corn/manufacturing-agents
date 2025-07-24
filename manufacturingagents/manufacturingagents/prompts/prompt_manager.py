"""
制造业智能体提示词管理器

负责加载、管理和提供所有制造业智能体的提示词模板。
"""

import os
from typing import Dict, Optional
from pathlib import Path


class ManufacturingPromptManager:
    """制造业智能体提示词管理器"""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.prompts_cache: Dict[str, str] = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self):
        """加载所有提示词模板"""
        try:
            # 加载分析师提示词
            self.prompts_cache["market_environment_analyst"] = self._load_prompt("analysts/market_environment_analyst.txt")
            self.prompts_cache["trend_prediction_analyst"] = self._load_prompt("analysts/trend_prediction_analyst.txt")
            self.prompts_cache["news_analyst"] = self._load_prompt("analysts/news_analyst.txt")
            self.prompts_cache["sentiment_insight_analyst"] = self._load_prompt("analysts/sentiment_insight_analyst.txt")
            
            # 加载决策顾问提示词
            self.prompts_cache["optimistic_advisor"] = self._load_prompt("advisors/optimistic_advisor.txt")
            self.prompts_cache["cautious_advisor"] = self._load_prompt("advisors/cautious_advisor.txt")
            
            # 加载协调员和风险管理提示词
            self.prompts_cache["decision_coordinator"] = self._load_prompt("coordinator/decision_coordinator.txt")
            self.prompts_cache["risk_assessment"] = self._load_prompt("risk_mgmt/risk_assessment.txt")
            
            # 加载工具类提示词
            self.prompts_cache["preprocessing_assistant"] = self._load_prompt("utils/preprocessing_assistant.txt")
            self.prompts_cache["conclusion_extractor"] = self._load_prompt("utils/conclusion_extractor.txt")
            
        except Exception as e:
            print(f"加载提示词时发生错误: {e}")
    
    def _load_prompt(self, filename: str) -> str:
        """加载单个提示词文件"""
        try:
            file_path = self.current_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                print(f"提示词文件不存在: {file_path}")
                return ""
        except Exception as e:
            print(f"读取提示词文件 {filename} 时发生错误: {e}")
            return ""
    
    def get_prompt(self, agent_name: str) -> Optional[str]:
        """获取指定智能体的提示词"""
        return self.prompts_cache.get(agent_name)
    
    def update_prompt(self, agent_name: str, prompt_content: str):
        """更新指定智能体的提示词"""
        self.prompts_cache[agent_name] = prompt_content
    
    def get_all_prompts(self) -> Dict[str, str]:
        """获取所有提示词"""
        return self.prompts_cache.copy()


# 全局提示词管理器实例
prompt_manager = ManufacturingPromptManager() 