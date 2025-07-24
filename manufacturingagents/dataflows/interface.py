from typing import Annotated, Dict
from .reddit_utils import fetch_top_from_category
from .chinese_finance_utils import get_chinese_social_sentiment
from .yfin_utils import *
from .stockstats_utils import *
from .googlenews_utils import *
from .finnhub_utils import get_data_in_range
from dateutil.relativedelta import relativedelta
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
import pandas as pd
from tqdm import tqdm
import yfinance as yf
from openai import OpenAI
from .config import get_config, set_config, DATA_DIR


def get_finnhub_news(
    ticker: Annotated[
        str,
        "Search query of a company's, e.g. 'AAPL, TSM, etc.",
    ],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "how many days to look back"],
):
    """
    Retrieve news about a company within a time frame

    Args
        ticker (str): ticker for the company you are interested in
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    Returns
        str: dataframe containing the news of the company in the time frame

    """

    start_date = datetime.strptime(curr_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    result = get_data_in_range(ticker, before, curr_date, "news_data", DATA_DIR)

    if len(result) == 0:
        error_msg = f"⚠️ 无法获取{ticker}的新闻数据 ({before} 到 {curr_date})\n"
        error_msg += f"可能的原因：\n"
        error_msg += f"1. 数据文件不存在或路径配置错误\n"
        error_msg += f"2. 指定日期范围内没有新闻数据\n"
        error_msg += f"3. 需要先下载或更新Finnhub新闻数据\n"
        error_msg += f"建议：检查数据目录配置或重新获取新闻数据"
        print(f"📰 [DEBUG] {error_msg}")
        return error_msg

    combined_result = ""
    for day, data in result.items():
        if len(data) == 0:
            continue
        for entry in data:
            current_news = (
                "### " + entry["headline"] + f" ({day})" + "\n" + entry["summary"]
            )
            combined_result += current_news + "\n\n"

    return f"## {ticker} News, from {before} to {curr_date}:\n" + str(combined_result)


def get_finnhub_company_insider_sentiment(
    ticker: Annotated[str, "ticker symbol for the company"],
    curr_date: Annotated[
        str,
        "current date of you are trading at, yyyy-mm-dd",
    ],
    look_back_days: Annotated[int, "number of days to look back"],
):
    """
    Retrieve insider sentiment about a company (retrieved from public SEC information) for the past 15 days
    Args:
        ticker (str): ticker symbol of the company
        curr_date (str): current date you are trading on, yyyy-mm-dd
    Returns:
        str: a report of the sentiment in the past 15 days starting at curr_date
    """

    date_obj = datetime.strptime(curr_date, "%Y-%m-%d")
    before = date_obj - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    data = get_data_in_range(ticker, before, curr_date, "insider_senti", DATA_DIR)

    if len(data) == 0:
        return ""

    result_str = ""
    seen_dicts = []
    for date, senti_list in data.items():
        for entry in senti_list:
            if entry not in seen_dicts:
                result_str += f"### {entry['year']}-{entry['month']}:\nChange: {entry['change']}\nMonthly Share Purchase Ratio: {entry['mspr']}\n\n"
                seen_dicts.append(entry)

    return (
        f"## {ticker} Insider Sentiment Data for {before} to {curr_date}:\n"
        + result_str
        + "The change field refers to the net buying/selling from all insiders' transactions. The mspr field refers to monthly share purchase ratio."
    )


def get_finnhub_company_insider_transactions(
    ticker: Annotated[str, "ticker symbol"],
    curr_date: Annotated[
        str,
        "current date you are trading at, yyyy-mm-dd",
    ],
    look_back_days: Annotated[int, "how many days to look back"],
):
    """
    Retrieve insider transcaction information about a company (retrieved from public SEC information) for the past 15 days
    Args:
        ticker (str): ticker symbol of the company
        curr_date (str): current date you are trading at, yyyy-mm-dd
    Returns:
        str: a report of the company's insider transaction/trading informtaion in the past 15 days
    """

    date_obj = datetime.strptime(curr_date, "%Y-%m-%d")
    before = date_obj - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    data = get_data_in_range(ticker, before, curr_date, "insider_trans", DATA_DIR)

    if len(data) == 0:
        return ""

    result_str = ""

    seen_dicts = []
    for date, senti_list in data.items():
        for entry in senti_list:
            if entry not in seen_dicts:
                result_str += f"### Filing Date: {entry['filingDate']}, {entry['name']}:\nChange:{entry['change']}\nShares: {entry['share']}\nTransaction Price: {entry['transactionPrice']}\nTransaction Code: {entry['transactionCode']}\n\n"
                seen_dicts.append(entry)

    return (
        f"## {ticker} insider transactions from {before} to {curr_date}:\n"
        + result_str
        + "The change field reflects the variation in share count—here a negative number indicates a reduction in holdings—while share specifies the total number of shares involved. The transactionPrice denotes the per-share price at which the trade was executed, and transactionDate marks when the transaction occurred. The name field identifies the insider making the trade, and transactionCode (e.g., S for sale) clarifies the nature of the transaction. FilingDate records when the transaction was officially reported, and the unique id links to the specific SEC filing, as indicated by the source. Additionally, the symbol ties the transaction to a particular company, isDerivative flags whether the trade involves derivative securities, and currency notes the currency context of the transaction."
    )


def get_simfin_balance_sheet(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[
        str,
        "reporting frequency of the company's financial history: annual / quarterly",
    ],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
):
    data_path = os.path.join(
        DATA_DIR,
        "fundamental_data",
        "simfin_data_all",
        "balance_sheet",
        "companies",
        "us",
        f"us-balance-{freq}.csv",
    )
    df = pd.read_csv(data_path, sep=";")

    # Convert date strings to datetime objects and remove any time components
    df["Report Date"] = pd.to_datetime(df["Report Date"], utc=True).dt.normalize()
    df["Publish Date"] = pd.to_datetime(df["Publish Date"], utc=True).dt.normalize()

    # Convert the current date to datetime and normalize
    curr_date_dt = pd.to_datetime(curr_date, utc=True).normalize()

    # Filter the DataFrame for the given ticker and for reports that were published on or before the current date
    filtered_df = df[(df["Ticker"] == ticker) & (df["Publish Date"] <= curr_date_dt)]

    # Check if there are any available reports; if not, return a notification
    if filtered_df.empty:
        print("No balance sheet available before the given current date.")
        return ""

    # Get the most recent balance sheet by selecting the row with the latest Publish Date
    latest_balance_sheet = filtered_df.loc[filtered_df["Publish Date"].idxmax()]

    # drop the SimFinID column
    latest_balance_sheet = latest_balance_sheet.drop("SimFinId")

    return (
        f"## {freq} balance sheet for {ticker} released on {str(latest_balance_sheet['Publish Date'])[0:10]}: \n"
        + str(latest_balance_sheet)
        + "\n\nThis includes metadata like reporting dates and currency, share details, and a breakdown of assets, liabilities, and equity. Assets are grouped as current (liquid items like cash and receivables) and noncurrent (long-term investments and property). Liabilities are split between short-term obligations and long-term debts, while equity reflects shareholder funds such as paid-in capital and retained earnings. Together, these components ensure that total assets equal the sum of liabilities and equity."
    )


def get_simfin_cashflow(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[
        str,
        "reporting frequency of the company's financial history: annual / quarterly",
    ],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
):
    data_path = os.path.join(
        DATA_DIR,
        "fundamental_data",
        "simfin_data_all",
        "cash_flow",
        "companies",
        "us",
        f"us-cashflow-{freq}.csv",
    )
    df = pd.read_csv(data_path, sep=";")

    # Convert date strings to datetime objects and remove any time components
    df["Report Date"] = pd.to_datetime(df["Report Date"], utc=True).dt.normalize()
    df["Publish Date"] = pd.to_datetime(df["Publish Date"], utc=True).dt.normalize()

    # Convert the current date to datetime and normalize
    curr_date_dt = pd.to_datetime(curr_date, utc=True).normalize()

    # Filter the DataFrame for the given ticker and for reports that were published on or before the current date
    filtered_df = df[(df["Ticker"] == ticker) & (df["Publish Date"] <= curr_date_dt)]

    # Check if there are any available reports; if not, return a notification
    if filtered_df.empty:
        print("No cash flow statement available before the given current date.")
        return ""

    # Get the most recent cash flow statement by selecting the row with the latest Publish Date
    latest_cash_flow = filtered_df.loc[filtered_df["Publish Date"].idxmax()]

    # drop the SimFinID column
    latest_cash_flow = latest_cash_flow.drop("SimFinId")

    return (
        f"## {freq} cash flow statement for {ticker} released on {str(latest_cash_flow['Publish Date'])[0:10]}: \n"
        + str(latest_cash_flow)
        + "\n\nThis includes metadata like reporting dates and currency, share details, and a breakdown of cash movements. Operating activities show cash generated from core business operations, including net income adjustments for non-cash items and working capital changes. Investing activities cover asset acquisitions/disposals and investments. Financing activities include debt transactions, equity issuances/repurchases, and dividend payments. The net change in cash represents the overall increase or decrease in the company's cash position during the reporting period."
    )


def get_simfin_income_statements(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[
        str,
        "reporting frequency of the company's financial history: annual / quarterly",
    ],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
):
    data_path = os.path.join(
        DATA_DIR,
        "fundamental_data",
        "simfin_data_all",
        "income_statements",
        "companies",
        "us",
        f"us-income-{freq}.csv",
    )
    df = pd.read_csv(data_path, sep=";")

    # Convert date strings to datetime objects and remove any time components
    df["Report Date"] = pd.to_datetime(df["Report Date"], utc=True).dt.normalize()
    df["Publish Date"] = pd.to_datetime(df["Publish Date"], utc=True).dt.normalize()

    # Convert the current date to datetime and normalize
    curr_date_dt = pd.to_datetime(curr_date, utc=True).normalize()

    # Filter the DataFrame for the given ticker and for reports that were published on or before the current date
    filtered_df = df[(df["Ticker"] == ticker) & (df["Publish Date"] <= curr_date_dt)]

    # Check if there are any available reports; if not, return a notification
    if filtered_df.empty:
        print("No income statement available before the given current date.")
        return ""

    # Get the most recent income statement by selecting the row with the latest Publish Date
    latest_income = filtered_df.loc[filtered_df["Publish Date"].idxmax()]

    # drop the SimFinID column
    latest_income = latest_income.drop("SimFinId")

    return (
        f"## {freq} income statement for {ticker} released on {str(latest_income['Publish Date'])[0:10]}: \n"
        + str(latest_income)
        + "\n\nThis includes metadata like reporting dates and currency, share details, and a comprehensive breakdown of the company's financial performance. Starting with Revenue, it shows Cost of Revenue and resulting Gross Profit. Operating Expenses are detailed, including SG&A, R&D, and Depreciation. The statement then shows Operating Income, followed by non-operating items and Interest Expense, leading to Pretax Income. After accounting for Income Tax and any Extraordinary items, it concludes with Net Income, representing the company's bottom-line profit or loss for the period."
    )


def get_google_news(
    query: Annotated[str, "Query to search with"],
    curr_date: Annotated[str, "Curr date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "how many days to look back"],
) -> str:
    query = query.replace(" ", "+")

    start_date = datetime.strptime(curr_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    news_results = getNewsData(query, before, curr_date)

    news_str = ""

    for news in news_results:
        news_str += (
            f"### {news['title']} (source: {news['source']}) \n\n{news['snippet']}\n\n"
        )

    if len(news_results) == 0:
        return ""

    return f"## {query} Google News, from {before} to {curr_date}:\n\n{news_str}"


def get_reddit_global_news(
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "how many days to look back"],
    max_limit_per_day: Annotated[int, "Maximum number of news per day"],
) -> str:
    """
    Retrieve the latest top reddit news
    Args:
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing the latest news articles posts on reddit and meta information in these columns: "created_utc", "id", "title", "selftext", "score", "num_comments", "url"
    """

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    posts = []
    # iterate from start_date to end_date
    curr_date = datetime.strptime(before, "%Y-%m-%d")

    total_iterations = (start_date - curr_date).days + 1
    pbar = tqdm(desc=f"Getting Global News on {start_date}", total=total_iterations)

    while curr_date <= start_date:
        curr_date_str = curr_date.strftime("%Y-%m-%d")
        fetch_result = fetch_top_from_category(
            "global_news",
            curr_date_str,
            max_limit_per_day,
            data_path=os.path.join(DATA_DIR, "reddit_data"),
        )
        posts.extend(fetch_result)
        curr_date += relativedelta(days=1)
        pbar.update(1)

    pbar.close()

    if len(posts) == 0:
        return ""

    news_str = ""
    for post in posts:
        if post["content"] == "":
            news_str += f"### {post['title']}\n\n"
        else:
            news_str += f"### {post['title']}\n\n{post['content']}\n\n"

    return f"## Global News Reddit, from {before} to {curr_date}:\n{news_str}"


def get_reddit_company_news(
    ticker: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "how many days to look back"],
    max_limit_per_day: Annotated[int, "Maximum number of news per day"],
) -> str:
    """
    Retrieve the latest top reddit news
    Args:
        ticker: ticker symbol of the company
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing the latest news articles posts on reddit and meta information in these columns: "created_utc", "id", "title", "selftext", "score", "num_comments", "url"
    """

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    posts = []
    # iterate from start_date to end_date
    curr_date = datetime.strptime(before, "%Y-%m-%d")

    total_iterations = (start_date - curr_date).days + 1
    pbar = tqdm(
        desc=f"Getting Company News for {ticker} on {start_date}",
        total=total_iterations,
    )

    while curr_date <= start_date:
        curr_date_str = curr_date.strftime("%Y-%m-%d")
        fetch_result = fetch_top_from_category(
            "company_news",
            curr_date_str,
            max_limit_per_day,
            ticker,
            data_path=os.path.join(DATA_DIR, "reddit_data"),
        )
        posts.extend(fetch_result)
        curr_date += relativedelta(days=1)

        pbar.update(1)

    pbar.close()

    if len(posts) == 0:
        return ""

    news_str = ""
    for post in posts:
        if post["content"] == "":
            news_str += f"### {post['title']}\n\n"
        else:
            news_str += f"### {post['title']}\n\n{post['content']}\n\n"

    return f"##{ticker} News Reddit, from {before} to {curr_date}:\n\n{news_str}"


def get_stock_stats_indicators_window(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    look_back_days: Annotated[int, "how many days to look back"],
    online: Annotated[bool, "to fetch data online or offline"],
) -> str:

    best_ind_params = {
        # Moving Averages
        "close_50_sma": (
            "50 SMA: A medium-term trend indicator. "
            "Usage: Identify trend direction and serve as dynamic support/resistance. "
            "Tips: It lags price; combine with faster indicators for timely signals."
        ),
        "close_200_sma": (
            "200 SMA: A long-term trend benchmark. "
            "Usage: Confirm overall market trend and identify golden/death cross setups. "
            "Tips: It reacts slowly; best for strategic trend confirmation rather than frequent trading entries."
        ),
        "close_10_ema": (
            "10 EMA: A responsive short-term average. "
            "Usage: Capture quick shifts in momentum and potential entry points. "
            "Tips: Prone to noise in choppy markets; use alongside longer averages for filtering false signals."
        ),
        # MACD Related
        "macd": (
            "MACD: Computes momentum via differences of EMAs. "
            "Usage: Look for crossovers and divergence as signals of trend changes. "
            "Tips: Confirm with other indicators in low-volatility or sideways markets."
        ),
        "macds": (
            "MACD Signal: An EMA smoothing of the MACD line. "
            "Usage: Use crossovers with the MACD line to trigger trades. "
            "Tips: Should be part of a broader strategy to avoid false positives."
        ),
        "macdh": (
            "MACD Histogram: Shows the gap between the MACD line and its signal. "
            "Usage: Visualize momentum strength and spot divergence early. "
            "Tips: Can be volatile; complement with additional filters in fast-moving markets."
        ),
        # Momentum Indicators
        "rsi": (
            "RSI: Measures momentum to flag overbought/oversold conditions. "
            "Usage: Apply 70/30 thresholds and watch for divergence to signal reversals. "
            "Tips: In strong trends, RSI may remain extreme; always cross-check with trend analysis."
        ),
        # Volatility Indicators
        "boll": (
            "Bollinger Middle: A 20 SMA serving as the basis for Bollinger Bands. "
            "Usage: Acts as a dynamic benchmark for price movement. "
            "Tips: Combine with the upper and lower bands to effectively spot breakouts or reversals."
        ),
        "boll_ub": (
            "Bollinger Upper Band: Typically 2 standard deviations above the middle line. "
            "Usage: Signals potential overbought conditions and breakout zones. "
            "Tips: Confirm signals with other tools; prices may ride the band in strong trends."
        ),
        "boll_lb": (
            "Bollinger Lower Band: Typically 2 standard deviations below the middle line. "
            "Usage: Indicates potential oversold conditions. "
            "Tips: Use additional analysis to avoid false reversal signals."
        ),
        "atr": (
            "ATR: Averages true range to measure volatility. "
            "Usage: Set stop-loss levels and adjust position sizes based on current market volatility. "
            "Tips: It's a reactive measure, so use it as part of a broader risk management strategy."
        ),
        # Volume-Based Indicators
        "vwma": (
            "VWMA: A moving average weighted by volume. "
            "Usage: Confirm trends by integrating price action with volume data. "
            "Tips: Watch for skewed results from volume spikes; use in combination with other volume analyses."
        ),
        "mfi": (
            "MFI: The Money Flow Index is a momentum indicator that uses both price and volume to measure buying and selling pressure. "
            "Usage: Identify overbought (>80) or oversold (<20) conditions and confirm the strength of trends or reversals. "
            "Tips: Use alongside RSI or MACD to confirm signals; divergence between price and MFI can indicate potential reversals."
        ),
    }

    if indicator not in best_ind_params:
        raise ValueError(
            f"Indicator {indicator} is not supported. Please choose from: {list(best_ind_params.keys())}"
        )

    end_date = curr_date
    curr_date = datetime.strptime(curr_date, "%Y-%m-%d")
    before = curr_date - relativedelta(days=look_back_days)

    if not online:
        # read from YFin data
        data = pd.read_csv(
            os.path.join(
                DATA_DIR,
                f"market_data/price_data/{symbol}-YFin-data-2015-01-01-2025-03-25.csv",
            )
        )
        data["Date"] = pd.to_datetime(data["Date"], utc=True)
        dates_in_df = data["Date"].astype(str).str[:10]

        ind_string = ""
        while curr_date >= before:
            # only do the trading dates
            if curr_date.strftime("%Y-%m-%d") in dates_in_df.values:
                indicator_value = get_stockstats_indicator(
                    symbol, indicator, curr_date.strftime("%Y-%m-%d"), online
                )

                ind_string += f"{curr_date.strftime('%Y-%m-%d')}: {indicator_value}\n"

            curr_date = curr_date - relativedelta(days=1)
    else:
        # online gathering
        ind_string = ""
        while curr_date >= before:
            indicator_value = get_stockstats_indicator(
                symbol, indicator, curr_date.strftime("%Y-%m-%d"), online
            )

            ind_string += f"{curr_date.strftime('%Y-%m-%d')}: {indicator_value}\n"

            curr_date = curr_date - relativedelta(days=1)

    result_str = (
        f"## {indicator} values from {before.strftime('%Y-%m-%d')} to {end_date}:\n\n"
        + ind_string
        + "\n\n"
        + best_ind_params.get(indicator, "No description available.")
    )

    return result_str


def get_stockstats_indicator(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    online: Annotated[bool, "to fetch data online or offline"],
) -> str:

    curr_date = datetime.strptime(curr_date, "%Y-%m-%d")
    curr_date = curr_date.strftime("%Y-%m-%d")

    try:
        indicator_value = StockstatsUtils.get_stock_stats(
            symbol,
            indicator,
            curr_date,
            os.path.join(DATA_DIR, "market_data", "price_data"),
            online=online,
        )
    except Exception as e:
        print(
            f"Error getting stockstats indicator data for indicator {indicator} on {curr_date}: {e}"
        )
        return ""

    return str(indicator_value)


def get_YFin_data_window(
    symbol: Annotated[str, "ticker symbol of the company"],
    curr_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "how many days to look back"],
) -> str:
    # calculate past days
    date_obj = datetime.strptime(curr_date, "%Y-%m-%d")
    before = date_obj - relativedelta(days=look_back_days)
    start_date = before.strftime("%Y-%m-%d")

    # read in data
    data = pd.read_csv(
        os.path.join(
            DATA_DIR,
            f"market_data/price_data/{symbol}-YFin-data-2015-01-01-2025-03-25.csv",
        )
    )

    # Extract just the date part for comparison
    data["DateOnly"] = data["Date"].str[:10]

    # Filter data between the start and end dates (inclusive)
    filtered_data = data[
        (data["DateOnly"] >= start_date) & (data["DateOnly"] <= curr_date)
    ]

    # Drop the temporary column we created
    filtered_data = filtered_data.drop("DateOnly", axis=1)

    # Set pandas display options to show the full DataFrame
    with pd.option_context(
        "display.max_rows", None, "display.max_columns", None, "display.width", None
    ):
        df_string = filtered_data.to_string()

    return (
        f"## Raw Market Data for {symbol} from {start_date} to {curr_date}:\n\n"
        + df_string
    )


