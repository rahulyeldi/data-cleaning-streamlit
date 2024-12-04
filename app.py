import streamlit as st
import pandas as pd
from data_cleaning import (
    handle_missing_values, remove_duplicates, correct_data_types,
    standardize_data, encode_categorical_variables
)

st.title("Automated Data Cleaning Tool")

# File uploader to load CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("### Original Data", df)

    # Feature selection for cleaning
    feature = st.selectbox("Select a cleaning feature", [
        "Handle Missing Values",
        "Remove Duplicates",
        "Correct Data Types",
        "Standardize Data",
        "Label Encoding"
    ])

    if feature == "Handle Missing Values":
        method = st.radio("Filling Method", ["mean", "median", "mode"])
        drop = st.checkbox("Drop rows/columns with missing values")
        cleaned_df = handle_missing_values(df, method, drop)

    elif feature == "Remove Duplicates":
        # Add a dropdown to select columns to check for duplicates
        column_selection = st.multiselect("Select columns to check for duplicates", df.columns.tolist())
        cleaned_df = remove_duplicates(df, subset_columns=column_selection) if column_selection else remove_duplicates(df)
        
    elif feature == "Correct Data Types":
        cleaned_df = correct_data_types(df)

    elif feature == "Standardize Data":
        # Allow users to select columns to standardize
        column_selection = st.multiselect("Select Columns to Standardize", df.columns.tolist())
        if column_selection:
            cleaned_df = standardize_data(df, column_selection)
        else:
            st.warning("No columns selected for standardization.")
            cleaned_df = df

    elif feature == "Label Encoding":
        # Select columns for label encoding
        column_selection = st.multiselect("Select columns to encode", df.select_dtypes(include=['object']).columns)
        if column_selection:
            cleaned_df = encode_categorical_variables(df, method='label', columns=column_selection)
        else:
            st.warning("No columns selected for label encoding.")
            cleaned_df = df

    # Display the cleaned data
    st.write("### Cleaned Data", cleaned_df)

    # Add a download button for cleaned data
    st.download_button("Download Cleaned CSV", 
                       cleaned_df.to_csv(index=False).encode('utf-8'), 
                       "cleaned_data.csv", 
                       "text/csv")