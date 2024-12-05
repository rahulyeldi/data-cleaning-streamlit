import streamlit as st
import pandas as pd
from data_cleaning import (
    handle_missing_values, remove_duplicates,
    standardize_data, encode_categorical_variables
)

st.title("Data Cleaning Tool")

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
        "Standardize Data",
        "Label Encoding"
    ])

    if feature == "Handle Missing Values":
        st.write("### Missing Data Handling")
        selected_columns = st.multiselect("Select numerical columns to handle missing data", df.select_dtypes(include=['number']).columns)
        method = st.radio("Choose filling method for numerical columns", ["mean", "median", "mode"], index=0)
        
        if st.button("Perform Missing Data Handling"):
            cleaned_df = handle_missing_values(df, columns=selected_columns, method=method)
            st.write("### Cleaned Data", cleaned_df)
            st.download_button(
                "Download Cleaned CSV",
                cleaned_df.to_csv(index=False).encode('utf-8'),
                "cleaned_data.csv",
                "text/csv",
                key="missing_values_download"
            )

    elif feature == "Remove Duplicates":
        st.write("### Duplicate Data Handling")
        selected_columns = st.multiselect("Select columns to check for duplicates (If no columns are selected then operation is performed to all columns)", df.columns)
    
        if selected_columns:
            cleaned_df = remove_duplicates(df, subset_columns=selected_columns)
        else:
            cleaned_df = remove_duplicates(df)  # Default to all columns if none selected
    
        st.write("### Cleaned Data", cleaned_df)
        st.download_button(
            "Download Cleaned CSV",
            cleaned_df.to_csv(index=False).encode('utf-8'),
            "cleaned_data.csv",
            "text/csv",
            key="remove_duplicates_download"
        )

    elif feature == "Standardize Data":
        st.write("### Data Standardization")
        selected_columns = st.multiselect("Select columns to standardize", df.columns)
        if selected_columns:
            cleaned_df = standardize_data(df, selected_columns)
            st.write("### Cleaned Data", cleaned_df)
            st.download_button(
                "Download Cleaned CSV",
                cleaned_df.to_csv(index=False).encode('utf-8'),
                "cleaned_data.csv",
                "text/csv",
                key="standardize_data_download"
            )
        else:
            st.warning("No columns selected for standardization.")
            cleaned_df = df

    elif feature == "Label Encoding":
        st.write("### Label Encoding")
        selected_columns = st.multiselect("Select columns to encode", df.select_dtypes(include=['object']).columns)
        if selected_columns:
            cleaned_df = encode_categorical_variables(df, method='label', columns=selected_columns)
            st.write("### Cleaned Data", cleaned_df)
            st.download_button(
                "Download Cleaned CSV",
                cleaned_df.to_csv(index=False).encode('utf-8'),
                "cleaned_data.csv",
                "text/csv",
                key="label_encoding_download"
            )
        else:
            st.warning("No columns selected for label encoding.")
            cleaned_df = df