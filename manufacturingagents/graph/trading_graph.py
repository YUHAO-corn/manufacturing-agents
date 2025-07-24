# TradingAgents/graph/trading_graph.py

import os
from pathlib import Path
import json
from datetime import date
from typing import Dict, Any, Tuple, List, Optional

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from manufacturingagents.llm_adapters import ChatDashScope

from langgraph.prebuilt import ToolNode

from manufacturingagents.agents import *
from manufacturingagents.default_config import DEFAULT_CONFIG
from manufacturingagents.agents.utils.memory import FinancialSituationMemory
from manufacturingagents.agents.utils.agent_states import (
    AgentState,
    InvestDebateState,
    RiskDebateState,
)
from manufacturingagents.dataflows.interface import set_config

from .conditional_logic import ConditionalLogic
from .setup import GraphSetup
from .propagation import Propagator
from .reflection import Reflector
from .signal_processing import SignalProcessor


class TradingAgentsGraph:
    """Main class that orchestrates the trading agents framework."""

    def __init__(
        self,
        selected_analysts=["market", "social", "news", "fundamentals"],
        debug=False,
        config: Dict[str, Any] = None,
    ):
        """Initialize the trading agents graph and components.

        Args:
            selected_analysts: List of analyst types to include
            debug: Whether to run in debug mode
            config: Configuration dictionary. If None, uses default config
        """
        self.debug = debug
        self.config = config if config is not None else DEFAULT_CONFIG

        # Update the interface's config
        set_config(self.config)

        # Create necessary directories
        os.makedirs(
            os.path.join(self.config["project_dir"], "dataflows/data_cache"),
            exist_ok=True,
        )

        # Initialize LLMs
        self._initialize_llms()
        
        self.toolkit = Toolkit(config=self.config)

        # Initialize memories (如果启用)
        self._initialize_memories()

        # Create tool nodes
        self.tool_nodes = self._create_tool_nodes()

        # Initialize components
        self.conditional_logic = ConditionalLogic()
        self.graph_setup = GraphSetup(
            quick_thinking_llm=self.quick_thinking_llm,
            deep_thinking_llm=self.deep_thinking_llm,
            toolkit=self.toolkit,
            tool_nodes=self.tool_nodes,
            bull_memory=self.bull_memory,
            bear_memory=self.bear_memory,
            trader_memory=self.trader_memory,
            invest_judge_memory=self.invest_judge_memory,
            risk_manager_memory=self.risk_manager_memory,
            conditional_logic=self.conditional_logic,
            config=self.config,
            react_llm=getattr(self, 'react_llm', None),
        )

        # Note: The new get_llm_for_agent method is available for more granular control
        # if needed in the future, but GraphSetup still uses the global thinkers for now.
        # To enable agent-specific LLMs, we would need to modify GraphSetup.

        self.propagator = Propagator()
        self.reflector = Reflector(self.quick_thinking_llm)
        self.signal_processor = SignalProcessor(self.quick_thinking_llm)

        # State tracking
        self.curr_state = None
        self.ticker = None
        self.log_states_dict = {}  # date to full state dict

        # Set up the graph
        self.graph = self.graph_setup.setup_graph(selected_analysts)

    def _create_llm_instance(self, provider: str, model_name: str, config: Dict[str, Any]) -> BaseChatModel:
        """Creates an LLM instance based on the provider and configuration."""
        if provider.lower() in ["openai", "ollama", "openrouter"]:
            return ChatOpenAI(model=model_name, base_url=config.get("backend_url"))
        elif provider.lower() == "anthropic":
            return ChatAnthropic(model=model_name, base_url=config.get("backend_url"))
        elif provider.lower() == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=os.getenv('GOOGLE_API_KEY'),
                temperature=config.get("temperature", 0.1),
                max_output_tokens=config.get("max_tokens", 2000)
            )
        elif provider.lower() in ["dashscope", "alibaba", "阿里百炼"]:
            return ChatDashScope(
                model=model_name,
                temperature=config.get("temperature", 0.1),
                max_tokens=config.get("max_tokens", 2000)
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _initialize_llms(self):
        """Initializes all LLM instances, including global fallbacks and agent-specific ones."""
        # Initialize global fallback LLMs
        self.deep_thinking_llm = self._create_llm_instance(
            self.config["llm_provider"],
            self.config["deep_think_llm"],
            self.config
        )
        self.quick_thinking_llm = self._create_llm_instance(
            self.config["llm_provider"],
            self.config["quick_think_llm"],
            self.config
        )
        
        # Initialize ReAct LLM for DashScope if needed
        provider_lower = self.config.get("llm_provider", "").lower()
        if "dashscope" in provider_lower or "阿里百炼" in provider_lower:
            from langchain_community.llms import Tongyi
            self.react_llm = Tongyi()
            quick_model = self.config["quick_think_llm"]
            if quick_model in ["gpt-4o-mini", "o4-mini"]:
                quick_model = "qwen-turbo"
            self.react_llm.model_name = quick_model
            print(f"📊 [DEBUG] ReAct LLM模型设置为: {quick_model}")

        # Initialize agent-specific LLMs
        self.agent_llms = {}
        agent_configs = self.config.get("agent_llms", {})
        for agent_name, agent_config in agent_configs.items():
            provider = agent_config.get("provider", self.config["llm_provider"])
            model_name = agent_config.get("model")
            if model_name:
                # Merge global and agent-specific configs
                merged_config = self.config.copy()
                merged_config.update(agent_config)
                self.agent_llms[agent_name] = self._create_llm_instance(
                    provider, model_name, merged_config
                )

    def get_llm_for_agent(self, agent_name: str, thinking_type: str = 'deep'):
        """
        Gets the appropriate LLM for a given agent.
        Falls back to global thinking LLMs if no specific one is configured.
        """
        if agent_name in self.agent_llms:
            return self.agent_llms[agent_name]
        
        if thinking_type == 'deep':
            return self.deep_thinking_llm
        else:
            return self.quick_thinking_llm

    def _initialize_memories(self):
        """Initializes financial situation memories for relevant agents."""
        memory_enabled = self.config.get("memory_enabled", True)
        if memory_enabled:
            self.bull_memory = FinancialSituationMemory("bull_memory", self.config)
            self.bear_memory = FinancialSituationMemory("bear_memory", self.config)
            self.trader_memory = FinancialSituationMemory("trader_memory", self.config)
            self.invest_judge_memory = FinancialSituationMemory("invest_judge_memory", self.config)
            self.risk_manager_memory = FinancialSituationMemory("risk_manager_memory", self.config)
        else:
            self.bull_memory, self.bear_memory, self.trader_memory, self.invest_judge_memory, self.risk_manager_memory = [None] * 5

    def _create_tool_nodes(self) -> Dict[str, ToolNode]:
        """Create tool nodes for different data sources."""
        return {
            "market": ToolNode(
                [
                    # online tools
                    self.toolkit.get_YFin_data_online,
                    self.toolkit.get_stockstats_indicators_report_online,
                    # 中国股票专用工具
                    self.toolkit.get_china_stock_data,
                    # offline tools
                    self.toolkit.get_YFin_data,
                    self.toolkit.get_stockstats_indicators_report,
                ]
            ),
            "social": ToolNode(
                [
                    # online tools
                    self.toolkit.get_stock_news_openai,
                    # offline tools
                    self.toolkit.get_reddit_stock_info,
                ]
            ),
            "news": ToolNode(
                [
                    # online tools
                    self.toolkit.get_global_news_openai,
                    self.toolkit.get_google_news,
                    # offline tools
                    self.toolkit.get_finnhub_news,
                    self.toolkit.get_reddit_news,
                ]
            ),
            "fundamentals": ToolNode(
                [
                    # online tools
                    self.toolkit.get_fundamentals_openai,
                    # 中国股票专用工具
                    self.toolkit.get_china_stock_data,
                    self.toolkit.get_china_fundamentals,
                    # offline tools
                    self.toolkit.get_finnhub_company_insider_sentiment,
                    self.toolkit.get_finnhub_company_insider_transactions,
                    self.toolkit.get_simfin_balance_sheet,
                    self.toolkit.get_simfin_cashflow,
                    self.toolkit.get_simfin_income_stmt,
                ]
            ),
            # === 制造业专用工具节点 ===
            "manufacturing_macro": ToolNode(
                [
                    # 宏观经济数据工具
                    self.toolkit.get_manufacturing_pmi_data,
                    self.toolkit.get_manufacturing_ppi_data,
                    self.toolkit.get_manufacturing_commodity_data,
                ]
            ),
            "manufacturing_environment": ToolNode(
                [
                    # 环境和外部因素工具
                    self.toolkit.get_manufacturing_weather_data,
                    self.toolkit.get_manufacturing_holiday_data,
                ]
            ),
            "manufacturing_intelligence": ToolNode(
                [
                    # 市场情报和新闻工具
                    self.toolkit.get_manufacturing_news_data,
                ]
            ),
        }

    def propagate(self, company_name, trade_date):
        """Run the trading agents graph for a company on a specific date."""

        self.ticker = company_name

        # Initialize state
        init_agent_state = self.propagator.create_initial_state(
            company_name, trade_date
        )
        args = self.propagator.get_graph_args()

        if self.debug:
            # Debug mode with tracing
            trace = []
            for chunk in self.graph.stream(init_agent_state, **args):
                if len(chunk["messages"]) == 0:
                    pass
                else:
                    chunk["messages"][-1].pretty_print()
                    trace.append(chunk)

            final_state = trace[-1]
        else:
            # Standard mode without tracing
            final_state = self.graph.invoke(init_agent_state, **args)

        # Store current state for reflection
        self.curr_state = final_state

        # Log state
        self._log_state(trade_date, final_state)

        # Return decision and processed signal
        return final_state, self.process_signal(final_state["final_trade_decision"], company_name)

    def _log_state(self, trade_date, final_state):
        """Log the final state to a JSON file."""
        self.log_states_dict[str(trade_date)] = {
            "company_of_interest": final_state["company_of_interest"],
            "trade_date": final_state["trade_date"],
            "market_report": final_state["market_report"],
            "sentiment_report": final_state["sentiment_report"],
            "news_report": final_state["news_report"],
            "fundamentals_report": final_state["fundamentals_report"],
            "investment_debate_state": {
                "bull_history": final_state["investment_debate_state"]["bull_history"],
                "bear_history": final_state["investment_debate_state"]["bear_history"],
                "history": final_state["investment_debate_state"]["history"],
                "current_response": final_state["investment_debate_state"][
                    "current_response"
                ],
                "judge_decision": final_state["investment_debate_state"][
                    "judge_decision"
                ],
            },
            "trader_investment_decision": final_state["trader_investment_plan"],
            "risk_debate_state": {
                "risky_history": final_state["risk_debate_state"]["risky_history"],
                "safe_history": final_state["risk_debate_state"]["safe_history"],
                "neutral_history": final_state["risk_debate_state"]["neutral_history"],
                "history": final_state["risk_debate_state"]["history"],
                "judge_decision": final_state["risk_debate_state"]["judge_decision"],
            },
            "investment_plan": final_state["investment_plan"],
            "final_trade_decision": final_state["final_trade_decision"],
        }

        # Save to file
        directory = Path(f"eval_results/{self.ticker}/TradingAgentsStrategy_logs/")
        directory.mkdir(parents=True, exist_ok=True)

        with open(
            f"eval_results/{self.ticker}/TradingAgentsStrategy_logs/full_states_log.json",
            "w",
        ) as f:
            json.dump(self.log_states_dict, f, indent=4)

    def reflect_and_remember(self, returns_losses):
        """Reflect on decisions and update memory based on returns."""
        self.reflector.reflect_bull_researcher(
            self.curr_state, returns_losses, self.bull_memory
        )
        self.reflector.reflect_bear_researcher(
            self.curr_state, returns_losses, self.bear_memory
        )
        self.reflector.reflect_trader(
            self.curr_state, returns_losses, self.trader_memory
        )
        self.reflector.reflect_invest_judge(
            self.curr_state, returns_losses, self.invest_judge_memory
        )
        self.reflector.reflect_risk_manager(
            self.curr_state, returns_losses, self.risk_manager_memory
        )

    def process_signal(self, full_signal, stock_symbol=None):
        """Process a signal to extract the core decision."""
        return self.signal_processor.process_signal(full_signal, stock_symbol)
