import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.cleaner import clean_data
from src.analyzer import detect_outliers


def test_duplicates_removed():
    df = pd.DataFrame({"A": [1, 1, 2], "B": ["x", "x", "y"]})
    assert len(clean_data(df)) == 2


def test_missing_filled():
    df = pd.DataFrame({"Num": [1, None, 3], "Cat": ["a", "a", None]})
    assert clean_data(df).isna().sum().sum() == 0


def test_column_names_standardized():
    df = pd.DataFrame({"Employee ID": [1]})
    assert "employee_id" in clean_data(df).columns


def test_outlier_detection():
    df = pd.DataFrame({"v": [10, 11, 12, 10, 11, 500]})
    assert detect_outliers(df)["v"]["count"] == 1
