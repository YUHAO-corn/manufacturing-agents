# 风险管理智能体

## 概述

风险管理智能体是 TradingAgents 框架的安全守护者，负责识别、评估和控制投资风险。通过多层次的风险评估机制，确保交易决策在可接受的风险范围内，保护投资组合免受重大损失。

## 风险管理架构

### 风险管理体系

```python
class RiskManagementSystem:
    """风险管理系统 - 统筹所有风险管理活动"""
    
    def __init__(self, config):
        self.config = config
        self.risk_assessors = self._initialize_risk_assessors()
        self.risk_monitor = RiskMonitor()
        self.risk_controller = RiskController()
        
    def _initialize_risk_assessors(self):
        """初始化风险评估智能体"""
        return {
            "aggressive": AggressiveRiskAssessor(self.config),
            "conservative": ConservativeRiskAssessor(self.config),
            "neutral": NeutralRiskAssessor(self.config)
        }
    
    def assess_trading_risk(self, trading_decision: Dict, market_data: Dict) -> Dict:
        """评估交易风险"""
        
        # 1. 多角度风险评估
        risk_assessments = {}
        for assessor_type, assessor in self.risk_assessors.items():
            risk_assessments[assessor_type] = assessor.assess_risk(
                trading_decision, market_data
            )
        
        # 2. 综合风险评估
        consolidated_risk = self._consolidate_risk_assessments(risk_assessments)
        
        # 3. 风险等级分类
        risk_classification = self._classify_risk_level(consolidated_risk)
        
        # 4. 风险控制建议
        control_recommendations = self._generate_control_recommendations(
            consolidated_risk, risk_classification
        )
        
        return {
            "individual_assessments": risk_assessments,
            "consolidated_risk": consolidated_risk,
            "risk_classification": risk_classification,
            "control_recommendations": control_recommendations,
            "approval_status": self._determine_approval_status(risk_classification)
        }
```

## 1. 激进风险评估智能体

### 特点与职责
```python
class AggressiveRiskAssessor:
    """激进风险评估 - 支持高风险高收益策略"""
    
    def __init__(self, config):
        self.config = config
        self.risk_appetite = "high"
        self.return_focus = "high"
        
    专业特点:
    - 高风险容忍度
    - 关注收益最大化
    - 支持杠杆使用
    - 鼓励机会把握
    
    评估重点:
    - 收益潜力分析
    - 机会成本评估
    - 市场时机把握
    - 竞争优势利用
```

### 风险评估方法
```python
def assess_risk(self, trading_decision: Dict, market_data: Dict) -> Dict:
    """激进角度的风险评估"""
    
    # 基础风险指标
    base_risk_metrics = self._calculate_base_risk_metrics(trading_decision, market_data)
    
    # 激进调整因子
    aggressive_adjustments = {
        "volatility_tolerance": 1.5,      # 高波动容忍度
        "drawdown_tolerance": 1.3,        # 高回撤容忍度
        "leverage_acceptance": 1.2,       # 接受适度杠杆
        "opportunity_weight": 1.4         # 高机会权重
    }
    
    # 调整风险评估
    adjusted_risk = self._apply_aggressive_adjustments(
        base_risk_metrics, aggressive_adjustments
    )
    
    # 收益风险比分析
    return_risk_analysis = self._analyze_return_risk_ratio(
        trading_decision, adjusted_risk
    )
    
    # 机会成本评估
    opportunity_cost = self._assess_opportunity_cost(trading_decision, market_data)
    
    return {
        "risk_score": adjusted_risk["overall_risk"],
        "return_potential": return_risk_analysis["return_potential"],
        "risk_adjusted_return": return_risk_analysis["risk_adjusted_return"],
        "opportunity_cost": opportunity_cost,
        "recommendation": self._generate_aggressive_recommendation(
            adjusted_risk, return_risk_analysis, opportunity_cost
        ),
        "key_considerations": [
            "高收益潜力值得承担相应风险",
            "市场机会稍纵即逝，应果断行动",
            "适度风险是获得超额收益的必要条件",
            "风险可通过主动管理得到控制"
        ]
    }

def _analyze_return_risk_ratio(self, decision: Dict, risk_metrics: Dict) -> Dict:
    """分析收益风险比"""
    
    expected_return = decision.get("take_profit", 0.1)
    risk_level = risk_metrics.get("overall_risk", 0.5)
    
    # 激进视角下的收益风险比计算
    # 更看重收益潜力，对风险相对宽容
    risk_adjusted_return = expected_return / max(risk_level * 0.8, 0.1)
    
    return_potential_score = min(expected_return * 10, 1.0)  # 收益潜力评分
    
    return {
        "return_potential": return_potential_score,
        "risk_adjusted_return": risk_adjusted_return,
        "return_risk_ratio": expected_return / max(risk_level, 0.1),
        "attractiveness": "高" if risk_adjusted_return > 1.5 else "中" if risk_adjusted_return > 1.0 else "低"
    }

def _assess_opportunity_cost(self, decision: Dict, market_data: Dict) -> Dict:
    """评估机会成本"""
    
    # 不行动的机会成本
    inaction_cost = self._calculate_inaction_cost(decision, market_data)
    
    # 延迟行动的成本
    delay_cost = self._calculate_delay_cost(decision, market_data)
    
    # 保守策略的机会成本
    conservative_cost = self._calculate_conservative_cost(decision)
    
    total_opportunity_cost = inaction_cost + delay_cost + conservative_cost
    
    return {
        "inaction_cost": inaction_cost,
        "delay_cost": delay_cost,
        "conservative_cost": conservative_cost,
        "total_cost": total_opportunity_cost,
        "urgency_level": "高" if total_opportunity_cost > 0.1 else "中" if total_opportunity_cost > 0.05 else "低"
    }
```

