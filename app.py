import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import read_excel, ask_gemini

st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title("📊 Excel Chatbot for Excel-Based Insights (NeoStats)")

uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    df = read_excel(uploaded_file)
    st.success("✅ File loaded successfully!")
    st.dataframe(df.head(10))

    question = st.text_input("Ask a question about your data:")

    if question:
        with st.spinner("Thinking..."):
            answer = ask_gemini(df, question)

        # Try to parse if Gemini returned a chart instruction
        try:
            parsed = json.loads(answer)
            st.markdown(f"**Answer:** {parsed.get('answer')}")
            chart_type = parsed.get("chart_type", "").lower()
            x = parsed.get("x")
            y = parsed.get("y")

            if chart_type and x:
                if chart_type == "bar":
                    chart = px.bar(df, x=x, y=y, title=f"{chart_type.title()} Chart")
                elif chart_type == "histogram":
                    chart = px.histogram(df, x=x, title=f"Histogram of {x}")
                elif chart_type == "line" and y:
                    chart = px.line(df, x=x, y=y, title=f"Line Chart of {y} over {x}")
                elif chart_type == "pie":
                    chart = px.pie(df, names=x, title=f"Pie Chart of {x}")
                elif chart_type == "scatter" and y:
                    chart = px.scatter(df, x=x, y=y, title=f"Scatter Plot of {y} vs {x}")
                else:
                    chart = None
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
        except Exception:
            # If not JSON or chart, just show answer as text
            st.markdown(f"**Answer:**\n\n{answer}")

    st.caption("Note: This assistant works with any Excel schema, no hardcoded columns. Try asking for summaries, filters, groupings, or trends!")

else:
    st.info("Please upload an Excel file to get started.")
