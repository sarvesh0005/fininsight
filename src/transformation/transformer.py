"""Data transformation module for FinSight: cleans and enriches raw stock data."""

from typing import Dict

import pandas as pd

from config.settings import TICKERS, RAW_DATA_PATH, PROCESSED_DATA_PATH
from config.logging_config import get_logger

logger = get_logger(__name__)

COLUMN_RENAME_MAP = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
    "Ticker": "ticker",
}

REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume", "ticker"]

ROLLING_WINDOW_SHORT = 7
ROLLING_WINDOW_LONG = 30
VOLATILITY_WINDOW = 30


def transform_ticker(ticker: str) -> pd.DataFrame:
    """Load, clean, and enrich raw data for a single ticker."""
    safe_ticker = ticker.replace(".", "_")
    raw_path = RAW_DATA_PATH / f"{safe_ticker}.csv"

    if not raw_path.exists():
        logger.warning(f"Raw file not found for ticker: {ticker}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(raw_path, header=0)

        if df.empty:
            logger.warning(f"Raw data is empty for ticker: {ticker}")
            return df

        # Drop any residual yfinance header rows (second header row artifact)
        df = df[df["Date"] != "Date"].reset_index(drop=True)

        # Remove duplicates and missing values
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        # Rename columns
        df.rename(columns=COLUMN_RENAME_MAP, inplace=True)

        # Guard: adj_close may be absent when auto_adjust=True was used historically
        if "adj_close" not in df.columns and "close" in df.columns:
            df["adj_close"] = df["close"]

        # Validate required columns present
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            logger.error(f"Missing columns for {ticker}: {missing}")
            return pd.DataFrame()

        # Convert types
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["date"], inplace=True)
        for col in ["open", "high", "low", "close", "adj_close", "volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df.dropna(inplace=True)

        # Ensure ticker column
        df["ticker"] = ticker

        # Sort chronologically
        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Feature engineering
        df["daily_return"] = df["close"].diff()
        df["daily_pct_return"] = df["close"].pct_change() * 100
        df["ma_7"] = df["close"].rolling(window=ROLLING_WINDOW_SHORT).mean()
        df["ma_30"] = df["close"].rolling(window=ROLLING_WINDOW_LONG).mean()
        df["volatility_30"] = df["daily_pct_return"].rolling(window=VOLATILITY_WINDOW).std()

        df.dropna(inplace=True)

        if df.empty:
            logger.warning(f"No rows remaining after feature engineering for {ticker}")
            return df

        output_path = PROCESSED_DATA_PATH / f"{safe_ticker}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Saved processed data for {ticker} to {output_path} ({len(df)} rows)")

        return df

    except Exception as e:
        logger.error(f"Failed to transform data for {ticker}: {e}")
        return pd.DataFrame()


def transform_all() -> Dict[str, pd.DataFrame]:
    """Transform raw data for all configured tickers."""
    results: Dict[str, pd.DataFrame] = {}

    for ticker in TICKERS:
        df = transform_ticker(ticker)
        results[ticker] = df

    logger.info(f"Transformation complete for {len(results)} tickers")
    return results


if __name__ == "__main__":
    transform_all()