## 2. 保守风险评估智能体

### 特点与职责
```python
class ConservativeRiskAssessor:
    """保守风险评估 - 强调风险控制和资本保护"""
    
    def __init__(self, config):
        self.config = config
        self.risk_appetite = "low"
        self.capital_preservation_focus = True
        
    专业特点:
    - 低风险容忍度
    - 强调资本保护
    - 谨慎的仓位管理
    - 严格的风险控制
    
    评估重点:
    - 下行风险保护
    - 最大回撤控制
    - 流动性风险管理
    - 尾部风险防范
```

### 风险评估方法
```python
def assess_risk(self, trading_decision: Dict, market_data: Dict) -> Dict:
    """保守角度的风险评估"""
    
    # 基础风险指标
    base_risk_metrics = self._calculate_base_risk_metrics(trading_decision, market_data)
    
    # 保守调整因子
    conservative_adjustments = {
        "volatility_penalty": 1.5,        # 高波动惩罚
        "drawdown_penalty": 1.8,          # 高回撤惩罚
        "liquidity_requirement": 1.3,     # 高流动性要求
        "safety_margin": 1.4              # 高安全边际
    }
    
    # 调整风险评估
    adjusted_risk = self._apply_conservative_adjustments(
        base_risk_metrics, conservative_adjustments
    )
    
    # 下行风险分析
    downside_risk = self._analyze_downside_risk(trading_decision, market_data)
    
    # 尾部风险评估
    tail_risk = self._assess_tail_risk(trading_decision, market_data)
    
    # 流动性风险评估
    liquidity_risk = self._assess_liquidity_risk(trading_decision, market_data)
    
    return {
        "risk_score": adjusted_risk["overall_risk"],
        "downside_risk": downside_risk,
        "tail_risk": tail_risk,
        "liquidity_risk": liquidity_risk,
        "capital_at_risk": self._calculate_capital_at_risk(adjusted_risk),
        "recommendation": self._generate_conservative_recommendation(
            adjusted_risk, downside_risk, tail_risk
        ),
        "risk_mitigation_measures": [
            "严格设置止损位，控制最大损失",
            "分散投资，降低单一资产风险",
            "保持充足现金储备",
            "定期重新评估风险状况",
            "避免过度集中和杠杆"
        ]
    }

def _analyze_downside_risk(self, decision: Dict, market_data: Dict) -> Dict:
    """分析下行风险"""
    
    stop_loss = decision.get("stop_loss", 0.05)
    position_size = decision.get("quantity", 0.05)
    
    # 最大可能损失
    max_loss = stop_loss * position_size
    
    # 下行波动率
    downside_volatility = market_data.get("downside_volatility", 0.2)
    
    # VaR 计算 (95% 置信度)
    var_95 = position_size * downside_volatility * 1.65  # 95% VaR
    
    # CVaR 计算 (条件风险价值)
    cvar_95 = var_95 * 1.3  # 估算 CVaR
    
    return {
        "max_loss": max_loss,
        "var_95": var_95,
        "cvar_95": cvar_95,
        "downside_volatility": downside_volatility,
        "risk_level": "高" if max_loss > 0.02 else "中" if max_loss > 0.01 else "低"
    }

def _assess_tail_risk(self, decision: Dict, market_data: Dict) -> Dict:
    """评估尾部风险"""
    
    # 极端市场情况下的风险
    market_stress_scenarios = {
        "market_crash": {"probability": 0.05, "impact": -0.3},
        "liquidity_crisis": {"probability": 0.03, "impact": -0.2},
        "sector_collapse": {"probability": 0.08, "impact": -0.25},
        "black_swan": {"probability": 0.01, "impact": -0.5}
    }
    
    position_size = decision.get("quantity", 0.05)
    
    tail_risk_exposure = 0
    scenario_impacts = {}
    
    for scenario, params in market_stress_scenarios.items():
        scenario_loss = position_size * abs(params["impact"])
        expected_loss = scenario_loss * params["probability"]
        tail_risk_exposure += expected_loss
        
        scenario_impacts[scenario] = {
            "potential_loss": scenario_loss,
            "expected_loss": expected_loss,
            "probability": params["probability"]
        }
    
    return {
        "total_tail_risk": tail_risk_exposure,
        "scenario_impacts": scenario_impacts,
        "tail_risk_level": "高" if tail_risk_exposure > 0.01 else "中" if tail_risk_exposure > 0.005 else "低",
        "mitigation_priority": "高" if tail_risk_exposure > 0.01 else "中"
    }
```

