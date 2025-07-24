from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json


def create_market_analyst_react(llm, toolkit):
    """使用ReAct Agent模式的市场分析师（适用于通义千问）"""
    def market_analyst_react_node(state):
        print(f"📈 [DEBUG] ===== ReAct市场分析师节点开始 =====")

        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        print(f"📈 [DEBUG] 输入参数: ticker={ticker}, date={current_date}")

        # 检查是否为中国股票
        def is_china_stock(ticker_code):
            import re
            return re.match(r'^\d{6}$', str(ticker_code))

        is_china = is_china_stock(ticker)
        print(f"📈 [DEBUG] 股票类型检查: {ticker} -> 中国A股: {is_china}")

        if toolkit.config["online_tools"]:
            # 在线模式，使用ReAct Agent
            if is_china:
                print(f"📈 [市场分析师] 使用ReAct Agent分析中国股票")

                # 创建中国股票数据工具
                from langchain_core.tools import BaseTool

                class ChinaStockDataTool(BaseTool):
                    name: str = "get_china_stock_data"
                    description: str = f"获取中国A股股票{ticker}的市场数据和技术指标（优化缓存版本）。直接调用，无需参数。"

                    def _run(self, query: str = "") -> str:
                        try:
                            print(f"📈 [DEBUG] ChinaStockDataTool调用，股票代码: {ticker}")
                            # 使用优化的缓存数据获取
                            from manufacturingagents.dataflows.optimized_china_data import get_china_stock_data_cached
                            return get_china_stock_data_cached(
                                symbol=ticker,
                                start_date='2025-05-28',
                                end_date=current_date,
                                force_refresh=False
                            )
                        except Exception as e:
                            print(f"❌ 优化A股数据获取失败: {e}")
                            # 备用方案：使用原始API
                            try:
                                return toolkit.get_china_stock_data.invoke({
                                    'stock_code': ticker,
                                    'start_date': '2025-05-28',
                                    'end_date': current_date
                                })
                            except Exception as e2:
                                return f"获取股票数据失败: {str(e2)}"

                tools = [ChinaStockDataTool()]
                query = f"""请对中国A股股票{ticker}进行详细的技术分析。

执行步骤：
1. 使用get_china_stock_data工具获取股票市场数据
2. 基于获取的真实数据进行深入的技术指标分析
3. 直接输出完整的技术分析报告内容

重要要求：
- 必须输出完整的技术分析报告内容，不要只是描述报告已完成
- 报告必须基于工具获取的真实数据进行分析
- 报告长度不少于800字
- 包含具体的数据、指标数值和专业分析

报告格式应包含：
## 股票基本信息
## 技术指标分析
## 价格趋势分析
## 成交量分析
## 市场情绪分析
## 投资建议"""
            else:
                print(f"📈 [市场分析师] 使用ReAct Agent分析美股/港股")

                # 创建美股数据工具
                from langchain_core.tools import BaseTool

                class USStockDataTool(BaseTool):
                    name: str = "get_us_stock_data"
                    description: str = f"获取美股/港股{ticker}的市场数据和技术指标（优化缓存版本）。直接调用，无需参数。"

                    def _run(self, query: str = "") -> str:
                        try:
                            print(f"📈 [DEBUG] USStockDataTool调用，股票代码: {ticker}")
                            # 使用优化的缓存数据获取
                            from manufacturingagents.dataflows.optimized_us_data import get_us_stock_data_cached
                            return get_us_stock_data_cached(
                                symbol=ticker,
                                start_date='2025-05-28',
                                end_date=current_date,
                                force_refresh=False
                            )
                        except Exception as e:
                            print(f"❌ 优化美股数据获取失败: {e}")
                            # 备用方案：使用原始API
                            try:
                                return toolkit.get_YFin_data_online.invoke({
                                    'symbol': ticker,
                                    'start_date': '2025-05-28',
                                    'end_date': current_date
                                })
                            except Exception as e2:
                                return f"获取股票数据失败: {str(e2)}"

                class FinnhubNewsTool(BaseTool):
                    name: str = "get_finnhub_news"
                    description: str = f"获取美股{ticker}的最新新闻和市场情绪（通过FINNHUB API）。直接调用，无需参数。"

                    def _run(self, query: str = "") -> str:
                        try:
                            print(f"📈 [DEBUG] FinnhubNewsTool调用，股票代码: {ticker}")
                            return toolkit.get_finnhub_news.invoke({
                                'ticker': ticker,
                                'start_date': '2025-05-28',
                                'end_date': current_date
                            })
                        except Exception as e:
                            return f"获取新闻数据失败: {str(e)}"

                tools = [USStockDataTool(), FinnhubNewsTool()]
                query = f"""请对美股{ticker}进行详细的技术分析。

执行步骤：
1. 使用get_us_stock_data工具获取股票市场数据和技术指标（通过FINNHUB API）
2. 使用get_finnhub_news工具获取最新新闻和市场情绪
3. 基于获取的真实数据进行深入的技术指标分析
4. 直接输出完整的技术分析报告内容

重要要求：
- 必须输出完整的技术分析报告内容，不要只是描述报告已完成
- 报告必须基于工具获取的真实数据进行分析
- 报告长度不少于800字
- 包含具体的数据、指标数值和专业分析
- 结合新闻信息分析市场情绪

报告格式应包含：
## 股票基本信息
## 技术指标分析
## 价格趋势分析
## 成交量分析
## 新闻和市场情绪分析
## 投资建议"""

            try:
                # 创建ReAct Agent
                prompt = hub.pull("hwchase17/react")
                agent = create_react_agent(llm, tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    handle_parsing_errors=True,
                    max_iterations=10,  # 增加到10次迭代，确保有足够时间完成分析
                    max_execution_time=180  # 增加到3分钟，给更多时间生成详细报告
                )

                print(f"📈 [DEBUG] 执行ReAct Agent查询...")
                result = agent_executor.invoke({'input': query})

                report = result['output']
                print(f"📈 [市场分析师] ReAct Agent完成，报告长度: {len(report)}")

            except Exception as e:
                print(f"❌ [DEBUG] ReAct Agent失败: {str(e)}")
                report = f"ReAct Agent市场分析失败: {str(e)}"
        else:
            # 离线模式，使用原有逻辑
            report = "离线模式，暂不支持"

        print(f"📈 [DEBUG] ===== ReAct市场分析师节点结束 =====")

        return {
            "messages": [("assistant", report)],
            "market_report": report,
        }

    return market_analyst_react_node


