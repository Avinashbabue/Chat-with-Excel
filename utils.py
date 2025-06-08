import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
import random

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

def find_header_row(sheet, min_cols=2):
    for idx, row in enumerate(sheet.values):
        valid_cells = [cell for cell in row if pd.notnull(cell)]
        if len(valid_cells) >= min_cols and all(isinstance(cell, str) for cell in valid_cells):
            return idx
    return 0

def read_excel(uploaded_file):
    # Read without header to detect actual header row
    raw = pd.read_excel(uploaded_file, header=None)
    header_row = find_header_row(raw)
    # Now load with detected header
    df = pd.read_excel(uploaded_file, header=header_row)
    # Drop all-NaN columns
    df = df.dropna(axis=1, how='all')
    # Remove trailing rows after the table (where all values become NaN)
    first_all_nan_row = df[df.isnull().all(axis=1)].index
    if len(first_all_nan_row) > 0:
        df = df.loc[:first_all_nan_row[0]-1]
    # Drop all-NaN rows
    df = df.dropna(axis=0, how='all')
    df.columns = [str(col).strip() for col in df.columns]
    return df

def detect_column_type(series):
    unique_vals = series.dropna().unique()
    if pd.api.types.is_numeric_dtype(series):
        if len(unique_vals) == 2:
            # Check for binary like 0/1 or True/False
            if set(map(str, unique_vals)).issubset({'0', '1', 'True', 'False'}):
                return 'binary'
        return 'numerical'
    else:
        if len(unique_vals) == 2:
            # Check for binary like Yes/No or Y/N
            lower_vals = set(map(lambda x: str(x).strip().lower(), unique_vals))
            if lower_vals in [{'yes','no'}, {'y','n'}, {'true','false'}, {'0','1'}]:
                return 'binary'
        if len(unique_vals) <= 10:
            return 'categorical'
        return 'categorical' if series.dtype == object else 'other'

def fill_missing_values(df):
    df_filled = df.copy()
    for col in df.columns:
        col_type = detect_column_type(df[col])
        if col_type == 'numerical':
            df_filled[col] = df[col].fillna(0)
        elif col_type == 'categorical':
            df_filled[col] = df[col].fillna('Not sure')
        elif col_type == 'binary':
            # Find possible binary values
            vals = df[col].dropna().unique()
            if len(vals) == 2:
                fill_val = random.choice(vals)
                df_filled[col] = df[col].apply(lambda x: fill_val if pd.isna(x) else x)
            else:
                df_filled[col] = df[col].fillna('Yes')  # fallback
        else:
            df_filled[col] = df[col].fillna('Not sure')
    return df_filled

def summarize_dataframe(df):
    summary = []
    for col in df.columns:
        col_type = detect_column_type(df[col])
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        unique = df[col].nunique(dropna=True)
        col_summary = f"- {col} (type: {dtype}, logical_type: {col_type}, unique: {unique}, nulls: {nulls})"
        if col_type == 'numerical':
            desc = df[col].describe()
            col_summary += f", min: {desc['min']:.2f}, max: {desc['max']:.2f}, mean: {desc['mean']:.2f}"
        elif col_type == 'binary' or (col_type == 'categorical' and unique <= 10):
            vc = df[col].value_counts(dropna=False).to_dict()
            col_summary += f", values: {vc}"
        summary.append(col_summary)
    return "\n".join(summary)

def ask_gemini(df, question):
    """
    Asks Gemini about the DataFrame using a well-structured prompt.
    """
    # Fill missing values according to type
    df_cleaned = fill_missing_values(df)
    schema_info = summarize_dataframe(df_cleaned)
    # Show both head and random sample for diversity
    sample_rows = pd.concat([df_cleaned.head(5), df_cleaned.sample(min(len(df_cleaned), 5), random_state=42)]).drop_duplicates().to_markdown(index=False)
    prompt = f"""
You are an expert data analyst.
Here is the data schema:
{schema_info}

Here are some data samples:
{sample_rows}

User's question: {question}

If the question requires a chart, suggest the most suitable chart type and the columns to use.
Return your answer in the following JSON format if a chart is needed:
{{
    "answer": "<textual answer>",
    "chart_type": "<bar|histogram|line|pie|scatter|...>",
    "x": "<column for x-axis>",
    "y": "<column for y-axis or null>"
}}
If no chart is needed, just answer as plain text.
Do not assume any specific column names. Always use the exact column names as shown.
    """
    response = model.generate_content(prompt)
    return response.text