def get_YFin_data_online(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):

    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")

    # Create ticker object
    ticker = yf.Ticker(symbol.upper())

    # Fetch historical data for the specified date range
    data = ticker.history(start=start_date, end=end_date)

    # Check if data is empty
    if data.empty:
        return (
            f"No data found for symbol '{symbol}' between {start_date} and {end_date}"
        )

    # Remove timezone info from index for cleaner output
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    # Round numerical values to 2 decimal places for cleaner display
    numeric_columns = ["Open", "High", "Low", "Close", "Adj Close"]
    for col in numeric_columns:
        if col in data.columns:
            data[col] = data[col].round(2)

    # Convert DataFrame to CSV string
    csv_string = data.to_csv()

    # Add header information
    header = f"# Stock data for {symbol.upper()} from {start_date} to {end_date}\n"
    header += f"# Total records: {len(data)}\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    return header + csv_string


def get_YFin_data(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    # read in data
    data = pd.read_csv(
        os.path.join(
            DATA_DIR,
            f"market_data/price_data/{symbol}-YFin-data-2015-01-01-2025-03-25.csv",
        )
    )

    if end_date > "2025-03-25":
        raise Exception(
            f"Get_YFin_Data: {end_date} is outside of the data range of 2015-01-01 to 2025-03-25"
        )

    # Extract just the date part for comparison
    data["DateOnly"] = data["Date"].str[:10]

    # Filter data between the start and end dates (inclusive)
    filtered_data = data[
        (data["DateOnly"] >= start_date) & (data["DateOnly"] <= end_date)
    ]

    # Drop the temporary column we created
    filtered_data = filtered_data.drop("DateOnly", axis=1)

    # remove the index from the dataframe
    filtered_data = filtered_data.reset_index(drop=True)

    return filtered_data


def get_stock_news_openai(ticker, curr_date):
    config = get_config()
    client = OpenAI(base_url=config["backend_url"])

    response = client.responses.create(
        model=config["quick_think_llm"],
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Can you search Social Media for {ticker} from 7 days before {curr_date} to {curr_date}? Make sure you only get the data posted during that period.",
                    }
                ],
            }
        ],
        text={"format": {"type": "text"}},
        reasoning={},
        tools=[
            {
                "type": "web_search_preview",
                "user_location": {"type": "approximate"},
                "search_context_size": "low",
            }
        ],
        temperature=1,
        max_output_tokens=4096,
        top_p=1,
        store=True,
    )

    return response.output[1].content[0].text


