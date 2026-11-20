"""Smart analysis: summary statistics, outliers, correlations."""
import pandas as pd


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all").T


def detect_outliers(df: pd.DataFrame) -> dict:
    """Detect outliers per numeric column using the IQR rule."""
    outliers = {}
    for col in df.select_dtypes(include="number").columns:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (df[col] < low) | (df[col] > high)
        if mask.any():
            outliers[col] = {
                "count": int(mask.sum()),
                "lower_bound": float(low),
                "upper_bound": float(high),
                "row_indexes": df.index[mask].tolist(),
            }
    return outliers


def correlations(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include="number")
    return numeric.corr().round(3) if numeric.shape[1] > 1 else pd.DataFrame()


def generate_insights(df: pd.DataFrame, outliers: dict, corr: pd.DataFrame) -> list:
    """Create human-readable insights."""
    insights = [f"Dataset has {len(df)} rows and {len(df.columns)} columns."]
    for col, info in outliers.items():
        insights.append(f"Column '{col}' has {info['count']} outlier(s).")
    if not corr.empty:
        for i, a in enumerate(corr.columns):
            for b in corr.columns[i + 1:]:
                if abs(corr.loc[a, b]) >= 0.7:
                    kind = "positive" if corr.loc[a, b] > 0 else "negative"
                    insights.append(
                        f"Strong {kind} correlation between '{a}' and '{b}' ({corr.loc[a, b]})."
                    )
    return insights
