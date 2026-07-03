"""Centralized configuration for FinSight."""

from pathlib import Path
from datetime import date, timedelta

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Stock tickers to track
TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

# Data paths
RAW_DATA_PATH = BASE_DIR / "data" / "raw"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed"

# Database
DB_PATH = BASE_DIR / "data" / "db" / "finsight.db"

# Logging
LOG_PATH = BASE_DIR / "logs" / "finsight.log"
LOG_LEVEL = "INFO"

# Date range for data extraction
END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=365)

# Ensure required directories exist
for directory in (RAW_DATA_PATH, PROCESSED_DATA_PATH, DB_PATH.parent, LOG_PATH.parent):
    directory.mkdir(parents=True, exist_ok=True)