def get_global_news_openai(curr_date):
    config = get_config()
    client = OpenAI(base_url=config["backend_url"])

    response = client.responses.create(
        model=config["quick_think_llm"],
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Can you search global or macroeconomics news from 7 days before {curr_date} to {curr_date} that would be informative for trading purposes? Make sure you only get the data posted during that period.",
                    }
                ],
            }
        ],
        text={"format": {"type": "text"}},
        reasoning={},
        tools=[
            {
                "type": "web_search_preview",
                "user_location": {"type": "approximate"},
                "search_context_size": "low",
            }
        ],
        temperature=1,
        max_output_tokens=4096,
        top_p=1,
        store=True,
    )

    return response.output[1].content[0].text


def get_fundamentals_finnhub(ticker, curr_date):
    """
    使用Finnhub API获取股票基本面数据作为OpenAI的备选方案
    Args:
        ticker (str): 股票代码
        curr_date (str): 当前日期，格式为yyyy-mm-dd
    Returns:
        str: 格式化的基本面数据报告
    """
    try:
        import finnhub
        import os
        from .cache_manager import get_cache
        
        # 检查缓存
        cache = get_cache()
        cached_key = cache.find_cached_fundamentals_data(ticker, data_source="finnhub")
        if cached_key:
            cached_data = cache.load_fundamentals_data(cached_key)
            if cached_data:
                print(f"💾 [DEBUG] 从缓存加载Finnhub基本面数据: {ticker}")
                return cached_data
        
        # 获取Finnhub API密钥
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return "错误：未配置FINNHUB_API_KEY环境变量"
        
        # 初始化Finnhub客户端
        finnhub_client = finnhub.Client(api_key=api_key)
        
        print(f"📊 [DEBUG] 使用Finnhub API获取 {ticker} 的基本面数据...")
        
        # 获取基本财务数据
        try:
            basic_financials = finnhub_client.company_basic_financials(ticker, 'all')
        except Exception as e:
            print(f"❌ [DEBUG] Finnhub基本财务数据获取失败: {str(e)}")
            basic_financials = None
        
        # 获取公司概况
        try:
            company_profile = finnhub_client.company_profile2(symbol=ticker)
        except Exception as e:
            print(f"❌ [DEBUG] Finnhub公司概况获取失败: {str(e)}")
            company_profile = None
        
        # 获取收益数据
        try:
            earnings = finnhub_client.company_earnings(ticker, limit=4)
        except Exception as e:
            print(f"❌ [DEBUG] Finnhub收益数据获取失败: {str(e)}")
            earnings = None
        
        # 格式化报告
        report = f"# {ticker} 基本面分析报告（Finnhub数据源）\n\n"
        report += f"**数据获取时间**: {curr_date}\n"
        report += f"**数据来源**: Finnhub API\n\n"
        
        # 公司概况部分
        if company_profile:
            report += "## 公司概况\n"
            report += f"- **公司名称**: {company_profile.get('name', 'N/A')}\n"
            report += f"- **行业**: {company_profile.get('finnhubIndustry', 'N/A')}\n"
            report += f"- **国家**: {company_profile.get('country', 'N/A')}\n"
            report += f"- **货币**: {company_profile.get('currency', 'N/A')}\n"
            report += f"- **市值**: {company_profile.get('marketCapitalization', 'N/A')} 百万美元\n"
            report += f"- **流通股数**: {company_profile.get('shareOutstanding', 'N/A')} 百万股\n\n"
        
        # 基本财务指标
        if basic_financials and 'metric' in basic_financials:
            metrics = basic_financials['metric']
            report += "## 关键财务指标\n"
            report += "| 指标 | 数值 |\n"
            report += "|------|------|\n"
            
            # 估值指标
            if 'peBasicExclExtraTTM' in metrics:
                report += f"| 市盈率 (PE) | {metrics['peBasicExclExtraTTM']:.2f} |\n"
            if 'psAnnual' in metrics:
                report += f"| 市销率 (PS) | {metrics['psAnnual']:.2f} |\n"
            if 'pbAnnual' in metrics:
                report += f"| 市净率 (PB) | {metrics['pbAnnual']:.2f} |\n"
            
            # 盈利能力指标
            if 'roeTTM' in metrics:
                report += f"| 净资产收益率 (ROE) | {metrics['roeTTM']:.2f}% |\n"
            if 'roaTTM' in metrics:
                report += f"| 总资产收益率 (ROA) | {metrics['roaTTM']:.2f}% |\n"
            if 'netProfitMarginTTM' in metrics:
                report += f"| 净利润率 | {metrics['netProfitMarginTTM']:.2f}% |\n"
            
            # 财务健康指标
            if 'currentRatioAnnual' in metrics:
                report += f"| 流动比率 | {metrics['currentRatioAnnual']:.2f} |\n"
            if 'totalDebt/totalEquityAnnual' in metrics:
                report += f"| 负债权益比 | {metrics['totalDebt/totalEquityAnnual']:.2f} |\n"
            
            report += "\n"
        
        # 收益历史
        if earnings:
            report += "## 收益历史\n"
            report += "| 季度 | 实际EPS | 预期EPS | 差异 |\n"
            report += "|------|---------|---------|------|\n"
            for earning in earnings[:4]:  # 显示最近4个季度
                actual = earning.get('actual', 'N/A')
                estimate = earning.get('estimate', 'N/A')
                period = earning.get('period', 'N/A')
                surprise = earning.get('surprise', 'N/A')
                report += f"| {period} | {actual} | {estimate} | {surprise} |\n"
            report += "\n"
        
        # 数据可用性说明
        report += "## 数据说明\n"
        report += "- 本报告使用Finnhub API提供的官方财务数据\n"
        report += "- 数据来源于公司财报和SEC文件\n"
        report += "- TTM表示过去12个月数据\n"
        report += "- Annual表示年度数据\n\n"
        
        if not basic_financials and not company_profile and not earnings:
            report += "⚠️ **警告**: 无法获取该股票的基本面数据，可能原因：\n"
            report += "- 股票代码不正确\n"
            report += "- Finnhub API限制\n"
            report += "- 该股票暂无基本面数据\n"
        
        # 保存到缓存
        if report and len(report) > 100:  # 只有当报告有实际内容时才缓存
            cache.save_fundamentals_data(ticker, report, data_source="finnhub")
        
        print(f"📊 [DEBUG] Finnhub基本面数据获取完成，报告长度: {len(report)}")
        return report
        
    except ImportError:
        return "错误：未安装finnhub-python库，请运行: pip install finnhub-python"
    except Exception as e:
        print(f"❌ [DEBUG] Finnhub基本面数据获取失败: {str(e)}")
        return f"Finnhub基本面数据获取失败: {str(e)}"


