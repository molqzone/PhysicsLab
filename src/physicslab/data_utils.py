# src/physicslab/data_utils.py

import pandas as pd
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]


def load_transposed_csv(filepath: PathLike) -> pd.DataFrame:
    """
    Loads and processes a CSV file where parameters are stored in rows.

    This function performs the following steps:
    1. Reads the CSV using the first column as the index.
    2. Transposes the DataFrame to have parameters as columns.
    3. Converts all data to numeric types, coercing errors into NaN (Not a Number).

    Args:
        filepath (PathLike): The path to the input CSV file.

    Returns:
        pd.DataFrame: A cleaned, transposed DataFrame ready for analysis.
                      Returns an empty DataFrame if the file is not found.
    """
    filepath = Path(filepath)

    try:
        df = pd.read_csv(filepath, index_col=0)
        df_transposed = df.T
        print(f"✅ Successfully loaded and transposed data from: {filepath.name}")
        return df_transposed
    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred while loading {filepath}: {e}")
        return pd.DataFrame()


def check_missing_data(df: pd.DataFrame, df_name: str = "DataFrame") -> None:
    """
    Checks for missing data in the DataFrame and prints a summary.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        df_name (str): The name of the DataFrame (for reporting purposes).
    """
    print(f"\n--- 🔬 Data Quality Report for: {df_name} ---")

    if not isinstance(df, pd.DataFrame) or df.empty:
        print("Provided object is not a valid or non-empty DataFrame.")
        print("-" * (35 + len(df_name)))
        return

    missing_summary = df.isnull().sum()
    reportable_missing = missing_summary[missing_summary > 0]

    if reportable_missing.empty:
        print("✅ Excellent! No missing values found in any column.")
    else:
        print("⚠️ Warning! Missing values detected in the following columns:")
        # Sort to show columns with the most missing values first
        print(reportable_missing.sort_values(ascending=False))

    print("-" * (35 + len(df_name)))


def save_processed_data(df: pd.DataFrame, filepath: PathLike) -> None:
    """
    Saves the processed DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        filepath (PathLike): The path to the output CSV file.
    """
    filepath = Path(filepath)
    try:
        output_dir = filepath.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        df.to_csv(filepath, index=True)
        print(f"Processed data saved to: {filepath}")
    except Exception as e:
        print(f"Error saving file {filepath}: {e}")
