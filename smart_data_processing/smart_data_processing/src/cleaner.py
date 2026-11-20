"""Automatic data cleaning: column names, duplicates, types, missing values."""
import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names and replace spaces with underscores."""
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"[Cleaner] Removed {before - len(df)} duplicate rows")
    return df


def infer_types(df: pd.DataFrame) -> pd.DataFrame:
    """Try converting text columns to numbers or dates when most values fit."""
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        s = df[col].astype("object").map(lambda v: v.strip() if isinstance(v, str) else v)
        df[col] = s
        valid = s.notna().sum()
        if valid == 0:
            continue
        numeric = pd.to_numeric(s, errors="coerce")
        if numeric.notna().sum() >= 0.8 * valid:
            df[col] = numeric
            continue
        if "date" in col or "time" in col:
            dates = pd.to_datetime(s, errors="coerce")
            if dates.notna().sum() >= 0.8 * valid:
                df[col] = dates
    return df


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric -> median, categorical -> mode, datetime -> forward/back fill."""
    df = df.copy()
    total = int(df.isna().sum().sum())
    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].ffill().bfill()
        else:
            mode = df[col].mode()
            df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else "Unknown")
    print(f"[Cleaner] Filled {total} missing values")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the complete cleaning pipeline."""
    df = standardize_columns(df)
    df = remove_duplicates(df)
    df = infer_types(df)
    df = fill_missing(df)
    return df