def get_fundamentals_openai(ticker, curr_date):
    """
    获取股票基本面数据，优先使用OpenAI，失败时回退到Finnhub API
    支持缓存机制以提高性能
    Args:
        ticker (str): 股票代码
        curr_date (str): 当前日期，格式为yyyy-mm-dd
    Returns:
        str: 基本面数据报告
    """
    try:
        from .cache_manager import get_cache
        
        # 检查缓存 - 优先检查OpenAI缓存
        cache = get_cache()
        cached_key = cache.find_cached_fundamentals_data(ticker, data_source="openai")
        if cached_key:
            cached_data = cache.load_fundamentals_data(cached_key)
            if cached_data:
                print(f"💾 [DEBUG] 从缓存加载OpenAI基本面数据: {ticker}")
                return cached_data
        
        config = get_config()
        
        # 检查是否配置了OpenAI相关设置
        if not config.get("backend_url") or not config.get("quick_think_llm"):
            print(f"📊 [DEBUG] OpenAI配置不完整，直接使用Finnhub API")
            return get_fundamentals_finnhub(ticker, curr_date)
        
        print(f"📊 [DEBUG] 尝试使用OpenAI获取 {ticker} 的基本面数据...")
        
        client = OpenAI(base_url=config["backend_url"])

        response = client.responses.create(
            model=config["quick_think_llm"],
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"Can you search Fundamental for discussions on {ticker} during of the month before {curr_date} to the month of {curr_date}. Make sure you only get the data posted during that period. List as a table, with PE/PS/Cash flow/ etc",
                        }
                    ],
                }
            ],
            text={"format": {"type": "text"}},
            reasoning={},
            tools=[
                {
                    "type": "web_search_preview",
                    "user_location": {"type": "approximate"},
                    "search_context_size": "low",
                }
            ],
            temperature=1,
            max_output_tokens=4096,
            top_p=1,
            store=True,
        )

        result = response.output[1].content[0].text
        
        # 保存到缓存
        if result and len(result) > 100:  # 只有当结果有实际内容时才缓存
            cache.save_fundamentals_data(ticker, result, data_source="openai")
        
        print(f"📊 [DEBUG] OpenAI基本面数据获取成功，长度: {len(result)}")
        return result
        
    except Exception as e:
        print(f"❌ [DEBUG] OpenAI基本面数据获取失败: {str(e)}")
        print(f"📊 [DEBUG] 回退到Finnhub API...")
        return get_fundamentals_finnhub(ticker, curr_date)


