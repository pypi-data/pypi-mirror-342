import pandas as pd
import os
from typing import Literal

def load_match_data(filepath: str) -> pd.DataFrame:

    """
    Loads match data from a CSV or Excel file into a DataFrame.

    Args:
        filepath (str): path to the CSV (.csv) or Excel (.xlsx, .xls) file

    Returns:
        pd.DataFrame: loaded match data

    Raises:
        ValueError: if file extension is unsupported or loading fails
    """
    try:
        _, ext = os.path.splitext(filepath.lower())

        if ext == ".csv":
            df = pd.read_csv(filepath)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        raise ValueError(f"Failed to load file '{filepath}': {e}")

    return df

def clean_data(df: pd.DataFrame, missing_strategy: Literal["fill", "drop", "none"] = "fill") -> pd.DataFrame:
    
    """
    Cleans match data: fixes dtypes, handles missing values.

    Args:
        df (pd.DataFrame): raw data to be cleaned
        missing_strategy (str): strategy for handling missing values:
            - "fill": fill missing numeric values with column mean
            - "drop": drop rows with missing value in at least one variable
            - "none": leave missing values untouched (default)

    Returns:
        pd.DataFrame: cleaned DataFrame

    Raises:
        ValueError: if an unknown missing_strategy is given
    """
    df = df.convert_dtypes()

    if missing_strategy == "fill":
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif missing_strategy == "drop":
        df = df.dropna()
    elif missing_strategy == "none":
        pass
    else:
        raise ValueError(f"Invalid missing_strategy: '{missing_strategy}'. Use 'fill', 'drop' or 'none'.")
    
    return df

def data_profiling(df: pd.DataFrame) -> None:

    """
    Prints basic information about the DataFrame: column names, types, number of rows, missing values and basic statistics.

    Args:
        df (pd.DataFrame): the DataFrame to analyze

    Returns:
        None: the function only prints information to the console
    """

    print("Basic information about the DataFrame:\n")

    # Column names and types
    print("Columns and their types:")
    print(df.dtypes)
    print("\n")

    # Number of rows
    print(f"Number of rows: {df.shape[0]}")
    
    # Number of columns
    print(f"Number of columns: {df.shape[1]}")
    print("\n")

    # Missing values
    missing_values = df.isnull().sum()
    print("Missing values (per column):")
    print(missing_values[missing_values > 0])
    print("\n")

    # Basic statistics for numeric columns
    print("Basic statistics for numeric columns:")
    print(df.describe())
    print("\n")

    # Basic statistics for categorical columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    if len(categorical_columns) > 0:
        print("Basic statistics for categorical columns:")
        for col in categorical_columns:
            print(f"\n{col}:")
            print(df[col].value_counts())
    print("\n")

if __name__ == "__main__":
    print("Data submodule of our pyTSPA toolbox")
    print("Does nothing when run, please import it in your code, for example: 'import pyTSPA.data'")