## 3. 中性风险评估智能体

### 特点与职责
```python
class NeutralRiskAssessor:
    """中性风险评估 - 平衡风险和收益"""
    
    def __init__(self, config):
        self.config = config
        self.risk_appetite = "medium"
        self.balanced_approach = True
        
    专业特点:
    - 平衡的风险观
    - 理性的收益预期
    - 适度的风险承担
    - 全面的风险考量
    
    评估重点:
    - 风险收益平衡
    - 多维度风险分析
    - 情景分析
    - 概率加权评估
```

### 风险评估方法
```python
def assess_risk(self, trading_decision: Dict, market_data: Dict) -> Dict:
    """中性角度的风险评估"""
    
    # 全面风险分析
    comprehensive_risk = self._conduct_comprehensive_risk_analysis(
        trading_decision, market_data
    )
    
    # 情景分析
    scenario_analysis = self._conduct_scenario_analysis(trading_decision, market_data)
    
    # 风险收益平衡评估
    risk_return_balance = self._assess_risk_return_balance(
        trading_decision, comprehensive_risk
    )
    
    # 概率加权风险评估
    probability_weighted_risk = self._calculate_probability_weighted_risk(
        scenario_analysis
    )
    
    return {
        "comprehensive_risk": comprehensive_risk,
        "scenario_analysis": scenario_analysis,
        "risk_return_balance": risk_return_balance,
        "probability_weighted_risk": probability_weighted_risk,
        "overall_assessment": self._generate_balanced_assessment(
            comprehensive_risk, scenario_analysis, risk_return_balance
        ),
        "balanced_recommendation": self._generate_balanced_recommendation(
            comprehensive_risk, risk_return_balance
        )
    }

def _conduct_scenario_analysis(self, decision: Dict, market_data: Dict) -> Dict:
    """进行情景分析"""
    
    scenarios = {
        "bull_case": {"probability": 0.3, "return": 0.15, "risk": 0.1},
        "base_case": {"probability": 0.4, "return": 0.08, "risk": 0.15},
        "bear_case": {"probability": 0.3, "return": -0.05, "risk": 0.25}
    }
    
    position_size = decision.get("quantity", 0.05)
    
    scenario_outcomes = {}
    expected_return = 0
    expected_risk = 0
    
    for scenario_name, params in scenarios.items():
        scenario_return = params["return"] * position_size
        scenario_risk = params["risk"] * position_size
        probability = params["probability"]
        
        expected_return += scenario_return * probability
        expected_risk += scenario_risk * probability
        
        scenario_outcomes[scenario_name] = {
            "return": scenario_return,
            "risk": scenario_risk,
            "probability": probability,
            "risk_adjusted_return": scenario_return / max(scenario_risk, 0.01)
        }
    
    return {
        "scenarios": scenario_outcomes,
        "expected_return": expected_return,
        "expected_risk": expected_risk,
        "risk_return_ratio": expected_return / max(expected_risk, 0.01),
        "scenario_dispersion": self._calculate_scenario_dispersion(scenario_outcomes)
    }

def _assess_risk_return_balance(self, decision: Dict, risk_metrics: Dict) -> Dict:
    """评估风险收益平衡"""
    
    expected_return = decision.get("take_profit", 0.1)
    expected_risk = risk_metrics.get("overall_risk", 0.5)
    
    # 夏普比率估算
    risk_free_rate = 0.02  # 假设无风险利率
    excess_return = expected_return - risk_free_rate
    sharpe_ratio = excess_return / max(expected_risk, 0.01)
    
    # 风险调整后收益
    risk_adjusted_return = expected_return / max(expected_risk, 0.01)
    
    # 平衡评分
    balance_score = self._calculate_balance_score(sharpe_ratio, risk_adjusted_return)
    
    return {
        "sharpe_ratio": sharpe_ratio,
        "risk_adjusted_return": risk_adjusted_return,
        "balance_score": balance_score,
        "balance_assessment": self._assess_balance_quality(balance_score),
        "optimization_suggestions": self._suggest_balance_optimization(
            expected_return, expected_risk, balance_score
        )
    }
```