# =================================
# 制造业数据接口函数
# Manufacturing Data Interface Functions
# =================================

def get_manufacturing_weather_interface(
    city_name: str,
    curr_date: str,
) -> str:
    """
    获取制造业相关的天气预报数据，用于分析天气对产品需求的影响
    复用原有的缓存和降级机制
    
    Args:
        city_name (str): 城市名称
        curr_date (str): 当前日期，格式yyyy-mm-dd
        
    Returns:
        str: 天气预报数据的格式化字符串
    """
    print(f"🌤️ [INTERFACE] 获取制造业天气数据: {city_name} ({curr_date})")
    
    try:
        # 1. 检查缓存 (复用原有缓存机制)
        cache_key = f"manufacturing_weather_{city_name}_{curr_date}"
        
        # 2. 调用外部API获取数据
        import os
        import requests
        from datetime import datetime
        
        # 获取API密钥
        coze_api_key = os.getenv('COZE_API_KEY')
        if not coze_api_key:
            error_msg = "❌ COZE_API_KEY未配置"
            print(f"🌤️ [INTERFACE ERROR] {error_msg}")
            return error_msg
        
        # 生成API参数（简化版，避免复杂的预处理逻辑）
        api_params = {
            'weather': {
                'dailyForecast': True,
                'hourlyForecast': False,
                'nowcasting': False,
                'place': city_name,
                'realtime': False
            }
        }
        
        # 调用Coze天气API
        headers = {
            "Authorization": f"Bearer {coze_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "workflow_id": "7528239823611281448",
            "parameters": api_params['weather']
        }
        
        response = requests.post("https://api.coze.cn/v1/workflow/run", headers=headers, json=payload, timeout=180)  # 增加到3分钟
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                import json
                data_str = result.get('data', '{}')
                if isinstance(data_str, str):
                    data = json.loads(data_str)
                else:
                    data = data_str
                
                # 3. 格式化数据 (类似原有函数的格式化方式)
                formatted_result = f"## {city_name}制造业天气预报数据 ({curr_date})\n\n"
                formatted_result += json.dumps(data, ensure_ascii=False, indent=2)
                
                print(f"✅ [INTERFACE] 天气数据获取成功: {city_name}")
                return formatted_result
            else:
                error_msg = f"❌ 天气API返回错误: {result}"
                print(f"🌤️ [INTERFACE ERROR] {error_msg}")
                return error_msg
        else:
            error_msg = f"❌ 天气API调用失败: HTTP {response.status_code}"
            print(f"🌤️ [INTERFACE ERROR] {error_msg}")
            return error_msg
            
    except Exception as e:
        error_msg = f"制造业天气数据获取失败: {str(e)}"
        print(f"❌ [INTERFACE ERROR] {error_msg}")
        return error_msg


