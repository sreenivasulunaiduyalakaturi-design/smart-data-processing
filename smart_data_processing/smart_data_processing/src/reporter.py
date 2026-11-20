"""Save cleaned data and a text report to the output folder."""
import os
from datetime import datetime


def save_outputs(df, stats, outliers, corr, insights, out_dir="output"):
    os.makedirs(out_dir, exist_ok=True)

    cleaned_path = os.path.join(out_dir, "cleaned_data.csv")
    df.to_csv(cleaned_path, index=False)

    report_path = os.path.join(out_dir, "report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("SMART DATA PROCESSING REPORT\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write("=" * 60 + "\n\n")
        f.write("KEY INSIGHTS\n" + "-" * 60 + "\n")
        for line in insights:
            f.write(f"* {line}\n")
        f.write("\nSUMMARY STATISTICS\n" + "-" * 60 + "\n")
        f.write(stats.to_string() + "\n")
        f.write("\nOUTLIERS (IQR method)\n" + "-" * 60 + "\n")
        if outliers:
            for col, info in outliers.items():
                f.write(f"{col}: {info['count']} outlier(s), "
                        f"valid range [{info['lower_bound']:.2f}, {info['upper_bound']:.2f}], "
                        f"rows {info['row_indexes']}\n")
        else:
            f.write("None detected\n")
        f.write("\nCORRELATION MATRIX\n" + "-" * 60 + "\n")
        f.write(corr.to_string() if not corr.empty else "Not enough numeric columns")
        f.write("\n")

    print(f"[Reporter] Saved {cleaned_path}")
    print(f"[Reporter] Saved {report_path}")
    return cleaned_path, report_path
