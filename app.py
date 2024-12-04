import streamlit as st
import pandas as pd
from data_cleaning import (
    handle_missing_values, remove_duplicates, correct_data_types,
    standardize_dates, encode_categorical_variables
)

st.title("Automated Data Cleaning Tool")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Original Data", df)

    feature = st.selectbox("Select a cleaning feature", [
        "Handle Missing Values",
        "Remove Duplicates",
        "Correct Data Types",
        "Standardize Dates",
        "Label Encoding"
    ])

    if feature == "Handle Missing Values":
        method = st.radio("Filling Method", ["mean", "median", "mode"])
        drop = st.checkbox("Drop rows/columns with missing values")
        cleaned_df = handle_missing_values(df, method, drop)
        
    elif feature == "Remove Duplicates":
        # Add a dropdown to select columns to check for duplicates
        column_selection = st.multiselect("Select columns to check for duplicates", df.columns.tolist())

        if column_selection:
            # If columns are selected, use them for duplicate removal
            cleaned_df = remove_duplicates(df, subset_columns=column_selection)
        else:
            # If no columns are selected, use all columns for duplicate removal
            cleaned_df = remove_duplicates(df)  # Use all columns by default
        
    elif feature == "Correct Data Types":
        cleaned_df = correct_data_types(df)
        
    elif feature == "Standardize Dates":
        date_cols = st.multiselect("Select Date Columns", df.columns)
        if date_cols:
            cleaned_df = standardize_dates(df, date_cols)
        else:
            st.warning("No date columns selected.")
            cleaned_df = df
        
    elif feature == "Label Encoding":
        # Select columns for label encoding
        column_selection = st.multiselect("Select columns to encode", df.select_dtypes(include=['object']).columns)
        if column_selection:
            cleaned_df = encode_categorical_variables(df, method='label', columns=column_selection)
        else:
            st.warning("No columns selected for label encoding.")
            cleaned_df = df

    st.write("### Cleaned Data", cleaned_df)
    st.download_button("Download Cleaned CSV", 
                       cleaned_df.to_csv(index=False).encode('utf-8'), 
                       "cleaned_data.csv", 
                       "text/csv")