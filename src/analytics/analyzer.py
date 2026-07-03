"""Analytics module for FinSight: derives insights from stored stock data."""

import sqlite3
from typing import Any, Dict

import pandas as pd

from config.settings import DB_PATH
from config.logging_config import get_logger

logger = get_logger(__name__)


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection to the FinSight database."""
    return sqlite3.connect(DB_PATH)


def load_stock_data(ticker: str = None) -> pd.DataFrame:
    """Load stock price data from the database, optionally filtered by ticker."""
    conn = get_connection()
    try:
        query = "SELECT * FROM stock_prices"
        params = ()
        if ticker:
            query += " WHERE ticker = ?"
            params = (ticker,)
        df = pd.read_sql_query(query, conn, params=params)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        logger.error(f"Failed to load stock data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def analyze_ticker(ticker: str) -> Dict[str, Any]:
    """Compute key analytics metrics for a single ticker."""
    df = load_stock_data(ticker)

    if df.empty:
        logger.warning(f"No data available for ticker: {ticker}")
        return {}

    try:
        highest_close_row = df.loc[df["close"].idxmax()]
        lowest_close_row = df.loc[df["close"].idxmin()]
        highest_volume_row = df.loc[df["volume"].idxmax()]
        highest_volatility_row = df.loc[df["volatility_30"].idxmax()]

        metrics = {
            "ticker": ticker,
            "highest_closing_price": round(float(highest_close_row["close"]), 2),
            "highest_closing_date": highest_close_row["date"].strftime("%Y-%m-%d"),
            "lowest_closing_price": round(float(lowest_close_row["close"]), 2),
            "lowest_closing_date": lowest_close_row["date"].strftime("%Y-%m-%d"),
            "average_daily_return": round(float(df["daily_return"].mean()), 4),
            "highest_volume": int(highest_volume_row["volume"]),
            "highest_volume_date": highest_volume_row["date"].strftime("%Y-%m-%d"),
            "highest_volatility": round(float(highest_volatility_row["volatility_30"]), 4),
            "highest_volatility_date": highest_volatility_row["date"].strftime("%Y-%m-%d"),
        }

        logger.info(f"Computed analytics for {ticker}")
        return metrics

    except Exception as e:
        logger.error(f"Failed to compute analytics for {ticker}: {e}")
        return {}


def analyze_all() -> Dict[str, Dict[str, Any]]:
    """Compute analytics metrics for all tickers present in the database."""
    df = load_stock_data()

    if df.empty:
        logger.warning("No data available in database for analytics")
        return {}

    results: Dict[str, Dict[str, Any]] = {}
    tickers = df["ticker"].unique()

    for ticker in tickers:
        results[ticker] = analyze_ticker(ticker)

    logger.info(f"Analytics complete for {len(results)} tickers")
    return results


def print_report(metrics: Dict[str, Any]) -> None:
    """Print a formatted analytics report for a single ticker."""
    if not metrics:
        return

    print(f"\n{'=' * 50}")
    print(f"  Analytics Report: {metrics['ticker']}")
    print(f"{'=' * 50}")
    print(f"  Highest Closing Price : {metrics['highest_closing_price']} on {metrics['highest_closing_date']}")
    print(f"  Lowest Closing Price  : {metrics['lowest_closing_price']} on {metrics['lowest_closing_date']}")
    print(f"  Average Daily Return  : {metrics['average_daily_return']}")
    print(f"  Highest Volume        : {metrics['highest_volume']:,} on {metrics['highest_volume_date']}")
    print(f"  Highest Volatility    : {metrics['highest_volatility']} on {metrics['highest_volatility_date']}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    all_metrics = analyze_all()
    for ticker_metrics in all_metrics.values():
        print_report(ticker_metrics)
