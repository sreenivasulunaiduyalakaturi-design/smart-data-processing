"""Load data from CSV / Excel / JSON files into a pandas DataFrame."""
import os
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Load a dataset based on its file extension."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    elif ext == ".json":
        df = pd.read_json(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    print(f"[Loader] Loaded {len(df)} rows and {len(df.columns)} columns from '{path}'")
    return df