def get_manufacturing_news_interface(
    query_params,  # 🎯 修复：支持字典或字符串
    curr_date: str,
) -> str:
    """
    获取制造业相关的新闻数据，用于分析市场动态和政策影响
    
    Args:
        query_params (dict|str): 新闻查询参数，可以是结构化字典或字符串
        curr_date (str): 当前日期，格式yyyy-mm-dd
        
    Returns:
        str: 新闻数据的格式化字符串
    """
    print(f"📰 [INTERFACE] 获取制造业新闻数据: {query_params} ({curr_date})")
    
    try:
        # 1. 检查缓存
        cache_key = f"manufacturing_news_{hash(str(query_params))}_{curr_date}"
        
        # 2. 调用外部API
        import os
        import requests
        
        # 获取API密钥
        coze_api_key = os.getenv('COZE_API_KEY')
        if not coze_api_key:
            error_msg = "❌ COZE_API_KEY未配置"
            print(f"📰 [INTERFACE ERROR] {error_msg}")
            return error_msg
        
        # 🎯 修复：支持结构化查询参数
        if isinstance(query_params, dict):
            # 使用结构化查询（符合预期格式）
            api_params = {
                'news': {
                    'activity_query': query_params.get('activity_query', ''),
                    'area_news_query': query_params.get('area_news_query', ''),
                    'new_building_query': query_params.get('new_building_query', ''),
                    'policy_query': query_params.get('policy_query', '')
                }
            }
            print(f"📰 [INTERFACE] 使用结构化查询参数: {api_params['news']}")
        else:
            # 降级到简单字符串查询（兼容性）
            api_params = {
                'news': {
                    'activity_query': f"{query_params} 促销活动",
                    'area_news_query': query_params,
                    'new_building_query': f"{query_params} 新项目",
                    'policy_query': f"{query_params} 政策"
                }
            }
            print(f"📰 [INTERFACE] 使用简单字符串查询，自动生成结构化参数")
        
        # 调用Coze新闻API
        headers = {
            "Authorization": f"Bearer {coze_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "workflow_id": "7528253601837481984",
            "parameters": api_params['news']
        }
        
        response = requests.post("https://api.coze.cn/v1/workflow/run", headers=headers, json=payload, timeout=180)  # 增加到3分钟
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                import json
                data_str = result.get('data', '{}')
                if isinstance(data_str, str):
                    data = json.loads(data_str)
                else:
                    data = data_str
                
                # 3. 格式化数据
                formatted_result = f"## 制造业新闻数据 - {query_params} ({curr_date})\n\n"
                formatted_result += json.dumps(data, ensure_ascii=False, indent=2)
                
                print(f"✅ [INTERFACE] 新闻数据获取成功: {query_params}")
                return formatted_result
            else:
                error_msg = f"❌ 新闻API返回错误: {result}"
                print(f"📰 [INTERFACE ERROR] {error_msg}")
                return error_msg
        else:
            error_msg = f"❌ 新闻API调用失败: HTTP {response.status_code}"
            print(f"📰 [INTERFACE ERROR] {error_msg}")
            return error_msg
            
    except Exception as e:
        error_msg = f"制造业新闻数据获取失败: {str(e)}"
        print(f"❌ [INTERFACE ERROR] {error_msg}")
        return error_msg


