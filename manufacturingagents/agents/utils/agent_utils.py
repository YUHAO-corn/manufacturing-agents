from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage
from typing import List
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import RemoveMessage
from langchain_core.tools import tool
from datetime import date, timedelta, datetime
import functools
import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from langchain_openai import ChatOpenAI
import manufacturingagents.dataflows.interface as interface
from manufacturingagents.default_config import DEFAULT_CONFIG
from langchain_core.messages import HumanMessage
from typing import Union


def create_msg_delete():
    def delete_messages(state):
        """Clear messages and add placeholder for Anthropic compatibility"""
        messages = state["messages"]
        
        # Remove all messages
        removal_operations = [RemoveMessage(id=m.id) for m in messages]
        
        # Add a minimal placeholder message
        placeholder = HumanMessage(content="Continue")
        
        return {"messages": removal_operations + [placeholder]}
    
    return delete_messages


class Toolkit:
    _config = DEFAULT_CONFIG.copy()

    @classmethod
    def update_config(cls, config):
        """Update the class-level configuration."""
        cls._config.update(config)

    @property
    def config(self):
        """Access the configuration."""
        return self._config

    def __init__(self, config=None):
        if config:
            self.update_config(config)

    @staticmethod
    @tool
    def get_reddit_news(
        curr_date: Annotated[str, "Date you want to get news for in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve global news from Reddit within a specified time frame.
        Args:
            curr_date (str): Date you want to get news for in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing the latest global news from Reddit in the specified time frame.
        """
        
        global_news_result = interface.get_reddit_global_news(curr_date, 7, 5)

        return global_news_result

    @staticmethod
    @tool
    def get_finnhub_news(
        ticker: Annotated[
            str,
            "Search query of a company, e.g. 'AAPL, TSM, etc.",
        ],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest news about a given stock from Finnhub within a date range
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            start_date (str): Start date in yyyy-mm-dd format
            end_date (str): End date in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing news about the company within the date range from start_date to end_date
        """

        end_date_str = end_date

        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        look_back_days = (end_date - start_date).days

        finnhub_news_result = interface.get_finnhub_news(
            ticker, end_date_str, look_back_days
        )

        return finnhub_news_result

    @staticmethod
    @tool
    def get_reddit_stock_info(
        ticker: Annotated[
            str,
            "Ticker of a company. e.g. AAPL, TSM",
        ],
        curr_date: Annotated[str, "Current date you want to get news for"],
    ) -> str:
        """
        Retrieve the latest news about a given stock from Reddit, given the current date.
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            curr_date (str): current date in yyyy-mm-dd format to get news for
        Returns:
            str: A formatted dataframe containing the latest news about the company on the given date
        """

        stock_news_results = interface.get_reddit_company_news(ticker, curr_date, 7, 5)

        return stock_news_results

    @staticmethod
    @tool
    def get_chinese_social_sentiment(
        ticker: Annotated[str, "Ticker of a company. e.g. AAPL, TSM"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ) -> str:
        """
        获取中国社交媒体和财经平台上关于特定股票的情绪分析和讨论热度。
        整合雪球、东方财富股吧、新浪财经等中国本土平台的数据。
        Args:
            ticker (str): 股票代码，如 AAPL, TSM
            curr_date (str): 当前日期，格式为 yyyy-mm-dd
        Returns:
            str: 包含中国投资者情绪分析、讨论热度、关键观点的格式化报告
        """
        try:
            # 这里可以集成多个中国平台的数据
            chinese_sentiment_results = interface.get_chinese_social_sentiment(ticker, curr_date)
            return chinese_sentiment_results
        except Exception as e:
            # 如果中国平台数据获取失败，回退到原有的Reddit数据
            return interface.get_reddit_company_news(ticker, curr_date, 7, 5)

    @staticmethod
    @tool
    def get_china_stock_data(
        stock_code: Annotated[str, "中国股票代码，如 000001(平安银行), 600519(贵州茅台)"],
        start_date: Annotated[str, "开始日期，格式 yyyy-mm-dd"],
        end_date: Annotated[str, "结束日期，格式 yyyy-mm-dd"],
    ) -> str:
        """
        获取中国A股实时和历史数据，通过通达信API提供高质量的本土股票数据。
        支持实时行情、历史K线、技术指标等全面数据。
        Args:
            stock_code (str): 中国股票代码，如 000001(平安银行), 600519(贵州茅台)
            start_date (str): 开始日期，格式 yyyy-mm-dd
            end_date (str): 结束日期，格式 yyyy-mm-dd
        Returns:
            str: 包含实时行情、历史数据、技术指标的完整股票分析报告
        """
        try:
            print(f"📊 [DEBUG] ===== agent_utils.get_china_stock_data 开始调用 =====")
            print(f"📊 [DEBUG] 参数: stock_code={stock_code}, start_date={start_date}, end_date={end_date}")

            from manufacturingagents.dataflows.tdx_utils import get_china_stock_data
            print(f"📊 [DEBUG] 成功导入 get_china_stock_data 函数")

            print(f"📊 [DEBUG] 正在调用 tdx_utils.get_china_stock_data...")
            result = get_china_stock_data(stock_code, start_date, end_date)

            print(f"📊 [DEBUG] tdx_utils.get_china_stock_data 调用完成")
            print(f"📊 [DEBUG] 返回结果类型: {type(result)}")
            print(f"📊 [DEBUG] 返回结果长度: {len(result) if result else 0}")
            print(f"📊 [DEBUG] 返回结果前200字符: {str(result)[:200]}...")
            print(f"📊 [DEBUG] ===== agent_utils.get_china_stock_data 调用结束 =====")

            return result
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ [DEBUG] ===== agent_utils.get_china_stock_data 异常 =====")
            print(f"❌ [DEBUG] 错误类型: {type(e).__name__}")
            print(f"❌ [DEBUG] 错误信息: {str(e)}")
            print(f"❌ [DEBUG] 详细堆栈:")
            print(error_details)
            print(f"❌ [DEBUG] ===== 异常处理结束 =====")
            return f"中国股票数据获取失败: {str(e)}。建议安装pytdx库: pip install pytdx"

    @staticmethod
    @tool
    def get_china_market_overview(
        curr_date: Annotated[str, "当前日期，格式 yyyy-mm-dd"],
    ) -> str:
        """
        获取中国股市整体概览，包括主要指数的实时行情。
        涵盖上证指数、深证成指、创业板指、科创50等主要指数。
        Args:
            curr_date (str): 当前日期，格式 yyyy-mm-dd
        Returns:
            str: 包含主要指数实时行情的市场概览报告
        """
        try:
            from manufacturingagents.dataflows.tdx_utils import get_china_market_overview
            return get_china_market_overview()
        except Exception as e:
            return f"中国市场概览获取失败: {str(e)}。建议安装pytdx库: pip install pytdx"

    @staticmethod
    @tool
    def get_YFin_data(
        symbol: Annotated[str, "ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve the stock price data for a given ticker symbol from Yahoo Finance.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            start_date (str): Start date in yyyy-mm-dd format
            end_date (str): End date in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
        """

        result_data = interface.get_YFin_data(symbol, start_date, end_date)

        return result_data

    @staticmethod
    @tool
    def get_YFin_data_online(
        symbol: Annotated[str, "ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve the stock price data for a given ticker symbol from Yahoo Finance.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            start_date (str): Start date in yyyy-mm-dd format
            end_date (str): End date in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
        """

        result_data = interface.get_YFin_data_online(symbol, start_date, end_date)

        return result_data

    @staticmethod
    @tool
    def get_stockstats_indicators_report(
        symbol: Annotated[str, "ticker symbol of the company"],
        indicator: Annotated[
            str, "technical indicator to get the analysis and report of"
        ],
        curr_date: Annotated[
            str, "The current trading date you are trading on, YYYY-mm-dd"
        ],
        look_back_days: Annotated[int, "how many days to look back"] = 30,
    ) -> str:
        """
        Retrieve stock stats indicators for a given ticker symbol and indicator.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            indicator (str): Technical indicator to get the analysis and report of
            curr_date (str): The current trading date you are trading on, YYYY-mm-dd
            look_back_days (int): How many days to look back, default is 30
        Returns:
            str: A formatted dataframe containing the stock stats indicators for the specified ticker symbol and indicator.
        """

        result_stockstats = interface.get_stock_stats_indicators_window(
            symbol, indicator, curr_date, look_back_days, False
        )

        return result_stockstats

    @staticmethod
    @tool
    def get_stockstats_indicators_report_online(
        symbol: Annotated[str, "ticker symbol of the company"],
        indicator: Annotated[
            str, "technical indicator to get the analysis and report of"
        ],
        curr_date: Annotated[
            str, "The current trading date you are trading on, YYYY-mm-dd"
        ],
        look_back_days: Annotated[int, "how many days to look back"] = 30,
    ) -> str:
        """
        Retrieve stock stats indicators for a given ticker symbol and indicator.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            indicator (str): Technical indicator to get the analysis and report of
            curr_date (str): The current trading date you are trading on, YYYY-mm-dd
            look_back_days (int): How many days to look back, default is 30
        Returns:
            str: A formatted dataframe containing the stock stats indicators for the specified ticker symbol and indicator.
        """

        result_stockstats = interface.get_stock_stats_indicators_window(
            symbol, indicator, curr_date, look_back_days, True
        )

        return result_stockstats

    @staticmethod
    @tool
    def get_finnhub_company_insider_sentiment(
        ticker: Annotated[str, "ticker symbol for the company"],
        curr_date: Annotated[
            str,
            "current date of you are trading at, yyyy-mm-dd",
        ],
    ):
        """
        Retrieve insider sentiment information about a company (retrieved from public SEC information) for the past 30 days
        Args:
            ticker (str): ticker symbol of the company
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
            str: a report of the sentiment in the past 30 days starting at curr_date
        """

        data_sentiment = interface.get_finnhub_company_insider_sentiment(
            ticker, curr_date, 30
        )

        return data_sentiment

    @staticmethod
    @tool
    def get_finnhub_company_insider_transactions(
        ticker: Annotated[str, "ticker symbol"],
        curr_date: Annotated[
            str,
            "current date you are trading at, yyyy-mm-dd",
        ],
    ):
        """
        Retrieve insider transaction information about a company (retrieved from public SEC information) for the past 30 days
        Args:
            ticker (str): ticker symbol of the company
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
            str: a report of the company's insider transactions/trading information in the past 30 days
        """

        data_trans = interface.get_finnhub_company_insider_transactions(
            ticker, curr_date, 30
        )

        return data_trans

    @staticmethod
    @tool
    def get_simfin_balance_sheet(
        ticker: Annotated[str, "ticker symbol"],
        freq: Annotated[
            str,
            "reporting frequency of the company's financial history: annual/quarterly",
        ],
        curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
    ):
        """
        Retrieve the most recent balance sheet of a company
        Args:
            ticker (str): ticker symbol of the company
            freq (str): reporting frequency of the company's financial history: annual / quarterly
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
            str: a report of the company's most recent balance sheet
        """

        data_balance_sheet = interface.get_simfin_balance_sheet(ticker, freq, curr_date)

        return data_balance_sheet

    @staticmethod
    @tool
    def get_simfin_cashflow(
        ticker: Annotated[str, "ticker symbol"],
        freq: Annotated[
            str,
            "reporting frequency of the company's financial history: annual/quarterly",
        ],
        curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
    ):
        """
        Retrieve the most recent cash flow statement of a company
        Args:
            ticker (str): ticker symbol of the company
            freq (str): reporting frequency of the company's financial history: annual / quarterly
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
                str: a report of the company's most recent cash flow statement
        """

        data_cashflow = interface.get_simfin_cashflow(ticker, freq, curr_date)

        return data_cashflow

    @staticmethod
    @tool
    def get_simfin_income_stmt(
        ticker: Annotated[str, "ticker symbol"],
        freq: Annotated[
            str,
            "reporting frequency of the company's financial history: annual/quarterly",
        ],
        curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
    ):
        """
        Retrieve the most recent income statement of a company
        Args:
            ticker (str): ticker symbol of the company
            freq (str): reporting frequency of the company's financial history: annual / quarterly
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
                str: a report of the company's most recent income statement
        """

        data_income_stmt = interface.get_simfin_income_statements(
            ticker, freq, curr_date
        )

        return data_income_stmt

    @staticmethod
    @tool
    def get_google_news(
        query: Annotated[str, "Query to search with"],
        curr_date: Annotated[str, "Curr date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest news from Google News based on a query and date range.
        Args:
            query (str): Query to search with
            curr_date (str): Current date in yyyy-mm-dd format
            look_back_days (int): How many days to look back
        Returns:
            str: A formatted string containing the latest news from Google News based on the query and date range.
        """

        google_news_results = interface.get_google_news(query, curr_date, 7)

        return google_news_results

    @staticmethod
    @tool
    def get_realtime_stock_news(
        ticker: Annotated[str, "Ticker of a company. e.g. AAPL, TSM"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ) -> str:
        """
        获取股票的实时新闻分析，解决传统新闻源的滞后性问题。
        整合多个专业财经API，提供15-30分钟内的最新新闻。
        Args:
            ticker (str): 股票代码，如 AAPL, TSM
            curr_date (str): 当前日期，格式为 yyyy-mm-dd
        Returns:
            str: 包含实时新闻分析、紧急程度评估、时效性说明的格式化报告
        """
        try:
            from manufacturingagents.dataflows.realtime_news_utils import get_realtime_stock_news
            return get_realtime_stock_news(ticker, curr_date, hours_back=6)
        except Exception as e:
            # 如果实时新闻获取失败，回退到Google新闻
            return interface.get_google_news(f"{ticker} stock news", curr_date, 1)

    @staticmethod
    @tool
    def get_stock_news_openai(
        ticker: Annotated[str, "the company's ticker"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest news about a given stock by using OpenAI's news API.
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            curr_date (str): Current date in yyyy-mm-dd format
        Returns:
            str: A formatted string containing the latest news about the company on the given date.
        """

        openai_news_results = interface.get_stock_news_openai(ticker, curr_date)

        return openai_news_results

    @staticmethod
    @tool
    def get_global_news_openai(
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest macroeconomics news on a given date using OpenAI's macroeconomics news API.
        Args:
            curr_date (str): Current date in yyyy-mm-dd format
        Returns:
            str: A formatted string containing the latest macroeconomic news on the given date.
        """

        openai_news_results = interface.get_global_news_openai(curr_date)

        return openai_news_results

    @staticmethod
    @tool
    def get_fundamentals_openai(
        ticker: Annotated[str, "the company's ticker"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest fundamental information about a given stock on a given date by using OpenAI's news API.
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            curr_date (str): Current date in yyyy-mm-dd format
        Returns:
            str: A formatted string containing the latest fundamental information about the company on the given date.
        """
        print(f"📊 [DEBUG] get_fundamentals_openai 被调用: ticker={ticker}, date={curr_date}")

        # 检查是否为中国股票
        import re
        if re.match(r'^\d{6}$', str(ticker)):
            print(f"📊 [DEBUG] 检测到中国A股代码: {ticker}")
            # 从MongoDB获取中国股票名称
            try:
                from manufacturingagents.dataflows.tdx_utils import _get_stock_name_from_mongodb
                company_name = _get_stock_name_from_mongodb(ticker)
                if not company_name:
                    company_name = f"股票代码{ticker}"
                print(f"📊 [DEBUG] 中国股票名称映射: {ticker} -> {company_name}")
            except Exception as e:
                print(f"⚠️ [DEBUG] 从MongoDB获取股票名称失败: {e}")
                company_name = f"股票代码{ticker}"

            # 修改查询以包含正确的公司名称
            modified_query = f"{company_name}({ticker})"
            print(f"📊 [DEBUG] 修改后的查询: {modified_query}")
        else:
            print(f"📊 [DEBUG] 检测到非中国股票: {ticker}")
            modified_query = ticker

        try:
            openai_fundamentals_results = interface.get_fundamentals_openai(
                modified_query, curr_date
            )
            print(f"📊 [DEBUG] OpenAI基本面分析结果长度: {len(openai_fundamentals_results) if openai_fundamentals_results else 0}")
            return openai_fundamentals_results
        except Exception as e:
            print(f"❌ [DEBUG] OpenAI基本面分析失败: {str(e)}")
            return f"基本面分析失败: {str(e)}"

    @staticmethod
    @tool
    def get_china_fundamentals(
        ticker: Annotated[str, "中国A股股票代码，如600036"],
        curr_date: Annotated[str, "当前日期，格式为yyyy-mm-dd"],
    ):
        """
        获取中国A股股票的基本面信息，使用通达信数据源。
        Args:
            ticker (str): 中国A股股票代码，如600036, 000001
            curr_date (str): 当前日期，格式为yyyy-mm-dd
        Returns:
            str: 包含股票基本面信息的格式化字符串
        """
        print(f"📊 [DEBUG] get_china_fundamentals 被调用: ticker={ticker}, date={curr_date}")

        # 检查是否为中国股票
        import re
        if not re.match(r'^\d{6}$', str(ticker)):
            return f"错误：{ticker} 不是有效的中国A股代码格式"

        try:
            # 从MongoDB获取股票名称
            from manufacturingagents.dataflows.tdx_utils import _get_stock_name_from_mongodb
            company_name = _get_stock_name_from_mongodb(ticker)
            if not company_name:
                company_name = f"股票代码{ticker}"

            print(f"📊 [DEBUG] 中国股票名称: {company_name}")

            # 构建基本面分析提示
            query = f"请对{company_name}({ticker})进行详细的基本面分析，包括：1.公司基本情况 2.财务状况分析 3.行业地位 4.竞争优势 5.投资价值评估。"

            # 调用OpenAI基本面分析
            openai_fundamentals_results = interface.get_fundamentals_openai(
                company_name, curr_date
            )

            print(f"📊 [DEBUG] 中国基本面分析完成，结果长度: {len(openai_fundamentals_results) if openai_fundamentals_results else 0}")
            return openai_fundamentals_results

        except Exception as e:
            print(f"❌ [DEBUG] 中国基本面分析失败: {str(e)}")
            return f"中国股票基本面分析失败: {str(e)}"

    # === 制造业专用工具函数 ===
    
    @staticmethod
    @tool
    def get_manufacturing_weather_data(
        city_name: Annotated[str, "城市名称，如'广州'"],
    ):
        """
        获取制造业相关的天气预报数据，用于分析天气对产品需求的影响
        Args:
            city_name (str): 城市名称
        Returns:
            str: 天气预报数据的格式化字符串
        """
        print(f"🌤️ [TOOLKIT] get_manufacturing_weather_data 被调用: city={city_name}")
        
        try:
            # 调用interface层函数，遵循原架构数据流
            from datetime import datetime
            import manufacturingagents.dataflows.interface as interface
            
            curr_date = datetime.now().strftime('%Y-%m-%d')
            result = interface.get_manufacturing_weather_interface(city_name, curr_date)
            
            # 🎯 修复：检查返回结果是否为错误消息
            if result.startswith("❌") or "失败" in result or "错误" in result:
                print(f"❌ [TOOLKIT] 天气数据获取失败: {city_name}")
                return result  # 返回具体错误信息，不使用降级
            else:
                print(f"✅ [TOOLKIT] 天气数据获取成功: {city_name}")
                return result
                
        except Exception as e:
            print(f"❌ [TOOLKIT] 天气数据获取失败: {str(e)}")
            return f"天气数据获取失败: {str(e)}"

    @staticmethod
    @tool
    def get_manufacturing_news_data(
        query_params: Annotated[Union[str, dict], "新闻查询参数，支持结构化字典或字符串格式"],
    ):
        """
        获取制造业相关的新闻数据，用于分析市场动态和政策影响
        Args:
            query_params (dict|str): 新闻查询参数，支持结构化字典或字符串
        Returns:
            str: 新闻数据的格式化字符串
        """
        print(f"📰 [TOOLKIT] get_manufacturing_news_data 被调用: query={query_params}")
        
        try:
            # 调用interface层函数，遵循原架构数据流
            from datetime import datetime
            import manufacturingagents.dataflows.interface as interface
            
            curr_date = datetime.now().strftime('%Y-%m-%d')
            
            # 🎯 修复：支持字典和字符串参数
            result = interface.get_manufacturing_news_interface(query_params, curr_date)
            
            # 🎯 修复：检查返回结果是否为错误消息
            if result.startswith("❌") or "失败" in result or "错误" in result:
                print(f"❌ [TOOLKIT] 新闻数据获取失败")
                return result  # 返回具体错误信息，不使用降级
            else:
                print(f"✅ [TOOLKIT] 新闻数据获取成功")
                return result
                
        except Exception as e:
            print(f"❌ [TOOLKIT] 新闻数据获取失败: {str(e)}")
            return f"新闻数据获取失败: {str(e)}"

    @staticmethod
    @tool
    def get_manufacturing_holiday_data(
        date_range: Annotated[str, "日期范围，如'2025-07到2025-10'"],
    ):
        """
        获取节假日数据，用于分析节假日对制造业需求的影响
        Args:
            date_range (str): 日期范围
        Returns:
            str: 节假日数据的格式化字符串
        """
        print(f"📅 [TOOLKIT] get_manufacturing_holiday_data 被调用: range={date_range}")
        
        try:
            # 调用interface层函数，遵循原架构数据流
            import manufacturingagents.dataflows.interface as interface
            
            result = interface.get_manufacturing_holiday_interface(date_range)
            
            # 🎯 修复：检查返回结果是否为错误消息
            if result.startswith("❌") or "失败" in result or "错误" in result:
                print(f"❌ [TOOLKIT] 节假日数据获取失败")
                return result  # 返回具体错误信息，不使用降级
            else:
                print(f"✅ [TOOLKIT] 节假日数据获取成功: {date_range}")
                return result
                
        except Exception as e:
            print(f"❌ [TOOLKIT] 节假日数据获取失败: {str(e)}")
            return f"节假日数据获取失败: {str(e)}"

    @staticmethod
    @tool
    def get_manufacturing_pmi_data(
        time_range: Annotated[str, "时间范围，如'最近3个月'"],
    ):
        """
        获取PMI制造业采购经理指数，用于分析宏观经济环境
        Args:
            time_range (str): 时间范围描述
        Returns:
            str: PMI数据的格式化字符串
        """
        print(f"📈 [TOOLKIT] get_manufacturing_pmi_data 被调用: range={time_range}")
        
        try:
            # 调用interface层函数，遵循原架构数据流
            import manufacturingagents.dataflows.interface as interface
            
            result = interface.get_manufacturing_economic_interface('pmi', time_range)
            
            print(f"✅ [TOOLKIT] PMI数据获取成功")
            return result
                
        except Exception as e:
            print(f"❌ [TOOLKIT] PMI数据获取失败: {str(e)}")
            return f"PMI数据获取失败: {str(e)}"

    @staticmethod
    @tool
    def get_manufacturing_ppi_data(
        time_range: Annotated[str, "时间范围，如'最近3个月'"],
    ):
        """
        获取PPI工业生产者价格指数，用于分析原材料价格趋势
        Args:
            time_range (str): 时间范围描述
        Returns:
            str: PPI数据的格式化字符串
        """
        print(f"📈 [TOOLKIT] get_manufacturing_ppi_data 被调用: range={time_range}")
        
        try:
            # 调用interface层函数，遵循原架构数据流
            import manufacturingagents.dataflows.interface as interface
            
            result = interface.get_manufacturing_economic_interface('ppi', time_range)
            
            print(f"✅ [TOOLKIT] PPI数据获取成功")
            return result

        except Exception as e:
            print(f"❌ [TOOLKIT] PPI数据获取失败: {str(e)}")
            return f"PPI数据获取失败: {str(e)}"

    @staticmethod
    @tool
    def get_manufacturing_commodity_data(
        commodity_type: Annotated[str, "商品类型，如'铜期货'"],
    ):
        """
        获取大宗商品期货数据，用于分析原材料价格趋势
        Args:
            commodity_type (str): 商品类型
        Returns:
            str: 期货数据的格式化字符串
        """
        print(f"📈 [TOOLKIT] get_manufacturing_commodity_data 被调用: type={commodity_type}")
        
        try:
            # 调用interface层函数，遵循原架构数据流
            import manufacturingagents.dataflows.interface as interface
            
            result = interface.get_manufacturing_economic_interface('commodity', '最近1个月', commodity_type)
            
            # 🎯 修复：检查返回结果是否为错误消息
            if result.startswith("❌") or "失败" in result or "错误" in result:
                print(f"❌ [TOOLKIT] 期货数据获取失败")
                return result  # 返回具体错误信息，不使用降级
            else:
                print(f"✅ [TOOLKIT] 期货数据获取成功")
                return result
                
        except Exception as e:
            print(f"❌ [TOOLKIT] 期货数据获取失败: {str(e)}")
            return f"期货数据获取失败: {str(e)}"
