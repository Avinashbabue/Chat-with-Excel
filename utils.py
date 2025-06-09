import os
import re
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (TOGETHER_API_KEY)
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def read_excel(uploaded_file):
    """
    Reads an Excel file, auto-detects the header row,
    cleans empty rows/columns, and normalizes column names.
    """
    raw_df = pd.read_excel(uploaded_file, sheet_name=0, header=None)


    header_row = None
    for i, row in raw_df.iterrows():
        non_null_count = row.count()
        string_count = row.apply(lambda x: isinstance(x, str)).sum()
        
        if string_count >= 2 and non_null_count >= len(row) / 2:
            header_row = i
            break

    if header_row is None:
        raise ValueError("Could not find a valid header row in the Excel file.")

    
    df = pd.read_excel(uploaded_file, sheet_name=0, header=header_row)

   
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    
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
    llm = OpenAI(api_token=together_api_key, model="gpt-3.5-turbo")
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": False})
    result = sdf.chat(question)
    return str(result), None
