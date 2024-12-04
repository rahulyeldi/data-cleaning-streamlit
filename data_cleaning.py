import pandas as pd
from sklearn.preprocessing import LabelEncoder

def handle_missing_values(df, method="mode", drop=False):
    # Apply the mode, mean, or median filling only for numerical columns (int, float)
    if method == "mode":
        for col in df.select_dtypes(include=['number']).columns:
            # Fill missing values for numerical columns with the mode
            df[col] = df[col].fillna(df[col].mode()[0])  # Mode for numerical columns
    
    elif method == "mean":
        # Fill missing values in only numerical columns with mean
        df = df.fillna(df.select_dtypes(include=['number']).mean())
    
    elif method == "median":
        # Fill missing values in only numerical columns with median
        df = df.fillna(df.select_dtypes(include=['number']).median())
    
    # Drop rows with missing values (optional)
    if drop:
        df = df.dropna(axis=0, how='any')  # Drop rows with any missing values
    
    # Remove duplicate rows after filling missing values
    df = df.drop_duplicates()
    
    return df

def remove_duplicates(df, subset_columns=None, fuzzy_threshold=90):
    # If no specific columns are provided, use all columns
    if subset_columns is None:
        subset_columns = df.columns

    # Step 1: Remove exact duplicates first based on the selected subset of columns
    df_cleaned = df.drop_duplicates(subset=subset_columns)

    return df_cleaned

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

def standardize_dates(df, date_cols):
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def encode_categorical_variables(df, method='label', columns=None):
    if method == 'label' and columns:
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col])
    return df