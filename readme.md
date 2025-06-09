# Excel Insight Assistant (Streamlit + PandasAI + Together AI)

A conversational Excel data analysis assistant that lets you upload Excel files (`.xlsx`), ask natural language questions about your data, and get insightful answers (including visualizations!).  
Powered by [PandasAI](https://github.com/gventuri/pandas-ai) and Together AI's GPT-3.5-turbo API for LLM-backed reasoning.

---

## 🚀 Features

- **Automatic Excel header detection:** Handles messy or irregular Excel files.
- **Column name cleaning:** Automatically normalizes and cleans column names for easier querying.
- **Natural language Q&A:** Ask questions like "Show average sales by region" or "Plot age distribution".
- **Visualization support:** Returns answers and (optionally) direct visualizations with Plotly.
- **Together AI API integration:** Uses your Together API key to access GPT-3.5-turbo for cost-effective, scalable LLM inference.
- **Powered by PandasAI:** Leverages SmartDataframe for context-aware data analysis.

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/excel-insight-assistant.git
cd excel-insight-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your Together API Key

- Create a `.env` file in the project root:

  ```
  TOGETHER_API_KEY=your_together_api_key_here
  ```

- Or set the environment variable in your shell/session:

  ```bash
  export TOGETHER_API_KEY=your_together_api_key_here
  ```

---

## 🏃‍♂️ Usage

```bash
streamlit run app.py
```

- Open your browser to the displayed Streamlit URL.
- Upload an Excel file (`.xlsx`).
- Ask natural language questions about your data.
- View answers and visualizations!

---

## 📁 Project Structure

```
.
├── app.py          # Streamlit UI logic
├── utils.py        # Excel reading, cleaning, and PandasAI query logic
├── requirements.txt
└── README.md
```

---

## 💡 Example Questions

- What is the average income?
- How many rows have age > 30?
- Show sales distribution by product category.
- Compare revenue between regions.
- Plot age distribution as a histogram.

---

## ⚙️ How it Works

- **Excel file upload:** Reads the Excel file, auto-detects the header, cleans up columns.
- **Natural language query:** Your question is sent (with cleaned data) to PandasAI, which uses your Together API key to call GPT-3.5-turbo.
- **Answer & visualization:** The assistant parses the LLM response and renders text and/or charts using Plotly.

---

## 🧩 Dependencies

- `streamlit`
- `pandas`
- `pandasai`
- `python-dotenv`
- `plotly`
- `openpyxl`

---

## 🌐 Deployment

You can run this locally, or deploy on platforms that support custom Python/Streamlit apps (with environment variable support, e.g., Hugging Face Spaces, private cloud, etc.). **Note:**  
- Do **not** use Streamlit Cloud free tier for models requiring more than 800MB RAM or external API keys.
- For Hugging Face Spaces, set your secrets in the Space's "Secrets" section for secure API key handling.

---

## 🔒 Security

- Your Together API Key is required to access the LLM.
- Never commit your API key to public repositories.

---

## 📜 License

MIT License

---

## 🙏 Acknowledgements

- [PandasAI](https://github.com/gventuri/pandas-ai) — Natural language dataframe analysis
- [Together AI](https://www.together.ai/) — Fast, scalable open-source LLM APIs

---

**Enjoy conversational Excel analytics!**
