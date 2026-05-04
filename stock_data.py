from plotly import data
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_stock_info(ticker: str) -> dict:
    """Fetch real-time stock information using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        data = {
            "name": info.get("longName", ticker),
            "ticker": ticker.upper(),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice", "N/A"),
            "previous_close": info.get("previousClose", "N/A"),
            "open": info.get("open", "N/A"),
            "day_high": info.get("dayHigh", "N/A"),
            "day_low": info.get("dayLow", "N/A"),
            "week_52_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "week_52_low": info.get("fiftyTwoWeekLow", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "volume": info.get("volume", "N/A"),
            "avg_volume": info.get("averageVolume", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A"),
            "website": info.get("website", "N/A"),
            "currency": info.get("currency", "USD"),
        }

        # Calculate price change
        if data["current_price"] != "N/A" and data["previous_close"] != "N/A":
            change = data["current_price"] - data["previous_close"]
            change_pct = (change / data["previous_close"]) * 100
            data["price_change"] = round(float(change), 2)
            data["price_change_pct"] = round(float(change_pct), 2)
        else:
            data["price_change"] = "N/A"
            data["price_change_pct"] = "N/A"

        return data

    except Exception as e:
        return {"error": str(e)}


def get_stock_history(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """Fetch historical stock price data."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        return pd.DataFrame()


def format_market_cap(value) -> str:
    """Format market cap into readable format."""
    if value == "N/A" or value is None:
        return "N/A"
    try:
        value = float(value)
        if value >= 1_000_000_000_000:
            return f"${value/1_000_000_000_000:.2f}T"
        elif value >= 1_000_000_000:
            return f"${value/1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
        else:
            return f"${value:,.0f}"
    except:
        return "N/A"


def format_volume(value) -> str:
    """Format volume into readable format."""
    if value == "N/A" or value is None:
        return "N/A"
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value/1_000:.2f}K"
        else:
            return f"{value:,.0f}"
    except:
        return "N/A"


def get_stock_context_for_llm(stock_data: dict) -> str:
    """Format stock data as context string for LLM."""
    if "error" in stock_data:
        return f"Error fetching stock data: {stock_data['error']}"

    context = f"""
REAL-TIME STOCK DATA (as of {datetime.now().strftime('%Y-%m-%d %H:%M')}):

Company: {stock_data.get('name', 'N/A')}
Ticker: {stock_data.get('ticker', 'N/A')}
Sector: {stock_data.get('sector', 'N/A')}
Industry: {stock_data.get('industry', 'N/A')}

PRICE INFORMATION:
- Current Price: {stock_data.get('currency', '$')} {stock_data.get('current_price', 'N/A')}
- Previous Close: {stock_data.get('previous_close', 'N/A')}
- Price Change: {stock_data.get('price_change', 'N/A')} ({stock_data.get('price_change_pct', 'N/A')}%)
- Day High: {stock_data.get('day_high', 'N/A')}
- Day Low: {stock_data.get('day_low', 'N/A')}
- 52-Week High: {stock_data.get('week_52_high', 'N/A')}
- 52-Week Low: {stock_data.get('week_52_low', 'N/A')}

FUNDAMENTALS:
- Market Cap: {format_market_cap(stock_data.get('market_cap'))}
- P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
- EPS: {stock_data.get('eps', 'N/A')}
- Dividend Yield: {stock_data.get('dividend_yield', 'N/A')}
- Volume: {format_volume(stock_data.get('volume'))}

COMPANY OVERVIEW:
{stock_data.get('summary', 'N/A')[:500]}...
"""
    return context