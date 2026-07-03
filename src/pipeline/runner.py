"""Pipeline runner for FinSight: executes the full ETL and analytics workflow."""

import sys

from config.logging_config import get_logger
from src.extraction.extractor import extract_all
from src.transformation.transformer import transform_all
from src.database.db_manager import load_all
from src.analytics.analyzer import analyze_all, print_report

logger = get_logger(__name__)


def run_pipeline() -> None:
    """Execute the FinSight ETL pipeline: extract, transform, load, analyze."""
    try:
        logger.info("=== FinSight Pipeline Started ===")

        logger.info("Step 1/4: Extraction")
        extract_all()

        logger.info("Step 2/4: Transformation")
        transform_all()

        logger.info("Step 3/4: Load")
        load_all()

        logger.info("Step 4/4: Analytics")
        all_metrics = analyze_all()
        for ticker_metrics in all_metrics.values():
            print_report(ticker_metrics)

        logger.info("=== FinSight Pipeline Completed Successfully ===")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()