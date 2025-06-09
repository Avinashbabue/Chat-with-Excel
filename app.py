# app.py
import streamlit as st
import pandas as pd
from utils import read_excel, run_pandasai

st.set_page_config(page_title="Excel Insight Assistant", layout="wide")
st.title("📊 Chat with Excel")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel (.xlsx) file", type=["xlsx"])

if uploaded_file:
    try:
        df = read_excel(uploaded_file)
        st.subheader("🔍 Preview of Your Data")
        st.dataframe(df.head(10), use_container_width=True)

        # Input question
        question = st.text_input("Ask something about this data...")
        if question:
            with st.spinner("Thinking..."):
                response, chart = run_pandasai(df, question)
                st.subheader("🧠 Answer")
                st.markdown(response)

                if chart:
                    st.plotly_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
