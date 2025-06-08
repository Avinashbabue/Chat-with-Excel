{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ddecea6a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# app.py\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "from utils import read_excel, ask_gemini\n",
    "\n",
    "st.set_page_config(page_title=\"Excel Chatbot\", layout=\"wide\")\n",
    "st.title(\"📊 Excel Chatbot using Gemini\")\n",
    "\n",
    "uploaded_file = st.file_uploader(\"Upload an Excel file (.xlsx)\", type=\"xlsx\")\n",
    "\n",
    "if uploaded_file:\n",
    "    df = read_excel(uploaded_file)\n",
    "    st.success(\"✅ File loaded successfully!\")\n",
    "    st.dataframe(df.head(10))\n",
    "\n",
    "    question = st.text_input(\"Ask something about this data...\")\n",
    "\n",
    "    if question:\n",
    "        if any(word in question.lower() for word in [\"chart\", \"plot\", \"graph\", \"visual\"]):\n",
    "            col = st.selectbox(\"Choose a column to visualize:\", df.columns)\n",
    "            chart = px.histogram(df, x=col, title=f\"Chart of {col}\")\n",
    "            st.plotly_chart(chart)\n",
    "        else:\n",
    "            with st.spinner(\"Thinking...\"):\n",
    "                answer = ask_gemini(df, question)\n",
    "                st.markdown(f\"**Answer:**\\n\\n{answer}\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
