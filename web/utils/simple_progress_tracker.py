"""
简化进度追踪器
Simple Progress Tracker

为制造业智能体分析过程提供进度展示和日志记录功能
"""

import datetime
from typing import Optional, List, Dict, Any
import streamlit as st


class SimpleProgressTracker:
    """简化的进度追踪器"""
    
    def __init__(self, progress_bar, status_display, log_display):
        """
        初始化进度追踪器
        
        Args:
            progress_bar: Streamlit进度条组件
            status_display: Streamlit状态文本显示组件
            log_display: Streamlit日志显示组件
        """
        self.progress_bar = progress_bar
        self.status_display = status_display
        self.log_display = log_display
        self.logs: List[str] = []
        self.current_step = 0
        self.total_steps = 7
        self.start_time = datetime.datetime.now()
        
        # 🎯 生成更加唯一的ID避免key冲突 - 使用时间戳+UUID+随机数
        import uuid
        import random
        import time
        timestamp = str(int(time.time() * 1000))[-6:]  # 时间戳后6位
        uuid_part = str(uuid.uuid4())[:8]
        random_part = str(random.randint(1000, 9999))
        self.unique_id = f"{timestamp}_{uuid_part}_{random_part}"
        
        # 定义分析步骤
        self.step_names = [
            "市场环境分析师",      # 14%
            "趋势预测分析师",      # 28% 
            "行业资讯分析师",      # 42%
            "消费者洞察分析师",    # 56%
            "决策辩论阶段",        # 70%
            "决策协调阶段",        # 85%
            "风险评估完成"         # 100%
        ]
        
        # 事件图标映射
        self.event_icons = {
            "think": "💭",      # 智能体思考
            "action": "🔧",     # 工具调用/API调用
            "success": "✅",    # 成功完成
            "error": "❌",      # 错误/失败
            "start": "🚀",      # 开始阶段
            "progress": "📊",   # 进度更新
            "debate": "🎭",     # 辩论过程
            "decision": "⚖️",   # 决策过程
            "risk": "⚠️",      # 风险评估
            "complete": "🎉"    # 全部完成
        }
    
    def log_event(self, event_type: str, message: str) -> None:
        """
        记录事件日志
        
        Args:
            event_type: 事件类型（think, action, success, error等）
            message: 事件消息
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        icon = self.event_icons.get(event_type, '📝')
        log_entry = f"[{timestamp}] {icon} {message}"
        
        self.logs.append(log_entry)
        self._update_log_display()
    
    def update_progress(self, step: int, total_steps: Optional[int] = None) -> None:
        """
        更新进度
        
        Args:
            step: 当前步骤（1-based）
            total_steps: 总步骤数（可选）
        """
        if total_steps:
            self.total_steps = total_steps
            
        self.current_step = step
        progress = step / self.total_steps
        
        # 更新进度条
        self.progress_bar.progress(progress)
        
        # 更新状态文本
        current_step_name = self.step_names[min(step-1, len(self.step_names)-1)] if step > 0 else "准备开始"
        elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()
        
        status_text = f"进度: {step}/{self.total_steps} ({progress*100:.0f}%) - {current_step_name}"
        if elapsed_time > 10:  # 显示耗时（超过10秒才显示）
            status_text += f" | 耗时: {elapsed_time:.0f}秒"
            
        self.status_display.text(status_text)
        
        # 记录进度日志
        self.log_event("progress", f"进入阶段 {step}/{self.total_steps}: {current_step_name}")
    
    def log_agent_start(self, agent_name: str) -> None:
        """记录智能体开始工作"""
        self.log_event("start", f"{agent_name}启动")
    
    def log_agent_thinking(self, agent_name: str, thought: str) -> None:
        """记录智能体思考过程"""
        self.log_event("think", f"{agent_name}：{thought}")
    
    def log_api_call(self, api_name: str, status: str = "调用中") -> None:
        """记录API调用"""
        self.log_event("action", f"调用API：{api_name} -> {status}")
    
    def log_agent_complete(self, agent_name: str, result_summary: str = "") -> None:
        """记录智能体完成工作"""
        message = f"{agent_name}分析完成"
        if result_summary:
            message += f"，{result_summary}"
        self.log_event("success", message)
    
    def log_debate_round(self, advisor_type: str, round_num: int) -> None:
        """记录辩论轮次"""
        self.log_event("debate", f"{advisor_type}决策顾问发言（第{round_num}轮）")
    
    def log_decision_phase(self, phase: str) -> None:
        """记录决策阶段"""
        self.log_event("decision", f"决策阶段：{phase}")
    
    def log_risk_assessment(self, risk_level: str) -> None:
        """记录风险评估"""
        self.log_event("risk", f"风险评估：{risk_level}风险")
    
    def log_analysis_complete(self) -> None:
        """记录分析完成"""
        elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()
        self.log_event("complete", f"制造业补货分析完成！总耗时: {elapsed_time:.0f}秒")
        self.update_progress(self.total_steps)
    
    def log_error(self, error_message: str) -> None:
        """记录错误信息"""
        self.log_event("error", f"错误：{error_message}")
    
    def _update_log_display(self) -> None:
        """更新日志显示 - 聊天窗口体验"""
        try:
            # 🎯 智能显示策略：确保最新消息始终可见
            # 600px高度大约能显示25行，我们显示最近20条确保有缓冲
            recent_logs = self.logs[-20:] if len(self.logs) > 20 else self.logs
            
            if recent_logs:
                # 🎯 聊天窗口体验：最老消息在顶部，最新消息在底部且可见
                log_text = f"📋 分析进度 (最新{len(recent_logs)}/{len(self.logs)}条)\n{'='*50}\n"
                log_text += "\n".join(recent_logs)
                log_text += f"\n{'='*50}\n📍 最新消息 ↑"
            else:
                log_text = "🔄 准备开始分析..."
            
            # 🎯 使用更强健的唯一键策略 - 包含日志数量避免缓存问题
            log_key = f"progress_log_{self.unique_id}_{len(self.logs)}"
            
            self.log_display.text_area(
                label="分析日志",
                value=log_text,
                height=600,  # 🎯 修复1: 增加一倍高度 
                disabled=True,
                key=log_key,  # 🎯 修复2: 使用动态key，包含日志数量
                label_visibility="collapsed"  # 🎯 修复3: 隐藏label避免重复显示
            )
        except Exception as e:
            # 🎯 如果出现键冲突，使用fallback显示
            import streamlit as st
            try:
                # 🎯 fallback也显示多条消息，不只是最后一条
                recent_logs = self.logs[-10:] if len(self.logs) > 10 else self.logs
                if recent_logs:
                    fallback_text = f"📋 分析进度 (最新{len(recent_logs)}/{len(self.logs)}条)\n"
                    fallback_text += "=" * 40 + "\n"
                    fallback_text += "\n".join(recent_logs)
                    fallback_text += "\n" + "=" * 40 + "\n📍 最新消息 ↑"
                else:
                    fallback_text = "🔄 准备开始分析..."
                
                # 使用动态key避免冲突
                fallback_key = f"fallback_log_{self.unique_id}_{len(self.logs)}"
                self.log_display.text_area(
                    label="分析日志",
                    value=fallback_text,
                    height=600,
                    disabled=True,
                    key=fallback_key,
                    label_visibility="collapsed"
                )
            except:
                # 最后的fallback：至少显示基本信息
                self.log_display.text(f"📋 分析进度 (共{len(self.logs)}条日志)\n⚠️ 日志显示异常，请刷新页面")
    
    def get_current_status(self) -> Dict[str, Any]:
        """获取当前状态信息"""
        return {
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "progress_percentage": (self.current_step / self.total_steps) * 100,
            "current_phase": self.step_names[min(self.current_step-1, len(self.step_names)-1)] if self.current_step > 0 else "准备开始",
            "elapsed_time": (datetime.datetime.now() - self.start_time).total_seconds(),
            "total_logs": len(self.logs)
        }
    
    def clear_logs(self) -> None:
        """清空日志"""
        self.logs.clear()
        self._update_log_display()
    
    def __call__(self, message: str, step: Optional[int] = None, total_steps: Optional[int] = None) -> None:
        """
        兼容原有progress_callback接口
        
        Args:
            message: 进度消息
            step: 当前步骤
            total_steps: 总步骤数
        """
        if step is not None:
            self.update_progress(step, total_steps)
        else:
            self.log_event("progress", message)


class ProgressTrackerFactory:
    """进度追踪器工厂类"""
    
    @staticmethod
    def create_tracker(progress_bar, status_display, log_display) -> SimpleProgressTracker:
        """创建进度追踪器实例"""
        return SimpleProgressTracker(progress_bar, status_display, log_display)
    
    @staticmethod
    def create_temp_tracker() -> None:
        """创建临时追踪器（用于测试）"""
        # 创建虚拟的Streamlit组件
        progress_bar = st.progress(0)
        status_display = st.empty()
        log_display = st.empty()
        
        return SimpleProgressTracker(progress_bar, status_display, log_display) 