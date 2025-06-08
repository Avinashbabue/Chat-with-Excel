import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

def find_header_row(sheet, min_cols=2):
    """
    Automatically find the header row of the table in an Excel sheet.
    Returns the index of the detected header row.
    """
    for idx, row in enumerate(sheet.values):
        valid_cells = [cell for cell in row if pd.notnull(cell)]
        # Heuristic: Look for a row with mostly strings and enough columns
        if len(valid_cells) >= min_cols and all(isinstance(cell, str) for cell in valid_cells):
            return idx
    return 0  # fallback

def read_excel(uploaded_file):
    """
    Reads Excel data, skipping headings and blank rows/columns before the main table.
    Returns a cleaned DataFrame with standardized column names.
    """
    # Read without header to detect actual header row
    raw = pd.read_excel(uploaded_file, header=None)
    header_row = find_header_row(raw)
    # Now load with detected header
    df = pd.read_excel(uploaded_file, header=header_row)
    # Drop all-NaN columns and rows
    df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
    df.columns = [str(col).strip() for col in df.columns]
    return df

def summarize_dataframe(df):
    """
    Generates a schema summary for the LLM prompt.
    """
    summary = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        unique = df[col].nunique(dropna=True)
        col_summary = f"- {col} (type: {dtype}, unique: {unique}, nulls: {nulls})"
        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe()
            col_summary += f", min: {desc['min']:.2f}, max: {desc['max']:.2f}, mean: {desc['mean']:.2f}"
        elif unique <= 10:
            vc = df[col].value_counts(dropna=False).to_dict()
            col_summary += f", values: {vc}"
        summary.append(col_summary)
    return "\n".join(summary)

def ask_gemini(df, question):
    """
    Asks Gemini about the DataFrame using a well-structured prompt.
    """
    schema_info = summarize_dataframe(df)
    # Show both head and random sample for diversity
    sample_rows = pd.concat([df.head(5), df.sample(min(len(df), 5), random_state=42)]).drop_duplicates().to_markdown(index=False)
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
