"""Smart Data Processing - main entry point.

Usage:
    python main.py                       # uses data/sample_data.csv
    python main.py path/to/your_file.csv # your own dataset
"""
import sys
from src.loader import load_data
from src.cleaner import clean_data
from src.analyzer import (summary_statistics, detect_outliers,
                          correlations, generate_insights)
from src.reporter import save_outputs


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_data.csv"

    df = load_data(path)
    df = clean_data(df)

    stats = summary_statistics(df)
    outliers = detect_outliers(df)
    corr = correlations(df)
    insights = generate_insights(df, outliers, corr)

    save_outputs(df, stats, outliers, corr, insights)

    print("\n--- Key Insights ---")
    for line in insights:
        print("*", line)


if __name__ == "__main__":
    main()
