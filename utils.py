import os
import re
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (TOGETHER_API_KEY)
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Specify Together's OpenAI-compatible endpoint, if needed (otherwise OpenAI default)
# For many OpenAI-compatible providers, you can override the API base URL like this:
# os.environ["OPENAI_API_BASE"] = "https://api.together.xyz/v1"

def read_excel(uploaded_file):
    """
    Reads an Excel file, auto-detects the header row,
    cleans empty rows/columns, and normalizes column names.
    """
    raw_df = pd.read_excel(uploaded_file, sheet_name=0, header=None)

    # Detect the header row by looking for a row with mostly strings
    header_row = None
    for i, row in raw_df.iterrows():
        non_null_count = row.count()
        string_count = row.apply(lambda x: isinstance(x, str)).sum()
        # At least 2 strings and half non-null values
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

    # Normalize column names: strip, lower, underscore, remove special chars
    def normalize_col(col):
        col = str(col).strip().lower()
        col = re.sub(r"\s+", "_", col)
        col = re.sub(r"[^\w]", "", col)
        return col

    df.columns = [normalize_col(col) for col in df.columns]
    return df

def run_pandasai(df, question, together_api_key=TOGETHER_API_KEY):
    """
    Run PandasAI using Together API's GPT-3.5-turbo model.
    Returns: (text_response, plotly_figure_or_None)
    """
    # If Together API is OpenAI-compatible, this works out-of-the-box
    llm = OpenAI(api_token=together_api_key, model="gpt-3.5-turbo")
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": False})

    # Get response (may be text or a plot, depending on the question)
    result = sdf.chat(question)

    # If you want to handle charts, extend here (for now just text)
    return str(result), None
