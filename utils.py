# utils.py
import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

def read_excel(uploaded_file):
    return pd.read_excel(uploaded_file)

def ask_gemini(df, question):
    preview = df.head(15).to_markdown()
    prompt = f"""You are an intelligent data analyst. Analyze the table below:\n\n{preview}\n\nQuestion: {question}"""
    response = model.generate_content(prompt)
    return response.text
