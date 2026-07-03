"""Database loading module for FinSight: persists processed data into SQLite."""

import sqlite3
from typing import Dict

import pandas as pd

from config.settings import TICKERS, PROCESSED_DATA_PATH, DB_PATH
from config.logging_config import get_logger

logger = get_logger(__name__)

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS stock_prices (
    date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER,
    daily_return REAL,
    daily_pct_return REAL,
    ma_7 REAL,
    ma_30 REAL,
    volatility_30 REAL,
    PRIMARY KEY (date, ticker)
);
"""


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection, ensuring the table exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(CREATE_TABLE_QUERY)
    conn.commit()
    return conn


def load_ticker(ticker: str, conn: sqlite3.Connection) -> int:
    """Load processed CSV data for a single ticker into the database."""
    safe_ticker = ticker.replace(".", "_")
    processed_path = PROCESSED_DATA_PATH / f"{safe_ticker}.csv"

    if not processed_path.exists():
        logger.warning(f"Processed file not found for ticker: {ticker}")
        return 0

    try:
        df = pd.read_csv(processed_path)

        if df.empty:
            logger.warning(f"Processed data is empty for ticker: {ticker}")
            return 0

        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        records = df.to_dict(orient="records")

        insert_query = """
        INSERT OR IGNORE INTO stock_prices (
            date, ticker, open, high, low, close, adj_close, volume,
            daily_return, daily_pct_return, ma_7, ma_30, volatility_30
        ) VALUES (
            :date, :ticker, :open, :high, :low, :close, :adj_close, :volume,
            :daily_return, :daily_pct_return, :ma_7, :ma_30, :volatility_30
        );
        """

        cursor = conn.cursor()
        cursor.executemany(insert_query, records)
        conn.commit()

        inserted = cursor.rowcount if cursor.rowcount != -1 else len(records)
        logger.info(f"Loaded {len(records)} rows for {ticker} ({inserted} new)")

        return len(records)

    except Exception as e:
        logger.error(f"Failed to load data for {ticker}: {e}")
        conn.rollback()
        return 0


def load_all() -> Dict[str, int]:
    """Load processed data for all configured tickers into the database."""
    results: Dict[str, int] = {}
    conn = get_connection()

    try:
        for ticker in TICKERS:
            count = load_ticker(ticker, conn)
            results[ticker] = count
    finally:
        conn.close()

    logger.info(f"Database load complete for {len(results)} tickers")
    return results


if __name__ == "__main__":
    load_all()