def create_market_analyst(llm, toolkit):

    def market_analyst_node(state):
        print(f"📈 [DEBUG] ===== 市场分析师节点开始 =====")

        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        print(f"📈 [DEBUG] 输入参数: ticker={ticker}, date={current_date}")
        print(f"📈 [DEBUG] 当前状态中的消息数量: {len(state.get('messages', []))}")
        print(f"📈 [DEBUG] 现有市场报告: {state.get('market_report', 'None')[:100]}...")

        # 根据股票代码格式选择数据源
        def is_china_stock(ticker_code):
            """判断是否为中国A股代码"""
            import re
            # A股代码格式：6位数字
            return re.match(r'^\d{6}$', str(ticker_code))

        if toolkit.config["online_tools"]:
            if is_china_stock(ticker):
                # 中国A股使用通达信数据源
                tools = [
                    toolkit.get_china_stock_data,
                ]
            else:
                # 美股和港股使用Yahoo Finance
                tools = [
                    toolkit.get_YFin_data_online,
                    toolkit.get_stockstats_indicators_report_online,
                ]
        else:
            tools = [
                toolkit.get_YFin_data,
                toolkit.get_stockstats_indicators_report,
            ]

        system_message = (
            """你是一位专业的交易助手，负责分析金融市场。你的角色是从以下列表中选择**最相关的指标**来分析给定的市场条件或交易策略。目标是选择最多**8个指标**，提供互补的见解而不重复。各类别及其指标如下：

移动平均线：
- close_50_sma: 50日简单移动平均线：中期趋势指标。用途：识别趋势方向并作为动态支撑/阻力。提示：滞后于价格；结合更快的指标获得及时信号。
- close_200_sma: 200日简单移动平均线：长期趋势基准。用途：确认整体市场趋势并识别金叉/死叉设置。提示：反应缓慢；最适合战略趋势确认而非频繁交易入场。
- close_10_ema: 10日指数移动平均线：响应迅速的短期平均线。用途：捕捉动量快速变化和潜在入场点。提示：在震荡市场中容易产生噪音；与较长平均线结合使用以过滤虚假信号。

MACD相关指标：
- macd: MACD：通过EMA差值计算动量。用途：寻找交叉和背离作为趋势变化信号。提示：在低波动或横盘市场中需要其他指标确认。
- macds: MACD信号线：MACD线的EMA平滑。用途：使用与MACD线的交叉来触发交易。提示：应作为更广泛策略的一部分以避免虚假信号。
- macdh: MACD柱状图：显示MACD线与其信号线之间的差距。用途：可视化动量强度并及早发现背离。提示：可能波动较大；在快速移动市场中需要额外过滤器。

动量指标：
- rsi: RSI：测量动量以标记超买/超卖条件。用途：应用70/30阈值并观察背离以信号反转。提示：在强趋势中，RSI可能保持极端值；始终与趋势分析交叉验证。

波动性指标：
- boll: 布林带中轨：作为布林带基础的20日SMA。用途：作为价格运动的动态基准。提示：与上下轨结合使用以有效发现突破或反转。
- boll_ub: 布林带上轨：通常是中线上方2个标准差。用途：信号潜在超买条件和突破区域。提示：用其他工具确认信号；在强趋势中价格可能沿着轨道运行。
- boll_lb: 布林带下轨：通常是中线下方2个标准差。用途：指示潜在超卖条件。提示：使用额外分析以避免虚假反转信号。
- atr: ATR：平均真实范围以测量波动性。用途：根据当前市场波动性设置止损水平和调整仓位大小。提示：这是一个反应性指标，应作为更广泛风险管理策略的一部分。

成交量指标：
- vwma: VWMA：按成交量加权的移动平均线。用途：通过整合价格行为和成交量数据来确认趋势。提示：注意成交量激增造成的偏斜结果；与其他成交量分析结合使用。

- 选择提供多样化和互补信息的指标。避免冗余（例如，不要同时选择rsi和stochrsi）。还要简要解释为什么它们适合给定的市场环境。当你调用工具时，请使用上面提供的指标的确切名称，因为它们是定义的参数，否则你的调用将失败。请确保首先调用get_YFin_data来检索生成指标所需的CSV。写一份非常详细和细致的趋势观察报告。不要简单地说趋势是混合的，提供详细和细粒度的分析和见解，可能帮助交易者做出决策。

请确保所有分析都使用中文，并在报告末尾附加一个Markdown表格来组织报告中的要点，使其有组织且易于阅读。"""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一位有用的AI助手，与其他助手协作。"
                    "使用提供的工具来回答问题。"
                    "如果你无法完全回答，没关系；另一位具有不同工具的助手"
                    "将从你停下的地方继续帮助。执行你能做的来取得进展。"
                    "如果你或任何其他助手有最终交易建议：**买入/持有/卖出**或可交付成果，"
                    "请在你的回复前加上'最终交易建议：**买入/持有/卖出**'，这样团队就知道要停止了。"
                    "你可以使用以下工具：{tool_names}。\n{system_message}"
                    "供你参考，当前日期是{current_date}。我们要分析的公司是{ticker}。请确保所有分析都使用中文。",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        # 处理市场分析报告
        if len(result.tool_calls) == 0:
            # 没有工具调用，直接使用LLM的回复
            report = result.content
        else:
            # 有工具调用，需要等待工具执行完成后获取最终报告
            report = f"市场分析师正在调用工具进行分析: {[call.get('name', 'unknown') for call in result.tool_calls]}"
            print(f"📊 [市场分析师] 工具调用: {[call.get('name', 'unknown') for call in result.tool_calls]}")

        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