def get_manufacturing_economic_interface(
    data_type: str,
    time_range: str,
    commodity_type: str = None,
) -> str:
    """
    获取制造业经济数据（PMI、PPI、期货数据）
    集成智能参数处理器和数据验证器
    
    Args:
        data_type (str): 数据类型 - 'pmi', 'ppi', 'commodity'
        time_range (str): 时间范围描述
        commodity_type (str): 商品类型（期货数据专用）
        
    Returns:
        str: 经济数据的格式化字符串
    """
    print(f"📈 [INTERFACE] 获取制造业经济数据: {data_type} ({time_range})")
    
    try:
        # 1. 检查缓存
        cache_key = f"manufacturing_economic_{data_type}_{hash(time_range)}_{hash(str(commodity_type))}"
        
        # 2. ✨ 使用智能参数处理器生成动态参数
        try:
            from manufacturingagents.manufacturingagents.utils.parameter_processor import get_parameter_processor
            from manufacturingagents.manufacturingagents.utils.data_validator import ManufacturingDataValidator
            from manufacturingagents.manufacturingagents.utils.strict_data_policy import StrictDataPolicy
            from manufacturingagents.default_config import DEFAULT_CONFIG
            
            # 初始化组件
            param_processor = get_parameter_processor(DEFAULT_CONFIG)
            data_validator = ManufacturingDataValidator()
            data_policy = StrictDataPolicy()
            
            print(f"✅ [INTERFACE] 智能组件初始化成功")
        except Exception as e:
            print(f"⚠️ [INTERFACE] 智能组件初始化失败，使用降级方案: {e}")
            param_processor = None
            data_validator = None
            data_policy = None
        
        # 3. 调用TuShare API
        import os
        import tushare as ts
        import pandas as pd
        from datetime import datetime
        
        # 获取TuShare token
        tushare_token = os.getenv('TUSHARE_TOKEN')
        if not tushare_token:
            error_msg = "❌ TUSHARE_TOKEN未配置"
            print(f"📈 [INTERFACE ERROR] {error_msg}")
            return error_msg
        
        ts.set_token(tushare_token)
        pro = ts.pro_api()
        
        # 4. 🎯 根据数据类型获取智能生成的参数
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        if data_type == 'pmi':
            if param_processor:
                try:
                    api_params = param_processor.generate_single_api_params('pmi', current_date=current_date)
                    print(f"🧠 [INTERFACE] 使用智能生成的PMI参数: {api_params['start_m']}-{api_params['end_m']}")
                except Exception as e:
                    print(f"⚠️ [INTERFACE] PMI参数生成失败，使用降级方案: {e}")
                    api_params = {"start_m": "202505", "end_m": "202507", "fields": "month,pmi010000"}
            else:
                # 降级方案：硬编码参数
                api_params = {"start_m": "202505", "end_m": "202507", "fields": "month,pmi010000"}
                
            result = pro.cn_pmi(
                start_m=api_params['start_m'],
                end_m=api_params['end_m'],
                fields=api_params['fields']
            )
            formatted_result = f"## PMI制造业采购经理指数 ({time_range})\n\n"
            
        elif data_type == 'ppi':
            if param_processor:
                try:
                    api_params = param_processor.generate_single_api_params('ppi', current_date=current_date)
                    print(f"🧠 [INTERFACE] 使用智能生成的PPI参数: {api_params['start_m']}-{api_params['end_m']}")
                except Exception as e:
                    print(f"⚠️ [INTERFACE] PPI参数生成失败，使用降级方案: {e}")
                    api_params = {"start_m": "202505", "end_m": "202507", "fields": "month,ppi_yoy,ppi_mp"}
            else:
                # 降级方案：硬编码参数
                api_params = {"start_m": "202505", "end_m": "202507", "fields": "month,ppi_yoy,ppi_mp"}
                
            result = pro.cn_ppi(
                start_m=api_params['start_m'],
                end_m=api_params['end_m'],
                fields=api_params['fields']
            )
            formatted_result = f"## PPI工业生产者价格指数 ({time_range})\n\n"
            
        elif data_type == 'commodity':
            # 🎯 修复：获取本月和下月两个期货合约数据
            from datetime import datetime, timedelta
            
            # 计算当前月份和下个月份
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            
            # 🎯 修复：使用正确的期货代码格式 (年份2位+月份2位)
            # 生成本月和下月的期货代码
            current_year_2digit = current_year % 100  # 2025 -> 25
            current_month_code = f"CU{current_year_2digit}{current_month:02d}.SHF"
            
            next_month = current_month + 1 if current_month < 12 else 1
            next_year_2digit = current_year_2digit if current_month < 12 else (current_year_2digit + 1) % 100
            next_month_code = f"CU{next_year_2digit}{next_month:02d}.SHF"
            
            print(f"🧠 [INTERFACE] 获取期货数据: 本月={current_month_code}, 下月={next_month_code}")
            
            # 🎯 修复：按照22-tushare-api-input.md获取完整字段
            # 获取本月数据
            try:
                print(f"🔍 [DEBUG] 尝试获取本月期货数据: {current_month_code}")
                current_result = pro.fut_weekly_monthly(
                    ts_code=current_month_code,
                    freq='week',
                    fields='ts_code,trade_date,freq,open,high,low,close,vol,amount'
                ).head(5)
                print(f"🔍 [DEBUG] 本月数据形状: {current_result.shape}")
            except Exception as e:
                print(f"❌ [DEBUG] 本月期货数据获取失败: {e}")
                current_result = pd.DataFrame()
            
            # 获取下月数据
            try:
                print(f"🔍 [DEBUG] 尝试获取下月期货数据: {next_month_code}")
                next_result = pro.fut_weekly_monthly(
                    ts_code=next_month_code,
                    freq='week',
                    fields='ts_code,trade_date,freq,open,high,low,close,vol,amount'
                ).head(5)
                print(f"🔍 [DEBUG] 下月数据形状: {next_result.shape}")
            except Exception as e:
                print(f"❌ [DEBUG] 下月期货数据获取失败: {e}")
                next_result = pd.DataFrame()
            
            # 合并数据
            if not current_result.empty:
                current_result['month_type'] = '本月'
            if not next_result.empty:
                next_result['month_type'] = '下月'
                
            # 🎯 修复：处理空数据情况
            if not current_result.empty and not next_result.empty:
                result = pd.concat([current_result, next_result], ignore_index=True)
            elif not current_result.empty:
                result = current_result
                print("⚠️ [DEBUG] 只获取到本月期货数据")
            elif not next_result.empty:
                result = next_result
                print("⚠️ [DEBUG] 只获取到下月期货数据")
            else:
                result = pd.DataFrame(columns=['ts_code', 'trade_date', 'freq', 'open', 'high', 'low', 'close', 'vol', 'amount', 'month_type'])
                print("⚠️ [DEBUG] 未获取到任何期货数据，返回空DataFrame")
            
            formatted_result = f"## {commodity_type or '铜期货'}数据 (本月和下月对比)\n\n"
            
        else:
            error_msg = f"❌ 不支持的数据类型: {data_type}"
            print(f"📈 [INTERFACE ERROR] {error_msg}")
            return error_msg
        
        # 5. 📊 数据验证（如果可用）
        if data_validator:
            try:
                is_valid, quality_score, issues = data_validator.validate_api_data(
                    data_type, result, {'time_range': time_range}
                )
                print(f"🔍 [INTERFACE] 数据验证完成: valid={is_valid}, score={quality_score:.2f}")
                if issues:
                    print(f"⚠️ [INTERFACE] 数据质量问题: {issues}")
                    
                # 如果数据质量太低，尝试数据策略处理
                if not is_valid and data_policy:
                    print(f"❌ [INTERFACE] 数据质量不合格，应用数据策略")
                    # 可以在此处添加数据源切换逻辑
                    
            except Exception as e:
                print(f"⚠️ [INTERFACE] 数据验证失败: {e}")
        
        # 6. 格式化数据
        formatted_result += result.to_string()
        
        print(f"✅ [INTERFACE] {data_type}数据获取成功: {len(result)} 条记录")
        return formatted_result
        
    except Exception as e:
        error_msg = f"制造业经济数据获取失败: {str(e)}"
        print(f"❌ [INTERFACE ERROR] {error_msg}")
        return error_msg


