import pandas as pd
from sklearn.preprocessing import LabelEncoder

def handle_missing_values(df, method="mode", drop=False):
    if method == "mode":
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = df[col].fillna(df[col].mode()[0])
    
    elif method == "mean":
        df = df.fillna(df.select_dtypes(include=['number']).mean())
    
    elif method == "median":
        df = df.fillna(df.select_dtypes(include=['number']).median())
    
    if drop:
        df = df.dropna(axis=0, how='any')
    
    df = df.drop_duplicates()
    
    return df

def remove_duplicates(df, subset_columns=None, fuzzy_threshold=90):
    if subset_columns is None:
        subset_columns = df.columns

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

def standardize_data(df, columns):
    for col in columns:
        if col in df.columns:
            # Check if the column is of type string (for Name, Gender, or other string columns)
            if df[col].dtype == 'object':  # Check if column is a string
                # Standardize Name and Gender columns by capitalizing the first letter
                df[col] = df[col].apply(lambda x: x.title() if isinstance(x, str) else x)
            
            # If the column is a string type and appears to be a date (either 'YYYY/MM/DD' or 'YYYY-MM-DD')
            if df[col].dtype == 'object':  # String type column
                for i, value in df[col].items():
                    if isinstance(value, str):
                        # Check if the string is in 'YYYY/MM/DD' format and needs conversion
                        if '/' in value:
                            try:
                                # Attempt conversion from 'YYYY/MM/DD' to 'YYYY-MM-DD'
                                df.at[i, col] = pd.to_datetime(value, format='%Y/%m/%d').strftime('%Y-%m-%d')
                            except Exception:
                                pass  # Ignore if conversion fails
                        # Check if the string is in 'YYYY-MM-DD' format
                        elif '-' in value:
                            try:
                                # Check if it's a valid 'YYYY-MM-DD' format date
                                pd.to_datetime(value, format='%Y-%m-%d')
                            except Exception:
                                df.at[i, col] = None  # Set invalid dates to None

    return df
def encode_categorical_variables(df, method='label', columns=None):
    if method == 'label' and columns:
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col])
    return df