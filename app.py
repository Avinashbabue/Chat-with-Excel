# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import read_excel, ask_gemini

st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title("📊 Excel Chatbot using Gemini")

uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    df = read_excel(uploaded_file)
    st.success("✅ File loaded successfully!")
    st.dataframe(df.head(10))

    question = st.text_input("Ask something about this data...")

    if question:
        if any(word in question.lower() for word in ["chart", "plot", "graph", "visual"]):
            col = st.selectbox("Choose a column to visualize:", df.columns)
            chart = px.histogram(df, x=col, title=f"Chart of {col}")
            st.plotly_chart(chart)
        else:
            with st.spinner("Thinking..."):
                answer = ask_gemini(df, question)
                st.markdown(f"**Answer:**\n\n{answer}")
