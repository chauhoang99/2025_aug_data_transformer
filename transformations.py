# Here we can add as many transformation functions as we want

import pandas as pd
from registry import registry


def validate_column(df: pd.DataFrame, column: str):
    if column not in df.columns:
        raise ValueError("column is not in data")


@registry.register("filter_rows")
def filter_rows(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    validate_column(df, column)
    return df[df[column] == value]


@registry.register("rename_column")
def rename_column(df: pd.DataFrame, column: str, new_name: str) -> pd.DataFrame:
    validate_column(df, column)
    return df.rename(columns={column: new_name})


@registry.register("uppercase_column")
def uppercase_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validate_column(df, column)
    df[column] = df[column].astype(str).str.upper()
    return df


@registry.register("titlecase_column")
def titlecase_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validate_column(df, column)
    df[column] = df[column].astype(str).str.title()
    return df


@registry.register("trim_whitespace")
def trim_whitespace(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validate_column(df, column)
    df[column] = df[column].astype(str).str.strip()
    return df
