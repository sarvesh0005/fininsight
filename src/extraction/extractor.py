"""Data extraction module for FinSight: downloads stock data via yfinance."""

from typing import Dict

import pandas as pd
import yfinance as yf

from config.settings import TICKERS, RAW_DATA_PATH, START_DATE, END_DATE
from config.logging_config import get_logger

logger = get_logger(__name__)


def extract_ticker(ticker: str) -> pd.DataFrame:
    """Download historical data for a single ticker and save it to CSV."""
    try:
        logger.info(f"Downloading data for {ticker} ({START_DATE} to {END_DATE})")
        df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            progress=False,
            auto_adjust=False,
        )

        if df.empty:
            logger.warning(f"No data returned for ticker: {ticker}")
            return df

        # Flatten MultiIndex columns produced by recent yfinance versions
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.reset_index(inplace=True)
        df["Ticker"] = ticker

        safe_ticker = ticker.replace(".", "_")
        output_path = RAW_DATA_PATH / f"{safe_ticker}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Saved raw data for {ticker} to {output_path}")

        return df

    except Exception as e:
        logger.error(f"Failed to extract data for {ticker}: {e}")
        return pd.DataFrame()


def extract_all() -> Dict[str, pd.DataFrame]:
    """Download historical data for all configured tickers."""
    results: Dict[str, pd.DataFrame] = {}

    for ticker in TICKERS:
        df = extract_ticker(ticker)
        results[ticker] = df

    logger.info(f"Extraction complete for {len(results)} tickers")
    return results


if __name__ == "__main__":
    extract_all()
