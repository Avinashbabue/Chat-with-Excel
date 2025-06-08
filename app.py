import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import read_excel, ask_gemini, fill_missing_values  # Make sure fill_missing_values is imported

st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title("📊 Chat with Excel)")

uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    df = read_excel(uploaded_file)
    df_clean = fill_missing_values(df)  # Make sure to fill missing values for charting
    st.success("✅ File loaded successfully!")
    st.dataframe(df_clean.head(10))  # Show more context

    question = st.text_input("Ask a question about your data:")

    if question:
        with st.spinner("Thinking..."):
            answer = ask_gemini(df, question)

        try:
            parsed = json.loads(answer)
            st.markdown(f"**Answer:** {parsed.get('answer')}")
            chart_type = parsed.get("chart_type", "").lower()
            x = parsed.get("x")
            y = parsed.get("y")

            chart = None
            if chart_type and x and x in df_clean.columns:
                if chart_type == "bar" and y and y in df_clean.columns:
                    chart = px.bar(df_clean, x=x, y=y, title=f"Bar Chart of {y} by {x}")
                elif chart_type == "histogram":
                    chart = px.histogram(df_clean, x=x, title=f"Histogram of {x}")
                elif chart_type == "line" and y and y in df_clean.columns:
                    chart = px.line(df_clean, x=x, y=y, title=f"Line Chart of {y} over {x}")
                elif chart_type == "pie":
                    chart = px.pie(df_clean, names=x, title=f"Pie Chart of {x}")
                elif chart_type == "scatter" and y and y in df_clean.columns:
                    chart = px.scatter(df_clean, x=x, y=y, title=f"Scatter Plot of {y} vs {x}")
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("No valid chart could be generated with the specified columns.")
        except Exception:
            st.markdown(f"**Answer:**\n\n{answer}")

    st.caption("Note: This assistant works with any Excel schema, no hardcoded columns. Try asking for summaries, filters, groupings, or trends!")

else:
    st.info("Please upload an Excel file to get started.")
