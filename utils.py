# utils.py
import pandas as pd
import re
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

def read_excel(uploaded_file):
    """
    Reads an Excel file and automatically detects the header row.
    Cleans empty rows/columns and normalizes column names.
    """
    raw_df = pd.read_excel(uploaded_file, sheet_name=0, header=None)

    # Detect the header row by looking for a row with mostly strings
    header_row = None
    for i, row in raw_df.iterrows():
        # Count non-null values
        non_null_count = row.count()
        # Count string type cells in the row
        string_count = row.apply(lambda x: isinstance(x, str)).sum()
        # If at least 2 cells are strings and at least half the row is non-null, consider it header
        if string_count >= 2 and non_null_count >= len(row) / 2:
            header_row = i
            break

    if header_row is None:
        raise ValueError("Could not find a valid header row in the Excel file.")

    # Read again using detected header row
    df = pd.read_excel(uploaded_file, sheet_name=0, header=header_row)

    # Drop fully empty rows and columns
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    # Normalize column names:
    # strip whitespace, lowercase, replace spaces with underscore, remove special characters
    def normalize_col(col):
        col = str(col).strip().lower()
        col = re.sub(r"\s+", "_", col)
        col = re.sub(r"[^\w]", "", col)
        return col

    df.columns = [normalize_col(col) for col in df.columns]

    return df


def run_pandasai(df, question, openai_api_key=None):
    """
    Runs PandasAI to answer the question on the dataframe.
    Returns (text_response, plotly_figure_or_None).
    """
    # Initialize OpenAI LLM for PandasAI
    llm = OpenAI(api_token=openai_api_key)
    pandas_ai = PandasAI(llm, conversational=False)

    # Run the question on the dataframe
    result = pandas_ai.run(df, prompt=question)

    # PandasAI may return text or figures, handle both
    # For simplicity, here we only return the result text and None for chart
    # (You can extend this to detect and return plotly charts if available)
    return str(result), None
