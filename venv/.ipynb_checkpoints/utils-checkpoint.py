{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "01780430",
   "metadata": {},
   "outputs": [],
   "source": [
    "# utils.py\n",
    "import os\n",
    "import pandas as pd\n",
    "from dotenv import load_dotenv\n",
    "import google.generativeai as genai\n",
    "\n",
    "# Load API key\n",
    "load_dotenv()\n",
    "api_key = os.getenv(\"GEMINI_API_KEY\")\n",
    "genai.configure(api_key=api_key)\n",
    "\n",
    "# Load Gemini model\n",
    "model = genai.GenerativeModel(\"gemini-pro\")\n",
    "\n",
    "def read_excel(uploaded_file):\n",
    "    return pd.read_excel(uploaded_file)\n",
    "\n",
    "def ask_gemini(df, question):\n",
    "    preview = df.head(15).to_markdown()\n",
    "    prompt = f\"\"\"You are an intelligent data analyst. Analyze the table below:\\n\\n{preview}\\n\\nQuestion: {question}\"\"\"\n",
    "    response = model.generate_content(prompt)\n",
    "    return response.text\n"
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
