"""
进度跟踪器
用于在分析过程中提供详细的进度反馈
"""

import time
from typing import Optional, Callable, Dict, List
import streamlit as st

class AnalysisProgressTracker:
    """分析进度跟踪器"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.steps = []
        self.current_step = 0
        self.start_time = time.time()
        
        # 定义分析步骤
        self.analysis_steps = [
            {"name": "环境检查", "description": "验证API密钥和环境配置"},
            {"name": "参数配置", "description": "设置分析参数和模型配置"},
            {"name": "目录创建", "description": "创建必要的数据和结果目录"},
            {"name": "引擎初始化", "description": "初始化AI分析引擎"},
            {"name": "数据获取", "description": "获取股票价格和市场数据"},
            {"name": "技术分析", "description": "计算技术指标和趋势分析"},
            {"name": "基本面分析", "description": "分析财务数据和公司基本面"},
            {"name": "情绪分析", "description": "分析市场情绪和新闻影响"},
            {"name": "AI推理", "description": "AI模型进行综合分析和推理"},
            {"name": "结果整理", "description": "整理分析结果和生成报告"},
            {"name": "完成", "description": "分析完成"}
        ]
    
    def update(self, message: str, step: Optional[int] = None, total_steps: Optional[int] = None):
        """更新进度"""
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # 记录步骤
        self.steps.append({
            'message': message,
            'timestamp': current_time,
            'elapsed': elapsed_time
        })
        
        # 根据消息内容自动判断当前步骤
        if step is None:
            step = self._detect_step_from_message(message)
        
        if step is not None:
            self.current_step = step
        
        # 调用回调函数
        if self.callback:
            progress = self.current_step / len(self.analysis_steps) if len(self.analysis_steps) > 0 else 0
            self.callback(message, self.current_step, len(self.analysis_steps), progress, elapsed_time)
    
    def _detect_step_from_message(self, message: str) -> Optional[int]:
        """根据消息内容检测当前步骤"""
        message_lower = message.lower()
        
        if "环境" in message or "检查" in message:
            return 0
        elif "配置" in message or "参数" in message:
            return 1
        elif "目录" in message or "创建" in message:
            return 2
        elif "初始化" in message or "引擎" in message:
            return 3
        elif "获取" in message or "数据" in message:
            return 4
        elif "技术" in message or "指标" in message:
            return 5
        elif "基本面" in message or "财务" in message:
            return 6
        elif "情绪" in message or "新闻" in message:
            return 7
        elif "分析" in message and ("开始" in message or "进行" in message):
            return 8
        elif "整理" in message or "结果" in message:
            return 9
        elif "完成" in message:
            return 10
        
        return None
    
    def get_current_step_info(self) -> Dict:
        """获取当前步骤信息"""
        if self.current_step < len(self.analysis_steps):
            return self.analysis_steps[self.current_step]
        return {"name": "完成", "description": "分析已完成"}
    
    def get_progress_percentage(self) -> float:
        """获取进度百分比"""
        return (self.current_step / len(self.analysis_steps)) * 100 if len(self.analysis_steps) > 0 else 0
    
    def get_elapsed_time(self) -> float:
        """获取已用时间"""
        return time.time() - self.start_time
    
    def format_time(self, seconds: float) -> str:
        """格式化时间显示"""
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小时"

class StreamlitProgressDisplay:
    """Streamlit进度显示组件"""
    
    def __init__(self, container):
        self.container = container
        self.progress_bar = None
        self.status_text = None
        self.step_info = None
        self.time_info = None
        self.setup_display()
    
    def setup_display(self):
        """设置显示组件"""
        with self.container:
            st.markdown("### 🔄 分析进度")
            self.progress_bar = st.progress(0)
            self.status_text = st.empty()
            self.step_info = st.empty()
            self.time_info = st.empty()
    
    def update(self, message: str, current_step: int, total_steps: int, progress: float, elapsed_time: float):
        """更新显示"""
        # 更新进度条
        self.progress_bar.progress(progress)
        
        # 更新状态文本
        self.status_text.markdown(f"**当前状态:** {message}")
        
        # 更新步骤信息
        step_text = f"**进度:** 第 {current_step + 1} 步，共 {total_steps} 步 ({progress:.1%})"
        self.step_info.markdown(step_text)
        
        # 更新时间信息
        time_text = f"**已用时间:** {self._format_time(elapsed_time)}"
        if progress > 0:
            estimated_total = elapsed_time / progress
            remaining = estimated_total - elapsed_time
            time_text += f" | **预计剩余:** {self._format_time(remaining)}"
        
        self.time_info.markdown(time_text)
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间显示"""
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小时"
    
    def clear(self):
        """清除显示"""
        self.container.empty()

def create_progress_callback(display: StreamlitProgressDisplay) -> Callable:
    """创建进度回调函数"""
    tracker = AnalysisProgressTracker()
    
    def callback(message: str, step: Optional[int] = None, total_steps: Optional[int] = None):
        tracker.update(message, step, total_steps)
        
        current_step = tracker.current_step
        total_steps = len(tracker.analysis_steps)
        progress = tracker.get_progress_percentage() / 100
        elapsed_time = tracker.get_elapsed_time()
        
        display.update(message, current_step, total_steps, progress, elapsed_time)
    
    return callback
