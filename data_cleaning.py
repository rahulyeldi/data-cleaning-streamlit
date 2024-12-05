import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def handle_missing_values(df, columns=None, method="mean"):
    if not columns:
        return df  # No action if no columns selected

    for col in columns:
        if df[col].dtype in ['int64', 'float64']:
            if method == "mean":
                df[col].fillna(df[col].mean(), inplace=True)
            elif method == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif method == "mode":
                df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna("NaN", inplace=True)  # Fill non-numerical missing values with "NaN"

    return df

def remove_duplicates(df, subset_columns=None):
    """Removes duplicate rows in the dataset based on selected columns."""
    if subset_columns:  # Check if subset_columns is not empty
        return df.drop_duplicates(subset=subset_columns)
    else:
        return df.drop_duplicates()  # Drop duplicates across all columns if none selected

def correct_data_types(df):
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except ValueError:
                pass
        elif pd.api.types.is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except ValueError:
                pass
    return df

def standardize_data(df, columns):
    for col in columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: x.title() if isinstance(x, str) else x)

            if df[col].dtype == 'object':
                for i, value in df[col].items():
                    if isinstance(value, str):
                        if '/' in value:
                            try:
                                df.at[i, col] = pd.to_datetime(value, format='%Y/%m/%d').strftime('%Y-%m-%d')
                            except Exception:
                                pass
                        elif '-' in value:
                            try:
                                pd.to_datetime(value, format='%Y-%m-%d')
                            except Exception:
                                df.at[i, col] = None

    return df

def encode_categorical_variables(df, method='label', columns=None):
    if method == 'label' and columns:
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col])
    return df