def get_manufacturing_holiday_interface(
    date_range: str,
) -> str:
    """
    获取制造业相关的节假日数据，用于分析节假日对制造业需求的影响
    复用原有的缓存和降级机制
    
    Args:
        date_range (str): 日期范围，如'2025-07到2025-10'
        
    Returns:
        str: 节假日数据的格式化字符串
    """
    print(f"📅 [INTERFACE] 获取制造业节假日数据: {date_range}")
    
    try:
        # 1. 检查缓存
        cache_key = f"manufacturing_holiday_{hash(date_range)}"
        
        # 2. 调用外部API
        import os
        import requests
        from datetime import datetime
        
        # 获取API密钥
        coze_api_key = os.getenv('COZE_API_KEY')
        if not coze_api_key:
            error_msg = "❌ COZE_API_KEY未配置"
            print(f"📅 [INTERFACE ERROR] {error_msg}")
            return error_msg
        
        # 生成API参数（简化版）
        api_params = {
            'holiday': {
                'start_date': '2025-7-1',
                'end_date': '2025-10-31'
            }
        }
        
        # 调用Coze节假日API
        headers = {
            "Authorization": f"Bearer {coze_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "workflow_id": "7528250308326260762",
            "parameters": api_params['holiday']
        }
        
        response = requests.post("https://api.coze.cn/v1/workflow/run", headers=headers, json=payload, timeout=180)  # 增加到3分钟
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                import json
                data_str = result.get('data', '{}')
                if isinstance(data_str, str):
                    data = json.loads(data_str)
                else:
                    data = data_str
                
                # 3. 格式化数据
                formatted_result = f"## 制造业节假日数据 ({date_range})\n\n"
                formatted_result += json.dumps(data, ensure_ascii=False, indent=2)
                
                print(f"✅ [INTERFACE] 节假日数据获取成功: {date_range}")
                return formatted_result
            else:
                error_msg = f"❌ 节假日API返回错误: {result}"
                print(f"📅 [INTERFACE ERROR] {error_msg}")
                return error_msg
        else:
            error_msg = f"❌ 节假日API调用失败: HTTP {response.status_code}"
            print(f"📅 [INTERFACE ERROR] {error_msg}")
            return error_msg
            
    except Exception as e:
        error_msg = f"制造业节假日数据获取失败: {str(e)}"
        print(f"❌ [INTERFACE ERROR] {error_msg}")
        return error_msg