## 4. 风险管理决策

### 风险决策框架
```python
class RiskDecisionFramework:
    """风险决策框架"""
    
    def make_risk_decision(self, risk_assessments: Dict, trading_decision: Dict) -> Dict:
        """制定风险管理决策"""
        
        # 1. 风险共识分析
        risk_consensus = self._analyze_risk_consensus(risk_assessments)
        
        # 2. 风险等级确定
        final_risk_level = self._determine_final_risk_level(risk_assessments, risk_consensus)
        
        # 3. 决策建议生成
        decision_recommendation = self._generate_decision_recommendation(
            final_risk_level, risk_consensus, trading_decision
        )
        
        # 4. 风险控制措施
        risk_controls = self._design_risk_controls(final_risk_level, trading_decision)
        
        # 5. 监控要求
        monitoring_requirements = self._define_monitoring_requirements(
            final_risk_level, trading_decision
        )
        
        return {
            "risk_consensus": risk_consensus,
            "final_risk_level": final_risk_level,
            "decision": decision_recommendation,
            "risk_controls": risk_controls,
            "monitoring": monitoring_requirements,
            "approval_status": self._determine_final_approval(decision_recommendation)
        }
    
    def _analyze_risk_consensus(self, assessments: Dict) -> Dict:
        """分析风险评估共识"""
        
        risk_scores = [
            assessments["aggressive"]["risk_score"],
            assessments["conservative"]["risk_score"],
            assessments["neutral"]["comprehensive_risk"]["overall_risk"]
        ]
        
        # 计算共识指标
        avg_risk = sum(risk_scores) / len(risk_scores)
        risk_std = np.std(risk_scores)
        consensus_level = 1.0 - min(risk_std / avg_risk, 1.0) if avg_risk > 0 else 0.0
        
        # 分析分歧点
        disagreement_areas = self._identify_disagreement_areas(assessments)
        
        return {
            "average_risk_score": avg_risk,
            "risk_score_std": risk_std,
            "consensus_level": consensus_level,
            "disagreement_areas": disagreement_areas,
            "consensus_quality": "高" if consensus_level > 0.8 else "中" if consensus_level > 0.6 else "低"
        }
    
    def _generate_decision_recommendation(self, risk_level: str, consensus: Dict, decision: Dict) -> Dict:
        """生成决策建议"""
        
        consensus_level = consensus["consensus_level"]
        avg_risk = consensus["average_risk_score"]
        
        if risk_level == "low" and consensus_level > 0.7:
            recommendation = "approve"
            confidence = 0.9
        elif risk_level == "medium" and consensus_level > 0.6:
            recommendation = "approve_with_conditions"
            confidence = 0.7
        elif risk_level == "high" and consensus_level > 0.8:
            recommendation = "approve_with_strict_controls"
            confidence = 0.6
        else:
            recommendation = "reject"
            confidence = 0.8
        
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": self._explain_recommendation_reasoning(
                risk_level, consensus_level, avg_risk, recommendation
            ),
            "conditions": self._define_approval_conditions(recommendation, risk_level)
        }
```

### 风险监控系统
```python
class RiskMonitor:
    """风险监控系统"""
    
    def __init__(self):
        self.active_positions = {}
        self.risk_alerts = []
        self.monitoring_rules = self._setup_monitoring_rules()
    
    def monitor_position_risk(self, position_id: str, current_data: Dict) -> Dict:
        """监控仓位风险"""
        
        position = self.active_positions.get(position_id)
        if not position:
            return {"status": "position_not_found"}
        
        # 实时风险计算
        current_risk = self._calculate_current_risk(position, current_data)
        
        # 风险阈值检查
        risk_alerts = self._check_risk_thresholds(position, current_risk)
        
        # 止损止盈检查
        exit_signals = self._check_exit_conditions(position, current_data)
        
        # 更新监控状态
        monitoring_status = self._update_monitoring_status(
            position, current_risk, risk_alerts, exit_signals
        )
        
        return {
            "position_id": position_id,
            "current_risk": current_risk,
            "risk_alerts": risk_alerts,
            "exit_signals": exit_signals,
            "monitoring_status": monitoring_status,
            "recommended_actions": self._recommend_risk_actions(
                current_risk, risk_alerts, exit_signals
            )
        }
```

风险管理智能体通过多角度评估、严格控制和持续监控，确保交易活动在可控的风险范围内进行，保护投资组合的安全。
