"""
Main entry point for the FinSight application.
"""

print("Starting FinSight...")

from src.pipeline.runner import run_pipeline


def main():
    print("Inside main()")
    run_pipeline()


if __name__ == "__main__":
    print("__name__ block executed")
    main()